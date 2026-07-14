---
name: headlines-research
description: Pesquisa headlines reais de portais de notícia top-tier brasileiros (G1, UOL, Folha, Estadão, Veja) sobre o tema do brief. Extrai a TÉCNICA estrutural (curiosity gap, número, contraste, paradoxo, negação+pivô) — DESCARTA o vocabulário sensacionalista. PASSO 3 do workflow v2 — depois do brief, antes ou em paralelo com o carrossel-roteirizador. Acionar quando o usuário pedir "pesquisa de headlines", "técnicas de manchete", "padrões de gancho de portal", ou quando brief.json acaba de ser criado.
---

# Headlines Research — repertório persistente

Extrai PADRÕES estruturais de headlines de portais (nacionais E internacionais)
isolando a técnica do tom. Alimenta o gerador pra construir o slide 1 (capa)
com gancho topo de funil ancorado em padrão validado COM FONTE REAL.

## Fonte primária: o repertório persistente
**Consulte SEMPRE primeiro** `agente-carrosseis/headlines-repertoire.json`
— é a biblioteca de técnicas já pesquisadas, cada uma com estrutura abstrata + exemplos reais (URL)
+ o veredito de performance na nossa conta (`pergunta-paradoxo` e `numero/lista` VENCERAM).
O gerador escolhe uma técnica que case com o tema e ADAPTA a estrutura. Nunca inventa.

Esta skill (pesquisa nova) só roda pra **CRESCER o repertório**: achar exemplo topical novo,
preencher lacuna (hoje `especificidade-concreta` está no piso, 0 nacional), ou registrar técnica
nova. O resultado é APENDADO ao headlines-repertoire.json (com a mesma verificação de fonte),
não sobrescreve. Prioriza ganchos com veredito `venceu`.

## Filtro crítico — técnica sim, vocabulário NÃO

Portais brasileiros usam linguagem sensacionalista que QUEBRA o tom RECONECTA
(editorial, autoridade implícita, sem hipérbole).

Esta skill captura **só a estrutura**:
- Curiosity gap ("Por que X faz Y?")
- Número específico ("3 erros que destroem...")
- Contraste mensurável ("Antes vs depois")
- Paradoxo ("Estratégia que parece errada...")
- Negação seguida de pivô ("Não é X, é Y")
- Pergunta de auto-reconhecimento ("Você está fazendo isso sem perceber?")

E descarta:
- Adjetivos amplificadores ("chocante", "incrível", "brutal")
- Hipérbole verbal ("destrói", "acaba", "muda tudo")
- Apelo emocional explícito ("você precisa ver isso", "não vai acreditar")
- Linguagem corporativa ("revolução", "transformação", "disrupção")
- Clickbait declarado ("o número 7 vai te chocar")

## Workflow

### Passo 1 — Ler brief.json
`SEM{xx}/{slug}/brief.json`. Extrair:
- `pilar` (categoria mental)
- `angulo` (recorte específico)
- Inferir 2-3 termos de busca a partir do ângulo (palavras-chave do tema externo)

### Passo 2 — Buscar headlines em portais top-tier (WebSearch)
Rodar 4-6 queries variadas:
- `"{termo principal}" site:g1.globo.com`
- `"{termo principal}" site:uol.com.br`
- `"{termo conceitual}" site:folha.uol.com.br`
- `"{termo}" site:estadao.com.br`
- `"{termo}" site:veja.abril.com.br`
- `"{categoria do tema}" portal notícias 2025 brasil`

Coletar 12-20 headlines reais. Anotar URL e fonte.

**Não buscar headlines em revistas de nicho de saúde/estética** — elas
contaminam o tom (parecem "a doutora").

### Passo 3 — Filtrar e classificar
Pra cada headline, classificar:
- Estrutura sintática (qual padrão da lista acima?)
- Carga de curiosidade (o que insinua sem revelar?)
- Tem número específico? Qual?
- Anti-padrão presente? Marcar pra DESCARTE.

Reter 8-12 headlines com técnica limpa. Descartar as sensacionalistas.

### Passo 4 — Sintetizar 5-7 padrões aplicáveis
Reduzir as 8-12 retidas em 5-7 padrões abstratos, com:
- **Nome da técnica** (ex: "Curiosity gap por contradição")
- **Estrutura abstrata** (template com lacunas: ex: "Por que [grupo aparentemente certo] [resulta em paradoxo]?")
- **Por que funciona** (1 linha — qual ginástica mental força no leitor)
- **Exemplo aplicado AO TEMA DO BRIEF** (não copy-paste do portal — adapta)
- **Fonte de inspiração** (URL + headline original)

### Passo 5 — Recomendar padrão pro slide 1
Dos 5-7 padrões, escolher 1 mais aplicável ao ângulo do brief. Justificar
em 1 frase.

### Passo 6 — Gravar headlines.json
```json
{
  "slug": "...",
  "tema_busca": "...",
  "fontes_pesquisadas": ["g1.globo.com", "uol.com.br", "folha.uol.com.br"],
  "padrões": [
    {
      "tecnica": "Curiosity gap por contradição",
      "estrutura": "Por que [grupo aparentemente certo] [resulta em paradoxo]?",
      "porque_funciona": "força o leitor a reconciliar duas verdades aparentemente incompatíveis",
      "exemplo_aplicado": "Por que o cliente que você 'educa' acaba fechando com a concorrência?",
      "fonte_inspiração": {
        "url": "https://g1.globo.com/...",
        "headline_original": "Por que empresas que mais investem em treinamento perdem mais funcionários"
      }
    }
  ],
  "recomendado_para_slide_1": "Curiosity gap por contradição",
  "justificativa_recomendacao": "ângulo do brief tem natureza paradoxal (dentista que faz tudo certo perde a venda) — padrão maximiza fricção mental"
}
```

Caminho: `SEM{xx}/{slug}/headlines.json`.

### Passo 7 — Reportar
> "Headlines.json gerado com 5 padrões aplicáveis. Recomendação pro slide 1:
> '{tecnica}'. Próximo passo: rodar `/carrossel-roteirizador` (se ainda não rodou)
> e depois `/copy-builder` que junta tudo."

## Anti-padrões
- Copy-paste literal de headline do portal → contamina tom.
- Manter adjetivos amplificadores ("chocante", "brutal") → fora do voice-dna.
- Buscar em revistas de nicho do tema → enviesa pra linguagem da concorrência.
- Pular o filtro de descarte → headlines.json fica poluído.
- Recomendar mais de 1 padrão pro slide 1 → escolher um, justificar.
