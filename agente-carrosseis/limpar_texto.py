#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove TEXTO SOBREPOSTO de foto de marca (inpainting com LaMa, local e offline).

Por que existe (29/ago/26): as marcas brasileiras de beleza publicam quase só CARD
DE ANÚNCIO — foto boa com headline, bolha de comentário e "arraste" por cima. Isso
é veto de fundo (armadilha 33: texto do card brigando com o nosso). O LaMa apaga o
texto e devolve a fotografia limpa, sem rastro visível.

NÃO usa nuvem, não precisa de chave, roda em CPU. O modelo (big-lama.pt, ~200MB)
baixa sozinho na primeira execução e fica em ~/.cache/torch.

INTERPRETADOR: o venv Python 3.10 — o 3.14 do sistema não compila as dependências.
    /tmp/ia-img/bin/python3   (recriar: python3.10 -m venv <dir> && pip install simple-lama-inpainting)

Uso:
    <venv>/bin/python3 limpar_texto.py foto.jpg saida.jpg "x1,y1,x2,y2" ["x1,y1,x2,y2" ...]

As caixas são as ÁREAS DE TEXTO a apagar, em FRAÇÃO da imagem (0 a 1), o que
dispensa saber o tamanho em pixels:
    "0.33,0.10,0.83,0.28"   = da esquerda 33% ao 83%, do topo 10% ao 28%

Exemplo real (card da Natura com 3 blocos de texto):
    python3 limpar_texto.py card.jpg limpa.jpg "0.33,0.10,0.83,0.28" \
        "0.33,0.31,0.87,0.48" "0.58,0.53,0.90,0.62"

Dicas de qualidade:
 - Sobre a máscara com folga (uns 2% além do texto): sobra de letra é pior que
   sobra de máscara.
 - Texto sobre fundo liso/desfocado sai perfeito; sobre padrão complexo pode
   borrar — nesse caso, cropar é melhor que limpar.
 - SEMPRE olhar o PNG depois (armadilha 34): o LaMa erra em silêncio.
"""

import sys
from PIL import Image, ImageDraw


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    entrada, saida, caixas = sys.argv[1], sys.argv[2], sys.argv[3:]

    from simple_lama_inpainting import SimpleLama

    im = Image.open(entrada).convert("RGB")
    W, H = im.size
    mascara = Image.new("L", (W, H), 0)
    desenho = ImageDraw.Draw(mascara)
    for c in caixas:
        x1, y1, x2, y2 = [float(v) for v in c.split(",")]
        desenho.rectangle([int(W * x1), int(H * y1), int(W * x2), int(H * y2)],
                          fill=255)

    resultado = SimpleLama()(im, mascara)
    resultado.save(saida, quality=94)
    print(f"limpo: {saida} ({resultado.size[0]}x{resultado.size[1]}), "
          f"{len(caixas)} área(s) apagada(s) — CONFERIR no pixel antes de usar")


if __name__ == "__main__":
    main()
