#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Imagens de POST já usadas — varredura que aguenta RECORTE.

Por que existe (07/ago/26): o `prints_usados.py` usa dHash e é ótimo pra print de
depoimento (recompressão, escala), mas dHash compara um grid fixo 17x16 — se a
imagem foi RECORTADA, todo o grid desloca e a distância estoura. Foi assim que a
capa do SEM32/AD013 passou como "livre" sendo LITERALMENTE a mesma fotografia da
capa do SEM31/AD002, publicada 10 dias antes: só 40px cortados no topo, e o dHash
deu distância 66 (o limiar era 30). A diferença de pixel no alinhamento certo era
ZERO nos três canais.

Este script faz o oposto: procura a imagem candidata DENTRO das já usadas (e vice-
versa), deslizando o alinhamento. É mais lento, mas responde a pergunta certa:
"esta foto já foi ao ar, mesmo que com outro enquadramento?"

Uso:
  ./imagens_usadas.py candidata.png            # já usei essa foto (mesmo recortada)?
  ./imagens_usadas.py candidata.png --dias 45  # limita a janela dos posts comparados
"""

import argparse
import glob
import json
import os
import sys

try:
    from PIL import Image, ImageChops, ImageStat
except ImportError:
    sys.exit("ERRO: PIL não disponível (metricas-ig/.venv)")

BASE = "/Volumes/SSD kenipe/estáticos/novos"
LARGURA = 320          # normaliza a largura antes de comparar (barato e suficiente)
LIMIAR_MEAN = 6.0      # diferença média por canal abaixo disso = mesma foto


def carrega(p, largura=LARGURA):
    im = Image.open(p).convert("RGB")
    r = largura / im.size[0]
    return im.resize((largura, max(1, int(im.size[1] * r))), Image.LANCZOS)


def contida(a, b):
    """A menor desliza dentro da maior; devolve (melhor_diferença, deslocamento)."""
    if a.size[1] > b.size[1]:
        a, b = b, a
    if a.size[1] > b.size[1]:
        return 999.0, 0
    melhor = (999.0, 0)
    passo = max(1, (b.size[1] - a.size[1]) // 60 or 1)
    for off in range(0, b.size[1] - a.size[1] + 1, passo):
        d = ImageChops.difference(b.crop((0, off, a.size[0], off + a.size[1])), a)
        m = sum(ImageStat.Stat(d).mean) / 3
        if m < melhor[0]:
            melhor = (m, off)
    return melhor


def usadas(dias=None):
    """Toda imagem de slide de post produzido (hero/slide2), com data de publicação."""
    itens = []
    for f in sorted(glob.glob(os.path.join(BASE, "SEM*", "AD*", "img", "*.png"))):
        if "/._" in f or os.path.basename(f).startswith("dep"):
            continue
        pasta = os.path.dirname(os.path.dirname(f))
        post = f.split("/novos/")[1].split("/img/")[0]
        publicado = os.path.exists(os.path.join(pasta, "POSTADO.txt"))
        itens.append({"arquivo": f, "post": post, "publicado": publicado,
                      "slot": os.path.basename(f)})
    return itens


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("candidata")
    ap.add_argument("--dias", type=int, default=None)
    args = ap.parse_args()

    try:
        cand = carrega(args.candidata)
    except Exception as e:
        sys.exit(f"ERRO ao ler {args.candidata}: {e}")

    alvo = os.path.abspath(args.candidata)
    achou = False
    for it in usadas(args.dias):
        if os.path.abspath(it["arquivo"]) == alvo:
            continue
        try:
            m, off = contida(cand, carrega(it["arquivo"]))
        except Exception:
            continue
        if m <= LIMIAR_MEAN:
            marca = "PUBLICADO" if it["publicado"] else "produzido, não publicado"
            print(f"  ⚠ MESMA FOTO (dif média {m:.2f}, desloc {off}px) — "
                  f"[{marca}] {it['post']} / {it['slot']}")
            achou = True

    print("  ✓ INÉDITA — nenhuma correspondência" if not achou
          else "  → NÃO usar sem decisão explícita (mesma foto já foi ao ar)")


if __name__ == "__main__":
    main()
