# Checklist de Pauta Semanal — Carrossel RECONECTA

> **Para quem é:** o modelo que monta a pauta da semana (escrito pro Opus; o Fable também roda).
> **Quando roda:** no primeiro dia útil da semana, DEPOIS da análise semanal (`run-analise-semanal.sh` → `data/analise-semanal/SEM{xx}.json`). Pauta sem análise antes = pauta no escuro.
> **O que ele NÃO é:** checklist de copy. Aqui se decide O QUE entra na semana; como se escreve é o `checklist-producao.md`, e o juiz final continua sendo o portão.
> Item **PARE** reprovado → a pauta não vai pro Sávio até resolver.

---

## 1 · Ler os dados do jeito certo **(PARE)**

- [ ] **Regra da maturidade (28/jul/26, medida com 18 posts em 2 snapshots):** alcance em D+1 chegou a crescer +502% depois; D+4 cresce 60-120%; só assenta ~D+14. Post com **D+6 ou menos = leitura PROVISÓRIA**, sempre rotulada. Veredito de uma semana só é confiável na segunda SEGUINTE.
- [ ] **Ranquear por TAXA, nunca por alcance bruto.** s/r (shares/reach) e saves/r estabilizam ~D+7; alcance não. Comparar D+4 com D+12 por alcance é erro de método.
- [ ] **Cada métrica tem uma função — não somar tudo num "score":**
  - **shares/r = distribuição** (o sinal nº1 do algoritmo; é o que decide pauta)
  - **saves/r = utilidade** (bom, mas save é "guardo pra mim" — não distribui)
  - **follows = aquisição** (o forte dos posts de carona em trend)
  - **comments = motor do CTA** (comment-to-DM), não qualidade do conteúdo
- [ ] **Benchmark da era antes de julgar qualquer post** (recalcular no `SEM{xx}.json`, não usar de cabeça). Referência em 28/jul/26, só carrosséis D+7+: era da copywriter (mai-jun/26) mediana 1,38% · p75 2,95% · teto 5,79%. Nossa era (jul/26) mediana 1,09% · p75 1,60% · teto 3,21%. **O gap está no TETO, não na mediana** — o alvo da pauta é produzir pico (≥3%), não subir a média.
- [ ] **Views ≠ alcance ao conversar com o Sávio:** ele olha views no app (views = plays totais; alcance = pessoas únicas; razão típica ~1,7x). Citar as duas quando o número for grande.

## 2 · Herdar ELEMENTOS, nunca temas **(PARE — regra do zero, 27/jul)**

- [ ] **Semana nova nasce do zero.** Dos posts vencedores herda-se o ELEMENTO nomeado (fórmula de capa, mecânica de prova, tipo de CTA, formato de momento) — nunca o tema, nunca a frase. Gaveta não entra sozinha; revival de tema = só com autorização explícita do Sávio (precedente: Disney, 27/jul).
- [ ] **Todo slot da pauta declara o elemento herdado + a fonte:** "capa de frase literal (AD002 SEM29, s/r 2,42% maduro)". Slot sem elemento rastreável a dado = achismo.
- [ ] **Checagem de queimadas NO NÍVEL DO TEMA** (`headlines-repertoire.json`, bloco `queimadas`): a família da frase/tese proposta está queimada? Adjacência conta (ex.: "vou ver com meu financeiro" = família do marido; "manda a tabela" = família do quanto-custa). Na dúvida, trocar o tema — não advogar.
- [ ] **Mapa de território das últimas 2 semanas** antes de fechar os temas: o que cada post publicado reivindicou (frase, fórmula de gancho, mecânica, print). Tema novo não pisa em território de post com menos de 14 dias.

## 3 · Teste do encaminhamento **(PARE — o filtro que faltava, 28/jul)**

Dado que motivou: os dois posts de parábola ampla sem âncora de clínica (cabeleireiro 0,48% D+4, Disney 0,19% D+1) são os piores da safra de julho até aqui; a capa de frase literal madura fez 2,42%. Save subiu enquanto share caiu = estávamos escrevendo "útil de guardar", não "urgente de mandar".

- [ ] **Pra cada tema, responder POR ESCRITO: "pra quem, especificamente, a doutora manda esse post?"** ("a sócia", "a secretária", "a colega que responde por áudio", "a amiga que abriu clínica"). Resposta genérica ("é útil pra todas") = save-bait; o tema volta pra mesa.
- [ ] **Capa ancora na clínica.** Parábola cultural ampla só entra se a ponte com a clínica está NA CAPA (headline ou sub), não guardada pro slide 3. A doutora fria precisa se reconhecer em ≤2s.
- [ ] **≥1 momento datável por tema** (hora, dia da semana, cena de rotina: "9h07", "terça de manhã", "antes do bom dia"). Momento datável é o que faz a leitora dizer "isso aconteceu comigo HOJE" — e encaminhar.

## 4 · Mix da semana

- [ ] **80/10/10** (definição completa no `checklist-producao.md` §5-B): ~80% validado · ~10% notícia em alta (slot FLEX preenchido pelo radar 07:20 DO DIA, nunca antecipado — não passou no filtro, vira validado) · ~10% disruptivo (tese contrária com âncora na metodologia + refutador extra no portão).
- [ ] **Carona em trend tem função declarada: alcance + follows, NÃO s/r** (Vini Jr: 80k alcance/135k views, 37 follows, s/r 0,27% — funcionou pro que serve). Não cobrar share de post de trend nem trend de post de share.
- [ ] **Os dois públicos do Leonardo (14/jul) aparecem na semana:** (a) iniciante com medo de vender/não saber oferecer · (b) quem tem lead mas perde venda/sem ticket. O pilar (a) tem ≥1 slot.
- [ ] **Variação interna da semana em tabela** (não de cabeça): fórmula de gancho da capa, formato do post, dispositivo de prova — dias consecutivos não repetem os três eixos. Capa de frase literal ≤2 na semana (fórmula vencedora também satura).
- [ ] **Pareamento de designs (era 2 posts/dia, SEM31+):** post A = design atual, post B = design novo (Figma v2). Os DOIS posts do mesmo dia não dividem território nem público-alvo primário; o tema não pode depender do design pra funcionar.

## 5 · Registro e entrega

- [ ] **Pauta gravada em `data/pautas/SEM{xx}.md`**, um bloco por slot: dia · design (A/B) · tema em 1 frase · elemento herdado + fonte (post, taxa, maturidade) · destinatário do encaminhamento · público (a/b) · slot do mix (validado/trend/disruptivo) · status (proposta → aprovado → produzido → POSTADO).
- [ ] **Apresentar ao Sávio como PROPOSTA** com os dados que sustentam cada escolha. Pauta aprovada não muda sem avisar; slot FLEX de trend é decidido no dia com o radar.
- [ ] **Depois da aprovação:** produção segue `checklist-producao.md` desde o §0 — a pauta dá o território; a copy continua nascendo do zero com tabela de âncoras própria.
