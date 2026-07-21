#!/bin/zsh
# Radar de trends quentes — roda a skill radar-trends-quentes headless (diário, 07:20)
# e avisa o Sávio (Slack; fallback: notificação macOS). Disparado pelo LaunchAgent
# com.reconecta.radar-quente. Desligar:
#   launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.reconecta.radar-quente.plist
#
# Slack: token e canal vêm do ambiente ($SLACK_BOT_TOKEN / $RADAR_SLACK_CHANNEL) OU,
# de preferência, do Keychain do macOS (persistente entre reinícios, nunca em arquivo):
#   security add-generic-password -s reconecta-slack -a bot-token -w 'xoxb-...' -U
#   security add-generic-password -s reconecta-slack -a radar-channel -w 'C0XXXXXXX' -U
# Token inválido/ausente → fallback pra notificação do macOS + log (o radar roda igual).
# Modelo: opus (o julgamento da ponte é o núcleo do radar — decisão 21/jul/26).

export PATH="/Users/saviomoraes/.local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
BASE="/Users/saviomoraes/reconecta"
LOGDIR="$BASE/agente-carrosseis/logs"
RADAR_JSON="$BASE/agente-carrosseis/data/radar-quente.json"
mkdir -p "$LOGDIR"
cd "$BASE" || exit 1

log() { echo "$1" >> "$LOGDIR/radar.log" }
log "=== radar-trends-quentes $(date '+%Y-%m-%d %H:%M') ==="

# --- rodar com retry (2 tentativas extras; o runner evergreen já morreu 2x por timeout) ---
ok=""
for tentativa in 1 2 3; do
  claude -p "Use a skill radar-trends-quentes: varredura do dia, filtro RADAR, mini-ponte dos aprovados, grave agente-carrosseis/data/radar-quente.json e imprima o resumo (Passo 5). NAO produza carrossel." \
    --permission-mode bypassPermissions \
    --model opus \
    --max-budget-usd 6 \
    --allowedTools "WebSearch WebFetch Read Write Bash" \
    >> "$LOGDIR/radar.log" 2>> "$LOGDIR/radar_error.log"
  if [ $? -eq 0 ]; then ok=1; break; fi
  log "--- tentativa $tentativa falhou; aguardando 120s ---"
  sleep 120
done

notifica_mac() {
  /usr/bin/osascript -e "display notification \"$1\" with title \"Radar de trends\" sound name \"Glass\"" 2>/dev/null
}

if [ -z "$ok" ]; then
  log "--- RADAR FALHOU nas 3 tentativas ---"
  notifica_mac "Radar FALHOU 3x hoje — ver logs/radar_error.log"
  exit 1
fi

# --- montar o aviso a partir do json (determinístico, sem depender do modelo) ---
MSG=$(python3 - "$RADAR_JSON" <<'PYEOF'
import json, sys
try:
    d = json.load(open(sys.argv[1]))
except Exception:
    print("Radar rodou mas o radar-quente.json não parseia — conferir."); sys.exit(0)
# <!channel> = @canal do Slack — SÓ quando há candidato (pedido do Sávio, 21/jul);
# no "sem candidato hoje" ninguém é marcado.
def curto(t, n=110):
    t = str(t or '').strip().replace('\n', ' ')
    return t if len(t) <= n else t[:n].rsplit(' ', 1)[0] + '…'
prefixo = "<!channel> " if d.get('alerta') and d.get('candidatos') else ""
linhas = [f"{prefixo}📡 Radar {d.get('rodado_em','')}: {d.get('resumo_1_linha','?')}"]
for c in d.get('candidatos', [])[:2]:
    mp = c.get('mini_ponte', {})
    r = c.get('rubrica', {})
    linhas.append(f"• {c.get('titulo','?')} (postável até {c.get('postavel_ate','?')})")
    linhas.append(f"  ✔ por quê: estourou {c.get('estourou_em','?')} · ponte: {r.get('ponte','?')} · risco de marca: {r.get('risco_marca','?')}")
    hero = mp.get('hero_candidato','').replace('\n',' / ')
    if hero: linhas.append(f"  hero: {hero}")
# justificativa dos que ficaram DE FORA (pedido do Sávio, 21/jul: o radar sempre
# explica por que X entrou e os outros temas em alta não)
desc = d.get('descartados', [])
if desc:
    linhas.append("🗑 Por que os outros temas em alta não entraram:")
    for x in desc[:8]:
        linhas.append(f"• {curto(x.get('tema',''), 70)} → {curto(x.get('motivo',''))}")
    if len(desc) > 8:
        linhas.append(f"(+{len(desc)-8} descartes no radar-quente.json)")
print("\n".join(linhas))
PYEOF
)
log "$MSG"

# --- avisar: Slack se der, senão notificação macOS ---
# KEYCHAIN VENCE o env (bug 21/jul: o env ainda carregava o token morto do bot antigo
# via launchctl setenv e o script preferia ele). Env é só fallback.
KC_TOKEN=$(security find-generic-password -s reconecta-slack -a bot-token -w 2>/dev/null)
KC_CHANNEL=$(security find-generic-password -s reconecta-slack -a radar-channel -w 2>/dev/null)
SLACK_BOT_TOKEN="${KC_TOKEN:-$SLACK_BOT_TOKEN}"
RADAR_SLACK_CHANNEL="${KC_CHANNEL:-$RADAR_SLACK_CHANNEL}"
export RADAR_SLACK_CHANNEL
enviado=""
if [ -n "$SLACK_BOT_TOKEN" ] && [ -n "$RADAR_SLACK_CHANNEL" ]; then
  resp=$(curl -s -X POST https://slack.com/api/chat.postMessage \
    -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
    -H "Content-Type: application/json; charset=utf-8" \
    -d "$(python3 -c "import json,os,sys; print(json.dumps({'channel': os.environ['RADAR_SLACK_CHANNEL'], 'text': sys.argv[1]}))" "$MSG")")
  if echo "$resp" | grep -q '"ok":true'; then
    enviado=1; log "--- aviso enviado no Slack ($RADAR_SLACK_CHANNEL) ---"
  else
    log "--- Slack falhou: $(echo "$resp" | head -c 200) ---"
  fi
fi
if [ -z "$enviado" ]; then
  notifica_mac "$(echo "$MSG" | head -2 | tail -1)"
  log "--- aviso via notificação macOS (Slack indisponível) ---"
fi

log "--- fim ok $(date '+%H:%M') ---"
