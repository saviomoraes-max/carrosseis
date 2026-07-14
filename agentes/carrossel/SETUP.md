# Setup — Agente de Carrosséis RECONECTA

Guia de instalação para novos membros do time. Tempo estimado: 20–30 minutos.

---

## Pré-requisitos

- macOS com Homebrew instalado
- Python 3.11+: `brew install python`
- Claude Code instalado e autenticado
- Acesso ao repositório `reconecta` no GitHub
- Acesso à conta Adobe Creative Cloud da RECONECTA
- Acesso ao workspace Slack da RECONECTA

---

## Passo 1 — Clonar o repositório

```bash
git clone https://github.com/RECONECTA/reconecta.git ~/reconecta
```

---

## Passo 2 — Criar o diretório do agente no seu SSD (ou pasta local)

O agente precisa de um diretório base para armazenar o banco de imagens, provas sociais e carrosséis gerados. Pode ser um SSD externo ou qualquer pasta local.

```bash
# Exemplo com SSD externo
mkdir -p "/Volumes/SEU_SSD/agentes/carrossel"

# Exemplo em pasta local
mkdir -p ~/agentes/carrossel
```

Copie os scripts do repositório para lá:

```bash
cp ~/reconecta/agentes/carrossel/*.py "/Volumes/SEU_SSD/agentes/carrossel/"
cp ~/reconecta/agentes/carrossel/build_template.py.txt "/Volumes/SEU_SSD/agentes/carrossel/"
```

---

## Passo 3 — Criar o arquivo de configuração

Copie o template de configuração para o diretório base do agente e preencha os caminhos do **seu** ambiente:

```bash
cp ~/reconecta/agentes/carrossel/agente.config.json.template \
   "/Volumes/SEU_SSD/agentes/carrossel/agente.config.json"
```

Edite `agente.config.json`:

```json
{
  "BASE": "/Volumes/SEU_SSD/agentes/carrossel",
  "TEMPLATE_DIR": "/Users/SEU_USUARIO/reconecta/carrosseis/_template",
  "NOISE_SRC": "/Users/SEU_USUARIO/reconecta/carrosseis/ad004-1paciente/img/noise.png",
  "PYTHON": "/opt/homebrew/bin/python3"
}
```

> O `agente.config.json` está no `.gitignore` — nunca será commitado. Cada pessoa tem o seu.

---

## Passo 4 — Também criar config dentro do repo (para o agente Claude ler)

O Claude Code lê o config a partir do repositório. Crie o mesmo arquivo dentro do repo:

```bash
cp ~/reconecta/agentes/carrossel/agente.config.json.template \
   ~/reconecta/agentes/carrossel/agente.config.json
```

Preencha com os mesmos valores do Passo 3.

---

## Passo 5 — Instalar dependências Python

```bash
pip3 install pillow pytesseract slack_sdk
```

Para o filtro de texto nas imagens (opcional mas recomendado):

```bash
brew install tesseract
```

Para o coletor do Pinterest:

```bash
brew install gallery-dl
```

---

## Passo 6 — Instalar a skill no Claude Code

Copie a skill para o diretório de skills do usuário:

```bash
mkdir -p ~/.claude/skills/carrossel-reconecta
cp ~/reconecta/.claude/skills/carrossel-reconecta/skill.md \
   ~/.claude/skills/carrossel-reconecta/skill.md
```

Reinicie o Claude Code. A skill `/carrossel-reconecta` estará disponível.

---

## Passo 7 — Autenticar MCPs necessários

No Claude Code, autentique os seguintes MCPs (peça ao Jardel os acessos):

- **Adobe for Creativity** — necessário para tratamento de imagens
- **Instagram** — necessário para análise de top performers
- **Slack** — necessário para busca de provas sociais

---

## Passo 8 — Configurar o coletor automático do Pinterest (opcional)

O `pinterest_collector.py` alimenta o banco de imagens toda semana. Para rodar automaticamente todo domingo às 08h:

```bash
# Edite o caminho do script no plist antes de instalar
cp ~/reconecta/scripts/com.reconecta.pinterest_collector.plist \
   ~/Library/LaunchAgents/

launchctl load ~/Library/LaunchAgents/com.reconecta.pinterest_collector.plist
```

Para rodar manualmente agora e popular o banco inicial:

```bash
/opt/homebrew/bin/python3 "/Volumes/SEU_SSD/agentes/carrossel/pinterest_collector.py"
```

---

## Passo 9 — Testar

Abra o Claude Code no diretório do repositório e peça:

```
Cria 1 carrossel de teste
```

O agente deve:
1. Ler o `agente.config.json`
2. Analisar o Instagram
3. Propor um tema
4. Criar a estrutura de pasta no seu SSD
5. Selecionar e tratar uma imagem via Adobe
6. Gerar o copy e o `build.py`
7. Abrir o preview no navegador

---

## Estrutura de arquivos após setup

```
{BASE}/
  bank/                  ← banco de imagens (alimentado pelo pinterest_collector)
  bank_manifest.json     ← registro de todas as imagens
  provas_sociais/        ← prints de depoimentos (alimentado pelo slack_collector)
  provas_indice.json     ← índice das provas sociais
  agente_carrosseis.py   ← CLI do agente
  pinterest_collector.py ← coletor de imagens
  slack_collector.py     ← coletor de provas sociais
  build_template.py.txt  ← template para gerar build.py de cada carrossel
  agente.config.json     ← sua configuração local (NÃO commitar)
  SEM18/                 ← carrosséis da semana 18
    erro-financeiro-dentista/
      build.py
      carousel.html
      img/hero.jpg
      slides/
```

---

## Problemas comuns

**"agente.config.json não encontrado"**
→ Você esqueceu o Passo 4. Crie o arquivo dentro do repo `~/reconecta/agentes/carrossel/`.

**"gallery-dl não encontrado"**
→ `brew install gallery-dl`

**"banco vazio"**
→ Rode `pinterest_collector.py` manualmente para popular o banco antes de criar carrosséis.

**Adobe retorna erro de autenticação**
→ Re-autentique o MCP Adobe no Claude Code (`/mcp` → Adobe for Creativity).
