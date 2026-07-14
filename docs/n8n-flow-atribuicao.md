# Flow n8n — captura de atribuição (lead-in → Zoho Deal)

> 2026-06-03. Resposta ao Jardel. Atualiza o passo 1 do projeto (ver
> [captura-atribuicao-v1.md](captura-atribuicao-v1.md) e a spec do produto em
> [utmify-clone-spec.md](utmify-clone-spec.md)).
>
> **Descoberta:** a LP (supercaso.com.br) **já captura** tudo e posta um JSON
> rico no webhook `/webhook/lead-in`. Então não precisa de snippet client-side
> novo — o trabalho é um **flow n8n** que parseia esse payload e grava os campos
> de atribuição no Deal. Os IDs que nunca chegavam no Zoho **já estão no payload**,
> embutidos nas UTMs no formato `ID_Texto`.

---

## 1. Estrutura do flow (novo, sem tocar na produção)

```
[Webhook] (path novo, ex.: /webhook/lead-in-attr   OU   um Webhook de teste)
   │
   ▼
[Code]  "Parsear atribuição"  ← cola o conteúdo de snippets/n8n-parse-atribuicao.js
   │      (split ID_Texto, reconstrói fbc, normaliza source/medium, monta os campos)
   ▼
[Zoho CRM] Upsert Deal  ← faz merge da saída do Code com os campos que você já seta
```

Como o Jardel pediu pra **não quebrar produção**, duas formas de plugar:

- **Opção A (recomendada) — cutover:** o flow novo passa a ser o que cria o Deal
  (Code + sua lógica de qualificação atual). Valida em paralelo apontando a LP
  pra um webhook de teste; quando os campos vierem certos, repointa a LP do
  `/webhook/lead-in` pro novo e aposenta o antigo.
- **Opção B — enriquecimento:** a LP segue postando no flow de produção e
  **também** no flow novo; o flow novo faz `Update Deal` casando por telefone/
  e-mail/`session_id`. Funciona, mas tem risco de corrida (o Deal pode não
  existir ainda quando o update roda) — daí a preferência pela A.

O Code node está em [snippets/n8n-parse-atribuicao.js](snippets/n8n-parse-atribuicao.js)
(modo *Run Once for All Items*). Ele lê de `$json.body` e devolve os campos com
os **api_names exatos** do Deal + um objeto `_capi` com os dados pro CAPI futuro.

---

## 2. Mapa de campos (payload real → Zoho)

| No payload | Parse | → Campo Zoho (1º toque) | → Campo Zoho (último) |
|---|---|---|---|
| `utm_parameters.utm_campaign` | split `ID_nome` | nome → `utm_campaign` / id → `campaign_id` | `utm_campaign_last` / `id_campaign_last` |
| `utm_parameters.utm_term` | split `ID_nome` | nome → `utm_term` | `utm_term_last` / `id_adset_last` |
| `utm_parameters.utm_content` | split `ID_nome` | nome → `utm_content` / id → `ad_id` | `utm_content_last` / `id_ad_last` |
| `utm_parameters.utm_source` | normaliza ig/fb/meta → `meta` | `utm_source` | `utm_source_last` |
| `utm_parameters.utm_medium` | normaliza cpc/social → `paid` | `utm_medium` | `utm_medium_last` |
| `other_parameters.placement` | — | `ad_placement` | — |
| `utm_parameters.fbclid` | `fb.1.<ts>.<fbclid>` | `fb_click_id` | — |
| `body.timestamp` | ISO | — | `dt_last_utm` |
| `body.funil_origem` | — | `funil_origem` (VSL/SE) | — |
| `form_data.classificado` | — | `lead_classification` (Atua +12 etc.) | — |
| fixo | — | `fonte_de_lead = 'Tráfego pago'` | — |

> Mapeamento dos IDs Meta confirmado pelos nomes: **campanha** = `utm_campaign`
> ("VSL | Teste | CBO"), **conjunto/adset** = `utm_term` ("AB - Aberto" = teste/
> segmentação), **anúncio/ad** = `utm_content` ("AD0014_1F" + headline do criativo).
> Não há campo de 1º toque pra adset no Zoho — por isso `adset_id` vai só pro
> `id_adset_last`.

---

## 3. Exemplo resolvido (lead "Priscila Codina" do payload do Jardel)

```json
{
  "utm_source": "meta",
  "utm_medium": "paid",
  "utm_campaign": "VSL | Teste | CBO | Programar",
  "utm_term": "[26] [SEM_20] - [AD0014] AB - Aberto",
  "utm_content": "[26] [20] [AD0014_1F] - A fixação por mostrar o que sabe",
  "campaign_id": "120245620450500505",
  "id_adset_last": "120245951888880505",
  "ad_id": "120245951918420505",
  "ad_placement": "Instagram_Feed",
  "fb_click_id": "fb.1.1780488042101.PAZXh0bgNhZW0BMABhZGlkAaszEPU9oflz...",
  "dt_last_utm": "2026-06-03T12:00:42.101Z",
  "funil_origem": "VSL",
  "lead_classification": "Atua +12",
  "fonte_de_lead": "Tráfego pago",
  "utm_source_last": "meta", "utm_medium_last": "paid",
  "utm_campaign_last": "VSL | Teste | CBO | Programar",
  "id_campaign_last": "120245620450500505",
  "id_ad_last": "120245951918420505",
  "_capi": {
    "fbclid": "PAZXh0bgNhZW0B...", "fbc": "fb.1.1780488042101.PAZ...",
    "ip": "177.26.253.59", "user_agent": "Mozilla/5.0 (iPhone; ...)",
    "email": "pricodina@gmail.com", "phone": "5511995696410",
    "session_id": "57bbca38-213d-4bd7-a157-c51559680d9c"
  }
}
```

---

## 4. Bug pra corrigir na origem (não bloqueante)

A URL de destino do anúncio está gerando `?` duplicado:
`/treinamento-gratis?%3Futm_source=Meta&...` (o `%3F` é um `?` a mais). Por isso
o `utm_source=Meta` do template da Meta virou a chave quebrada `?utm_source` em
`other_parameters`, e sobrou um `utm_source=ig` hardcoded na LP. O parser
contorna (normaliza tudo pra `meta`), mas o certo é **tirar o `?`/`%3F` extra**
da URL de destino do anúncio pra query string vir limpa.

---

## 5. Preparação pro CAPI (passo 4 do plano, não é agora)

O objeto `_capi` carrega o que a conversão offline pro Meta vai precisar quando o
Deal virar "Ganho": `fbc`, `ip`, `user_agent`, `email`, `phone`, `session_id`.
Hoje **não há campo no Zoho** pra ip/ua/fbp/session_id. Recomendação leve: criar
um campo texto `fbp` (e opcionalmente `ip`/`session_id`) no Deal pra elevar o
match quality do CAPI. O `fb_click_id` já existe e já basta pra começar.

---

## 6. Aceite

1. Disparar o payload de teste no webhook novo → conferir no Zoho o Deal com
   `campaign_id`/`id_adset_last`/`ad_id` preenchidos e `fb_click_id` no formato
   `fb.1.<ts>.<fbclid>`.
2. 48h após o go-live, rodar a COQL de cobertura (`campaign_id is not null`) e ver
   a taxa sair de ~0%.
3. Lead de social seller continua entrando com `fonte_de_lead = 'Fábrica de
   Contatos'`, sem UTM, fora do CAC pago.
