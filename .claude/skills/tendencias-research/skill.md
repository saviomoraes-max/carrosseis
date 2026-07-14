---
name: tendencias-research
description: Busca assuntos em alta (notícias, comportamento de consumo, negócio de clínica/estética) e roda cada candidato pelo filtro de relevância do nicho ANTES de virar candidato a carrossel. Tendência que não conversa com o público é DESCARTADA e logada, nunca adaptada na marra. Roda a cada 1-3 dias. Acionar quando o usuário pedir "tendências", "o que está em alta", "temas da semana", ou para abastecer a fila do gerador de carrossel.
---

# Tendências Research — Fase 1 do agente de carrosséis

Abastece a fila de temas do gerador. NÃO inventa tema: parte de assunto real em alta e só
deixa passar o que o filtro de relevância aprovar. Zero achismo.

## Inputs
- `agente-carrosseis/relevance-filter.json` (público, dores, temas priorizados, rubrica, gate)
- `agente-carrosseis/voice-spec.md` (o que aumentar/reduzir)

## Workflow

### Passo 1 — Coletar candidatos (WebSearch)
Buscar assuntos em alta no MUNDO ADJACENTE ao público (não notícia genérica):
- Negócio/gestão de clínica e estética, economia da beleza, comportamento do consumidor de estética
- Marketing/vendas para profissionais de saúde, posicionamento, atendimento
- Mudanças de plataforma (Instagram, regras de anúncio) que afetam captação
- Datas/sazonalidade que mexem com a agenda da clínica

Rodar 5-8 queries variadas (ex: `tendência estética 2026`, `comportamento consumidor beleza`,
`captação de pacientes`, `economia da beleza brasil`). Coletar 12-20 candidatos com fonte/URL.
NÃO buscar fofoca de celebridade nem assunto de paciente leigo.

### Passo 2 — Rodar o filtro de relevância
Para CADA candidato, aplicar a `rubrica_de_pontuacao` do relevance-filter.json:
pontuar `conecta_dor_ou_desejo`, `mapeia_tema`, `ancoravel_em_gancho_vencedor`, `sem_distorcao`.
Aplicar o GATE. Quem reprova vai pra lista de DESCARTADOS com o motivo (transparência).

### Passo 3 — Priorizar
Os aprovados sobem na fila por prioridade do tema mapeado: temas `aumentar`
(indicação, recorrência, perfil-que-atrai, prospecção) primeiro; `reduzir` só com ângulo novo.

### Passo 4 — Gravar a fila
`agente-carrosseis/data/trends-queue.json`:
```json
{
  "rodado_em": "<data>",
  "aprovados": [
    {
      "tema_candidato": "...",
      "fonte": {"titulo": "...", "url": "..."},
      "tema_mapeado": "indicacao / follow-up",
      "prioridade": "alta",
      "dor_ou_desejo_conectado": "...",
      "por_que_relevante": "...",
      "gancho_vencedor_sugerido": "pergunta-paradoxo | numero/lista",
      "pontuacao": {"conecta": 3, "mapeia": 3, "ancoravel": 2, "sem_distorcao": 3}
    }
  ],
  "descartados": [{"tema": "...", "motivo": "não conecta dor / exige distorção / cultura-pop sem ponte"}]
}
```

### Passo 5 — Reportar
Resumo: N aprovados (com o tema mapeado e prioridade), N descartados (com motivo).
Os aprovados ficam disponíveis pro `gerador-carrossel`.

## Agendamento
Roda a cada 1-3 dias. **Mecanismo a confirmar com o usuário** (não criar automação recorrente
sem ok): opções = LaunchAgent local que invoca o Claude, rotina de nuvem (skill `schedule`),
ou disparo manual. Até definir, rodar sob demanda.

## Anti-padrões
- Forçar uma tendência que não conecta ("adaptar na marra") → DESCARTAR e logar.
- Trazer fofoca de celebridade sem ponte real com uma dor → o tema "analogia-celebridade" só existiu na conta.
- Tema de paciente leigo (público final), não da doutora → descartar.
- Pular o log de descartados → o usuário precisa ver o que foi cortado e por quê.
