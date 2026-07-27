#!/bin/zsh
# Análise semanal do Instagram (segunda 07:50) — puxa insights da semana anterior
# via MCP meta-insights (@mikusnuz/meta-mcp, Graph API v25), analisa e posta no
# Slack. Disparado pelo LaunchAgent com.reconecta.analise-semanal. Desligar:
#   launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.reconecta.analise-semanal.plist
#
# Credenciais (Keychain, nunca em arquivo):
#   reconecta-meta/insights-token + reconecta-meta/ig-user-id  (Graph API)
#   reconecta-slack/bot-token + reconecta-slack/radar-channel  (aviso)
# Sem token Meta → modo degradado: avisa no Slack que a análise precisa do token
# e usa o que houver em data/perf-manual.json.

export PATH="/Users/saviomoraes/.local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
BASE="/Users/saviomoraes/reconecta"
LOGDIR="$BASE/agente-carrosseis/logs"
OUTDIR="$BASE/agente-carrosseis/data/analise-semanal"
mkdir -p "$LOGDIR" "$OUTDIR"
cd "$BASE" || exit 1

SEMANA=$(date -v-7d '+%V')   # semana ISO da SEMANA ANTERIOR (a analisada)
OUT_JSON="$OUTDIR/SEM${SEMANA}.json"
OUT_RESUMO="$OUTDIR/SEM${SEMANA}-resumo.txt"

log() { echo "$1" >> "$LOGDIR/analise-semanal.log" }
log "=== analise-semanal SEM${SEMANA} $(date '+%Y-%m-%d %H:%M') ==="

PROMPT="Análise semanal do Instagram RECONECTA (SEM${SEMANA}, a semana que acabou).
1. Use as ferramentas do MCP meta-insights: liste as mídias dos últimos 14 dias e puxe os insights por post (views, reach, saved, shares, likes, comments, follows, profile_visits) e os da conta (reach com breakdown de seguidor/não-seguidor se disponível).
2. Se o MCP falhar por falta de credencial, use agente-carrosseis/data/perf-manual.json e diga claramente no resumo que a análise está em modo degradado aguardando o token Meta.
3. Calcule por post: s/r (shares/reach), saves/reach, follows. Ranqueie a semana, compare com os 16 hits históricos (agente-carrosseis/data/carousels_perf.json) e com a semana anterior em data/analise-semanal/ se existir.
4. Extraia os ELEMENTOS vencedores reaplicáveis (fórmula de capa, mecânica de prova, arquitetura, CTA) — nunca temas prontos (regra: conteúdo novo nasce do zero).
5. Grave o relatório completo em ${OUT_JSON} (JSON válido) e um resumo de ATÉ 12 linhas pro Slack em ${OUT_RESUMO} (texto puro, sem markdown pesado): top 3 posts com s/r, o que aprendemos, 2-3 recomendações objetivas pra semana atual.
NÃO produza carrossel. NÃO edite posts."

ok=""
for tentativa in 1 2 3; do
  claude -p "$PROMPT" \
    --permission-mode bypassPermissions \
    --model opus \
    >> "$LOGDIR/analise-semanal.log" 2>&1
  if [ -f "$OUT_RESUMO" ] && [ -s "$OUT_RESUMO" ]; then ok="1"; break; fi
  log "tentativa $tentativa falhou; aguardando 120s"
  sleep 120
done

# --- aviso no Slack (Keychain VENCE env) ---
SLACK_TOKEN="$(security find-generic-password -s reconecta-slack -a bot-token -w 2>/dev/null)"
SLACK_CHANNEL="$(security find-generic-password -s reconecta-slack -a radar-channel -w 2>/dev/null)"

if [ -n "$ok" ]; then
  TITULO="📊 Análise semanal SEM${SEMANA} — Instagram"
  CORPO="$(cat "$OUT_RESUMO")"
else
  TITULO="⚠️ Análise semanal SEM${SEMANA} FALHOU"
  CORPO="O runner tentou 3x e não produziu resumo. Ver logs/analise-semanal.log"
fi

if [ -n "$SLACK_TOKEN" ] && [ -n "$SLACK_CHANNEL" ]; then
  python3 - "$SLACK_TOKEN" "$SLACK_CHANNEL" "$TITULO" "$CORPO" <<'EOF' >> "$LOGDIR/analise-semanal.log" 2>&1
import json, sys, urllib.request
token, channel, titulo, corpo = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
blocks = [
    {"type": "header", "text": {"type": "plain_text", "text": titulo[:150]}},
    {"type": "section", "text": {"type": "mrkdwn", "text": corpo[:2900]}},
    {"type": "context", "elements": [{"type": "mrkdwn",
        "text": "análise completa em agente-carrosseis/data/analise-semanal/"}]},
]
payload = {"channel": channel, "text": titulo, "blocks": blocks,
           "username": "Leo Diaz Reconecta"}
req = urllib.request.Request("https://slack.com/api/chat.postMessage",
    data=json.dumps(payload).encode(),
    headers={"Authorization": f"Bearer {token}",
             "Content-Type": "application/json; charset=utf-8"})
print(urllib.request.urlopen(req).read().decode()[:300])
EOF
else
  osascript -e "display notification \"$TITULO\" with title \"Análise semanal RECONECTA\"" 2>/dev/null
fi
log "--- fim $(date '+%H:%M') ---"
