# Padrão de refinamento (independente de modelo)

O padrão de qualidade deste pipeline não pode morar no julgamento de quem está
escrevendo. Ele mora aqui, em regras que rodam igual em qualquer sessão e em
qualquer modelo. Quando a sessão troca de modelo (Fable, Opus, Sonnet), o júri
muda; estas regras não.

## 1. Portões (numéricos, medidos por script)

Um capítulo só é dado por fechado quando os quatro passam:

| Portão | Valor | Onde se mede |
| --- | --- | --- |
| Detector PT-BR | ≤ 25 | `scripts/detector_ptbr.py --corpus <fala da autora>` sobre `capitulo-limpo.md` |
| Achados de gravidade alta confirmados | 0 na última rodada | `rodada-N.json`, campo `altas_confirmadas` |
| Leitor cego | **termômetro, não portão** (ver 3c) | `rodada-N.json`, campo `cego` |
| Travessão | 0 | `grep -c "—"` no manuscrito |
| Fonte x render | nenhum bloco perdido | `render_pdf.py` conta e para o build (ver 3j) |
| Banca de leitura | 0 achados altos confirmados | `wf_banca.js` sobre `livro_continuo.py` (ver 3i) |

A banca é portão de LIVRO, não de capítulo: roda uma vez quando os blocos estão fechados, e de
novo depois de qualquer rodada que mexa em mais de um bloco. É a única lente que enxerga o que
existe entre capítulos.

O leitor cego saiu da lista de portões em 08/set, depois de um experimento
controlado (`experimento-desalinho.md` no projeto do livro): ele penalizou uma
citação literal da autora como se fosse moderação de máquina. Ele continua sendo
medido e reportado, com três leitores e decisão por maioria, mas não manda no
texto e nunca vence a fidelidade.

Exceção registrada: em capítulo prescritivo (os sete passos), o cego costuma
ficar entre 60 e 78 mesmo depois de limpo. A causa está diagnosticada: costura
entre transcrição literal e prosa composta, sem amostra ESCRITA da autora. Nesse
caso o portão do cego relaxa para "confiança ≥ 70 + leitura humana", e isso vai
declarado no relatório, nunca escondido.

O `--corpus` não é opcional quando existe corpus da autora: sem ele o detector acusa como
vocabulário de IA palavras que são dela (ver 3f). O portão vale sobre a leitura COM corpus.

O `capitulo-limpo.md` é o capítulo como a leitora vê, só sem front matter. Quem
separa prosa de não-prosa é o próprio detector: desde 08/set ele apaga, sem mexer
nos índices, os blocos `:::frase`, `:::cena`, `:::evite` e `:::grafico`, que são
texto literal das fontes ou conteúdo de quadro. `:::punch` e `:::pergunta` ficam,
porque são frases do autor.

Isso corrigiu um viés grave do instrumento: ele penalizava o acerto. Quando eu
consertei a fidelidade de uma cena (pondo o slot `[Nome]` igual ao card), o score
SUBIU oito pontos. Uma régua que sobe quando o texto melhora empurra o trabalho
na direção errada, então ela some do caminho crítico e vira ruído. Apagar em
vez de recortar é o que preserva as densidades: recortar o bloco muda os
denominadores e mede outra coisa.

Segunda correção do instrumento (08/set): bloco com menos de 300 palavras de
prosa sai marcado como `amostra_pequena` e **não vale como portão**. Um anexo de
cards tem cinco parágrafos de prosa, e métrica de uniformidade sobre cinco
parágrafos mede ruído: apagar quatro palavras do anexo A moveu o score de 28 pra
49. O score continua saindo pra inspeção, mas o bloco passa a valer dois degraus
em vez de três no medidor de andamento.

## 2. Regra do cético (mecânica, não editorial)

Um achado só vira correção se um cético que leu a fonte confirmou. Em concreto:

- Achado com `motivo: "sem veredito do cetico (falha)"` **nunca é aplicado**.
  Esse rótulo significa que o agente morreu (limite de sessão, erro de API), não
  que a acusação seja boa.
- Uma rodada que volta com `brutos: 0` e a lista de `failures` cheia **não é uma
  rodada limpa**. É uma rodada que não aconteceu. Registrar como pendente.
- Correção proposta pelo revisor que o cético aprovou "com ressalva" entra na
  versão da ressalva, não na original.
- Achado de fidelidade tem precedência sobre achado de voz. Inventar fato para
  consertar ritmo é pior que o tell.

## 2b. O cético de um bloco não enxerga os outros

Rodada de seis blocos em paralelo, seis garimpeiros, seis céticos, cada um lendo o seu
bloco. Três achados confirmados colidiram entre si: dois garimpeiros diferentes acharam a
MESMA passagem do corpus e a puseram em capítulos diferentes. O livro ficou com a mesma
anedota da autora ("você é linda" / "esse conforto diminui a velocidade da decisão") em
dois capítulos seguidos, e com a fórmula "se ela falar flacidez, a gente clareia flacidez"
em três lugares.

Nenhum cético podia ver isso: cada um estava certo dentro do seu bloco. Repetir a mesma
frase três vezes é assinatura de máquina tanto quanto qualquer tell de parágrafo.

**Regra: toda rodada multi-bloco termina com uma varredura de colisão**, mecânica, antes de
aplicar. Duas checagens, ambas baratas:
- o mesmo fragmento do corpus citado por achados de blocos diferentes;
- a mesma frase (acima de ~45 caracteres) em propostas de blocos diferentes.
Colidiu, escolhe UM bloco e reverte os outros. Quem fica é o capítulo que ensina; anexo de
consulta e cola ficam com a formulação curta que já tinham.

**Segunda armadilha da mesma rodada:** a proposta do cético às vezes reescreve um trecho
MAIOR que o `trecho_livro` acusado, incluindo a abertura do parágrafo. Substituição literal
então duplica essa abertura. Aconteceu em quatro dos 22 achados aplicados. Depois de
aplicar, varrer repetição imediata (`(.{40,400}?)\1`) e frase longa repetida dentro do
mesmo arquivo.

## 3. Paridade de júri

Os revisores, os céticos e o leitor cego herdam o modelo da sessão, salvo se o
argumento `juri` for passado ao workflow (`juri: "fable"` fixa a régua antiga).
Trocar o modelo da sessão troca o júri, e isso é a única variável de padrão que
os portões não capturam sozinhos.

**Teste de paridade.** Ao trocar o modelo da sessão no meio de um livro, passar
pelo júri novo um capítulo já fechado e aprovado por humano, sem alterar uma
vírgula dele. Comparar com o veredito do júri antigo no mesmo texto:

- Confirmados altos perto de zero e cego igual → as réguas concordam, seguir.
- Enxurrada de achados altos num capítulo aprovado → a régua mudou. Antes de
  aplicar qualquer coisa, decidir qual régua vale e registrar a decisão.

Guardar o resultado em `paridade-de-juri.md` no projeto do livro, com data,
modelo, capítulo usado e os dois vereditos lado a lado.

## 3b. Auditoria de invenção (varredura de livro inteiro)

Nasceu do teste de paridade de 08/set, quando uma definição inventada sobreviveu
a quatro rodadas no capítulo mais revisado do livro. Rodada de uma vez sobre
todos os blocos, com dois papéis opostos:

- **auditor por bloco**: extrai toda afirmação que funcione como fato ou regra
  (definição, doutrina, política, número, causa, caso, atribuição do tipo "pelo
  que eu observo") e procura a fonte com Grep antes de acusar;
- **advogado de defesa por bloco**: faz o contrário, tenta ACHAR a fonte de cada
  acusação, inclusive por paráfrase ou sinônimo. Só sobrevive o que ele não achar.

Primeira execução: 15 blocos, 98 acusações, **28 confirmadas** em 13 blocos. O
padrão que mais apareceu não foi caso inventado, foi **quantificador e ordinal
sem fonte** ("a maioria das clínicas", "já na segunda mensagem", "o mais pulado",
"o meu sinal preferido", "o 150 da clínica ao lado") e **termo da casa usado com
o sinal trocado** (o "bastão", que na fonte é de quem pergunta e deve ser mantido,
aparecia como coisa ruim de se ter).

## 3c. Quando o revisor e o leitor cego brigam, o cego ganha

Aprendizado de 08/set, e é o mais caro do projeto até aqui. O capítulo 1 estava
em "pessoa 60". Apliquei duas correções que o revisor de tell pediu e o cético
aprovou, ambas construídas em cima de hábitos documentados da autora: um
contraste espelhado ("tarde demais / cedo demais... Parece o contrário. É a mesma
coisa.") e uma anáfora de três negações ("Não tem porta, não tem cadeira, não tem
área de espera."). O capítulo caiu para "IA 68", e o leitor cego citou como
pistas número 1 e número 2 exatamente essas duas passagens.

A explicação: o fingerprint documenta que ela FAZ anáfora e contraste. Ela faz,
uma vez, torto, no meio de 800 palavras faladas. Prosa composta que executa o
mesmo recurso com simetria perfeita, no ponto exato onde ele rende mais, lê como
máquina justamente por estar bem executado. O revisor otimiza para o padrão; o
leitor cego mede o resultado.

Regras que saem disso:
- **O cego é a medida de resultado, o revisor é proxy.** Quando conflitam, vale
  o cego, e a correção do revisor é revertida ou torta de propósito.
- **Simetria perfeita é suspeita**, mesmo quando o recurso é dela. Tricolon com
  anáfora exata, quiasmo e par "Parece X. É Y." fechando parágrafo entram no
  máximo uma vez por capítulo, e de preferência com uma quebra no ritmo.
- **Nunca aplicar correção de estilo sem remedir o cego depois.** Correção de
  fidelidade é segura; correção de ritmo não é.
- **Um leitor cego é ruído, três são medida.** Decidir por maioria.

## 3d. O fingerprint pode estar errado, e ele contamina tudo

Aprendizado de 08/set, o mais caro do projeto. O fingerprint v2 da Ana foi feito
com 1.816 palavras de três stories. Ele elegeu como assinatura dela: contraste
"não X, é Y", anáfora em escada, espelhamento dos dois lados e "frase longa
seguida de pancada curta".

Quando apareceram 80.938 palavras dela falando sobre o assunto do livro, a
medição desmentiu os quatro:

| v2 afirmava | medido em 80.9k |
| --- | --- |
| pancada curta depois de longa é o traço principal | efeito **zero**: 27,7% contra base de 26,5% |
| contraste é assinatura, 3 de 3 | 0,10 por mil, uma a cada 1.900 palavras |
| anáfora de 3+ degraus | uma a cada 5.900 palavras |
| espelhamento dos dois lados | **zero** ocorrências |

E os revisores, obedecendo ao v2, passaram semanas **empurrando essas
construções para dentro do texto**, que é exatamente o que o leitor cego marca
como escrita de máquina. O livro chegou a ter 10x a taxa de antítese dela.

Regras que saem disso:
- **Fingerprint com menos de 10 mil palavras de corpus é hipótese, não régua.**
  Marcar cada traço com o tamanho da amostra que o sustenta.
- **Registro importa mais que autor.** As 1.816 palavras eram story; o livro é
  ensino. A mesma pessoa tem doses diferentes por registro, e a v2 media uma pra
  prescrever na outra.
- **Medir o livro contra o corpus na mesma unidade**, sempre. Unidade de fôlego
  (corte em vírgula) é imune à pontuação automática da transcrição; contagem de
  frase não é.
- **A régua de irregularidade é o coeficiente de variação.** Prosa composta fica
  regular (CV 0,65) e fala humana é irregular (CV 1,07). Perseguir esse número é
  mais útil que perseguir qualquer tell isolado.
- Antes de confiar num fingerprint, procurar mais corpus da pessoa. Neste
  projeto ele estava a uma busca de distância, no Google Drive da empresa.

## 3e. Não é a dose, é a distribuição

Terceira tentativa fracassada de vencer o leitor cego, e a que finalmente explica
as outras duas.

Depois de refazer o fingerprint com 80.938 palavras, apliquei 111 edições pra
levar o livro às doses medidas dela. Funcionou nos números: antítese caiu de 1,04
pra 0,56 por mil, coeficiente de variação subiu de 0,652 pra 0,768, blocos acima
do portão do detector caíram de seis pra dois. **E o leitor cego piorou**, de 6
blocos "pessoa" pra 4.

O motivo, na palavra dele: *"Os marcadores de oralidade estão distribuídos com
regularidade suspeita: um por parágrafo. Fala real amontoa e repete o mesmo
bordão em rajada; isso aqui é rodízio controlado de vocabulário."*

Medi a queixa. Coeficiente de variação dos intervalos entre marcadores orais:

| | Valor |
| --- | --- |
| Fala dela | 1,175 (vem em rajada) |
| Livro | 0,996 (espalhado) |

Ou seja: acertei a dose e errei a distribuição. E é a terceira vez que o mesmo
erro acontece com nome diferente. Aplicar um alvo medido de maneira uniforme
**cria** assinatura de máquina, porque uniformidade é justamente o que o
detector procura. Foi assim com o contraste do v2, com a pancada curta e agora
com o "né".

**Regra:** alvo estatístico se aplica com a variância dele junto. Se a métrica
diz "5 a 7 por capítulo", isso não quer dizer um a cada quatrocentas palavras.
Quer dizer três seguidos num parágrafo e nenhum nos dois seguintes. Quando não
der pra reproduzir a variância, **não perseguir o alvo**: um número certo mal
distribuído é pior que o número errado.

**Consequência prática:** parei de editar o livro para agradar o leitor cego.
Três tentativas, duas pioraram. Ele fica como termômetro reportado. O que ainda
pode mover é substituir prosa composta por fala real dela, que o corpus de 80 mil
palavras agora permite, e isso é reescrita, não edição.

**Em 09/set isso foi testado e a previsão estava certa. Ver 3h.**

## 3f. O detector também pode punir a voz da autora

Terceira vez que um instrumento deste pipeline penaliza o acerto, e a mais direta.
Depois de trocar prosa composta por fala literal da autora, o capítulo 11 SUBIU de 35
para 40. O achado de gravidade alta era `vocabulario_n1: "gerar valor"`, numa frase que
sai inteira do corpus dela e onde a expressão aparece quatro vezes.

O padrão é sempre o mesmo: a régua foi calibrada contra escrita de máquina em geral, e a
autora real usa parte desse vocabulário. Quando isso acontece, quem cede é a régua.

**Regra: acusação sobre a PALAVRA se cala diante do corpus.** `detector_ptbr.py --corpus
<arquivo>` tira do score todo achado de categoria lexical (`vocabulario_n1/n2/n3`,
`transicao`, `hedge`) cujo termo apareça duas ou mais vezes na fala medida da autora. Duas,
não uma, porque transcrição automática inventa palavra. Os absolvidos continuam saindo em
`absolvidos_pelo_corpus`, pra inspeção.

**O que NÃO se absolve:** achado de ESTRUTURA. Anáfora, dois-pontos em cadência, contraste
fácil, tríade, uniformidade de parágrafo. Esses são sobre composição, e a autora falando
não compõe: quem compôs foi quem escreveu. No caso do 11, a absolvição tirou 12 pontos
(40 → 28) e os achados estruturais ficaram todos de pé, que era o correto.

## 3g. Andaime de catálogo é chrome, não prosa

Capítulo de consulta (manual de objeções, banco de perguntas) tende a carregar a estrutura
em prosa: "A paciente diz X", "Se quiser perder a paciente:", "Por que não funciona:",
repetidos a cada entrada. Isso é rótulo de formulário escrito por extenso, e o detector o
lê como anáfora e cadência de dois-pontos, com razão.

A saída não é reescrever: é **promover o andaime a rótulo de bloco**. No Script 715 as 20
entradas do capítulo 11 viraram `:::caso` com três slots (`ela:`, `perde:`, `responde:`), a
explicação ficou de fora como prosa medida, e o detector caiu de 40 para 22 sem trocar uma
palavra do conteúdo.

**Regra: conversão de estrutura só entra com prova de neutralidade.** O script que converte
compara os multiconjuntos de palavras antes e depois, descontando exatamente os rótulos
removidos, e se recusa a gravar se sobrar ou faltar qualquer palavra. Sem essa prova é
reescrita disfarçada de formatação.

Cuidados que a conversão automática exige, e que só apareceram na prova visual:
- o texto depois de "Por que não funciona:" vira parágrafo e começa em minúscula;
- os parágrafos gerados precisam de linha em branco entre eles, senão o markdown funde tudo;
- capitalizar por regex pega o front matter YAML junto.

## 3h. O que finalmente moveu o leitor cego: substituição, não edição

Depois de três tentativas fracassadas de vencer o leitor cego por EDIÇÃO (3c, 3d, 3e), a
quarta funcionou, e ela não foi edição: foi trocar prosa composta por fala literal da
autora, garimpada no corpus dela.

Método, em uma rodada de seis blocos:
1. Um **garimpeiro** por bloco. Ele não corrige nada. Lê o bloco e faz dezenas de Grep no
   corpus procurando a autora dizendo aquilo. Só propõe troca quando a fala dela é MELHOR,
   mais concreta, menos simétrica. Copia o trecho do corpus literal.
2. Um **cético** por bloco, cuja primeira obrigação é fazer o grep de novo: citação que não
   aparece literal no corpus é paráfrase e cai. Depois checa contradição com o resto do bloco.
3. Aplicação: só ajusta pontuação e corta gagueira de transcrição ("o o", "que que"). Trocar
   palavra dela por sinônimo anula todo o efeito.

Resultado no livro inteiro, três leitores cegos independentes por bloco: **de 4 blocos
lidos como "pessoa" para 15 de 15**, em um dia. Trinta e nove leitores.

Os quatro primeiros, que provaram o método:

| Bloco | Antes | Depois |
| --- | --- | --- |
| 03 | ia 65 | **pessoa 78** (3 a 0) |
| 04 | ia 72 | **pessoa 74** (3 a 0) |
| 05 | ia 72 | **pessoa 69** (3 a 0) |
| 11 | pessoa 67 | **pessoa 72** (3 a 0) |

**Os teimosos cedem na segunda passada, com as pistas do cego no briefing.** Dois blocos
resistiram (capítulo 9 e o anexo A). A segunda rodada de garimpo recebeu, no prompt, as
pistas exatas que os leitores tinham citado, e os dois viraram (pessoa 73, 3 a 0 nos dois).
O workflow aceita `foco` por bloco justamente pra isso.

O capítulo 9 tinha ZERO "né" em 956 palavras, contra 4,74 por mil medidos na fala dela. A
correção não foi salpicar "né" (que é a armadilha do 3e): foi procurar no corpus a fala dela
sobre fechamento, horário e PIX. A fala vem com as muletas no lugar certo e em rajada, de
graça. Perseguir a dose direto é o que nunca funcionou. O que eles citam como prova de humanidade é exatamente o que
um revisor de estilo teria cortado: autocorreção que sobreviveu ("ela morre no meio da
conversa. Ela desaparece no meio da conversa"), interjeição ("pô"), diminutivo depreciativo
("descontinho"), concordância travada, troca de gênero no meio do parágrafo, grafia instável
da mesma interjeição em pontos diferentes do capítulo.

**Regras que saem disso:**
- **Fala transcrita não se pune por ser torta.** A costura torta É a assinatura humana. Depois
  de aplicar uma troca, resistir à vontade de arrumar a concordância.
- **Irregularidade entre trechos vale mais que perfeição dentro de um.** Dois leitores citaram
  a MESMA prova: "Humm..." num lugar e "Hmm" em outro. Padronizar seria destruir evidência.
- **Corpus é pré-requisito, não luxo.** Sem fala medida da autora esta técnica não existe, e
  aí o cego continua sendo termômetro. Antes de aceitar "não dá pra melhorar a voz", procurar
  corpus: neste projeto ele estava no Google Drive da empresa.
- O cego **continua não sendo portão** (3c vale). Ele virou o que sempre deveria ter sido: a
  medida de resultado que diz se a reescrita valeu, não a régua que dita a edição.

**Limite desta seção, posto pelo dono do produto em 10/set:** tudo acima vale pra decidir
QUE MATERIAL entra, e para de valer na hora de decidir COMO ELE É PONTUADO. Ver 3k.

## 3i. A banca: alguém precisa ler o livro inteiro, e ninguém estava lendo

Este pipeline inteiro lia UM BLOCO POR VEZ. O detector mede um capítulo, os revisores conferem
um capítulo contra a fonte, o leitor cego lê um capítulo sem saber que existe livro em volta.
Depois de 39 leitores cegos, 15 blocos no portão do detector e zero achado de pontuação, o
Script 715 tinha treze defeitos que nenhuma dessas lentes podia enxergar, porque todas eram
estruturalmente cegas para o que só existe ENTRE capítulos.

**A banca é seis lentes lendo o livro inteiro, na ordem, de uma sentada:**

| Lente | O que só ela vê |
| --- | --- |
| língua | erro mecânico de português, com o registro oral protegido por lista explícita |
| continuidade | promessa feita e não cumprida, remissão cruzada errada, termo usado antes de ser explicado |
| repetição | a mesma anedota, fórmula ou frase em dois capítulos diferentes |
| contradição | o capítulo A prescreve o oposto do capítulo B |
| leitora-alvo | onde ela perde o fio, onde cansa, o que ela fecha o livro sem saber |
| termos | vocabulário e grafia oscilando ao longo do livro |

Cada uma tem um cético que reabre o livro, e a **primeira obrigação do cético é o grep da
citação**: trecho que não aparece literal é paráfrase, e a acusação cai antes de qualquer
julgamento de mérito. Um relator fecha, junta o que duas lentes acharam no mesmo trecho (isso
é sinal de gravidade) e separa o que é conserto do que é decisão humana.

**O insumo é `livro_continuo.py`**, que junta os quinze blocos num arquivo só, na ordem do
sumário, trocando cerca de compilador por rótulo legível. Ninguém lê `:::frase`; a banca
precisa receber o objeto que a leitora recebe.

**Proteger a voz é o que decide se a banca presta.** O corretor de língua recebe uma lista dura
do que NÃO é erro neste produto: "pra", "tá", "né", frase sem verbo, autocorreção no meio do
raciocínio, coloquialismo de norma não culta dentro da voz da autora. Sem essa lista ele
endireita justamente o que 39 leitores cegos citaram como prova de que o texto é humano. Na
dúvida entre erro e jeito de falar, é jeito de falar.

**Resultado da primeira execução:** 57 acusações, 13 confirmadas, 4 altas. As notas por lente
são o mapa de onde doer: continuidade 8,5 e língua 8,5 (a espinha está firme) contra repetição
6,0 e termos 6,5 (é ali que o livro sangra).

## 3j. Nada comparava a FONTE com o RENDER, e por isso um capítulo saiu incompleto

O achado nº 1 da banca não era de escrita: era um capítulo chegando incompleto no PDF pago.
Uma cerca de fechamento com texto colado na mesma linha (`::: E aí ela responde...`) fazia o
parser não reconhecer o fechamento, seguir até a cerca seguinte e engolir, calado, um parágrafo
inteiro e o bloco "o que evitar" do capítulo.

**Por que nenhum instrumento pegou:** o detector mede a prosa do markdown, o linter mede o
markdown, o leitor cego lê `capitulo-limpo.md`, que é o markdown. Todos liam a FONTE. O render
era o único lugar onde o texto sumia, e ninguém olhava pra ele.

**Duas guardas, as duas em `render_pdf.py`:**
1. Dentro do laço que consome um bloco, qualquer linha que comece com `:::` e não seja cerca de
   fechamento **para o build** e diz o arquivo e a linha. A checagem tem de estar DENTRO do
   laço: no topo ela nunca roda, porque a linha malformada é consumida como conteúdo. Foi
   exatamente esse o ponto cego do parser.
2. Depois de montar o HTML, conta os blocos por tipo no markdown e no render. Se o render tem
   menos, **o build morre** dizendo qual tipo sumiu.

**Regra geral, que vale além deste bug:** toda régua deste pipeline lê a fonte. Se o
compilador perder alguma coisa entre a fonte e o entregável, só um leitor humano descobre, e
tarde. Onde houver compilação, tem que haver conferência de fonte contra saída.

## 3k. Fala real é o insumo, não o acabamento: a fronteira que o dono do produto traçou

A técnica de 3h funciona, e é por isso que ela é perigosa. Ao trocar prosa composta por
fala literal da autora, entra junto tudo que vem colado na fala: a muleta no meio da frase,
o "né" fechando afirmação com ponto, a autocorreção. Os leitores cegos premiam isso, porque
é exatamente o que máquina não produz. **Só que leitor cego não é a leitora, e ebook pago
não é transcrição.**

Em 10/set o dono do produto olhou uma linha do Script 715 e disse: *"esse ', né,' quebra a
leitura demais. É um ebook, não é pra colocar todos os vícios de linguagem dela."* Estava
certo, e a régua acima estava empurrando na direção errada.

**A fronteira, e ela é de POSIÇÃO NA FRASE, não de palavra:**

| Onde está | O que é | Decisão |
| --- | --- | --- |
| `, né,` no MEIO da frase | filler puro, corta o fôlego da leitora no meio | **corta** |
| `, né.` fechando com PONTO | nem tag question é (essa fecha com "?"), é resíduo de transcrição | **corta** |
| `, né?` fechando pergunta | pergunta de confirmação, recurso escrito legítimo | **fica** |
| `Gente,` abrindo frase | vocativo que se dirige a quem lê | **fica** |
| `, gente.` fechando frase | vocativo, idem | **fica** |

No Script 715 isso deu 38 cortes: 22 do meio e 16 de fim com ponto, contra 28 tag questions
mantidas em 11 mil palavras de prosa.

**Cortar não é apagar.** Em seis dos 22 casos, remover a muleta deixava duas orações
independentes coladas por vírgula, porque era ela que fazia a junção. Esses viram ponto
final ou dois-pontos. Aplicar `re.sub` na muleta e ir embora produz erro de pontuação onde
antes havia oralidade, o que é uma troca ruim.

**Mede antes de cortar, e mede POR POSIÇÃO.** O total não diz nada: no Script 715 eram 24
no meio, 45 fechando e 8 abrindo, e só o primeiro grupo era problema. Quem contar só
"quantos né tem no livro" corta os 77 ou não corta nenhum, e os dois estão errados.

**Consequência aceita, não escondida:** essas muletas eram literalmente o que os 39
leitores cegos citaram como prova de humanidade. Tirá-las deve empurrar o veredito na
direção de "ia". Isso é preço, não defeito: o produto é lido por uma doutora cansada no
celular, não por um detector. Quando as duas réguas brigarem, ganha a leitora.

## 3l. Metáfora inventada é andaime, e o detector não a vê

O capítulo mais curto do livro (a transição, 7 páginas de prosa) foi o único que os três
leitores cegos reprovaram por unanimidade: **3 a 0 pra "IA"**. Ao mesmo tempo o detector
dava score **0** nele, o mais limpo do livro inteiro. As duas medições estavam certas e
mediam coisas diferentes.

O que os cegos ouviam era **uma metáfora que eu inventei sustentando o capítulo**. A palavra
era "ponte": a transição era a ponte, a frase pronta era a ponte, e o erro fazia "a ponte
cair". Três aparições, nas três dobras estruturais do capítulo.

A conferência que resolve isso é de uma linha:

```bash
grep -c "ponte" corpus/autora.txt   # 0 em 80.938 palavras
grep -rn "ponte" fontes/*.md        # 0
```

**Zero na fala dela, zero nas fontes.** Era minha, e estava carregando o capítulo.

### Por que o detector não pega

O detector mede vocabulário e estrutura de frase contra o corpus. Metáfora inventada não usa
palavra de IA, não usa conector proibido, não faz antítese. Ela passa limpa. O que ela produz
é **ritmo**: uma imagem inventada precisa ser plantada, retomada e paga, e essas três batidas
caem em pontos regulares. Foi exatamente isso que os cegos descreveram, cada um com outra
palavra: "beat desenhado", "todo parágrafo termina com um clique redondo", "regularidade
rítmica é o tell mais forte".

### A régua

1. **Toda imagem que organiza um capítulo precisa passar no grep do corpus.** Se a autora
   nunca disse aquilo, ela não pode ser a viga. Pode ser uma frase de passagem; não pode ser
   o que segura três parágrafos.
2. **Pancada curta de uma palavra fechando parágrafo** ("A ponte.", "Mantém.") é o
   maneirismo que o fingerprint proíbe explicitamente. Ela não faz isso.
3. **O conserto não é cortar, é substituir por fala real.** Cortar a metáfora deixa o buraco
   e o capítulo fica mais liso ainda. Ir ao corpus e achar como ela diz aquilo é o que move
   o cego. Aqui virou "a parte em que a gente oferece pra ela o problema resolvido", que é
   dela, e entrou junto uma doutrina que o capítulo não tinha ("a pessoa não pode sair da
   transição com medo").
4. **Depois de enxertar, rode o detector no bloco.** O meu enxerto introduziu um contraste
   "não é X, é Y", que o fingerprint limita a um por capítulo. O detector pegou na hora.

Resultado da passada: 0 a 3 pra "IA" virou **2 a 1 pra "pessoa"**, e as duas provas de que
era gente que os leitores citaram foram as frases dela que eu enxertei.

**Corolário pro portão:** um bloco com detector baixo e cego reprovando não é contradição, é
divisão de trabalho. O detector vê palavra, o cego ouve ritmo. Bloco de prosa composta, sem
cena e sem caso, é o candidato natural — rode o cego nele mesmo quando o detector estiver
zerado.

## 3m. O bloco canário, e por que a correção também precisa de portão

O capítulo mais composto do livro (a transição: o mais curto, sem cena de paciente, sem caso)
oscilou **quatro vezes num único dia** entre "pessoa" e "IA", e cada volta foi por um tell
DIFERENTE, todos escritos por mim, um deles introduzido pela correção anterior:

| passada | veredito | o que os cegos ouviram |
| --- | --- | --- |
| 1 | 0×3 pessoa | a metáfora inventada ("a ponte"), plantada e paga em três dobras |
| 2 | 2×1 pessoa | — (a fala real enxertada virou a prova de humanidade) |
| 3 | 1×2 pessoa | decalque de tradução ("e é isso que a transição é") + contabilidade da própria lista ("três desses quatro… o quarto") |
| 4 | 2×1 pessoa | cadência: três seções abrindo com fragmento curto isolado + antítese espelhada |

Três lições, e a terceira é a que dói.

**1. Existe um bloco canário, e dá pra saber qual é antes de medir.** É o mais curto, o de
prosa 100% composta, o que não tem cena nem caso nem transcrição. Ele acusa primeiro. Numa
rodada com orçamento apertado, mede esse antes de todos.

**2. O detector e o cego não brigam, dividem trabalho.** Esse capítulo esteve com score 0 e
3×0 "IA" ao mesmo tempo. Palavra contra ritmo. Score baixo não dispensa cego.

**3. A correção precisa passar no mesmo portão que o texto original.** Duas das quatro voltas
foram causadas pela correção anterior: eu comprimi a fala dela ("transformar essa transição em
algo que deixe ela mais certa… ao invés de incerteza, mais certa") numa antítese espelhada
("mais certa da decisão, e não mais incerta"), que é o maneirismo mais previsível de máquina em
PT-BR. **Comprimir fala real é reescrever.** Se a frase dela é torta e longa, ela entra torta e
longa, ou não entra.

Régua: depois de aplicar qualquer correção num bloco, roda o detector NELE e, se for bloco
canário, roda o cego de novo. Correção não é isenta de medição.

## 4. O que nunca entra

- Caso, número, data ou frase pronta que não esteja nas fontes ou na fala
  transcrita da autora. Exercício, meta e conta inventados saem, mesmo quando
  ficam bons.
- Frase pronta de script alterada. Ela vai literal do PDF; adaptação só em cena,
  e com o card literal por perto.
- Placeholder da fonte vazando para o texto corrido (`Dra. Mariana`, `Fulana`).

## 5. Rastro obrigatório

Cada rodada deixa em `revisao/NN/`: a versão anterior do capítulo
(`capitulo-vK.md`), o JSON da rodada, o TXT legível e o detector da versão nova.
Sem esse rastro não dá para provar que o padrão foi seguido, e a palavra de quem
escreveu não vale como prova.
