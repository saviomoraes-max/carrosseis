# Script 715 — estado do projeto

Ponto de retomada técnica. Quem pegar isto sem contexto nenhum consegue continuar.
Atualizado em 10/set/2026, depois da AUDITORIA DE ENTREGA (nove lentes, 22 achados corrigidos).

Para decisão (o que dá pra vender, o que falta, o que depende do Sávio), ler o
`relatorio-de-entrega.md` ao lado.

---

## O que é

Ebook pago, vendido pela página da VSL, sobre o **Script 715**: sete passos de
atendimento no WhatsApp de clínica de harmonização facial, do primeiro "oi" ao
comprovante do PIX. Narrado em primeira pessoa pela **Ana Luiza**, fundadora.
Leitora-alvo: doutora que comprou pela VSL.

**Andamento: 99%** (medido, não estimado: `andamento.py`).

| Frente | Peso | Feito |
| --- | --- | --- |
| Fontes, voz e transcrições | 10% | 90% |
| Escrita dos blocos | 20% | 100% |
| Revisão adversarial | 35% | 100% |
| Design e diagramação | 20% | 100% |
| Fecho e entrega | 15% | 100% |

Os 10% que faltam em "Fontes" são as **amostras escritas da Ana**, e só ela pode dar.
Todo o resto está fechado.

O que segurava "Revisão adversarial" era o degrau do leitor cego, e ele caiu inteiro:
**os 15 blocos leem "pessoa"**, contra 4 na manhã de 09/set. Ver a descoberta 6.

A tabela abaixo sai de `andamento.py --detalhe`, que é a fonte de verdade: ele escolhe o
cego mais RECENTE por data de gravação. Ler os `rodada-N.json` na mão erra, porque em
vários blocos a medição mais nova está num arquivo avulso de cego, não na rodada numerada.

---

## Onde estão as coisas

```
ebooks/715/
  manuscrito/*.md          15 blocos: 01-12, A (cola), B (banco), C (paciente modelo)
  fontes/
    01-framework-715.md    02-manual-objecoes.md    03-manual-perguntas.md   (PDFs extraídos)
    voz/fingerprint-ana.md          régua de voz VIGENTE (é a v3)
    voz/fingerprint-ana-v2-arquivado.md   a v2, que estava ERRADA (ver abaixo)
    voz/corpus/ana-luiza-falas-treinamentos.txt   80.938 palavras dela
    transcricao/*.txt      3 aulas do WAID transcritas com WhisperX
  revisao/NN/              por bloco: capitulo-vK.md, detector-vK.json, rodada-K.json/txt
  revisao/_pre-*/          snapshots antes de cada passada grande
  render/script-715.pdf    150 páginas, 9:16, 123 links internos + 22 marcadores
  render/provas/*.png      uma PNG por página
  render/cola/*.png        a cola dos 7 passos como peça de celular (cola_png.py)
  render/preview.html      abrir no browser pra folhear
  render/indice-paginas.json  em que página começa cada bloco
  render/livro-continuo.md    o livro inteiro num arquivo só, na ordem, pra BANCA ler
  revisao/bancas-10set.md     rastro comparado das SETE bancas + a 8ª abortada
  revisao/banca{,2,3,4,5,6,7}-10set.json  os pareceres crus (6ª e 7ª também em banca{6,7}-parecer.md)
  revisao/banca8-ABORTADA-10set.json     a 8ª morreu no limite semanal; NÃO tem cético, não aplicar
  aplicar-correcao-metodologia.py        as 2 correções que dependem de decisão do Sávio, prontas
  PARA-O-REVISOR.md                      o briefing que vai junto pro revisor humano
  entrega/                               o pacote pronto: PDF, briefing, texto corrido e a cola em PNG
  revisao/auditoria-entrega-parecer.md   o parecer das nove lentes que olharam a entrega
```

Scripts em `~/.claude/skills/ebook-humano-reconecta/scripts/`, com espelho
versionado em `~/reconecta/skills/ebook-humano-reconecta/` (a skill viva é a de
`~/.claude`; ver `ESPELHO.md` pra ressincronizar):
`render_pdf.py`, `linkar_pdf.py`, `detector_ptbr.py`, `andamento.py`, `graficos.py`, `cola_png.py`,
`revisor_pontuacao.py`, `livro_continuo.py`, `wf_revisao_capitulo.js`, `wf_corpus_fala.js`,
`wf_cego.js`, `wf_banca.js`, `coleta_slack_autor.py`.

**O detector agora exige `--corpus`.** Sem ele acusa como vocabulário de IA palavras
que são da autora. Ver a descoberta 7.

Réguas em `referencias/`: `padrao-de-refinamento.md` (a mais importante),
`ortotipografia-ptbr.md`, `catalogo-tells-ptbr.md`.

**Quarta fonte, autorizada pelo Sávio em 10/set: `~/llm-wiki-time`.** É o vault da casa, e
foi de lá que saíram os três buracos de conteúdo que as fontes originais não tinham. O que
vale ler primeiro:
`02-wiki/decisoes/2026-07-28-resolucao-das-divergencias-da-redacao-9-decisoes-canonicas-da-metodologia.md`
(as nove decisões canônicas do Leo, e o aviso de que 9 fichas do vault estão erradas até
serem corrigidas), `02-wiki/referencias/reconecta-metodologia-tema-t4-atendimento-fabrica-contatos.md`
e `.../reconecta-metodologia-tema-t0-transversal.md`.

---

## Estado bloco a bloco

| Bloco | Detector | Cego | Degraus |
| --- | --- | --- | --- |
| 01 | 0 | pessoa 68 | 3/3 |
| 02 | 20 | pessoa 72 | 3/3 |
| 03 | 12 | pessoa 80 | 3/3 |
| 04 | 0 | pessoa 81 | 3/3 |
| 05 | 13 | pessoa 70 | 3/3 |
| 06 | 14 | pessoa 73 | 3/3 |
| 07 | 0 | pessoa 66 | 3/3 |
| 08 | 0 | pessoa 69 | 3/3 |
| 09 | 13 | pessoa 67 | 3/3 |
| 10 | 9 | pessoa 77 | 3/3 |
| 11 | 14 | pessoa 78 | 3/3 |
| 12 | 12 | pessoa 71 | 3/3 |
| A | 28* | pessoa 73 | 2/2 |
| B | 33* | pessoa 84 | 2/2 |
| C | 17 | pessoa 73 | 3/3 |

Detector medido **com `--corpus`**, que é a régua do portão desde 09/set. Cego: três
leitores independentes por bloco, decisão por maioria.

`*` = amostra pequena (menos de 300 palavras de prosa), fora do portão.

**Todos os blocos avaliáveis passam no portão do detector.** A e B ficam fora dele por
amostra pequena (264 e 119 palavras de prosa), e o único achado de cada um é o formato da
peça: tríade na cola, lista no banco de perguntas.

**O 11 saiu de 40 pra 22 sem trocar uma palavra**, convertendo o andaime de catálogo em
bloco `:::caso`. A conversão foi provada neutra por contagem: 0 palavra perdida, 0 inventada.

**Diagramação:** 150 páginas em 4 partes, com contracapa. **34 gráficos vetoriais em 15 tipos**, e todo bloco tem pelo menos um, **zero páginas órfãs** (o render audita isso sozinho e denuncia página de miolo abaixo de 35% de ocupação). Dois bugs do paginador
corrigidos em 09/set: lista numerada era bloco indivisível (agora quebra entre
páginas, com `start=` continuando a numeração) e o balanceamento da última página
do capítulo media `scrollHeight`, que nunca fica menor que a caixa porque
`.conteudo` tem altura fixa com `overflow:hidden` (agora mede o último filho).

**Ortotipografia:** 205 pares de aspas curvas fechando, zero aspa reta no corpo,
zero travessão, aspas simples só dentro de duplas.

---

## As treze descobertas que mudaram o projeto

Cada uma tem arquivo próprio. Ler antes de mexer em qualquer coisa.

1. **`paridade-de-juri.md`** — ao trocar de modelo no meio do livro, o júri novo
   achou no capítulo 1 (que o Sávio tinha aprovado) uma definição inventada que
   passou por quatro rodadas do júri anterior. A Ana só PERGUNTA "salinha do
   fechamento ou do pagamento", nunca define, e o capítulo tinha trocado a
   palavra dela invertendo a concessão.

2. **`auditoria-invencao.txt`** — varredura dos 15 blocos: 98 acusações, 28
   confirmadas. O padrão dominante não foi caso inventado, foi quantificador sem
   fonte ("a maioria das clínicas", "já na segunda mensagem", "o mais pulado").

3. **`experimento-desalinho.md`** — o leitor cego foi **rebaixado de portão a
   termômetro**, porque penalizou uma citação literal da Ana como se fosse
   moderação de máquina. Três tentativas de vencê-lo por edição, duas pioraram.

4. **O fingerprint v2 estava errado e contaminou tudo.** Feito com 1.816
   palavras de story, ele elegeu como assinatura dela contraste "não X, é Y",
   anáfora em escada, espelhamento e "frase longa seguida de pancada curta". As
   80.938 palavras desmentiram os quatro (espelhamento: **zero** ocorrências).
   E os revisores passaram semanas empurrando essas construções para dentro do
   texto, que é exatamente o que o leitor cego marca como máquina.

5. **Não é a dose, é a distribuição.** As 111 edições de recalibração acertaram
   todos os números e o cego PIOROU, porque distribuí os marcadores orais
   uniformemente. Fala real vem em rajada (CV dos intervalos 1,175 contra 0,996
   do livro). Alvo estatístico se aplica com a variância junto.

---

6. **A substituição por fala real virou o leitor cego, e isso resolve o maior
   problema aberto do livro.** A descoberta 5 previu que só a substituição moveria
   o cego, e não a edição. Testado em 09/set nos blocos 03, 04, 05 e 11: três
   leitores independentes por bloco, **doze leitores, zero voto "ia"**. O 03 saiu
   de "ia 65" pra "pessoa 78". O método está em `padrao-de-refinamento.md` 3h, e o
   registro em `revisao/cego-pos-corpus-09set.json`.

   O que os leitores citam como prova de humanidade é o que um revisor cortaria:
   autocorreção que sobreviveu, "pô", "descontinho", concordância travada, e a
   MESMA interjeição grafada de dois jeitos no mesmo capítulo. **Não arrumar isso.**

7. **O detector também punia a voz da autora.** Depois da troca, o capítulo 11
   SUBIU de 35 pra 40, com achado de gravidade alta em `"gerar valor"` — expressão
   que aparece quatro vezes na fala dela. Terceira vez que um instrumento deste
   pipeline penaliza o acerto. `detector_ptbr.py --corpus <arquivo>` agora absolve
   achado LEXICAL cujo termo apareça 2+ vezes no corpus da autora. Achado de
   ESTRUTURA (anáfora, dois-pontos, contraste) não se absolve: composição é de quem
   escreveu, não de quem falou.

8. **A banca de leitura: sete passadas, e o capítulo que saía incompleto.** Tudo no
   projeto lia UM BLOCO POR VEZ, e por isso era cego pra promessa quebrada, remissão
   errada, repetição entre capítulos e cansaço da leitora. A banca põe seis examinadores
   lendo o livro INTEIRO de ponta a ponta (`livro_continuo.py` monta o objeto que a
   leitora recebe), um cético por examinador e um relator. Rastro comparado em
   `revisao/bancas-10set.md`.

   | Banca | Brutos | Confirm. | Média |
   | --- | --- | --- | --- |
   | 1ª | 57 | 13 | 7,5 |
   | 2ª | 53 | 6 | 7,7 |
   | 3ª | 53 | 9 | 7,8 |
   | 4ª | 59 | 5 | 7,7 |
   | 5ª | 48 | 3 | 8,1 |
   | 6ª | 51 | 4 | 8,2 |
   | 7ª | 46 | 3 | **8,2** |

   O achado nº 1 da primeira não era de escrita: o capítulo 05 chegava **incompleto no PDF
   pago**. Uma cerca `:::` com texto colado fazia o parser engolir, calado, um parágrafo e
   o bloco "o que evitar". Nenhum instrumento pegava porque **todos liam a fonte e ninguém
   olhava o render**. Hoje o build morre em cerca malformada e confere bloco a bloco fonte
   contra saída.

   **A banca é boa em pegar o que EU escrevo.** Na 3ª, quatro lentes independentes
   apontaram o mesmo trecho que eu tinha escrito uma hora antes. Na 4ª, ela achou que o
   meu texto novo se contradizia em dois pontos.

   Na **6ª**, a primeira com **zero achado de gravidade alta**, o que moveu o ponteiro
   não foi a banca em si: foi ler o parecer da 5ª procurando o que o cético NÃO tinha
   confirmado. O relator escreve uma lista maior que a dos confirmados, e boa parte dela
   é contagem, não opinião — dá pra provar com grep. Oito eram defeito de verdade, seis
   eu descartei com motivo escrito. O mais caro: no anexo C, três números diferentes
   (valor do protocolo, valor de modelo, valor da reserva) usavam o mesmo `[valor]` numa
   frase que a doutora preenche e **envia**. O erro saía da clínica dela, não do livro.

   Descoberta de método junto: as duas fontes da metodologia **discordam entre si** na
   redação de quatro frases prontas. O livro carregava as duas porque era fiel às duas, e
   agora reflete cada uma na casa dela: capítulos e cola seguem o framework, anexo B segue
   o manual de perguntas.

9. **Cético de um bloco não vê os outros.** Numa rodada de seis blocos em paralelo,
   três achados confirmados colidiram: garimpeiros diferentes acharam a MESMA
   passagem do corpus e a puseram em capítulos diferentes. O livro ficou com a mesma
   anedota da Ana em dois capítulos seguidos. Toda rodada multi-bloco agora termina
   com varredura de colisão antes de aplicar.

10. **Detector 0 e leitor cego 3 a 0 pra "IA", no mesmo capítulo.** As duas medições
    estavam certas: o detector vê PALAVRA, o cego ouve RITMO. O capítulo 07, o mais curto
    e o único de prosa 100% composta, era sustentado por uma metáfora que **eu inventei**
    — "a ponte" —, plantada, retomada e paga em três dobras estruturais. A conferência é de
    uma linha: `grep -c ponte corpus/` deu **0 em 80.938 palavras**, e 0 nas fontes. O
    conserto não foi cortar, foi substituir por fala real dela ("a parte em que a gente
    oferece pra ela o problema resolvido") e enxertar uma doutrina que faltava ("a pessoa
    não pode sair da transição com medo"). Voltou pra **2 a 1 pessoa**, e as duas provas
    de que era gente que os leitores citaram foram justamente as frases dela que entraram.
    Régua gravada como 3l no padrão. **Corolário: bloco de prosa composta, sem cena e sem
    caso, precisa de cego mesmo com o detector zerado.**

11. **A banca pode morrer no meio, e banca sem cético não é banca.** A 8ª passada abortou no
    limite semanal da conta: três lentes de seis terminaram e NENHUM cético rodou. Os 34
    achados voltaram todos com `sem veredito do cetico (falha)`. Isso não quer dizer que sejam
    bons, quer dizer que ninguém conferiu — e o `wf_banca.js` já entrega o campo `real=false`
    com esse motivo justamente pra não confundir as duas coisas. **Nada foi aplicado.** As
    notas parciais também não são comparáveis com as das outras passadas, porque faltam três
    lentes. Ficou gravada como `banca8-ABORTADA-10set.json`, só como pista.

    Corolário operacional: antes de rodar banca, olhe se dá pra pagar por ela. Uma banca são
    13 agentes e ~1,5M de tokens de subagente.

12. **Cinco lentes olharam as 150 páginas RENDERIZADAS, e nenhum instrumento tinha feito isso.**
    Todo o pipeline lia texto: o detector lê markdown, o linter lê markdown, o cego lê markdown,
    a banca lê o livro-contínuo. **Ninguém abria a prova.** A auditoria de entrega pôs cinco
    revisores de prova gráfica lendo os PNGs um a um, mais uma lente preenchendo a camada
    colável e mandando na cabeça, mais fidelidade às fontes, estrutura e completude. Nove
    lentes, cético por lente: **22 achados confirmados, 4 altos**, todos corrigidos.

    O que só a prova pega: `R$` separado do valor na quebra de linha, dentro da frase que a
    leitora copia. Bloco gráfico partindo e deixando o quarto item sozinho no topo da página
    seguinte. Deixa terminando em dois-pontos no pé de uma página com o card que ela anuncia
    abrindo a próxima. Título de abertura deixando uma palavra sozinha na segunda linha.
    Coluna de gráfico desalinhada porque o título quebrou em duas linhas. Fio de conector
    parando 4px antes da caixa, que era o SVG inline sentando na linha de base do texto.

    O que só a camada colável PREENCHIDA pega: `sobre o [procedimento/consulta]` vira "sobre o
    consulta". `me chame no [dia]` morre em cinco dos sete dias da semana, que são femininos.
    Cartão com duas mensagens de entrada e uma resposta só que serve pra uma delas. Cartão que
    pergunta o dia e na frase seguinte já usa o dia.

    **Régua: antes de entregar, alguém tem que OLHAR a prova e alguém tem que PREENCHER as
    frases.** Ler o markdown não é ler o livro.

13. **Os links existiam e podiam não funcionar.** O Chromium escreve todo link interno como
    DESTINO NOMEADO, que vários leitores de celular ignoram em silêncio: o clique não faz
    nada e nada acusa. Eu tinha conferido destino a destino, e o que conferi foi que o
    arquivo estava certo, não que a leitora conseguiria usar. `linkar_pdf.py` troca por
    destino explícito, cria os marcadores do PDF e morre se algum link ficar sem alvo.

    Na mesma passada entrou o que ninguém tinha tornado clicável: a lista das páginas de
    parte e **os sete círculos do trilho** (passo N leva ao capítulo N+2). Como o trilho é
    SVG e o Chromium só faz link de `<a>` de HTML, a solução é âncora transparente por cima,
    conferida medindo o `/Rect` contra o centro do círculo. **De 40 pra 123 links internos.**

    Junto: **o PDF não embute a TT Modernoir, e é melhor assim.** O Chromium não embute
    fonte que não permite, então desenha cada glifo como vetor (Type3). A tipografia sai
    certa, ninguém redistribui arquivo licenciado e o texto continua pesquisável. Era assim
    desde ontem; o que estava errado era a frase no relatório, que dizia o contrário e foi
    corrigida.

## Decisões já tomadas (não reabrir)

- Título: "7 passos para 1 **agendamento** a cada 5 contatos" (era "consulta").
- Leitor cego é **termômetro**, não portão. Fidelidade sempre vence.
- Exercício das "20 conversas" foi **removido**: era invenção minha.
- Link do CTA no cap. 12: `https://supercaso.com.br/consulta?utm_source=ebook&utm_medium=material-rico&utm_campaign=FRAMEWORK-715&utm_content=cta-final`
- Aspas tipográficas `“ ”` no corpo, retas no front matter YAML, zero travessão.
- Só vetor e texto no PDF, sem foto de fundo. Formato 9:16.
- Vídeo das aulas do WAID: só a 5.1 entrou (virou o Anexo C). As outras duas são
  de captação com ManyChat, fora do escopo.
- Capítulo 11 é catálogo em `:::caso` (slots ela/perde/responde), não prosa com
  andaime. A conversão foi provada neutra: 0 palavra perdida, 0 inventada.
- Livro dividido em 4 partes com página-marcador. Os rótulos são navegação, não
  doutrina.
- A cola sai como peça própria (`cola_png.py`), não como recorte de página do PDF.
- **Muleta oral no MEIO da frase não entra** (decisão do Sávio, 10/set: "é um ebook, não
  é pra colocar todos os vícios de linguagem dela"). Foram 38 cortes: 22 do meio e 16 de
  `, né.` fechando com ponto. **Ficam** as 28 que fecham pergunta com `?` e os vocativos.
  A régua está em `padrao-de-refinamento.md` 3k, e ela LIMITA a 3h: fala real é insumo,
  não acabamento. **Não reabrir** achando que é oralidade a preservar.
- **Quem digita fala da doutora em terceira pessoa, e isso é proposital** (decisão do
  Sávio, 10/set). As 29 frases prontas seguem o framework. Existe no `llm-wiki-time` a
  decisão canônica **D-C de 28/jul** dizendo o oposto ("a secretária SE PASSA pela
  doutora... naquela conversa ela é a doutora"), que revoga a ficha T8.23 e parte do
  fluxo de handoff. **Não reabrir:** o livro segue o framework, e o capítulo 02 declara
  uma vez quem é "você".
- **Sem assinatura de autora.** Capa e rodapé levam só Reconecta (decisão do Sávio em
  10/set). A narração em primeira pessoa continua sendo a da Ana; o que saiu foi a
  assinatura, não a voz. `livro.json` sem a chave `autor` já omite o bloco na capa.

---

## O que falta

**Nada bloqueia o lançamento.** Andamento 99%: escrita, revisão, design e fecho em 100%.
Os 10% que faltam em "Fontes" são as amostras escritas da Ana, e deixaram de importar
quando a substituição por fala real resolveu o cego em 15 dos 15 blocos.

**Fechado em 10/set, não reabrir:**
- ~~Licença da fonte.~~ A TT Modernoir licenciada vem do Adobe Fonts ativado na máquina.
  Os 11 arquivos de trial foram **apagados** de três pastas, e os três pipelines que
  apontavam pra eles (cola, engine dos carrosséis, motion) passaram a resolver a família
  pelo sistema. A pasta `Reconecta Design System/fonts/` ficou **vazia**.
- ~~Os três buracos de conteúdo.~~ Preenchidos com doutrina canônica do `llm-wiki-time`.
- ~~Quem digita no WhatsApp.~~ O livro segue o framework, terceira pessoa. Ver as decisões.
- ~~Os dois pontos de cansaço.~~ Cortados.
- ~~As duas correções em card de script.~~ Já estavam aplicadas; o item era resíduo.
- ~~Links internos no PDF (item F).~~ Já estavam no `inline()`, **mas ninguém tinha
  verificado que sobrevivem à impressão.** O Chromium podia ter descartado a âncora e o
  sumário viraria retângulo morto. Conferidos destino a destino contra o
  `indice-paginas.json`: **35 links internos, todos na abertura certa**, mais os 2
  externos do CTA. O regex do render cobria só anexo A e B; foi pra A-D.
- ~~A faxina do parecer da 5ª banca.~~ Oito defeitos aplicados, seis descartados com
  motivo. Detalhe item a item em `ideias-de-leitura.md`.
- ~~O capítulo 07 lendo "IA" por 3 a 0.~~ Metáfora inventada fora, fala real dentro. Ver a
  descoberta 10. **Ele oscilou três vezes no mesmo dia** (3×0 ia → 2×1 pessoa → 2×1 ia → 2×1
  pessoa) e cada volta foi por um tell diferente que EU tinha escrito: primeiro a metáfora
  "ponte", depois um decalque de tradução ("e é isso que a transição é"), depois a
  contabilidade da própria lista ("três desses quatro... o quarto"), depois a cadência de
  três fragmentos abrindo três seções e uma antítese espelhada. É o bloco mais composto do
  livro, o mais curto e o que menos carrega fala transcrita. **Trate ele como o canário:
  qualquer passada nova mede o 07 primeiro.**
- ~~Os quatro pedidos de acabamento da leitora.~~ Três feitos (a objeção do PIX à noite virou
  família no cap 11, o cartão do orçamento ganhou a frase montada, os gráficos pararam de
  ecoar o parágrafo). O quarto, os doze fins de capítulo, é escopo e está registrado abaixo.
- ~~O gráfico `leituras` descartando linha em silêncio.~~ Achado pelo leitor cego, não pela
  banca. Consertado no `graficos.py`.

**O achado que QUATRO bancas seguidas apontaram e que NÃO foi corrigido**, por decisão do
Sávio de que metodologia é proposital: a frase da apresentação, `"vai te ajudar com o
[problema] e parar de se sentir"`, que lida ao pé da letra põe a doutora como quem para de
se sentir mal. Idem `"desde [tempo]"` na transição. As duas são literais do framework.

**As duas correções estão prontas e não foram aplicadas:** `aplicar-correcao-metodologia.py`,
na raiz do projeto. Ele confere antes de escrever (`--conferir`), morre se o manuscrito tiver
mudado, e mexe em CONECTIVO, não em conteúdo: `e parar` → `pra você parar` em 4 lugares, e
`desde [tempo]` → `há [tempo]` em 4. **Só roda com a palavra do Sávio.**

A 6ª e a 7ª bancas trouxeram um argumento mais afiado no `desde [tempo]`, e ele merece uma
segunda olhada do Sávio **porque mudou de natureza**: não é a leitura do livro que quebra, é a
mensagem que sai. A leitora preenche com o que o próprio livro manda ("tem uns dois anos
que eu reparo") e envia *"desde dois anos"*. O anexo B, que segue o manual, já traz
`há [tempo informado]`. Quatro ocorrências. Continua sendo decisão do dono, e não foi
mexido.

**Escopo, não revisão (a banca diz isso com todas as letras):** os doze fins de capítulo
perguntam o que ela errou e não dão tarefa pra amanhã. Mexer significa reeditar os doze fechos
de um livro pronto, então não fiz por conta própria. Vale registrar que a instrução prática
existe, só não está no fecho: nos sete capítulos de passo ela vem em "Quando avançar", logo
acima da pergunta, e no livro inteiro vem no anexo A e no cap 12.

**Melhoria opcional, não pendência:** `ideias-de-leitura.md` tem o anexo B indexado "pelo
que ela disse", carimbos tipográficos e um glossário. **Medido em 10/set: o glossário fecha
um buraco menor do que parecia** — cada termo da casa já nasce definido na primeira
aparição (bastão no cap 02, presente inaceitável é o título do 05, cortina de fumaça abre o
10). Se for feito, toda entrada tem que ser frase LITERAL do livro com o capítulo de
origem: definição inventada já passou por quatro rodadas aqui uma vez.

## Como retomar

```bash
P=~/reconecta/ebooks/715
S=~/.claude/skills/ebook-humano-reconecta/scripts
C=$P/fontes/voz/corpus/ana-luiza-falas-treinamentos.txt

python3 $S/andamento.py $P --detalhe                     # onde estamos
python3 $S/revisor_pontuacao.py $P                       # pontuação e eco
python3 $S/detector_ptbr.py $P/revisao/11/capitulo-limpo.md --corpus $C   # um bloco
python3 $S/render_pdf.py $P --provas                     # PDF + PNGs + cola + preview
python3 $S/livro_continuo.py $P                          # monta o insumo da banca
```

O `--corpus` **não é opcional**: sem ele o detector acusa como vocabulário de IA palavras
que são da autora. E o `render_pdf` agora morre em QUATRO situações, de propósito: cerca
`:::` malformada, bloco perdido entre a fonte e o render, família TT Modernoir não resolvida,
e link interno apontando pra destino que não existe. Nenhuma delas deve ser contornada.

O `linkar_pdf.py` roda sozinho no fim do render: troca destino nomeado por explícito e cria
os marcadores do PDF. Ver a descoberta 13.

Pra rodar a banca (13 agentes, ~17 min), depois de `livro_continuo.py`:
`wf_banca.js` com `{livro, ortotipografia, fingerprint}`.

Pro leitor cego, **regere antes o `capitulo-limpo.md`** (é o manuscrito sem o front matter,
e é o que o `wf_cego.js` lê; se você editar o manuscrito e não regerar, o cego mede a
versão velha e você conclui errado). Depois de rodar, **grave o veredito** num
`revisao/<bloco>/rodada-cego-*.json` com a chave `cego`, senão o `andamento.py` continua
reportando a medição anterior.

**Não confie no detector zerado.** Ele mede palavra; o cego ouve ritmo. O bloco 07 tinha
score 0 e os três leitores diziam "IA". Bloco de prosa composta, sem cena e sem caso, pede
cego mesmo com o detector limpo. Ver a descoberta 10 e a régua 3l.

Regra que vale mais que todas: **achado só vira correção com veredito de
cético**. Achado marcado `"sem veredito do cetico (falha)"` significa que o
agente morreu, não que a acusação seja boa. Nunca aplicar.
