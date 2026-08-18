#!/bin/bash
# Instala as fontes do design system RECONECTA nesta máquina.
# Rode uma vez: bash design-system/instalar-fontes.sh
set -euo pipefail
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESTINO="$HOME/Library/Fonts"

echo "Instalando as fontes Google (Archivo Black + Figtree)..."
cp "$AQUI"/fontes/google/*.ttf "$DESTINO"/
echo "  ok — $(ls "$AQUI"/fontes/google/*.ttf | wc -l | tr -d ' ') arquivos"

# As licenciadas (Dx Monstral, Grift, Alga) vivem no template do carrossel e NÃO
# podem ser redistribuídas. Instala só se já existirem nesta máquina.
LICENCIADAS="$AQUI/../carrosseis/_template/fonts"
if [ -d "$LICENCIADAS" ]; then
  echo "Instalando as licenciadas (uso interno, confira os seats da licença)..."
  cp "$LICENCIADAS"/*.ttf "$LICENCIADAS"/*.otf "$DESTINO"/ 2>/dev/null || true
  echo "  ok"
else
  echo "Fontes licenciadas não encontradas — segue só com as Google (é o suficiente pra apresentação)."
fi

echo
echo "Pronto. Feche e reabra o PowerPoint/Keynote pra ele enxergar as fontes novas."
