#!/bin/zsh
# Pulso de trends — aviso de HORA EM HORA no Slack com os trending topics do
# Twitter/X (Brasil + Mundo), o Google "trending now" (Brasil) e as fofocas do
# Portal Leo Dias, liderado pelo que SUBIU/é novo desde a última rodada + nota da
# IA barata (haiku) nos quentes. Disparado pelo LaunchAgent com.reconecta.trends-
# pulse (StartCalendarInterval Minute=0 => todo HH:00, 24/7). É SEPARADO do radar
# curado diário 07:20. Desligar:
#   launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.reconecta.trends-pulse.plist
#
# Slack: token e canal vêm do KEYCHAIN (mesmas chaves do radar). Keychain VENCE o
# env. O token vai pro curl via STDIN (nunca no argv/ps, nunca no log). O motor
# (trends_pulse.py) monta o payload e grava o estado NOVO em .pending; aqui só o
# promovemos pra trends-pulse-state.json DEPOIS de o Slack confirmar (senão uma
# queda de Slack consumiria os movers da hora e a onda sumiria).

export PATH="/Users/saviomoraes/.local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
BASE="/Users/saviomoraes/reconecta"
LOGDIR="$BASE/agente-carrosseis/logs"
DATA="$BASE/agente-carrosseis/data"
STATE="$DATA/trends-pulse-state.json"
STATE_PENDING="$STATE.pending"
ALERT_MARKER="$LOGDIR/.pulse-fail-alerted"
LOGFILE="$LOGDIR/trends-pulse.log"
mkdir -p "$LOGDIR"
cd "$BASE" || exit 1

# rotação simples: mantém o log num teto (job 24/7 append-only cresceria sem fim)
if [ -f "$LOGFILE" ] && [ "$(wc -c < "$LOGFILE")" -gt 2000000 ]; then
  tail -n 2000 "$LOGFILE" > "$LOGFILE.tmp" 2>/dev/null && mv "$LOGFILE.tmp" "$LOGFILE"
fi

log() { echo "$1" >> "$LOGFILE" }
log "=== trends-pulse $(date '+%Y-%m-%d %H:%M') ==="

# payload por execução (evita corrida se rodarem à mão junto com o LaunchAgent)
PAYLOAD=$(mktemp "$LOGDIR/.pulse-payload.XXXXXX.json") || exit 1
trap 'rm -f "$PAYLOAD"' EXIT

# notificação macOS via argv (aspas/backslash no texto não quebram o AppleScript)
notifica_mac() {
  /usr/bin/osascript - "$1" <<'APPLESCRIPT' 2>/dev/null
on run argv
  display notification (item 1 of argv) with title "Pulso de trends" sound name "Pop"
end run
APPLESCRIPT
}

# --- chaves (Keychain vence o env) ---
KC_TOKEN=$(security find-generic-password -s reconecta-slack -a bot-token -w 2>/dev/null)
KC_CHANNEL=$(security find-generic-password -s reconecta-slack -a radar-channel -w 2>/dev/null)
SLACK_BOT_TOKEN="${KC_TOKEN:-$SLACK_BOT_TOKEN}"
PULSE_SLACK_CHANNEL="${KC_CHANNEL:-$PULSE_SLACK_CHANNEL}"
export PULSE_SLACK_CHANNEL

# posta o payload JSON no Slack; token via stdin (fora do argv). Devolve 0 se ok.
post_payload() {
  [ -n "$SLACK_BOT_TOKEN" ] && [ -n "$PULSE_SLACK_CHANNEL" ] || return 1
  local resp
  resp=$(printf 'Authorization: Bearer %s\n' "$SLACK_BOT_TOKEN" \
    | curl -s -X POST https://slack.com/api/chat.postMessage \
        -H @- -H "Content-Type: application/json; charset=utf-8" \
        --data-binary @"$PAYLOAD")
  echo "$resp" | grep -q '"ok":true' && return 0
  log "--- Slack falhou: $(echo "$resp" | head -c 200) ---"
  return 1
}

# posta uma mensagem de texto simples (usado no alerta de falha total)
post_texto() {
  [ -n "$SLACK_BOT_TOKEN" ] && [ -n "$PULSE_SLACK_CHANNEL" ] || return 1
  local body
  body=$(python3 -c 'import json,sys;print(json.dumps({"channel":sys.argv[1],"text":sys.argv[2]}))' \
         "$PULSE_SLACK_CHANNEL" "$1") || return 1
  printf 'Authorization: Bearer %s\n' "$SLACK_BOT_TOKEN" \
    | curl -s -X POST https://slack.com/api/chat.postMessage \
        -H @- -H "Content-Type: application/json; charset=utf-8" \
        --data-binary "$body" | grep -q '"ok":true'
}

# --- rodar o motor (fetch + parse + velocidade + IA + payload) ---
RESUMO=$(python3 "$BASE/agente-carrosseis/trends_pulse.py" "$PAYLOAD" 2>> "$LOGFILE")
rc=$?
log "resumo: $RESUMO (rc=$rc)"

# --- falha (fontes fora ou erro): NÃO some em silêncio; alerta no Slack (máx 1x/3h) ---
if [ $rc -ne 0 ] || [ ! -s "$PAYLOAD" ]; then
  log "--- sem payload (fontes fora ou erro) ---"
  if [ -z "$(find "$ALERT_MARKER" -mmin -180 2>/dev/null)" ]; then
    if post_texto "⚠️ *Pulso de trends*: sem dados nesta rodada (fontes fora do ar ou erro). Ver \`logs/trends-pulse.log\`."; then
      touch "$ALERT_MARKER"; log "--- alerta de falha postado no Slack ---"
    fi
  fi
  notifica_mac "Pulso de trends: sem dados — ver logs/trends-pulse.log"
  exit 1
fi

rm -f "$ALERT_MARKER"   # teve dados: zera o throttle de alerta

# --- postar: Slack se der, senão notificação macOS ---
if post_payload; then
  log "--- aviso enviado no Slack ---"
  # só avança o estado de velocidade DEPOIS de entregar (senão a onda some)
  [ -f "$STATE_PENDING" ] && mv -f "$STATE_PENDING" "$STATE"
else
  notifica_mac "$RESUMO"
  log "--- aviso via notificação macOS (Slack indisponível); estado NÃO avançado ---"
fi

log "--- fim ok $(date '+%H:%M') ---"
