#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
detector_ptbr.py: portão determinístico de "sotaque de IA" em português do Brasil.

Uso:
    python3 detector_ptbr.py arquivo.md [--json] [--min-gravidade baixa|media|alta|critica]
                                        [--limite N] [--padroes caminho.json]

Porte adaptado de conorbronsdon/avoid-ai-writing (detector/patterns.js) pra PT-BR,
com os 10 tells da skill escrita-humana-reconecta e uma categoria nova de calques.

Como o score funciona (documentado também no README):
    1. Cada achado tem um peso pela gravidade (baixa 1, média 2.5, alta 5, crítica 10),
       lido do padroes_ptbr.json. Métricas estatísticas têm peso próprio.
    2. Mesmo padrão + mesmo texto repetido: a primeira ocorrência vale peso cheio, as
       seguintes valem peso x fator_extra (0.4). A soma de um padrão nunca passa do teto (20).
       Isso porta a deduplicação do original sem zerar a repetição, que em PT-BR é o tell.
    3. densidade = pontos / max(palavras, 300) * 1000. O original normaliza por
       log2(palavras/50); aqui a normalização é por densidade porque capítulo de ebook tem
       1.500 a 5.000 palavras e o log2 achatava demais texto longo. O piso de 300 palavras
       impede que um box curto vire 50 por causa de um achado só.
    4. score = 100 * (1 - exp(-densidade / k)), k = 50. Saturante: densidade 50 dá ~63,
       densidade 115 dá ~90. Nota por categoria usa a mesma curva com k = 15 sobre a
       densidade só daquela categoria.

Guardas de falso positivo: ignora front matter YAML, blocos e spans de código, comentários
HTML, tabelas markdown, blockquotes, URLs, citações entre aspas com 5+ palavras (fala
transcrita) e títulos curtos (até 8 palavras) na varredura de prosa.
"""

import argparse
import json
import math
import os
import re
import statistics
import sys
from collections import Counter, defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
PADROES_PADRAO = os.path.join(AQUI, "padroes_ptbr.json")
ORDEM_GRAVIDADE = {"baixa": 0, "media": 1, "alta": 2, "critica": 3}

# Palavra: letras (com acento), opcionalmente com apóstrofo ou hífen interno.
RE_PALAVRA = re.compile(r"[^\W\d_]+(?:['’-][^\W\d_]+)*")
# Frase: tudo até um terminador (. ! ? …), mais aspas/parêntese de fechamento.
RE_FRASE = re.compile(r"[^.!?…]+(?:[.!?…]+[\"'”’)\]]*)?")
RE_LINHA_LISTA = re.compile(r"^[ \t]*(?:[-*+•]|\d{1,3}[.)])[ \t]+(.+)$")
RE_TITULO = re.compile(r"^[ \t]{0,3}#{1,6}[ \t]+(.*?)[ \t]*$", re.M)
# Verbo/auxiliar mais comum em item de lista; se não aparece, o item é sintagma nominal.
RE_TEM_VERBO = re.compile(
    r"\b(?:é|são|está|estão|foi|era|tem|têm|há|pode|podem|deve|devem|vai|vão|faz|fazem|"
    r"fica|ficam|precisa|precisam|use|faça|evite|não|nunca|sempre|quando|se|porque)\b",
    re.I,
)
RE_TRIADE = re.compile(
    r"\b([^\W\d_]+(?:\s[^\W\d_]+){0,2}),\s([^\W\d_]+(?:\s[^\W\d_]+){0,2})\se\s([^\W\d_]+(?:\s[^\W\d_]+){0,2})\b"
)


# ─────────────────────────────────────────────────────────────────────────────
# Carregamento dos padrões
# ─────────────────────────────────────────────────────────────────────────────

def carregar_padroes(caminho):
    """Lê o JSON e compila todos os regex uma vez só."""
    with open(caminho, encoding="utf-8") as f:
        cfg = json.load(f)

    def compilar(rx, flags_txt=""):
        flags = re.I | re.U
        if "m" in flags_txt:
            flags |= re.M
        if "s" in flags_txt:
            flags |= re.S
        return re.compile(rx, flags)

    for p in cfg["padroes"]:
        p["_rx"] = compilar(p["regex"], p.get("flags", ""))
    for nivel in ("nivel1", "nivel2", "nivel3"):
        for v in cfg["vocabulario"][nivel]:
            v["_rx"] = compilar(v["regex"])
    cfg["metricas"]["fechos_grandiosos"]["_rx_abstratos"] = re.compile(
        r"\b(?:" + cfg["metricas"]["fechos_grandiosos"]["abstratos"] + r")\b", re.I
    )
    return cfg


# ─────────────────────────────────────────────────────────────────────────────
# Máscaras (preservam índice: cada char apagado vira espaço, \n fica)
# ─────────────────────────────────────────────────────────────────────────────

def mascarar(texto):
    """
    Devolve (prosa, titulos, info):
      prosa   = texto com tudo que não é prosa do autor apagado (índices preservados)
      titulos = texto com SÓ as linhas de título visíveis (pra padrões de escopo 'titulos')
      info    = contagem do que foi mascarado
    """
    chars = list(texto)
    info = Counter()

    def apagar(a, b):
        for i in range(a, b):
            if chars[i] != "\n":
                chars[i] = " "

    m = re.match(r"\A﻿?---[ \t]*\n.*?\n---[ \t]*(?:\n|\Z)", texto, re.S)
    if m:
        apagar(0, m.end())
        info["frontmatter"] += 1

    for m in re.finditer(r"^[ \t]{0,3}(`{3,}|~{3,})[^\n]*\n.*?^[ \t]{0,3}\1[ \t]*$", texto, re.S | re.M):
        apagar(m.start(), m.end())
        info["blocos_codigo"] += 1

    for m in re.finditer(r"`[^`\n]+`", texto):
        apagar(m.start(), m.end())
        info["codigo_inline"] += 1

    for m in re.finditer(r"<!--.*?-->", texto, re.S):
        apagar(m.start(), m.end())
        info["comentarios_html"] += 1

    for m in re.finditer(r"https?://\S+|www\.\S+", texto):
        apagar(m.start(), m.end())
        info["urls"] += 1

    for m in re.finditer(r"^[ \t]*\|.*$", texto, re.M):
        apagar(m.start(), m.end())
        info["linhas_tabela"] += 1

    for m in re.finditer(r"^[ \t]*>.*$", texto, re.M):
        apagar(m.start(), m.end())
        info["linhas_blockquote"] += 1

    # Blocos de script e de diagrama do manuscrito (:::frase, :::cena, :::evite, :::grafico).
    # São texto literal das fontes ou conteúdo de quadro, não prosa do autor: o detector não
    # deve cobrar deles ritmo, placeholder nem hedge. :::punch e :::pergunta FICAM, porque
    # são frases escritas pelo autor. Apagar preservando índices mantém as densidades corretas.
    for m in re.finditer(r"^:::(frase|cena|evite|grafico|caso)[^\n]*\n.*?^:::[ \t]*$", texto, re.S | re.M):
        apagar(m.start(), m.end())
        info["blocos_script"] += 1

    # Marcador de bloco solto (:::punch / :::pergunta): some a linha do marcador, fica o conteúdo.
    for m in re.finditer(r"^:::[^\n]*$", texto, re.M):
        apagar(m.start(), m.end())
        info["marcadores_bloco"] += 1

    # Citação entre aspas com 5+ palavras: fala transcrita de paciente, print de WhatsApp,
    # frase pronta de script. Não é prosa do autor.
    rx_aspas = re.compile(r"\"([^\"\n]{1,600})\"|“([^”\n]{1,600})”|«([^»\n]{1,600})»")
    for m in re.finditer(rx_aspas, texto):
        interior = next(g for g in m.groups() if g is not None)
        if len(RE_PALAVRA.findall(interior)) >= 5:
            apagar(m.start(), m.end())
            info["citacoes"] += 1

    # Títulos curtos saem da varredura de prosa; ficam numa cópia só de títulos.
    so_titulos = [" " if c != "\n" else "\n" for c in texto]
    for m in RE_TITULO.finditer(texto):
        for i in range(m.start(), m.end()):
            so_titulos[i] = texto[i]
        if len(RE_PALAVRA.findall(m.group(1))) <= 8:
            apagar(m.start(), m.end())
            info["titulos_curtos"] += 1

    return "".join(chars), "".join(so_titulos), info


# ─────────────────────────────────────────────────────────────────────────────
# Segmentação
# ─────────────────────────────────────────────────────────────────────────────

def paragrafos_de(prosa):
    """Lista de dicts {inicio, fim, texto} pra cada parágrafo com pelo menos uma palavra."""
    saida = []
    for m in re.finditer(r"(?:[^\n]*\S[^\n]*\n?)+", prosa):
        bloco = m.group(0)
        if RE_PALAVRA.search(bloco):
            saida.append({"inicio": m.start(), "fim": m.end(), "texto": bloco})
    return saida


def frases_de(texto, base=0):
    """Frases (com offset absoluto) de um trecho; só frases com pelo menos 1 palavra."""
    saida = []
    for m in RE_FRASE.finditer(texto):
        t = m.group(0)
        if not RE_PALAVRA.search(t):
            continue
        esq = len(t) - len(t.lstrip())
        saida.append({
            "inicio": base + m.start() + esq,
            "fim": base + m.end(),
            "texto": t.strip(),
            "palavras": RE_PALAVRA.findall(t),
        })
    return saida


def linha_de(texto, pos):
    return texto.count("\n", 0, pos) + 1


def trecho_em(texto, inicio, fim, margem=90):
    """Frase (ou janela) do texto ORIGINAL em volta do achado, com o achado entre « »."""
    a = max(0, inicio - margem)
    b = min(len(texto), fim + margem)
    # Encosta nos limites de frase/linha mais próximos dentro da margem.
    m = re.search(r"[.!?\n][^.!?\n]*$", texto[a:inicio])
    if m:
        a = a + m.start() + 1
    m = re.search(r"[.!?\n]", texto[fim:b])
    if m:
        b = fim + m.end()
    pedaco = texto[a:inicio] + "«" + texto[inicio:fim] + "»" + texto[fim:b]
    return re.sub(r"\s+", " ", pedaco).strip()


# ─────────────────────────────────────────────────────────────────────────────
# Achados
# ─────────────────────────────────────────────────────────────────────────────

def novo_achado(cfg, id_, categoria, subtipo, gravidade, texto, inicio, fim, explicacao, sugestao, peso=None):
    return {
        "id": id_,
        "categoria": categoria,
        "subtipo": subtipo,
        "gravidade": gravidade,
        "peso": cfg["pesos_gravidade"][gravidade] if peso is None else peso,
        "texto": texto,
        "inicio": inicio,
        "fim": fim,
        "explicacao": explicacao,
        "sugestao": sugestao,
    }


def rodar_padroes(cfg, prosa, titulos):
    achados = []
    for p in cfg["padroes"]:
        alvo = titulos if p.get("escopo") == "titulos" else prosa
        for m in p["_rx"].finditer(alvo):
            bruto = m.group(0)
            if not bruto.strip():
                continue
            esq = len(bruto) - len(bruto.lstrip())
            dir_ = len(bruto) - len(bruto.rstrip())
            achados.append(novo_achado(
                cfg, p["id"], p["categoria"], p["subtipo"], p["gravidade"],
                bruto.strip(), m.start() + esq, m.end() - dir_, p["explicacao"], p["substituto"],
            ))
    return achados


def rodar_vocabulario(cfg, prosa, paragrafos, n_palavras):
    achados = []
    voc = cfg["vocabulario"]
    regras = cfg["regras_vocabulario"]

    # Nível 1: sempre marca.
    for v in voc["nivel1"]:
        for m in v["_rx"].finditer(prosa):
            achados.append(novo_achado(
                cfg, v["id"], "linguagem", "vocabulario_n1", "alta", m.group(0), m.start(), m.end(),
                "Vocabulário de IA (nível 1: sempre marca).", v["substituto"],
            ))

    # Nível 2: só quando 2+ termos distintos caem no mesmo parágrafo.
    minimo = regras["nivel2_min_distintos_paragrafo"]
    for par in paragrafos:
        vistos = []
        for v in voc["nivel2"]:
            m = v["_rx"].search(par["texto"])
            if m:
                vistos.append((v, m))
        if len(vistos) >= minimo:
            nomes = ", ".join(v["termo"] for v, _ in vistos)
            for v, m in vistos:
                achados.append(novo_achado(
                    cfg, v["id"], "linguagem", "vocabulario_n2", "media", m.group(0),
                    par["inicio"] + m.start(), par["inicio"] + m.end(),
                    f"Vocabulário de IA nível 2 em cluster ({len(vistos)} no mesmo parágrafo: {nomes}).",
                    v["substituto"],
                ))

    # Nível 3: só por densidade.
    min_oc = regras["nivel3_min_ocorrencias"]
    min_mil = regras["nivel3_min_por_mil"]
    for v in voc["nivel3"]:
        ocorr = list(v["_rx"].finditer(prosa))
        n = len(ocorr)
        if n >= min_oc and n / max(n_palavras, 1) * 1000 >= min_mil:
            peso = min(6.0, 1 + 0.5 * (n - min_oc))
            achados.append(novo_achado(
                cfg, v["id"], "linguagem", "vocabulario_n3", "baixa", f"{v['termo']} x{n}",
                ocorr[0].start(), ocorr[0].end(),
                f"Palavra comum usada demais ({n} vezes em {n_palavras} palavras).",
                v["substituto"], peso=peso,
            ))
    return achados


# ─────────────────────────────────────────────────────────────────────────────
# Métricas estatísticas e estruturais
# ─────────────────────────────────────────────────────────────────────────────

def cv(valores):
    if len(valores) < 2:
        return 0.0
    m = statistics.mean(valores)
    return statistics.pstdev(valores) / m if m else 0.0


def rodar_metricas(cfg, texto, prosa, paragrafos, frases, n_palavras, achados_regex):
    """Devolve (achados, numeros). `numeros` vai cru pro relatório, mesmo sem achado."""
    M = cfg["metricas"]
    achados = []
    num = {}
    por_mil = lambda n: round(n / max(n_palavras, 1) * 1000, 2)

    # 1. Ritmo de metrônomo: desvio-padrão do tamanho das frases.
    c = M["ritmo_metronomo"]
    tam = [len(f["palavras"]) for f in frases if len(f["palavras"]) >= 2]
    if len(tam) >= c["min_frases"]:
        media = statistics.mean(tam)
        v = cv(tam)
        num["frases_media_palavras"] = round(media, 1)
        num["frases_desvio_padrao"] = round(statistics.pstdev(tam), 1)
        num["frases_cv"] = round(v, 2)
        if media >= c["min_media_palavras"] and v < c["cv_media"]:
            grav, peso = ("alta", c["peso_alta"]) if v < c["cv_alta"] else ("media", c["peso_media"])
            achados.append(novo_achado(
                cfg, "m_ritmo_metronomo", c["categoria"], "ritmo", grav,
                f"frases com ~{media:.0f} palavras (CV {v:.2f})", frases[0]["inicio"], frases[0]["fim"],
                c["explicacao"], "Quebre: uma frase de três palavras. Depois uma longa, que respira.", peso=peso,
            ))

    # 2. Parágrafos do mesmo tamanho.
    c = M["paragrafos_uniformes"]
    tp = [len(RE_PALAVRA.findall(p["texto"])) for p in paragrafos]
    grandes = [t for t in tp if t >= c["min_palavras_paragrafo"]]
    num["paragrafos"] = len(paragrafos)
    if len(grandes) >= c["min_paragrafos"]:
        med = statistics.median(grandes)
        dentro = sum(1 for t in grandes if abs(t - med) <= c["tolerancia"] * med)
        prop = dentro / len(grandes)
        num["paragrafos_mediana_palavras"] = med
        num["paragrafos_proporcao_mesmo_tamanho"] = round(prop, 2)
        if prop >= c["proporcao_minima"]:
            achados.append(novo_achado(
                cfg, "m_paragrafos_uniformes", c["categoria"], "ritmo", "media",
                f"{dentro} de {len(grandes)} parágrafos com ~{med:.0f} palavras", paragrafos[0]["inicio"],
                paragrafos[0]["fim"], c["explicacao"], "Varie: um parágrafo de uma linha, outro que se estende.",
                peso=c["peso"],
            ))

    # 3. Todos os parágrafos com o mesmo número de frases.
    c = M["paragrafos_mesmas_frases"]
    nf = [len(frases_de(p["texto"])) for p in paragrafos]
    if len(nf) >= c["min_paragrafos"]:
        media = statistics.mean(nf)
        if media >= c["min_media_frases"] and all(abs(n - media) <= 1 for n in nf):
            achados.append(novo_achado(
                cfg, "m_paragrafos_mesmas_frases", c["categoria"], "ritmo", "baixa",
                f"todos os parágrafos com ~{media:.0f} frases", paragrafos[0]["inicio"], paragrafos[0]["fim"],
                c["explicacao"], "Varie o tamanho dos parágrafos de propósito.", peso=c["peso"],
            ))

    # 4. Ritmo entre parágrafos (burstiness): variação da variação.
    c = M["ritmo_entre_paragrafos"]
    cvs = []
    for p in paragrafos:
        fs = [len(f["palavras"]) for f in frases_de(p["texto"]) if len(f["palavras"]) >= 2]
        if len(fs) >= c["min_frases_paragrafo"]:
            cvs.append(cv(fs))
    if len(cvs) >= c["min_paragrafos"]:
        desvio = statistics.pstdev(cvs)
        num["ritmo_entre_paragrafos_desvio"] = round(desvio, 3)
        if desvio < c["desvio_max"] and statistics.mean(cvs) < c["cv_medio_max"]:
            achados.append(novo_achado(
                cfg, "m_ritmo_entre_paragrafos", c["categoria"], "ritmo", "media",
                f"cadência igual em {len(cvs)} parágrafos (desvio {desvio:.2f})", paragrafos[0]["inicio"],
                paragrafos[0]["fim"], c["explicacao"], "Um parágrafo seco ao lado de um que divaga.", peso=c["peso"],
            ))

    # 5. Densidade de pontuação uniforme entre parágrafos.
    c = M["pontuacao_uniforme"]
    dens = []
    for p in paragrafos:
        w = len(RE_PALAVRA.findall(p["texto"]))
        if w >= c["min_palavras_paragrafo"]:
            dens.append(len(re.findall(r"[,;:()\u2014]", p["texto"])) / w)
    if len(dens) >= c["min_paragrafos"]:
        v = cv(dens)
        num["pontuacao_cv"] = round(v, 2)
        if v < c["cv_max"] and statistics.mean(dens) >= c["media_min"]:
            achados.append(novo_achado(
                cfg, "m_pontuacao_uniforme", c["categoria"], "ritmo", "baixa",
                f"pontuação uniforme entre parágrafos (CV {v:.2f})", paragrafos[0]["inicio"], paragrafos[0]["fim"],
                c["explicacao"], "Parágrafo denso de vírgula ao lado de parágrafo seco.", peso=c["peso"],
            ))

    # 6. Diversidade lexical (TTR), só em texto longo e só quando muito baixa.
    c = M["diversidade_lexical"]
    tokens = [w.lower() for w in RE_PALAVRA.findall(prosa)]
    if len(tokens) >= c["min_tokens"]:
        ttr = len(set(tokens)) / len(tokens)
        num["ttr"] = round(ttr, 3)
        if ttr < c["ttr_max"]:
            achados.append(novo_achado(
                cfg, "m_diversidade_lexical", c["categoria"], "vocabulario", "baixa",
                f"TTR {ttr:.2f} ({len(set(tokens))} palavras distintas em {len(tokens)})", 0, 0,
                c["explicacao"], "Varie substantivo e verbo, ou confira se o tema pede a repetição.", peso=c["peso"],
            ))

    # 7. Anáfora: 3+ frases seguidas com o mesmo começo.
    c = M["anafora"]
    stop = set(c["stoplist"])
    iguais_ao_anterior = 0
    i = 0
    seq = [f for f in frases if f["palavras"]]
    while i < len(seq):
        j = i
        w1 = seq[i]["palavras"][0].lower()
        big = " ".join(x.lower() for x in seq[i]["palavras"][:2])
        while j + 1 < len(seq):
            nxt = seq[j + 1]
            nw1 = nxt["palavras"][0].lower()
            nbig = " ".join(x.lower() for x in nxt["palavras"][:2])
            mesma_palavra = nw1 == w1 and w1 not in stop and len(w1) >= 3
            mesmo_bigrama = nbig == big and len(nxt["palavras"]) >= 2
            if mesma_palavra or mesmo_bigrama:
                j += 1
            else:
                break
        run = j - i + 1
        if run >= c["min_frases_sequencia"]:
            achados.append(novo_achado(
                cfg, "m_anafora", c["categoria"], "anafora", "media",
                f"{run} frases seguidas começando com «{' '.join(seq[i]['palavras'][:2])}»",
                seq[i]["inicio"], seq[j]["fim"], c["explicacao"], "Deixe uma; reescreva as outras com outro começo.",
                peso=c["peso"],
            ))
        i = j + 1
    for a, b in zip(seq, seq[1:]):
        if a["palavras"][0].lower() == b["palavras"][0].lower():
            iguais_ao_anterior += 1
    num["frases_mesmo_inicio_proporcao"] = round(iguais_ao_anterior / max(len(seq) - 1, 1), 2)

    # 8. Travessão: já vem do padrão es_travessao; aqui só a densidade.
    n_trav = sum(1 for a in achados_regex if a["id"] == "es_travessao")
    num["travessoes"] = n_trav
    num["travessoes_por_mil"] = por_mil(n_trav)

    # 9. Dois-pontos no meio da frase.
    c = M["dois_pontos"]
    dp = [m for m in re.finditer(r"(?<=[^\W\d_\s]):\s", prosa)]
    num["dois_pontos"] = len(dp)
    num["dois_pontos_por_mil"] = por_mil(len(dp))
    if len(dp) >= c["min_ocorrencias"] and por_mil(len(dp)) > c["max_por_mil"]:
        achados.append(novo_achado(
            cfg, "m_dois_pontos", c["categoria"], "pontuacao", "media",
            f"{len(dp)} dois-pontos em {n_palavras} palavras", dp[0].start(), dp[0].end(),
            c["explicacao"], "Troque por ponto ou vírgula; deixe só os que apresentam algo.", peso=c["peso"],
        ))

    # 10. Listas: proporção de linhas em lista, e lista de sintagmas sem verbo.
    c = M["listas"]
    linhas = prosa.split("\n")
    nao_vazias = [l for l in linhas if l.strip()]
    itens = [(idx, RE_LINHA_LISTA.match(l)) for idx, l in enumerate(linhas)]
    itens = [(idx, m) for idx, m in itens if m]
    num["itens_lista"] = len(itens)
    num["proporcao_linhas_em_lista"] = round(len(itens) / max(len(nao_vazias), 1), 2)
    if len(itens) >= c["min_itens"] and num["proporcao_linhas_em_lista"] >= c["proporcao_max"]:
        pos = sum(len(l) + 1 for l in linhas[: itens[0][0]])
        achados.append(novo_achado(
            cfg, "m_listas", c["categoria"], "lista", "media",
            f"{len(itens)} itens de lista em {len(nao_vazias)} linhas", pos, pos + len(linhas[itens[0][0]]),
            c["explicacao"], "Texto de gente anda em parágrafo. Lista só quando a estrutura pede.", peso=c["peso"],
        ))
    # Sequências de itens curtos sem verbo.
    run, run_ini = [], None
    def fechar_run():
        if len(run) >= c["np_min_itens"]:
            curtos = [t for t in run if 0 < len(RE_PALAVRA.findall(t)) <= c["np_max_palavras"] and not RE_TEM_VERBO.search(t)]
            if len(curtos) >= c["np_min_itens"] and len(curtos) / len(run) >= 0.75:
                pos = sum(len(l) + 1 for l in linhas[:run_ini])
                achados.append(novo_achado(
                    cfg, "m_lista_sintagmas", c["categoria"], "lista", "alta",
                    f"{len(run)} itens curtos sem verbo em sequência", pos, pos + len(linhas[run_ini]),
                    "Lista de sintagmas nominais: andaime de IA.", "Vire parágrafo ou dê verbo a cada item.",
                    peso=c["np_peso"],
                ))
    brancas = 0
    for idx, l in enumerate(linhas):
        m = RE_LINHA_LISTA.match(l)
        if m:
            if not run:
                run_ini = idx
            run.append(m.group(1).strip())
            brancas = 0
        elif not l.strip():
            brancas += 1
            if brancas >= 2:
                fechar_run(); run, run_ini = [], None
        else:
            fechar_run(); run, run_ini = [], None
    fechar_run()

    # 11. Negrito.
    c = M["negrito"]
    neg = list(re.finditer(r"\*\*[^*\n]+\*\*|__[^_\n]+__", prosa))
    num["negritos"] = len(neg)
    limite = max(c["minimo_absoluto"], n_palavras // c["palavras_por_negrito"])
    if len(neg) > limite:
        grav, peso = ("alta", c["peso_alta"]) if len(neg) > 2 * limite else ("media", c["peso_media"])
        achados.append(novo_achado(
            cfg, "m_negrito", c["categoria"], "formatacao", grav,
            f"{len(neg)} trechos em negrito em {n_palavras} palavras", neg[0].start(), neg[0].end(),
            c["explicacao"], "Tire o negrito da maioria; se importa, lidere a frase com aquilo.", peso=peso,
        ))

    # 12. Tríades "X, Y e Z".
    c = M["triades"]
    tri = list(RE_TRIADE.finditer(prosa))
    num["triades"] = len(tri)
    num["triades_por_mil"] = por_mil(len(tri))
    if len(tri) >= c["min_ocorrencias"] and por_mil(len(tri)) >= c["min_por_mil"]:
        exemplos = "; ".join(m.group(0) for m in tri[:3])
        achados.append(novo_achado(
            cfg, "m_triades", c["categoria"], "triade", "media",
            f"{len(tri)} tríades ({exemplos})", tri[0].start(), tri[0].end(),
            c["explicacao"], "Use dois itens, quatro, ou uma frase inteira.", peso=c["peso"],
        ))

    # 13. Contrastes em série (os individuais já vieram dos padrões).
    c = M["contrastes_em_serie"]
    contr = [a for a in achados_regex if a["subtipo"] == "contraste"]
    num["contrastes"] = len(contr)
    if len(contr) >= c["min_ocorrencias"]:
        achados.append(novo_achado(
            cfg, "m_contrastes_em_serie", c["categoria"], "contraste", "alta",
            f"{len(contr)} contrastes 'não é X, é Y' no texto", contr[0]["inicio"], contr[0]["fim"],
            c["explicacao"], "Deixe no máximo um, e só se revelar algo.", peso=c["peso"],
        ))

    # 14. Parágrafo fechando em pergunta.
    c = M["perguntas_fim_paragrafo"]
    fim_perg = [p for p in paragrafos if p["texto"].rstrip().endswith("?")]
    num["paragrafos_terminando_em_pergunta"] = len(fim_perg)
    prop = len(fim_perg) / max(len(paragrafos), 1)
    if len(fim_perg) >= c["min_ocorrencias"] and prop >= c["proporcao_min"]:
        achados.append(novo_achado(
            cfg, "m_perguntas_fim", c["categoria"], "pergunta_retorica", "media",
            f"{len(fim_perg)} de {len(paragrafos)} parágrafos terminam em pergunta", fim_perg[0]["inicio"],
            fim_perg[0]["fim"], c["explicacao"], "Responda a pergunta ou corte; termine direto.", peso=c["peso"],
        ))

    # 15. Fecho grandioso: última frase curta, abstrata, sem número.
    c = M["fechos_grandiosos"]
    fechos = []
    for p in paragrafos:
        fs = frases_de(p["texto"], p["inicio"])
        if len(fs) < c["min_frases_paragrafo"]:
            continue
        ult = fs[-1]
        t = ult["texto"]
        if (len(ult["palavras"]) <= c["max_palavras"] and not re.search(r"\d", t) and t.endswith((".", "!"))
                and c["_rx_abstratos"].search(t) and not RE_LINHA_LISTA.match(t)):
            fechos.append(ult)
    num["fechos_grandiosos"] = len(fechos)
    for f in fechos:
        achados.append(novo_achado(
            cfg, "m_fecho_grandioso", c["categoria"], "fecho_grandioso", "media", f["texto"], f["inicio"], f["fim"],
            c["explicacao"], "Termine direto. Às vezes o melhor fim é parar uma frase antes.", peso=c["peso"],
        ))
    if len(fechos) >= c["min_serie"]:
        achados.append(novo_achado(
            cfg, "m_fechos_em_serie", c["categoria"], "fecho_grandioso", "alta",
            f"{len(fechos)} parágrafos fechando em frase de efeito", fechos[0]["inicio"], fechos[0]["fim"],
            "Fecho grandioso virou hábito no texto.", "Corte a maioria; deixe um, se muito.", peso=c["peso_serie"],
        ))

    # 16. Hedging em série.
    c = M["hedging_em_serie"]
    hedges = [a for a in achados_regex if a["subtipo"] == "hedge"]
    num["hedges"] = len(hedges)
    num["hedges_por_mil"] = por_mil(len(hedges))
    if len(hedges) >= c["min_ocorrencias"] and por_mil(len(hedges)) >= c["min_por_mil"]:
        achados.append(novo_achado(
            cfg, "m_hedging_em_serie", c["categoria"], "hedge", "alta",
            f"{len(hedges)} hedges em {n_palavras} palavras", hedges[0]["inicio"], hedges[0]["fim"],
            c["explicacao"], "Tome posição. Ressalva real tem nome, não vaguidão.", peso=c["peso"],
        ))

    return achados, num


# ─────────────────────────────────────────────────────────────────────────────
# Pontuação
# ─────────────────────────────────────────────────────────────────────────────

def pontuar(cfg, achados, n_palavras):
    """Aplica repetição com desconto e teto por padrão; devolve totais e por categoria."""
    fator = cfg["repeticao"]["fator_extra"]
    teto = cfg["repeticao"]["teto_por_padrao"]
    vistos = Counter()
    por_id = defaultdict(float)
    for a in achados:
        chave = (a["id"], a["texto"].lower())
        a["contribuicao"] = a["peso"] if vistos[chave] == 0 else a["peso"] * fator
        vistos[chave] += 1
        por_id[a["id"]] += a["contribuicao"]
    for a in achados:
        total = por_id[a["id"]]
        if total > teto:
            a["contribuicao"] = a["contribuicao"] * teto / total
        a["contribuicao"] = round(a["contribuicao"], 2)

    k = cfg["score"]["k"]
    k_cat = cfg["score"]["k_categoria"]
    # Piso no denominador: texto curto (uma legenda, um box) não vira 50 por causa de um achado.
    base = max(n_palavras, cfg["score"].get("piso_palavras", 1))
    pontos = sum(a["contribuicao"] for a in achados)
    dens = pontos / base * 1000
    score = int(round(100 * (1 - math.exp(-dens / k))))

    categorias = {}
    for cat in cfg["categorias"]:
        pc = sum(a["contribuicao"] for a in achados if a["categoria"] == cat)
        dc = pc / base * 1000
        categorias[cat] = {
            "rotulo": cfg["categorias"][cat]["rotulo"],
            "achados": sum(1 for a in achados if a["categoria"] == cat),
            "pontos": round(pc, 1),
            "densidade": round(dc, 1),
            "nota": int(round(100 * (1 - math.exp(-dc / k_cat)))),
        }
    return score, round(pontos, 1), round(dens, 1), categorias


def faixa_de(cfg, score):
    for f in cfg["score"]["faixas"]:
        if score <= f["ate"]:
            return f["rotulo"]
    return cfg["score"]["faixas"][-1]["rotulo"]


# ─────────────────────────────────────────────────────────────────────────────
# Análise completa
# ─────────────────────────────────────────────────────────────────────────────

# Categorias em que a acusação é sobre a PALAVRA escolhida. Se a palavra está na fala
# medida da autora, ela não é vocabulário de IA: é vocabulário dela. Acusação de ESTRUTURA
# (anáfora, dois-pontos, contraste, ritmo) não entra aqui, porque é sobre composição, não léxico.
CATEGORIAS_LEXICAIS = {"vocabulario_n1", "vocabulario_n2", "vocabulario_n3", "transicao", "hedge"}
MIN_OCORRENCIAS_CORPUS = 2   # uma ocorrência pode ser erro de transcrição

def absolver_pelo_corpus(achados, corpus):
    """Tira do score o que a autora comprovadamente fala.

    Nasceu de um caso concreto: o detector marcou 'gerar valor' como vocabulário de IA
    nível 1 (gravidade alta) numa frase LITERAL dela, que aparece quatro vezes no corpus.
    Uma régua que pune a voz da autora empurra o texto pra longe dela.
    """
    if not corpus:
        return achados, []
    baixo = corpus.lower()
    vivos, absolvidos = [], []
    for a in achados:
        termo = (a.get("texto") or "").strip().lower()
        termo = re.sub(r"\s*\(.*?\)\s*", " ", termo)
        termo = re.sub(r"\s*x\d+$", "", termo).strip()
        if (a.get("subtipo") in CATEGORIAS_LEXICAIS and len(termo) >= 3
                and baixo.count(termo) >= MIN_OCORRENCIAS_CORPUS):
            a = dict(a); a["absolvido_pelo_corpus"] = baixo.count(termo)
            absolvidos.append(a)
        else:
            vivos.append(a)
    return vivos, absolvidos

def analisar(texto, cfg, nome="texto", corpus=None):
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    prosa, titulos, info = mascarar(texto)
    paragrafos = paragrafos_de(prosa)
    frases = []
    for p in paragrafos:
        frases.extend(frases_de(p["texto"], p["inicio"]))
    n_palavras = len(RE_PALAVRA.findall(prosa))

    resultado = {
        "arquivo": nome,
        "palavras": n_palavras,
        "paragrafos": len(paragrafos),
        "frases": len(frases),
        "mascarado": dict(info),
        "avisos": [],
        "absolvidos_pelo_corpus": [],
    }
    if n_palavras < cfg["score"]["min_palavras"]:
        resultado.update({"score": 0, "faixa": "texto curto demais pra pontuar", "pontos": 0, "densidade": 0,
                          "categorias": {}, "metricas": {}, "achados": []})
        resultado["avisos"].append(f"Menos de {cfg['score']['min_palavras']} palavras de prosa; sem score.")
        return resultado

    achados = rodar_padroes(cfg, prosa, titulos)
    achados += rodar_vocabulario(cfg, prosa, paragrafos, n_palavras)
    met, numeros = rodar_metricas(cfg, texto, prosa, paragrafos, frases, n_palavras, achados)
    achados += met
    achados, absolvidos = absolver_pelo_corpus(achados, corpus)

    resultado["absolvidos_pelo_corpus"] = [
        {"termo": a.get("texto"), "subtipo": a.get("subtipo"),
         "gravidade": a.get("gravidade"), "no_corpus": a["absolvido_pelo_corpus"]} for a in absolvidos]
    score, pontos, dens, categorias = pontuar(cfg, achados, n_palavras)
    for a in achados:
        a["linha"] = linha_de(texto, a["inicio"])
        a["trecho"] = trecho_em(texto, a["inicio"], a["fim"]) if a["fim"] > a["inicio"] else ""
    achados.sort(key=lambda a: (a["inicio"], -ORDEM_GRAVIDADE[a["gravidade"]]))

    # Abaixo do piso de palavras, métricas de densidade (uniformidade de parágrafo, CV de
    # frase, pontuação) medem ruído: um anexo de cards tem 5 parágrafos de prosa. O score
    # continua saindo pra inspeção, mas marcado como não avaliável, e o portão o ignora.
    piso = cfg["score"].get("piso_palavras", 300)
    if n_palavras < piso:
        resultado["amostra_pequena"] = True
        resultado["avisos"].append(
            f"{n_palavras} palavras de prosa (piso {piso}): score informativo, não use como portão.")
    else:
        resultado["amostra_pequena"] = False

    resultado.update({
        "score": score,
        "faixa": faixa_de(cfg, score),
        "pontos": pontos,
        "densidade": dens,
        "formula": cfg["score"]["formula"],
        "categorias": categorias,
        "metricas": numeros,
        "achados": achados,
    })
    return resultado


# ─────────────────────────────────────────────────────────────────────────────
# Saída
# ─────────────────────────────────────────────────────────────────────────────

def filtrar(achados, min_grav):
    piso = ORDEM_GRAVIDADE[min_grav]
    return [a for a in achados if ORDEM_GRAVIDADE[a["gravidade"]] >= piso]


def imprimir_humano(r, min_grav):
    print(f"detector_ptbr  {r['arquivo']}  ({r['palavras']} palavras, {r['paragrafos']} parágrafos, {r['frases']} frases)")
    if r["mascarado"]:
        print("ignorado: " + ", ".join(f"{k} {v}" for k, v in r["mascarado"].items()))
    print(f"\nSCORE {r['score']}/100  {r['faixa']}")
    if r["avisos"]:
        for av in r["avisos"]:
            print(f"aviso: {av}")
        return
    print(f"pontos {r['pontos']}  densidade {r['densidade']}/mil palavras\n")
    print("Por categoria (nota 0-100 | achados | pontos):")
    for cat, c in r["categorias"].items():
        print(f"  {c['rotulo']:<38} {c['nota']:>3} | {c['achados']:>3} | {c['pontos']}")

    m = r["metricas"]
    chaves = ["frases_media_palavras", "frases_cv", "frases_mesmo_inicio_proporcao", "paragrafos_proporcao_mesmo_tamanho",
              "travessoes_por_mil", "dois_pontos_por_mil", "proporcao_linhas_em_lista", "negritos", "triades_por_mil",
              "contrastes", "paragrafos_terminando_em_pergunta", "fechos_grandiosos", "hedges_por_mil", "ttr"]
    print("\nMétricas: " + "  ".join(f"{k}={m[k]}" for k in chaves if k in m))

    vis = filtrar(r["achados"], min_grav)
    ocultos = len(r["achados"]) - len(vis)
    print(f"\nAchados ({len(vis)}" + (f", {ocultos} abaixo de '{min_grav}' ocultos" if ocultos else "") + "):")
    for a in vis:
        print(f"  L{a['linha']:<4} [{a['gravidade']:<7}] {a['categoria']}/{a['subtipo']:<18} {a['texto']}")
        print(f"        {a['explicacao']}  →  {a['sugestao']}")
        if a["trecho"] and a["trecho"] != f"«{a['texto']}»":
            print(f"        {a['trecho'][:220]}")
    print()


def main():
    ap = argparse.ArgumentParser(description="Detector de sotaque de IA em PT-BR (portão determinístico).")
    ap.add_argument("arquivo", help="arquivo .md/.txt ('-' lê da entrada padrão)")
    ap.add_argument("--json", action="store_true", help="saída estruturada em JSON")
    ap.add_argument("--min-gravidade", choices=list(ORDEM_GRAVIDADE), default="baixa",
                    help="oculta achados abaixo desta gravidade (o score não muda)")
    ap.add_argument("--limite", type=int, default=None,
                    help="sai com código 2 se o score passar deste valor (uso em pipeline)")
    ap.add_argument("--padroes", default=PADROES_PADRAO, help="caminho alternativo do padroes_ptbr.json")
    ap.add_argument("--corpus", default=None,
                    help="corpus de fala da autora: termo que ela usa de verdade sai do score")
    args = ap.parse_args()

    cfg = carregar_padroes(args.padroes)
    if args.arquivo == "-":
        texto = sys.stdin.read()
        nome = "stdin"
    else:
        with open(args.arquivo, encoding="utf-8") as f:
            texto = f.read()
        nome = args.arquivo

    corpus = None
    if args.corpus:
        with open(args.corpus, encoding="utf-8") as f:
            corpus = f.read()
    r = analisar(texto, cfg, nome, corpus=corpus)

    if args.json:
        saida = dict(r)
        saida["achados"] = filtrar(r["achados"], args.min_gravidade)
        saida["achados_ocultos"] = len(r["achados"]) - len(saida["achados"])
        saida["min_gravidade"] = args.min_gravidade
        print(json.dumps(saida, ensure_ascii=False, indent=2))
    else:
        imprimir_humano(r, args.min_gravidade)

    if args.limite is not None and r["score"] > args.limite:
        sys.exit(2)


if __name__ == "__main__":
    main()
