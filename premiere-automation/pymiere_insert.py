#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pymiere_insert.py — RECONECTA (Rota B, exige Premiere ABERTO + Pymiere Link)

Importa os 3 clips do ad_spec.json e os insere na SEQUÊNCIA ATIVA do Premiere,
cada um no timestamp 'posicao_s' do spec.

Pré-requisitos (ver README, seção "Rota B"):
  1. Premiere Pro ABERTO com um projeto e uma sequência ativa.
  2. Extensão CEP "Pymiere Link" instalada e o painel aberto pelo menos uma vez
     (Window > Extensions > Pymiere Link) — é ele que sobe o servidor HTTP que
     o pymiere usa.
  3. PlayerDebugMode habilitado na chave CSXS da sua versão do Premiere
     (CSXS.12 p/ Premiere 2025+), com killall cfprefsd && killall Finder.

Limitações conhecidas (dos fatos verificados):
  - Áudio linkado pode NÃO acompanhar o insertClip (aviso da própria Adobe).
  - pymiere roda ExtendScript ES3 por baixo; cada chamada é um round-trip HTTP.
  - pymiere testado oficialmente até Premiere 23.1; em 25.x validar caso a caso.

Uso:
    python pymiere_insert.py                # lê ./ad_spec.json
    python pymiere_insert.py outro_spec.json
"""

import json
import os
import sys
import time


def carregar_spec(caminho_spec):
    with open(caminho_spec, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def main():
    caminho_spec = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "ad_spec.json")
    if not os.path.isfile(caminho_spec):
        print(f"[ERRO] spec não encontrado: {caminho_spec}")
        sys.exit(1)

    base_dir = os.path.dirname(caminho_spec)
    spec = carregar_spec(caminho_spec)
    clips = spec.get("clips", [])
    if not clips:
        print("[ERRO] ad_spec.json sem clips.")
        sys.exit(1)

    # --- 1) Importar o pymiere (depende do pacote instalado) ---
    try:
        import pymiere
        from pymiere.wrappers import time_from_seconds
    except ImportError:
        print(
            "[ERRO] pymiere não instalado.\n"
            "       pip install pymiere   (de preferência num venv Python 3.10)\n"
            "       Veja a seção 'Rota B' do README."
        )
        sys.exit(2)

    # --- 2) Conectar ao Premiere (só resolve com o painel Pymiere Link no ar) ---
    try:
        app = pymiere.objects.app
        # Toca em algo do app pra forçar o round-trip HTTP e detectar falha cedo.
        documento_aberto = app.isDocumentOpen()
    except Exception as erro:  # noqa: BLE001
        print(
            "[ERRO] não consegui falar com o Premiere.\n"
            f"       Detalhe: {erro}\n\n"
            "       Checklist:\n"
            "       - Premiere Pro está ABERTO?\n"
            "       - Window > Extensions > Pymiere Link foi aberto ao menos 1x?\n"
            "       - PlayerDebugMode habilitado? (CSXS.12 p/ Premiere 2025+)\n"
            "         defaults write com.adobe.CSXS.12 PlayerDebugMode 1\n"
            "         killall cfprefsd ; killall Finder ; reabrir o Premiere"
        )
        sys.exit(3)

    if not documento_aberto:
        print(
            "[ERRO] nenhum projeto aberto no Premiere.\n"
            "       Abra/crie um projeto (File > New > Project) e uma sequência,\n"
            "       depois rode de novo."
        )
        sys.exit(4)

    project = app.project  # projeto ativo (NÃO app.project.project)

    # --- 3) Garantir uma sequência ativa ---
    seq = project.activeSequence
    if seq is None:
        print(
            "[ERRO] não há sequência ativa.\n"
            "       Abra uma sequência na Timeline (duplo clique numa sequence\n"
            "       do Project panel) e rode de novo."
        )
        sys.exit(5)

    print(f"[OK] conectado. Projeto e sequência ativa: '{seq.name}'.")

    # --- 4) Importar + inserir cada clip na posição do spec ---
    for indice, clip_spec in enumerate(clips, start=1):
        caminho_rel = clip_spec["arquivo"]
        caminho_abs = os.path.abspath(os.path.join(base_dir, caminho_rel))
        posicao_s = float(clip_spec.get("posicao_s", 0.0))
        numero_track = int(clip_spec.get("track", 1))

        if not os.path.isfile(caminho_abs):
            print(f"[AVISO] mídia inexistente, pulando: {caminho_abs}")
            continue

        try:
            # importFiles(list_paths, suppressUI, targetBin, importAsNumberedStills)
            project.importFiles(
                [caminho_abs],
                suppressUI=True,
                targetBin=project.getInsertionBin(),
                importAsNumberedStills=False,
            )

            # Localiza o ProjectItem recém-importado pelo caminho da mídia.
            itens = project.rootItem.findItemsMatchingMediaPath(
                caminho_abs, ignoreSubclips=False
            )
            if not itens:
                print(f"[AVISO] não localizei o item importado de {caminho_abs}.")
                continue
            clip_item = itens[0]

            # Track de vídeo destino (videoTracks é base-0; track 1 = índice 0).
            indice_track = max(0, numero_track - 1)
            if indice_track >= len(seq.videoTracks):
                print(
                    f"[AVISO] track V{numero_track} não existe na sequência "
                    f"(há {len(seq.videoTracks)}). Usando V1."
                )
                indice_track = 0
            v_track = seq.videoTracks[indice_track]

            # insertClip empurra o resto pra frente (ripple) a partir de 'at'.
            # Para sobrescrever sem empurrar, use overwriteClip(clip_item, at).
            at = time_from_seconds(posicao_s)
            v_track.insertClip(clip_item, at)

            print(
                f"[OK] clip {indice}: {os.path.basename(caminho_rel)} inserido em "
                f"{posicao_s:.2f}s na track V{numero_track}."
            )
            # Pequena folga entre round-trips HTTP (cada chamada é síncrona/lenta).
            time.sleep(0.3)

        except Exception as erro:  # noqa: BLE001
            print(
                f"[ERRO] falhou ao inserir o clip {indice} "
                f"({os.path.basename(caminho_rel)}): {erro}"
            )

    # --- 5) Salvar o projeto ---
    try:
        project.save()
        print("\n[OK] projeto salvo. Confira a Timeline no Premiere.")
    except Exception as erro:  # noqa: BLE001
        print(f"[AVISO] não consegui salvar o projeto automaticamente: {erro}")


if __name__ == "__main__":
    main()
