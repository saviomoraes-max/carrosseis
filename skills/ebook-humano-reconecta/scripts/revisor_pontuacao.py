#!/usr/bin/env python3
"""Linter de pontuação e ortotipografia pro manuscrito do ebook.

Não julga estilo nem voz: procura só o que está mecanicamente errado ou
inconsistente, o tipo de coisa que faz a leitora tropeçar sem saber por quê.

Uso: python3 revisor_pontuacao.py ebooks/<slug> [--csv]
"""
import re, sys, pathlib, collections

# fala reportada: verbo de dizer + vírgula/dois-pontos + fala que NÃO abre com aspas
VERBOS_FALA = r"(?:falou|falei|fala|falam|disse|dizia|diz|dizem|respondeu|responde|perguntou|pergunta|pensou|pensa|pensei|comenta|comentou|avisa|avisou|conta|contou|emenda|emendou|manda|mandou|escreve|escreveu)"

# "pergunta", "resposta", "fala" e "conta" também são SUBSTANTIVO. Quando vem determinante
# antes, não é verbo de dizer: "uma pergunta, igual você fez" não é fala reportada.
DETERMINANTE = r"(?<![Uu]ma )(?<![Aa] )(?<![Ee]ssa )(?<![Ss]ua )(?<![Dd]a )(?<![Mm]esma )(?<![Oo]utra )(?<![Nn]enhuma )(?<![Aa]quela )"

# Depois da vírgula, palavra de função abre ORAÇÃO, não fala. Fala reportada de verdade
# começa com verbo ou interjeição: "ela disse, vou pensar".
POS_VIRGULA = (r"(?!(?:n[ãa]o|mas|porque|que|quando|como|se|igual|embora|"
               r"com|sem|de|do|da|dos|das|em|no|na|nos|nas|por|pra|para|"
               r"a|o|os|as|um|uma|voc[ê]s?|ela|ele|eles|elas|eu|a gente|"
               r"j[áa]|ainda|tamb[ée]m|s[óo]|nem|depois|antes|tem|t[êe]m|cita|feit[ao]|dit[ao]|mais|menos|tanto)\b)")

def blocos_protegidos(t):
    """Intervalos que não são prosa do autor: front matter e blocos :::."""
    faixas = []
    m = re.match(r"\A---\n.*?\n---\n", t, re.S)
    if m: faixas.append((m.start(), m.end()))
    for m in re.finditer(r"^:::[^\n]*\n.*?^:::[ \t]*$", t, re.S | re.M):
        faixas.append((m.start(), m.end()))
    return faixas

def protegido(pos, faixas):
    return any(a <= pos < b for a, b in faixas)

def linha_de(t, pos):
    return t.count("\n", 0, pos) + 1

REGRAS = [
    # (id, descrição, regex, dica)
    ("fala-sem-aspas",
     "fala reportada sem aspas: a leitora não sabe onde a fala começa e termina",
     rf"{DETERMINANTE}\b{VERBOS_FALA},\s+(?![\"“«A-ZÀ-Ú]){POS_VIRGULA}[a-zà-ú]",
     "abrir aspas na fala e fechar onde ela acaba"),

    ("aspas-retas",
     "aspas retas em vez de curvas",
     r'"',
     "usar “ ” (curvas), padrão tipográfico do livro"),

    ("aspas-impares",
     "número ímpar de aspas curvas na linha: alguma não fechou",
     None, None),  # tratada à parte

    ("virgula-antes-de-tag",
     "muleta de checagem sem vírgula antes",
     r"[a-zà-ú]\s+(?:né|tá|sabe|viu)\?",
     "vírgula antes: “..., né?”"),

    ("vocativo-sem-virgula",
     "vocativo sem vírgula",
     r"^(?:Gente|Doutora|Olha)\s+(?![,.!?])(?!(?:s[óo]|aqui|l[áa]|essa|esse|isso|uma?|os?|as?|que|como|quando|se|bem|pra|para|pro)\b)",
     "vírgula depois do vocativo: “Gente, ...”"),

    ("espaco-antes-pontuacao",
     "espaço antes de pontuação",
     r"[^\s:] +[,;!?](?![:])",
     "colar a pontuação na palavra"),

    ("espaco-duplo",
     "espaço duplo",
     r"[^\n] {2,}[^\n]",
     "um espaço só"),

    ("reticencias-pontos",
     "reticências com três pontos separados em vez de …",
     None, None),  # informativo, decisão do projeto

    ("interrogativa-sem-interrogacao",
     "frase curta que começa com pronome interrogativo e termina em ponto",
     r"(?:^|(?<=[.!?]) )(?:O que|Que|Quem|Quando|Onde|Como|Por que|Qual|Quanto)\b"
     r"(?!(?:(?![.!?\n]).)*\b(?:[ée]|foi|s[ãa]o|eram?|est[áa]|est[ãa]o|t[áa]|tava|ficou?|vira|virou|significa|quer dizer)\b)"
     r"[^.!?\n]{5,45}\.",
     "trocar o ponto por interrogação, ou reescrever"),

    ("paragrafo-em-minuscula",
     "parágrafo começando com letra minúscula",
     r"(?<=\n\n)(?!https?://)[a-zà-ÿ]",
     "maiúscula: no manuscrito cada parágrafo é uma linha"),

    ("minuscula-apos-ponto",
     "minúscula depois de ponto final",
     r"(?<=[a-zà-ú])\.\s+[a-zà-ú]{2,}",
     "maiúscula, ou trocar o ponto por vírgula"),

    ("virgula-antes-de-e-porque",
     "‘porque’ colado sem vírgula depois de oração completa",
     None, None),  # ruído demais, fora
]

def auditar(arq):
    t = arq.read_text()
    faixas = blocos_protegidos(t)
    achados = []
    for rid, desc, rx, dica in REGRAS:
        if not rx: continue
        for m in re.finditer(rx, t, re.M):
            if protegido(m.start(), faixas): continue
            ini = max(0, m.start() - 55); fim = min(len(t), m.end() + 55)
            trecho = re.sub(r"\s+", " ", t[ini:fim]).strip()
            achados.append((linha_de(t, m.start()), rid, desc, trecho, dica))
    # Eco: a mesma frase longa duas vezes DENTRO do mesmo parágrafo. É a assinatura do
    # enxerto duplicado — quando uma correção reescreve um trecho maior do que o acusado,
    # a substituição literal repete a abertura do parágrafo. Um leitor cego pegou isso
    # antes de mim, o que quer dizer que a leitora também pegaria.
    for m in re.finditer(r"^(?!:::)(?!#).+$", t, re.M):
        if protegido(m.start(), faixas): continue
        vistas = {}
        for f in re.split(r"(?<=[.!?])\s+", m.group(0)):
            f = f.strip()
            if len(f) < 25: continue
            if f in vistas:
                achados.append((linha_de(t, m.start()), "eco-no-paragrafo",
                                "a mesma frase aparece duas vezes no mesmo parágrafo",
                                re.sub(r"\s+", " ", f)[:130], "apagar a repetição"))
            vistas[f] = 1

    # aspas ímpares por parágrafo
    for m in re.finditer(r"^(?!:::)(?!#).+$", t, re.M):
        if protegido(m.start(), faixas): continue
        ln = m.group(0)
        if (ln.count("“") + ln.count("”")) % 2 or ln.count('"') % 2:
            achados.append((linha_de(t, m.start()), "aspas-impares",
                            "aspas que abrem e não fecham na mesma linha",
                            re.sub(r"\s+", " ", ln)[:130], "fechar a aspa"))
    return sorted(achados)

def main():
    raiz = pathlib.Path(sys.argv[1])
    tot = collections.Counter()
    for arq in sorted((raiz / "manuscrito").glob("*.md")):
        ach = auditar(arq)
        if not ach: continue
        print(f"\n{'='*80}\n{arq.name}  ({len(ach)} achados)")
        for ln, rid, desc, trecho, dica in ach:
            tot[rid] += 1
            print(f"  L{ln:<4} [{rid}] {desc}")
            print(f"        …{trecho}…")
            if dica: print(f"        → {dica}")
    print(f"\n{'='*80}\nRESUMO")
    for rid, n in tot.most_common():
        print(f"  {n:>4}  {rid}")
    print(f"  {sum(tot.values()):>4}  TOTAL")

if __name__ == "__main__":
    main()
