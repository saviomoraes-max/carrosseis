export const meta = {
  name: 'corpus-fala-autora',
  description: 'Garimpa o corpus de fala da autora pra trocar prosa composta por fala real, e checa fidelidade contra o corpus',
  phases: [
    { title: 'Garimpar', detail: 'um garimpeiro por bloco: busca no corpus de 81k palavras' },
    { title: 'Confirmar', detail: 'um cetico por bloco: confere a citacao no corpus antes de aceitar' },
  ],
}

// args: { raiz, corpus, fingerprint, fontes: [...], blocos: [{k, arquivo}] }
const A = args || {}
const R = A.raiz

const ACHADOS = {
  type: 'object',
  properties: {
    trocas: { type: 'array', items: { type: 'object', properties: {
      trecho_livro: { type: 'string', description: 'citacao EXATA do manuscrito que soa prosa composta, 1 a 3 frases' },
      motivo: { type: 'string', description: 'por que este trecho soa escrito e nao falado' },
      fala_dela: { type: 'string', description: 'trecho LITERAL do corpus, copiado sem alterar uma palavra' },
      proposta: { type: 'string', description: 'o paragrafo reescrito usando a fala dela, so com pontuacao ajustada' },
      gravidade: { type: 'string', enum: ['alta', 'media', 'baixa'] },
    }, required: ['trecho_livro', 'motivo', 'fala_dela', 'proposta', 'gravidade'] } },
    sem_fonte: { type: 'array', items: { type: 'object', properties: {
      afirmacao: { type: 'string', description: 'citacao EXATA do manuscrito' },
      onde_procurei: { type: 'string', description: 'os termos que voce buscou nas fontes E no corpus' },
      gravidade: { type: 'string', enum: ['alta', 'media', 'baixa'] },
    }, required: ['afirmacao', 'onde_procurei', 'gravidade'] } },
    resumo: { type: 'string' },
  },
  required: ['trocas', 'sem_fonte', 'resumo'],
}

const VER = {
  type: 'object',
  properties: { vereditos: { type: 'array', items: { type: 'object', properties: {
    i: { type: 'number' },
    lista: { type: 'string', enum: ['troca', 'sem_fonte'] },
    real: { type: 'boolean' },
    motivo: { type: 'string' },
    proposta_alternativa: { type: 'string' },
  }, required: ['i', 'lista', 'real', 'motivo'] } } },
  required: ['vereditos'],
}

const LEIS = `LEIS DO PROJETO (valem acima de qualquer achado seu):
- Fidelidade vence voz. Inventar fato pra consertar ritmo e pior que o problema de ritmo.
- Travessao (—) e italico sao PROIBIDOS. Nenhuma proposta pode conter.
- Frase pronta de script vai LITERAL do PDF da fonte. Nao reescreva conteudo de bloco :::frase.
- Nao perseguir dose uniforme de marcador oral. Fala real vem em rajada: tres "ne" num paragrafo
  e nenhum nos dois seguintes e MAIS humano que um por paragrafo. Nao espalhe.
- Simetria perfeita e suspeita, mesmo quando o recurso e dela. Nada de anafora exata de tres
  degraus, quiasmo, espelhamento, nem par "Parece X. E Y." fechando paragrafo.
- Nao invente problema pra preencher. Lista vazia e resposta legitima e boa.
- Portugues do Brasil.`

phase('Garimpar')

const garimpo = (b) => `Voce e o GARIMPEIRO DE FALA deste livro. O livro e narrado em primeira pessoa pela Ana Luiza, e o
problema conhecido dele e este: partes do texto sao PROSA COMPOSTA imitando a fala dela, e leitores cegos
independentes enxergam a costura entre a fala transcrita e a prosa composta. O corpus de fala dela existe e
tem 80.938 palavras sobre EXATAMENTE o assunto do livro. Sua tarefa e trocar prosa composta por fala real.

Leia com Read: o bloco ${R}/manuscrito/${b.arquivo} e o fingerprint ${A.fingerprint}.
${b.foco ? `\nRODADA FOCADA. Leitores cegos independentes ja leram este bloco e apontaram isto. Ataque estes pontos primeiro, procurando no corpus a fala dela que substitui cada um:\n- ${b.foco.join('\n- ')}\n` : ''}
Use Grep (nao Read, o arquivo e enorme) no corpus ${A.corpus} pra achar a fala dela sobre cada assunto do bloco.
Busque por termo do dominio (o assunto do bloco, o nome do passo, as palavras que a paciente usa), com -i e -C 3
pra pegar contexto. Faca MUITAS buscas, com sinonimos, ate esgotar.

DUAS LISTAS:

1. "trocas": passagens do bloco que soam escritas e para as quais o corpus tem a fala dela dizendo a mesma
   coisa melhor. Em "fala_dela" copie o trecho do corpus LITERAL, sem mudar uma palavra, do jeito que saiu
   no grep. Em "proposta" escreva o paragrafo do livro ja com a fala dela dentro: pode ajustar SO pontuacao
   e cortar repeticao de transcricao ("o o", "que que"), nunca trocar as palavras dela por sinonimos seus.
   O corpus e transcricao automatica: a pontuacao dele nao vale, o vocabulario vale.
   So proponha troca quando a fala dela for MELHOR, mais concreta ou mais dela. Se a prosa composta ja esta
   boa, deixa quieto. Prefira poucas trocas fortes a muitas fracas.

2. "sem_fonte": afirmacoes do bloco que funcionam como fato ou regra (definicao, doutrina, numero,
   quantificador como "a maioria", ordinal como "o mais pulado", causa, caso) e que voce NAO acha nem nas
   fontes ${(A.fontes || []).join(', ')} nem no corpus. Busque nos dois antes de acusar, inclusive por
   parafrase e sinonimo. Em "onde_procurei" liste os termos que voce buscou. Esta e a primeira vez que o
   corpus entra nessa checagem: coisa que a auditoria anterior cortou por nao estar no PDF pode estar aqui.

${LEIS}`

const listar = (r) => {
  const t = (r.trocas || []).map((x, i) => `[troca ${i}] gravidade ${x.gravidade}\nno livro: ${JSON.stringify(x.trecho_livro)}\nmotivo: ${JSON.stringify(x.motivo)}\nfala dela (alegada): ${JSON.stringify(x.fala_dela)}\nproposta: ${JSON.stringify(x.proposta)}`).join('\n\n')
  const s = (r.sem_fonte || []).map((x, i) => `[sem_fonte ${i}] gravidade ${x.gravidade}\nafirmacao: ${JSON.stringify(x.afirmacao)}\nbuscou: ${JSON.stringify(x.onde_procurei)}`).join('\n\n')
  return `${t}\n\n${s}`
}

const cetico = (b, r) => `Voce e o CETICO. Abaixo estao as propostas de um garimpeiro sobre o bloco
${R}/manuscrito/${b.arquivo}. Abra o bloco com Read. Sua funcao e REFUTAR, nao ajudar.

Para cada item da lista "troca", so confirme (real=true) se TODAS valerem:
 (1) voce achou a "fala_dela" no corpus ${A.corpus} com Grep, LITERAL. Se o grep nao acha, a citacao foi
     inventada ou parafraseada: real=false, e diga isso no motivo. ISTO E O TESTE MAIS IMPORTANTE. Faca o grep.
 (2) o "trecho_livro" existe no bloco exatamente como citado;
 (3) a fala dela realmente diz a mesma coisa que o trecho do livro, e nao outra coisa parecida;
 (4) a proposta nao quebra o raciocinio do paragrafo vizinho, nao contradiz outro trecho do bloco, e nao
     entra dentro de bloco :::frase (script literal, intocavel);
 (5) a proposta nao tem travessao, nao tem italico, e nao empilha marcador oral de forma uniforme.
Se (1)-(4) valem mas (5) falha, devolva real=true com proposta_alternativa corrigida.

Para cada item de "sem_fonte", tente ACHAR a fonte: busque nas fontes ${(A.fontes || []).join(', ')} E no
corpus, por parafrase e sinonimo, antes de aceitar a acusacao. So confirme se voce tambem nao achou.

Na duvida, refute. Motivo em 1 a 3 frases. Um veredito por indice, com o campo "lista" dizendo de qual
das duas listas o indice veio.

${listar(r)}`

const resultados = await pipeline(
  A.blocos,
  (b) => agent(garimpo(b), { label: `garimpo:${b.k}`, phase: 'Garimpar', schema: ACHADOS }),
  async (r, b) => {
    if (!r) return { bloco: b.k, erro: 'garimpeiro nao devolveu' }
    const n = (r.trocas || []).length + (r.sem_fonte || []).length
    if (!n) return { bloco: b.k, resumo: r.resumo, trocas: [], sem_fonte: [], brutos: 0 }
    const v = await agent(cetico(b, r), { label: `cetico:${b.k}`, phase: 'Confirmar', schema: VER })
    const mapa = new Map((v && v.vereditos ? v.vereditos : []).map(x => [`${x.lista}:${x.i}`, x]))
    const marcar = (lista, arr) => (arr || []).map((x, i) => {
      const d = mapa.get(`${lista}:${i}`) || { real: false, motivo: 'sem veredito do cetico (falha)' }
      return { ...x, real: d.real, motivo_cetico: d.motivo, proposta_final: d.proposta_alternativa || x.proposta }
    })
    return {
      bloco: b.k, arquivo: b.arquivo, resumo: r.resumo, brutos: n,
      trocas: marcar('troca', r.trocas),
      sem_fonte: marcar('sem_fonte', r.sem_fonte),
    }
  },
)

const ok = resultados.filter(Boolean)
for (const r of ok) {
  const tc = (r.trocas || []).filter(x => x.real).length
  const sc = (r.sem_fonte || []).filter(x => x.real).length
  log(`${r.bloco}: ${r.brutos || 0} brutos -> ${tc} trocas e ${sc} sem-fonte confirmadas`)
}
return { blocos: ok }
