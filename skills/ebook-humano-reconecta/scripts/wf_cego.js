export const meta = {
  name: 'leitor-cego',
  description: 'Tres leitores cegos independentes por bloco, decisao por maioria',
  phases: [{ title: 'Ler', detail: 'tres leitores por bloco, sem contexto nenhum' }],
}
const A = args || {}
const CEGO = {
  type: 'object',
  properties: {
    veredito: { type: 'string', enum: ['pessoa', 'ia', 'indeciso'] },
    confianca: { type: 'number', description: '0 a 100' },
    pistas: { type: 'array', items: { type: 'object', properties: {
      trecho: { type: 'string' }, pista: { type: 'string' },
    }, required: ['trecho', 'pista'] } },
  },
  required: ['veredito', 'confianca', 'pistas'],
}
phase('Ler')
const lentes = [
  'Voce le muito e reconhece texto de maquina por instinto.',
  'Voce e editor de nao-ficcao ha vinte anos e ja recusou original por soar sintetico.',
  'Voce e leiga no assunto e so quer saber se parece gente escrevendo.',
]
const res = await parallel(A.blocos.flatMap((b) => lentes.map((lente, i) => () =>
  agent(`${lente}

Leia com Read SOMENTE o arquivo ${A.raiz}/revisao/${b}/capitulo-limpo.md. Voce nao sabe nada sobre quem escreveu, nem sobre o livro, nem sobre o assunto.

Responda com honestidade: este texto foi escrito por uma PESSOA ou por uma IA? De um veredito, uma confianca de 0 a 100 nesse veredito, e as 5 pistas mais fortes, cada uma com o trecho exato. Se voce achou que e pessoa, as pistas sao o que te convenceu de que e pessoa. Portugues do Brasil, sem elogio, sem diplomacia.`,
    { label: `cego:${b}:${i + 1}`, phase: 'Ler', schema: CEGO })
    .then(r => ({ bloco: b, leitor: i + 1, ...(r || {}) })))))

const porBloco = {}
for (const r of res.filter(Boolean)) {
  if (!r.veredito) continue
  ;(porBloco[r.bloco] = porBloco[r.bloco] || []).push(r)
}
const saida = Object.entries(porBloco).map(([bloco, rs]) => {
  const votos = { pessoa: 0, ia: 0, indeciso: 0 }
  rs.forEach(r => votos[r.veredito]++)
  const maioria = Object.entries(votos).sort((a, b) => b[1] - a[1])[0][0]
  const conf = Math.round(rs.reduce((s, r) => s + (r.confianca || 0), 0) / rs.length)
  log(`${bloco}: ${votos.pessoa} pessoa / ${votos.ia} ia / ${votos.indeciso} indeciso -> ${maioria} (${conf})`)
  return { bloco, votos, maioria, confianca_media: conf, leitores: rs }
})
return { blocos: saida }
