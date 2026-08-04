# Pauta SEM32 (03–07/ago/2026) — 2 posts/dia, trilho A (hero) + trilho B (hero_b)

**Contexto que manda nesta semana** (SEM31-leitura, 03/ago): o viral AD006 (3,73%,
41.914) provou a configuração vencedora — **UMA frase-que-custa-caro ocupando o post
inteiro**, conversa comercial, scripts colável, prova conectada. A mesma frase como
item de lista mediu 0,30%. Todos os 12 hits ≥2% da era são conversa comercial.
Gancho de notícia compra alcance, não share (Vini Jr: 81.823 / 0,27%).

**Processo desta pauta:** 10 slots propostos por síntese sobre 3 leituras (corpus
virgem, mecânica top/bottom 12, território+doutrina) → painel adversarial de 4
lentes por slot (fonte, território/doutrina, força, mecânica-do-viral) → **9 de 10
caíram** → esta versão reconstrói cada slot com o conserto proposto pelos próprios
refutadores. Bruto completo em `SEM32-workflow-bruto.json`.

**O que o painel provou e virou lei do lote:**
- Capa "Você não está vendendo. Está dando uma aula." era verbatim do SEM31/AD002
  (6 dias). Frame aula/explicar-demais: 4 usos em 5 semanas — família queimada.
- "Medo Que Vaza" como taxonomia já rodou maduro: s/r 0,11%. Não re-minar formato.
- "As 3 Frases" original: capa idêntica à proposta mediu 0,53%. Motor ml→conta→
  objeção é do SEM31/AD007 (4d). Slot adiado pra SEM33.
- "Cobrar barato é confessar" como capa já mediu 0,58% maduro (= mediana). Capa nova.
- 2 slots rebaixavam a frase-que-custa a item de checklist — o padrão dos 0,30%.
- Família "comparação de preço": 3 usos na janela (16d/10d/7d) — só com declaração
  e diferenciação explícita (justificar ≠ comparar).

## Os 10 slots

| # | dia | tr | capa | título de trabalho | fonte | surface (anti-adjacência) |
|---|-----|----|------|--------------------|-------|---------------------------|
| 1 | SEG | A | aspa | A Paciente Que Chega Sabendo Tudo | corpus[22] SEM20/AD004 (beat virgem, SEM frame aula) | paciente "educada" que não fecha |
| 2 | SEG | B | pergunta | Paciente Modelo Sem Queimar Produto | corpus[31] SEM21/AD003 | captação de modelo |
| 3 | TER | A | numero | R$4 Mil Pelo Relatório Bonito | corpus[27] SEM20/AD009 + hit triagem 10/mai | capa=dor do tráfego, MIOLO=script de triagem do curioso (conserto do painel: corpo vira conversa comercial) |
| 4 | TER | B | afirmacao | Justificar Preço É Pedir Desculpa | corpus[45] SEM23/AD007 | justificar ≠ comparar; declarar família compara 3x (16/10/7d), verbatim "quanto mais justifica" NÃO vai pra capa (punch de slide há 31d) |
| 5 | QUA | A | afirmacao | O Valor É R$X (E a Consulta Morreu Ali) | corpus[26] SEM20/AD008 + hit 4,61% (13/jun) | preço como PRIMEIRA fala; SEM a pergunta "o que te trouxe" (SEM31/AD002) e SEM moldura "se vender antes do preço"; declarar adjacência AD003 SEM31 (áudio responde tudo — superfície distinta: velocidade vs completude) |
| 6 | QUA | B | numero | Fechar 8 de 10 Na Consulta | corpus[62] SEM26/AD003 | condução da consulta PRESENCIAL (não WhatsApp); frase-que-custa: começar a consulta pelo procedimento; alinhar com doutrina AD006 (consulta tem valor próprio) |
| 7 | QUI | A | aspa | "Eu Sou Dentista, Não Sou Vendedora" | corpus[25] SEM20/AD007 — SÓ a aspa (precedente 2,94%); miolo NOVO = cena da apresentação do plano, fala hesitante vs fala inteira (scripts) | crença-escudo; QUI = D+14 do SEM30/AD004, território libera; NADA de taxonomia de medos (0,11% maduro) |
| 8 | QUI | B | trend (≠numero) | SLOT FLEX — radar 07:20 de quinta | radar → mini-ponte → filtro → OK do Sávio | julgar por ALCANCE/follows, nunca por s/r; **reserva NOVA**: corpus[65] SEM26/AD007 re-mine focado — "Ah, é paga? Vou no concorrente que faz de graça" (post 3,90% maduro; só o beat da gratuidade, "vou pensar" NÃO entra — SEM31/AD002); declarar família consulta-paga (AD006 4d, ângulos distintos: cobrar ≠ contornar) |
| 9 | SEX | A | pergunta | Por Que Ela Espera a Sua Promoção? | corpus[5] sinal 04 VIRA o post inteiro (conserto do painel) + prova Manu Barcelos | promoção mensal ensina a esperar desconto; declarar família desconto (AD006 = abatimento, superfície distinta) |
| 10 | SEX | B | pergunta→capa "Se é tão boa, por que cobra como quem está começando?" | corpus[11] SEM19/AD002 | precificação/autovalor; capa antiga (0,58%) NÃO volta; miolo = matemática 100×1k vs 10×10k + cena real; SEM cena de comparação (é do slot 4) |

Fórmulas de capa por trilho (sem repetição em dias consecutivos):
A: aspa · numero · afirmacao · aspa · pergunta — B: pergunta · afirmacao · numero · trend · pergunta

CTA padrão do lote: comentário SUPERCASO (mecânica dos campeões: o material é a
EXTENSÃO depois da entrega completa, nunca no lugar dela).

**Checklist por post antes de escrever:** ler a peça-fonte inteira no corpus →
`doutrina.py <assuntos>` → territorio-vivo (4-gramas) → escrever com a tese ocupando
o post → print inédito (`prints_usados.py` no candidato E no lote) → render →
portão (com D5) → export. Prova social conecta com a tese (D3) e punch não ecoa o
print.

---

## Atualizações de execução

**04/ago — AD002 "Modelo Sem Queimar Produto" DESCARTADO por decisão do Sávio**
("não vamos usar o ad002"). Produzido e exportado, mas NÃO publica — sem POSTADO.txt,
o território continua tratando ele como não-publicado (correto). Sem substituto: a
semana fica com 9 posts (AD001 seg + 2/dia ter→sex). O slot B de segunda ficou vazio.
Nota pro futuro: se o tema captação-modelo voltar, o post está pronto na pasta e o
print prova_0249 segue tecnicamente inédito no feed.

**03/ago à noite — portões de TER-SEX caíram no limite de sessão** (finders sem
veredito). Pela regra "refutador morto não absolve", AD003-AD010 seguem BLOQUEADOS
até o portão completar. Retomado em 04/ago do cache.

**04/ago — AD003 finalizado com prioridade (pedido do Sávio) e liberado pra postar.**
Aplicados os 19 achados do portão, deduplicados: (1) print da prova TROCADO — o da
Maria Eduarda creditava o resultado ao tráfego e citava "outra mentoria", desmentindo
o punch; entrou prova_0243 (fechamento da semana: "apenas de lead, foram 5
agendamentos"), inédita por dHash; (2) scripts do slide 4 VARIADOS pra não re-ensinar
verbatim o SEM30/AD003 publicado há 13 dias (itens 2 e 3 reescritos preservando a
mecânica; item 1 mantém o verbatim virgem do corpus[49]); (3) D5: corpo do slide 3
alinhado com a peça-fonte ("a configuração certa traz; a primeira resposta decide");
(4) fecho novo — o antigo entregava de graça a tese do AD004 do mesmo dia;
(5) legenda P1-P2 reescritas (cena da conta do custo-por-paciente-fechada, zero eco);
(6) ênfase champagne aplicada (regra de 04/ago).
**DECLARAÇÃO DE ADJACÊNCIA (capa):** a capa aspa "QUANTO CUSTA O BOTOX?" divide o
device "quanto custa" com o SEM30/AD003 publicado em 22/jul (13d). Diferenciação:
SEM30 = como responder o quanto-custa (conduta no direct); SEM32/AD003 = por que o
tráfego só entrega essa pergunta e a triagem que a converte. Mantida por ser a
objeção literal na capa (mecânica dos campeões) — decisão registrada, Sávio ciente.
