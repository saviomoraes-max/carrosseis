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
