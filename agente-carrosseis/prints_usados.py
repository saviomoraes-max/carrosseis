#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prints já usados — varredura POR IMAGEM, não por punch.

Por que existe (29/jul/26): a verificação de ineditismo de print era feita varrendo
os PUNCHES publicados atrás do número do print. Isso é falso-negativo por construção:
um print pode ir ao ar sem que o punch cite o número dele. Foi assim que o p06
(publicado inteiro, com nome, em SEM27/AD003) passou como "inédito" e só o portão
adversarial pegou.

Este script compara a IMAGEM: assinatura perceptual (dHash) de cada img/dep*.png de
todos os posts produzidos, e aponta colisões. Resistente a recorte leve, mudança de
escala e recompressão — que é exatamente como um print reaparece "disfarçado".

Uso:
  ./prints_usados.py                      # lista todos e aponta colisões
  ./prints_usados.py candidato.png        # esse candidato já foi ao ar?
"""

import glob
import os
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("ERRO: PIL não disponível (pip install pillow no venv de metricas-ig)")

SSD = "/Volumes/SSD kenipe/estáticos/novos"
# sem o SSD (outro membro do time): posts vivem em ./producao na raiz do repo (CLAUDE.md)
BASE = SSD if os.path.isdir(SSD) else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "producao")


def dhash(caminho, tam=16):
    """Assinatura perceptual: gradiente horizontal em 16x17 — 256 bits."""
    try:
        im = Image.open(caminho).convert("L").resize((tam + 1, tam), Image.LANCZOS)
    except Exception:
        return None
    px = im.load()
    bits = 0
    for y in range(tam):
        for x in range(tam):
            bits = (bits << 1) | (1 if px[x, y] > px[x + 1, y] else 0)
    return bits


def distancia(a, b):
    return bin(a ^ b).count("1")


def catalogo():
    """Todos os prints de todos os posts produzidos, com sua assinatura."""
    itens = []
    padroes = ["dep*.png", "depo*.png", "prova*.png", "prova*.jpg", "p[0-9]*.png"]
    arquivos = []
    for pad in padroes:
        arquivos += glob.glob(os.path.join(BASE, "SEM*", "AD*", "img", pad))
    # o padrão novo das semanas 38+ é prova-N.png; sem ele a varredura volta limpa
    # e vira um no-op (pego na auditoria de território da SEM41, 05/out/26).
    for f in sorted(set(arquivos)):
        if "/._" in f:
            continue
        h = dhash(f)
        if h is None:
            continue
        post = f.split("/novos/")[1].split("/img/")[0]
        publicado = os.path.exists(os.path.join(os.path.dirname(os.path.dirname(f)),
                                                "POSTADO.txt"))
        itens.append({"arquivo": f, "post": post, "hash": h, "publicado": publicado})
    return itens


def main():
    cat = catalogo()
    LIMIAR = 22   # ≤22 bits de 256 = mesma imagem (crop/escala/recompressão)

    if len(sys.argv) > 1:
        alvo = sys.argv[1]
        h = dhash(alvo)
        if h is None:
            sys.exit(f"ERRO: não consegui ler {alvo}")
        achou = False
        alvo_abs = os.path.abspath(alvo)
        for it in cat:
            if os.path.abspath(it["arquivo"]) == alvo_abs:
                continue          # não colidir consigo mesmo
            d = distancia(h, it["hash"])
            if d <= LIMIAR:
                marca = "PUBLICADO" if it["publicado"] else "produzido, não publicado"
                print(f"  ⚠ COLIDE (dist {d}) com [{marca}] {it['post']}")
                achou = True
        print("  ✓ INÉDITO — nenhuma colisão" if not achou else "  → NÃO usar sem decisão explícita")
        return

    print(f"{len(cat)} prints catalogados em posts produzidos\n")
    vistos = []
    colisoes = 0
    for it in cat:
        for outro in vistos:
            d = distancia(it["hash"], outro["hash"])
            if d <= LIMIAR and it["post"] != outro["post"]:
                print(f"  ⚠ {it['post'][:44]:46} == {outro['post'][:44]} (dist {d})")
                colisoes += 1
        vistos.append(it)
    print(f"\n{colisoes} colisão(ões) entre posts diferentes"
          if colisoes else "\nnenhuma colisão entre posts diferentes ✓")


if __name__ == "__main__":
    main()
