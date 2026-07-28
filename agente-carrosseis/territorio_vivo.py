#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Território vivo — o mapa MECÂNICO do que os posts publicados reivindicaram.

Por que existe (28/jul/26): o mapa de território morava na cabeça de quem produzia
(ler N jsons e lembrar). O Opus seguindo checklist pega string literal; a parte que
dá pra automatizar (extrair TUDO que foi dito nos últimos 21 dias + prints usados +
fórmulas de capa) vira este JSON. A parte que continua sendo julgamento (parentesco:
"financeiro" é família de "marido") fica com o produtor + portão — mas agora sobre
um mapa completo, não sobre memória.

Uso:
  python3 territorio_vivo.py            # gera data/territorio-vivo.json + resumo
  python3 territorio_vivo.py --dias 30  # janela maior

Saída (data/territorio-vivo.json):
  posts[]        — pasta, data estimada (POSTADO.txt ou mtime), dias
  frases_4g      — todo 4-grama de slide publicado -> [posts]  (colisão literal = achado)
  punches        — todos os punches/headlines com post e idade
  fórmulas_capa  — classificação grosseira (aspa/pergunta/número/afirmação)
  prints         — números citados nos proofs (a varredura por punch)
  burns_legenda  — última frase do §4 de cada legenda (dispositivo do MANDA)
  aberturas_leg  — primeiras 6 palavras de cada § de legenda
O produtor CONSULTA este arquivo antes de escrever; o portão recebe ele no contexto.
"""

import argparse
import glob
import json
import os
import re
import unicodedata
from datetime import datetime

BASE = "/Volumes/SSD kenipe/estáticos/novos"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "territorio-vivo.json")


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9 ]", " ", s)


def data_do_post(pasta):
    """POSTADO.txt (data no texto ou mtime) > mtime do copy.json."""
    p = os.path.join(pasta, "POSTADO.txt")
    if os.path.exists(p):
        txt = open(p, encoding="utf-8", errors="replace").read()
        m = re.search(r"(\d{4}-\d{2}-\d{2})", txt)
        if m:
            return datetime.strptime(m.group(1), "%Y-%m-%d")
        return datetime.fromtimestamp(os.path.getmtime(p))
    js = glob.glob(os.path.join(pasta, "copy*.json"))
    return datetime.fromtimestamp(os.path.getmtime(js[0])) if js else None


def classifica_capa(h):
    h = h or ""
    if "“" in h or "\"" in h[:3]:
        return "aspa"
    if "?" in h:
        return "pergunta"
    if re.search(r"\d", h):
        return "numero"
    return "afirmacao"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dias", type=int, default=21)
    args = ap.parse_args()

    agora = datetime.now()
    posts, frases, punches, capas, prints, burns, aberturas = [], {}, [], [], [], [], []

    for pasta in sorted(glob.glob(os.path.join(BASE, "SEM*", "AD*"))):
        js = glob.glob(os.path.join(pasta, "copy*.json"))
        if not js:
            continue
        dt = data_do_post(pasta)
        if not dt:
            continue
        idade = (agora - dt).days
        if idade > args.dias:
            continue
        try:
            j = json.load(open(js[0], encoding="utf-8"))
        except Exception:
            continue
        nome = pasta.split("/novos/")[1]
        publicado = os.path.exists(os.path.join(pasta, "POSTADO.txt"))
        posts.append({"pasta": nome, "dias": idade, "publicado": publicado})

        for i, s in enumerate(j.get("slides", []), 1):
            head = s.get("headline") or s.get("punch") or ""
            if head:
                punches.append({"post": nome, "dias": idade, "slide": i,
                                "texto": head.replace("\n", " / ")})
            if i == 1:
                capas.append({"post": nome, "dias": idade,
                              "formula": classifica_capa(head),
                              "texto": head.replace("\n", " / ")})
            if s.get("type") == "proof":
                nums = re.findall(r"[\d][\d.,]{2,}|\d+k|\d+K", head)
                prints.append({"post": nome, "dias": idade, "punch": head.replace("\n", " / "),
                               "numeros": nums})
            blocos = [head] + (s.get("body") or [])
            for it in (s.get("items") or []):
                blocos += [it.get("title", ""), it.get("body", "")]
            for b in blocos:
                for m in re.finditer(r"(?:\S+\s+){3}\S+", norm(b)):
                    frases.setdefault(m.group(0), set()).add(nome)

        leg = j.get("legenda", "")
        if leg:
            pars = [p for p in leg.split("⠀") if p.strip()]
            for p in pars:
                palavras = p.strip().split()
                aberturas.append({"post": nome, "dias": idade,
                                  "abre": " ".join(palavras[:6])})
            if len(pars) >= 4:
                frases_p4 = re.split(r"(?<=[.!?])\s+", pars[3].strip())
                burns.append({"post": nome, "dias": idade, "burn": frases_p4[-1][:120]})

    # só 4-gramas que aparecem (colisão em potencial) — corta ruído de hapax gigante
    frases_out = {k: sorted(v) for k, v in frases.items()}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump({
        "gerado_em": agora.isoformat(timespec="seconds"),
        "janela_dias": args.dias,
        "posts": posts,
        "punches": punches,
        "formulas_capa": capas,
        "prints": prints,
        "burns_legenda": burns,
        "aberturas_legenda": aberturas,
        "frases_4g": frases_out,
    }, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print(f"território vivo: {len(posts)} posts na janela de {args.dias} dias")
    print(f"  {len(punches)} punches · {len(frases_out)} 4-gramas · "
          f"{len(prints)} proofs · {len(burns)} burns")
    print(f"  gravado em {OUT}")
    caps = {}
    for c in capas:
        caps[c["formula"]] = caps.get(c["formula"], 0) + 1
    print("  fórmulas de capa na janela:", caps)


if __name__ == "__main__":
    main()
