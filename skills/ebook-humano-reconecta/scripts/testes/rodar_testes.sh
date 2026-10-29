#!/usr/bin/env bash
# Roda o detector nos três textos de teste e falha se alguma faixa não bater.
#   ia_tipico.md  deve pontuar ALTO  (> 60)
#   humano.md     deve pontuar BAIXO (< 25)   (fala real transcrita da Ana Luiza)
#   misto.md      deve ficar no meio (25 a 60)
set -u
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DET="$AQUI/../detector_ptbr.py"
falhas=0

score_de() {
  python3 "$DET" "$1" --json | python3 -c 'import json,sys; print(json.load(sys.stdin)["score"])'
}

checar() {
  local arquivo="$1" min="$2" max="$3"
  local s
  s="$(score_de "$AQUI/$arquivo")"
  if [ "$s" -ge "$min" ] && [ "$s" -le "$max" ]; then
    echo "OK    $arquivo  score=$s  (esperado $min..$max)"
  else
    echo "FALHA $arquivo  score=$s  (esperado $min..$max)"
    falhas=$((falhas + 1))
  fi
}

checar ia_tipico.md 61 100
checar humano.md 0 24
checar misto.md 25 60

if [ "$falhas" -eq 0 ]; then
  echo "todos os testes passaram"
  exit 0
fi
echo "$falhas teste(s) falharam"
exit 1
