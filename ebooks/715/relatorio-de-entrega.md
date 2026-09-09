# Script 715 — relatório de entrega

Para o Sávio. O que o livro é, o que foi medido, o que depende de você e como
regerar tudo. Escrito em 09/set/2026.

O documento de retomada técnica é o `ESTADO.md`, ao lado deste. Este aqui é o de
decisão: o que dá pra vender, o que ainda não, e por quê.

---

## O produto

Ebook pago, vendido pela página da VSL, sobre o **Script 715**: sete passos de
atendimento no WhatsApp de clínica de harmonização facial, do primeiro "oi" ao
comprovante do PIX. Narrado em primeira pessoa pela **Ana Luiza**. Leitora-alvo:
doutora que comprou pela VSL e lê no celular, entre um paciente e outro.

**Arquivo:** `render/script-715.pdf`, 9:16 (1080×1920), feito pra tela de celular
e não pra papel.

**Estrutura:** capa, sumário, quatro partes com página-marcador, doze capítulos,
três anexos e contracapa com o CTA. São 138 páginas, zero páginas órfãs.

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

**3. Linter de pontuação** (`revisor_pontuacao.py`). Fala reportada sem aspas, aspa
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

**2. Amostras ESCRITAS da Ana.** Mensagem, e-mail, post, qualquer coisa que ela
tenha digitado. Todo o fingerprint de voz hoje é FALA transcrita, e a passagem de
fala para papel ainda é inferência minha. Isto deixou de ser bloqueio quando a
substituição por fala real resolveu 13 dos 15 blocos, mas é o que fecharia o
resíduo dos dois que faltam.

O Slack não serve pra isso: o token do ambiente está morto (`account_inactive`) e
o do Keychain só tem `chat:write`, `channels:read` e `files:read`. Faltam
`users:read` e `channels:history` no app que já existe — é uma alteração de escopo
no app, não um app novo.

**3. Duas correções de pontuação dentro de card de script.** Estão em
`revisao-pontuacao.json`, campo `em_card`. Não apliquei porque frase de script vai
literal, e mexer nelas é decisão sua, não minha.

---

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
