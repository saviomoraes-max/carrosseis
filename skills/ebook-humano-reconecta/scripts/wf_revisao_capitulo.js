export const meta = {
  name: 'revisao-capitulo-ebook',
  description: 'Revisao adversarial de um capitulo de ebook: 4 revisores, cetico por achado, detector cego',
  phases: [
    { title: 'Revisar', detail: '4 lentes em paralelo: tells, fidelidade, leitora, voz' },
    { title: 'Confirmar', detail: 'um cetico por revisor (lote); segundo cetico so nas altas' },
    { title: 'Cego', detail: 'detector cego: so o texto, sem contexto' },
  ],
}

// args esperados:
// { capitulo: 'caminho.md', capitulo_limpo: 'copia sem front matter (pro cego)', revisores: ['tell','voz'] (opcional, default todos),
//   fontes: ['...md'], fingerprint: '...md', catalogo: '...md',
//   detector_json: '...json', mapa: '...md', rodada: 1, trechos_mudados: ['...'] (opcional) }
const A = args || {}
const cap = A.capitulo
// juri: modelo dos revisores/ceticos/cego. Default = modelo da sessao. Fixar quando quiser
// reproduzir a regua de outra sessao (ex.: 'fable' pra manter a regua das rodadas anteriores).
const JURI = A.juri ? { model: A.juri } : {}
const foco = (A.trechos_mudados && A.trechos_mudados.length)
  ? `\nRODADA FOCADA: concentre-se nestes trechos que mudaram desde a rodada anterior (mas acuse qualquer coisa grave fora deles):\n- ${A.trechos_mudados.join('\n- ')}\n`
  : ''

const ACHADOS = {
  type: 'object',
  properties: {
    achados: { type: 'array', items: { type: 'object', properties: {
      trecho: { type: 'string', description: 'citacao EXATA do manuscrito, 1 a 3 frases' },
      tipo: { type: 'string', enum: ['tell', 'fidelidade', 'leitora', 'voz'] },
      detalhe: { type: 'string', description: 'o que esta errado, com nome do tell ou citacao da fonte' },
      gravidade: { type: 'string', enum: ['alta', 'media', 'baixa'] },
      correcao: { type: 'string', description: 'reescrita proposta NA VOZ DA AUTORA, ou o que resolveria' },
    }, required: ['trecho', 'tipo', 'detalhe', 'gravidade', 'correcao'] } },
    resumo: { type: 'string' },
  },
  required: ['achados', 'resumo'],
}
const VER = {
  type: 'object',
  properties: {
    real: { type: 'boolean' },
    motivo: { type: 'string' },
    correcao_alternativa: { type: 'string' },
  },
  required: ['real', 'motivo'],
}
const CEGO = {
  type: 'object',
  properties: {
    veredito: { type: 'string', enum: ['pessoa', 'ia', 'indeciso'] },
    confianca: { type: 'number' },
    pistas: { type: 'array', items: { type: 'object', properties: {
      trecho: { type: 'string' }, pista: { type: 'string' },
    }, required: ['trecho', 'pista'] } },
  },
  required: ['veredito', 'confianca', 'pistas'],
}

const regras = `Regras: cite trechos EXATOS (copie do arquivo). Nao seja diplomatico, nao elogie.
Nao invente problema pra preencher: se o capitulo esta bom em algo, resumo diz isso e achados vem vazio.
Nunca proponha correcao com travessao (—) nem com italico. Portugues do Brasil.`

phase('Revisar')
const revisores = [
  { k: 'tell', p: `Voce e o EDITOR DE TELLS de um ebook em portugues do Brasil. Leia com Read: o capitulo ${cap}; o catalogo de tells ${A.catalogo}; o fingerprint da autora ${A.fingerprint} (a secao WHITELIST e intocavel: habitos dela que parecem tell mas sao dela; NAO acuse nada que esteja la); a saida do detector automatico ${A.detector_json} (use como pista, nao como verdade).
Procure PADRAO, nao palavra: contraste facil (nao e X, e Y), triade automatica, anafora, ritmo de metronomo, hedging, fecho grandioso, explicar demais, calque do ingles, vocabulario nivel 1 do catalogo, sobra de chatbot. Cada achado: trecho exato, qual tell (nome do catalogo), gravidade, e a correcao escrita NA VOZ DA AUTORA conforme o fingerprint (nao numa voz neutra). Marque so o que pesa: um contraste isolado num capitulo nao e achado; tres, sao. ${foco} ${regras}` },
  { k: 'fidelidade', p: `Voce e o FISCAL DE FIDELIDADE. O livro so pode conter o que esta nas fontes. Leia com Read: o capitulo ${cap}; as fontes ${(A.fontes||[]).join(', ')}; o mapa ${A.mapa} (o que este capitulo prometeu entregar).
Para CADA afirmacao factual, caso, numero, nome, frase pronta de script no capitulo: existe na fonte? esta distorcida? Frase pronta de script deve ser LITERAL (compare palavra a palavra). Placeholder da fonte ("Dra. Mariana", "Fulana", "[procedimento]") que sobrou no texto e achado. Conteudo que o mapa prometeu e o capitulo nao entregou e achado (media). Inventado ou distorcido = alta. Em 'detalhe', cite o que a fonte diz de verdade. ${foco} ${regras}` },
  { k: 'leitora', p: `Voce e a LEITORA-ALVO: dentista de harmonizacao facial, 32 anos, atende o WhatsApp da propria clinica entre um paciente e outro, comprou este ebook pela pagina de vendas, esta lendo no celular a noite. Leia com Read SO o capitulo ${cap} e o mapa ${A.mapa}.
Marque: onde voce perde o fio; onde a autora explica o que voce ja entendeu; onde falta o exemplo que faria voce entender; onde voce pularia; onde soa que alguem esta te vendendo algo dentro de um livro que voce ja pagou; onde a frase pronta e boa mas voce nao saberia QUANDO usar. Nao reescreva: diga o que sentiu e o que resolveria. Use tipo 'leitora'. ${foco} ${regras}` },
  { k: 'voz', p: `Voce e o GUARDIAO DE VOZ. Leia com Read: o capitulo ${cap} e o fingerprint da autora ${A.fingerprint}.
Onde o texto NAO soa ela: registro mais formal do que ela usa, conector que ela nao usa, imagem generica onde ela usaria imagem concreta (ela fala em "salinha do financeiro", "levar facada"), frase longa demais onde ela cortaria, ironia que falta, muleta oral em excesso pra texto escrito (ver guia fala -> escrita), primeira pessoa que some. Tambem acuse quando um habito da WHITELIST foi apagado do capitulo. Cada achado: trecho, o que ela diria em vez disso citando o fingerprint, gravidade. Use tipo 'voz'. ${foco} ${regras}` },
]

const VER_LOTE = {
  type: 'object',
  properties: { vereditos: { type: 'array', items: { type: 'object', properties: {
    i: { type: 'number', description: 'indice do achado (0..n-1) como listado' },
    real: { type: 'boolean' }, motivo: { type: 'string' }, correcao_alternativa: { type: 'string' },
  }, required: ['i', 'real', 'motivo'] } } },
  required: ['vereditos'],
}
const listar = (achs) => achs.map((a, i) => `[${i}] gravidade ${a.gravidade} | tipo ${a.tipo}\ntrecho: ${JSON.stringify(a.trecho)}\ndetalhe: ${JSON.stringify(a.detalhe)}\ncorrecao proposta: ${JSON.stringify(a.correcao)}`).join('\n\n')
const ceticoPrompt = (achs, revisor) => `Voce e um CETICO. Abra com Read o capitulo ${cap} inteiro e a secao WHITELIST do fingerprint ${A.fingerprint}. Abaixo estao ${achs.length} acusacoes do revisor ${revisor}. Para CADA uma, localize o trecho no arquivo com o paragrafo anterior e o posterior e tente REFUTAR.
So confirme (real=true) se TODAS valem: (1) o problema existe no trecho como esta no arquivo; (2) nao esta protegido pela whitelist; (3) uma leitora real notaria ou seria prejudicada; (4) a correcao proposta nao introduz outro tell, nao usa travessao, e nao achata a voz da autora. Se (1)-(3) valem mas (4) falha, devolva real=true com correcao_alternativa na voz da autora. Na duvida, refute. Motivo em 1 a 3 frases por acusacao. Devolva um veredito por indice.

${listar(achs)}`
const julgar = async (achs, revisor, rotulo) => {
  if (!achs.length) return []
  const r = await agent(ceticoPrompt(achs, revisor), { label: rotulo, phase: 'Confirmar', schema: VER_LOTE, ...JURI })
  const mapa = new Map((r && r.vereditos ? r.vereditos : []).map(v => [v.i, v]))
  return achs.map((a, i) => ({ a, v: mapa.get(i) || { real: false, motivo: 'sem veredito do cetico (falha)' } }))
}

const ativos = (A.revisores && A.revisores.length) ? revisores.filter(r => A.revisores.includes(r.k)) : revisores
const brutos = await pipeline(
  ativos,
  r => agent(r.p, { label: `rev:${r.k}`, phase: 'Revisar', schema: ACHADOS, ...JURI }),
  (res, r) => (res && res.achados ? res.achados.map(a => ({ ...a, revisor: r.k })) : []),
  async (achs, r) => {
    const j1 = await julgar(achs, r.k, `ok:${r.k}`)
    // segundo cetico so pros achados de gravidade alta que o primeiro confirmou
    const altas = j1.filter(x => x.v.real && x.a.gravidade === 'alta').map(x => x.a)
    const j2 = await julgar(altas, r.k, `ok2:${r.k}`)
    const j2map = new Map(j2.map(x => [x.a, x.v]))
    return j1.map(({ a, v }) => {
      const v2 = j2map.get(a)
      const real = v.real && (v2 ? v2.real : true)
      const ceticos = v2 ? [v, v2] : [v]
      const alt = ceticos.map(c => c.correcao_alternativa).find(Boolean)
      return { ...a, real, ceticos, correcao_final: alt || a.correcao }
    })
  },
)

phase('Cego')
const capLimpo = A.capitulo_limpo || cap
const cego = await agent(`Leia com Read SOMENTE o arquivo ${capLimpo}. Voce nao sabe nada sobre quem escreveu. Responda com honestidade: este capitulo foi escrito por uma PESSOA ou por uma IA? De um veredito, uma confianca de 0 a 100 nesse veredito, e as 5 pistas mais fortes que te levaram a ele, cada uma com o trecho exato. Se voce achou que e pessoa, as pistas sao o que te convenceu de que e pessoa. Portugues do Brasil, sem elogio.`,
  { label: 'detector-cego', phase: 'Cego', schema: CEGO, ...JURI })

const todos = brutos.flat().filter(Boolean)
const confirmados = todos.filter(a => a.real)
const porRevisor = {}
for (const a of todos) { porRevisor[a.revisor] = porRevisor[a.revisor] || { brutos: 0, confirmados: 0 }; porRevisor[a.revisor].brutos++; if (a.real) porRevisor[a.revisor].confirmados++ }
log(`rodada ${A.rodada || 1}: ${todos.length} acusacoes, ${confirmados.length} confirmadas; cego: ${cego ? cego.veredito + ' ' + cego.confianca : 'n/a'}`)

return {
  capitulo: cap, rodada: A.rodada || 1,
  brutos: todos.length, confirmados_n: confirmados.length,
  altas_confirmadas: confirmados.filter(a => a.gravidade === 'alta').length,
  por_revisor: porRevisor,
  confirmados: confirmados.map(a => ({ revisor: a.revisor, tipo: a.tipo, gravidade: a.gravidade, trecho: a.trecho, detalhe: a.detalhe, correcao: a.correcao_final, motivos: a.ceticos.map(c => c.motivo) })),
  refutados: todos.filter(a => !a.real).map(a => ({ revisor: a.revisor, trecho: a.trecho, detalhe: a.detalhe, motivo: (a.ceticos[0] || {}).motivo })),
  cego,
}
