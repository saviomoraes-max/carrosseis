#!/usr/bin/env bash
# install.sh — Instalador do Agente de Carrosséis RECONECTA
# Rode com: bash agentes/carrossel/install.sh (a partir da raiz do repo reconecta)
set -euo pipefail

# ── Cores ─────────────────────────────────────────────────────────────────────
BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
RESET='\033[0m'

ok()   { echo -e "${GREEN}  ✓${RESET} $1"; }
info() { echo -e "${CYAN}  →${RESET} $1"; }
warn() { echo -e "${YELLOW}  !${RESET} $1"; }
fail() { echo -e "${RED}  ✗${RESET} $1"; exit 1; }
ask()  { echo -e "${BOLD}$1${RESET}"; }

# ── Cabeçalho ─────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════════════╗${RESET}"
echo -e "${BOLD}║   Agente de Carrosséis RECONECTA — Instalador       ║${RESET}"
echo -e "${BOLD}╚══════════════════════════════════════════════════════╝${RESET}"
echo ""

# ── Localizar raiz do repo ────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

info "Repositório detectado em: $REPO_ROOT"

if [[ ! -f "$REPO_ROOT/CLAUDE.md" ]]; then
  fail "Execute este script a partir da raiz do repositório reconecta.\nUso: bash agentes/carrossel/install.sh"
fi

# ── Python ────────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}[1/7] Verificando Python...${RESET}"

PYTHON=""
for candidate in /opt/homebrew/bin/python3 /usr/local/bin/python3 /usr/bin/python3 python3; do
  if command -v "$candidate" &>/dev/null; then
    PYTHON="$(command -v "$candidate")"
    break
  fi
done

if [[ -z "$PYTHON" ]]; then
  fail "Python 3 não encontrado. Instale com: brew install python"
fi

PYTHON_VER="$("$PYTHON" --version 2>&1)"
ok "Python encontrado: $PYTHON ($PYTHON_VER)"

# ── Homebrew e dependências ────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}[2/7] Verificando dependências...${RESET}"

if ! command -v brew &>/dev/null; then
  warn "Homebrew não encontrado. Algumas dependências podem precisar ser instaladas manualmente."
else
  ok "Homebrew encontrado"

  if ! command -v gallery-dl &>/dev/null; then
    info "Instalando gallery-dl (coletor de imagens do Pinterest)..."
    brew install gallery-dl
  fi
  ok "gallery-dl: $(gallery-dl --version 2>&1 | head -1)"

  if ! command -v tesseract &>/dev/null; then
    info "Instalando tesseract (filtro de texto em imagens)..."
    brew install tesseract
  fi
  ok "tesseract: $(tesseract --version 2>&1 | head -1)"
fi

info "Instalando pacotes Python (pillow, pytesseract, slack_sdk)..."
"$PYTHON" -m pip install --quiet pillow pytesseract slack_sdk
ok "Pacotes Python instalados"

# ── Diretório base do agente ───────────────────────────────────────────────────
echo ""
echo -e "${BOLD}[3/7] Configurando diretório base do agente...${RESET}"
echo ""
ask "Onde você quer armazenar o banco de imagens e os carrosséis gerados?"
ask "Pode ser um SSD externo ou uma pasta local. Exemplos:"
echo "   /Volumes/SSD kenipe/agentes/carrossel  (SSD externo)"
echo "   $HOME/agentes/carrossel                (pasta local)"
echo ""
read -r -p "$(echo -e "${BOLD}  Caminho BASE [padrão: $HOME/agentes/carrossel]: ${RESET}")" BASE_INPUT

if [[ -z "$BASE_INPUT" ]]; then
  BASE="$HOME/agentes/carrossel"
else
  BASE="$BASE_INPUT"
fi

info "Criando estrutura de pastas em: $BASE"
mkdir -p "$BASE/bank" "$BASE/provas_sociais" "$BASE/logs"
ok "Pastas criadas"

# ── Copiar scripts ─────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}[4/7] Copiando scripts para $BASE...${RESET}"

for script in agente_carrosseis.py pinterest_collector.py slack_collector.py build_template.py.txt; do
  cp "$SCRIPT_DIR/$script" "$BASE/$script"
  ok "$script copiado"
done

# ── Criar agente.config.json ──────────────────────────────────────────────────
echo ""
echo -e "${BOLD}[5/7] Criando arquivo de configuração...${RESET}"

TEMPLATE_DIR="$REPO_ROOT/carrosseis/_template"
NOISE_SRC="$REPO_ROOT/carrosseis/ad004-1paciente/img/noise.png"

# Config no SSD (usado pelos scripts Python)
CONFIG_SSD="$BASE/agente.config.json"
cat > "$CONFIG_SSD" <<EOF
{
  "BASE": "$BASE",
  "TEMPLATE_DIR": "$TEMPLATE_DIR",
  "NOISE_SRC": "$NOISE_SRC",
  "PYTHON": "$PYTHON"
}
EOF
ok "Config criado em $CONFIG_SSD"

# Config no repo (usado pelo Claude Code para ler paths na sessão)
CONFIG_REPO="$REPO_ROOT/agentes/carrossel/agente.config.json"
cat > "$CONFIG_REPO" <<EOF
{
  "BASE": "$BASE",
  "TEMPLATE_DIR": "$TEMPLATE_DIR",
  "NOISE_SRC": "$NOISE_SRC",
  "PYTHON": "$PYTHON"
}
EOF
ok "Config criado em $CONFIG_REPO"

# ── Skill no Claude Code ──────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}[6/7] Instalando skill no Claude Code...${RESET}"

SKILL_DST="$HOME/.claude/skills/carrossel-reconecta"
mkdir -p "$SKILL_DST"
cp "$REPO_ROOT/.claude/skills/carrossel-reconecta/skill.md" "$SKILL_DST/skill.md"
ok "Skill instalada em $SKILL_DST/skill.md"
info "Reinicie o Claude Code para ativar a skill."

# ── Banco de imagens inicial ──────────────────────────────────────────────────
echo ""
echo -e "${BOLD}[7/7] Banco de imagens inicial...${RESET}"
echo ""
ask "Deseja popular o banco de imagens agora?"
ask "Isso vai coletar ~42 fotos do Pinterest (pode levar 2–3 minutos)."
read -r -p "$(echo -e "${BOLD}  Rodar agora? [s/N]: ${RESET}")" RUN_COLLECTOR

if [[ "${RUN_COLLECTOR,,}" == "s" ]]; then
  info "Rodando pinterest_collector.py..."
  "$PYTHON" "$BASE/pinterest_collector.py" && ok "Banco de imagens populado!" || warn "Coleta falhou — rode manualmente depois: python3 $BASE/pinterest_collector.py"
else
  warn "Banco vazio. Antes de criar carrosséis, rode:"
  warn "  python3 \"$BASE/pinterest_collector.py\""
fi

# ── Resumo final ──────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════════════╗${RESET}"
echo -e "${BOLD}║   Instalação concluída!                              ║${RESET}"
echo -e "${BOLD}╚══════════════════════════════════════════════════════╝${RESET}"
echo ""
echo -e "  ${CYAN}Base do agente:${RESET}  $BASE"
echo -e "  ${CYAN}Template:${RESET}        $TEMPLATE_DIR"
echo -e "  ${CYAN}Python:${RESET}          $PYTHON"
echo -e "  ${CYAN}Skill:${RESET}           $SKILL_DST"
echo ""
echo -e "  ${GREEN}Próximos passos:${RESET}"
echo "  1. Reinicie o Claude Code"
echo "  2. Autentique os MCPs: Adobe, Instagram e Slack"
echo "  3. Digite: \"cria 7 carrosséis\""
echo ""
echo -e "  Dúvidas? Veja: $REPO_ROOT/agentes/carrossel/SETUP.md"
echo ""
