export const meta = {
  name: 'banca-do-livro',
  description: 'Banca de leitura: seis examinadores leem o LIVRO INTEIRO de ponta a ponta, cetico por examinador, e um relator fecha',
  phases: [
    { title: 'Ler', detail: 'seis lentes, cada uma lendo o livro inteiro na ordem' },
    { title: 'Conferir', detail: 'um cetico por examinador, reabrindo o livro pra refutar' },
    { title: 'Relatar', detail: 'o relator junta o que sobreviveu e fecha a banca' },
  ],
}

// args: { livro, ortotipografia, fingerprint, contexto }
const A = args || {}

const ACHADOS = {
  type: 'object',
  properties: {
    achados: { type: 'array', items: { type: 'object', properties: {
      trecho: { type: 'string', description: 'citacao EXATA do livro, copiada sem alterar nada, 1 a 3 frases' },
      onde: { type: 'string', description: 'capitulo ou anexo onde esta, ex "Capitulo 09" ou "Anexo C"' },
      problema: { type: 'string', description: 'o que esta errado, em uma ou duas frases' },
      gravidade: { type: 'string', enum: ['alta', 'media', 'baixa'] },
      correcao: { type: 'string', description: 'a frase corrigida, ou o que resolveria' },
    }, required: ['trecho', 'onde', 'problema', 'gravidade', 'correcao'] } },
    nota: { type: 'number', description: 'de 0 a 10, o quanto o livro passa nesta lente' },
    resumo: { type: 'string', description: 'parecer em 3 a 6 frases: o que esta bom e o que nao esta' },
  },
  required: ['achados', 'nota', 'resumo'],
}

const VER = {
  type: 'object',
  properties: { vereditos: { type: 'array', items: { type: 'object', properties: {
    i: { type: 'number' }, real: { type: 'boolean' }, motivo: { type: 'string' },
    correcao_alternativa: { type: 'string' },
  }, required: ['i', 'real', 'motivo'] } } },
  required: ['vereditos'],
}

const CONTEXTO = `O LIVRO. Ebook pago sobre atendimento no WhatsApp de clinica de harmonizacao facial:
sete passos, do primeiro "oi" ao comprovante do PIX. Narrado em PRIMEIRA PESSOA pela fundadora
da empresa, uma mulher que fala como quem da aula ao vivo. A leitora e uma doutora que comprou
o livro pela pagina de vendas e le no celular, a noite, entre um paciente e outro.

O REGISTRO E DELIBERADO E NAO E ERRO. Este livro foi construido a partir de 80.938 palavras de
fala transcrita da autora, e a oralidade dela e o ativo do produto, nao um defeito a limpar.
NAO acuse, em hipotese nenhuma:
- "pra", "ta", "ne", "o", "gente", "a gente", "so que", "agora, se", "ai";
- frase sem verbo, fragmento, frase comecando com E ou Mas ou Entao;
- autocorrecao no meio do raciocinio ("ela morre no meio da conversa. Ela desaparece no meio
  da conversa") e repeticao para martelar um ponto: sao marca de fala real e leitores cegos
  independentes citam isso como prova de que o texto foi escrito por gente;
- coloquialismo de norma nao culta que o brasileiro fala ("se responde com pergunta",
  "fazer ela dizer", "por que que"), quando esta na voz da autora ou dentro de fala citada;
- variacao de grafia de interjeicao entre capitulos.

O QUE E ERRO DE VERDADE: concordancia ou regencia que quebra o sentido, palavra faltando ou
sobrando, correlacao quebrada ("quanto mais... mas..."), pronome sem referente ou com referente
errado, tempo verbal que desmonta a sequencia, frase que nao fecha a sintaxe e nao da pra
entender, ambiguidade que faz a leitora entender o contrario, numero ou nome trocado.

PROIBIDO em qualquer correcao proposta: travessao (—) e italico. Aspas do corpo sao curvas.`

const REGRAS = `Leia com Read o livro inteiro em ${A.livro}, do comeco ao fim, na ordem. Ele tem cerca de
15 mil palavras: LEIA TUDO antes de acusar qualquer coisa, porque a sua lente so funciona com o
livro inteiro na cabeca.

Cite o trecho EXATO, copiado do arquivo sem mudar uma virgula, senao o achado nao pode ser
localizado e sera descartado. Nao seja diplomatico e nao elogie. Nao invente problema pra
preencher: lista vazia com nota alta e resposta legitima e boa. Portugues do Brasil.

${CONTEXTO}`

phase('Ler')

const lentes = [
  { k: 'lingua', p: `Voce e o CORRETOR DE LINGUA da banca, o que corrige redacao de vestibular. Leia tambem
${A.ortotipografia} antes de comecar, porque as regras de aspas, travessao e pontuacao deste livro estao la.

Procure SO erro mecanico de lingua: concordancia verbal e nominal, regencia, crase, pontuacao que muda o
sentido, correlacao quebrada, palavra faltando ou repetida por engano, frase truncada, paralelismo
quebrado numa enumeracao, pronome sem referente. Para cada um, devolva a frase corrigida inteira.

Cuidado que e o mais importante do seu trabalho: a maior parte do que parece erro neste livro e a voz
da autora e esta protegida acima. Se voce ficar em duvida entre "erro" e "jeito dela falar", e o jeito
dela falar. Um corretor que endireita a voz da autora estraga o produto.` },

  { k: 'continuidade', p: `Voce e o FISCAL DE CONTINUIDADE. Ninguem nunca leu este livro de ponta a ponta, e e
exatamente por isso que voce existe.

Procure: promessa feita e nao cumprida ("eu prometi no capitulo 9", "voce vai ver no capitulo 11", "a cola
do anexo A"); referencia cruzada errada (o capitulo citado nao e o que tem aquilo); termo da casa usado
antes de ser explicado (bastao, cortina de fumaca, presente inaceitavel, leitura, transicao, edicao);
numeracao dos sete passos inconsistente entre capitulos; conteudo que o livro anuncia e nunca entrega;
personagem ou exemplo que aparece do nada como se ja tivesse sido apresentado.

Confira CADA referencia cruzada abrindo o capitulo citado. Nao acuse de memoria.` },

  { k: 'repeticao', p: `Voce e o CACADOR DE REPETICAO ENTRE CAPITULOS. Atencao: repeticao DENTRO de um paragrafo,
pra martelar um ponto, e voz da autora e nao e achado seu. O que voce procura e outra coisa: a mesma
ideia, a mesma anedota, a mesma formula ou a mesma frase aparecendo em DOIS LUGARES DIFERENTES do livro,
onde a leitora vai reconhecer e sentir que ja leu aquilo.

Exemplos do que interessa: a mesma historia pessoal contada duas vezes; a mesma frase de efeito reusada
em outro capitulo; a mesma explicacao de um conceito repetida por extenso em vez de referenciada.

Cuidado: anexo que RESUME o capitulo esta cumprindo a funcao dele, e frase pronta de script se repete de
proposito, porque e material de consulta. Nesses dois casos, nao e achado.` },

  { k: 'contradicao', p: `Voce e o CACADOR DE CONTRADICAO. Procure lugar em que o livro diz uma coisa num capitulo
e o contrario em outro: prescricao oposta, definicao que muda de sentido, sinal de avancar que aparece
diferente em dois lugares, ordem dos passos trocada, regra apresentada como absoluta num capitulo e
relativizada em outro sem aviso.

Para cada acusacao, cite os DOIS trechos que se contradizem, um em "trecho" e o outro em "problema".
Contradicao aparente que o proprio texto resolve com uma ressalva nao e contradicao.` },

  { k: 'leitora', p: `Voce e a LEITORA-ALVO e vai ler o livro inteiro de uma sentada, como ela leria: dentista de
harmonizacao facial, 32 anos, atende o WhatsApp da propria clinica, comprou este ebook pela pagina de
vendas e esta lendo no celular a noite, cansada.

Marque onde VOCE, lendo assim: perde o fio e precisa voltar; sente que ja entendeu e o livro continua
explicando; encontra um exemplo que nao ajuda; pularia a pagina; sente que estao te vendendo alguma
coisa dentro de um livro que voce ja pagou; le uma frase pronta boa e nao sabe QUANDO usar ela; chega no
fim de um capitulo sem saber o que fazer amanha de manha.

Marque tambem o contrario, no resumo: onde o livro te ganhou. Nao reescreva nada: diga o que sentiu, em
que ponto, e o que resolveria. Sua nota e o quanto voce recomendaria este livro pra uma colega.` },

  { k: 'termos', p: `Voce e o GUARDIAO DE CONSISTENCIA. Leia tambem o fingerprint da autora em ${A.fingerprint}.

Procure incoerencia de vocabulario e de grafia ao longo do livro inteiro: a paciente ora chamada de
"lead", ora "cliente", ora "pessoa", ora "paciente", sem criterio; "consulta" e "agendamento" trocados;
grafia de marca e termo tecnico oscilando (WhatsApp, PIX, Instagram, harmonizacao facial); estilo de
placeholder mudando ([Nome], [nome], [NOME], [procedimento/consulta]); numero escrito ora por extenso
ora em algarismo no mesmo tipo de contexto; titulo de capitulo citado no corpo com nome diferente do
que esta no sumario.

O fingerprint diz como a autora chama as coisas de verdade: onde o livro divergir DELA, e achado.` },
]

const listar = (achs) => achs.map((a, i) =>
  `[${i}] gravidade ${a.gravidade} | ${a.onde}\ntrecho: ${JSON.stringify(a.trecho)}\nproblema: ${JSON.stringify(a.problema)}\ncorrecao: ${JSON.stringify(a.correcao)}`).join('\n\n')

const cetico = (achs, lente) => `Voce e o CETICO da banca. Abaixo estao ${achs.length} acusacoes do examinador de
${lente} sobre o livro ${A.livro}. Abra o livro com Read e, para cada acusacao, VA ATE O TRECHO e tente REFUTAR.

So confirme (real=true) se TUDO valer:
 (1) o trecho existe no arquivo LITERALMENTE como citado. Se voce nao achar com Grep, o examinador
     parafraseou e a acusacao cai. Faca a busca, e este teste vem antes de todos.
 (2) o problema existe mesmo, lendo o paragrafo anterior e o seguinte;
 (3) nao esta protegido pelo registro deliberado do livro (a lista de "NAO acuse" abaixo);
 (4) uma leitora real tropecaria ali;
 (5) a correcao proposta nao introduz outro problema, nao usa travessao nem italico, e nao achata a voz.
Se (1) a (4) valem mas (5) falha, devolva real=true com correcao_alternativa.

Na duvida, refute. Motivo em 1 a 3 frases por acusacao. Um veredito por indice.

${CONTEXTO}

${listar(achs)}`

const julgar = async (achs, lente) => {
  if (!achs.length) return []
  const v = await agent(cetico(achs, lente), { label: `cetico:${lente}`, phase: 'Conferir', schema: VER })
  const mapa = new Map((v && v.vereditos ? v.vereditos : []).map(x => [x.i, x]))
  return achs.map((a, i) => {
    const d = mapa.get(i) || { real: false, motivo: 'sem veredito do cetico (falha)' }
    return { ...a, lente, real: d.real, motivo_cetico: d.motivo, correcao_final: d.correcao_alternativa || a.correcao }
  })
}

const brutos = await pipeline(
  lentes,
  l => agent(`${l.p}\n\n${REGRAS}`, { label: `banca:${l.k}`, phase: 'Ler', schema: ACHADOS }),
  (r, l) => ({ lente: l.k, nota: r ? r.nota : null, resumo: r ? r.resumo : '', achados: r && r.achados ? r.achados : [] }),
  async (x) => ({ ...x, julgados: await julgar(x.achados, x.lente) }),
)

const ok = brutos.filter(Boolean)
const confirmados = ok.flatMap(x => x.julgados.filter(a => a.real))
for (const x of ok) log(`${x.lente}: nota ${x.nota}, ${x.achados.length} achados -> ${x.julgados.filter(a => a.real).length} confirmados`)

phase('Relatar')
const relatorio = await agent(`Voce e o RELATOR da banca deste livro. Seis examinadores leram o livro inteiro
(${A.livro}) e um cetico conferiu cada acusacao. Abaixo estao os pareceres, as notas e os achados que
sobreviveram ao cetico.

Escreva o parecer da banca, em portugues do Brasil, para o dono do produto. Ele precisa saber, nesta ordem:
1. O livro esta pronto pra vender? Uma frase, sem rodeio.
2. O que a banca achou de mais grave, em ordem de gravidade, com o trecho e o que fazer.
3. O que esta bom e nao deve ser mexido.
4. O que a banca NAO consegue avaliar e depende de decisao humana.

Nao invente achado que nao esta na lista. Nao repita achado que aparece em duas lentes: junte. Se um achado
de lente diferente aponta pro mesmo trecho, isso e sinal de gravidade, diga.

PARECERES:
${ok.map(x => `--- ${x.lente} (nota ${x.nota}) ---\n${x.resumo}`).join('\n\n')}

ACHADOS CONFIRMADOS (${confirmados.length}):
${confirmados.map((a, i) => `[${i}] ${a.lente} | ${a.gravidade} | ${a.onde}\ntrecho: ${a.trecho}\nproblema: ${a.problema}\ncorrecao: ${a.correcao_final}\ncetico: ${a.motivo_cetico}`).join('\n\n')}`,
  { label: 'relator', phase: 'Relatar' })

const notas = ok.filter(x => typeof x.nota === 'number').map(x => x.nota)
return {
  notas: Object.fromEntries(ok.map(x => [x.lente, x.nota])),
  nota_media: notas.length ? Number((notas.reduce((a, b) => a + b, 0) / notas.length).toFixed(1)) : null,
  brutos_n: ok.reduce((s, x) => s + x.achados.length, 0),
  confirmados_n: confirmados.length,
  altas: confirmados.filter(a => a.gravidade === 'alta').length,
  pareceres: ok.map(x => ({ lente: x.lente, nota: x.nota, resumo: x.resumo })),
  confirmados,
  refutados: ok.flatMap(x => x.julgados.filter(a => !a.real).map(a => ({ lente: a.lente, trecho: a.trecho, problema: a.problema, motivo: a.motivo_cetico }))),
  relatorio,
}
