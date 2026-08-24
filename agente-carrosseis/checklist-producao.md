# Checklist de Produção — Carrossel RECONECTA
> **Para quem é:** o modelo que estiver produzindo (escrito pro Opus; o Fable também roda).
> **O que é:** o self-check que roda DURANTE a produção — antes do portão adversarial (`portao-qualidade.md`), que continua sendo o juiz final. O portão pega o que escapou; este checklist existe pra chegar lá com quase nada escapando.
> **A tese:** a diferença entre um carrossel de Fable e um de Opus não é conhecimento, é AUTOCRÍTICA. O Opus escreve uma vez e se aprova; o Fable escreve e depois ataca o próprio texto como se fosse outra pessoa. Este arquivo converte esse ataque em passes explícitos. Rodar TODOS, na ordem, com evidência (o grep, o render, a comparação lado a lado). Marcar item sem evidência = teatro.
> Item **PARE** reprovado → não avança até resolver. Todos os "casos reais" citados aconteceram nesta operação (jul/2026) e custaram retrabalho e confiança do usuário.
> **GATILHO OBRIGATÓRIO (pedido do usuário, 09/jul):** os PASSES B→E rodam **TODA VEZ que uma copy sai — de carrossel OU de legenda, versão nova OU reescrita, mesmo um ajuste de uma frase.** Não existe "mudança pequena demais pra checar": as piores reprovações vieram de ajustes que pareciam pequenos. Copy entregue sem os passes rodados = copy não terminada.

---

## PRE-FLIGHT — os 6 cheques que pegaram TUDO nesta operação (rodar SEMPRE, com evidência)

Dado da SEM32 (04/ago): o portão confirmou 78 defeitos em 8 posts produzidos "seguindo
o checklist". Quase todos caem em 6 famílias. Rode ESTES seis com evidência antes de
qualquer outra coisa — o resto do checklist detalha, mas é aqui que se ganha o jogo:

1. **Eco legenda↔slide** — nenhum parágrafo da legenda recicla frase/cena de slide
   (diff literal, parágrafo a parágrafo).
2. **Eco <14d vs PUBLICADO** — punch/frase/capa contra `territorio-vivo.json` E contra
   os posts publicados das 2 semanas (o lote da semana conta como publicado).
3. **D5 doutrina** — `python3 doutrina.py <assunto>` pra cada assunto prescrito; nunca
   contradizer em silêncio (nem post antigo, nem a peça-fonte, nem o par do dia).
4. **Prova conecta e não desmente** — o print prova a TESE deste post (não credita
   outra causa), é inédito (`prints_usados.py` no candidato E no lote) e o punch
   argumenta sem ecoar o texto do print.
5. **Adjacência interna do lote** — os 2 posts do MESMO dia não dividem dispositivo,
   fórmula de capa, molde de legenda nem tese; dias seguidos não repetem fórmula no
   mesmo trilho.
6. **PRE-FLIGHT MECÂNICO ANTES DO PORTÃO (06/ago):** rode o cálculo de *run máximo
   de palavras contíguas* da legenda contra cada slide, e da legenda/punches contra
   os OUTROS posts do mesmo dia. Limite: 3 palavras. **Exceção única:** o §5 da
   legenda espelha o CTA do card por exigência da E2 — ali o run alto é correto.
   *Por que virou item: no AD012 (06/ago) os 33 agentes do portão não pegaram duas
   colisões de 4-grama com o AD007 do MESMO DIA ("no seu feed agora" e "e manda pra
   colega que"); um script de 20 linhas pegou as duas em 2 segundos. Verificação
   mecânica não substitui o portão, mas o portão também não substitui ela — o que é
   contável se conta, não se julga.*
7. **Âncora de TUDO** — número/frase/claim sem linha na tabela de âncoras não entra;
   "plausível no espírito" é inventado (caso R$4 mil: o painel da pauta inventou e a
   produção quase herdou).

## 0 · Setup (antes de qualquer palavra)

- [ ] **Li `voice-dna.md` INTEIRO nesta sessão** — os 5 dispositivos, o CANON, "O CHEIRO DE IA", a legenda-fórmula e TODOS os anti-padrões.
- [ ] **Li `portao-qualidade.md`.**
- [ ] **Sei o que já foi postado na semana** e qual foi a fórmula de gancho e o rótulo de lista de cada um. *Como: `ls` na `SEM__/` + `copy.engine.json` de cada AD exportado. Regra VARIE: não repetir fórmula de gancho nem rótulo de lista do post imediatamente anterior; não reabrir a legenda com o dispositivo do post anterior.*
- [ ] **STATUS DE PUBLICAÇÃO antes de EDITAR qualquer post (PARE — 21/jul):** a pasta não diz se foi ao ar e o perf-manual só ganha entrada quando chegam números. Regra: todo post publicado ganha `POSTADO.txt` na raiz da pasta (com a data) NO DIA da publicação; pasta sem o marcador e com dúvida → PERGUNTAR ao usuário antes de tocar em copy/render/export. *Caso real 21/jul: troquei a hero do SEM30/AD001 já publicado achando que estava no banco; o Sávio pegou e revertemos. Post publicado é IMUTÁVEL.*

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
   - **GERAÇÃO POR SELEÇÃO (PARE — 28/jul, `gabarito-punchline.md`):** punch de topo NUNCA sai de primeira tentativa. Pra cada punch: 5 candidatos (um por MECANISMO do gabarito: contraste seco, reframe disruptivo, desproporção, cena+virada, número, pergunta-paradoxo), leitura em voz alta, 4 morrem, o sobrevivente enfrenta o benchmark da sua mecânica. Registrar os mortos — o portão (B6.3) confere que a seleção existiu. *Motivo: checklist detecta erro; não gera acerto. Copy limpa e morna passava em tudo.*
   - **DOUTRINA FIXA (PARE — 07/ago):** ler `doutrina-fixa.md` INTEIRO antes de escrever prescrição. É o que a metodologia ENSINA (fonte: o Sávio), enquanto o `doutrina.py` é o que os posts já disseram — e post publicado pode estar errado. *Casos que criaram o arquivo: (a) o AD013 mandava tirar o CRO da bio quando a casa ensina que o registro FICA e a linha de posicionamento se SOMA; (b) "educação" como rótulo cru de pilar, três dias depois de uma capa nossa dizer que "a paciente que você educa fecha com a concorrência".*
   - **DOUTRINA ANTES DA PRIMEIRA PRESCRIÇÃO (PARE — 30/jul):** todo post que ensina alguma coisa (item de lista, script, regra) roda `python3 doutrina.py <assunto>` ANTES de escrever, pra cada assunto que vai prescrever — abatimento, preço, sinal, agendamento, comparecimento, retorno, whatsapp, objeção, conteúdo, triagem. O acervo já mandou a doutora fazer coisas; **contradizer o que a gente mesmo ensinou é pior que repetir**. Se a prescrição nova inverte a antiga: alinha, ou corrige explicitamente na copy, ou troca o ângulo — nunca em silêncio. *Caso real que criou a regra: o SEM31/AD006 mandava "NUNCA PROMETA O ABATIMENTO" e o SEM25/AD003 (campeão, s/r 3,95% × mediana 0,64%) ensinava o oposto — segure e TROQUE por compromisso de agendamento. O Sávio pegou lendo o post antigo, não o portão.* Vira a dimensão **D5** do `portao-qualidade.md`.
   - **TERRITÓRIO VIVO ANTES DA PRIMEIRA PALAVRA:** rodar `python3 territorio_vivo.py` e consultar `data/territorio-vivo.json` (punches, 4-gramas, fórmulas de capa, proofs e burns dos últimos 21 dias — mapa MECÂNICO, não de memória). O que está lá não se reusa; o julgamento de PARENTESCO (família de frase queimada, ex.: "financeiro"≈"marido") continua sendo seu, sobre o mapa completo.
   - **Verbatim vence paráfrase:** se a âncora tem um marcador de voz que JÁ É a tese do slide, o punch é o VERBATIM dela, não a sua versão. *Caso real (AD001, 15/jul): escrevi "QUEM QUEBRA O SILÊNCIO PRIMEIRO, PAGA POR ELE" com "Quem fala primeiro, perde." disponível no corpus — o portão restaurou o dela.*
3. **Arquitetura de funil (regra do Sávio, 14/jul/26):** capa = TOPO de funil (dor ou cena ampla que a doutora FRIA reconhece na hora; zero jargão de metodologia, zero nome de framework, zero promessa de fundo); slide 2 = MEIO de funil (a prova ou o porquê que conecta a dor ao mecanismo); slides 3+ = FUNDO de funil (mecanismo, aplicação, script, CTA). Base em dado: os 16 hits com s/r ≥ 3% (análise de 14/jul) abrem todos em reconhecimento amplo — a fala da paciente entre aspas é TOFU porque é cena, não mecanismo.
4. Bodies montados A PARTIR das âncoras (preferir montar com as linhas literais dela a "escrever no estilo dela").
5. Legenda por último, já em modo anti-eco (seção 4).

### PASSE B — Frase a frase (rodar em CADA frase do carrossel)
- [ ] **Teste da voz alta:** li em voz alta. Soa como ela falando com uma doutora, ou como redator escrevendo? Marcadores de redator: construção elegante demais, ritmo perfeito, abstração ("a pergunta que ela veio responder" → reescrever).
- [ ] **Teste do "quem diria isso":** ela diria ESSA frase num áudio de WhatsApp? Se só existe no papel, não é dela. *Marcadores de papel: "da que enrola à que joga...", "cujo", "sob", gerúndio encadeado, aposto explicativo longo.*
- [ ] **Teste do corte:** se eu deletar esta frase, o slide perde algo? Não perde → deleta. (A maioria das frases de IA existe pra "completar o parágrafo", não pra dizer algo.)
- [ ] **Palavras amaciadoras:** "quase", "meio", "um pouco", "talvez", "acaba que" — ela é assertiva; amaciador sem função = cortar. *Caso real: "quase nunca é sobre o marido" (o verbatim dela é "nunca").*
- [ ] **Pessoa e registro consistentes** dentro da frase e do slide (lead/ela, você/tu — não misturar no mesmo período).
- [ ] **Rabo sem âncora = cortar.** Frase literal dela NÃO ganha extensão minha emendada ("...e a pergunta fica com ela", "Ela ouve isso sem você falar nada"). O verbatim fecha a frase; se a aterrissagem extra não tem âncora própria (grep no corpus ANTES), ela não existe. *Caso real: as duas extensões acima caíram no portão do AD001 (15/jul) por grep negativo.*

### PASSE C — Slide a slide
- [ ] **O body NÃO reafirma o punch.** Teste explícito: a última frase do body diz o mesmo que o punch com outras palavras? → trocar por uma aterrissagem NOVA (detalhe concreto, monólogo interno, gancho pro próximo slide). *Caso real: punch "some na sua próxima mensagem" + fecho do body "a tua mensagem seguinte matou" = a mesma tese 2x no mesmo slide.*
- [ ] **Leitura fria de cada aspa:** li a frase pronta SOZINHA, como se chegasse no meu WhatsApp sem contexto. Tem referente? Dá pra responder? Depende de setup que não está ali → restaurar o setup ou trocar a linha. *Caso real: "É isso mesmo, ou eu tô enganada?" solta — "não tem pé nem cabeça essa p*rra".*
- [ ] **LEITURA FRIA DA CAPA, LINHA POR LINHA (PARE — 29/jul).** O teste acima vale pra ASPA; a capa exige mais: **cada linha** tem que se sustentar sozinha, porque a capa é lida por quem tem ZERO contexto, em 2 segundos, rolando o feed. Ler a última linha isolada e perguntar: *falta alguma palavra aqui?*
  - **Elipse sem verbo é o erro clássico**: "nunca mais", "e pronto", "e já era", "e olhe lá", "e nada" — todas pedem um verbo que a cabeça do leitor não completa sozinha. *Caso real 29/jul: a capa do AD004 saiu "«Isso é só na avaliação.» «Agenda pelo link.» E A LEAD, NUNCA MAIS." e o Sávio pegou no preview: "nunca mais O QUÊ? erro grotesco". Fix: "E A LEAD FOI EMBORA." (sujeito + verbo explícitos).*
  - **O portão não pega isso sozinho**: 59 agentes passaram batido porque as dimensões miravam território/eco/voz. Este teste é do PRODUTOR, e o portão ganhou a dimensão SENTIDO pra cobrir (ver `portao-qualidade.md` C5).
  - **Ao consertar, re-checar o território da palavra nova**: o primeiro conserto que escrevi ("E A LEAD NUNCA MAIS RESPONDEU") usava "respondeu", raiz que estava na CAPA do dia anterior — e "voltou", a outra opção óbvia, estava em duas capas de 10 e 1 dia. Conserto de sentido não dispensa o grep.
- [ ] **Aforismos ≤ 1 por slide** (contar, não sentir). Dois seguidos → um vira cena.
- [ ] **Etiqueta pós-aspa = 0.** Nada de rótulo depois da frase pronta ("Isso reabre a conversa.", "Ela vira sua aliada."). A frase se explica; o que humaniza é o ERRO encenado ANTES dela. *Caso real: 4 itens com etiqueta simétrica = "cara de IA" na hora.*
- [ ] **Cada item de lista responde sozinho "por quê / como assim?"** Não responde → encenar o erro antes da regra (verbatim comprimido = manual).
- [ ] **Formas VARIADAS entre itens:** um abre pelo erro, outro solta a frase seca, outro reframe. Molde repetido (setup + "Devolve:" + aspa ×4) = mecânico. Variar também os VERBOS de comando (grep: um mesmo verbo estrutural ≤2 no slide).
- [ ] **Fechos dos itens variam TAMBÉM:** máx 1 selo/kicker curto por lista — 3 itens fechando com selo no mesmo ritmo e sobre o mesmo sujeito ("...fica com ela" / "...ELA faz" / "...sem você falar nada") = simetria mecânica. *Caso real AD001, 15/jul.*
- [ ] **Eco vizinho título↔body:** o fecho de um item não repete string do TÍTULO do item seguinte (o grep de ecos inclui títulos, não só bodies). *Caso real: "a pergunta fica com ela" colado em "O PROBLEMA FICA COM ELA".*
- [ ] **Slides de entrega têm as 4 camadas:** ação concreta + mecanismo causal + exemplo vivo (frase pronta/vignette) + frame. Slide de entrega sem exemplo vivo = aula.
- [ ] **Escada da especificidade:** toda palavra abstrata que sobrou (experiência, valor, cuidado, transformação usada como conceito) → dá pra trocar por cena, objeto, hora ou número? Troca. ("ela se sente cuidada" → "um áudio de 20 segundos numa terça, sem motivo").

### PASSE D — O carrossel inteiro
- [ ] **METRALHADORA DE PUNCHLINE (o bafo que o usuário mais odeia — 09/jul).** IA escreve frase de impacto O TEMPO TODO; gente deixa frase terminar normal. Teste em duas escalas, contando: **(a) escala carrossel:** olhe SÓ a última frase do body de cada slide — final "de efeito" em TODOS os slides = robô; pelo menos 2 slides terminam em coisa comum (um fato, uma cena, um pedido, o gancho pro próximo). **(b) escala slide:** depois do punch do topo, a primeira frase do body RESPIRA (cena/fato), não emenda outra facada. O punch é o tiro; o body é a cena. *Na legenda, o mesmo teste é o cheiro #1 do `checklist-legenda.md` (máx 2 finais de efeito em 5 parágrafos).*
- [ ] **Leitura em sequência como a leitora** (hero → 2 → 3 → 4 → 5 → CTA → legenda, sem parar): cada slide puxa o próximo? A promessa da capa é entregue? Algum slide repete ideia do vizinho?
- [ ] **Teste do encaminhamento (28/jul — dado da análise SEM29/30):** terminei de ler e respondo por escrito "pra quem, especificamente, a doutora MANDA isso?" (a sócia, a secretária, a colega que faz X). Se a resposta honesta é "ela salva pra ela" → o post é útil mas não distribui; procurar o slide/frase que dá o motivo de ENVIO (a frase que a outra pessoa precisa ver) e afiar ali. *Dado: save subiu (1,60→1,72%) enquanto share caiu (1,38→1,09% mediana; teto 5,79→3,21%) — estávamos escrevendo "útil de guardar", não "urgente de mandar". O burn do MANDA na legenda (§4) já mira isso; este teste confere se o CARROSSEL dá o motivo.*
- [ ] **Arco de funil (binário):** a capa lê TOFU (doutora fria se reconhece sem nenhum contexto)? O slide 2 é MOFU (prova/porquê)? Jargão de metodologia e nome de framework só aparecem do slide 3 em diante? Capa com mecanismo ou promessa de fundo = reescrever a capa, não o resto.
- [ ] **Contagem de ecos por grep** (não de cabeça): palavra-conceito do tema ≤2 no carrossel; verbo estrutural repetido ≤2; construção sintática assinatura ("Você não X. Você Y." / "Quem X, Y") ≤1.
- [ ] **Quotas de dispositivos (mínimos, com citação):** ≥1 frase pronta exata POR slide de entrega · ≥1 contraste seco no carrossel · ≥1 detalhe concreto inesperado · ≥1 monólogo interno + punch · número de capa escalado/específico quando houver número.
- [ ] **Emphasis nos lugares certos:** `{vermelho}` na palavra disruptiva do punch (não em palavra neutra); `«champagne»` só em aparte/ironia.
- [ ] **Regras duras:** zero travessão no meio de frase · zero "high/alto ticket" · zero "HOF"/"harmonização orofacial" (é **harmonização facial**, por extenso) · zero @handle · zero dado sem print/fonte · frase à paciente jamais expõe limitação do produto (retorno = parte do tratamento) · copy do usuário é literal (ênfase só por cor/peso).

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

> **Versão completa:** `checklist-design.md` (régua física do engine, art direction da hero, fx por foto, inspeção slide a slide, engine-vs-post, 15 armadilhas com caso real). Este §5 é o resumo; em produção, rodar o arquivo dedicado.

- [ ] **PROTOCOLO DE RENDER VERIFICADO (PARE — endurecido em 24/ago/26, caso "CTA 715"):**
  o render só conta como feito depois de QUATRO evidências, nesta ordem:
  1. `cd carrosseis/_template/html-engine && python3 engine.py "<pasta>/copy.engine.json" "<pasta>/slides"`
     — o `cd` vai NO MESMO comando (o cwd do shell persiste entre chamadas: um `cd`
     de outro passo quebra o caminho relativo do engine e o python morre em silêncio).
  2. **Ver as linhas `ok slide_N` impressas, uma por slide.** NUNCA filtrar a saída
     com `grep -c`/contagem: o erro do python vira "0 avisos" e parece aprovação.
     Se as linhas `ok` não aparecerem, o render NÃO aconteceu — não importa o que o
     pipe disse.
  3. **mtime fresco** dos `slides/slide_N.png` (`ls -la`) — hora de agora, não de horas atrás.
  4. **Leitura VISUAL (Read) de todo slide cuja copy/imagem mudou**, antes de
     exportar e antes de avisar o usuário. "O JSON está certo" não prova nada: o
     usuário vê o PNG.
  Só depois disso: exportar (`[AA] [SS] [AD00N_M] - Título.png`). Export de PNG
  velho = entregar o erro com carimbo de novo.
  *Caso real (24/ago/26): duas re-renderizações do AD001/SEM35 rodaram com cwd
  errado; o `grep -cE "⚠"` engoliu o erro do python e imprimiu "0"; os PNGs antigos
  (CTA SUPERCASO) foram re-exportados como novos DUAS vezes e o Sávio recebeu duas
  entregas erradas seguidas ("aqui não aparece que você atualizou nada" e depois
  "pq o ad001 ainda está com cta supercaso??"). O JSON estava certo desde o início —
  a imagem, não.*
- [ ] **Preview no navegador tem CACHE:** depois de re-render, avisar o usuário de
  recarregar com força (Cmd+Shift+R) ou reabrir o preview — aba antiga mostra PNG
  velho e a entrega certa parece errada. Antes de discutir "não mudou nada",
  verificar o ARQUIVO em disco (Read no PNG), nunca a lembrança nem o navegador.
- [ ] **`_overflow.json` não existe.** Se existir: cortar COPY (nunca fonte). Micro-corte não resolve — derrubar LINHA inteira: caçar linha órfã (1-2 palavras) no PNG e encurtar ali.
- [ ] **Abri e OLHEI cada PNG** (Read em todos, SEMPRE que a copy ou imagem mudar):
  - **Hero (engine atualizado 14/jul):** o engine NUNCA mais quebra linha art-directed no meio — desce a fonte de 98px até a linha mais longa caber (piso 60px; abaixo disso avisa "REQUEBRAR" e grava `_overflow.json`). Conferir no render: linhas do PNG = `\n`+1 e corpo não desceu de ~78px (log "hero fit"). Cantos superiores VAZIOS. Legibilidade sobre a foto: fx escolhido OLHANDO a foto (`checklist-design.md` §1.3).
  - **Photo/text/list:** gap uniforme, nada colado em borda, corpo ≥30.
  - **Proof — a SELEÇÃO de prints é do agente, nunca do usuário (regra do Sávio, 15/jul):** pool curado nos `img/depoimentos-sugeridos/` das semanas + `DEPOIMENTOS-MAP.md`. REGISTRO por PÁGINA: pXX que já foi ao ar não volta, mesmo em arquivo/crop/versão diferente; detalhe-estrela da mesma clínica idem (caso "tráfego R$250" — cropar a linha resolve); tema do print casa com a TESE do post (ticket alto pra post de preço, consultas pra post de consulta). O punch só fecha DEPOIS dos prints escolhidos, com número literal deles.
  - **Proof (engine atualizado 14/jul):** o bloco de prints abraça o conteúdo sozinho (log "proof fit"; `block_h` só pra travar altura na mão) — conferir clareira equilibrada em cima/embaixo; NENHUM nome/telefone/CNPJ/avatar legível (crop/blur PIL em `_anon`/`_crop`, originais intactos); R$ NÍTIDO; punch = números LITERAIS dos prints. **Print ALTO é CLIPADO em silêncio:** o engine limita o card a 360px (`.print{max-height:360px}`) — se `altura_original × largura_no_slide ÷ largura_original > 360`, o fim da mensagem some SEM aviso. Cropar a bolha essencial antes e CONFERIR NO PNG que a última linha aparece inteira. *(Caso real 09/jul: o "de outubro" que sustentava o punch sumiu no clip; e não chute coordenada de crop em screenshot alto — meça as bolhas por varredura de pixel ou itere crop→olhar.)*
  - **CTA:** card Figma verbatim + "TOQUE NO LINK DA BIO" (ou COMENTE "SUPERCASO" quando o usuário pedir).
- [ ] **CAPA × SLIDE 2 É DECISÃO, NÃO SORTEIO (regra do Sávio, 24/ago/26):** com o
  par de fotos do post na mão, comparar as duas PELO PAPEL: capa = a foto que conta
  a história da headline (protagonista da cena, tensão, cantos livres, terço
  inferior escurecível); slide 2 = a foto do erro/da outra personagem. Registrar no
  ORIGEM por que cada uma ganhou o lugar. *Caso real: no "Ela Veio Fazer Botox" a
  foto editorial elegante estava na capa e a "ela" da história no slide 2 —
  invertidas, a capa passou a mostrar a protagonista da frase.*
- [ ] **ALTERAÇÃO DE DESIGN SÓ COM OK DO SÁVIO (PARE — regra dele, 24/ago/26):**
  fx, sombra, fonte, espaçamento, tipo de slide novo, skin — propor com preview
  comparativo e ESPERAR a aprovação; nunca aplicar e avisar depois. Padrão vigente
  de capa A: `fx:{scrim:"strong"}` SEM `shadow` (o fade segura a legibilidade; a
  sombra na fonte foi banida por ele). Exceção única: bug fix que restaura
  comportamento já aprovado.
- [ ] **IMAGENS: POOL SEMANAL, SELEÇÃO NOSSA (novo fluxo, 28/jul):** o Sávio deposita ~20 imagens em `/Volumes/SSD kenipe/downloads/IMG/SEM{xx}/` no início da semana — a seleção é do agente, post a post (como nos prints). Critérios: capa A = cena que encena a tese + cantos superiores vazios + terço inferior escurecível; capa B = retrato editorial com ROSTO NO TERÇO SUPERIOR (o texto vive em 800-1140) e, se possível, objeto que conta a piada da headline (caso 28/jul: telefone antigo + cara de tédio pro post do áudio); slide2 = cena do erro/momento, zona inferior livre. Celebridades reconhecíveis do pool → reservar pros slots de trend. Registrar no NECESSARIO.txt qual arquivo foi usado onde (imagem usada não repete na semana).
- [ ] **`img/NECESSARIO.txt`** criado no início e atualizado (registra a imagem escolhida por slide).
- [ ] **`open` no `preview.html`** sempre que renderizar pro usuário.

## 5-B · MIX EDITORIAL DA SEMANA (regra do Sávio, 15/jul/26 — vale pra toda pauta)

Toda semana de conteúdo mira **80 / 10 / 10**:

- **~80% VALIDADO** — o pipeline atual: tema ancorado no corpus + engenharia reversa dos 16 hits (s/r ≥ 3%), checklists, portão. É o piso confiável.
- **~10% NOTÍCIA EM ALTA** (1 slot/semana, CONDICIONAL) — notícia de conhecimento GERAL no pico (≤72h do auge; regra nascida do caso Spotify, morto por timing em 06/jul; caso-canon de acerto: Vini Jr SEM30/AD002, 20-21/jul). Fluxo (v2, 21/jul): skill `radar-trends-quentes` roda DIÁRIO 07:20 (LaunchAgent `com.reconecta.radar-quente` → `run-radar.sh` → `data/radar-quente.json` + aviso Slack/macOS) — celebridade/esporte/TV/viral ENTRAM aqui, diferente do evergreen `tendencias-research` (Seg/Qua/Sex, alimenta os 80%) → candidato passa no filtro RADAR (janela ≤72h + ponte sem distorção + risco de marca + fatos etiquetados com atribuição) → a notícia vira a CENA do slide 1 (TOFU natural) e o nosso ensino entra do slide 3+ (mesma arquitetura de funil). Radar APONTA com mini-ponte; produção só com OK do Sávio. **Não passou no filtro = slot vira validado** — nunca adaptar tendência na marra.
- **~10% DISRUPTIVO** (1 slot/semana) — tese CONTRÁRIA a uma crença que o próprio mercado de estética/mentoria vende, sustentada pela nossa metodologia. Precedente real no acervo: "Agradeça quando o lead disser vou pensar" e "Quanto mais você responde objeção, menos fecha" (s/r 4,13%). Regras duras: nunca contradizer a metodologia; âncora obrigatória em ensino real; no portão, refutador extra com a pergunta "isso queima a marca ou só incomoda o suficiente?".

Linha editorial pedida pelo Leonardo (Slack, 14/jul): dois públicos a cobrir no calendário — **(a) iniciante com medo de vender/não saber oferecer** (âncora no acervo: hit 08/jun "A gente acha que está sendo gentil. Na verdade, está com medo.", s/r 3,02%) e **(b) quem tem lead mas sem ticket médio / perde venda / consulta longa** (o território campeão, mediana s/r 2,05%). O pilar (a) entra como slot recorrente a partir da SEM30.

## 6 · Produção em LOTE (2+ posts de uma vez — 09/jul, lote sexta/sábado/domingo)

- [ ] **MAPA DE TERRITÓRIO antes da primeira palavra (PARE):** ler o `copy.engine.json` de TODOS os posts já publicados da semana e listar o que cada um REIVINDICOU: frases literais dela já usadas, fórmula do hero, abertura da legenda, dispositivo do burn, formato do punch de prova, prints usados. O que está no mapa NÃO se reusa. *Casos reais de hoje, pegos só pelo mapa: "ninguém acorda querendo botox" ia ser um hero — o AD012 já tinha usado no body; "prateleira de supermercado" ia pra legenda — era do AD008; "nenhuma paciente sai sem retorno" ia pra alavanca 4 — era item do AD004.*
- [ ] **VARIAÇÃO INTERNA DO LOTE:** posts que saem em dias seguidos variam ENTRE SI (não só vs o último postado): fórmula de gancho do hero, abertura da legenda, burn do MANDA e formato do punch de prova — os quatro eixos, checados em tabela.
- [ ] **REGISTRO DE PRINTS — VARREDURA POR IMAGEM (PARE — 29/jul, substitui a varredura por punch):** rodar `metricas-ig/.venv/bin/python3 prints_usados.py <candidato.png>`, que compara a IMAGEM (dHash 256 bits, limiar 22 — aguenta recorte, escala e recompressão). A varredura por PUNCH continua útil como segunda passada, mas é falso-negativa por construção: um print vai ao ar sem que o punch cite o número dele. *Caso real 29/jul: o p06 foi publicado inteiro, com nome, no SEM27/AD003 e passou como "inédito" na varredura por punch.* **E rodar o script sem argumento antes de fechar o lote**, pra pegar dois posts do MESMO dia usando o mesmo arquivo — *caso real 30/jul: SEM31/AD006 e AD007 saíam na mesma quinta com o print idêntico (distância 0), cada um citando uma linha diferente da mesma conversa; nenhuma regra de texto pegaria isso.* Depois da varredura por imagem, continua valendo: *Caso real 28/jul: a lista de memória falhou DUAS vezes no mesmo dia — p28 ("17 novos agendamentos") era o proof do SEM29/AD002 e p10 ("bati 600k") era o do SEM27/AD009; os dois teriam ido ao ar repetidos. O punch não mente; a lista mente.* Print postado não volta; print da MESMA clínica com o mesmo detalhe-estrela também não (caso "R$250 de tráfego"); verbatim RARO dela = no máximo UM uso por lote. **Punch de proof sem aspas quando o print é relatório/lista** (aspas = citação; relatório ninguém "falou") e nunca afirmar período/causa que o crop não mostra (caso "NO MÊS", 28/jul).
- [ ] **REGISTRO DE FRASES-TESE — É CONTADOR, NÃO VETO (revisto em 30/jul):** verbatim dela usado como punch/tese em 2+ posts nas últimas ~6 semanas → registrar no bloco `queimadas` do `headlines-repertoire.json` e CONSULTAR esse bloco antes de ancorar punch novo. **A política do Sávio é repetir o que funciona** ("a intenção é sempre repetir o que pode ter feito um post se sair muito bem", 30/jul). Então o registro serve pra você DECLARAR o desgaste — nº de usos + distância do último — e decidir, não pra bloquear sozinho. Só é reprova quando: (a) a repetição cai em posts ADJACENTES no feed (mesmo dia ou dias seguidos), ou (b) a formulação inteira é copiada palavra por palavra, sem ângulo novo. Fora disso, repetir é legítimo — e frequentemente é o certo. *Caso real 30/jul: "a consulta é abatida no procedimento" estava marcada até SEM34 com 2 usos e eu travei o post inteiro; a resposta do Sávio foi liberar. O erro não foi repetir, foi tratar o contador como muro.*
- [ ] **Prova cruzada no portão:** o workflow de auditoria recebe, além dos postados, os OUTROS posts do lote — repetição interna é reprova igual.

## 7 · Antes de entregar **(PARE)**

- [ ] **Portão adversarial rodado** (Workflow: finders por dimensão → verificação adversarial que refuta por padrão). TODOS os diffs confirmados aplicados, re-render, overflow re-conferido.
- [ ] **Reconciliação de diffs conflitantes (15/jul):** finders diferentes propõem fixes diferentes pra MESMA linha — nunca aplicar em sequência cega. Prioridade: 1º restaurar/preservar verbatim dela · 2º matar o eco/defeito confirmado · 3º contagens de palavra.
  · *Conserto mínimo preserva a mecânica campeã (04/ago, palavra do Sávio):* "sempre reaproveite as mecânicas que fizeram os campeões serem campeões, trazendo ângulos novos — não trocando tudo". Ao aplicar diff de eco/queimada, a PRIMEIRA opção é variar o mínimo (trocar as palavras que colidem, manter o movimento, a estrutura e a fórmula que performou); reescrever o alvo inteiro é o último recurso, só quando o defeito é a própria mecânica. Diff que "conserta" jogando fora o dispositivo vencedor cria defeito maior do que o que mata.
  **CASEBOOK DE ADJUDICAÇÃO (28/jul — como decidir quando as PRÓPRIAS regras colidem; toda exceção é DECLARADA no relatório, nunca silenciosa):**
  · *Verbatim dela × território reaceso (<7d):* o verbatim SÓ vence se está no uso ancorado original; se é TRANSPLANTE de movimento (ex.: "dá pra resolver isso por aqui mesmo" de foto→áudio) e a string reacendeu num post recente, o território vence — paráfrase declarada que preserva o MOVIMENTO. (Caso: SEM31/AD003 S3.)
  · *Diff confirmado do portão × palavra queimada DENTRO do diff:* nunca aplicar cego — reescrever o diff sem a palavra (caso: diff sugeria "leva pra casa" com "em casa" queimado; virou "antes de te agradecer na saída").
  · *Dois confirmados que se contradizem:* aplicar o de MAIOR severidade e re-rodar o teste do outro no estado final (nunca os dois em sequência).
  · *Achado sem veredito (teto de verificação):* NUNCA absolver por silêncio — adjudicar um a um com evidência, no critério acima, e listar cada decisão (48 casos em 28/jul). Depois de aplicar TODOS os diffs, **re-grep dos ecos no estado final** — diff pode criar eco novo (caso "fala primeiro" 2×: dentro da cota, mas tem que ser contado e declarado, não descoberto pelo leitor). **E leitura fria da PALAVRA nova, principalmente em capa**: diff que troca palavra de headline re-roda o teste de ambiguidade — o refutador checou a colisão dele, não a palavra dele. *Caso real (AD004, 19/jul): o portão trocou "bolsa"→"DOBRADO" pra matar colisão, e "orçamento dobrado" lia como "em dobro"; ninguém re-rodou a leitura fria até o Sávio perguntar. Fix: "IMPRESSO".*
- [ ] **Refutador morto não absolve:** se um verificador do portão falhar (limite de sessão, erro), o achado fica SEM VEREDITO e bloqueia — silêncio nunca é aprovação. *Caso real 14/jul: 6 refutadores morreram no limite e o script contou "zero confirmados" como aprovada; a legenda tinha 3 bloqueios reais.*
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
| 20 | **Paráfrase por cima de verbatim disponível** (AD001 15/jul) | Punch = marcador de voz dela quando ele já é a tese (Passe A) |
| 21 | **Rabo sem âncora emendado em verbatim** (AD001 15/jul) | Verbatim fecha a frase; extensão só com âncora própria (Passe B) |
| 22 | **Selo simétrico ×3 nos fechos da lista** (AD001 15/jul) | Máx 1 kicker por lista; fechos variam (Passe C) |
| 23 | **Diffs do portão aplicados em sequência cega** (15/jul) | Reconciliar por prioridade + re-grep pós-diff (§7) |
| 24 | **Candidato MORTO ressuscitado noutra superfície** (29/jul): matei "NINGUÉM FOI GROSSA. SÓ NINGUÉM FOI GENTE." no registro do punch S2 e ele voltou na LEGENDA como "…só ninguém foi humana" — trocar sinônimo não cura o motivo da morte | O registro de candidatos vale pro POST INTEIRO, não pro slot: antes de fechar a legenda, reler os mortos de TODOS os slots e grepar as construções mortas em slides+legenda. Motivo da morte é da FAMÍLIA, não da palavra |
| 25 | **Valência invertida entre posts consecutivos** (29/jul): "duas linhas" era a SOLUÇÃO ensinada ontem (AD003 "A RESPOSTA DE DUAS LINHAS") e virou a VILÃ hoje ("Recebeu duas linhas de regulamento") — quem salvou o script de ontem reencontra a própria receita como crime | Pior que eco: **contradição**. No mapa de território, marcar o que os posts recentes PRESCREVERAM (não só o que disseram) e checar se o post novo condena algum. Se condenar, nomear a diferença explicitamente ou trocar as palavras |
| 26 | **Fôrma de punch repetida (as palavras mudam, o molde não)** (29/jul): "O SCRIPT DO BALCÃO, EM 3 TROCAS" × "O SCRIPT DA PRIMEIRA MENSAGEM, EM 3 TEMPOS" (6d) — e "AGENDA NÃO NASCE DE X. NASCE DE Y" × "A VENDA NÃO MORRE NO X. MORRE NO Y" (1d) | Comparar ESQUELETOS, não strings: reduzir cada punch ao molde ("O [rótulo] D[X], EM N [Y]" / "NÃO [verbo] EM A. [verbo] EM B") e checar contra os punches do `territorio-vivo.json`. Molde repetido ≤1 em 21 dias |
| 27 | **Drible por sinônimo de string proibida** (29/jul): "devolve a pergunta" estava proibida e escrevi "devolve o foco pra ela" — mesma jogada, uma palavra trocada | Proibição é do MOVIMENTO, não da string. Ao contornar uma proibida, perguntar "estou mudando a jogada ou só a fantasia dela?"; se for fantasia, o achado continua vivo |
| 29 | **Render fantasma v2: pipe que engole o erro** (24/ago — o `cd` de outro passo mudou o cwd, o python morreu e `grep -c` imprimiu "0 avisos") | Protocolo de render verificado (§5): `cd` no MESMO comando + linhas `ok slide_N` visíveis + mtime + Read do slide alterado. Nunca filtrar render com contagem |
| 30 | **"Feito" sem olhar o pixel** (24/ago — dois avisos de "pronto" com PNG velho; a confiança veio do JSON, não da imagem) | Nenhum "feito" de mudança visual sem Read do PNG renderizado DEPOIS da mudança. O que o usuário vê é o arquivo, não a intenção |
| 28 | **ELIPSE SEM VERBO NA CAPA** (29/jul, o pior da semana): "«Isso é só na avaliação.» «Agenda pelo link.» E A LEAD, NUNCA MAIS." — nunca mais O QUÊ? A frase não fecha, e está na superfície lida em 2s sem contexto. Passou por 59 agentes do portão | Leitura fria da capa LINHA POR LINHA (§3C) + dimensão SENTIDO no portão (C5), rodando ANTES de território/eco. Elipse ("nunca mais", "e pronto", "e já era") = reprova automática na capa |
