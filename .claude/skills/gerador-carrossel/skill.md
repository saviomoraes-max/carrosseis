---
name: gerador-carrossel
description: Gera a copy de um carrossel RECONECTA combinando spec de voz (ponderada por performance) + tema vetado pelo filtro de relevância + técnica de headline ancorada em fonte real do repertório. Roda o portão de qualidade no fim e só entrega o que passa. Acionar quando o usuário pedir "gera um carrossel sobre X", "monta a copy", ou para consumir um item da trends-queue. É o motor da Fase 1.
---

# Gerador de Carrossel — motor da Fase 1

Orquestra a copy de um carrossel a partir de um tema JÁ vetado. Nunca inventa headline nem
tema do zero: consulta os ativos do agente. Termina rodando o portão de qualidade.

## Inputs (fontes da régua — sempre consultar)
- `agente-carrosseis/voice-spec.md` — ganchos/estruturas/temas que VENCERAM, ritmo, dial, nunca-faz
- `agente-carrosseis/voice-dna.md` — COMO escrever pra soar como a copywriter, não como IA (5 dispositivos + checklist anti-robótico); OBRIGATÓRIO
- `agente-carrosseis/headlines-repertoire.json` — técnicas de headline com exemplo real + URL
- `agente-carrosseis/relevance-filter.json` — confirmar que o tema passou no gate
- `agente-carrosseis/portao-qualidade.md` — o checklist final
- Tema: um item de `data/trends-queue.json` (aprovado) OU tema manual do usuário

## Workflow

### Passo 1 — Travar o tema e o ângulo
Pegar o tema vetado. Confirmar o veredito na spec (`aumentar`/`manter`/`reduzir`).
Se `reduzir`, exigir ângulo novo (não repetir o que já saturou). Checar canibalização
contra o acervo (SEM17→atual) e os ADs vizinhos.

### Passo 2 — Escolher a estrutura vencedora
Da spec, pegar um esqueleto `venceu` que case com o tema:
antes/depois→SUPERCASO · tático-WhatsApp/objeção-script (swipe file) · indicação-na-sala.
1 ideia por slide; slides de entrega com as 4 camadas.

### Passo 3 — Ancorar a headline no repertório
Escolher do `headlines-repertoire.json` uma técnica `venceu` (pergunta-paradoxo ou número/lista)
que sirva ao ângulo. Adaptar o template ao tema. Guardar `tecnica_aplicada` + a URL de origem
(o portão vai exigir). NUNCA escrever headline sem ancorar numa entrada do repertório.

### Passo 4 — Escrever a copy
Aplicar o `voice-spec.md`: dial de postura + gíria leve no registro doutora, léxico recorrente,
sem vocabulário proibido. Slides de entrega com 4 camadas. CTA: o slide usa **"TOQUE NO LINK DA BIO"**
(padrão decidido 30/jun — link leva a evento/oferta); a **LEGENDA** faz a distribuição (pede SALVAR +
mandar pra uma colega/SEND). Sem dado inventado: ancorar ou demonstrar via processo.
Gravar no **formato do engine** (`carrosseis/_template/html-engine/engine.py`): slides com `type`
∈ hero/photo/text/list/proof/cta + campos; marcação `{vermelho}`/`«champagne»`/`\n`. Ver `design-spec.md`.
Em lote, usar o workflow `agente-carrosseis/gerar-semana.js` (gera→portão→render automático).

### Passo 5 — Rodar o portão de qualidade
Aplicar `portao-qualidade.md` (A→E). Só "entregar" se cruzar tudo.
- APROVADO → reportar com o cabeçalho de fontes (URL da headline, dor que o tema conecta, âncora dos dados).
- REPROVADO → diff focado no slide, re-rodar. Não reescreve o carrossel inteiro.

### Passo 6 — Handoff
Copy aprovada → pasta pronta pro design (Figma do usuário ou as design-* skills, na Fase 2).
Imagens (hero + depoimentos) ficam como `imagens_a_depositar` no copy.json.

## Não-negociáveis
- Headline sem entrada no repertório (com URL) → não escreve.
- Tema sem passagem pelo filtro de relevância → não escreve.
- Afirmação factual sem âncora → não escreve; demonstra via processo.
- Gancho `só existiu` (analogia-celebridade) ou tema `reduzir` sem ângulo novo → barra no portão.
