export const meta = {
  name: 'gerar-lote-carrosseis',
  description: 'Pipeline de produção: para cada tema vetado, gera a copy ancorada na spec+repertório e roda o portão de qualidade. Só aprova o que cruza A→E.',
  phases: [
    { title: 'Gerar + Portão', detail: 'cada tema passa por gerador e depois portão de qualidade, em pipeline' },
  ],
}

const DATA = '/Users/saviomoraes/reconecta/agente-carrosseis'

// Em produção, estes temas vêm de data/trends-queue.json (tendencias-research).
// Para o teste de fumaça, 2 temas VENCEDORES subproduzidos, com canibalização a evitar.
const TEMAS = [
  { tema: 'indicacao / follow-up', prioridade: 'alta', sem: 'SEM27', slug: 'indicacao-sem-pedir',
    brief: 'Como a paciente satisfeita vira fonte de 3+ indicações sozinha, sem você implorar nem dar desconto por indicação. A indicação nasce na ENTREGA do resultado, não num programa de pontos.',
    evitar: ['SEM21/AD010 Janela de 5 Minutos (indicação na hora)', 'post publicado de indicação 3-5-7'] },
  { tema: 'recorrencia', prioridade: 'alta', sem: 'SEM27', slug: 'recorrencia-nasce-na-primeira',
    brief: 'A paciente recorrente nasce na PRIMEIRA venda (quem comprou transformação volta; quem comprou procedimento some). Não é fidelizar depois, é como você vendeu.',
    evitar: ['SEM19/AD003 Recorrencia que Garante 58k'] },
]

const COPY_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['slug', 'titulo', 'tema_mapeado', 'tecnica_headline', 'estrutura_usada', 'slides', 'legenda', 'ancoras'],
  properties: {
    slug: { type: 'string' }, titulo: { type: 'string' }, tema_mapeado: { type: 'string' },
    tecnica_headline: { type: 'object', additionalProperties: false, required: ['tecnica', 'url_fonte'], properties: { tecnica: { type: 'string' }, url_fonte: { type: 'string', description: 'URL da entrada do repertório que ancora a headline' } } },
    estrutura_usada: { type: 'string', description: 'qual esqueleto VENCEU foi usado' },
    slides: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['n', 'tipo'], properties: {
      n: { type: 'number' }, tipo: { type: 'string' },
      headline: { type: 'string' }, subhead: { type: 'string' }, kicker: { type: 'string' },
      body: { type: 'string' }, objecao: { type: 'string' }, resposta: { type: 'string' },
      send_cue: { type: 'string' }, cta_label: { type: 'string' },
    } } },
    legenda: { type: 'string' },
    ancoras: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['afirmacao', 'ancora'], properties: { afirmacao: { type: 'string' }, ancora: { type: 'string', description: 'dado real / copy antiga / fonte / "demonstrado via processo"' } } } },
  },
}

const PORTAO_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['aprovado', 'blocos', 'falhas', 'cabecalho_fontes'],
  properties: {
    aprovado: { type: 'boolean' },
    blocos: { type: 'object', additionalProperties: false, required: ['A', 'B', 'C', 'D', 'E'], properties: {
      A: { type: 'string' }, B: { type: 'string' }, C: { type: 'string' }, D: { type: 'string' }, E: { type: 'string' } } },
    falhas: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['slide', 'bloco', 'criterio', 'diff_proposto', 'porque'], properties: {
      slide: { type: 'string' }, bloco: { type: 'string' }, criterio: { type: 'string' }, diff_proposto: { type: 'string' }, porque: { type: 'string' } } } },
    cabecalho_fontes: { type: 'string', description: 'o "por que passou" com as fontes (URL headline, dor que o tema conecta, âncoras)' },
  },
}

phase('Gerar + Portão')

const out = await pipeline(TEMAS,
  (t) => agent(
    `Você é o gerador de carrossel da RECONECTA. Gere a copy de UM carrossel topo de funil sobre: ${t.tema} (prioridade ${t.prioridade}).\nBrief do ângulo: ${t.brief}\nEvite canibalizar: ${t.evitar.join('; ')}.\n\n` +
    `CONSULTE (use Read) e OBEDEÇA:\n- ${DATA}/voice-spec.md (ganchos/estruturas/temas que VENCERAM, ritmo, dial de voz, nunca-faz)\n- ${DATA}/voice-dna.md (COMO escrever pra soar como a copywriter, não como IA — 5 dispositivos + checklist anti-robótico; OBRIGATÓRIO)\n- ${DATA}/headlines-repertoire.json (escolha uma técnica VENCEU — pergunta-paradoxo ou numero/lista — e ADAPTE a estrutura ao tema; guarde a url_fonte)\n- ${DATA}/relevance-filter.json (público e dores)\n\n` +
    `REGRAS: 8-9 slides, 1 ideia por slide. VOZ (NÃO-NEGOCIÁVEL, senão sai robótico e reprova): aplique os dispositivos do voice-dna.md — ≥1 FRASE PRONTA exata por slide de entrega, ≥1 CONTRASTE SECO, ≥1 DETALHE CONCRETO inesperado, número de capa ESCALADO (3,5,7), e ENCENE a cena em vez de explicar o conceito. Slides de entrega com 4 camadas (ação+mecanismo+exemplo vivo+frame). Dial: postura firme + gíria leve, registro doutora (como o SEM27/AD002). Sem travessão, sem "high ticket"/"alto ticket", sem autoelogio, sem comparar com concorrente. ZERO dado inventado: toda afirmação factual vai em 'ancoras' com a âncora (dado real/copy antiga/fonte) ou marcada "demonstrado via processo". CTA: slide = "TOQUE NO LINK DA BIO". A LEGENDA (entregue SEMPRE junto) roda o MESMO filtro voice-dna, pede SALVAR + MANDAR (send) e FECHA com CTA de link na bio que ESPELHA o CTA do último card (o do Figma) em prosa ("Se você quer que o meu time analise o seu cenário atual e te mostre o mapa claro pra converter 9 a cada 10 consultas e subir o seu ticket médio, toca no link da bio."), NUNCA parafraseie torto nem use "clique agora" de IA. FORMATO da legenda: entre parágrafos, a linha em branco leva SOZINHA o caractere invisível U+2800 ("⠀") — segura a quebra no Instagram e deixa a leitura dinâmica. Slide 1 sem masthead. CTA sem @handle.\n\n` +
    `Headline: ancore numa técnica do repertório e registre tecnica + url_fonte. Retorne no schema.`,
    { label: `gerar:${t.tema}`, phase: 'Gerar + Portão', schema: COPY_SCHEMA, effort: 'high' }
  ),
  (copy, t) => agent(
    `Você é o PORTÃO DE QUALIDADE (adversarial, zero achismo). Audite esta copy de carrossel contra o checklist.\n\n` +
    `Leia (use Read) ${DATA}/portao-qualidade.md e aplique os blocos A→E, cada item pass/fail COM evidência. Também confira contra ${DATA}/voice-spec.md (gancho/estrutura/tema que venceram) e ${DATA}/headlines-repertoire.json (a tecnica_headline existe lá? a url bate?).\n\n` +
    `COPY A AUDITAR:\n${JSON.stringify(copy, null, 2)}\n\n` +
    `Seja rigoroso: marque fail em qualquer item sem evidência (headline sem âncora no repertório, dado sem âncora, gancho que só existiu, CTA sem SEND, travessão, etc.). Para cada fail, dê o slide + critério + um diff_proposto focado + o porquê. aprovado=true só se A→E todos passam. Preencha cabecalho_fontes com o "por que passou" + as fontes.`,
    { label: `portao:${t.tema}`, phase: 'Gerar + Portão', schema: PORTAO_SCHEMA, effort: 'high' }
  ).then(p => ({ tema: t.tema, sem: t.sem, slug: t.slug, copy, portao: p }))
)

return { resultados: out.filter(Boolean) }
