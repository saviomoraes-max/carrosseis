# Script 715 — briefing para a revisão humana

Você está recebendo um ebook pago pra revisar. Este documento existe por um motivo específico:
**o maior risco desta revisão é ela ser bem feita demais.** Boa parte do que parece erro aqui é
proposital, e uma passada de revisor competente mataria justamente o que faz o livro funcionar.

Leia estas quatro páginas antes de abrir o PDF. Depois disso, o texto é seu.

---

## 1. O que é o livro

| | |
| --- | --- |
| **Produto** | Ebook pago, vendido pela página da VSL |
| **Assunto** | Os sete passos do Script 715: atendimento no WhatsApp de clínica de harmonização facial, do primeiro "oi" ao comprovante do PIX |
| **Narradora** | Ana Luiza, fundadora da RECONECTA, em primeira pessoa |
| **Leitora** | Doutora de harmonização facial que comprou pela VSL e lê no celular, à noite, cansada |
| **Tamanho** | 16.600 palavras, 150 páginas, formato 9:16 (1080×1920), fundo escuro |
| **Estrutura** | 12 capítulos em 4 partes + 3 anexos (A: cola rápida, B: banco de perguntas, C: paciente modelo) |
| **Camada colável** | 52 frases prontas e 23 cartões de objeção — este é o produto de verdade |

**O arquivo pra revisar é `script-715.pdf`.** O texto-fonte, se você preferir revisar em texto
corrido, está em `script-715-texto-corrido.md`: é o livro inteiro num arquivo só, na ordem de
leitura, sem as marcações do compilador.

**Ele navega.** Abra os marcadores do PDF (o painel lateral) e você tem as quatro partes com os
quinze blocos aninhados. No sumário, cada linha leva à página do capítulo. Dentro do texto, toda
menção a "capítulo 11" ou "anexo A" é link. Nas páginas de parte, cada linha da lista é link. E
**cada um dos sete círculos do trilho é link pro capítulo daquele passo** — são 122 links internos,
todos conferidos um a um contra a página de destino.

Duas observações de arquivo, pra você não estranhar: o texto é selecionável e pesquisável, mas o
*chrome* com espaçamento de letra (kicker, cabeçalho, rodapé, rótulos dos cartões) sai da busca
como letra separada, `C A P Í T U L O  0 3` — é do espaçamento, vale pra qualquer leitor. E as
fontes de título e de corpo vêm do sistema e são desenhadas como vetor, então o PDF não carrega
arquivo de fonte licenciada dentro dele.

---

## 2. O que é DELIBERADO e não deve ser consertado

O livro foi construído a partir de **80.938 palavras de fala transcrita da Ana** em 20
treinamentos ao vivo sobre este exato assunto. A oralidade dela é o ativo do produto, não um
defeito a limpar. Leitores independentes que leram o texto sem saber de nada citaram exatamente
estes traços como prova de que foi gente que escreveu.

**Não corrija:**

- **Coloquialismo dela:** "pra", "tá", "né", "ó", "gente", "a gente", "só que", "agora, se", "aí".
- **Frase sem verbo, fragmento, frase começando com E, Mas ou Então.** É respiração de fala.
- **Anacoluto e regência de fala:** *"ajudar ela"*, *"fazer ela dizer"*, *"qual que é"*,
  *"mantém elas"*, *"se responde com pergunta"*. Ela fala assim.
- **Autocorreção deixada no texto:** *"ela volta na hora que ela quer. Ela acha que ela pode
  voltar na hora que ela quer."* Isso é ela se corrigindo em voz alta, e fica.
- **Repetição para martelar um ponto dentro do mesmo parágrafo.**
- **Grafia de interjeição variando entre capítulos** ("Humm..." num lugar, "Hmm," noutro).

Se você ficar em dúvida entre "erro" e "jeito dela falar", **é o jeito dela falar.**

**Três decisões do dono, já tomadas. Não são para reabrir:**

1. **`"vai te ajudar com o [problema] e parar de se sentir [x]"`** (cap 08, anexo A, anexo B).
   Lido ao pé da letra, quem para de se sentir mal é a doutora. **Cinco revisões automáticas
   independentes acharam isso.** A redação é literal do framework da metodologia (p.8), e a
   decisão registrada é manter a metodologia literal.
2. **`"desde [tempo]"`** na transição (cap 07 e anexo A). "Desde" pede marco e a paciente dá
   duração, então sai *"desde dois anos"*. Também é literal do framework (p.7). Mesma decisão.
   *(O anexo B traz `há [tempo informado]` porque segue o outro manual da casa, e os dois
   manuais divergem entre si. Isso é conhecido e é proposital.)*
3. **A saída do anexo C**, *"as vagas de paciente modelo desse mês já foram encerradas"*, dita
   para quem não passou na seleção. Contradiz a régua do próprio livro de dar sempre o motivo
   verdadeiro, **e é literal da transcrição da aula 5.1**, com a justificativa da própria autora
   ("sem falar assim, ah, você não foi selecionada"). Decisão do dono: manter.

Se você discordar de alguma das três, **escreva o argumento** — mas não aplique.

---

## 3. O que já foi checado, e com quê (não gaste tempo aqui)

Isto não é pra te impressionar, é pra você não refazer trabalho de máquina:

| O quê | Instrumento | Estado |
| --- | --- | --- |
| Aspas curvas abrindo e fechando | linter próprio | 221/221 duplas, 10/10 simples |
| Aspa reta no corpo | linter | zero (as 210 do arquivo estão no cabeçalho YAML, que não renderiza) |
| Travessão na prosa | linter | zero |
| Crase | corretor de língua | conferidas uma a uma |
| Vírgula, dois-pontos, maiúscula depois de ponto | linter | zero achado |
| Eco: mesma frase repetida no mesmo parágrafo | linter | zero |
| Remissões entre capítulos ("está no capítulo 11") | fiscal de continuidade | abertas uma a uma |
| Contagens declaradas ("são oito", "seis jeitos") | três lentes independentes | todas fecham |
| Numeração dos sete passos entre corpo, cola e anexos | fiscal de continuidade | idêntica |
| Grafia de marca (WhatsApp, PIX, Instagram) | guardião de consistência | 25/25, 25/25, 1/1 |
| "harmonização facial" nunca vira sigla | guardião | confirmado |
| Links internos do PDF (sumário e menções a capítulo) | conferência no PDF gerado | todos na página certa, conferidos destino a destino |
| As 150 páginas renderizadas, uma a uma | cinco revisores de prova gráfica, em paralelo | 13 defeitos achados e corrigidos |
| Camada colável PREENCHIDA e lida em voz alta | lente dedicada | 4 defeitos achados e corrigidos |
| Toda prescrição e todo número rastreados até a fonte | auditor de fidelidade | 2 prescrições sem fonte, cortadas |
| Página órfã (miolo com menos de 35% de ocupação) | o próprio render audita | zero |
| Bloco perdido entre o markdown e o PDF | o render conta e morre se perder | confere a cada compilação |
| "Isto foi escrito por pessoa ou por IA?" | 3 leitores cegos por bloco, sem contexto | 15 de 15 blocos lidos como pessoa |

O livro passou por **sete bancas completas** — seis examinadores lendo o livro inteiro de ponta
a ponta, um cético conferindo cada acusação e um relator fechando. A nota média subiu de 7,5
para 8,2. O rastro comparado está em `revisao/bancas-10set.md`.

---

### Uma auditoria de entrega rodou logo antes de você receber isto

Nove lentes independentes, com um cético conferindo cada acusação: **cinco leram as 150 páginas
renderizadas uma a uma**, e as outras quatro olharam fidelidade às fontes, a camada colável
preenchida, a estrutura e a completude do pacote. **Vinte e dois achados foram confirmados e
todos foram corrigidos** antes desta entrega. Os principais, pra você saber o que já não vai
achar:

- quatro frases prontas quebravam quando preenchidas de verdade (artigo fixo antes do colchete,
  dia da semana masculino num colchete que recebe dia feminino, cartão com duas entradas e uma
  resposta só, cartão que pergunta o dia e já usa o dia);
- narração da autora tinha vazado pra dentro de um balão rotulado "ELA MANDA";
- o `R$` se separava do valor na quebra de linha, dentro da frase que a leitora copia;
- um bloco gráfico partia entre páginas e deixava o quarto item sozinho no topo da seguinte;
- deixas terminando em dois-pontos ficavam no pé de uma página com o card que elas anunciam
  abrindo a página seguinte;
- duas prescrições do capítulo 12 não existiam em fonte nenhuma e foram cortadas.

O parecer inteiro está em `revisao/auditoria-entrega-parecer.md`.

## 4. Onde o seu tempo vale mais

É aqui que nenhuma máquina chega:

**A camada colável, lida em voz alta e preenchida.** As 52 frases prontas são o que a doutora
copia e manda pra uma paciente de verdade. Preencha os colchetes com um caso real e leia em voz
alta. É o único teste que importa e é o que mais rende.

**O ritmo da segunda metade.** A lente de repetição é a nota mais baixa do livro (7,0) em todas
as passadas. A anedota da salinha do financeiro volta em quatro capítulos, e nos do meio ela é
recontada em vez de referenciada. Nenhum cético confirmou que isso quebra o livro, mas nenhum
cético lê de uma sentada como a leitora lê.

**O fecho dos capítulos.** Os doze terminam numa pergunta sobre o que a leitora perdeu, e nenhum
dá uma tarefa pra amanhã de manhã. A instrução prática existe (nos capítulos de passo,
em "Quando avançar", e no anexo A), mas não no fecho. Mudar isso é reeditar doze fechos, então
ficou registrado como decisão editorial, não como erro. **É a sua opinião que decide.**

**A verdade dos casos, dos valores e das cenas.** Nenhuma lente tinha como checar. Se algum
número é ilustrativo, quem confirma é a casa.

**Conformidade.** Ninguém olhou o livro do ponto de vista de regra de publicidade ou de conselho
de classe. **O anexo C trata de vaga de paciente modelo, reserva e abatimento no valor do
procedimento.** Se isso precisa passar por advogado, precisa passar antes de vender.

---

## 5. Como devolver

Escreva a correção com o **trecho exato** que você quer trocar e o **texto novo inteiro**, não
uma instrução. Duas regras de ortotipografia da casa:

- **Nunca travessão (—)** e nunca hífen no meio de frase. Use vírgula ou ponto.
- **Nunca itálico.** A ênfase do livro é só cor, aplicada no compilador com `«palavra»`.

Se a sua correção mexer numa lista, numa contagem ou na ordem dos passos, avise: existem
contagens declaradas no corpo do texto que dependem do tamanho das listas, e elas precisam ser
reconferidas depois.

---

*Documento gerado em 10/set/2026. O estado técnico completo está em `ESTADO.md`; o que depende
de decisão do dono está em `relatorio-de-entrega.md`.*
