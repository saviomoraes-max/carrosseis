#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Doutrina — o que cada post JÁ ENSINOU, pra nunca contradizer post anterior.

Por que existe (30/jul/26, pedido do Sávio: "vamos tomar cuidado pra a gente nunca
contradizer o que a gente botou em outro post"): o SEM31/AD006 saiu do forno
mandando "NUNCA PROMETA O ABATIMENTO" enquanto o SEM25/AD003 — campeão do acervo,
s/r 3,95% maduro contra mediana de 0,64% — ensinava o OPOSTO: segure o abatimento
e TROQUE ele por compromisso de agendamento. Sete dimensões do portão passaram por
cima disso, porque todas perguntam "isso se repete?" e nenhuma perguntava "isso
CONTRADIZ?". Território cuida de repetição; doutrina cuida de coerência.

O `territorio_vivo.py` mapeia o que foi DITO. Este mapeia o que foi PRESCRITO:
regras (nunca/sempre/só/não), scripts entre aspas e os fechos — que é onde mora a
instrução que a doutora vai levar pro consultório.

A comparação semântica continua sendo julgamento (do produtor e do portão). O que
o script entrega é o AGRUPAMENTO por assunto: "estes 6 posts prescreveram algo
sobre ABATIMENTO — leia os 6 antes de prescrever o 7º".

Uso:
  python3 doutrina.py                  # gera data/doutrina.json + resumo por assunto
  python3 doutrina.py abatimento       # o que já foi prescrito sobre esse assunto
  python3 doutrina.py --dias 400       # janela maior (default: acervo inteiro)
"""

import argparse
import glob
import json
import os
import re
import sys
from datetime import datetime

from territorio_vivo import BASE, data_do_post, norm

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "doutrina.json")

# marcas de PRESCRIÇÃO: a frase manda fazer (ou não fazer) alguma coisa
PRESCRITIVO = re.compile(
    r"\bnunca\b|\bsempre\b|\bjamais\b|\bnão (?:emende|prometa|entregue|ofereça|diga|"
    r"fale|d[êe]|faça|use|aceite)\b|\bs[óo] (?:use|fale|entregue|ofereça)\b|"
    r"\bpasse\b|\bconduza\b|\bfaça\b|\bpeça\b|\bvolte\b|\bdiga\b|\bguarde\b|"
    r"\bsegure\b|\btroque\b|\bmarque\b|\bcobre\b|\bevite\b|\bpare de\b|\bdeixe de\b",
    re.I)

# assuntos que a clínica repete post a post — é onde a contradição dói
ASSUNTOS = {
    "abatimento":   r"abat|deduz|desconto|abate",
    "preço":        r"pre[çc]o|valor da consulta|investimento|quanto custa|tabela",
    "sinal":        r"\bsinal\b|pago antes|pagamento antecipado|pix",
    "agendamento":  r"agendar|agendamento|marcar|remarcar|confirma",
    "comparecimento": r"faltou|faltar|no.?show|compareci|apareceu|n[ãa]o veio",
    "retorno":      r"retorno|revis[ãa]o|manuten[çc][ãa]o",
    "whatsapp":     r"whats|[áa]udio|mensagem|direct|dm\b",
    "objeção":      r"obje[çc]|vou pensar|caro|pensar melhor|marido|financeiro",
    "conteúdo":     r"feed|post|reels|conte[úu]do|stories|seguidor",
    "triagem":      r"triagem|qualifica|filtro|perguntas antes",
}


def frases_prescritivas(j):
    """Toda linha do post que PRESCREVE: punch, título/corpo de item, fecho, callout."""
    saida = []
    for i, s in enumerate(j.get("slides", []), 1):
        blocos = []
        for k in ("punch", "headline", "sub", "fecho", "callout"):
            if s.get(k):
                blocos.append((k, s[k]))
        body = s.get("body") or []
        if isinstance(body, str):
            body = [body]
        blocos += [("body", b) for b in body if isinstance(b, str)]
        for it in (s.get("items") or []):
            if isinstance(it, dict):
                blocos.append(("item", f'{it.get("title","")} — {it.get("body","")}'))
            elif isinstance(it, str):
                blocos.append(("item", it))
        for campo, txt in blocos:
            limpo = txt.replace("\n", " ").strip()
            # item de lista e fecho são prescrição POR CONSTRUÇÃO (são os passos do
            # método e o saldo dele) — não exigir verbo imperativo. O detector de
            # verbo perdia coisas como "O ABATE NA HORA CERTA — guardado pra hora
            # certa, o mesmo abate transforma o valor em compromisso" (SEM30/AD004),
            # que é prescrição pura sem um único imperativo.
            if campo in ("item", "fecho") or PRESCRITIVO.search(limpo):
                saida.append({"slide": i, "campo": campo, "texto": limpo})
    return saida


# ── era pré-engine ───────────────────────────────────────────────────────────
# Os posts até ~SEM26 não têm copy.json: a copy mora dentro do build.py, em
# chamadas tipo para("..."), quote_card("..."), punch_cr("..."). É onde vive o
# SEM25/AD003 — o campeão (s/r 3,95%) que o SEM31/AD006 contradisse. Ignorar essa
# era seria construir a trava justamente sem o caso que a motivou.
_TAG = re.compile(r"<[^>]+>")
_LIXO = re.compile(r"px|#[0-9a-fA-F]{3,6}|font-|url\(|/Volumes|\.png|\.jpg|"
                   r"^\s*[a-z_]+\s*=|rgba?\(|:\s*\d|"
                   r"={4,}|-{4,}|SLIDE \d|styl|f'|\{|\}|_para|_uri|import |def |"
                   # aspas de atributo HTML fazem o regex atravessar o literal e
                   # colar código na copy ("...pacientes.', subtitle=(")
                   r"'\s*,|\w=\(|=\"|\bsize=|\bwidth=", re.I)


def copy_de_build_py(pasta):
    """Extração aproximada da copy de um post pré-engine. Sem estrutura de slide —
    o que importa aqui é O QUE FOI PRESCRITO, não em qual card estava."""
    bp = os.path.join(pasta, "build.py")
    if not os.path.exists(bp):
        return []
    fonte = open(bp, encoding="utf-8", errors="replace").read()
    achados = []
    for lit in re.findall(r"'([^'\\]{25,400})'|\"([^\"\\]{25,400})\"", fonte):
        txt = (lit[0] or lit[1])
        if _LIXO.search(txt):
            continue
        txt = _TAG.sub(" ", txt).replace("&ldquo;", "“").replace("&rdquo;", "”")
        txt = txt.replace("&hellip;", "…").replace("&nbsp;", " ")
        txt = re.sub(r"\s+", " ", txt).strip()
        if len(txt) < 25 or " " not in txt:
            continue
        achados.append({"slide": 0, "campo": "build.py", "texto": txt})
    return achados


def scripts(j):
    """Frases entre aspas curvas — o que a doutora vai FALAR, palavra por palavra."""
    txt = json.dumps(j, ensure_ascii=False)
    achados = re.findall(r"[“\"]([^”\"]{25,300})[”\"]", txt)
    return [a.replace("\\n", " ").strip() for a in achados]


def assuntos_de(texto):
    n = norm(texto)
    return sorted(k for k, rx in ASSUNTOS.items() if re.search(rx, n, re.I))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("assunto", nargs="?", help="filtra por assunto (ex.: abatimento)")
    ap.add_argument("--dias", type=int, default=100000)
    args = ap.parse_args()

    agora = datetime.now()
    posts = []
    for pasta in sorted(glob.glob(os.path.join(BASE, "SEM*", "AD*"))):
        js = glob.glob(os.path.join(pasta, "copy*.json"))
        nome = pasta.split("/novos/")[1]
        if js:
            dt = data_do_post(pasta)
            if not dt or (agora - dt).days > args.dias:
                continue
            try:
                j = json.load(open(js[0], encoding="utf-8"))
            except Exception:
                continue
            regras, scr = frases_prescritivas(j), scripts(j)
        else:
            # post pré-engine: data vem do mtime do build.py, é só pra ordenar
            bp = os.path.join(pasta, "build.py")
            if not os.path.exists(bp):
                continue
            dt = datetime.fromtimestamp(os.path.getmtime(bp))
            if (agora - dt).days > args.dias:
                continue
            regras = copy_de_build_py(pasta)
            scr = [r["texto"] for r in regras if r["texto"].startswith("“")]
        if not regras:
            continue
        posts.append({
            "post": nome,
            "publicado": os.path.exists(os.path.join(pasta, "POSTADO.txt")),
            "pre_engine": not bool(js),   # POSTADO.txt é convenção nova; pré-engine não tem
            "dias": (agora - dt).days,
            "regras": regras,
            "scripts": scr,
            "assuntos": assuntos_de(" ".join(r["texto"] for r in regras)),
        })

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump({"gerado_em": agora.isoformat(timespec="seconds"), "posts": posts},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    if args.assunto:
        alvo = args.assunto.lower()
        rx = ASSUNTOS.get(alvo)
        if not rx:
            sys.exit(f"assunto desconhecido. use um de: {', '.join(ASSUNTOS)}")
        print(f"O QUE JÁ FOI PRESCRITO SOBRE '{alvo.upper()}'"
              f" — leia tudo antes de prescrever de novo\n")
        for p in sorted(posts, key=lambda x: -x["dias"]):
            regras = [r for r in p["regras"] if re.search(rx, norm(r["texto"]), re.I)]
            if not regras:
                continue
            marca = ("publicado" if p["publicado"] else
                     "pré-engine" if p.get("pre_engine") else "não publicado")
            print(f"── {p['post']}  (d+{p['dias']}, {marca})")
            for r in regras:
                print(f"     S{r['slide']} [{r['campo']}] {r['texto'][:150]}")
            print()
        return

    print(f"doutrina: {len(posts)} posts com prescrição · gravado em {OUT}\n")
    contagem = {}
    for p in posts:
        for a in p["assuntos"]:
            contagem.setdefault(a, []).append(p["post"])
    for a, ps in sorted(contagem.items(), key=lambda kv: -len(kv[1])):
        print(f"  {a:16} {len(ps):2} posts prescreveram  "
              f"→ python3 doutrina.py {a}")


if __name__ == "__main__":
    main()
