---
name: revisor-copy
description: Valida copy.json contra checklist obrigatório (5 princípios do time + voice-dna + 4 camadas + continuidade narrativa + sem dados fabricados + sem travessão). PASSO 5 do workflow v2 — checkpoint humano antes de seguir pro design. Reprovação aponta slide específico e propõe diff focado, NÃO refaz o carrossel inteiro. Acionar quando copy.json acaba de ser gerada, ou quando o usuário pedir "revisar copy", "checa se tá ok", "passa pelo checklist".
---

# Revisor Copy — Passo 5 do workflow v2 (CHECKPOINT 1)

Roda checklist obrigatório contra a copy gerada pelo copy-builder. Em caso de
reprovação: aponta slide específico → propõe diff → **espera usuário aprovar**.
Não refaz o carrossel inteiro nem segue pro próximo passo automaticamente.

## Inputs
- `SEM{xx}/{slug}/copy.json`

## Referências
- 5 princípios do time: memória `feedback_carrossel_5_principios_time.md`
- Voice DNA: `.claude/skills/voice-dna/dna.md`
- 4 camadas (gabarito): `.claude/skills/carrossel-roteirizador/exemplo-canonico.md`
- Regras invioláveis: `carrosseis/_template/primitivas.json` (seção `regras_invioláveis`)
- Sem travessão: memória `feedback_sem_travessao.md`
- Sem dado fabricado: memória `feedback_nunca_inventar_dados.md`
- Tom humano: memória `feedback_tom_de_comunicacao.md`

## Workflow

### Passo 1 — Ler copy.json + carregar referências
Validar JSON estruturalmente (8 slides com tipos esperados). Se quebrado, parar.

### Passo 2 — Rodar checklist por slide

#### Globais (TODOS os 8 slides)
- [ ] Sem travessão (—) ou hífen (-) entre palavras no meio de frase?
- [ ] Sem dado fabricado (% ou número sem fonte real)?
- [ ] Vocabulário voice-dna respeitado (zero "high ticket", "alto ticket", "engajamento", "algoritmo", "solução", "ecossistema")?
- [ ] Tom mentor-desafiador (não professor, não par sofrendo junto)?
- [ ] Sem autoelogio ("sou o melhor", "diferente dos outros", "meu método é único")?

#### Slide 1 (capa)
- [ ] Headline topo de funil (sem jargão de nicho — "preenchimento", "bioestimulador", "harmonização")?
- [ ] Cria curiosity gap (insinua sem revelar)?
- [ ] Aplica técnica de `headlines.json` (campo `tecnica_headline_aplicada`)?
- [ ] Subtitle promete benefício específico (não vago)?

#### Slide 2 (promessa de valor — 4 movimentos)
- [ ] (a) Afirmação categórica paga a curiosidade da capa?
- [ ] (b) Negação tripla das falsas saídas (3 coisas que NÃO são)?
- [ ] (c) Pivô conceitual claro?
- [ ] (d) Estado final + imperativo de identidade?

#### Slides 3–6 (entregas concretas — 4 camadas)
Pra CADA slide:
- [ ] Camada 1: ação concreta (verbo + objeto exato)?
- [ ] Camada 2: mecanismo (cadeia causal — o que acontece se fizer/não fizer)?
- [ ] Camada 3: exemplo vivo (frase pronta, vignette, antes/depois textual)?
- [ ] Camada 4: frame conceitual (metáfora ou polaridade)?
- [ ] 1 ideia central por slide (não duas)?
- [ ] Termina puxando o próximo (gancho explícito)?

#### Slide 7 (prova social)
- [ ] Body curto introduz a prova de forma natural?
- [ ] `prova_slot: true` no JSON?
- [ ] `tema_prova` definido pra busca semântica do prova-social-fetcher?

#### Slide 8 (CTA final)
- [ ] `cta_text` bate exatamente com `brief.cta_semana`?
- [ ] Body fecha o arco (sugere, não vende — sem "matricule-se", "compre", "garante")?
- [ ] Sem handles (@oleonardorosso, @mentoriareconecta) — regra `feedback_cta_sem_handles.md`?

#### Continuidade narrativa (cross-slide)
- [ ] Promessa do slide 1 entregue nos slides 3-5?
- [ ] Sem repetição de ideia entre slides 4 e 5?
- [ ] Cada slide intermediário pede o próximo?
- [ ] Slide 7 conecta semanticamente com a entrega central (não é prova solta)?

### Passo 3 — Output revisao-copy.md

#### Cenário A: TUDO PASSA
```markdown
# Revisão de copy — SEM{xx}/{slug}

## Status: ✅ APROVADO

Todos os critérios passam. Pode seguir pro Passo 6 (`/prova-social-fetcher`)
e depois pra fase de design.

## Resumo do que foi validado
- 5 princípios do time ✓
- Voice DNA (tom + vocabulário proibido) ✓
- 4 camadas em cada slide de entrega (3-6) ✓
- Continuidade narrativa entre slides ✓
- Regras invioláveis (sem travessão, sem dado fabricado, sem handles no CTA) ✓
```

#### Cenário B: ALGO FALHA
```markdown
# Revisão de copy — SEM{xx}/{slug}

## Status: ❌ REPROVADO ({N} falhas em {M} slides)

### Falhas encontradas

#### Slide 4 — Critério "4 camadas: falta camada 3 (exemplo vivo)"
**Texto atual:**
> "Aprofunde a consequência da dor."

**Diff proposto:**
> "Aprofunde a consequência. Pergunte: 'Como você se sente ao ver isso no
> espelho todos os dias?'. A resposta dela mostra o tamanho real do problema
> que ela vinha minimizando."

**Por quê:** atual tem só camada 1 (ação) + 2 (mecanismo implícito). Camada 3
exige frase pronta / vignette concreta. Adicionado também frame conceitual
("tamanho real do problema").

---

#### Slide 7 — Critério "sem travessão"
**Texto atual:**
> "Quem entendeu isso — está vivendo essa realidade."

**Diff proposto:**
> "Quem entendeu isso, está vivendo essa realidade."

**Por quê:** memória `feedback_sem_travessao.md` proíbe travessão entre palavras.

---

[continua pra cada falha]

## Próximo passo
Aprovar os diffs acima individualmente ou em bloco. Após aprovação, eu aplico
em `copy.json` e re-rodo este revisor pra confirmar status APROVADO.
```

Caminho: `SEM{xx}/{slug}/revisao-copy.md`.

### Passo 4 — CHECKPOINT 1 (esperar humano)
**Não seguir pro próximo passo do workflow automaticamente.**

Se status = APROVADO → indicar próximo (`/prova-social-fetcher`) mas aguardar
luz verde explícita do usuário.

Se status = REPROVADO → aguardar:
- "aprovo todos os diffs" → aplicar tudo + re-rodar revisor
- "aprovo só o slide X" → aplicar só esse + re-rodar
- "rejeita esse, faz assim" → escutar nova proposta, atualizar diff

## Anti-padrões
- Marcar pass num critério sem evidência clara → checklist vira teatro.
- Reescrever slide inteiro quando só falta 1 camada → diff focado.
- Aprovar com warnings ("passou, mas...") → pass ou fail, sem zona cinza.
- Seguir pro próximo passo sem aprovação humana → quebra checkpoint.
- Ignorar continuidade narrativa porque cada slide isolado passa → revisão tem que olhar o conjunto.
