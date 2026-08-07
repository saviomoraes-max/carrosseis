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

## BLOCO B-6 · COMPETITIVIDADE — "limpo ≠ bom" *(novo, 28/jul — o gate anti-morno)*

> Motivo: o portão até aqui só reprovava DEFEITO nomeável. Copy correta e morna passava
> em tudo. Este bloco compara com os CAMPEÕES, não com as regras.

- [ ] **B6.1 · Punch a punch contra o top vigente.** Cada punch de S2-S6 é lido AO LADO
  dos 3 melhores punches do top-8 maduro (`data/pautas/SEM{xx}.md` traz a lista viva) e
  responde: numa disputa cega, este punch perde FEIO pra algum deles? Perde feio =
  APROVADO-MORNO → volta pro produtor com pedido de 2 candidatos novos por mecanismo
  diferente (`gabarito-punchline.md`). *Evidência: o par comparado + veredito por punch.*
- [ ] **B6.2 · Teste do corredor.** A doutora repetiria este punch DE CABEÇA pra sócia
  no corredor, hoje, sem errar? Punch que não se repete de cabeça não compartilha.
- [ ] **B6.3 · Seleção provada.** O produtor mostrou os candidatos MORTOS de cada punch
  (procedimento do gabarito: 5 candidatos, 1 sobrevive). Punch de primeira tentativa
  sem seleção registrada = devolver, mesmo que bom (o processo é o produto).

## BLOCO C — Estrutura e 4 camadas *(herdado do revisor-copy)*

- [ ] **C1 · 1 ideia por slide** (não duas).
- [ ] **C2 · Slides de entrega têm as 4 camadas:** ação concreta + mecanismo (cadeia causal) + exemplo vivo (frase pronta/vignette) + frame conceitual.
- [ ] **C3 · Cada slide intermediário puxa o próximo** (gancho explícito).
- [ ] **C4 · Legibilidade:** corpo dentro do piso (≥30), respiro, sem encolher texto pra caber copy.
- [ ] **C5 · SENTIDO LITERAL — leitura fria linha a linha *(novo, 29/jul; falha dura na capa)*.** Antes de qualquer análise de eco/voz/território, ler CADA linha de punch, headline e frase pronta **isolada**, como quem tem zero contexto e 2 segundos. A linha se sustenta sozinha? Falta palavra? **Elipse sem verbo reprova** ("nunca mais", "e pronto", "e já era", "e olhe lá"). *Evidência: a leitura isolada de cada linha da capa + veredito.* *Caso real: a capa "«Isso é só na avaliação.» «Agenda pelo link.» E A LEAD, NUNCA MAIS." passou por 59 agentes deste portão porque nenhuma dimensão perguntava se a frase FECHA — o Sávio pegou no preview ("nunca mais O QUÊ? erro grotesco"). Todo portão novo carrega uma dimensão de SENTIDO, e ela roda ANTES das outras.*

## BLOCO D — Continuidade narrativa

- [ ] **D1 · A promessa da capa é entregue** nos slides de entrega.
- [ ] **D2 · Sem repetição de ideia** entre slides vizinhos.
- [ ] **D3 · A prova social conecta** semanticamente com a entrega central (não é prova solta). **E o punch não é o eco do print:** se o print é uma frase só, o punch ARGUMENTA e o print PROVA — punch repetindo o print palavra por palavra vira gagueira e queima o slide. *Caso real 30/jul (SEM31/AD006): print "Passando de uma consulta de 80 reais para uma consulta de 250,00" com punch citando exatamente isso; virou "A CONSULTA NÃO MUDOU. MUDOU O QUE ELA DIZ QUE A CONSULTA VALE."* Quando o print é longo, aí sim o punch comprime (é o padrão dos outros: pull-quote das 3 batidas fortes).

- [ ] **D5.0 · DOUTRINA FIXA (PARE — ler `doutrina-fixa.md` ANTES do resto do D5).** Esse arquivo é o que a metodologia ENSINA, dito pelo Sávio; o `doutrina.json` é só o que os posts já disseram (e pode conter erro publicado). **Em conflito, a doutrina-fixa vence.** Contradizer o que está lá é reprova dura — não é adjacência declarável, é erro de conteúdo. Hoje ela cobre: (1) o registro profissional FICA na bio, a linha de posicionamento se SOMA a ele, nunca substitui; (2) "educativo"/"educação" como rótulo cru colide com a doutrina de que paciente super-informada fecha com a concorrência — se usar, qualificar no próprio rótulo. *Evidência: citar a seção da doutrina-fixa que o post toca e por que não a contradiz.*

- [ ] **D5 · COERÊNCIA DE DOUTRINA — o post não pode CONTRADIZER post anterior *(novo, 30/jul; pedido do Sávio: "vamos tomar cuidado pra a gente nunca contradizer o que a gente botou em outro post")*.** Rodar `python3 doutrina.py <assunto>` pra cada assunto que o post PRESCREVE e ler o que o acervo já mandou fazer. Se a prescrição nova inverte a antiga, só há três saídas legítimas: **(1)** alinhar com a antiga, **(2)** manter a nova e declarar a correção explicitamente na copy ("por muito tempo eu falei X; hoje eu faço Y porque…"), ou **(3)** trocar o ângulo do post. Contradição silenciosa = **reprova**, mesmo que as duas frases sejam boas isoladamente. *Evidência: a saída do `doutrina.py` do assunto + o veredito de cada prescrição.* *Caso real que criou esta dimensão: o SEM31/AD006 saiu com "NUNCA PROMETA O ABATIMENTO" enquanto o SEM25/AD003 — campeão do acervo, s/r 3,95% contra mediana de 0,64% — ensinava o oposto ("use o abatimento só se a paciente perguntar" e troque ele por compromisso de agendamento). Sete dimensões passaram por cima: todas perguntavam "isso se repete?", nenhuma perguntava "isso contradiz?". Território cuida de repetição; doutrina cuida de coerência.* **Atenção ao acervo pré-engine:** os posts até ~SEM26 não têm `copy.json` (a copy mora no `build.py`) e o `doutrina.py` extrai deles de forma aproximada — é ali que estão vários campeões, então essas entradas se leem com atenção redobrada, não se ignoram.

- [ ] **D4 · Repetição do que funcionou NÃO é achado *(política do Sávio, 30/jul)*.** Reusar mecânica, fórmula de capa, tipo de prova ou tese que já performou é a INTENÇÃO — "a intenção é sempre repetir o que pode ter feito um post se sair muito bem". Não abrir achado por "isso já foi usado". Só vira reprova em dois casos: **(a) adjacência de feed** — os dois usos caem no mesmo dia ou em dias seguidos (o leitor vê os dois na mesma rolagem), ou **(b) cópia integral** — a formulação inteira palavra por palavra, sem ângulo novo. *Evidência: citar os dois usos com a distância em dias.* *Caso real: a frase "a consulta é abatida no procedimento" travou um post inteiro por estar num registro de queimadas; o registro é CONTADOR de desgaste, não muro.*

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
