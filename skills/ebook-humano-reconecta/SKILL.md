---
name: ebook-humano-reconecta
description: >-
  Escreve ebook (ou qualquer prosa longa: capítulo, apostila, manual, carta de vendas longa)
  a partir de transcrição de aula, PDFs de apoio e amostras reais de quem assina, sem sotaque
  de IA em português do Brasil. Pipeline guiado em 4 fases (fontes → fingerprint da voz → mapa
  de capítulos → capítulo a capítulo) com portão determinístico (detector_ptbr.py), loop de
  revisão por agentes especialistas (editor, fiscal de fidelidade, leitora-alvo, guardião de voz)
  e um CÉTICO por achado que tenta refutar, mais um detector cego que só recebe o texto.
  Compila em PDF na identidade RECONECTA. Acionar em "escreve o ebook", "capítulo do livro",
  "transforma essa aula em texto", "tá com cara de IA", "revisa esse capítulo", "humaniza",
  "compila o PDF do ebook". Compõe com escrita-humana-reconecta (que é a régua curta) e
  reconecta-copywriting (argumento). Esta aqui é o pipeline inteiro pra texto LONGO.
---

# ebook-humano-reconecta

Livro que soa de gente sai de três coisas: fonte real (nada inventado), voz real (fingerprint
de quem assina, com whitelist dos hábitos dela) e revisão adversarial (quem acusa não é quem
confirma). A skill é esse pipeline. O detector automático é só o primeiro portão; o cético
continua obrigatório mesmo com detector zerado, porque padrão de superfície não pega
argumento genérico nem voz achatada.

## Arquivos desta skill

- `referencias/catalogo-tells-ptbr.md`: o catálogo de maneirismos de IA em PT-BR, por família,
  com exemplo, conserto e guarda de falso positivo. Inclui vocabulário em 3 níveis e a família
  de CALQUES DO INGLÊS (a lacuna que nenhuma skill pública cobre).
- `referencias/mapa-de-fontes.md`: de onde veio cada coisa (blader/humanizer, jooray/humanizer,
  conorbronsdon/avoid-ai-writing, luquiluke/claude-book-skill, gregorymm/humanize-text,
  ThomasHoussin/Claude-Book, Wikipedia "Signs of AI writing"). Clones em `refs/`.
- `scripts/detector_ptbr.py` + `scripts/padroes_ptbr.json`: portão determinístico, nota 0-100.
- `scripts/wf_revisao_capitulo.js`: o loop de revisão por agentes (Workflow tool).
- `scripts/render_pdf.py` + `scripts/template.html`: compila markdown → PDF A4 escuro, tokens
  do `design-system/core/tokens.json`, fontes Dx Monstral / Grift / Inter.
- `agentes/briefs.md`: papel e regras de cada agente, pra ler antes de rodar o workflow.

## Estrutura do projeto de um livro

```
ebooks/<slug>/
  fontes/            transcricao/*.txt|srt, pdf/*.pdf + *.md extraído, voz/amostras + fingerprint-<autor>.md
  mapa-de-capitulos.md          checkpoint 1 (usuário aprova antes de escrever)
  manuscrito/NN-slug.md         um capítulo por arquivo, front matter com fontes usadas
  revisao/NN/rodada-K.json      saída do workflow por rodada (achados brutos, confirmados, detector cego)
  render/                       template, HTML gerado, PDF final, provas em PNG
```

## Fases (modo guiado: parar em cada checkpoint)

### Fase 0: fontes
Transcrição (WhisperX, ver memória `reference_whisperx_pipeline_vsl`) e PDFs (pypdf) viram
markdown em `fontes/`. Toda frase pronta, caso, número e nome que o livro usar precisa estar
aqui. O que não está aqui não entra. Placeholders da fonte ("Dra. Mariana", "Fulana") viram
"a doutora"/"ela" ou o nome real que a transcrição trouxer.

### Fase 1: fingerprint da voz (agente Bibliotecário)
Entrada: 1+ amostras reais de quem assina (fala transcrita serve; texto digitado é melhor).
Saída: `fontes/voz/fingerprint-<autor>.md` com números (tamanho de frase, conectores reais),
ritmo, vocabulário e imagens dela, posições dela, WHITELIST (hábitos dela que parecem tell
mas são dela e o editor NÃO pode cortar), guia fala → escrita, e um teste de calibração
(3 pares IA x pessoa) pro usuário validar. Sem amostra suficiente, dizer a lacuna, não inventar.

### Fase 2: mapa de capítulos (agente Arquiteto) → CHECKPOINT 1
Tabela: capítulo, o que entrega, fonte (arquivo e página). Esqueleto fixo dos capítulos
repetidos. Perguntas abertas pro usuário. Só escreve depois do "aprovado".

### Fase 3: capítulo a capítulo → CHECKPOINT por capítulo
1. Escritor redige `manuscrito/NN-slug.md` com fingerprint + fontes + catálogo na frente.
   Regras de escrita em `agentes/briefs.md`. Front matter lista as fontes usadas.
2. Portão 1: `python3 scripts/detector_ptbr.py manuscrito/NN-slug.md --json`. Meta: nota ≤ 25.
   Acima disso, o Escritor reescreve antes de gastar agente.
3. Loop de agentes: `Workflow({scriptPath: scripts/wf_revisao_capitulo.js, args: {...}})`.
   Revisores em paralelo (Editor de tells, Fiscal de fidelidade, Leitora-alvo, Guardião de voz),
   um cético por revisor julgando o lote (segundo cético só nas altas), Detector cego por fora.
   O cego recebe SEMPRE uma cópia sem front matter (`revisao/NN/capitulo-limpo.md`, arg
   `capitulo_limpo`): na rodada 2 do cap. 1 ele usou a linha `fontes:` do YAML como pista de
   pipeline. Rodadas focadas podem passar `revisores: ['tell','voz']` pra não pagar os 4. Só achado que
   sobrevive ao cético vira correção. O cético do Editor também pergunta: "essa correção
   achata a voz? fere a whitelist?" e pode devolver correção alternativa.
4. Corrigir na fonte (o .md), rodar detector de novo, rodar workflow focado (rodada K+1,
   passando `trechos_mudados`). Parar quando: 0 achados de gravidade alta confirmados,
   detector ≤ 25, Detector cego não diz "IA" com confiança ≥ 60.
5. Mostrar ao usuário: capítulo, resumo das rodadas (achados brutos → confirmados), nota do
   detector, veredito do cego. Esperar aprovação. Nunca seguir sozinho pro próximo.

### Fase 4: compilar
`python3 scripts/render_pdf.py ebooks/<slug>` gera HTML + PDF + PNG de prova por página.
Olhar as provas (memória `feedback_revisar_antes_preview`): texto cortado, órfãs, card
quebrado entre páginas, dois vermelhos na mesma página.

## Regras invioláveis

- Fidelidade: nada que não esteja em `fontes/`. Sem dado, sem caso, sem citação inventada
  (memória `feedback_nunca_inventar_dados`). Frase pronta de script é copiada literal.
- Voz: o fingerprint manda. Whitelist é intocável. Editor que "melhora" a voz está errando.
- Sem travessão (—) nem hífen entre palavras no meio de frase. Vírgula, ponto ou dois-pontos.
- Ênfase só por cor, mesmo peso, nunca itálico (leis do design system).
- Sempre "harmonização facial". Nunca "HOF", nunca "orofacial". Vocabulário proibido da marca
  em `reconecta-copywriting/referencias/banco-de-termos.md`.
- O inimigo é comum, nunca a doutora.
- Texto de gente anda em parágrafo. Lista só onde a estrutura pede (banco de perguntas, cola).
- Nada de "neste capítulo vamos", "em resumo", "vale ressaltar", fecho grandioso, pergunta
  retórica de encerramento. O catálogo tem a lista completa.

## Custo e teto

Medido em 07/09/2026, capítulo 1 do 715 (950 palavras), rodada 1 com um cético POR ACUSAÇÃO:
29 acusações → 36 agentes → 2,74 milhões de tokens em 7 min. Estourou o teto de 500k por 5x.
Correção na mesma sessão: cético POR REVISOR (julga o lote inteiro de acusações daquele revisor
de uma vez) e segundo cético só nas altas confirmadas → 4 revisores + 4 a 8 céticos + 1 cego
≈ 9 a 13 agentes. Cada revisor lê o catálogo inteiro (~16k palavras), então o piso por agente
é alto; não mandar o catálogo pro Fiscal nem pra Leitora (eles não precisam). Teto: 800k por
rodada; declarar antes, reportar depois (memória `feedback_modo_exaustivo_com_teto`). O
Workflow só roda com autorização explícita do usuário. Taxa de refutação observada: 38%
(11 de 29), menor que os 74-80% do motion: revisores de texto acusam com mais precisão.

## Portões numéricos (resumo)

> Régua completa e independente de modelo: `referencias/padrao-de-refinamento.md`.
> Pontuação e aspas: `referencias/ortotipografia-ptbr.md` (voz solta, escrita correta).
> Leia esse arquivo ANTES de aplicar qualquer correção, e SEMPRE que a sessão
> trocar de modelo (o júri herda o modelo da sessão; o arg `juri` fixa a régua).


| Portão | Meta |
|---|---|
| detector_ptbr.py | ≤ 25 por capítulo |
| Achados alta confirmados | 0 |
| Subtítulos (H2) num capítulo de caso | ≤ 2, nunca citando a primeira nem a última frase do bloco (aprendizado cap. 1) |
| Detector cego | não acusa IA com confiança ≥ 60 |
| Travessão no manuscrito | 0 (grep) |
| Fidelidade | 0 achados confirmados de conteúdo sem fonte |

## Aprendizados do 715 (07/09/2026)

- Capítulo de CASO (cap. 1): o erro foi estrutura por regra (6 subtítulos entregando a pancada
  antes dela). Cego passou de "IA 60" pra "pessoa" quando o caso correu inteiro até o carimbo.
- Capítulo PRESCRITIVO (cap. 2): o erro foi transpor bullets do manual em prosa "limpa": 3 "eu" em
  600 palavras, 10 contrastes "não X, Y", pares simétricos de aforismo, parágrafo do framework
  parafraseado. Cego deu "IA 75". Regra: cada princípio ganha (a) primeira pessoa como observação
  ("pelo que eu observo"), (b) uma pergunta-gancho a cada 2 ou 3 parágrafos ("Por quê? Porque"),
  (c) uma frase longa encadeada com "e aí" antes da pancada, (d) concessão de humildade colada na
  primeira prescrição, (e) contraste na dose do fingerprint (3 a 5 por 2.000 palavras), (f) nada
  de fecho de uma linha repetindo o parágrafo. Aviso "não é formato rígido" só UMA vez no livro.
- Fiscal pegou contradição interna: "a agenda acontece sem você pedir" x passo 7, onde quem atende
  oferece horário, pede PIX e comprovante. Checar toda prescrição contra a etapa do framework.

- Limite de sessão mata os céticos no meio da rodada (aconteceu na rodada 4 do cap. 2, 07/09 à
  noite): os revisores ficam em cache, então relançar com `resumeFromRunId` roda só o que faltou.
  Nunca aplicar acusação sem veredito do cético (`motivo: "sem veredito do cetico (falha)"`).

- A COSTURA é o tell (cap. 2, 6 rodadas, cego preso entre 65 e 78): transcrição literal na
  abertura + prosa composta no miolo = duas texturas, e o cego lê "reescritor por cima de
  transcrição". Todo ajuste de superfície (menos contraste, menos staccato, item torto de
  propósito, "tá?" dosado) moveu pouco. O que resolve é estrutural: (1) ou o capítulo inteiro é
  prosa composta na voz dela (adaptar o caso, não colar a transcrição), (2) ou existe amostra
  DIGITADA por ela pra calibrar o registro escrito (lacuna nº 1 do fingerprint). Sem (2), o
  portão do cego em capítulo prescritivo fica em "não acusa IA com ≥ 70" e a leitura humana
  do Sávio decide. Não gastar mais de 2 rodadas de cego em ajuste de superfície.

## Aprendizado contínuo

Achado confirmado que o catálogo não tinha → entra no catálogo e no `padroes_ptbr.json` na
mesma sessão. Falso positivo recorrente → vira guarda. Fim de sessão bom = skill atualizada.
