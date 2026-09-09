# Paridade de júri — Fable → Opus (08/set/2026)

Teste feito quando a sessão trocou de modelo no meio do livro. Método em
`skills/ebook-humano-reconecta/referencias/padrao-de-refinamento.md`, seção 3.

## Montagem

Alvo: capítulo 1, `A salinha do financeiro`. Escolhido por ser o único capítulo
aprovado pelo Sávio e por estar congelado em `revisao/01/capitulo-APROVADO-v5.md`.
Antes de rodar, conferi que a prosa do manuscrito estava **byte a byte igual** à
que ele aprovou (os blocos de gráfico e de pergunta entraram depois e são
descontados no `capitulo-limpo.md`).

Fontes, fingerprint, catálogo, mapa e prompt: idênticos aos das rodadas Fable.
Única variável trocada: o modelo dos revisores, dos céticos e do leitor cego.

## Resultado

| | Júri Fable (rodadas 3 e 4) | Júri Opus (rodada 5) |
| --- | --- | --- |
| Achados brutos | 16 e 7 | 23 |
| Confirmados pelo cético | 5 e 2 | 6 |
| **Gravidade alta confirmada** | 1 e **0** | **2** |
| Leitor cego | pessoa 65 / pessoa 60 | não rodou (limite de sessão) |

## Veredito: a régua não derivou, ela ficou mais afiada na fidelidade

As duas altas do júri Opus são o mesmo defeito, e ele é **verdadeiro**. Conferi
na fonte, linha por linha, sem confiar no agente:

1. A Ana, na amostra A1, **só faz a pergunta** ("Na sua clínica, você tem a
   salinha do fechamento ou a salinha do pagamento."). Ela nunca define os dois
   termos. O capítulo definia os dois, como se fosse doutrina da casa.
2. Pior: a fonte diz "pode ser que a transação mesmo, **o fechamento** fique do
   lado de fora da sala". O capítulo escrevia "**o pagamento** mesmo fique do
   lado de fora", trocando a palavra dela para encaixar na taxonomia inventada.
   Isso inverte a concessão: na fala dela o fechamento fora da sala é concedido;
   no capítulo "fechamento" virou o rótulo do lado errado.
3. A frase "E aqui eu não estou falando que existe um certo ou errado", que é
   hábito confirmado dela (3 de 3 amostras) e está na fonte a doze linhas de
   distância, tinha sido cortada exatamente desse parágrafo.
4. O quadro de duas colunas que eu acrescentei em 08/set fixava a invenção em
   formato de tabela, que é o formato que mais parece regra.

Ou seja: o júri Fable passou quatro rodadas por cima de uma quebra de fidelidade
real, e o júri Opus achou. Não é rigor estético a mais, é verdadeiro positivo.

## Decisão

- **Seguir com o júri Opus**, sem fixar `juri: "fable"`.
- **Reabrir o capítulo 1**, mesmo aprovado. A instrução do Sávio de 08/set
  ("não invente nada, use apenas o que está na metodologia e nos PDFs") é mais
  nova e mais específica que a aprovação, e é exatamente o que foi violado.
- **Auditar o livro inteiro** procurando o mesmo tipo de defeito: definição,
  doutrina, política ou relação de causa que nenhuma fonte sustenta. Se
  sobreviveu quatro rodadas no capítulo mais revisado, sobrevive nos outros.

## Aplicado no capítulo 1 (v6)

Definições inventadas fora; palavra dela devolvida ("o fechamento"); concessão
"não tô falando que existe um certo ou errado" devolvida; quadro de duas colunas
removido; quadro da linha do tempo passou a mostrar a temperatura dela com as
palavras dela; inversão "tarde demais / cedo demais" nomeada; termo "salinha do
WhatsApp" agora é definido colado, como ela faz. Detector seguiu em 5.
Versão anterior guardada em `revisao/01/capitulo-v5-com-invencao.md`.
