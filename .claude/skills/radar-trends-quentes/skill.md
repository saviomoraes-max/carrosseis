---
name: radar-trends-quentes
description: Radar DIÁRIO de notícias quentes e momentos virais (celebridade, esporte, TV, cultura pop, plataforma) com ponte real pro nicho de clínica/estética — o alimentador do slot "~10% notícia em alta" do mix editorial. Diferente da tendencias-research (evergreen de negócio): aqui fofoca/celebridade/esporte ENTRAM, desde que a ponte exista sem distorção e a janela seja ≤72h. Caso-canon: Vini Jr SEM30/AD002 (20/jul/26). Acionar quando o usuário pedir "radar", "roda o radar", "tem notícia quente hoje?", ou via LaunchAgent com.reconecta.radar-quente.
---

# Radar de Trends Quentes — alimentador do slot notícia-em-alta

O objetivo NÃO é achar "assunto do dia": é achar a história quente que consiga virar
um carrossel no playbook do Vini Jr — **a notícia vira a CENA do slide 1 (TOFU
natural) e o NOSSO ensino entra do slide 3+** (checklist-producao §5-B). Zero achismo:
todo fato com fonte, hora e etiqueta de confiança.

## Inputs (ler antes de buscar)
- `agente-carrosseis/relevance-filter.json` — público, dores-núcleo, desejos, temas priorizados
- `agente-carrosseis/data/radar-quente.json` — histórico (não repropor candidato já reportado/descartado)
- Pastas `SEM{semana atual}` em `/Volumes/SSD kenipe/estáticos/novos/` (fallback `./producao/`) — o que JÁ virou post não volta (caso: não repropor Vini Jr depois do AD002)
- `agente-carrosseis/checklist-producao.md` §5-B — as regras do slot

## Passo 1 — Varredura multi-modal (WebSearch/WebFetch, PT-BR, últimas 24-72h)
Rodar TODOS os recortes (cada um é um ângulo cego dos outros):
1. **Celebridade × estética**: famoso + harmonização/procedimento/antes-depois/rosto novo (portais: Leo Dias, Hugo Gloss, Metrópoles celebridades, CNN pop, Quem, Caras)
2. **Esporte × visual**: jogador/atleta + rosto/visual/transformação; seleção; grandes eventos
3. **TV/reality/streaming**: BBB, Fazenda, novelas, documentário do momento — cena que o Brasil comentou
4. **O assunto do dia**: "mais comentado" geral (Google News BR destaque, buscas de trends) — mesmo fora de estética, se a MECÂNICA da história ilustrar nosso ensino (caso Spotify: experiência/escolha)
5. **Plataforma/mercado quente**: mudança de Instagram/Meta/WhatsApp com efeito em captação AGORA (não evergreen)
6. **Sazonalidade da semana**: data comemorativa/evento nos próximos 7-10 dias que mexa com agenda de clínica
Datar TUDO (dia + hora quando houver). Etiquetar cada fato: confirmado / reportado (por quem) / especulação.

## Passo 2 — Filtro RADAR (rubrica binária por candidato; reprovou = DESCARTADO com motivo)
- **JANELA**: pico ≤72h atrás OU ainda subindo. Notícia de 4+ dias = morta (caso Spotify, morto por timing em 06/jul). Registrar "estourou em: <data/hora>" e "postável até: <data>".
- **PONTE SEM DISTORÇÃO**: qual dor/tema do relevance-filter a história ILUSTRA de verdade? A ponte precisa caber no arco: notícia = cena TOFU do slide 1-2; mecanismo NOSSO (com tema mapeado do corpus) entra do slide 3+. Se precisar torcer a história pra caber = descarte ("nunca adaptar tendência na marra").
- **RISCO DE MARCA**: camada racial/identitária, deboche de pessoa real, tragédia, julgamento de rosto/corpo de terceiro, ética CFO/CFM (análise clínica de quem não é paciente) → descarte, ou ressalva explícita de como contornar (caso Vini: zero julgamento do resultado, zero memes, procedimento nunca nomeado como fato nosso).
- **FATOS**: 3-6 fatos com fonte+URL+data/hora e a quem atribuir (caso Vini: "segundo o portal Leo Dias"). Fato-perecível (ex: "fulano não se pronunciou") marcado como PERECÍVEL com hora do corte.

## Passo 3 — Mini-ponte (só pros top 1-3 aprovados)
Por candidato aprovado, esboçar SEM produzir o post:
- `hero_candidato`: pergunta/gancho TOFU, creme integral (sem cor), 3-4 linhas CURTAS (≤16 chars/linha de preferência — hero grande)
- `cena_slide2`: a notícia em 1-2 frases de cena (com o fato mais forte)
- `mecanismo_ancora`: tema mapeado + peça do corpus que ancora o ensino (ex: "indicação/confiança → SEM25/AD005 'confiança não se anuncia'") — consultar `agente-carrosseis/headlines-repertoire.json` bloco `queimadas` (frase/família queimada não pode ancorar punch)
- `prova_sugerida`: tema de print que casa com a tese
- `ressalvas`: minas + fatos perecíveis + o que re-checar antes de produzir

## Passo 4 — Gravar `agente-carrosseis/data/radar-quente.json`
```json
{
  "rodado_em": "<YYYY-MM-DD HH:MM>",
  "alerta": true,
  "resumo_1_linha": "<pro aviso: '1 candidato quente: X (janela até sexta)' ou 'sem candidato hoje'>",
  "candidatos": [{
    "titulo": "...", "estourou_em": "...", "postavel_ate": "...",
    "rubrica": {"janela": "ok", "ponte": "indicacao/confianca", "risco_marca": "baixo|ressalvas", "fatos": 4},
    "fatos": [{"fato": "...", "fonte": "...", "url": "...", "quando": "...", "confianca": "reportado", "perecivel": false}],
    "mini_ponte": {"hero_candidato": "...", "cena_slide2": "...", "mecanismo_ancora": "...", "prova_sugerida": "...", "ressalvas": "..."}
  }],
  "descartados": [{"tema": "...", "motivo": "janela morta | sem ponte | risco de marca | já produzido"}]
}
```
`alerta: false` + `resumo_1_linha: "sem candidato hoje"` é resultado VÁLIDO e frequente —
o slot vira validado (§5-B). Nunca forçar candidato fraco pra "ter o que reportar".

## Passo 5 — Reportar (stdout, o runner entrega o aviso)
Imprimir SÓ: a linha `RADAR: <resumo_1_linha>` + top candidato (título, janela, ponte,
hero_candidato) em ≤6 linhas. O runner (`run-radar.sh`) manda isso pro Slack/notificação.

## Regras duras
- Radar APONTA, nunca produz: produção de post só com OK do Sávio (mini-ponte é esboço).
- Zero achismo: sem fonte+data = não é fato, não entra.
- Custo consciente: ~10-15 buscas bem miradas; não varrer a internet inteira.
