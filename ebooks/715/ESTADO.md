# Script 715 — estado do projeto

Ponto de retomada técnica. Quem pegar isto sem contexto nenhum consegue continuar.
Atualizado em 09/set/2026, depois da rodada de corpus.

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
  render/script-715.pdf    143 páginas, 9:16 (1080×1920)
  render/provas/*.png      uma PNG por página
  render/cola/*.png        a cola dos 7 passos como peça de celular (cola_png.py)
  render/preview.html      abrir no browser pra folhear
  render/indice-paginas.json  em que página começa cada bloco
```

Scripts em `~/.claude/skills/ebook-humano-reconecta/scripts/`, com espelho
versionado em `~/reconecta/skills/ebook-humano-reconecta/` (a skill viva é a de
`~/.claude`; ver `ESPELHO.md` pra ressincronizar):
`render_pdf.py`, `detector_ptbr.py`, `andamento.py`, `graficos.py`, `cola_png.py`,
`revisor_pontuacao.py`, `wf_revisao_capitulo.js`, `wf_corpus_fala.js`, `wf_cego.js`,
`coleta_slack_autor.py`.

**O detector agora exige `--corpus`.** Sem ele acusa como vocabulário de IA palavras
que são da autora. Ver a descoberta 7.

Réguas em `referencias/`: `padrao-de-refinamento.md` (a mais importante),
`ortotipografia-ptbr.md`, `catalogo-tells-ptbr.md`.

---

## Estado bloco a bloco

| Bloco | Detector | Cego | Degraus |
| --- | --- | --- | --- |
| 01 | 0 | pessoa 68 | 3/3 |
| 02 | 23 | pessoa 67 | 3/3 |
| 03 | 12 | pessoa 78 | 3/3 |
| 04 | 11 | pessoa 74 | 3/3 |
| 05 | 13 | pessoa 69 | 3/3 |
| 06 | 12 | pessoa 71 | 3/3 |
| 07 | 0 | pessoa 68 | 3/3 |
| 08 | 18 | pessoa 60 | 3/3 |
| 09 | 14 | pessoa 73 | 3/3 |
| 10 | 9 | pessoa 85 | 3/3 |
| 11 | 22 | pessoa 72 | 3/3 |
| 12 | 0 | pessoa 68 | 3/3 |
| A | 28* | pessoa 73 | 2/2 |
| B | 33* | pessoa 84 | 2/2 |
| C | 17 | pessoa 72 | 3/3 |

Detector medido **com `--corpus`**, que é a régua do portão desde 09/set. Cego: três
leitores independentes por bloco, decisão por maioria.

`*` = amostra pequena (menos de 300 palavras de prosa), fora do portão.

**Todos os blocos avaliáveis passam no portão do detector.** A e B ficam fora dele por
amostra pequena (264 e 119 palavras de prosa), e o único achado de cada um é o formato da
peça: tríade na cola, lista no banco de perguntas.

**O 11 saiu de 40 pra 22 sem trocar uma palavra**, convertendo o andaime de catálogo em
bloco `:::caso`. A conversão foi provada neutra por contagem: 0 palavra perdida, 0 inventada.

**Diagramação:** 143 páginas em 4 partes, com contracapa. **34 gráficos vetoriais em 15 tipos**, e todo bloco tem pelo menos um, **zero páginas órfãs** (o render audita isso sozinho e denuncia página de miolo abaixo de 35% de ocupação). Dois bugs do paginador
corrigidos em 09/set: lista numerada era bloco indivisível (agora quebra entre
páginas, com `start=` continuando a numeração) e o balanceamento da última página
do capítulo media `scrollHeight`, que nunca fica menor que a caixa porque
`.conteudo` tem altura fixa com `overflow:hidden` (agora mede o último filho).

**Ortotipografia:** 205 pares de aspas curvas fechando, zero aspa reta no corpo,
zero travessão, aspas simples só dentro de duplas.

---

## As oito descobertas que mudaram o projeto

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

8. **Cético de um bloco não vê os outros.** Numa rodada de seis blocos em paralelo,
   três achados confirmados colidiram: garimpeiros diferentes acharam a MESMA
   passagem do corpus e a puseram em capítulos diferentes. O livro ficou com a mesma
   anedota da Ana em dois capítulos seguidos. Toda rodada multi-bloco agora termina
   com varredura de colisão antes de aplicar.

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
- **Sem assinatura de autora.** Capa e rodapé levam só Reconecta (decisão do Sávio em
  10/set). A narração em primeira pessoa continua sendo a da Ana; o que saiu foi a
  assinatura, não a voz. `livro.json` sem a chave `autor` já omite o bloco na capa.

---

## O que falta

**Depende do Sávio:**
- **Licença das fontes TT Modernoir.** É o único bloqueio de lançamento. O PDF está usando
  `TT_Modernoir_Trial_Bold.ttf`.
- **Amostras ESCRITAS da Ana** (mensagem, e-mail, post). Todo o fingerprint é FALA. Não é
  mais bloqueio (a substituição por fala resolveu o cego em 13 dos 15 blocos), mas é o que
  fecharia o resíduo. O Slack não serve: o token do ambiente está morto (`account_inactive`)
  e o do Keychain (`reconecta-slack`) só tem `chat:write`, `channels:read` e `files:read`.
  Faltam `users:read` e `channels:history` no app que já existe.
- Aprovar as duas correções de pontuação que caíram dentro de card de script
  (`revisao-pontuacao.json`, campo `em_card`).

**Não depende de ninguém, e nada disso é bloqueio:**
- `ideias-de-leitura.md` tem as propostas que sobraram, com o custo de cada uma. As três que
  não dependem de fonte nova: anexo B indexado "pelo que ela disse", glossário e carimbos
  tipográficos. O glossário é o mais arriscado: definição inventada já passou por quatro
  rodadas neste livro uma vez (`paridade-de-juri.md`), então só entra com verbete literal.

## Como retomar

```bash
P=~/reconecta/ebooks/715
S=~/.claude/skills/ebook-humano-reconecta/scripts
python3 $S/andamento.py $P --detalhe      # onde estamos
python3 $S/detector_ptbr.py $P/revisao/11/capitulo-limpo.md   # um bloco
python3 $S/revisor_pontuacao.py $P        # pontuação
python3 $S/render_pdf.py $P --provas      # PDF + PNGs + abre o preview
```

Regra que vale mais que todas: **achado só vira correção com veredito de
cético**. Achado marcado `"sem veredito do cetico (falha)"` significa que o
agente morreu, não que a acusação seja boa. Nunca aplicar.
