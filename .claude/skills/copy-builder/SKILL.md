---
name: copy-builder
description: Sintetiza copy final do carrossel (8 slides) integrando brief.json + roteiro do carrossel-roteirizador + headlines.json + estrutura do campeão atual + voice-dna. PASSO 4 do workflow v2 — depois do roteirizador, antes do revisor-copy. Acionar quando os 3 inputs (brief + roteiro + headlines) já existem na pasta da semana, ou quando o usuário pedir "monta a copy final", "junta tudo num carrossel", "aplica os 8 slides do campeão".
---

# Copy Builder — Passo 4 do workflow v2

Combina os 3 outputs anteriores em uma copy estruturada de 8 slides aplicando
estrutura do campeão atual, voice-dna, 4 camadas por slide e técnica de headline
escolhida.

## Inputs obrigatórios (lê do disco)
- `SEM{xx}/{slug}/brief.json` (pilar, ângulo, cta_semana)
- `SEM{xx}/{slug}/roteiro.md` (output do carrossel-roteirizador)
- `SEM{xx}/{slug}/headlines.json` (técnica recomendada pro slide 1)

Se faltar qualquer um, parar e indicar qual passo do workflow rodar antes.

## Referências de qualidade (lê do disco)
- Voice DNA: `.claude/skills/voice-dna/dna.md`
- Exemplo canônico (4 camadas): `.claude/skills/carrossel-roteirizador/exemplo-canonico.md`
- Top performer atual: `/Volumes/SSD kenipe/estáticos/novos/SEM18/cliente-que-educa-fecha-concorrencia/` (estrutura, NÃO copiar)

## Workflow

### Passo 1 — Ler os 3 inputs + referências
Carregar tudo pra contexto. Identificar:
- Promessa central do slide 1 (tema da headline)
- Ângulo do brief
- Técnica de headline escolhida (`recomendado_para_slide_1`)
- CTA da semana

### Passo 2 — Estruturar 8 slides aplicando estrutura do campeão

**SLIDE 1 — Capa**
- Headline em Alga (cor POP_HEADLINE), aplicando técnica de headlines.json
- Subtitle em Inter Bold 40px com a promessa específica
- Topo de funil — sem jargão de nicho

**SLIDE 2 — Promessa de valor (4 movimentos)**
- (a) Afirmação categórica que paga a curiosidade da capa
- (b) Negação tripla das falsas saídas (3 coisas que NÃO são a resposta)
- (c) Pivô conceitual (qual é a real lente)
- (d) Estado final + imperativo de identidade

**SLIDES 3–6 — 4 entregas concretas (4 camadas em cada)**
Cada slide precisa cumprir 4 camadas (gabarito do exemplo canônico):
1. Ação concreta (verbo + objeto exato)
2. Mecanismo (cadeia causal)
3. Exemplo vivo (frase pronta, vignette, antes/depois textual)
4. Frame conceitual (metáfora ou polaridade que eleva a regra)

**SLIDE 7 — Prova social**
- Body curto: "Quem entendeu isso, está vivendo essa realidade." (ou variante)
- `prova_slot: true` — imagem virá do prova-social-fetcher (Passo 6)
- Tema da prova marcado (semantic match com slide 5)

**SLIDE 8 — CTA final**
- Headline curta com a chamada (Alga, POP_HEADLINE)
- Body fechando o arco (não vende — sugere)
- `cta_text` = `brief.cta_semana` exato

### Passo 3 — Validar continuidade narrativa (interno)
Antes de gravar, conferir:
- [ ] Promessa do slide 1 entregue nos slides 3-5?
- [ ] Cada slide pede o próximo (gancho explícito)?
- [ ] Sem repetição de ideia entre slides 4 e 5?
- [ ] Slide 2 paga 100% a curiosidade da capa?
- [ ] Slide 7 conecta com a entrega central (não é prova solta)?

Se falhar algum, reescrever o slide afetado ANTES de gravar.

### Passo 4 — Aplicar regras de copy invioláveis
- Sem travessão (—) ou hífen (-) entre palavras
- Sem dado fabricado (estatística sem fonte real)
- Sem vocabulário proibido voice-dna (high ticket, alto ticket, engajamento)
- Sem "Olá", "Oi" ou saudação
- Tom: mentor desafiador, não professor / não par

### Passo 5 — Gravar copy.json
```json
{
  "slug": "...",
  "semana": "SEM19",
  "estrutura_referencia": "cliente-que-educa-fecha-concorrencia",
  "tecnica_headline_aplicada": "Curiosity gap por contradição",
  "primitiva_design_sugerida_por_slide": [
    {"n": 1, "primitiva": "A_hero_perfil"},
    {"n": 2, "primitiva": "B_text_only_short"},
    {"n": 3, "primitiva": "F_text_only_large"},
    {"n": 4, "primitiva": "D_text_body_image_cream"},
    {"n": 5, "primitiva": "F_text_only_large"},
    {"n": 6, "primitiva": "H_text_image_text"},
    {"n": 7, "primitiva": "G_single_image"},
    {"n": 8, "primitiva": "I_cta_final"}
  ],
  "slides": [
    {"n": 1, "tipo": "capa", "headline": "...", "subtitle": "..."},
    {"n": 2, "tipo": "promessa_valor", "body": "..."},
    {"n": 3, "tipo": "entrega_concreta", "headline_ou_topico": "...", "body": "...", "camadas": {"acao": "...", "mecanismo": "...", "exemplo": "...", "frame": "..."}},
    {"n": 4, "tipo": "entrega_concreta", "...": "..."},
    {"n": 5, "tipo": "entrega_concreta", "...": "..."},
    {"n": 6, "tipo": "entrega_concreta", "...": "..."},
    {"n": 7, "tipo": "prova_social", "body": "...", "prova_slot": true, "tema_prova": "..."},
    {"n": 8, "tipo": "cta_final", "headline": "...", "body": "...", "cta_text": "..."}
  ]
}
```

A escolha de primitiva por slide é SUGESTÃO (revisor-design pode ajustar).
Diretrizes:
- Slide 1 sempre A_hero_perfil
- Slide 8 sempre I_cta_final
- Slides com imagem importante → D, E, G, H
- Slides text-only → B, F
- Slide 7 prova social → G_single_image (imagem da prova) ou H_text_image_text

Caminho: `SEM{xx}/{slug}/copy.json`.

### Passo 6 — Reportar
> "copy.json gerado em `SEM{xx}/{slug}/`. Próximo passo: rodar `/revisor-copy`
> pra checar contra checklist obrigatório (5 princípios + voice-dna + 4 camadas
> + continuidade) — checkpoint humano antes do design."

## Anti-padrões
- Copiar copy do top performer literalmente → vira plágio.
- Slide com 2+ ideias → quebra ritmo. Cortar pra 1 ideia.
- Pular alguma das 4 camadas em slide de entrega → manual seco, abaixo do gabarito.
- CTA de venda no meio (slides 3-6) → quebra pacto educativo.
- Headline com jargão de nicho ("preenchimento", "bioestimulador", "harmonização") → estreita o funil cedo demais.
