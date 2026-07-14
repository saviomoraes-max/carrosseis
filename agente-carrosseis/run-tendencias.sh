#!/bin/zsh
# Roda a skill tendencias-research headless e grava a fila em data/trends-queue.json.
# Disparado pelo LaunchAgent com.reconecta.tendencias (Seg/Qua/Sex 07:30).
# Desligar: launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.reconecta.tendencias.plist

export PATH="/Users/saviomoraes/.local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
LOGDIR="/Users/saviomoraes/reconecta/agente-carrosseis/logs"
mkdir -p "$LOGDIR"
cd /Users/saviomoraes/reconecta || exit 1

echo "=== tendencias-research $(date '+%Y-%m-%d %H:%M') ===" >> "$LOGDIR/tendencias.log"

claude -p "Use a skill tendencias-research: colete assuntos em alta relevantes ao nosso nicho (negocio de clinica/estetica, comportamento de consumo, captacao), rode CADA candidato pelo agente-carrosseis/relevance-filter.json, e grave a fila em agente-carrosseis/data/trends-queue.json (aprovados priorizados + descartados com motivo). NAO gere carrossel, so a fila." \
  --permission-mode bypassPermissions \
  --model sonnet \
  --max-budget-usd 2 \
  --allowedTools "WebSearch WebFetch Read Write Bash" \
  >> "$LOGDIR/tendencias.log" 2>> "$LOGDIR/tendencias_error.log"

echo "--- fim (exit $?) ---" >> "$LOGDIR/tendencias.log"
