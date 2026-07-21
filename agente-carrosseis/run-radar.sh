#!/bin/zsh
# Radar de trends quentes ("Leo Diaz Reconecta" no Slack) — roda a skill
# radar-trends-quentes headless (diário, 07:20) e avisa no Slack (fallback:
# notificação macOS). Disparado pelo LaunchAgent com.reconecta.radar-quente. Desligar:
#   launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.reconecta.radar-quente.plist
#
# Slack: token e canal vêm do KEYCHAIN do macOS (persistente, nunca em arquivo):
#   security add-generic-password -s reconecta-slack -a bot-token -w 'xoxb-...' -U
#   security add-generic-password -s reconecta-slack -a radar-channel -w 'C0XXXXXXX' -U
# Keychain VENCE o env (bug 21/jul: env carregava o token morto do bot antigo).
# Token inválido/ausente → fallback pra notificação do macOS + log (o radar roda igual).
# Aviso em Block Kit (header/veredito/candidato/descartes) — legibilidade, pedido 21/jul.
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
  /usr/bin/osascript -e "display notification \"$1\" with title \"Leo Diaz Reconecta\" sound name \"Glass\"" 2>/dev/null
}

if [ -z "$ok" ]; then
  log "--- RADAR FALHOU nas 3 tentativas ---"
  notifica_mac "Radar FALHOU 3x hoje — ver logs/radar_error.log"
  exit 1
fi

# --- chaves (Keychain vence o env) ---
KC_TOKEN=$(security find-generic-password -s reconecta-slack -a bot-token -w 2>/dev/null)
KC_CHANNEL=$(security find-generic-password -s reconecta-slack -a radar-channel -w 2>/dev/null)
SLACK_BOT_TOKEN="${KC_TOKEN:-$SLACK_BOT_TOKEN}"
RADAR_SLACK_CHANNEL="${KC_CHANNEL:-$RADAR_SLACK_CHANNEL}"
export RADAR_SLACK_CHANNEL

# --- montar o aviso em Block Kit (determinístico, sem depender do modelo) ---
# Estrutura: header com data → veredito (com @canal SÓ se houver candidato) → bloco do
# candidato (janela/ponte/risco/hero) → "o que ficou de fora, e por quê" com respiro.
PAYLOAD="$LOGDIR/.radar-slack-payload.json"
RESUMO=$(python3 - "$RADAR_JSON" "$PAYLOAD" <<'PYEOF'
import json, os, sys
try:
    d = json.load(open(sys.argv[1]))
except Exception:
    print("Radar rodou mas o radar-quente.json não parseia — conferir."); sys.exit(0)

def curto(t, n=90):
    t = ' '.join(str(t or '').split())
    for sep in ('; ', ' — '):
        if sep in t and len(t) > n:
            t = t.split(sep)[0]
    return t if len(t) <= n else t[:n].rsplit(' ', 1)[0] + '…'

def tema_curto(t):
    t = ' '.join(str(t or '').split()).split(' (')[0]
    return t if len(t) <= 60 else t[:60].rsplit(' ', 1)[0] + '…'

quando = str(d.get('rodado_em', ''))
try:
    data, hora = quando.split(' ')
    _, m, dia = data.split('-')
    quando_fmt = f"{dia}/{m} às {hora.replace(':', 'h')}"
except Exception:
    quando_fmt = quando

alerta = bool(d.get('alerta') and d.get('candidatos'))
resumo = d.get('resumo_1_linha', '?')

blocks = [
    {"type": "header", "text": {"type": "plain_text", "text": f"📡 Radar de trends — {quando_fmt}", "emoji": True}},
    {"type": "section", "text": {"type": "mrkdwn", "text": ("<!channel> " if alerta else "") + f"*Veredito:* {resumo}"}},
]
for c in d.get('candidatos', [])[:2]:
    mp = c.get('mini_ponte', {}); r = c.get('rubrica', {})
    hero = mp.get('hero_candidato', '').replace('\n', ' / ')
    txt = (f"🔥 *{c.get('titulo', '?')}*\n"
           f"*Janela:* estourou {c.get('estourou_em', '?')} · postável até {c.get('postavel_ate', '?')}\n"
           f"*Ponte com a nossa dor:* {r.get('ponte', '?')}\n"
           f"*Risco de marca:* {r.get('risco_marca', '?')}")
    if hero:
        txt += f"\n*Hero rascunhada:* _{hero}_"
    blocks += [{"type": "divider"}, {"type": "section", "text": {"type": "mrkdwn", "text": txt}}]

desc = d.get('descartados', [])
if desc:
    itens = [f"• *{tema_curto(x.get('tema'))}*\n_{curto(x.get('motivo'))}_" for x in desc[:6]]
    corpo = "\n\n".join(itens)
    if len(desc) > 6:
        corpo += f"\n\n_+{len(desc) - 6} outros descartes no radar-quente.json_"
    blocks += [{"type": "divider"},
               {"type": "section", "text": {"type": "mrkdwn", "text": "*O que ficou de fora, e por quê:*\n\n" + corpo}}]

blocks.append({"type": "context", "elements": [{"type": "mrkdwn",
    "text": "Detalhes: agente-carrosseis/data/radar-quente.json · rodada automática diária às 07:20 · pra produzir: \"desembola o candidato do radar\""}]})

payload = {"channel": os.environ.get('RADAR_SLACK_CHANNEL', ''),
           "text": f"📡 Radar: {resumo}",
           "unfurl_links": False,
           "blocks": blocks}
json.dump(payload, open(sys.argv[2], 'w'), ensure_ascii=False)
print(resumo)
PYEOF
)
log "resumo: $RESUMO"

# --- avisar: Slack se der, senão notificação macOS ---
enviado=""
if [ -n "$SLACK_BOT_TOKEN" ] && [ -n "$RADAR_SLACK_CHANNEL" ] && [ -s "$PAYLOAD" ]; then
  resp=$(curl -s -X POST https://slack.com/api/chat.postMessage \
    -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
    -H "Content-Type: application/json; charset=utf-8" \
    --data-binary @"$PAYLOAD")
  if echo "$resp" | grep -q '"ok":true'; then
    enviado=1; log "--- aviso enviado no Slack (Block Kit) ---"
  else
    log "--- Slack falhou: $(echo "$resp" | head -c 200) ---"
  fi
fi
rm -f "$PAYLOAD"
if [ -z "$enviado" ]; then
  notifica_mac "$RESUMO"
  log "--- aviso via notificação macOS (Slack indisponível) ---"
fi

log "--- fim ok $(date '+%H:%M') ---"
