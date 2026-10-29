#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Caça a punchline de comparação (vício de IA) em legenda e copy de slide.

Sávio, 26/10/2026, sobre «Não é fórmula, é mapa. Tem lead que voa pela conexão e trava no
fechamento, tem lead que precisa de mais tempo...»: "esse tipo de frase me dá asco, essa punch
line de comparação é vício de IA total". Tolerância ZERO (antes o checklist aceitava até 2).

Pega: "não é X, é Y" · "não X. Y" com pivô · "X, nunca Y" · "para de X e passa a Y" ·
"tem quem/tem lead que ..., tem ... que" · "não tem nada a ver com X. Tem a ver com Y" ·
"menos X, mais Y" · "não quer X. Ela quer Y".
Uso: python3 vicio_comparacao.py <arquivo...>   (legenda.txt, tweets.json, dump.json, copy.md)
"""
import json, re, sys

PADROES = [
    (r"\bn[aã]o [eé]\b[^.!?\n]{1,60}[,;:.] *[eé]\b", "não é X, é Y"),
    (r"\bn[aã]o (?:é|era|foi|está|tá)\b[^.!?\n]{1,60}\. *(?:É|Era|Foi)\b", "não é X. É Y"),
    (r",\s*nunca\b", "X, nunca Y"),
    (r"\bpara de\b[^.!?\n]{1,80}\bpassa a\b", "para de X e passa a Y"),
    (r"\btem (?:quem|lead|gente|paciente|dia|cliente)[^.!?\n]{0,10} que\b[^.!?\n]{1,80}, tem\b", "tem X que..., tem Y que"),
    (r"\bn[aã]o tem nada a ver com\b[^.!?\n]{1,80}[.,] *tem\b", "não tem a ver com X, tem com Y"),
    (r"\bmenos [^.!?\n]{1,30}, mais\b", "menos X, mais Y"),
    (r"\bn[aã]o quer\b[^.!?\n]{1,40}\. *(?:Ela|Ele) quer\b", "não quer X. Quer Y"),
    (r"\bn[aã]o [eé] sobre\b", "não é sobre X"),
    (r"\bn[aã]o tem\b[^.!?\n]{1,50}, quem tem\b", "X não tem, quem tem é Y"),
    (r"\bn[aã]o\b[^.!?\n]{1,50}\.\s*(?:Ela|Ele|Você|A gente)\s+(?:só\s+)?(?:quer|precisa|vende|faz)\b", "não X. Ela quer Y"),
]


def textos(caminho):
    s = open(caminho, encoding="utf-8").read()
    if caminho.endswith(".json"):
        d = json.loads(s)
        itens = d.get("tweets") or d.get("cards") or []
        out = []
        for i, c in enumerate(itens, 1):
            for k in ("t", "headline", "sub", "pilula"):
                if c.get(k):
                    out.append((f"card {i}", c[k].replace("{", "").replace("}", "")))
        return out
    return [("texto", s)]


def main():
    total = 0
    for arq in sys.argv[1:]:
        for onde, t in textos(arq):
            plano = re.sub(r"\s*\n\s*", " ", t)
            for rx, nome in PADROES:
                for m in re.finditer(rx, plano, re.I):
                    total += 1
                    ini = max(0, m.start() - 30)
                    print(f"✗ {arq.split('/')[-2]}/{arq.split('/')[-1]} {onde} [{nome}]: …{plano[ini:m.end() + 30]}…")
    print("limpo" if not total else f"{total} ocorrência(s)")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
