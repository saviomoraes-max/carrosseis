#!/bin/zsh
# Wrapper do MCP @mikusnuz/meta-mcp (insights do Instagram via Graph API v25).
# Lê as credenciais do Keychain do macOS — NUNCA colocar token em arquivo.
# Setup (uma vez, pelo Sávio):
#   security add-generic-password -s reconecta-meta -a insights-token -w 'TOKEN' -U
#   security add-generic-password -s reconecta-meta -a ig-user-id    -w 'IG_USER_ID' -U
# O token vem do System User do Business Manager (expiração "Nunca") com:
#   instagram_basic + instagram_manage_insights + pages_read_engagement

export INSTAGRAM_ACCESS_TOKEN="$(security find-generic-password -s reconecta-meta -a insights-token -w 2>/dev/null)"
export INSTAGRAM_USER_ID="$(security find-generic-password -s reconecta-meta -a ig-user-id -w 2>/dev/null)"

if [ -z "$INSTAGRAM_ACCESS_TOKEN" ] || [ -z "$INSTAGRAM_USER_ID" ]; then
  echo "ERRO: credenciais reconecta-meta ausentes no Keychain (ver cabeçalho deste script)." >&2
  exit 1
fi

exec npx -y @mikusnuz/meta-mcp
