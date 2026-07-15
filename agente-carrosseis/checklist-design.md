# CHECKLIST DE DESIGN — carrosséis RECONECTA (html-engine)

> **A tese:** a diferença entre um slide de Fable e um slide de Opus não é gosto, é OLHAR O RENDER. O Opus renderiza e se aprova; o Fable renderiza, abre cada PNG e ataca o próprio slide como se fosse o Sávio vendo pela primeira vez. Este arquivo converte esse ataque em checagens binárias com evidência (o log do render, o PNG aberto, a medida). Marcar item sem ter ABERTO o PNG = teatro.
>
> **GATILHO OBRIGATÓRIO:** rodar em TODO render — post novo, retoque de 1 slide, troca de imagem, re-render por diff de portão. Não existe "mudança pequena demais pra conferir": as duas piores falhas de design do projeto (hero torta e prova no terço superior, ambas 14/jul) estavam em slides "prontos" que ninguém reabriu.
>
> Par deste arquivo: `checklist-producao.md` (copy; o §5 dele aponta pra cá). Juiz final: `portao-qualidade.md`.

## 0 · A régua física do engine (fatos, não opinião)

Engine: `carrosseis/_template/html-engine/engine.py` (réplica do Figma fuIFq4fA94kKjvf2A7vhXo). Renderiza `copy.engine.json` → PNGs 1080×1350 via Playwright.

| Constante | Valor | O que significa na prática |
|---|---|---|
| Canvas | 1080×1350 | feed 4:5; o ad 1080×1080 sai depois via `build_ads.py` |
| `MARGIN` | 93px | largura útil 894px; NADA encosta fora dela |
| `GAP` | 32px | gap ÚNICO entre todos os elementos (regra do Sávio, 30/jun) |
| `SAFE_V` | 130px | faixa segura vertical = 1090px; conteúdo de fundo centra DENTRO dela |
| `OVERFLOW_LIMIT` | 1130px | conteúdo medido acima disso = flag; entre 1090 e 1130 centra apertado mas limpo |
| Hero headline | 98px, auto-fit até piso 60px | quebra art-directed é LEI (ver §1); linha nunca quebra no meio |
| Punch | 60px | slides photo/text/list/proof/cta (todos menos o hero, que usa a headline própria); `"align": "left"` opcional |
| Corpo / itens | 34px, Grift | piso de legibilidade: NUNCA reduzir fonte pra caber copy |
| Prints (proof) | `max-height: 360px` | **clipa o card em silêncio** — ver armadilha 3 |
| Bloco de prints | auto-fit à borda real dos cards | `block_h` manual trava (data-fixed) e o auto-fit respeita |
| Cores | BG_TEXT `#2d0000` · BG_DARK `#0f0e0e` · BG_HERO `#6b0f0f` · CREAM `#faf0dd` · CHAMPAGNE `#f2ddb6` · BODY `#ececec` · RED `#ff2222` | vermelho = números/disrupção; champagne = aparte/ironia (itálico Grift) |
| Fontes | DxMonstral (display) · Grift (corpo; masthead = Grift 900 19px) · Inter (só no pill) | não existem substitutas; se o render cair em fallback, algo quebrou. (O docstring do engine diz "masthead Inter" — desatualizado; o CSS `.mast` é a verdade) |
| fx do hero | `scrim:"strong"` · `dim:0..1` · `spot:true` · `shadow:true` | por slide, retrocompatível; escolher pelo §1.3 |

### 0.5 · O contrato do `copy.engine.json` (schema)

Raiz: `{"ad", "week", "year", "slug", "titulo", "slides": [...], "legenda"}` — o engine só lê `slides`; o resto alimenta o export (§5) e a `legenda.txt`. Caminhos de imagem são **relativos à pasta do json** (`img/hero.png`).

Marcação inline vale em `headline`, `punch`, `body` e `items` (title/body) — **não** no label do `cta`, que é texto puro: `{texto}` = vermelho · `«texto»` = champagne itálico · `\n` = quebra art-directed.

| type | campos | notas |
|---|---|---|
| `hero` | `headline`, `image`, `fx?` | sem punch; sem masthead; pill automático |
| `photo` | `punch`, `body[]`, `image` | sem imagem = placeholder centralizado (render de prova) |
| `text` | `punch`, `body[]` | fundo BG_TEXT |
| `list` | `punch`, `items[{title, body}]` | números vermelhos automáticos |
| `proof` | `punch`, `prints[]`, `positions?[{x,y,w,rot}]`, `block_h?` | grupo centrado na horizontal sozinho |
| `cta` | `punch`, `cta` | label default "TOQUE NO LINK DA BIO"; sem masthead |

Engine alternativo `reconecta_blocks.py` (kit seclabel/cards/from_to; canon SEM24/AD005+AD007): pisos próprios — corpo ≥33, componentes ≥30, punch 40-43, headline 44-48. As regras visuais deste checklist (§1, §3, §4) valem pros dois; a régua da tabela acima é do html-engine.

## 1 · ANTES de renderizar — art direction na copy

### 1.1 Quebras da hero (art-directed, `\n`)
- [ ] **3-5 linhas** com comprimentos BALANCEADOS: forma de bloco ou ampulheta, nunca escada (cada linha menor que a anterior) nem dente (uma linha curtíssima no meio).
- [ ] **Nenhuma linha órfã**: linha de 1 palavra só se for palavra-punch deliberada (um número, um "NADA."), nunca preposição/conector sobrando ("COM", "MÊS,").
- [ ] **Vírgula/ponto fecham linha**, não abrem a próxima.
- [ ] **A linha mais longa dita o corpo da fonte** (auto-fit desce de 98px até caber). Linha longa demais = headline pequena demais: abaixo de ~78px a capa perde presença no feed → REQUEBRAR em mais linhas antes de aceitar corpo menor. Piso duro: 60px (o render avisa "REQUEBRAR" e grava em `_overflow.json`).
- [ ] **Ênfases:** `{vermelho}` na palavra/número disruptivo (1 por punch, na palavra que vira o sentido); `«champagne»` só em aparte/ironia. Vermelho em palavra neutra = desperdício da arma.

### 1.2 As fotos do post
- [ ] **Pasta `img/` + `img/NECESSARIO.txt` criados NO INÍCIO** (antes da copy): listar cada imagem esperada (hero, foto do photo, prints de prova) com uma linha do que serve — é por esse arquivo que o usuário sabe o que depositar.
- [ ] **Render sem as imagens é PROVA DE COPY, nunca entrega.** O engine renderiza placeholders de propósito (photo centralizado como text, prints cinza de 190px) pra validar texto e overflow cedo. Quando as imagens chegarem: re-render + inspeção §3 inteira de novo.
- [ ] **Cantos superiores 100% vazios** — o engine não põe masthead na hero, mas a FOTO também não pode ter texto/logo/elemento gráfico na faixa alta.
- [ ] **Zona do texto (terço inferior) livre de rosto e mãos**: o bloco ancora embaixo (bottom 88px + pill); se o sujeito da foto ocupa essa zona, trocar a foto ou aceitar que o texto passa por cima de área ESCURA do corpo, nunca do rosto/olhos.
- [ ] **Imagem do usuário é soberana** (ele deposita em `img/`); orgânica > stock; nada sensual/sugestivo; resolução mínima: largura ≥1080 real (upscale = grão falso).

### 1.3 fx por foto (decidir OLHANDO a foto, não por hábito)
- [ ] **`fx` só existe no slide HERO.** No slide `photo` o engine IGNORA o campo `fx` (o scrim de lá é fixo no código) — colocar fx no photo não faz nada e não avisa. Legibilidade ruim no photo se resolve trocando/tratando a FOTO ou encurtando o body, nunca via fx no json.
- [ ] Foto com **área clara na zona do texto** (vitrine, céu, parede branca) → `"fx": {"scrim": "strong"}`. *Caso real AD009 14/jul: pontas de "MÊS," e "COM" sobre a calçada clara → scrim strong resolveu sem tocar o rosto.*
- [ ] Foto **escura e uniforme** embaixo → default (sem fx).
- [ ] Ponto quente atrás do texto que o scrim não mata → `"spot": true` (radial atrás do bloco).
- [ ] `"dim"` (véu uniforme) só quando a foto INTEIRA compete com o texto — escurece o rosto junto, é o último recurso com `"shadow"`.
- [ ] Em slide `photo`: o scrim é FIXO no engine (transparente até ~30%, rampa contínua até o rodapé, nunca 100% sólido) e já cumpre a regra do Sávio — a checagem é VISUAL no PNG: rampa suave, sem degrau, **faixa escura chapada sobre a foto = reprova** (regra do Sávio, jul/26).

### 1.4 Prova social (proof)
- [ ] **A seleção de prints é do AGENTE, nunca do usuário (regra do Sávio, 15/jul).** Fluxo: pool curado (`img/depoimentos-sugeridos/` das semanas + `DEPOIMENTOS-MAP.md`) → registro de usados por PÁGINA (pXX que já foi ao ar não volta, mesmo em arquivo `_crop`/`_anon` diferente; detalhe-estrela da mesma clínica idem — cropar a linha do detalhe resolve) → tema do print casa com a TESE do post → crop de anonimização por varredura de banda de pixel (nunca coordenada chutada) → **conferir cada crop VISUALMENTE antes do render**.
- [ ] **O número-chave precisa ser LEGÍVEL na largura final** (~520-565px no slide). Print largo com texto pequeno (dashboard 1235px de largura) encolhe o R$ até sumir — cropar a região do número ou trocar de print. *Caso real 15/jul: o "R$ 779.741" de um dashboard virou pó na escala; troquei por bolha de WhatsApp legível.*
- [ ] **Stagger sem buraco:** as posições `y` são função das alturas ESCALADAS reais (`altura_original × w ÷ largura_original`), não do default — print curto com y de print alto abre um vão morto no meio da cascata. *Caso real 15/jul: bolha de 88px com y=470 deixou ~150px de buraco.*
- [ ] **Posições em cascata** com rotação alternada (default -2.5° / 2° / -2°): stagger legível na ordem de leitura, punch → cards. O engine centra o GRUPO na horizontal sozinho.
- [ ] **A bolha essencial** (a que sustenta o punch) tem que caber INTEIRA em 360px de altura na largura escolhida: `altura_original × largura_no_slide ÷ largura_original ≤ 360`. Não cabe → cropar a bolha ANTES (ver armadilha 3).
- [ ] **Anonimização é pré-render**: blur/crop de nome, telefone, CNPJ, avatar (crop de cabeçalho resolve 80%); R$ e números de resultado ficam NÍTIDOS. Originais intactos — trabalhar em cópia `_anon`/`_crop`.
- [ ] **Punch do proof usa números LITERAIS dos prints** — números que não estão visíveis nos cards não existem.
- [ ] `block_h` manual só quando quiser TRAVAR a altura (raro); sem ele o render abraça o conteúdo sozinho.

## 2 · RENDER — o ritual anti-fantasma

- [ ] **Caminhos à prova de fantasma:** `cd carrosseis/_template/html-engine && python3 engine.py "<pasta>/copy.engine.json" "<pasta>/slides"` com `<pasta>` SEMPRE absoluta. O engine acha fontes/grão sozinho (ancorados no próprio arquivo); o risco real é caminho RELATIVO: um `cd` que falha pula o render no `&&`, e um out_dir relativo despeja os PNGs em OUTRO lugar enquanto você relê os antigos. *Caso real 09/jul: li "SEM OVERFLOW" de um render que nunca rodou e revisei PNG velho.*
- [ ] **Toda imagem RESOLVE antes do render** (`image`/`prints` existem no caminho relativo à pasta do json). Imagem faltando NÃO dá erro — falha em silêncio: hero vira fundo bordô liso, photo cai no placeholder, print vira card cinza. **Formato: só jpg/png** — HEIC (padrão do iPhone) vira área vazia sem aviso; converter antes (`sips -s format png`).
- [ ] **Contar os `ok slide_N`** = número de slides do copy. Faltou um = render quebrou no meio.
- [ ] **mtime fresco em TODOS os PNGs** (`ls -la slides/`) — data/hora de agora, não de ontem.
- [ ] **Ler as linhas de fit do log** (elas contam o que o engine ajustou por você):
  - `hero fit: headline a Xpx` → o corpo desceu; se X < ~78, voltar ao §1.1 e requebrar.
  - `⚠ HERO ... REQUEBRAR` → bloqueio: headline não coube nem no piso.
  - `proof fit: bloco de prints a Xpx` → normal; a régua de aperto é o TOTAL (punch + 32 + bloco) contra a faixa: passou de 1090 centra apertado, e o ⚠ OVERFLOW dispara em 1130. Na prática: punch de 2 linhas → bloco até ~940px confortável; punch de 1 linha → até ~990px.
  - Slide proof **SEM** linha `proof fit:` no log = bloco travado por `block_h` — confirmar que travar foi intencional; se não foi, remover o `block_h` do json.
- [ ] **`_overflow.json` NÃO existe** na pasta slides/. Se existir: **cortar COPY, nunca fonte**. Micro-corte não resolve — derrubar LINHA inteira (caçar a linha órfã de 1-2 palavras no PNG e encurtar ali).
- [ ] **O medidor de overflow NÃO cobre hero nem photo** (só slides de `.center-wrap`: text/list/proof/cta). "_overflow.json ausente" não prova nada sobre os slides de foto: body longo no photo sobe sobre o rosto SEM flag — a checagem deles é 100% visual no §3 (no photo, o bloco punch+body começa abaixo da metade da tela; subiu além disso = cortar copy).

## 3 · INSPEÇÃO VISUAL — abrir CADA PNG (Read), com o olho do Sávio

Regra de ouro: **depois de QUALQUER re-render, olhar TODOS os slides de novo**, não só o que mudou — os fits são globais e um ajuste pode mover outro slide.

### Todos os slides
- [ ] Gap visualmente uniforme (32px) entre todos os elementos; nada colado em borda; nada sobreposto.
- [ ] Masthead "RECONECTA" no canto direito alto nos slides photo/text/list/proof — **hero e CTA não têm masthead** (é assim no engine e no canon; masthead "faltando" no último slide NÃO é defeito). **Nunca** número do AD em slide nenhum.
- [ ] Grão presente (textura, não banding liso).
- [ ] Nenhum texto cortado na borda direita/inferior (word-wrap comido é bug, não estilo).

### Hero (slide 1)
- [ ] **Contar as linhas no PNG** = número de `\n` + 1 da copy. Diferente = quebra torta (hoje estruturalmente impossível — mas conferir é grátis e já salvou o AD009).
- [ ] Bloco baixo, rosto/olhos livres, pill "RECONECTA /→" centrado embaixo com respiro.
- [ ] **Pontas das linhas legíveis** sobre as áreas mais claras da foto (olhar as EXTREMIDADES, não o centro do texto).
- [ ] Cantos superiores vazios (foto + engine).

### Photo (slide 2)
- [ ] Texto embaixo sobre o scrim; fade fecha acima do texto com rampa (ver §1.3); punch e corpo sem disputa com o sujeito da foto.

### Text / List
- [ ] **Centralização vertical DE VERDADE**: clareira equilibrada em cima e embaixo (medir de olho: diferença gritante = bug ou copy demais). Conteúdo no terço superior com vazio embaixo = reprova. *Caso real AD009 slide 5, 14/jul.*
- [ ] Slides sem foto = RICOS: corpo nunca chapado — callout pro próximo slide, lista numerada, ênfases. Parágrafo único cinza de 6 linhas = slide de aula, volta pra copy.
- [ ] Lista: números vermelhos alinhados, títulos Grift 900, itens respirando (gap 32 dentro e entre).

### Proof (slide 5)
- [ ] **Clareira equilibrada** acima do punch e abaixo do último print (o bloco agora abraça o conteúdo — se ainda assim ficou torto, tem espaço morto DENTRO dos cards ou copy demais no punch).
- [ ] **Última linha da bolha essencial visível INTEIRA** (anti-clip). *Caso real AD010 09/jul: o "de outubro" que sustentava o punch sumiu no clip de 360px.*
- [ ] Zero nome/telefone/CNPJ/avatar legível em zoom 100%; R$ nítido.
- [ ] Punch bate com os números visíveis nos prints.

### CTA (último slide)
- [ ] Card Figma verbatim + "TOQUE NO LINK DA BIO" (exceção única: COMENTE "SUPERCASO" quando o usuário pedir). Sem @handles. Sem headline nova inventada no CTA.

## 4 · Defeito estrutural → conserta o ENGINE, não o slide

Pergunta de decisão: **"isso pode acontecer de novo em qualquer post futuro?"**

- **SIM** (quebra de linha, bloco fixo, clip silencioso, colisão de layout) → conserto no `engine.py`, com: (a) retrocompatibilidade — override manual sempre vence o automático (`block_h`/`data-fixed` é o modelo); (b) **aviso durável** quando o automático não resolve (padrão `_overflow.json` + print no log — nunca corte/quebra silenciosa); (c) registrar o caso na tabela de armadilhas deste arquivo.
- **NÃO** (foto ruim, copy longa, print grande) → conserto no post (copy, crop, fx).
- **Proibido:** hardcodar pixel no `copy.engine.json` de UM post pra compensar bug do engine — o próximo post herda o bug.
- **Proibido:** re-renderizar pasta de post JÁ PUBLICADO com engine novo (post novo = pasta nova; exportado é imutável).

## 5 · Antes de avisar o usuário **(PARE)**

- [ ] Olhei TODOS os PNGs depois do ÚLTIMO re-render (não confiar em olhada de render anterior).
- [ ] Exports `[AA] [SS] [AD0NN_M] - Título.png` atualizados na raiz da pasta — copiar TODOS os slides do copy (o número VARIA; contar = nº de slides do json, nunca assumir 6). Decodificação: AA = ano em 2 dígitos · SS = semana ISO da pasta SEMxx · N = número do AD · M = índice do slide · Título = campo `titulo` do json.
- [ ] `open` no `preview.html` — GERADO pelo render automaticamente na pasta do post (ao lado do copy.engine.json), com cache-buster por mtime. Não criar preview na mão, não procurar em slides/.
- [ ] Entrega diz o que foi verificado E o que não foi (status honesto; "revisei os 6 PNGs no zoom" ≠ "renderizou ok").

## Armadilhas nomeadas (todas com caso real)

| # | Armadilha | Caso real | Antídoto |
|---|---|---|---|
| 1 | **Quebra de hero torta** (linha art-directed quebrada no meio pelo layout) | AD009 14/jul: "MÊS," e "COM" órfãs, 6 linhas tortas sobre o rosto | Engine: quebra é lei + auto-fit (piso 60). Conferir linhas no PNG = `\n`+1 |
| 2 | **Prova no terço superior** (espaço morto em bloco fixo engana a centralização) | AD009 slide 5, 14/jul: 254px mortos no bloco de 820 → 380px de vazio embaixo | Engine: proof fit abraça conteúdo. Olhar clareira em cima/embaixo |
| 3 | **Print clipado em silêncio** (`max-height:360px` come o fim da mensagem) | AD010 09/jul: "de outubro" sumiu e o punch ficou sem sustentação | Calcular altura escalada ≤360 OU cropar a bolha; conferir última linha no PNG |
| 4 | **Render fantasma** (PNG velho lido como novo) | 09/jul: "SEM OVERFLOW" de render que não rodou | `cd` certo + contar `ok` + mtime fresco |
| 5 | **Overflow "resolvido" com fonte menor** | tentação recorrente | Piso de legibilidade é inegociável: cortar COPY, derrubar linha inteira |
| 6 | **Chute de coordenada de crop** em screenshot alto | AD010 09/jul: crop às cegas cortou bolha errada | Medir bolhas por varredura de pixel OU iterar crop→olhar |
| 7 | **Texto sobre área clara sem tratamento** | AD009 14/jul: pontas sobre a vitrine | §1.3: escolher fx OLHANDO a foto |
| 8 | **Faixa escura chapada sobre a foto** | feedback do Sávio (jul/26, slide_photo) | Rampa contínua sem degrau (scrim do photo é fixo no engine; conferir VISUAL no PNG) |
| 9 | **Dado pessoal legível em print** | regra permanente (depoimentos) | Blur/crop pré-render; R$ nítido; zoom 100% no PNG final |
| 10 | **Aprovar sem abrir o PNG** | a causa-raiz de 1, 2 e 3 terem passado | Read em todos os slides, sempre, com evidência no relato |
| 11 | **Consertar no post o que é bug do engine** | tentação recorrente | §4: pergunta de decisão + retrocompat + aviso durável |
| 12 | **Re-render de post publicado** | regra permanente | Exportado é imutável; post novo = pasta nova |
| 13 | **Número ilegível em print largo** | 15/jul: R$779k de dashboard sumiu na escala | Legibilidade na largura final; cropar a região do número ou trocar o print (§1.4) |
| 14 | **Buraco no stagger da prova** | 15/jul: bolha curta com y default | Posições y em função das alturas ESCALADAS (§1.4) |
| 15 | **Pedir print ao usuário** | 15/jul: "não tem por que regredir o que a gente já progrediu" | Seleção automática: pool + registro por página + crop por banda (§1.4) |
