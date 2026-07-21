#!/bin/zsh
# Roda a skill tendencias-research headless e grava a fila em data/trends-queue.json.
# Disparado pelo LaunchAgent com.reconecta.tendencias (Seg/Qua/Sex 07:30).
# Desligar: launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.reconecta.tendencias.plist

export PATH="/Users/saviomoraes/.local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
LOGDIR="/Users/saviomoraes/reconecta/agente-carrosseis/logs"
mkdir -p "$LOGDIR"
cd /Users/saviomoraes/reconecta || exit 1

echo "=== tendencias-research $(date '+%Y-%m-%d %H:%M') ===" >> "$LOGDIR/tendencias.log"

# retry: as rodadas de 17 e 20/jul morreram em "Request timed out" e a fila ficou parada
ok=""
for tentativa in 1 2 3; do
  claude -p "Use a skill tendencias-research: colete assuntos em alta relevantes ao nosso nicho (negocio de clinica/estetica, comportamento de consumo, captacao), rode CADA candidato pelo agente-carrosseis/relevance-filter.json, e grave a fila em agente-carrosseis/data/trends-queue.json (aprovados priorizados + descartados com motivo). NAO gere carrossel, so a fila." \
    --permission-mode bypassPermissions \
    --model sonnet \
    --max-budget-usd 2 \
    --allowedTools "WebSearch WebFetch Read Write Bash" \
    >> "$LOGDIR/tendencias.log" 2>> "$LOGDIR/tendencias_error.log"
  if [ $? -eq 0 ]; then ok=1; break; fi
  echo "--- tentativa $tentativa falhou; aguardando 120s ---" >> "$LOGDIR/tendencias.log"
  sleep 120
done
if [ -z "$ok" ]; then
  /usr/bin/osascript -e 'display notification "tendencias-research FALHOU 3x — ver logs/tendencias_error.log" with title "Radar de trends"' 2>/dev/null
fi

echo "--- fim (ok=${ok:-0}) ---" >> "$LOGDIR/tendencias.log"
