---
name: brief
description: Coleta inputs estruturados pra um carrossel novo (pilar da semana, slug, ângulo, CTA), checa canibalização contra as últimas 4 SEMxx, e grava brief.json. PRIMEIRO passo do workflow v2 — sempre roda antes do carrossel-roteirizador. Acionar quando o usuário pedir um carrossel novo, "vamos começar o carrossel", "novo carrossel sobre X", iniciar a fase de copy semanal, ou apresentar tema novo sem brief estruturado.
---

# Brief — Passo 1 do workflow de carrossel v2

Abre o pipeline. Coleta os 4 inputs estruturados, valida contra os pilares da
metodologia, checa canibalização nas últimas 4 SEMxx e grava brief.json na
pasta da semana.

## Fontes de verdade
- Pilares da metodologia: `carrosseis/pilares.md`
- Pasta semanal raiz (criada por launchd aos domingos): `/Volumes/SSD kenipe/estáticos/novos/SEM{xx}/`

## Workflow

### Passo 1 — Identificar pilar da semana
Ler `pilares.md`. Localizar `## Pilar da semana`. Extrair o pilar marcado pra
SEM atual (formato `**SEM{xx} ({data}):** Nome do Pilar`).

Se estiver `_a definir_`, parar e perguntar ao usuário qual pilar (válidos:
**Fábrica de Contatos**, **SUPERCASO**, **Agenda do Milhão**, **Presente Inaceitável**).

### Passo 2 — Coletar 3 inputs do usuário
Pergunte (ou capture do contexto):
1. **slug** — kebab-case descrevendo o tema (ex: `paciente-que-fecha-na-segunda`)
2. **angulo** — 1 linha, recorte específico do pilar (ex: "consulta começando com 'me conta sua história' fecha mais")
3. **cta_semana** — texto exato (ex: "CLIQUE NO LINK DA BIO", "COMENTA SUPERCASO")

Se faltar qualquer um → perguntar ANTES de seguir. Brief sem ângulo = roteirizador chuta.

### Passo 3 — Calcular SEM atual
`date +%V` retorna semana ISO (ex: `19`). Pasta de destino:
`/Volumes/SSD kenipe/estáticos/novos/SEM{xx}/{slug}/`

Se a pasta SEM{xx} não existe, criar (raro — launchd cuida disso aos domingos).
Se a pasta `{slug}` JÁ existe, parar e avisar — provavelmente sobrescrita acidental
(memória `feedback_nao_sobrescrever_carrossel.md` proíbe sobrescrita).

### Passo 4 — Checar canibalização
Listar `SEM{xx-1}/*/brief.json` até `SEM{xx-4}/*/brief.json` (4 semanas pra trás).
Para cada brief.json existente, comparar:
- `pilar` igual ao novo?
- `angulo` semanticamente próximo (mesmo recorte, mesma promessa)?

Se MATCH (mesmo pilar + ângulo sobreposto), avisar:
> "Carrossel SEM{yy}/{slug-existente} já cobriu ângulo similar ('...'). Quer ajustar o ângulo novo ou seguir mesmo assim?"

Aguardar decisão antes de gravar.

### Passo 5 — Criar pasta e gravar brief.json
Criar:
- `SEM{xx}/{slug}/`
- `SEM{xx}/{slug}/img/`
- `SEM{xx}/{slug}/slides/`

Gravar `SEM{xx}/{slug}/brief.json`:
```json
{
  "slug": "paciente-que-fecha-na-segunda",
  "semana": "SEM19",
  "data_inicio_iso": "2026-05-04",
  "pilar": "Presente Inaceitável",
  "angulo": "consulta começando com 'me conta sua história' fecha mais que pitch técnico",
  "cta_semana": "CLIQUE NO LINK DA BIO",
  "criado_em": "2026-05-07T11:30:00",
  "estado_atual": "brief_concluido",
  "canibalizacao_check": "ok"
}
```

### Passo 6 — Reportar e indicar próximo
Mensagem ao usuário:
> "Brief criado em `SEM{xx}/{slug}/brief.json`. Pasta `img/` pronta pra você
> depositar imagens. Próximo passo: rodar `/carrossel-roteirizador` com o
> ângulo deste brief. Quer que eu já chame?"

## Output
- `SEM{xx}/{slug}/brief.json`
- `SEM{xx}/{slug}/img/` (vazia, pra usuário depositar)
- `SEM{xx}/{slug}/slides/` (vazia, será preenchida no export)

## Anti-padrões
- Criar brief sem pilar marcado → bloquear, perguntar pilar.
- Sobrescrever brief.json existente → bloquear, criar novo slug.
- Gravar fora da pasta da semana ISO atual → erro.
- Aceitar ângulo genérico ("vender mais", "atender melhor") → empurrar pra recorte específico.
