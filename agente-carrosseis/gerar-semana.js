export const meta = {
  name: 'gerar-semana-carrosseis',
  description: 'Lote semanal 80/10/10: gera ~10 carrosséis no formato do engine validado, passa cada um pelo portão de qualidade e renderiza os PNGs na pasta da semana. 8 validado + 1 variação + 1 teste.',
  phases: [
    { title: 'Gerar', detail: 'cada slot vira copy no formato do engine (hero/photo/text/list/proof/cta)' },
    { title: 'Portão', detail: 'auditoria adversarial A→E, zero achismo' },
    { title: 'Render', detail: 'escreve copy.json + renderiza 6 PNGs na pasta SEM{xx}/{slug}/' },
  ],
}

// ----------------------------------------------------------------------------
// Configuração (sobrescrevível por args)
// ----------------------------------------------------------------------------
const A = (typeof args === 'object' && args) ? args : {}
const DATA = '/Users/saviomoraes/reconecta/agente-carrosseis'
const ENGINE_DIR = '/Users/saviomoraes/reconecta/carrosseis/_template/html-engine'
const WEEK = A.week || 'SEM27'
const YEAR = A.year || 26
const OUTBASE = A.outbase || `/Volumes/SSD kenipe/estáticos/novos/${WEEK}`
const START_AD = A.startAd || 5  // SEM27 já tem AD001-004

// Pool de temas VALIDADOS (vencedores subproduzidos na voice-spec). Fallback
// quando a trends-queue está vazia. Em produção, A.slots vem da fila vetada.
const POOL = [
  { tema: 'consulta que converte', hook: 'pergunta-paradoxo', slug: 'consulta-vende-transformacao',
    brief: 'A consulta que mais converte não explica o procedimento, vende a transformação. Quem foca em "educar" sobre técnica perde pra quem faz mais barato. (ângulo do campeão AD001 — usar OUTRO recorte, não repetir.)',
    evitar: ['SEM27/AD001 Paciente que você educa'] },
  { tema: 'indicação', hook: 'numero-lista', slug: 'indicacao-nasce-na-entrega',
    brief: 'A paciente vira fonte de 3+ indicações sozinha quando a indicação nasce na ENTREGA do resultado, não num programa de pontos nem implorando.',
    evitar: ['SEM27/AD003 indicacao-nasce-na-entrega', 'SEM21/AD010 Janela de 5 Minutos'] },
  { tema: 'recorrência', hook: 'pergunta-paradoxo', slug: 'recorrencia-nasce-na-primeira-venda',
    brief: 'A paciente recorrente nasce na PRIMEIRA venda: quem comprou transformação volta, quem comprou procedimento some. É como você vendeu, não fidelização depois.',
    evitar: ['SEM27/AD004 recorrencia-nasce-na-primeira-venda', 'SEM19/AD003 Recorrencia 58k'] },
  { tema: 'perfil que atrai', hook: 'numero-lista', slug: 'perfil-que-atrai-paciente-certo',
    brief: 'O posicionamento (perfil/postura) que atrai a paciente que paga bem e some a que pechincha. Não é preço, é a leitura de quem você é antes da consulta.',
    evitar: [] },
  { tema: 'prospecção ativa', hook: 'pergunta-paradoxo', slug: 'prospeccao-sem-implorar',
    brief: 'Como puxar paciente nova de forma ativa sem parecer desesperada nem dar desconto. A prospecção que funciona parte de autoridade, não de oferta.',
    evitar: [] },
  { tema: 'follow-up / objeção WhatsApp', hook: 'numero-lista', slug: 'follow-up-que-fecha',
    brief: 'Swipe file: as respostas de WhatsApp que transformam "vou pensar" em agendamento, sem pressão. Script tático pronto pra usar.',
    evitar: ['SEM27/AD002 Respostas Vou Pensar'] },
  { tema: 'agenda do milhão', hook: 'numero-lista', slug: 'agenda-do-milhao-engrenagem',
    brief: 'A engrenagem da agenda lotada: 3 pacientes novas + 4 recorrências por semana. O cálculo que mostra que não é volume, é estrutura.',
    evitar: ['SEM21/AD008 6 Engrenagens da Agenda'] },
  { tema: 'SUPERCASO', hook: 'pergunta-paradoxo', slug: 'supercaso-lente-transformacao',
    brief: 'A lente do SUPERCASO: parar de mostrar antes/depois técnico e começar a contar a transformação de vida. Por que o caso que vende não é o melhor resultado clínico.',
    evitar: [] },
]

// 12 design-* skills pro slot de teste (design experimental)
const DESIGN_SKILLS = ['design-editorial-dark', 'design-cinematic', 'design-magazine',
  'design-swiss-bold', 'design-data-story', 'design-neobrutalist']

function pad(n) { return String(n).padStart(3, '0') }  // AD005, não AD05

function buildSlots() {
  const slots = []
  // 80% — 8 validado
  for (let i = 0; i < 8; i++) {
    const t = POOL[i % POOL.length]
    slots.push({ kind: 'validado', ad: `AD${pad(START_AD + i)}`, ...t })
  }
  // 10% — 1 variação (tema vencedor + hook trocado, "estilo diferente" controlado)
  const v = POOL[0]
  slots.push({ kind: 'variacao', ad: `AD${pad(START_AD + 8)}`,
    tema: v.tema, hook: 'numero-lista', slug: `${v.slug}-v2`,
    brief: `VARIAÇÃO do tema "${v.tema}": mesmo design validado, mas troca o gancho pra numero-lista e um recorte novo. ${v.brief}`,
    evitar: v.evitar })
  // 10% — 1 teste (tema experimental + design-* skill, fora do padrão)
  slots.push({ kind: 'teste', ad: `AD${pad(START_AD + 9)}`,
    tema: 'tendência experimental', hook: 'pergunta-paradoxo', slug: 'teste-experimental',
    brief: 'Slot de teste 100%: tema mais arriscado (tendência ainda não validada que passe no filtro de relevância) + design experimental. Aprende rápido, não é o padrão.',
    evitar: [], design: DESIGN_SKILLS[0] })
  return slots
}

const SLOTS = A.slots || buildSlots()
const RUN = A.only ? SLOTS.slice(0, A.only) : SLOTS

// ----------------------------------------------------------------------------
// Schemas
// ----------------------------------------------------------------------------
const SLIDE = {
  type: 'object', additionalProperties: false, required: ['type'],
  properties: {
    type: { type: 'string', enum: ['hero', 'photo', 'text', 'list', 'proof', 'cta'] },
    headline: { type: 'string', description: 'hero — caixa alta, use \\n pra quebra art-directed' },
    punch: { type: 'string', description: 'photo/text/list/proof/cta — caixa alta, \\n quebra, {vermelho} e «champagne» pra ênfase' },
    body: { type: 'array', items: { type: 'string' }, description: 'photo/text — 1-2 parágrafos; {vermelho}/«champagne» inline' },
    items: { type: 'array', description: 'list — itens numerados', items: { type: 'object', additionalProperties: false, required: ['title', 'body'], properties: { title: { type: 'string' }, body: { type: 'string' } } } },
    callout: { type: 'string', description: 'text — caixa-gancho do próximo slide (vira itálico champagne)' },
    cta: { type: 'string', description: 'cta — default "TOQUE NO LINK DA BIO"' },
    image_hint: { type: 'string', description: 'hero/photo — que imagem o usuário deve depositar no slot' },
    prints_hint: { type: 'string', description: 'proof — que prints de depoimento usar (do acervo, anonimizados)' },
  },
}

const COPY_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['slug', 'titulo', 'tema_mapeado', 'tecnica_headline', 'estrutura_usada', 'slides', 'legenda', 'ancoras'],
  properties: {
    slug: { type: 'string' }, titulo: { type: 'string' }, tema_mapeado: { type: 'string' },
    tecnica_headline: { type: 'object', additionalProperties: false, required: ['tecnica', 'url_fonte'], properties: { tecnica: { type: 'string' }, url_fonte: { type: 'string' } } },
    estrutura_usada: { type: 'string' },
    slides: { type: 'array', minItems: 6, items: SLIDE },
    legenda: { type: 'string', description: 'legenda que pede SALVAR + mandar pra uma colega (SEND), porque o slide manda pra bio' },
    ancoras: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['afirmacao', 'ancora'], properties: { afirmacao: { type: 'string' }, ancora: { type: 'string' } } } },
  },
}

const PORTAO_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['aprovado', 'blocos', 'falhas', 'cabecalho_fontes'],
  properties: {
    aprovado: { type: 'boolean' },
    blocos: { type: 'object', additionalProperties: false, required: ['A', 'B', 'C', 'D', 'E'], properties: { A: { type: 'string' }, B: { type: 'string' }, C: { type: 'string' }, D: { type: 'string' }, E: { type: 'string' } } },
    falhas: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['slide', 'bloco', 'criterio', 'diff_proposto', 'porque'], properties: { slide: { type: 'string' }, bloco: { type: 'string' }, criterio: { type: 'string' }, diff_proposto: { type: 'string' }, porque: { type: 'string' } } } },
    cabecalho_fontes: { type: 'string' },
  },
}

const RENDER_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['ok', 'pasta', 'pngs', 'imagens_necessarias', 'obs'],
  properties: {
    ok: { type: 'boolean' },
    pasta: { type: 'string' }, pngs: { type: 'array', items: { type: 'string' } },
    imagens_necessarias: { type: 'array', items: { type: 'string' } },
    obs: { type: 'string' },
  },
}

// Injeta os slots de imagem (determinístico) — o gerador cuida só da copy.
function withImageSlots(copy, slot) {
  let fotoN = 0
  const slides = copy.slides.map((s) => {
    if (s.type === 'hero') return { ...s, image: 'img/hero.jpg' }
    if (s.type === 'photo') { fotoN++; return { ...s, image: `img/foto_${fotoN}.jpg` } }
    if (s.type === 'proof') return { ...s, prints: [null, null, null] }
    return s
  })
  return { ad: slot.ad, week: WEEK, year: YEAR, kind: slot.kind, slug: copy.slug, titulo: copy.titulo, slides, legenda: copy.legenda }
}

// ----------------------------------------------------------------------------
// Pipeline: Gerar -> Portão -> Render (sem barreira; cada slot flui sozinho)
// ----------------------------------------------------------------------------
log(`Lote ${WEEK}: ${RUN.length} carrosséis (${RUN.filter(s => s.kind === 'validado').length} validado / ${RUN.filter(s => s.kind === 'variacao').length} variação / ${RUN.filter(s => s.kind === 'teste').length} teste)`)

const resultados = await pipeline(RUN,
  // --- 1. GERAR (formato do engine) ---
  (slot) => agent(
    `Você é o gerador de carrossel da RECONECTA. Gere a copy de UM carrossel topo de funil no FORMATO DO ENGINE VALIDADO (6 slides: hero · photo · text · list · proof · cta).\n\n` +
    `TEMA: ${slot.tema} (${slot.kind}). GANCHO sugerido: ${slot.hook}.\nÂNGULO/BRIEF: ${slot.brief}\nEVITE canibalizar: ${(slot.evitar || []).join('; ') || '—'}.\n\n` +
    `CONSULTE com Read e OBEDEÇA:\n- ${DATA}/voice-spec.md (ganchos/estruturas/temas que VENCERAM, ritmo, dial, nunca-faz)\n- ${DATA}/voice-dna.md (COMO escrever pra soar como a copywriter, não como IA — os 5 dispositivos + checklist anti-robótico)\n- ${DATA}/headlines-repertoire.json (escolha a técnica do gancho e GUARDE a url_fonte)\n- ${DATA}/relevance-filter.json (público/dores)\n- ${DATA}/design-spec.md (o look — pra escrever no tamanho certo de cada slot)\n\n` +
    `VOZ (NÃO-NEGOCIÁVEL, senão sai robótico e reprova): aplique os dispositivos do voice-dna.md — cada slide de entrega com ≥1 FRASE PRONTA exata (aspas, colável hoje), ≥1 CONTRASTE SECO no carrossel, ≥1 DETALHE CONCRETO inesperado (hora/número/objeto), número da capa ESCALADO (3,5,7 não redondo), e ENCENE a cena em vez de explicar o conceito. Antes de retornar, rode o checklist anti-robótico do voice-dna.md.\n\n` +
    `ESTRUTURA DO ENGINE (preencha cada slide com seu type):\n` +
    `1) hero: { type:"hero", headline } — pergunta/promessa em CAIXA ALTA, use \\n pra quebrar as linhas (art-directed, ~5 linhas). image_hint = que foto-retrato usar.\n` +
    `2) photo: { type:"photo", punch, body[1-2], image_hint } — punch caixa alta + 1-2 parágrafos. {vermelho} numa palavra-chave.\n` +
    `3) text: { type:"text", punch, body[1-2], callout } — desenvolve o mecanismo; callout = pergunta-gancho do próximo slide.\n` +
    `4) list: { type:"list", punch, items[3-4] {title,body} } — o passo-a-passo/conceito. punch pode ter «\\n» e {vermelho} numa metade. ATENÇÃO AO TAMANHO: o slide tem altura útil de ~1090px e NÃO se encolhe a fonte pra caber. Cada item.body = 1-2 LINHAS (≈140 caracteres MÁX), uma frase pronta + um fecho curto. A camada longa (mecanismo/frame) NÃO empilha aqui — ela mora no text/photo. 4 itens com body de 3-4 linhas ESTOURAM e o título/último item são cortados. Prefira 3 itens densos a 4 itens longos. Se a ideia precisa de body longo, use 3 itens. NÃO coloque número no title do item ("1. Escuta") — o engine já numera à esquerda; o title é só o nome ("A ESCUTA").\n` +
    `5) proof: { type:"proof", punch, prints_hint } — frase que conecta a prova; prints_hint = que depoimentos do acervo (anonimizados).\n` +
    `6) cta: { type:"cta", punch, cta:"TOQUE NO LINK DA BIO" } — punch caixa alta convidando pra análise/evento.\n\n` +
    `REGRAS DE COPY: 1 ideia por slide. Slides de entrega (photo/text/list) com as 4 CAMADAS (ação concreta + mecanismo causal + exemplo vivo/frase pronta + frame conceitual). Dial: postura firme + gíria leve, registro doutora (igual SEM27/AD002). PROIBIDO: travessão "—", "high ticket"/"alto ticket", autoelogio, comparar com concorrente, dado inventado. Toda afirmação factual vai em 'ancoras' com a âncora (dado real / copy antiga / fonte) OU "demonstrado via processo".\n` +
    `MARCAÇÃO: {texto}=vermelho, «texto»=champagne itálico, \\n=quebra de linha. Use com parcimônia (1 ênfase por bloco).\n` +
    `CTA: o slide manda "TOQUE NO LINK DA BIO" (link leva a evento/oferta). A LEGENDA (entregue SEMPRE junto com o post) é escrita na MESMA voz (aplique o voice-dna, roda o mesmo filtro anti-robótico da copy): faz o trabalho de distribuição pedindo SALVAR e MANDAR pra uma colega (send), e FECHA com um CTA de LINK NA BIO que ESPELHA o CTA do último card (o do Figma) em prosa (ex.: “Se você quer que o meu time analise o seu cenário atual e te mostre o mapa claro pra converter 9 a cada 10 consultas e subir o seu ticket médio, toca no link da bio.”), NUNCA parafraseie torto nem use “clique agora” de IA. FORMATO da legenda: entre parágrafos, a linha em branco leva SOZINHA o caractere invisível U+2800 ("⠀") — segura a quebra no Instagram e deixa a leitura dinâmica. Sem @handle no slide.\n` +
    `Headline ancorada numa entrada do repertório (registre tecnica + url_fonte). Retorne no schema.`,
    { label: `gerar:${slot.ad}`, phase: 'Gerar', schema: COPY_SCHEMA, effort: 'high' }
  ),

  // --- 2. PORTÃO ---
  (copy, slot) => agent(
    `Você é o PORTÃO DE QUALIDADE (adversarial, zero achismo) da RECONECTA. Audite a copy abaixo.\n\n` +
    `Leia com Read ${DATA}/portao-qualidade.md e aplique A→E, cada item pass/fail COM evidência. Confira contra ${DATA}/voice-spec.md (gancho/estrutura/tema que venceram) e ${DATA}/headlines-repertoire.json (a tecnica_headline existe lá? a url bate?).\n` +
    `Lembre do padrão de CTA atual: o slide usa "TOQUE NO LINK DA BIO" (E1) e a LEGENDA puxa salvar+SEND (E2). Sem @handle (E3).\n\n` +
    `COPY (${slot.ad} · ${slot.kind}):\n${JSON.stringify(copy, null, 2)}\n\n` +
    `Seja rigoroso: fail em qualquer item sem evidência (headline sem âncora, dado solto, gancho que só existiu, travessão, legenda sem SEND, slide de entrega sem as 4 camadas). Para cada fail: slide + critério + diff_proposto focado + porquê. aprovado=true só se A→E todos passam. cabecalho_fontes = o "por que passou" + fontes.`,
    { label: `portao:${slot.ad}`, phase: 'Portão', schema: PORTAO_SCHEMA, effort: 'high' }
  ).then(gate => ({ slot, copy, gate })),

  // --- 3. RENDER ---
  async (r) => {
    const { slot, copy, gate } = r
    if (!gate || !gate.aprovado) {
      log(`✗ ${slot.ad} reprovado no portão — não renderiza`)
      return { slot, copy, gate, render: { ok: false, pasta: '', pngs: [], imagens_necessarias: [], obs: 'reprovado no portão' } }
    }
    const finalCopy = withImageSlots(copy, slot)
    const pasta = `${OUTBASE}/${slot.ad} - ${copy.titulo}`
    const hints = copy.slides.filter(s => s.image_hint || s.prints_hint).map(s => `${s.type}: ${s.image_hint || s.prints_hint}`)
    const render = await agent(
      `Monte e renderize este carrossel RECONECTA. Faça EXATAMENTE:\n` +
      `1. Crie a pasta "${pasta}" e dentro dela "img/".\n` +
      `2. Escreva "${pasta}/copy.json" com este conteúdo EXATO (verbatim, sem alterar):\n\`\`\`json\n${JSON.stringify(finalCopy, null, 2)}\n\`\`\`\n` +
      `3. Escreva "${pasta}/img/NECESSARIO.txt" com a lista de imagens que o usuário precisa depositar (uma por linha):\n${hints.map(h => '   - ' + h).join('\n')}\n` +
      `4. Renderize: \`cd "${ENGINE_DIR}" && python3 engine.py "${pasta}/copy.json" "${pasta}/slides"\` (vai gerar slide_1..6.png; onde faltar imagem entra placeholder cinza — é esperado). O engine imprime \`⚠ OVERFLOW slide_N\` e grava \`slides/_overflow.json\` se algum slide não couber na faixa.\n` +
      `5. Confirme que os PNGs existem (ls "${pasta}/slides") E que NÃO existe \`${pasta}/slides/_overflow.json\`. Se existir, há overflow (copy longa demais, tipicamente o list de 4 itens): NÃO está pronto — reporte ok=false e em obs cite o slide e o over_px do JSON pra a copy ser encurtada (nunca encolher fonte).\n\n` +
      `Retorne no schema: ok, pasta, pngs (caminhos), imagens_necessarias (os hints), obs.`,
      { label: `render:${slot.ad}`, phase: 'Render', schema: RENDER_SCHEMA, effort: 'low' }
    )
    log(`✓ ${slot.ad} "${copy.titulo}" → ${render.pngs?.length || 0} PNGs`)
    return { slot, copy, gate, render }
  }
)

const ok = resultados.filter(r => r && r.render && r.render.ok)
const reprovados = resultados.filter(r => r && (!r.gate || !r.gate.aprovado))
log(`Lote ${WEEK} concluído: ${ok.length} renderizados, ${reprovados.length} reprovados no portão.`)

return {
  semana: WEEK,
  renderizados: ok.map(r => ({ ad: r.slot.ad, kind: r.slot.kind, titulo: r.copy.titulo, pasta: r.render.pasta, imagens_necessarias: r.render.imagens_necessarias })),
  reprovados: reprovados.map(r => ({ ad: r.slot.ad, titulo: r.copy?.titulo, falhas: r.gate?.falhas })),
}
