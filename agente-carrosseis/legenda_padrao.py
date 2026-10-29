#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Acusa padrão repetido entre uma legenda nova e as legendas recentes (26/10/2026).

Pedido do Sávio: "a abordagem pra isso em toda legenda [tem que ser] diferente, senão as pessoas
notam muito fácil o padrão". Compara a legenda nova com as legendas.txt das últimas N semanas:
  - sequência de 4+ palavras em comum (frase reciclada)
  - mesma primeira palavra / mesma abertura de CTA
Uso: python3 legenda_padrao.py <legenda.txt> [--semanas 3]
"""
import argparse, glob, os, re, unicodedata

SSD = "/Volumes/SSD kenipe/estáticos/novos"
# sem o SSD (outro membro do time): posts vivem em ./producao na raiz do repo (CLAUDE.md)
BASE = SSD if os.path.isdir(SSD) else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "producao")


def norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.findall(r"[a-z0-9]+", t)


def ngramas(p, n=4):
    return {" ".join(p[i:i + n]) for i in range(len(p) - n + 1)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("legenda")
    ap.add_argument("--semanas", type=int, default=3)
    a = ap.parse_args()
    nova = open(a.legenda, encoding="utf-8").read()
    pn = norm(nova)
    sems = sorted(glob.glob(BASE + "/SEM[0-9]*"), key=lambda p: int(re.sub(r"\D", "", os.path.basename(p)) or 0))[-a.semanas:]
    achou = 0
    for s in sems:
        for f in glob.glob(s + "/*/legenda.txt"):
            if os.path.abspath(f) == os.path.abspath(a.legenda):
                continue
            velha = open(f, encoding="utf-8").read()
            comum = ngramas(pn) & ngramas(norm(velha))
            # a palavra-gatilho e a promessa do SUPERCASO podem repetir; o resto não
            comum = {c for c in comum if not re.search(r"supercaso|10 60|10 a 60|novos pacientes|pacientes novos|meu time", c)}
            if comum:
                achou += 1
                print(f"⚠ {os.path.relpath(f, BASE)}: {len(comum)} trecho(s) iguais, ex.: «{sorted(comum)[0]}»")
            if pn[:1] and norm(velha)[:1] == pn[:1]:
                print(f"· mesma primeira palavra «{pn[0]}» que {os.path.relpath(f, BASE)}")
    print("sem repetição" if not achou else f"{achou} legenda(s) com frase reciclada")


if __name__ == "__main__":
    main()
