#!/bin/zsh
# Wrapper do coletor de métricas do Instagram (script oficial do time, via Meta
# Graph API). Existe por um motivo só: o Python desta máquina é o do Homebrew
# (3.14, PEP 668), então `pip3 install requests` global é BLOQUEADO pelo sistema.
# As dependências vivem num venv aqui do lado e este wrapper chama o Python dele.
#
# Uso (mesmos argumentos do script original):
#   ./coletar.sh --check-token
#   ./coletar.sh --dias 30
#
# Token: ~/.config/meta-api/token (arquivo 600, fora do repo, nunca commitado).

DIR="${0:A:h}"
PY="$DIR/.venv/bin/python"
SCRIPT="$DIR/coletar_metricas_instagram.py"
TOKEN="$HOME/.config/meta-api/token"

if [ ! -x "$PY" ]; then
  echo "ERRO: venv ausente em $DIR/.venv" >&2
  echo "  criar com: python3 -m venv .venv && ./.venv/bin/pip install requests" >&2
  exit 1
fi

if [ ! -f "$SCRIPT" ]; then
  echo "ERRO: coletar_metricas_instagram.py não está em $DIR" >&2
  echo "  o script vem do time (Jardel) por canal seguro — salvar aqui e rodar de novo." >&2
  exit 1
fi

if [ ! -f "$TOKEN" ]; then
  echo "ERRO: token ausente em $TOKEN" >&2
  echo "  colar o token (sem quebra de linha) e rodar: chmod 600 $TOKEN" >&2
  exit 1
fi

# permissão do token: se estiver frouxa, apertar antes de usar (não avisar só)
PERM="$(stat -f '%Lp' "$TOKEN" 2>/dev/null)"
if [ "$PERM" != "600" ]; then
  chmod 600 "$TOKEN"
  echo "aviso: permissão do token era $PERM; corrigida para 600." >&2
fi

exec "$PY" "$SCRIPT" "$@"
