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

**1. Licença das fontes TT Modernoir. Isto bloqueia o lançamento.** As fontes
instaladas são versão trial. O PDF está usando `TT_Modernoir_Trial_Bold.ttf`.
Vender o material com fonte trial é problema de licenciamento, não de design.

**2. As duas fontes da metodologia discordam entre si, e isso vazou pro livro.**
O `01-framework-715.md` e o `03-manual-perguntas.md` trazem redações diferentes
das mesmas frases prontas:

| Frase | Framework | Manual de perguntas |
| --- | --- | --- |
| Transição | "e de já estar **desde** [tempo]" | "e por já estar **há** [TEMPO INFORMADO]" |
| Apresentação | "com o [problema] **e parar de**" | "com a [DOR TRAZIDA] **e parar de**" |
| Horário | "na agenda **da Dra. Mariana**" | "na agenda é **[dia/horário]**" |
| Comprovante | "para já **confirmarmos** seu horário" | "para já **garantir** o seu horário" |

Padronizei no livro pela redação que fecha gramaticalmente, mas **o PDF da
metodologia precisa da mesma correção**, senão a divergência volta no próximo
material. Duas delas são erro de verdade, não variação:
- "desde [tempo]" não fecha: "desde" pede data e a paciente dá duração ("uns dois anos").
- "vai te ajudar com o [problema] **e** parar de se sentir" faz a DOUTORA parar de se
  sentir mal. É a frase mais copiada do livro, e ia direto pro WhatsApp da paciente
  assim. Virou "**pra você** parar de se sentir".

**3. Três buracos de conteúdo que eu não posso preencher sem inventar.**
- **O que responder quando ela diz que faz o PIX à noite.** O manual de objeções não
  tem esse card. O capítulo 09 prometia "objeção tem lugar próprio mais pra frente" e
  o capítulo 11 não entrega. Mudei a remissão pra apontar pra ferramenta genérica que
  existe, mas o card em si depende da Ana.
- **O que fazer com as conversas que já morreram no WhatsApp.** A leitora fechou o
  livro sem saber, e o livro pergunta isso em cinco capítulos. Existe material na fala
  dela sobre reativação, mas de outra coisa: lista fria de contatos que nunca
  agendaram, e depende de um "manual de abordagens" que não está entre as fontes.
  Declarei o recorte no capítulo 12 ("este livro é da próxima conversa em diante") pra
  não deixar a leitora pendurada. **Se você quiser o capítulo, ele precisa da Ana.**
- **No capítulo 11, dois cards mandam prometer o valor do procedimento e um terceiro
  proíbe passar valor de caso que ninguém olhou.** O livro não diz como se cumpre a
  promessa.

**4. Quem digita no WhatsApp.** O livro nunca decide: ora é você, ora é a atendente,
ora é a doutora, e as frases prontas pressupõem que a doutora é outra pessoa. Não se
resolve com achar e substituir: é escolha de leitora-alvo, e é barato resolver agora.

**5. Dois pontos de cansaço, que são decisão editorial.** A leitora cansou na abertura
do capítulo 02 (leu como a página de vendas de novo, com faturamento de 200 mil) e na
primeira metade do capítulo 12 (que reconta o capítulo 1 pela quarta vez).

**6. Duas correções de pontuação dentro de card de script.** Estão em
`revisao-pontuacao.json`, campo `em_card`. Não apliquei porque frase de script vai
literal, e mexer nelas é decisão sua.

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
