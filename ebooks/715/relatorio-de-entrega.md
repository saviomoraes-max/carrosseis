# Script 715 — relatório de entrega

Para o Sávio. O que o livro é, o que foi medido, o que depende de você e como
regerar tudo. Atualizado em 10/set/2026, depois da banca de leitura.

O documento de retomada técnica é o `ESTADO.md`, ao lado deste. Este aqui é o de
decisão: o que dá pra vender, o que ainda não, e por quê.

---

## O produto

Ebook pago, vendido pela página da VSL, sobre o **Script 715**: sete passos de
atendimento no WhatsApp de clínica de harmonização facial, do primeiro "oi" ao
comprovante do PIX. Narrado em primeira pessoa pela **Ana Luiza**. Leitora-alvo:
doutora que comprou pela VSL e lê no celular, entre um paciente e outro.

**Arquivo:** `render/script-715.pdf`, 9:16 (1080×1920), feito pra tela de celular
e não pra papel. Capa e rodapé levam só a marca Reconecta, sem assinatura de autora.

**Estrutura:** capa, sumário, quatro partes com página-marcador, doze capítulos,
três anexos e contracapa com o CTA. São 143 páginas, zero páginas órfãs, e **34 gráficos vetoriais** ilustrando o que o texto diz, sem uma foto.

| Parte | Capítulos |
| --- | --- |
| 1 · Antes do script | A salinha do financeiro · Vender o que ela já quer comprar |
| 2 · Os sete passos | Conexão · Situação · Presente inaceitável · Qualificação · Transição · Apresentação · Fechamento |
| 3 · Objeção e resposta | Objeção não é um não · O manual de respostas |
| 4 · Pra usar no dia | Doutora é vendedora também · Cola · Banco de perguntas · Paciente modelo |

**Peça extra:** `render/cola/` tem a cola dos sete passos como PNG solto
1080×1920, pra doutora salvar na galeria e abrir sem o PDF.

---

## De onde saiu cada frase

O livro só contém o que está nos três PDFs da metodologia (framework 715, manual
de objeções, manual de perguntas), na fala transcrita da Ana ou nas aulas do WAID.
Isso não é promessa, é medição: uma varredura de invenção passou nos quinze blocos
com dois papéis opostos, um acusando e outro defendendo, e as 28 afirmações que
sobreviveram à defesa foram cortadas ou reescritas. O padrão dominante do que caiu
não foi caso inventado, foi quantificador sem fonte ("a maioria das clínicas", "o
mais pulado").

Toda frase pronta de script vai **literal** do PDF. Adaptação só dentro de cena,
com o card literal por perto.

---

## O que foi medido, e com que régua

Três instrumentos, todos rodando por script e todos com o rastro em `revisao/`.

**1. Detector de sotaque de IA** (`detector_ptbr.py`). Portão: ≤ 25.

Todos os blocos avaliáveis passam. Os anexos A e B ficam fora do portão por
amostra pequena: têm 264 e 119 palavras de prosa, e métrica de densidade sobre
isso mede ruído. O único achado de cada um é o formato da peça (tríade na cola,
lista no banco de perguntas), não a escrita.

**2. Leitor cego.** Três leitores independentes por bloco, sem contexto nenhum,
decisão por maioria. **Não é portão**, é termômetro: em 08/set ele penalizou uma
citação literal da Ana como se fosse máquina, e desde então fidelidade sempre
vence. Mesmo assim ele é a única medida de resultado que existe.

**3. Banca de leitura** (`wf_banca.js`). Seis examinadores leem o livro INTEIRO de
ponta a ponta, um cético por examinador, e um relator fecha. Foi a primeira vez que
alguém leu este livro do começo ao fim: tudo que existia antes lia um bloco por vez.
Achou 13 defeitos confirmados que nenhuma outra lente podia ver, incluindo um
capítulo que chegava **incompleto no PDF pago**. Parecer completo em
`revisao/banca-10set.md`.

**4. Linter de pontuação** (`revisor_pontuacao.py`). Fala reportada sem aspas, aspa
que não fecha, espaço antes de pontuação, parágrafo em minúscula, e a mesma frase
repetida duas vezes no mesmo parágrafo. **Zero achados.** Zero travessão no livro
inteiro, 205 pares de aspas curvas fechando.

---

## O que aconteceu de mais importante

O livro tinha um problema que resistiu a três tentativas de conserto: leitores
cegos independentes reconheciam máquina em vários capítulos. A causa estava
diagnosticada — costura entre a fala transcrita da Ana e prosa composta imitando
ela — mas as três tentativas de resolver por EDIÇÃO falharam, e duas pioraram.

Em 09/set a quarta tentativa funcionou, e não foi edição. Agentes garimparam as
**80.938 palavras de fala da Ana** procurando ela dizendo a mesma coisa que a
prosa composta dizia, e trocaram. Cada citação foi conferida literal no corpus
antes de entrar: paráfrase não passa.

O método foi então aplicado ao livro inteiro. **De 4 blocos lidos como "pessoa" na
manhã de 09/set, o livro fechou em 15 de 15.** Trinta e nove leitores cegos
independentes, três por bloco, decisão por maioria, sem que nenhum soubesse nada
sobre o livro nem sobre quem escreveu.

E o que eles citam como prova de que é gente é justamente o que qualquer revisor
teria cortado: a autocorreção que sobreviveu ("ela morre no meio da conversa. Ela
desaparece no meio da conversa"), o "pô", o "descontinho", a concordância travada,
"misericórdia" no meio da oração, o "visto azul", e a mesma interjeição grafada de
dois jeitos em pontos diferentes do capítulo.

Os dois últimos, o capítulo 9 e o anexo A, resistiram à primeira passada e cederam
na segunda, quando os garimpeiros receberam no briefing as pistas exatas que os
leitores cegos tinham citado. O capítulo 9 tinha zero "né" em 956 palavras. A
correção NÃO foi salpicar "né": foi trocar prosa composta pela fala dela sobre
fechamento e PIX, que já vem com as muletas no lugar e em rajada.

Isso mudou o método do projeto e está registrado na skill, pra valer no próximo
livro.

---

## O que depende de você

**1. ~~A fonte~~ — resolvido em 10/set.** Você tinha razão: a TT Modernoir licenciada
já estava ativada nesta máquina pelo Adobe Fonts, e o `Trademark` dela diz *"TT
Modernoir (Special version for Adobe)"*. O que estava errado era o render, que apontava
por `@font-face` pros cinco `.ttf` de **trial do DaFont** que estão na pasta do design
system e, por isso, sobrepunha a licenciada e embutia no PDF a string *"not for
commercial or personal use"*.

O `@font-face` saiu. O Chromium resolve a família `TT Modernoir` pelo sistema, e o PDF
agora embute `TTModernoir-Bd` em 24 subsets, com zero menção a trial, a DaFont ou a
TypeType, e zero ocorrência de `Impact` (o fallback). O render também morre se a família
não resolver, pra nunca mais sair um PDF com a tipografia trocada em silêncio.

**Uma limpeza que vale fazer:** os cinco `TT_Modernoir_Trial_*.ttf` em
`Reconecta Design System/fonts/` podem ser apagados. Enquanto existirem, qualquer peça
nova que aponte pra pasta reintroduz o problema.

**2. Duas frases prontas da metodologia lidas ao pé da letra dizem outra coisa.**
Você decidiu que a metodologia é proposital, e o livro voltou a carregar a redação
literal dela. Registro aqui só pra você ter o dado, sem reabrir:
- *"a doutora vai te ajudar com o [problema] **e** parar de se sentir [como está se
  sentindo]"* — como "com o [problema]" é sintagma preposicional, "parar" coordena com
  "vai te ajudar", e quem para de se sentir mal, lido ao pé da letra, é a doutora. É a
  frase mais copiada do livro e vai colada pro WhatsApp da paciente.
- *"e de já estar **desde** [tempo] sentindo assim"* — "desde" pede data e a paciente dá
  duração, então sai "desde uns dois anos". O manual de perguntas escreve "**há** [TEMPO
  INFORMADO]", que fecha. As duas fontes discordam entre si, e o livro agora reflete
  cada uma na sua casa: capítulos e cola seguem o framework, anexo B segue o manual.

**3. As muletas orais saíram, e isso tem um preço declarado.** A seu pedido, 38 muletas
foram cortadas: o `, né,` do meio da frase e o `, né.` fechando com ponto. Ficaram as 28
que fecham pergunta com `?`, que são recurso escrito, e os vocativos que se dirigem a
quem lê. **O preço:** essas muletas eram literalmente o que os 39 leitores cegos citavam
como prova de que o texto era humano, então o veredito deles deve andar na direção de
"IA". Registro isso pra ninguém confundir a causa depois: não é o texto piorando, é uma
troca deliberada de régua, com a leitora ganhando do detector.

**4. Quatro posições da casa sobre quem digita no WhatsApp, e você já escolheu.**
Registro só pra não voltar à mesa: a ficha T8.23 diz que quem responde nunca se passa
pela doutora; a decisão canônica D-C de 28/jul diz o oposto e revoga a T8.23; o fluxo de
handoff apresenta a secretária com autoridade emprestada; e o framework 715, que é a
fonte do livro, fala da doutora em terceira pessoa em todas as frases prontas. **O livro
segue o framework, por decisão sua em 10/set**, e o capítulo 02 declara uma vez quem é
"você". Se um dia a D-C valer pro WhatsApp, são 29 frases prontas a virar.

## O que a leitora disse, e onde ela cansou

A banca põe uma leitora-alvo pra ler o livro inteiro de uma sentada, como ela leria:
dentista de harmonização facial, atende o WhatsApp da própria clínica, comprou pela
página de vendas, lendo no celular à noite. Ela deu **nota 8** e disse que
recomendaria pra uma colega. Onde o livro a ganhou, nas palavras dela:

- a cena da salinha do financeiro no capítulo 1, *"porque eu já fui essa paciente e eu
  já sou essa clínica"*;
- o gráfico do bastão no capítulo 2, *"a coisa mais útil do livro inteiro, porque eu me
  vi respondendo R$ 200 e olhando pro visto azul"*;
- a paciente do queixo, que atravessa do capítulo 4 ao 9 sem trocar de exemplo;
- o capítulo 11 inteiro, *"que é o que eu vou realmente usar"*.

**Ela cansou em dois pontos, e os dois são corte editorial, não defeito:**

**A abertura do capítulo 02.** É o bloco das quatro doutoras e do *"nós temos pessoas
que faturam 200 mil em cidades de 5 mil habitantes"*. Nas palavras dela: *"Essa página
eu pularia. É a página de vendas de novo, com faturamento e tudo, e eu já comprei. Nada
disso é atendimento no WhatsApp, e o capítulo só engata quando chega na parte de dentro
do WhatsApp."* O material é literal da fala da Ana e é bom argumento; o problema é o
lugar, logo depois de ela já ter pago.

**A primeira metade do capítulo 12.** A salinha do financeiro volta **quatro vezes** no
livro: capítulos 1, 6, 10 e 12. Nas duas últimas ela é renarrada com as frases do
capítulo 1 quase intactas, e o 12, que deveria ser o giro final, refaz a seção "A
salinha do WhatsApp" do capítulo 1. Ela: *"Na quarta vez eu passei o dedo pra frente."*

**Os dois foram cortados em 10/set, a seu pedido.** O corte foi cirúrgico, não uma
reescrita:

- No **capítulo 02** saiu só o bloco de faturamento (*"Nós temos pessoas que faturam 200
  mil em cidades de 5 mil habitantes..."*) e a pergunta que dependia dele. **A anedota
  das quatro doutoras ficou**, porque é ela que arma a tese, e a tese ficou inteira
  (*"Não foi nada externo, é sempre algo interno"*). O capítulo agora emenda direto no
  título "O que é interno no WhatsApp".
- No **capítulo 12** saiu a renarração da cena da salinha, que o parágrafo anterior já
  aponta (*"No capítulo 1 eu te contei a salinha pelo lado da paciente"*), e a frase
  quase idêntica à do capítulo 1 virou ponteiro (*"O fechamento pode até ficar do lado
  de fora, como eu falei lá no capítulo 1"*). O argumento do capítulo ficou intacto.

As voltas da salinha nos capítulos 6 e 10 **não** foram cortadas: lá ela é callback com
conteúdo novo (o estado emocional no diagnóstico, o monólogo dos dez minutinhos), não
renarração.

O terceiro ponto de cansaço que ela apontou, o link de rastreio à mostra dentro de um
produto pago, já está resolvido: a leitora vê `supercaso.com.br/consulta` e os UTMs
viajam no destino.

## O que dá pra fazer sem depender de ninguém

Estão em `ideias-de-leitura.md`, com o custo de cada uma. As três que valem mais:

- **Anexo B indexado "pelo que ela disse"** em vez de por etapa. Hoje a doutora
  precisa saber em que passo está; assim ela acha pela mensagem que chegou.
- **Glossário de uma página** (bastão, cortina de fumaça, presente inaceitável).
  É a mais arriscada: definição inventada já passou por quatro rodadas de revisão
  neste livro uma vez. Só entra com cada verbete literal de fonte.
- **Áudio da Ana por capítulo**, com link na abertura. Fecha o problema de voz de
  vez, mas depende dela gravar.

---

## Como regerar

```bash
P=~/reconecta/ebooks/715
S=~/.claude/skills/ebook-humano-reconecta/scripts

python3 $S/render_pdf.py $P --provas    # PDF + PNG por página + cola + abre o preview
python3 $S/andamento.py  $P --detalhe   # onde o projeto está, medido dos arquivos
python3 $S/revisor_pontuacao.py $P      # pontuação e ortotipografia
python3 $S/detector_ptbr.py $P/revisao/11/capitulo-limpo.md \
        --corpus $P/fontes/voz/corpus/ana-luiza-falas-treinamentos.txt
```

O `--corpus` não é opcional: sem ele o detector acusa como vocabulário de IA
palavras que são da Ana. Ele marcou "gerar valor" como sotaque de máquina numa
frase que sai inteira da boca dela, onde a expressão aparece quatro vezes.

Cada passada grande deixou um snapshot em `revisao/_pre-*`, então dá pra voltar
atrás em qualquer ponto. As provas em PNG e o HTML intermediário não vão pro git
(45 MB de derivado): `--provas` refaz em dois minutos.

O método está versionado em `skills/ebook-humano-reconecta/`, espelho da skill que
vive em `~/.claude/skills/`. A peça a ler antes do próximo livro é
`referencias/padrao-de-refinamento.md`.
