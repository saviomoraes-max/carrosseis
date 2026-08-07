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

**05/ago — registro de publicação.** No ar: AD001 (seg 03), AD003 + AD004 + **AD011**
(ter 04), AD005 (qua 05). AD002 descartado. Falta postar: AD006 (hoje), AD007+AD008
(qui), AD009+AD010 (sex).

O **AD011** foi um post EXTRA de carona em notícia (Georgina Rodríguez, 04/ago),
fora do plano original de 10. Função declarada: alcance, seguidores e CONVERSA nos
comentários — CTA de opinião, sem SUPERCASO e sem link. **Julgar por alcance,
comentários e seguidores; NUNCA por shares** (precedente medido: Vini Jr, 81.823 de
alcance com s/r 0,27%). Ele é o primeiro post da conta desenhado pra comentário —
o recorde atual de comentários é 167 (SEM31/AD006).

**Erro de processo registrado (05/ago):** ao consertar o itálico no engine eu
re-renderizei e re-exportei o AD004, que já estava publicado desde 04/ago — eu não
sabia, porque o POSTADO.txt ainda não existia. Os PNGs da pasta ficaram diferentes do
que está no ar (o publicado tem as ênfases em itálico nos slides 2-6). Marcado na
pasta. **A regra que falhou:** "checar POSTADO.txt antes de editar" só funciona se o
marcador for criado NO DIA. Quando a publicação é informada em lote no dia seguinte,
a janela fica aberta. Mitigação adotada: antes de qualquer re-render em massa,
PERGUNTAR o que já foi ao ar — não confiar só na ausência do marcador.

## AD012 — "Os 4 tipos de conteúdo" (06/ago, pedido do Sávio, 3º post do dia)

**Origem:** PDF "Banco de Referências" (treinamento RECONECTA, 4 pilares, 33
referências curadas: Educação 4 · Experiência & Bastidor 11 · Lifestyle 3 · Antes e
Depois 15). O material vai pro direct por automação; o post entrega a LENTE, o DM
entrega o MATERIAL.

**REUSO DECLARADO DE CAMPEÃO (a decisão central deste post).** Esse material já
rodou: **SEM20/AD005 "5 Conteúdos No Feed"**, publicado 14/mai/26, mediu
**s/r 2,59% e saves/r 2,86% com 29.369 de alcance** — hit confirmado, e o MELHOR
saves/r do acervo inteiro. Gatilho dele: `POST`. Reusado aqui, por escolha do Sávio:
- a fórmula da capa (número escalado + desproporção "só precisa" + promessa
  "chegar quase agendando") — mecânica idêntica, número trocado de 5 pra 4;
- o reframe do miolo ("a saída não é criar mais, é modelar o que já performou");
- a arquitetura do CTA (o trabalho já foi feito → validado → é chegar e adaptar).

**O que é NOVO (para não ser cópia integral, D4-b):**
- 4 pilares, não 5 — o material foi consolidado (Experiência e Bastidor viraram um);
- o conceito **modelagem ≠ cópia** com a engenharia explícita ("por que aquele gancho
  parou o dedo"), que não existia no post de mai — é o insight novo do PDF;
- a ENGENHARIA de cada pilar no slide 4 (o "o que observar"), no lugar de um slide
  por pilar como no original de 8 slides;
- gatilho **BANCO** (POST está queimado por ser deste mesmo material);
- prova nova: prova_1381 "primeiro pix de consulta feita pelo direct" — inédita por
  dHash, e prova a tese literal (o perfil gerou consulta paga sem anúncio).

**Adjacência declarada (D4-a):** SEM32/AD009 "Esperando a Promoção" sai na sexta
(07/ago) e também toca perfil/feed — dias seguidos. Diferenciação: AD009 é sobre o
que NÃO postar (promoção virando rotina ensina a esperar desconto); AD012 é sobre a
ARQUITETURA do feed (quais 4 tipos precisam existir). Superfícies distintas:
desconto × variedade. SEM31/AD007 (feed cria objeção, d+6) ataca a LEGENDA com ml —
superfície distinta de novo. Território conferido: "pilares", "modelar", "banco de
referências", "quase agendando sozinho", "criar do zero" — todos livres nos 4-gramas.

**Função e leitura:** este post é comment-to-DM, então o sinal primário é COMENTÁRIO
e saves. O campeão de mai fez saves/r 2,86% — é essa a régua, não o share.

**AD012 — fechamento (06/ago).** Portão rodado (33 agentes): 27 achados brutos, 4
confirmados, todos aplicados — (1) D5: rótulo do pilar 1 virou "EDUCAÇÃO DO PROBLEMA"
porque "EDUCAÇÃO" cru contradizia a capa do AD001 desta mesma semana ("a paciente que
você educa fecha com a concorrência"); (2) C5: "desses PILARES" no CTA era
demonstrativo sem antecedente (nenhum slide dizia "pilar") e invertia a agência —
virou "desses 4 TIPOS", que ainda fecha o arco com a capa; (3+4) E2: a legenda §2
reciclava duas frases inteiras do slide 2, substituída por cena adjacente nova.
Segunda rodada (refutadores que caíram por erro de API): 0 confirmados — mas os
finders vieram do cache, então essa rodada NÃO é auditoria limpa da versão nova.
**Por isso rodei o pre-flight mecânico à mão sobre o arquivo final, e ele pegou duas
colisões que os 33 agentes não pegaram:** "no seu feed agora" e "e manda pra colega
que" colidiam com o SEM31/AD007 e com o AD007 do MESMO DIA — adjacência de feed
(D4-a). Corrigido com variação mínima ("Desce três telas do seu feed" / "E marca
aquela colega"). Virou o item 6 do PRE-FLIGHT no checklist-producao.md.

**AD012 — ajustes finais do Sávio (06/ago):**
- Ele editou a HERO e trocou a foto. Medição no render (fundo atrás da headline):
  luz 22,0 · ruído 17,4 — melhor que a média do TOP 4 medido (28,2 · 19,9).
- Slide 2 trocado a pedido dele: a foto anterior (torcedora gritando na
  arquibancada, `Sy7ye0XUb8`) não conversava com "um feed só de resultado é um
  catálogo" e era a mais poluída do post. Entrou `magnific_vuvuuqxa47` (SEM31,
  editorial, fundo escuro): luz 37,1→28,8 e ruído 20,1→**13,8**, o mais limpo do post.
  Conferido por dHash contra as 54 imagens em uso nas SEM3x e contra o SEM27/AD010.
  **Descartada `magnific_DBDBH6Ipcl`** apesar de tecnicamente livre (distância 94):
  é a mesma modelo, mesma roupa e mesmo cenário da capa do SEM31/AD004, publicado
  há 8 dias — dHash não pega eco visual de mesma sessão fotográfica.
- **Gatilho trocado de BANCO para CONTEÚDO** (decisão do Sávio). Zero resíduo de
  BANCO no JSON. Ver a nota de acento abaixo.

**ERRO DE PROCESSO (06/ago): o catálogo `_pool-imagens.md` tem descrições erradas.**
Escrevi lendo as 20 imagens em lote e embaralhei; escolhi a foto do slide 2 pelo
catálogo em vez de abrir a imagem. Aviso gravado no topo do arquivo. Regra nova:
**imagem se escolhe abrindo a imagem, nunca por descrição de catálogo.**

**07/ago — hero do AD010 trocada pelo Sávio.** A capa da Anne Hathaway saiu e entrou
uma foto nova (inédita, conferida no `imagens_usadas.py`). Eu levantei objeção pela
regra de hero não-sugestiva e ele manteve a decisão: **"se eu coloquei a imagem, é
pra você usar"** — a política de imagem dele já estava registrada em 03/ago
("pool fechado, tudo é usável, exceção só quando ele apontar"). Decisão dele,
registrada, não é achado de portão.

**Efeito colateral bom:** a troca dissolveu a adjacência que o portão tinha apontado
no AD013 (Anne na capa do AD010 e no AD013 no mesmo dia). Com a Anne só no AD013,
os dois podem sair hoje sem colisão.

## Dois erros de DOUTRINA apontados pelo Sávio (07/ago) — viraram `doutrina-fixa.md`

**1. O CRO na bio (AD013, pego ANTES de publicar).** O item 1 do slide 4 dizia «No
lugar de "Dentista · Pós em HOF · CRO 00000", a linha que ela resolve: …». A casa
ensina o oposto: **o registro FICA (é obrigatório de conselho) e a linha de
posicionamento se SOMA a ele**. Palavra dele: "a gente ensina que tem que ter o CRO,
mas tem que ter essa frase também… então ele tá em parte certo e parte errado".
Corrigido para "O CRO fica, é obrigatório. O que falta é a linha de cima."
Âncora conferida no acervo: SEM24/AD006 e SEM23/AD009.

**2. A palavra "educativo" (AD012, já publicado).** O rótulo cru "EDUCAÇÃO" colide com
a doutrina central de que paciente super-informada compara preço e fecha com a
concorrência — e saiu três dias depois de o AD001 desta semana ter capa inteira sobre
isso. O portão já tinha corrigido pra "EDUCAÇÃO DO PROBLEMA", mas o Sávio confirmou
que o cuidado é permanente, não era só daquele post.

**Por que os dois passaram:** o `doutrina.py` compara o post novo contra o que os
posts ANTIGOS disseram. Nenhum dos dois era contradição com post anterior — eram
contradição com a METODOLOGIA, que não estava escrita em lugar que a máquina lesse.
Criado o `doutrina-fixa.md`, que vence o doutrina.json em conflito. Entrou como
**D5.0** no portão (PARE, antes do resto do D5) e no PASSE A do checklist-producao.

**07/ago — legenda do AD010 refeita: inimigo comum, não a doutora.** Os 5 parágrafos
punham o erro nela ("pedindo licença", "travessia de OPERÁRIA", "tentação de caber no
bolso de todo mundo", "se você quer ser percebida como autoridade"). Palavra do Sávio:
*"a gente tá atacando muito a doutora… isso pode dar muito ruim. A gente sempre tem
que atacar um inimigo em comum e não a doutora."* Reescrita com o inimigo do lado de
fora (a formação que não ensina preço · o mercado que ensinou a conta errada). Virou a
**seção 3 do `doutrina-fixa.md`** e entrou como item (0) do D5.0 no portão.
Escopo respeitado: só a legenda. **O slide 4 ainda tem o mesmo problema** — punch
"A TRAVESSIA DE «OPERÁRIA» PRA ESTRATEGISTA" e item "COBRE O PREÇO QUE FALTA CORAGEM"
— apontado ao Sávio, aguardando decisão dele.

**AD013 foi publicado e ARQUIVADO pelo Sávio** por causa do erro do CRO (ele postou
antes da correção sair). A versão da pasta já está corrigida; se for republicar, é a
que está lá.
