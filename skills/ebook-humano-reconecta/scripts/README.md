# detector_ptbr: portão de sotaque de IA em PT-BR

Detector determinístico (regex + estatística, só stdlib) que dá nota 0-100 de "sotaque de IA"
a um texto em português do Brasil. É o Portão 1 do pipeline de ebook: roda antes de gastar
agente. Porte adaptado de `refs/conorbronsdon_avoid-ai-writing/detector/patterns.js`, mais os
10 tells de `escrita-humana-reconecta` e uma categoria própria de calques do inglês.

## Rodar

```bash
python3 scripts/detector_ptbr.py manuscrito/03-slug.md            # relatório legível
python3 scripts/detector_ptbr.py manuscrito/03-slug.md --json     # pra outro agente consumir
python3 scripts/detector_ptbr.py cap.md --min-gravidade alta      # oculta achados menores (score não muda)
python3 scripts/detector_ptbr.py cap.md --limite 25               # sai com código 2 se passar de 25
cat cap.md | python3 scripts/detector_ptbr.py -                   # lê da entrada padrão
bash scripts/testes/rodar_testes.sh                               # suíte: ia_tipico > 60, humano < 25, misto 25..60
```

Sem pip. Python 3.8+.

## O que o score significa

| Faixa | Leitura | O que fazer |
|---|---|---|
| 0 a 15 | limpo, soa gente | segue pro loop de agentes |
| 16 a 25 | leve sotaque | passa no portão (meta do ebook: 25 ou menos por capítulo) |
| 26 a 45 | sotaque perceptível | o Escritor conserta os achados antes de gastar agente |
| 46 a 65 | sotaque forte | reescrever os trechos marcados |
| 66 a 100 | carregado | reescrever do zero |

Como é calculado (também no cabeçalho do `.py`):

1. Cada achado tem um peso pela gravidade: baixa 1, média 2.5, alta 5, crítica 10. Métricas
   estatísticas têm peso próprio (`metricas` no JSON).
2. Mesmo padrão com o mesmo texto repetido: a primeira vale peso cheio, as seguintes valem
   0.4 do peso, e a soma de um padrão nunca passa de 20. É a deduplicação do original, só que
   sem zerar a repetição (em PT-BR a repetição É o tell).
3. `densidade = pontos / max(palavras, 300) * 1000`. O original divide por `log2(palavras/50)`;
   aqui é densidade porque capítulo de ebook tem 1.500 a 5.000 palavras e o log2 achatava texto
   longo. O piso de 300 palavras impede que um box curto vire 50 por causa de um achado só.
4. `score = 100 * (1 - exp(-densidade / 50))`. Densidade 15 dá 26; 50 dá 63; 115 dá 90.
   Nota por categoria usa a mesma curva com k = 15 sobre a densidade só daquela categoria.

Referência: a fala transcrita da Ana Luiza (`testes/humano.md`, 800 palavras) pontua 5. Um
capítulo de 2.000 palavras com uns 5 "é importante destacar" e nada mais já bate 25.

## Categorias

- `conteudo`: atribuição vaga, inflação, fecho grandioso, hedging, concessão falsa, template.
- `linguagem`: vocabulário nível 1 (sempre), nível 2 (2+ no mesmo parágrafo), nível 3
  (só por densidade), transições automáticas.
- `estrutura`: contraste "não é X, é Y", anáfora, tríade, lista, negrito, travessão,
  dois-pontos, pergunta retórica no fecho.
- `comunicacao`: sobras de chatbot ("neste capítulo vamos", "espero que ajude",
  "certifique-se de"), placeholders, disclaimers de IA.
- `meta`: estatística do texto inteiro (desvio-padrão do tamanho das frases, parágrafos do
  mesmo tamanho, cadência igual entre parágrafos, pontuação uniforme, diversidade lexical).
- `calques`: tradução literal de inglês corporativo, gerundismo, burocratês (utilizar,
  possuir, bem como, uma vez que, no que tange).

## Guardas de falso positivo

Ignorados na varredura de prosa (índices preservados, então linha e trecho batem com o
arquivo): front matter YAML, blocos e spans de código, comentários HTML, tabelas markdown,
blockquotes, URLs, citações entre aspas com 5 ou mais palavras (fala transcrita, print de
WhatsApp, frase pronta de script) e títulos de até 8 palavras. Os padrões de título rodam
numa cópia só com os títulos.

## Limites conhecidos

- Só vê padrão de superfície. Não lê argumento, não sabe se o caso é inventado, não sabe se a
  voz é da autora. O cético humano ou por agente continua obrigatório; o detector é pista.
- Regex não entende contexto: "abordagem" clínica e "abordagem" corporativa caem no mesmo
  filtro. Por isso nível 2 só marca em cluster e nível 3 só por densidade. Ainda assim, um
  achado isolado de nível 1 pode ser uso legítimo; a whitelist do fingerprint decide.
- As métricas estatísticas precisam de volume (8+ frases, 4-5+ parágrafos, 500+ tokens pro
  TTR). Em texto curto elas ficam mudas, e o score de texto com menos de 40 palavras é 0
  com aviso.
- Fala transcrita tem tique próprio (reticência, "E aí", pergunta retórica). Os limiares
  foram calibrados pra não acusar a amostra da Ana, mas outro locutor pode disparar anáfora
  ou pergunta-no-fecho. Achado de gravidade baixa em transcrição é quase sempre ruído.
- Não foi validado contra um corpus rotulado. Os pesos vieram do original em inglês e de
  ajuste manual nos três testes. Toda semana de uso deve devolver falso positivo pra guarda e
  tell novo pro catálogo.

## Como adicionar um padrão

Tudo vive em `padroes_ptbr.json`. Sem tocar no `.py`.

Padrão de frase: acrescente um objeto em `padroes`:

```json
{ "id": "cq_exemplo", "categoria": "calques", "subtipo": "calque", "gravidade": "media",
  "regex": "\\bexemplo\\s+de\\s+calque\\b", "explicacao": "Por que é tell.",
  "substituto": "O que escrever no lugar." }
```

Campos: `id` único (prefixo por família: `tr_` transição, `cq_` calque, `cb_` chatbot, `ct_`
conteúdo, `es_` estrutura); `categoria` uma das seis; `gravidade` baixa/media/alta/critica;
`regex` em sintaxe Python, case-insensitive por padrão (`"flags": "m"` liga multiline; `\\b`
funciona com acento); opcional `"escopo": "titulos"` pra rodar só nos títulos.

Vocabulário: acrescente em `vocabulario.nivel1|nivel2|nivel3` um objeto com `id`, `termo`,
`regex` e `substituto`. Nível 1 sempre marca (alta); nível 2 só com 2+ termos distintos no
mesmo parágrafo (média); nível 3 só por densidade (baixa; limiares em `regras_vocabulario`).

Métrica nova precisa de código: escreva a função em `rodar_metricas` e ponha os limiares num
bloco novo de `metricas` no JSON, pra ficar ajustável sem mexer no código.

Depois de qualquer mudança: `bash scripts/testes/rodar_testes.sh`. Se a amostra humana subir,
o problema é o peso, não o texto.
