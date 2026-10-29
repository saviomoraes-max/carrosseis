#!/usr/bin/env python3
"""Endurece a navegação do PDF depois que o Chromium fecha o arquivo.

O Chromium escreve todo link interno como DESTINO NOMEADO (`/Dest /cap-01`), resolvido por
um dicionário `/Dests` no catálogo. É PDF válido e funciona no Acrobat e no Preview, mas é a
forma MENOS compatível que existe: vários leitores de celular e alguns visualizadores web
ignoram destino nomeado e o clique não faz nada. Num livro que a leitora abre no celular,
isso é a diferença entre sumário clicável e sumário decorativo.

Este script faz três coisas:

  1. Troca cada destino nomeado por DESTINO EXPLÍCITO, com a referência direta da página
     dentro da própria anotação. Não depende de tabela nenhuma e todo leitor entende.
  2. Cria os MARCADORES do PDF (o índice lateral), com as partes e os blocos aninhados.
     Sem isso, 150 páginas se navegam só por rolagem.
  3. Liga o modo de abertura em marcadores, pra quem abrir no computador já ver o índice.

Uso: python3 linkar_pdf.py <arquivo.pdf> [indice-paginas.json] [livro.json]
     (sem argumentos além do PDF, procura os dois JSON ao lado dele e na pasta acima)
"""
import json, pathlib, sys
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, NameObject, NumberObject, NullObject


def explicitar(pdf, indice_json=None, livro_json=None):
    pdf = pathlib.Path(pdf)
    r = PdfReader(str(pdf))
    dests = r.trailer["/Root"].get("/Dests") or {}

    # nome -> índice da página (0-based), pela referência indireta que o Chromium deixou
    idx_da_pagina = {}
    for i, p in enumerate(r.pages):
        if p.indirect_reference:
            idx_da_pagina[p.indirect_reference.idnum] = i
    nome_para_idx = {}
    for nome, alvo in dests.items():
        try:
            nome_para_idx[str(nome)] = idx_da_pagina[alvo[0].idnum]
        except Exception:
            pass

    w = PdfWriter()
    w.clone_document_from_reader(r)

    trocados = mortos = externos = 0
    for pg in w.pages:
        an = pg.get("/Annots")
        if not an:
            continue
        for a in an:
            o = a.get_object()
            if o.get("/Subtype") != "/Link":
                continue
            if o.get("/A") is not None:
                externos += 1
                continue
            d = o.get("/Dest")
            if d is None:
                continue
            nome = str(d)
            if nome not in nome_para_idx:
                mortos += 1
                continue
            alvo = w.pages[nome_para_idx[nome]]
            # [página, /XYZ, esquerda, topo, zoom]. topo = altura da página: abre no começo
            # dela. zoom nulo preserva o zoom que a leitora já estava usando, que é o que
            # importa em celular.
            altura = float(alvo.mediabox.height)
            o[NameObject("/Dest")] = ArrayObject([
                alvo.indirect_reference, NameObject("/XYZ"),
                NumberObject(0), NumberObject(round(altura)), NullObject(),
            ])
            trocados += 1

    # --- marcadores ---
    raiz = pdf.parent
    ind = pathlib.Path(indice_json) if indice_json else None
    if not ind or not ind.exists():
        for c in (raiz / "indice-paginas.json", raiz.parent / "render" / "indice-paginas.json"):
            if c.exists(): ind = c; break
    liv = pathlib.Path(livro_json) if livro_json else None
    if not liv or not liv.exists():
        for c in (raiz.parent / "livro.json", raiz / "livro.json"):
            if c.exists(): liv = c; break

    marcadores = 0
    if ind and ind.exists() and liv and liv.exists():
        indice = json.loads(ind.read_text())
        L = json.loads(liv.read_text())
        sumario = L.get("sumario") or []
        titulo = {e["numero"]: e["titulo"] for e in sumario}
        ordem = [e["numero"] for e in sumario if e["numero"] in indice]

        w.add_outline_item("Capa", 0)
        w.add_outline_item("Sumário", 1)
        marcadores += 2

        # cada parte vira um pai, e os blocos dela penduram embaixo
        partes = L.get("partes") or []
        inicio_da_parte = {p["de"]: p for p in partes}
        pai = None
        for num in ordem:
            pag = indice[num]
            if num in inicio_da_parte:
                pa = inicio_da_parte[num]
                # a página-marcador da parte vem uma antes da abertura do primeiro bloco
                pai = w.add_outline_item(f'{pa["rotulo"]} · {pa["titulo"]}', max(pag - 1, 0))
                marcadores += 1
            rotulo = f'{num} · {titulo.get(num, "")}'.strip(" ·")
            w.add_outline_item(rotulo, pag, parent=pai)
            marcadores += 1
        if L.get("contracapa"):
            w.add_outline_item("Contracapa", len(w.pages) - 1)
            marcadores += 1
        w.page_mode = "/UseOutlines"

    tmp = pdf.with_suffix(".pdf.tmp")
    with open(tmp, "wb") as f:
        w.write(f)
    tmp.replace(pdf)
    print(f"linkar_pdf: {trocados} link(s) interno(s) viraram destino explícito, "
          f"{externos} externo(s) intactos, {mortos} sem alvo, {marcadores} marcador(es)")
    if mortos:
        raise SystemExit(f"ERRO: {mortos} link(s) interno(s) apontam pra um destino que não existe. "
                         "Não publique: o clique não faz nada.")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        raise SystemExit("uso: linkar_pdf.py <arquivo.pdf> [indice-paginas.json] [livro.json]")
    explicitar(a[0], a[1] if len(a) > 1 else None, a[2] if len(a) > 2 else None)
