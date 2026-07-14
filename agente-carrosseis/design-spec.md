# Design Spec — Padrão Validado (80% dos posts)

> Extraído do Figma (arquivo `fuIFq4fA94kKjvf2A7vhXo`, 2026-06-30). Fonte de verdade visual.
> O engine HTML replica ISTO; o gerador escreve a copy; você só deposita as imagens.

## Formato & nomenclatura
- **1080×1350**, 6 slides (hero · 4 entrega · prova · CTA).
- Nome dos frames: **`[AA] [SS] [AD00N_M] - Título`** (ex: `[26] [23] [AD001_1] - Como fazer depoimento`). AA=ano-código, SS=semana, AD00N=anúncio, _M=slide. **Manter em TODOS os posts** (export já renomeia assim).

## Paleta
| Uso | Hex |
|---|---|
| Fundo escuro (base) | `#2d0000` bordô profundo (variações `#500000`, `#6b0f0f`) |
| Display / punch | `#faf0dd` creme |
| Ênfase | `#f2ddb6` champagne |
| Corpo | `#ececec` / `#f5f5f5` cinza claro |
| Acento (números, destaque) | `#ff2222` vermelho |
| Overlay sutil | `#040416` @5% |
| Textura | grão "ISO Noise" por cima de tudo |

## Tipografia *(verificado por render-compare contra os 6 frames, 30/jun)*
- **Display / punch → Dx Monstral Regular.** 98px no hero, 60px nos demais. Creme `#faf0dd`, caixa alta. `letter-spacing` ~0 (hero) / `-.005em` (punch), `line-height` .99–1.0.
- **Corpo → Grift.** 34px. Regular (corpo), Black (títulos de lista). Cor `#ececec`; ênfase champagne `#f2ddb6` itálico. `line-height` 1.35–1.4.
- **Masthead → Grift Black 19px** `#ececec`, caixa alta, `letter-spacing` .16em — **topo-direita** (NÃO Inter, NÃO tem "/").
- **Botão (hero/CTA) → Inter** 18px Bold, `#f5f5f5`, `letter-spacing` .14em, com seta "→".
- **Números de lista → Grift Black 34px `#ff2222`.**
- **Quebras de linha são art-directed (`\n`)** — o designer quebrou manualmente; o engine honra `\n` (não depende de auto-wrap coincidir).

## Alinhamento *(corrigido 30/jun — TUDO centralizado)*
Headline/punch/corpo **centralizados em TODOS os slides** — não há texto puxando pra esquerda. Única exceção estrutural: os **itens da lista numerada** (número vermelho à esquerda + texto do item alinhado à esquerda na coluna). Erro anterior (hero/text/proof à esquerda) foi corrigido — o usuário pegou.

## Espaçamento & distribuição vertical *(regra do usuário, 30/jun — NÃO violar)*
- **GAP de 32px UNIFORME** entre TODOS os elementos: título→corpo, corpo→corpo, entre itens da lista, título→corpo DENTRO do item, punch→bloco de prints. Ritmo parelho, nunca uns grandes e outros minúsculos. No engine = constante `GAP=32` (flex `gap`).
- **Centralização vertical:** nos slides de fundo (text/list/proof/cta) o bloco de conteúdo é **verticalmente centralizado** (`.center-wrap` justify-content:center) — respiro em cima ≈ embaixo, nunca colado no topo nem caindo embaixo.
- **Slides de foto (hero/photo):** texto **ancorado embaixo** sobre o scrim (`.bottom-wrap`) — NÃO centralizado (correto assim).
- **ZERO overlap:** nenhum elemento sobrepõe outro. O `proof` usa `.prints-block` (bloco próprio) separado do punch pelo gap de 32 — o título nunca encosta nos cards de depoimento. (Bug pego pelo usuário em 30/jun: punch sobre o frame de prints — resolvido.)
- **ZERO corte de borda:** nada vaza nem encosta nas bordas; legibilidade do corpo no piso (≥30), nunca apertado pra caber copy.
- **CABER NA FAIXA (sem encolher fonte):** o conteúdo de cada slide tem que caber na faixa segura (altura útil ≈1090px, entre o masthead e a margem de baixo). A trava é a COPY, não a fonte — **NUNCA encolher texto pra caber** (`feedback_legibilidade_piso_texto`). O ofensor típico é o **slide de lista com 4 itens de body longo (3-4 linhas)**: estoura e corta o título e o último item. Regra: **lista = 3-4 itens, body de 1-2 linhas**; a camada longa (mecanismo/frame) vai pro `text`/`photo`, não empilha no item. O engine MEDE a altura natural e, se passar da faixa, grava `slides/_overflow.json` + imprime `⚠ OVERFLOW` (nunca corta calado) — esse slide é **reprovado**, encurta a copy e re-renderiza.

## Fundos por slide
text `#2d0000` bordô + grão · photo & cta `#0f0e0e` quase-preto · hero `#6b0f0f` atrás da foto. **Grão = film grain FINO via SVG `feTurbulence`** (baseFrequency .9, grayscale), tile 220px, `opacity:.12` blend overlay — crisp e sutil (NÃO o grain.png antigo, que ficava grosso/murky).

## Componentes & ritmo
- **Botão (pill):** retângulo OUTLINE com `border-radius:20`, `stroke:1px` cor `#f5f5f5`, contendo `LABEL  /  →` (Inter 18 + separador "/" + seta). Mesmo componente no hero ("RECONECTA") e no CTA ("TOQUE NO LINK DA BIO"), centralizado. (NÃO é régua/linha.)
- **Hero:** foto portrait full-bleed + scrim inferior + headline Dx Monstral 98 na base + pill "RECONECTA /→" centralizado embaixo. SEM masthead no topo.
- **Photo:** foto full-bleed + scrim escuro forte embaixo + punch 60 + 1-2 corpos. Masthead topo-direita.
- **Text:** bordô + punch 60 + corpos + **callout** (gancho do próximo slide).
- **List:** punch 60 + itens (número vermelho + título Grift Black + corpo).
- **Proof:** punch + slots de prints espalhados/rotacionados com sombra.
- **CTA:** quase-preto + punch 60 centro + botão "TOQUE NO LINK DA BIO /→" (Inter, COM régua em cima).
- **Callout:** caixa borda vermelha `#ff2222` radius 14, texto Grift itálico champagne centralizado.
- **Ênfase inline na copy:** `{texto}` → vermelho `#ff2222`; `«texto»` → champagne itálico.
- Cantos arredondados: 14 (callout/prints), 20–21 cards maiores.

## Slots de imagem (você deposita)
- Hero: portrait ~1536×2048, color-graded.
- Grão "ISO Noise": textura fixa (eu embuto).
- Prova: prints de depoimento (slide 5).

## Engine HTML *(construído + validado 30/jun)*
- **`carrosseis/_template/html-engine/engine.py`** — Python + Playwright/Chromium. Fontes embutidas em base64 (auto-contido). 1 px Figma = 1 px CSS = 1 px de saída.
- **Uso:** `python3 engine.py copy.json out_dir/` → renderiza `slide_1.png`…`slide_6.png` em 1080×1350.
- **`copy.json`:** `{ ad, week, year, slug, slides:[…] }`. Cada slide tem `type` (hero/photo/text/list/proof/cta) + campos (`headline`/`punch`/`body`/`items`/`callout`/`cta`/`image`/`prints`/`align`).
- **Validado por render-compare** contra os 6 frames do Figma: fidelidade ~96-99% por slide. Deltas só em (a) imagens que você deposita e (b) quebra de 1 palavra (controlável por `\n`).

## Como conecta no gerador
`gerador-carrossel` escreve `copy.json` (com a marcação `{vermelho}`/`«champagne»`/`\n`) → `engine.py` renderiza os 6 PNGs com este look exato → você arrasta hero/foto/prints nos slots → export aplica a nomenclatura `[AA] [SS] [AD00N_M] - Título`. Roda no lote da semana, automático.

## Decisões (resolvidas 2026-06-30)
1. **CTA = "TOQUE NO LINK DA BIO"** (decisão do usuário; o link leva a evento/oferta). Pesquisa favorecia SUPERCASO+SEND — tradeoff consciente; a LEGENDA puxa salvar/compartilhar.
2. **Masthead:** content slides têm "RECONECTA" (Grift, topo-direita); hero/CTA NÃO têm masthead, usam botão centralizado embaixo. (`feedback_hero_masthead` desatualizada pro design novo.)
3. **Fonte Dx Monstral: RESOLVIDO** — `_template/fonts/DxMonstral-Regular.otf`, embutida no engine. Grift e Inter idem.
4. **Path de produção: HTML** (não PIL) — decisão do usuário ("replicar em HTML"). Engine novo NÃO toca os engines PIL existentes (`reconecta_carousel*.py`).
