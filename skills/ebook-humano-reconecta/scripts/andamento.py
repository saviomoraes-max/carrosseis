#!/usr/bin/env python3
"""Andamento do livro em porcentagem, medido dos arquivos, não estimado de cabeça.

Uso: python3 andamento.py ebooks/<slug> [--detalhe]

Cada frente tem peso e um medidor objetivo. Se um medidor não puder ser lido,
a frente aparece como "?" e NÃO entra na conta, pra não inflar o número.
"""
import json, re, sys, pathlib

FRENTES = [
    ("Fontes, voz e transcrições", 10),
    ("Escrita dos blocos",         20),
    ("Revisão adversarial",        35),
    ("Design e diagramação",       20),
    ("Fecho e entrega",            15),
]

def ler_json(p):
    try: return json.loads(p.read_text())
    except Exception: return None

def corpus_da_autora(raiz):
    """O detector precisa da MESMA régua do portão: termo que a autora fala não é tell dela."""
    for p in sorted((raiz / "fontes" / "voz" / "corpus").glob("*.txt")) if (raiz / "fontes" / "voz" / "corpus").exists() else []:
        return p
    return None

def ultimo_detector(d):
    """Devolve (score, avaliavel). Bloco com pouca prosa (anexo de cards) tem score
    informativo, não de portão: entra como não avaliável e sai da conta."""
    vs = sorted(d.glob("detector-v*.json"), key=lambda x: int(re.search(r"v(\d+)", x.name).group(1)))
    if not vs: return None, True
    j = ler_json(vs[-1])
    if not j: return None, True
    return j.get("score"), not j.get("amostra_pequena", False)

def rodadas_validas(d):
    """Rodada só conta se o cético julgou de verdade (brutos > 0). Rodada que morreu
    por limite de sessão volta com brutos 0 e não é rodada.

    O cego vale o MAIS RECENTE, por data de gravação do arquivo. Ordenar por nome fazia
    "rodada-cego-pos-v3.json" vencer "rodada-3.json" e o medidor reportava veredito velho;
    preferir a rodada numerada erra do outro lado, porque medição avulsa de cego é mais
    nova que a rodada em vários blocos. Data é a única régua que não mente aqui."""
    numeradas = sorted((x for x in d.glob("rodada-*.json") if re.match(r"rodada-\d+\.json$", x.name)),
                       key=lambda x: int(re.search(r"(\d+)", x.name).group(1)))
    n = sum(1 for rj in numeradas if (ler_json(rj) or {}).get("brutos"))
    candidatos = []
    for rj in list(numeradas) + sorted(d.glob("rodada-cego*.json")):
        c = (ler_json(rj) or {}).get("cego") or {}
        if c.get("veredito"):
            candidatos.append((rj.stat().st_mtime, c["veredito"], c.get("confianca")))
    cego = max(candidatos)[1:] if candidatos else None
    return n, cego

def medir(raiz):
    raiz = pathlib.Path(raiz)
    L = ler_json(raiz / "livro.json") or {}
    blocos = sorted((raiz / "manuscrito").glob("*.md"))
    n_planejado = max(len(L.get("sumario") or []), len(blocos))
    est = {}

    # 1. Fontes. O que decide não é quantidade de arquivo, é se há material suficiente
    #    pra escrever com fidelidade NA VOZ dela. Por isso o corpus é medido em PALAVRAS.
    fontes = list((raiz / "fontes").glob("*.md"))
    vozd = raiz / "fontes" / "voz"
    palavras_voz = sum(len(f.read_text(errors="ignore").split())
                       for f in list(vozd.glob("amostra*.txt")) + list((vozd / "corpus").glob("*.txt")))
    fp = (vozd / "fingerprint-ana.md").exists()
    tr = list((raiz / "fontes" / "transcricao").glob("*.txt"))
    escritas = list(vozd.glob("escrita*.txt")) + list((vozd / "corpus").glob("escrita*.txt"))
    ALVO_PALAVRAS = 20000     # abaixo disso a prosa composta domina e a costura aparece
    est["Fontes, voz e transcrições"] = (
        min(1.0, len(fontes) / 3) * 0.35
        + min(1.0, palavras_voz / ALVO_PALAVRAS) * 0.35
        + (0.10 if fp else 0)
        + min(1.0, len(tr) / 3) * 0.10
        + (0.10 if escritas else 0)   # amostra ESCRITA da autora: ainda não existe
    )

    # 2. Escrita: bloco existe e tem corpo.
    escritos = [b for b in blocos if len(b.read_text().split()) > 150]
    est["Escrita dos blocos"] = len(escritos) / n_planejado if n_planejado else 0

    # 3. Revisão: por bloco, três degraus de peso igual.
    #    (a) uma rodada válida aplicada  (b) detector no portão  (c) cego não diz IA
    a = b = c = 0
    obtidos = possiveis = 0
    detalhe = []
    for arq in blocos:
        num = arq.name.split("-")[0]
        d = raiz / "revisao" / num
        nr, cego = rodadas_validas(d) if d.exists() else (0, None)
        det, avaliavel = ultimo_detector(d) if d.exists() else (None, True)
        pa = 1 if nr >= 1 else 0
        pb = 1 if (det is not None and det <= 25) else 0
        pc = 1 if (cego and cego[0] != "ia") else 0
        degraus = 3 if avaliavel else 2          # sem detector de portão, o bloco vale 2 degraus
        soma = pa + pc + (pb if avaliavel else 0)
        a += pa; b += pb if avaliavel else 0; c += pc
        possiveis += degraus; obtidos += soma
        detalhe.append((num, nr, det if avaliavel else f"{det}*", cego, f"{soma}/{degraus}"))
    est["Revisão adversarial"] = obtidos / possiveis if possiveis else 0

    # 4. Design: render existe, provas existem, gráficos presentes; falta só a leitura visual final.
    r = raiz / "render"
    pdf = (r / f"{L.get('arquivo','livro')}.pdf").exists()
    provas = len(list((r / "provas").glob("pag*.png"))) if (r / "provas").exists() else 0
    com_grafico = sum(1 for x in blocos if ":::grafico" in x.read_text())
    est["Design e diagramação"] = (0.4 if pdf else 0) + (0.3 if provas else 0) + 0.3 * min(1.0, com_grafico / max(len(blocos) - 4, 1))

    # 5. Fecho: sem placeholder pendente, sem travessão, memória e relatório.
    txt = "\n".join(x.read_text() for x in blocos)
    sem_travessao = "—" not in txt
    pend = len(re.findall(r"\[LINK[^\]]*\]", txt))
    # O quarto termo estava faltando na soma: sem ele a frente tinha teto de 75% e o livro
    # nunca fechava, por bug de medicao e nao por trabalho pendente.
    relatorio = (raiz / "relatorio-de-entrega.md").exists() and (raiz / "ESTADO.md").exists()
    est["Fecho e entrega"] = ((0.25 if sem_travessao else 0) + (0.25 if pend == 0 else 0)
                              + (0.25 if pdf else 0) + (0.25 if relatorio else 0))

    return est, detalhe, {"blocos": len(blocos), "planejado": n_planejado, "pdf": pdf,
                          "provas": provas, "placeholders_pendentes": pend}

def main():
    raiz = sys.argv[1] if len(sys.argv) > 1 else "."
    est, detalhe, info = medir(raiz)
    total = sum(est[n] * p for n, p in FRENTES)
    print(f"{'frente':32}{'peso':>6}{'feito':>8}")
    for n, p in FRENTES:
        print(f"{n:32}{p:>5}%{est[n]*100:>7.0f}%")
    print(f"{'':32}{'':>6}{'':>8}")
    print(f"ANDAMENTO GERAL: {total:.0f}%")
    if "--detalhe" in sys.argv:
        print(f"\n{'bloco':7}{'rodadas':>8}{'detector':>9}  cego            degraus   (* = amostra pequena, fora do portão)")
        for num, nr, det, cego, deg in detalhe:
            cg = f"{cego[0]} {cego[1]}" if cego else "—"
            print(f"{num:7}{nr:>8}{str(det if det is not None else '?'):>9}  {cg:15} {deg}")
        print("\n", info)

if __name__ == "__main__":
    main()
