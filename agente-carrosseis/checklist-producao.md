# Checklist de Produção — Carrossel RECONECTA
> **Para quem é:** o modelo que estiver produzindo (escrito pro Opus; o Fable também roda).
> **O que é:** o self-check que roda DURANTE a produção — antes do portão adversarial (`portao-qualidade.md`), que continua sendo o juiz final. O portão pega o que escapou; este checklist existe pra chegar lá com quase nada escapando.
> **A tese:** a diferença entre um carrossel de Fable e um de Opus não é conhecimento, é AUTOCRÍTICA. O Opus escreve uma vez e se aprova; o Fable escreve e depois ataca o próprio texto como se fosse outra pessoa. Este arquivo converte esse ataque em passes explícitos. Rodar TODOS, na ordem, com evidência (o grep, o render, a comparação lado a lado). Marcar item sem evidência = teatro.
> Item **PARE** reprovado → não avança até resolver. Todos os "casos reais" citados aconteceram nesta operação (jul/2026) e custaram retrabalho e confiança do usuário.
> **GATILHO OBRIGATÓRIO (pedido do usuário, 09/jul):** os PASSES B→E rodam **TODA VEZ que uma copy sai — de carrossel OU de legenda, versão nova OU reescrita, mesmo um ajuste de uma frase.** Não existe "mudança pequena demais pra checar": as piores reprovações vieram de ajustes que pareciam pequenos. Copy entregue sem os passes rodados = copy não terminada.

---

## 0 · Setup (antes de qualquer palavra)

- [ ] **Li `voice-dna.md` INTEIRO nesta sessão** — os 5 dispositivos, o CANON, "O CHEIRO DE IA", a legenda-fórmula e TODOS os anti-padrões.
- [ ] **Li `portao-qualidade.md`.**
- [ ] **Sei o que já foi postado na semana** e qual foi a fórmula de gancho e o rótulo de lista de cada um. *Como: `ls` na `SEM__/` + `copy.engine.json` de cada AD exportado. Regra VARIE: não repetir fórmula de gancho nem rótulo de lista do post imediatamente anterior; não reabrir a legenda com o dispositivo do post anterior.*

## 1 · Tema **(PARE)**

- [ ] **Não canibaliza post publicado.** Compare a IDEIA CENTRAL slide a slide, não o título. *Caso real: AD006 era o AD003 postado com outras palavras (espelho, programa de pontos, "abra a porta") — só apareceu comparando lado a lado.*
- [ ] **O tema tem fonte no corpus** (`data/corpus.json`): pelo menos UMA peça dela com marcadores suficientes pros slides de entrega. Corpus com UMA peça já usada noutro post = tema queimado.
- [ ] **Referência cultural tem prazo de validade** (Spotify, celebridade, meme) → confirmar timing com o usuário ANTES de escrever. *Caso real: carrossel do Spotify inteiro descartado ("perdemos o timing").*

## 2 · Tabela de âncoras **(PARE — escrever ANTES da copy)**

- [ ] **Uma linha por passo/frase pronta/número/claim: (a) o texto, (b) a peça de origem, (c) o marcador literal.** *Como: grep/python no corpus (`marcadores_voz` = falas literais; `estrutura[].funcao` = movimentos por slide).*
- [ ] **Sem âncora → NÃO ENTRA.** "Plausível dentro do espírito" = inventado. *Casos reais reprovados: "aposente a palavra alta", "áudio de 30s pro marido", "aos poucos sai mais caro". Todos soavam perfeitos; nenhum existia.*
- [ ] **A âncora cobre o MOVIMENTO, não só as palavras.** Linha literal dela transplantada pra outro mecanismo = falso verbatim. *Caso real: "é isso mesmo ou tô enganada?" é a emenda do ÁUDIO MUDO (áudio de 5s → curiosidade → a frase); virou "mensagem sincera" e o usuário pegou: "não lembro disso na nossa metodologia".*
- [ ] **Ao parafrasear uma linha dela: diff palavra a palavra contra o original e justificar CADA desvio.** Desvio sem justificativa → restaurar o verbatim. *Casos reais: o "nunca é sobre o marido" dela amaciado pra "quase nunca"; o "entender MELHOR" dela perdido pra "entender". Paráfrase dilui; verbatim é o padrão.*

---

## 3 · PROTOCOLO DE AUTOCRÍTICA DE COPY (o coração — rodar os 5 passes na ordem)

### PASSE A — Escrever na ordem certa
1. Tabela de âncoras (seção 2) fechada.
2. Esqueleto: UM punch por slide, escrito antes dos bodies. Punch = contraste seco ou afirmação que vira o senso comum de cabeça pra baixo — **nunca um título descritivo ou resumo** ("As 4 respostas que funcionam" = título; "O lead não some no vou pensar. Some na sua próxima mensagem." = punch).
3. **Arquitetura de funil (regra do Sávio, 14/jul/26):** capa = TOPO de funil (dor ou cena ampla que a doutora FRIA reconhece na hora; zero jargão de metodologia, zero nome de framework, zero promessa de fundo); slide 2 = MEIO de funil (a prova ou o porquê que conecta a dor ao mecanismo); slides 3+ = FUNDO de funil (mecanismo, aplicação, script, CTA). Base em dado: os 16 hits com s/r ≥ 3% (análise de 14/jul) abrem todos em reconhecimento amplo — a fala da paciente entre aspas é TOFU porque é cena, não mecanismo.
4. Bodies montados A PARTIR das âncoras (preferir montar com as linhas literais dela a "escrever no estilo dela").
5. Legenda por último, já em modo anti-eco (seção 4).

### PASSE B — Frase a frase (rodar em CADA frase do carrossel)
- [ ] **Teste da voz alta:** li em voz alta. Soa como ela falando com uma doutora, ou como redator escrevendo? Marcadores de redator: construção elegante demais, ritmo perfeito, abstração ("a pergunta que ela veio responder" → reescrever).
- [ ] **Teste do "quem diria isso":** ela diria ESSA frase num áudio de WhatsApp? Se só existe no papel, não é dela. *Marcadores de papel: "da que enrola à que joga...", "cujo", "sob", gerúndio encadeado, aposto explicativo longo.*
- [ ] **Teste do corte:** se eu deletar esta frase, o slide perde algo? Não perde → deleta. (A maioria das frases de IA existe pra "completar o parágrafo", não pra dizer algo.)
- [ ] **Palavras amaciadoras:** "quase", "meio", "um pouco", "talvez", "acaba que" — ela é assertiva; amaciador sem função = cortar. *Caso real: "quase nunca é sobre o marido" (o verbatim dela é "nunca").*
- [ ] **Pessoa e registro consistentes** dentro da frase e do slide (lead/ela, você/tu — não misturar no mesmo período).

### PASSE C — Slide a slide
- [ ] **O body NÃO reafirma o punch.** Teste explícito: a última frase do body diz o mesmo que o punch com outras palavras? → trocar por uma aterrissagem NOVA (detalhe concreto, monólogo interno, gancho pro próximo slide). *Caso real: punch "some na sua próxima mensagem" + fecho do body "a tua mensagem seguinte matou" = a mesma tese 2x no mesmo slide.*
- [ ] **Leitura fria de cada aspa:** li a frase pronta SOZINHA, como se chegasse no meu WhatsApp sem contexto. Tem referente? Dá pra responder? Depende de setup que não está ali → restaurar o setup ou trocar a linha. *Caso real: "É isso mesmo, ou eu tô enganada?" solta — "não tem pé nem cabeça essa p*rra".*
- [ ] **Aforismos ≤ 1 por slide** (contar, não sentir). Dois seguidos → um vira cena.
- [ ] **Etiqueta pós-aspa = 0.** Nada de rótulo depois da frase pronta ("Isso reabre a conversa.", "Ela vira sua aliada."). A frase se explica; o que humaniza é o ERRO encenado ANTES dela. *Caso real: 4 itens com etiqueta simétrica = "cara de IA" na hora.*
- [ ] **Cada item de lista responde sozinho "por quê / como assim?"** Não responde → encenar o erro antes da regra (verbatim comprimido = manual).
- [ ] **Formas VARIADAS entre itens:** um abre pelo erro, outro solta a frase seca, outro reframe. Molde repetido (setup + "Devolve:" + aspa ×4) = mecânico. Variar também os VERBOS de comando (grep: um mesmo verbo estrutural ≤2 no slide).
- [ ] **Slides de entrega têm as 4 camadas:** ação concreta + mecanismo causal + exemplo vivo (frase pronta/vignette) + frame. Slide de entrega sem exemplo vivo = aula.
- [ ] **Escada da especificidade:** toda palavra abstrata que sobrou (experiência, valor, cuidado, transformação usada como conceito) → dá pra trocar por cena, objeto, hora ou número? Troca. ("ela se sente cuidada" → "um áudio de 20 segundos numa terça, sem motivo").

### PASSE D — O carrossel inteiro
- [ ] **METRALHADORA DE PUNCHLINE (o bafo que o usuário mais odeia — 09/jul).** IA escreve frase de impacto O TEMPO TODO; gente deixa frase terminar normal. Teste em duas escalas, contando: **(a) escala carrossel:** olhe SÓ a última frase do body de cada slide — final "de efeito" em TODOS os slides = robô; pelo menos 2 slides terminam em coisa comum (um fato, uma cena, um pedido, o gancho pro próximo). **(b) escala slide:** depois do punch do topo, a primeira frase do body RESPIRA (cena/fato), não emenda outra facada. O punch é o tiro; o body é a cena. *Na legenda, o mesmo teste é o cheiro #1 do `checklist-legenda.md` (máx 2 finais de efeito em 5 parágrafos).*
- [ ] **Leitura em sequência como a leitora** (hero → 2 → 3 → 4 → 5 → CTA → legenda, sem parar): cada slide puxa o próximo? A promessa da capa é entregue? Algum slide repete ideia do vizinho?
- [ ] **Arco de funil (binário):** a capa lê TOFU (doutora fria se reconhece sem nenhum contexto)? O slide 2 é MOFU (prova/porquê)? Jargão de metodologia e nome de framework só aparecem do slide 3 em diante? Capa com mecanismo ou promessa de fundo = reescrever a capa, não o resto.
- [ ] **Contagem de ecos por grep** (não de cabeça): palavra-conceito do tema ≤2 no carrossel; verbo estrutural repetido ≤2; construção sintática assinatura ("Você não X. Você Y." / "Quem X, Y") ≤1.
- [ ] **Quotas de dispositivos (mínimos, com citação):** ≥1 frase pronta exata POR slide de entrega · ≥1 contraste seco no carrossel · ≥1 detalhe concreto inesperado · ≥1 monólogo interno + punch · número de capa escalado/específico quando houver número.
- [ ] **Emphasis nos lugares certos:** `{vermelho}` na palavra disruptiva do punch (não em palavra neutra); `«champagne»` só em aparte/ironia.
- [ ] **Regras duras:** zero travessão no meio de frase · zero "high/alto ticket" · zero @handle · zero dado sem print/fonte · frase à paciente jamais expõe limitação do produto (retorno = parte do tratamento) · copy do usuário é literal (ênfase só por cor/peso).

### PASSE E — O adversário interno **(PARE — o passe que separa aprovado de reprovado)**
- [ ] **Vesti a persona do Sávio e ataquei o texto.** Gerar por escrito as 5 críticas mais prováveis dele — o histórico é o guia: *"tá com cara de IA"* · *"isso não tem pé nem cabeça"* · *"de onde você tirou isso? não é da nossa metodologia"* · *"tá mecânica, não orgânica"* · *"a legenda tá repetindo o carrossel"*. Pra cada uma: ou aponto a evidência de que não se aplica, ou CONSERTO antes de entregar.
- [ ] **Regra do "não defende":** se a minha justificativa pra manter uma frase começa com "mas tecnicamente…" ou "no contexto dá pra entender…", a frase cai. O leitor não tem o contexto da minha defesa.
- [ ] **Critério de reescrita:** slide que falhou em ≥2 checks deste protocolo → REESCREVER a partir da âncora, não remendar. Remendo em cima de remendo foi o que gerou as 3 versões reprovadas do AD010.
- [ ] **Segunda leitura fria com distância:** depois de tudo, reler o carrossel inteiro UMA vez como se outra pessoa tivesse escrito, procurando ativamente o que EU deixaria passar por apego. O que incomodar minimamente → resolver (o usuário sente o mesmo incômodo, amplificado).

---

## 4 · Legenda (feita JUNTO, entregue JUNTO — e roda os passes B e E também)

> **(PARE)** Depois da estrutura abaixo, rodar o **`checklist-legenda.md`** inteiro — os 7 cheiros de IA em legenda + o teste do áudio de WhatsApp. Estrutura certa com bafo de IA reprova igual (caso real: AD010, 09/jul).

- [ ] **5 parágrafos:** material NOVO (outro ângulo/teste imediato/efeito que não coube nos slides) → mecanismo vívido → o que tem nos slides SEM parafrasear → SALVA + MANDA com burn carinhoso → CTA espelho do card.
- [ ] **ANTI-ECO (PARE):** comparação LITERAL parágrafo × cada slide, lado a lado. Frase/cena/construção repetida = reescrever com material novo. Máximo UMA palavra-motivo. *Casos reais: AD012 (P1/P2 eram corpos de slides — o usuário explodiu) e AD010 (P2/P3 reciclavam "a tua mensagem seguinte"/"nenhuma empurra").*
- [ ] **CTA espelha o card em prosa humana.** Campanha de comentário: "comenta SUPERCASO aqui embaixo (tudo junto, é uma palavra só) que eu te chamo no direct". Nunca "clique agora/não perca". Card e legenda mudam JUNTOS.
- [ ] **Formato:** linha em branco entre parágrafos = U+2800 ("⠀") sozinho; `legenda.txt` na pasta SINCRONIZADO com o campo `legenda` do json (conferir os DOIS após qualquer edit).

## 5 · Render & design — checar nos PNGs, não na copy

> **Versão completa:** `checklist-design.md` (régua física do engine, art direction da hero, fx por foto, inspeção slide a slide, engine-vs-post, 12 armadilhas com caso real). Este §5 é o resumo; em produção, rodar o arquivo dedicado.

- [ ] **Renderizar do diretório certo:** `cd carrosseis/_template/html-engine && python3 engine.py "<pasta>/copy.engine.json" "<pasta>/slides"`. **Conferir `ok slide_N` pra TODOS + mtime fresco** (`ls -la slides/`). *Caso real: render sem `cd` falhou silencioso; li "SEM OVERFLOW" de render que não aconteceu e revisei PNG velho.*
- [ ] **`_overflow.json` não existe.** Se existir: cortar COPY (nunca fonte). Micro-corte não resolve — derrubar LINHA inteira: caçar linha órfã (1-2 palavras) no PNG e encurtar ali.
- [ ] **Abri e OLHEI cada PNG** (Read em todos, SEMPRE que a copy ou imagem mudar):
  - **Hero (engine atualizado 14/jul):** o engine NUNCA mais quebra linha art-directed no meio — desce a fonte de 98px até a linha mais longa caber (piso 60px; abaixo disso avisa "REQUEBRAR" e grava `_overflow.json`). Conferir no render: linhas do PNG = `\n`+1 e corpo não desceu de ~78px (log "hero fit"). Cantos superiores VAZIOS. Legibilidade sobre a foto: fx escolhido OLHANDO a foto (`checklist-design.md` §1.3).
  - **Photo/text/list:** gap uniforme, nada colado em borda, corpo ≥30.
  - **Proof (engine atualizado 14/jul):** o bloco de prints abraça o conteúdo sozinho (log "proof fit"; `block_h` só pra travar altura na mão) — conferir clareira equilibrada em cima/embaixo; NENHUM nome/telefone/CNPJ/avatar legível (crop/blur PIL em `_anon`/`_crop`, originais intactos); R$ NÍTIDO; punch = números LITERAIS dos prints. **Print ALTO é CLIPADO em silêncio:** o engine limita o card a 360px (`.print{max-height:360px}`) — se `altura_original × largura_no_slide ÷ largura_original > 360`, o fim da mensagem some SEM aviso. Cropar a bolha essencial antes e CONFERIR NO PNG que a última linha aparece inteira. *(Caso real 09/jul: o "de outubro" que sustentava o punch sumiu no clip; e não chute coordenada de crop em screenshot alto — meça as bolhas por varredura de pixel ou itere crop→olhar.)*
  - **CTA:** card Figma verbatim + "TOQUE NO LINK DA BIO" (ou COMENTE "SUPERCASO" quando o usuário pedir).
- [ ] **`img/NECESSARIO.txt`** criado no início e atualizado (o usuário deposita as imagens lá).
- [ ] **`open` no `preview.html`** sempre que renderizar pro usuário.

## 6 · Produção em LOTE (2+ posts de uma vez — 09/jul, lote sexta/sábado/domingo)

- [ ] **MAPA DE TERRITÓRIO antes da primeira palavra (PARE):** ler o `copy.engine.json` de TODOS os posts já publicados da semana e listar o que cada um REIVINDICOU: frases literais dela já usadas, fórmula do hero, abertura da legenda, dispositivo do burn, formato do punch de prova, prints usados. O que está no mapa NÃO se reusa. *Casos reais de hoje, pegos só pelo mapa: "ninguém acorda querendo botox" ia ser um hero — o AD012 já tinha usado no body; "prateleira de supermercado" ia pra legenda — era do AD008; "nenhuma paciente sai sem retorno" ia pra alavanca 4 — era item do AD004.*
- [ ] **VARIAÇÃO INTERNA DO LOTE:** posts que saem em dias seguidos variam ENTRE SI (não só vs o último postado): fórmula de gancho do hero, abertura da legenda, burn do MANDA e formato do punch de prova — os quatro eixos, checados em tabela.
- [ ] **REGISTRO DE PRINTS:** print postado não volta; print da MESMA clínica com o mesmo detalhe-estrela também não (caso "R$250 de tráfego"); verbatim RARO dela (ex.: "Quem entendeu isso tem vivido essa realidade") = no máximo UM uso por lote.
- [ ] **Prova cruzada no portão:** o workflow de auditoria recebe, além dos postados, os OUTROS posts do lote — repetição interna é reprova igual.

## 7 · Antes de entregar **(PARE)**

- [ ] **Portão adversarial rodado** (Workflow: finders por dimensão → verificação adversarial que refuta por padrão). TODOS os diffs confirmados aplicados, re-render, overflow re-conferido.
- [ ] **Entrega com:** resumo por slide + legenda completa + âncoras citadas (peça + marcador) + o que falta + status honesto do que foi e não foi verificado.
- [ ] **Export só após aprovação:** `[AA] [SS] [AD00N_M] - Título.png` na raiz (ano 26, semana ISO). Nunca sobrescrever exportado — post novo = pasta nova.

---

## Armadilhas nomeadas (os erros que JÁ aconteceram — conferir uma a uma)

| # | Armadilha | Teste que pega |
|---|---|---|
| 1 | **Passo inventado por analogia** ("aposente a alta", "áudio 30s", "aos poucos sai mais caro") | Tabela de âncoras ANTES da copy (§2) |
| 2 | **Falso verbatim** (linha dela, mecanismo trocado) | Âncora cobre o MOVIMENTO (§2) |
| 3 | **Paráfrase que dilui** ("nunca"→"quase nunca") | Diff palavra a palavra vs original (§2) |
| 4 | **Fragmento sem referente** (aspa que não se explica) | Leitura fria da aspa isolada (§3C) |
| 5 | **Etiqueta de swipe** (rótulo simétrico pós-frase) | Zero texto após a aspa; formas variadas (§3C) |
| 6 | **Verbatim comprimido** (regra sem a cena) | Item responde "por quê/como assim?" (§3C) |
| 7 | **Body que repete o punch** | Última frase do body ≠ punch (§3C) |
| 8 | **Legenda-eco** | Comparação literal lado a lado (§4) |
| 9 | **Tema clonado** (AD006 ≈ AD003) | Ideia central × todos os postados (§1) |
| 10 | **Render fantasma** (PNG velho lido como novo) | `ok slide_N` + mtime fresco (§5) |
| 11 | **Quebra de hero torta** (linha auto-quebrada) | Conferir quebras NO RENDER (§5) |
| 12 | **Frase à paciente expondo limitação do produto** | Regra dura (§3D) |
| 13 | **Referência cultural fora do timing** | Perguntar antes de escrever (§1) |
| 14 | **Escrever uma vez e se aprovar** | PASSE E inteiro — o adversário interno |
| 15 | **Metralhadora de punchline** (todo slide/parágrafo termina em facada) | Última frase de cada slide/¶: efeito em ≤ metade (§3D / legenda cheiro #1) |
| 16 | **Colagem de verbatim** (3-4 linhas dela, TODAS reais, empilhadas num slide só — no corpus viviam em slides separados; vira ritmo de robô mesmo sendo 100% ela) | Contar aforismos vale TAMBÉM pra verbatim: >1 linha-assinatura por slide → espalhar ou cortar (caso 09/jul, AD011 slide 3) |
| 17 | **Testemunho fabricado na 1ª pessoa** ("Eu já vi doutora brilhante desistir...") | "Eu vi/atendi/conheci" + caso = precisa de âncora igual a qualquer número; sem fonte → vira "eu sei como pesa" (empatia), nunca caso (caso 09/jul) |
| 18 | **Framework renomeado/misturado** (rótulo dela + conjunto diferente do que ela publicou: "4 alavancas" com uma alavanca trocada) | Se o rótulo é dela, o CONJUNTO inteiro tem que bater com a peça-fonte; mistura de peças = rótulo novo neutro (caso 09/jul) |
| 19 | **Causa inventada na prova** ("o feed captando" num print que credita "comercial alinhada"; "janeiro incluso" sem breakdown mensal) | O punch só AFIRMA o que o print MOSTRA; editorial não atribui causa que a aluna não disse (2 casos 09/jul) |
