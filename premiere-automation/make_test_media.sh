#!/usr/bin/env bash
# make_test_media.sh — RECONECTA
# Gera 3 clipes de teste com ffmpeg pra ter mídia REAL pro import no Premiere.
#
# Cada clip: 5s, 30fps, 1920x1080, H.264, com COR de fundo diferente + um
# padrão de teste em movimento (contador embutido), pra dar pra ver claramente
# o corte/ordem/posição na timeline depois do import.
#
# Robusto a builds de ffmpeg SEM o filtro 'drawtext' (ex.: Homebrew sem
# libfreetype): nesse caso usa 'testsrc2' (padrão com contador embutido)
# tingido com a cor do clip. Se 'drawtext' existir, escreve um rótulo grande.
#
# Uso:
#   bash make_test_media.sh
#
# Saída: media/clip1.mp4, media/clip2.mp4, media/clip3.mp4

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEDIA_DIR="${SCRIPT_DIR}/media"
mkdir -p "${MEDIA_DIR}"

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "[ERRO] ffmpeg não encontrado. Instale com: brew install ffmpeg" >&2
  exit 1
fi

FPS=30
DUR=5
W=1920
H=1080

# Este build do ffmpeg tem o filtro drawtext?
HAS_DRAWTEXT=0
if ffmpeg -hide_banner -filters 2>/dev/null | grep -q "drawtext"; then
  HAS_DRAWTEXT=1
fi

# Acha uma fonte pro drawtext (só usada se HAS_DRAWTEXT=1).
FONT=""
for f in \
  "/System/Library/Fonts/Supplemental/Arial.ttf" \
  "/System/Library/Fonts/Helvetica.ttc" \
  "/Library/Fonts/Arial.ttf"; do
  if [ -f "$f" ]; then FONT="$f"; break; fi
done
if [ "${HAS_DRAWTEXT}" -eq 1 ] && [ -z "${FONT}" ]; then
  HAS_DRAWTEXT=0  # sem fonte, não dá pra usar drawtext de forma confiável
fi

# Gera um clip. Args: <numero> <cor_hex_solida> <rotulo>
gerar_clip() {
  local numero="$1"
  local cor="$2"
  local rotulo="$3"
  local saida="${MEDIA_DIR}/clip${numero}.mp4"

  if [ "${HAS_DRAWTEXT}" -eq 1 ]; then
    # Fundo colorido sólido + rótulo + timer (segundos via %{pts}).
    local draw="drawtext=fontfile=${FONT}:text='${rotulo}':fontcolor=white:fontsize=160:x=(w-text_w)/2:y=(h-text_h)/2-100,drawtext=fontfile=${FONT}:text='%{pts\\:hms}':fontcolor=white:fontsize=90:x=(w-text_w)/2:y=(h-text_h)/2+120"
    ffmpeg -y -hide_banner -loglevel error \
      -f lavfi -i "color=c=${cor}:s=${W}x${H}:r=${FPS}:d=${DUR}" \
      -vf "${draw}" \
      -c:v libx264 -pix_fmt yuv420p -r "${FPS}" -t "${DUR}" \
      "${saida}"
  else
    # Fallback SEM drawtext: testsrc2 (padrão + contador de frame embutido),
    # misturado com a cor do clip (blend) pra cada clip ter cor dominante única.
    ffmpeg -y -hide_banner -loglevel error \
      -f lavfi -i "testsrc2=s=${W}x${H}:r=${FPS}:d=${DUR}" \
      -f lavfi -i "color=c=${cor}:s=${W}x${H}:r=${FPS}:d=${DUR}" \
      -filter_complex "[0:v][1:v]blend=all_mode=overlay:all_opacity=0.55,format=yuv420p[v]" \
      -map "[v]" \
      -c:v libx264 -r "${FPS}" -t "${DUR}" \
      "${saida}"
  fi

  echo "[OK] ${saida}"
}

if [ "${HAS_DRAWTEXT}" -eq 0 ]; then
  echo "[INFO] ffmpeg sem 'drawtext' (ou sem fonte) — usando testsrc2 tingido."
fi

gerar_clip 1 "0x1E3A8A" "CLIP 1"   # azul
gerar_clip 2 "0x166534" "CLIP 2"   # verde
gerar_clip 3 "0x991B1B" "CLIP 3"   # vermelho

echo ""
echo "[OK] mídia de teste gerada em: ${MEDIA_DIR}"
echo "Próximo passo: python otio_assemble.py"
