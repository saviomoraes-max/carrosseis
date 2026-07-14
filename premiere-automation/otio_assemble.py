#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
otio_assemble.py — RECONECTA (Rota A, 100% offline)

Lê ad_spec.json, monta a timeline com OpenTimelineIO e escreve o XML no formato
MAIS CONFIÁVEL pro Premiere Pro 2025/2026:

    FCP7 XML  (adapter 'fcp_xml', extensão .xml, raiz <xmeml>)  <- ROTA SEGURA

O Premiere atual importa esse .xml via File > Import e cria uma SEQUÊNCIA
EDITÁVEL com os clips na track, cada um com in/out e posição corretos.
O Premiere NÃO importa .fcpxml (Final Cut Pro X) diretamente — por isso o
arquivo principal é o FCP7 .xml. Se o adapter de FCPXML estiver instalado,
emitimos TAMBÉM um .fcpxml (útil pra DaVinci Resolve / Final Cut), mas ele
NÃO serve pro File > Import do Premiere.

Uso:
    python otio_assemble.py                 # lê ./ad_spec.json
    python otio_assemble.py outro_spec.json
    python otio_assemble.py ad_spec.json --out-dir saida/

Saída (por padrão na pasta do spec):
    <nome>.xml      (FCP7 / xmeml)  -> File > Import no Premiere
    <nome>.fcpxml   (FCP X)         -> só se o adapter fcpx_xml existir
"""

import argparse
import json
import os
import sys

import opentimelineio as otio


def carregar_spec(caminho_spec):
    """Lê e valida minimamente o ad_spec.json."""
    with open(caminho_spec, "r", encoding="utf-8") as arquivo:
        spec = json.load(arquivo)

    if "fps" not in spec:
        raise ValueError("ad_spec.json precisa do campo 'fps'.")
    if not spec.get("clips"):
        raise ValueError("ad_spec.json precisa de uma lista 'clips' não vazia.")
    return spec


def segundos_para_frames(segundos, fps):
    """
    Converte segundos -> frames INTEIROS no rate da timeline.

    RationalTime trabalha com FRAMES no rate dado (NÃO com segundos).
    Misturar segundos com rate, ou usar 30 onde o alvo é 29.97, causa drift.
    Por isso fechamos tudo em frames inteiros com o MESMO fps.
    """
    return round(float(segundos) * float(fps))


def tempo(frames, fps):
    """RationalTime(value=frames, rate=fps)."""
    return otio.opentime.RationalTime(frames, fps)


def faixa(start_frames, dur_frames, fps):
    """TimeRange(start_time, duration), tudo em frames @ fps."""
    return otio.opentime.TimeRange(
        start_time=tempo(start_frames, fps),
        duration=tempo(dur_frames, fps),
    )


def duracao_do_clip(clip_spec):
    """
    Resolve a duração do clip em segundos.

    Preferência: 'duracao_s' explícita. Senão, out - in. Senão, erro.
    """
    if clip_spec.get("duracao_s") is not None:
        return float(clip_spec["duracao_s"])
    if clip_spec.get("out") is not None and clip_spec.get("in") is not None:
        return float(clip_spec["out"]) - float(clip_spec["in"])
    raise ValueError(
        "Cada clip precisa de 'duracao_s' OU do par ('in','out'). "
        f"Clip problemático: {clip_spec.get('arquivo')}"
    )


def montar_timeline(spec, base_dir):
    """
    Monta a otio.schema.Timeline a partir do spec.

    Estratégia de posicionamento: o adapter fcp_xml escreve a track na ordem
    dos itens. Para respeitar 'posicao_s' (onde o clip começa na timeline),
    inserimos Gaps (espaços vazios) entre os clips quando há buraco. Assumimos
    clips na mesma track já ordenados por posicao_s e sem sobreposição.
    """
    fps = float(spec["fps"])

    timeline = otio.schema.Timeline(name=spec.get("nome", "timeline_reconecta"))
    # Trava o rate global da timeline (start em 0 no rate certo).
    timeline.global_start_time = tempo(0, fps)

    # Agrupa clips por track de vídeo (1 = V1, 2 = V2, ...).
    clips_por_track = {}
    for clip_spec in spec["clips"]:
        numero_track = int(clip_spec.get("track", 1))
        clips_por_track.setdefault(numero_track, []).append(clip_spec)

    # Cria as tracks em ordem crescente (V1, V2, ...).
    for numero_track in sorted(clips_por_track.keys()):
        track = otio.schema.Track(
            name=f"V{numero_track}",
            kind=otio.schema.TrackKind.Video,
        )
        timeline.tracks.append(track)

        # Ordena os clips desta track pela posição na timeline.
        clips_ordenados = sorted(
            clips_por_track[numero_track],
            key=lambda c: float(c.get("posicao_s", 0.0)),
        )

        # Cursor (em frames) da posição já preenchida nesta track.
        cursor_frames = 0

        for clip_spec in clips_ordenados:
            posicao_frames = segundos_para_frames(
                clip_spec.get("posicao_s", 0.0), fps
            )

            # Se o clip começa depois do cursor, preenche o buraco com um Gap.
            if posicao_frames > cursor_frames:
                gap_frames = posicao_frames - cursor_frames
                track.append(
                    otio.schema.Gap(source_range=faixa(0, gap_frames, fps))
                )
                cursor_frames = posicao_frames
            elif posicao_frames < cursor_frames:
                raise ValueError(
                    f"Sobreposição/posição inválida na track V{numero_track}: "
                    f"clip '{clip_spec.get('arquivo')}' começa em "
                    f"{clip_spec.get('posicao_s')}s, antes do cursor atual."
                )

            in_segundos = float(clip_spec.get("in", 0.0))
            dur_segundos = duracao_do_clip(clip_spec)

            in_frames = segundos_para_frames(in_segundos, fps)
            dur_frames = segundos_para_frames(dur_segundos, fps)

            # Caminho absoluto da mídia (relativo ao spec).
            caminho_rel = clip_spec["arquivo"]
            caminho_abs = os.path.abspath(os.path.join(base_dir, caminho_rel))

            # target_url = file:// absoluto. url_from_filepath faz o
            # percent-encoding correto (lida com espaços/acentos, ex.:
            # /Volumes/SSD kenipe/...). NÃO montar file:// na mão.
            url_midia = otio.url_utils.url_from_filepath(caminho_abs)

            # available_range = o trecho de mídia que existe no arquivo.
            # Cobrimos do início (0) até in + duração, garantindo que o
            # source_range usado cai dentro do disponível.
            media = otio.schema.ExternalReference(
                target_url=url_midia,
                available_range=faixa(0, in_frames + dur_frames, fps),
            )

            clip = otio.schema.Clip(
                name=os.path.basename(caminho_rel),
                media_reference=media,
                # source_range = trecho da MÍDIA usado: in point + duração.
                source_range=faixa(in_frames, dur_frames, fps),
            )
            track.append(clip)
            cursor_frames += dur_frames

    return timeline


def adapters_disponiveis():
    """Lista os nomes de adapters ativos no ambiente."""
    return [a.name for a in otio.plugins.ActiveManifest().adapters]


def main():
    parser = argparse.ArgumentParser(
        description="Monta timeline OTIO e gera FCP7 XML (+ FCPXML se possível)."
    )
    parser.add_argument(
        "spec",
        nargs="?",
        default="ad_spec.json",
        help="Caminho do ad_spec.json (padrão: ./ad_spec.json).",
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help="Pasta de saída (padrão: mesma pasta do spec).",
    )
    args = parser.parse_args()

    caminho_spec = os.path.abspath(args.spec)
    if not os.path.isfile(caminho_spec):
        print(f"[ERRO] spec não encontrado: {caminho_spec}", file=sys.stderr)
        sys.exit(1)

    base_dir = os.path.dirname(caminho_spec)
    out_dir = os.path.abspath(args.out_dir) if args.out_dir else base_dir
    os.makedirs(out_dir, exist_ok=True)

    spec = carregar_spec(caminho_spec)
    nome = spec.get("nome", "timeline_reconecta")

    # Sanidade: adapter fcp_xml DEVE estar presente (vem no bundle Plugins).
    adapters = adapters_disponiveis()
    if "fcp_xml" not in adapters:
        print(
            "[ERRO] adapter 'fcp_xml' não encontrado.\n"
            "       Instale: pip install OpenTimelineIO-Plugins==0.18.1\n"
            f"       Adapters ativos agora: {adapters}",
            file=sys.stderr,
        )
        sys.exit(2)

    timeline = montar_timeline(spec, base_dir)

    # --- ROTA SEGURA: FCP7 XML (xmeml) -> File > Import no Premiere ---
    saida_xml = os.path.join(out_dir, f"{nome}.xml")
    otio.adapters.write_to_file(timeline, saida_xml, adapter_name="fcp_xml")
    print(f"[OK] FCP7 XML (Premiere): {saida_xml}")

    # --- OPCIONAL: FCPXML (Final Cut Pro X) — só se o adapter existir ---
    # NÃO importável direto no Premiere; útil pra DaVinci Resolve / Final Cut.
    if "fcpx_xml" in adapters:
        saida_fcpxml = os.path.join(out_dir, f"{nome}.fcpxml")
        try:
            otio.adapters.write_to_file(
                timeline, saida_fcpxml, adapter_name="fcpx_xml"
            )
            print(f"[OK] FCPXML (DaVinci/FCP, NÃO p/ Premiere): {saida_fcpxml}")
        except Exception as erro:  # noqa: BLE001 — só avisa, não derruba a rota A
            print(f"[AVISO] falhou ao gerar .fcpxml ({erro}). Seguindo só com .xml.")
    else:
        print(
            "[INFO] adapter 'fcpx_xml' ausente — gerando apenas o .xml (FCP7), "
            "que é o que o Premiere importa. (Opcional: pip install "
            "otio-fcpx-xml-adapter)"
        )

    print("\nPróximo passo: Premiere Pro > File > Import > "
          f"{os.path.basename(saida_xml)}")


if __name__ == "__main__":
    main()
