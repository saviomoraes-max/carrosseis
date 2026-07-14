# Portão de Qualidade — Agente de Carrosséis RECONECTA

> **Antes do portão:** o modelo produtor roda o `checklist-producao.md` DURANTE a escrita (self-check com evidência, seção por seção). O portão é o juiz final; o checklist é o que faz chegar aqui limpo.
> O agente roda esta autocrítica contra TODO carrossel antes de entregar pro humano.
> **Só passa o que cruza A→E inteiro.** Tudo é pass/fail binário com evidência obrigatória — sem zona cinza, sem "passou, mas...".
> O que falha vira **diff focado no slide específico**, nunca sumiço silencioso nem reescrita do carrossel inteiro.
> Fontes da régua: `voice-spec.md` (performance), `relevance-filter.json`, `headlines-repertoire.json`, e as memórias de regra (sem travessão, sem dado inventado, CTA sem handle).

---

## BLOCO A — Gates de zero-achismo *(falha dura: reprova na hora)*

- [ ] **A1 · Headline ancorada.** A capa aplica uma técnica que existe no `headlines-repertoire.json`, e o campo `tecnica_aplicada` aponta a entrada + a URL de origem. *Evidência: id da técnica + URL.* Sem isso → reprova.
- [ ] **A2 · Tema vetado.** O tema passou pelo `relevance-filter.json` (gate aprovado) e carrega o registro `por_que_relevante`. *Evidência: pontuação da rubrica + a dor/desejo que conecta.* Tema sem passagem registrada → reprova.
- [ ] **A3 · Sem afirmação inventada.** Todo número, caso, nome e estatística está ancorado em (dado real / copy antiga / fonte) OU é demonstrado via processo. *Evidência: a âncora de cada afirmação factual.* Qualquer dado solto → reprova.
- [ ] **A4 · Sem adaptação na marra.** Se a tendência só encaixou torcendo o sentido, ela foi DESCARTADA, não forçada. *Evidência: o log do filtro não marcou "distorção".*
- [ ] **A5 · Passo ensinado existe na metodologia.** Todo passo tático de slide de entrega (regra, framework, vocabulário de consulta) tem âncora na metodologia REAL (corpus/copy antiga dela/material da mentoria) — nunca inventado por analogia, por mais plausível que soe. *Evidência: onde o passo aparece na fonte.* (Caso 02/jul: "aposente a palavra alta" era invenção → o usuário reprovou; o passo real era "Proximidade Digital Silenciosa", SEM19/AD003 dela.)

## BLOCO B — Conformidade com a spec de voz *(peso no que funcionou)*

- [ ] **B1 · Gancho que venceu.** A capa usa um padrão marcado `venceu` na spec (pergunta-paradoxo ou número/lista), não um `só existiu` (analogia-celebridade) nem só `mediano` sem razão. *Evidência: o padrão + seu veredito.*
- [ ] **B2 · Tema priorizado.** O tema é `aumentar`/`manter` na spec. Se for `reduzir` (objeção-preço pura, autoridade-celebridade), só passa com ângulo comprovadamente novo. *Evidência: veredito do tema + justificativa se for "reduzir".*
- [ ] **B3 · Estrutura validada.** Segue um dos esqueletos `venceu` (antes/depois→SUPERCASO, tático-WhatsApp/objeção-script, indicação-na-sala) ou um híbrido justificado.
- [ ] **B4 · Léxico e dial.** Vocabulário proibido = zero. Dial de postura + gíria leve no registro doutora (validado no SEM27/AD002), não gíria gen-g pesada nem corporativo frio.
- [ ] **B5 · Voz não-robótica (dispositivos do `voice-dna.md`).** O carrossel aplica os dispositivos reais dela: **≥1 frase pronta exata** por slide de entrega (aspas, colável), **≥1 contraste seco** (one-liner disruptivo), **≥1 detalhe concreto inesperado** (hora/número/objeto), **número de capa escalado** (3,5,7 não redondo), e **encena a cena** em vez de explicar o conceito. *Evidência: citar a frase pronta + o contraste + o detalhe.* Se ler como "IA descrevendo um conceito" (abstrato, genérico, sem fala literal) → **reprova**. É o gate que separa "âncora certa" de "soa como ela".

## BLOCO C — Estrutura e 4 camadas *(herdado do revisor-copy)*

- [ ] **C1 · 1 ideia por slide** (não duas).
- [ ] **C2 · Slides de entrega têm as 4 camadas:** ação concreta + mecanismo (cadeia causal) + exemplo vivo (frase pronta/vignette) + frame conceitual.
- [ ] **C3 · Cada slide intermediário puxa o próximo** (gancho explícito).
- [ ] **C4 · Legibilidade:** corpo dentro do piso (≥30), respiro, sem encolher texto pra caber copy.

## BLOCO D — Continuidade narrativa

- [ ] **D1 · A promessa da capa é entregue** nos slides de entrega.
- [ ] **D2 · Sem repetição de ideia** entre slides vizinhos.
- [ ] **D3 · A prova social conecta** semanticamente com a entrega central (não é prova solta).

## BLOCO E — CTA e distribuição

- [ ] **E1 · CTA segue o padrão.** O último slide usa **"TOQUE NO LINK DA BIO"** (padrão decidido em 30/jun: o link leva a evento/oferta). Exceção por campanha: posts com objetivo de comentário/DM podem usar SUPERCASO.
- [ ] **E2 · A LEGENDA puxa salvar + SEND, na voz dela, com CTA de link na bio humano.** Entregue SEMPRE junto com o post. Roda o MESMO filtro do BLOCO B5 (voice-dna) — a legenda não pode soar como IA (frase pronta / contraste / detalhe concreto, ENCENA não EXPLICA). Pede salvar e mandar pra uma colega ("sends per reach" é o sinal nº1) E fecha com **CTA de LINK NA BIO que ESPELHA o CTA do último card** (o do Figma), em prosa — não pode ser paráfrase torta nem um "clique agora" robótico. *Evidência: o CTA da legenda bate com o do card.* **Formato:** as linhas em branco entre parágrafos levam o caractere invisível U+2800 ("⠀") sozinho na linha (senão o Instagram engole a quebra); existe `legenda.txt` na pasta pronto pra colar. **Anti-eco:** a legenda NÃO repete frase/cena dos slides — comparar literal parágrafo a parágrafo; reciclagem de corpo de slide = reprova (caso 07/jul, AD012). Sem qualquer um desses → reprova.
- [ ] **E3 · Sem handle no slide.** O CTA não exibe @handles.
> Tradeoff consciente: a pesquisa 2026 favorece SUPERCASO+SEND no slide; o usuário optou por link-na-bio por razão de negócio. A régua de alcance migra pra legenda.

## BLOCO F — Layout do render *(checar nos PNGs, não na copy)*

- [ ] **F1 · Gap 32px uniforme.** O espaçamento entre todos os elementos (título→corpo, corpo→corpo, entre itens, punch→prints) parece parelho (~32px). Sem gaps gigantes ou minúsculos. *Evidência: o slide.*
- [ ] **F2 · Centralização vertical.** Slides de fundo (text/list/proof/cta) com o bloco de conteúdo centrado na vertical (respiro em cima ≈ embaixo). Slides de foto (hero/photo) com texto ancorado embaixo. Sem conteúdo colado no topo nem caindo embaixo.
- [ ] **F3 · Zero overlap.** Nenhum elemento sobrepõe outro. No proof, o título NÃO encosta nos cards de depoimento.
- [ ] **F4 · Zero corte de borda.** Nada vaza, corta ou encosta nas bordas. Corpo legível (≥30), nunca apertado pra caber copy.
- [ ] **F5 · Zero overflow (cabe na faixa).** Nenhum slide passa da faixa segura (~1090px). *Evidência: o arquivo `slides/_overflow.json` NÃO existe (o engine grava ele + imprime `⚠ OVERFLOW` quando o conteúdo não cabe).* Se existir → **reprova**: encurtar a copy do slide apontado (lista típica = 4 itens com body longo → cortar pra body de 1-2 linhas; a camada longa migra pro text/photo). **NUNCA encolher fonte pra caber** — a trava é a copy. Re-renderiza e confere que `_overflow.json` sumiu.
> Regra do usuário (30/jun). O engine já força F1-F4 por construção (`GAP=32`, `.center-wrap` na faixa segura `SAFE_V`, `.prints-block`) e DETECTA F5 (mede altura natural vs faixa, grava marcador). F é a rede de segurança visual. Ver `design-spec.md` → "Espaçamento & distribuição vertical".

---

## Protocolo de saída

**APROVADO (A→E todos pass):** entrega pro humano com um cabeçalho de 1 linha por bloco ("por que passou") + as fontes anexadas (URL da headline, dor que o tema conecta, âncora dos dados). A revisão do humano vira "confiro as âncoras", não "reescrevo".

**REPROVADO (qualquer item fail):** NÃO entrega. Gera um relatório apontando o slide + o critério + um **diff focado** + o porquê. Re-roda o portão após o ajuste. Nunca reescreve o carrossel inteiro por causa de 1 camada faltando.

## Anti-padrões do próprio portão
- Marcar pass sem evidência → o checklist vira teatro.
- Aprovar com ressalva ("passou, mas...") → é pass ou fail.
- Silenciar um corte ("cobri tudo") quando na verdade limitou cobertura → sempre logar o que ficou de fora.
