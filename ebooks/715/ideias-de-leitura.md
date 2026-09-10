# Script 715 · ideias pra leitura mais interessante

Estado: 10/set/2026. O que já entrou no render e o que depende de decisão do Sávio.

## Já feito nesta rodada (render v2, 121 páginas)

1. Respiro: parágrafo com 40px embaixo, entrelinha 1.5, mais ar sob o kicker. Página caiu de ~200 pra ~140 palavras.
2. Cena vira transcrição de WhatsApp: balão da paciente à esquerda, o seu à direita (dourado).
3. Trilho dos 7 passos no topo da abertura de cada passo (o passo do capítulo aceso).
4. "Como ela lê você" vira quadro: ponto vermelho (leitura negativa) e ponto dourado (positiva), frase literal do framework.
5. "Quando avançar" vira checklist numerado com caixas (itens literais do framework).
6. Frase-prova em página inteira (kicker "Prova") e pergunta final de cada capítulo em página inteira (kicker "Pergunta em aberto", rótulo do próprio DS).
7. Gráficos: linha do tempo da salinha (cap. 1), duas salinhas (cap. 1), funil 5 contatos → 1 agendamento (cap. 2), grade das 8 bases (cap. 2), bastão com ela × bastão com você (cap. 2), os 3 passos do fechamento (cap. 9), objeção real × cortina de fumaça (cap. 10), trilho completo na cola (anexo A).
8. Frase pronta com fio dourado à esquerda; "o que evitar" com fio vermelho.

Tudo vetor e texto, no vocabulário do DS (Space Mono, hairline, ponto, barra). Sem ícone, sem ilustração, sem foto.

## Feito na rodada de 09/set (render v3, 137 páginas)

9. **Páginas-marcador entre as partes (era a proposta B).** Quatro divisórias: Antes do
   script (01-02), Os sete passos (03-09), Objeção e resposta (10-11), Pra usar no dia
   (12 + anexos). Cada uma lista os capítulos da parte, então funciona como sumário local.
   Os rótulos são navegação, não doutrina: nenhuma afirmação nova entrou.
10. **Contracapa (era a I).** O convite e o link do CTA, com o texto LITERAL do capítulo 12.
11. **Barra de progresso no rodapé (era a G).** Hairline com a posição da leitora no livro.
12. **Cola exportada como PNG (era a E).** `render/cola/` tem três telas 1080×1920 geradas
    por `cola_png.py`, com tipografia própria de consulta rápida. Recortar página do PDF não
    servia: entregava o corpo de leitura de 38px e perdia as notas entre as frases pontas
    ("a chave PIX vai numa mensagem separada"). O empacotamento é medido no browser, não
    chutado, então nada estoura o rodapé.
13. **Capítulo 11 em cartão (era a A, e ficou melhor que a proposta).** Duas colunas não cabem
    em 9:16. Virou cartão vertical com três slots rotulados: ELA MANDA, SE RESPONDER ASSIM,
    PERDE (vermelho) e O QUE CONTINUA A CONVERSA (dourado). Como o andaime virou rótulo, o
    detector do capítulo caiu de 40 pra 22 sem trocar uma palavra — a conversão é provada
    neutra por contagem de palavras.
14. **O render se audita.** Toda compilação reporta página de miolo abaixo de 35% de ocupação.
    As páginas vazias por desenho (abertura, parte, capa, sumário, contracapa, frase inteira)
    ficam fora da conta.

## Feito em 10/set: sete tipos novos de gráfico

O livro tinha 22 gráficos em 8 tipos e quatro blocos sem nenhum. Passou a **34 em 15 tipos,
e todo bloco tem pelo menos um**. Todos seguem a mesma regra dos anteriores: só texto,
hairline, ponto e barra, sem ícone, sem ilustração, sem foto. E **todo rótulo é literal do
manuscrito** — nenhum diagrama afirma nada que o texto ao lado não diga.

15. **`bifurca`** — uma situação, dois caminhos, dois desfechos, com o que continua a
    conversa em dourado e o que perde a paciente em vermelho. Entrou no capítulo 10 (chega
    o "vou pensar"), no 5 (você oferece a espera) e no anexo C (a seleção).
16. **`convergem`** — caminhos diferentes que terminam no mesmo lugar. Capítulo 12: no
    WhatsApp o número vai cedo demais, na salinha vai por quem não ouviu nada, e nos dois
    casos ela sai com o número na mão.
17. **`escala`** — régua com dois extremos e o ponto do meio aceso. Anexo C: nem a mensagem
    "topa ou não topa", nem os sete passos completos.
18. **`ordem`** — sequência vertical numerada pra quando a ORDEM é o conteúdo. Capítulo 4:
    os quatro verbos do passo dois.
19. **`indice`** — índice de seções pra consulta rápida. Capítulo 11, que tem 1.900 palavras
    e seis famílias de objeção: a leitora acha o caso sem folhear.
20. **`mapa`** — ligação item → destino com o fio no meio. Capítulo 10: cada resposta pro
    "vou pensar" e o passo a que ela pertence.
21. **`rail` com conjunto** (`rail 1,2,6,7`) — caminho curto no trilho dos sete passos, com
    os pulados apagados e o fio tracejado entre eles. É o anexo C inteiro numa linha.

**Dois defeitos do paginador corrigidos junto:**
- Gráfico de linhas era indivisível, então quando não cabia empurrava tudo e deixava meia
  página vazia atrás. Agora `ordem`, `indice`, `sinais` e `mapa` quebram entre páginas como
  lista, com a numeração continuando. Os outros seguem inteiros de propósito: quebrar um
  `duas` ou um `leituras` separa a célula do par dela.
- O rótulo "FECHAMENTO" do trilho cortava na borda direita da página.

## Feito em 10/set (tarde): a faxina do parecer da 5ª banca

A 5ª banca confirmou três achados pelo cético e o relator escreveu, além deles, uma lista de
itens que ninguém tinha aplicado porque não passaram no cético. Só que boa parte deles não é
opinião, é CONTAGEM — dá pra provar com grep. Verifiquei um por um antes de tocar em qualquer
coisa. Oito eram defeito de verdade:

22. **Anexo C: três números diferentes com o mesmo `[valor]`.** "O valor normal desse protocolo
    é [valor] e, como paciente modelo, fica [valor]... uma reserva de [valor]." A doutora
    preenche e ENVIA. Virou `[valor normal]`, `[valor de modelo]`, `[valor da reserva]`. É o
    mais caro da lista porque o erro sai da clínica dela, não do livro.
23. **Anexo C: "edição" usada quatro vezes antes de ser definida**, e a primeira delas dentro da
    mensagem que a leitora manda. A definição era do próprio livro, só estava 31 linhas tarde
    demais. Subiu pra antes da primeira frase pronta.
24. **Anexo C não era chamado por ninguém.** Nove páginas que só o sumário alcançava. Uma linha
    no cap 12 resolve, e o link interno já aponta pra lá.
25. **Cap 10: "naqueles dez minutinhos da salinha".** No cap 01 os dez minutinhos são de espera
    na recepção, ANTES de entrar. A volta da cena contradizia o gráfico da própria cena.
26. **Cap 11: "nas duas respostas de preço lá em cima" são três.** Contadas: as três prometem
    passar a informação.
27. **Cap 02: "outro pecado mortal" sem primeiro pecado.** Nenhum dos quatro itens anteriores
    fala em pecado.
28. **Cap 02: a comparação da conversa robótica aparecia duas vezes.** No corpus a autora falou
    ela UMA vez. Fica no cap 05, onde a leitura negativa É o interrogatório.
29. **Cap 04: a troca de procedimento sem costura.** O cap 03 demonstra com preenchimento labial
    e o 04 abre com flacidez no queixo. Uma linha reconhece a troca e apresenta a paciente que
    atravessa 04, 05, 06, 07 e 08.
30. **Cap 07: o `[tempo]` creditado ao passo três.** Na cena do próprio livro ela entrega o tempo
    ("tem uns dois anos que eu reparo") respondendo o passo DOIS, uma fala antes da pergunta do
    "por que agora".

**Seis achados do mesmo parecer eu descartei, e o motivo importa mais que o corte:**
- "nem se a consulta for de graça vai valer a pena" nos caps 07 e 11: é literal do manual de
  objeções, que também a repete em dois lugares (p.48 e p.270). Metodologia é proposital.
- "olha esse caso que lindo" nos caps 03 e 06: o cap 06 declara a repetição na mesma frase
  ("é o erro que mais volta no material"). Callback marcado não é eco.
- "a salinha do fechamento ou a salinha do pagamento" nos caps 01 e 12: é o bookend do livro,
  a mesma pergunta abrindo e fechando.
- "lead" quatro vezes: é palavra da autora, está no corpus.
- `[tempo]` contra `[tempo informado]`: as duas metodologias divergem e o Sávio já decidiu.
- a frase da apresentação e o "desde [tempo]": decisão do Sávio, metodologia é proposital.

## Feito em 10/set (fim de tarde): os quatro pedidos de acabamento da leitora

A leitora-alvo da banca fez quatro pedidos práticos. Três eram meus e foram feitos; o quarto
é escopo e está registrado como decisão.

31. **A objeção mais comum do dia dela não tinha texto colável.** "Faço o PIX à noite"
    existia como PROSA no cap 09 (o que não fazer), e o próprio cap 09 delegava ao 10/11 —
    só que o cap 11 não tinha a família. Agora tem: **"Na hora do PIX"**, com dois cartões.
    A resposta e o "disclaimer pequeno" são fala literal dela no corpus, do dia em que essa
    objeção exata foi levada pra ela numa mentoria; a regra do horário é do cap 09
    ("sem PIX, sem agenda"). O cap 09 ganhou a remissão que faltava.
32. **O cartão do orçamento mandava ela escrever a própria frase**, num capítulo em que todo
    o resto é copiar e colar. O livro já abria a exceção ("se é você mesma que responde... só
    troca o 'eu só faço o agendamento' pelo motivo verdadeiro") e já tinha o motivo verdadeiro
    escrito no parágrafo seguinte. Montei a frase com as duas peças, sem inventar nada.
33. **Os gráficos repetiam o parágrafo palavra por palavra.** Medido: **13 dos 34**. O pior
    era o cap 04, com a mesma lista de quatro itens como frase corrida de 51 palavras e logo
    abaixo como diagrama. Nova divisão de trabalho: **o gráfico diz QUAIS são, a prosa diz
    POR QUE acontecem**. Ficou em 9 de 34, e os que sobraram são de um ou dois rótulos com
    parágrafo fazendo outro serviço.
34. **O gráfico `leituras` descartava linha em silêncio.** Achado pelo leitor cego, não pela
    banca: o parágrafo dizia "a leitura negativa tem três frases" e o diagrama ao lado
    mostrava UMA. O renderizador só guardava a última linha `NEG:` — qualquer segunda sumia
    sem aviso, do mesmo jeito que já fez um capítulo inteiro sumir do PDF. Consertado no
    `graficos.py` (aceita várias, e morre se não achar nenhuma) e as frases que faltavam,
    todas literais do framework, entraram nos caps 04, 06 e 08.

**Os doze fins de capítulo continuam perguntando o que ela errou sem dar tarefa pra amanhã.**
A leitora reclamou e a banca respondeu que isso é ESCOPO, não revisão: mexer significa
reeditar os doze fechos de um livro pronto. Não fiz por conta própria. Vale registrar que a
instrução prática existe, só não está no fecho: nos sete capítulos de passo ela vem em
"Quando avançar", logo acima da pergunta, e no livro inteiro vem no anexo A e no cap 12.

## Propostas (a validar)

~~A. Cap. 11 em duas colunas~~ — FEITO, como cartão (item 13). Duas colunas não cabem em 9:16. Era: "se quiser perder" (vermelho) × "se quiser continuar" (dourado). Hoje é prosa + card; em coluna vira consulta rápida no celular.
~~B. Páginas-marcador~~ — FEITO (item 9). Era: Parte 1 (caps 1-2, a tese), Parte 2 (caps 3-9, os 7 passos), Parte 3 (caps 10-11, objeções), Parte 4 (cap. 12 + anexos). Uma página escura com o número da parte gigante, como a abertura de capítulo.
C. Um caso completo em balões, do "quanto custa" ao comprovante, como anexo C. Precisa de fonte: uma conversa real anonimizada (canal de depoimentos no Slack) ou um roteiro que a Ana aprove. Não invento. **Continua sem fonte em 10/set** — segue fora.
~~D. Anexo B indexado "pelo que ela disse"~~ — **DESCARTADO em 10/set, com motivo.** A ideia era: palavra que ela usou → pergunta pra devolver. Só que a seção 2 do anexo B já é isso, cada pergunta carrega a palavra dentro, e o cap 04 ensina explicitamente que é UM movimento aplicável a qualquer palavra ("dá pra fazer isso com qualquer palavra que ela trouxer"). Um índice de dez entradas sugere consulta exaustiva e trabalha CONTRA a doutrina, fazendo a leitora procurar a palavra dela na lista em vez de aplicar o movimento. Não é falta de trabalho, é que a ideia estava errada.
~~E. Cola em PNG~~ — FEITO (item 12). Era: 1080×1920 separado, pra doutora salvar no celular e abrir sem o PDF.
~~F. Links internos no PDF~~ — FEITO **e verificado**. O sumário e toda menção a capítulo ou anexo viram link. A checagem que faltava era outra: o Chromium podia estar descartando âncora interna na impressão, e o sumário viraria retângulo morto sem ninguém perceber. Conferido no PDF gerado, destino por destino, contra o `indice-paginas.json`: 35 links internos, todos caindo na abertura certa, mais os 2 externos do CTA. O regex do render só cobria anexo A e B; foi pra A-D, senão a primeira menção a anexo C sairia como texto morto.
~~G. Barra de progresso~~ — FEITO (item 11). Era: (hairline com a posição), além do "Passo 03/07" do HUD.
H. Glossário de uma página: bastão, cortina de fumaça, presente inaceitável, leitura, transição. **Medido em 10/set e o buraco é menor do que parecia:** cada termo da casa já nasce definido na primeira aparição — bastão no cap 02, presente inaceitável é o título do 05, cortina de fumaça abre o 10, edição agora vem antes da primeira mensagem no anexo C. Sobra só "transição", usada no cap 06 antes do 07 definir, e ela já é nome de passo no trilho. Se for fazer, toda entrada é frase LITERAL do livro com o capítulo de origem: definição inventada já passou por quatro rodadas aqui.
~~I. Contracapa~~ — FEITO (item 10). Era: (hoje o link está solto no cap. 12).
J. Áudio: se a Ana gravar cada capítulo, QR/link na abertura. Fecha o problema de voz de vez.
K. Carimbos tipográficos nas aberturas ("Caso aberto", "Arquivo confidencial"), no vocabulário dos kickers do DS. Só se não pesar.

## O que NÃO vou fazer sem fonte

Exercícios, contas, metas ou casos que não estejam nos PDFs ou na fala da Ana. O exercício das 20 conversas saiu por isso.

## Ainda de pé, e o que cada uma custa

- **C (caso completo em balões)** e **J (áudio da Ana por capítulo)** dependem dela: fonte
  nova ou gravação. Não invento conversa.
- **D (anexo B indexado pelo que ela disse)**, **H (glossário)** e **K (carimbos)** são
  trabalho de render sem fonte nova. O glossário é o mais arriscado: definição inventada já
  passou por quatro rodadas neste livro uma vez (ver `paridade-de-juri.md`), então só entra
  com cada verbete literal de fonte.
- **F (links internos)** já está feito desde 08/set: sumário clicável e toda menção a
  "capítulo N" e "anexo A/B" vira link no PDF.
