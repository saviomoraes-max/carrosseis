#!/bin/zsh
# Análise semanal do Instagram (segunda 07:50) — puxa insights da semana anterior,
# analisa e posta no Slack. Disparado pelo LaunchAgent com.reconecta.analise-semanal.
# Desligar:
#   launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.reconecta.analise-semanal.plist
#
# FONTE DE VERDADE: metricas-ig/historico.csv (1 linha por post por snapshot).
# Ele é alimentado por DOIS caminhos, mesmo formato:
#   A. importar_business_suite.py — export manual do Business Suite, SEM TOKEN.
#      É o padrão. Só depende de reexportar quando a janela vencer.
#   B. coletar_metricas_ig.py — Graph API, precisa de token. Automatiza e
#      acrescenta profile_visits + watch time de Reels; não traz métrica nova
#      que decida pauta. Se houver token, o runner coleta antes de analisar.
# Sem nenhum dos dois: data/perf-manual.json, modo degradado avisado no Slack.
#
# Credenciais (nunca em arquivo do repo):
#   ~/.config/meta-api/token (600)                             coletor do time
#   reconecta-meta/insights-token + ig-user-id  (Keychain)     MCP
#   reconecta-slack/bot-token + radar-channel   (Keychain)     aviso

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

# --- coleta fresca antes de analisar (snapshot do dia na curva de cada post) ---
# Só roda se houver token; sem ele o histórico é o que o export manual trouxe.
CSV="$BASE/agente-carrosseis/data/metricas-ig/historico.csv"
COLETOR="$BASE/agente-carrosseis/metricas-ig/coletar_metricas_ig.py"
TEM_TOKEN=""
security find-generic-password -s reconecta-meta -a insights-token -w >/dev/null 2>&1 \
  && TEM_TOKEN="1"
[ -f "$HOME/.config/meta-api/token" ] && TEM_TOKEN="1"

if [ -n "$TEM_TOKEN" ] && [ -x "$COLETOR" ]; then
  log "token presente; coletando métricas (--dias 14)"
  "$COLETOR" --dias 14 >> "$LOGDIR/analise-semanal.log" 2>&1 \
    || log "coleta falhou (segue com o CSV que já existir)"
else
  log "sem token: usando o histórico do export manual do Business Suite"
fi

# idade do histórico: se o post mais novo for velho, a análise tem que dizer isso
IDADE=$(python3 - "$CSV" <<'PY' 2>/dev/null
import csv, sys
from datetime import datetime
try:
    d = max(r["publicado_em"][:10] for r in csv.DictReader(open(sys.argv[1])) if r.get("publicado_em"))
    print((datetime.now() - datetime.strptime(d, "%Y-%m-%d")).days)
except Exception:
    print("")
PY
)
log "post mais recente no histórico: ${IDADE:-?} dias atrás"

PROMPT="Análise semanal do Instagram RECONECTA (SEM${SEMANA}, a semana que acabou).
1. FONTE PRIMÁRIA: ${CSV} (uma linha por post por snapshot — use o snapshot mais recente de cada post e a diferença entre snapshots pra ver a curva; filtre pela coluna conta = oleonardorosso, o resto é ruído de outras contas no export). O post mais recente do histórico tem ${IDADE:-?} dias. SE ESSE NÚMERO FOR MAIOR QUE 10, o histórico está VENCIDO: abra o resumo dizendo que a análise não cobre a semana pedida e que o Sávio precisa reexportar o CSV de Conteúdo do Business Suite (ou colocar o token). Não finja cobertura que não existe. Se o arquivo não existir, tente o MCP meta-insights; se também falhar, use agente-carrosseis/data/perf-manual.json e diga no resumo que a análise está em MODO DEGRADADO.
2. Calcule por post: s/r (shares/reach), saves/reach, follows. Ranqueie a semana, compare com os 16 hits históricos (agente-carrosseis/data/carousels_perf.json) e com a semana anterior em data/analise-semanal/ se existir.
3. REGRA DURA — a Graph API NÃO expõe retenção de 3 segundos nem % de alcance de não-seguidores POR POST (só o breakdown seguidor/não-seguidor da CONTA por dia). Se algum desses dois números entrar na análise, ele tem que vir marcado como 'manual no app' e com o valor que o Sávio informou. ESTIMAR qualquer um dos dois é proibido — na dúvida, escreva 'não disponível'.
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
