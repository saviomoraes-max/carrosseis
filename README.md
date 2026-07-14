# RECONECTA — Agente de Conteúdo (Claude Code)

Ambiente completo do agente que produz os carrosséis e legendas do Instagram da RECONECTA na voz da nossa ex-copywriter. Clonou + abriu no Claude Code = o agente nasce sabendo o que precisa: o CLAUDE.md dá o contexto da empresa, as skills dão os fluxos, os checklists dão o padrão de qualidade e o corpus dá a voz.

## O que precisa instalar (uma vez, ~10 min)

1. **Claude Code** — [claude.com/claude-code](https://claude.com/claude-code) (app desktop ou CLI) + login com a conta Claude.
2. **Git** e **Python 3** (macOS já tem os dois).
3. **Playwright + Chromium** (motor de render dos slides):
   ```bash
   pip3 install playwright && python3 -m playwright install chromium
   ```
4. Clonar este repositório e abrir o Claude Code **dentro da pasta**:
   ```bash
   git clone <URL-DESTE-REPO> reconecta && cd reconecta && claude
   ```

## Primeira sessão (teste de fumaça)

Cole isto no Claude Code:

> Leia o CLAUDE.md, o `agente-carrosseis/checklist-producao.md` e o `agente-carrosseis/checklist-design.md`. Depois renderize o carrossel de exemplo em `carrosseis/` que tiver `copy.engine.json` e me mostre o preview.

Se o preview abrir com os 6 slides bordô, o ambiente está inteiro.

## Como usar no dia a dia

O fluxo semanal (o agente conhece os detalhes; você só conduz):

1. **Pauta** — peça: *"desembole os conteúdos dessa semana comigo"*. O agente propõe temas ancorados no corpus e na performance real, e você bate o martelo.
2. **Produção** — o agente escreve a copy (checklist de produção, 5 passes de autocrítica), roda o **portão adversarial** (agentes que tentam derrubar a copy antes de você ver) e renderiza.
3. **Imagens** — o agente cria a pasta do post com `img/NECESSARIO.txt` dizendo o que depositar; você solta as fotos lá e pede o render final.
4. **Export** — sai nomeado `[AA] [SS] [AD0NN_M] - Título.png`, com a legenda pronta em `legenda.txt`.

Regra de ouro da casa: **zero achismo** — toda frase, passo e número vem do corpus dela, de script real ou de print real. O agente sabe disso; se ele inventar, mande de volta pro checklist.

## Mapa do repositório

| Caminho | O que é |
|---|---|
| `CLAUDE.md` | Contexto da empresa, stack, regras de segurança — o agente lê sozinho |
| `agente-carrosseis/checklist-producao.md` | Autocrítica de COPY (5 passes, 19 armadilhas nomeadas) |
| `agente-carrosseis/checklist-design.md` | Autocrítica de DESIGN (régua do engine, 12 armadilhas) |
| `agente-carrosseis/portao-qualidade.md` | O juiz final (portão adversarial) |
| `agente-carrosseis/voice-dna.md` | Os 5 dispositivos da voz da copywriter + anti-padrões |
| `agente-carrosseis/checklist-legenda.md` | Anti-"bafo de IA" das legendas (7 cheiros + regras de Reels) |
| `agente-carrosseis/data/corpus.json` | Os 67 posts dela — a fonte da voz (não editar) |
| `carrosseis/_template/html-engine/engine.py` | Motor de render (copy.engine.json → 6 PNGs 1080×1350) |
| `carrosseis/_template/fonts/` | Fontes da marca (o engine acha sozinho) |
| `.claude/skills/` | As skills do agente (pauta, roteiro, copy, revisão, design, social) |
| `producao/` | SEUS posts produzidos (local, fora do git) — ver CLAUDE.md |

## O que NÃO vem no clone (e tudo bem)

- **Os posts já publicados e prints de prova** vivem no SSD do Sávio. Você produz na sua pasta `producao/` local. Se precisar do histórico/canon visual, peça ao Sávio a pasta `SEM24/AD005` (o padrão-ouro de hero) e o export das semanas recentes.
- **A memória pessoal da sessão do Sávio** não transfere — mas o essencial dela foi codificado nos checklists e no CLAUDE.md. É por isso que eles existem.
- **Tokens/credenciais** (Slack, Meta, Gemini) — cada máquina usa as suas, via variáveis de ambiente/`.env` local (nunca no git).

## Manutenção

- Melhorou um checklist ou o engine? Commit + push — o agente do outro lado herda no próximo `git pull`.
- Bug visual repetível → conserta o **engine** (com retrocompatibilidade + aviso durável), nunca o post individual. O checklist de design §4 explica a regra.
