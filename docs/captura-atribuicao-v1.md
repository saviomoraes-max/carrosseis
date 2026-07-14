# Captura de Atribuição v1 — especificação para o time de dev

> Documento operacional — 2026-06-03. Passo 1 do projeto "UTMify interno".
> Objetivo: **fazer toda nova venda voltar a gravar a origem do anúncio no Zoho**,
> e desta vez com o que nunca foi capturado: os **IDs** de campanha/conjunto/anúncio
> e o **fbclid** (necessário pro Meta CAPI). Spec técnica completa do produto em
> [utmify-clone-spec.md](utmify-clone-spec.md).

> **ATUALIZAÇÃO 2026-06-03 (após retorno do Jardel):** a LP (supercaso.com.br) **já
> captura** tudo e posta um JSON rico no webhook `/webhook/lead-in` (UTMs com IDs no
> formato `ID_Texto`, fbclid, IP, UA). Então a captura **client-side já existe** — o
> snippet da seção 3 vira referência/fallback pra LPs futuras que não tenham isso. O
> trabalho real é o **flow n8n** que parseia o payload e grava no Deal:
> ver **[n8n-flow-atribuicao.md](n8n-flow-atribuicao.md)** (mecanismo oficial deste passo).
> As seções 2 (template Meta), 4 (mapa de campos), 5 (segmentação), 6 (backfill) e
> 7 (LGPD) continuam valendo.

---

## 0. Diagnóstico que motivou esta spec (dados reais do Zoho)

- A gravação de UTM no Deal **parou em ~08/jan/2026** (os campos saíram do layout). De lá pra cá: **0 de 5.567 negócios novos** têm origem; os **131 ganhos** dos últimos 90 dias estão cegos.
- Mesmo quando funcionava, capturava só os **nomes** (`utm_campaign`, `utm_source="ig"`), **nunca os IDs** (`campaign_id`, `id_adset_last`, `id_ad_last` sempre nulos) e **`fb_click_id` = 0 em toda a base**.
- Sujeira de dado: `utm_source` ora "ig" ora "IG"; `utm_medium` ora "cpc" ora "paid" ora "social".

Recolocar os campos no layout (já planejado pelo dev) ressuscita só os nomes. Esta spec adiciona **IDs + fbclid + nomenclatura limpa**, que é o que torna o dado utilizável pra CAC real por ID e pro CAPI.

---

## 1. Os três componentes da captura

```
[Meta]  Template de "Parâmetros de URL" no anúncio   → injeta nomes E IDs na URL
   │
   ▼
[LP]    reconecta-attribution.js no <head>           → lê URL+cookies, persiste,
   │                                                    preenche o form (campos ocultos)
   ▼
[Zoho]  Campos de tracking no layout do Deal          → recebem e armazenam a origem
```

Os três precisam estar alinhados nos **mesmos nomes de campo**. É isso que a spec trava.

---

## 2. Componente Meta — template de Parâmetros de URL

No Gerenciador de Anúncios, em cada anúncio (ou via regra de conta), no campo
**"Parâmetros de URL"** (nível do anúncio → "Rastreamento" → Parâmetros de URL),
cole **exatamente** isto (sem `?`, sem a URL — só a string de parâmetros):

```
utm_source=meta&utm_medium=paid&utm_campaign={{campaign.name}}&utm_term={{adset.name}}&utm_content={{ad.name}}&campaign_id={{campaign.id}}&adset_id={{adset.id}}&ad_id={{ad.id}}&placement={{placement}}
```

Por que assim:
- `utm_source=meta` e `utm_medium=paid` **fixos e minúsculos** — mata a bagunça "ig/IG/cpc/social". A origem fina vem nos outros campos.
- Os `{{...}}` são macros que a Meta substitui na entrega pelos valores reais.
- Mandamos **nome e ID separados** (`utm_campaign` = nome, `campaign_id` = ID). Isso casa com os campos que já existem no Zoho e permite cruzar com o gasto por **ID** (estável; nome muda quando você renomeia a campanha).
- O `fbclid` a Meta **anexa sozinho** ao clique — não precisa estar no template. O snippet lê.

> Regra de nomenclatura nos nomes de campanha/conjunto/anúncio: **nunca** usar
> os caracteres `| # & ?` (quebram a query string). Manter o padrão atual
> ("AQUISIÇÃO - Lead+12 - ...") está ok.

---

## 3. Componente LP — instalar o snippet

Arquivo: [snippets/reconecta-attribution.js](snippets/reconecta-attribution.js).

1. Hospedar o arquivo (CDN/own) e incluir no `<head>` de **todas** as páginas do funil pago:
   ```html
   <script src="https://SEU-CDN/reconecta-attribution.js" async></script>
   ```
   (ou colar inline). Tem que estar em **todas** as páginas, não só a primeira — senão a origem se perde na navegação até o form.
2. Ajustar no topo do arquivo `CONFIG.cookieDomain` para o domínio raiz das LPs
   (ex.: `".reconectaoficial.com.br"`) pra o cookie sobreviver entre subdomínios.
3. Garantir que o **Pixel da Meta** está na página (o snippet aproveita os cookies
   `_fbp`/`_fbc` que o pixel cria; sem pixel, ele ainda reconstrói o `fbc` do `fbclid`).

O snippet preenche `<input type="hidden">` cujos `name` são os **api_name do Zoho**
(lista na seção 4). Se o form não tiver esses inputs, ele os cria
(`autoCreateHiddenInputs: true`).

### Como o form chega no Zoho
- **Se for Zoho WebForm nativo:** os campos da seção 4 precisam estar no formulário/layout (o dev já vai recolocar). Os `name` dos hidden inputs já batem com os api_name.
- **Se for form custom → n8n → API do Zoho:** o n8n recebe os campos com esses mesmos nomes no payload e mapeia pros api_name do Deal. (Validar payload antes de criar o registro, conforme CLAUDE.md.)

---

## 4. Componente Zoho — mapa de campos (já existem todos no módulo Deals)

| Capturado | → Campo Zoho (1º toque) | → Campo Zoho (último toque) |
|---|---|---|
| `utm_source` | `utm_source` | `utm_source_last` |
| `utm_medium` | `utm_medium` | `utm_medium_last` |
| `utm_campaign` | `utm_campaign` | `utm_campaign_last` |
| `utm_content` | `utm_content` | `utm_content_last` |
| `utm_term` | `utm_term` | `utm_term_last` |
| `campaign_id` | `campaign_id` | `id_campaign_last` |
| `adset_id` | *(não há campo de 1º toque)* | `id_adset_last` |
| `ad_id` | `ad_id` | `id_ad_last` |
| `fbclid` → `fbc` | `fb_click_id` | — |
| `placement` | `ad_placement` | — |
| timestamp do toque | — | `dt_last_utm` |

Tudo isso **já existe** no layout do Deal (288 campos no módulo). Ação do dev:
**recolocar esses campos no layout** ativo e garantir que aceitam escrita pela
origem do form. Os campos `_cal` (`fb_click_id_cal`, `utm_*_cal`) são de outra
ferramenta (booking/calendário) — não mexer.

> **Pendência a criar (1 campo novo):** não existe campo `fbp` no Zoho. O `_fbp`
> melhora o match do CAPI. Recomendo criar um campo texto `fbp` no Deal e
> adicionar a linha no `MAP_FIRST` do snippet. Não é bloqueante pro MVP (fbc +
> email + telefone já dão match razoável).

---

## 5. Segmentação pago × orgânico (regra de ouro do dashboard)

Nem todo negócio é de tráfego pago — os das **social sellers** ("fábrica de
contatos") são criados manualmente e **não têm gasto de anúncio**. Não podem
entrar no CAC por campanha. O campo limpo pra isso é **`fonte_de_lead`**:

- **Entra no CAC pago:** `fonte_de_lead = 'Tráfego pago'` **OU** `campaign_id` preenchido.
- **Fica de fora (orgânico/manual):** `Fábrica de Contatos`, `Tráfego orgânico`, `Indicação cliente`, `Indicação time`, `Outbound`, `Reengajamento`, `Campanhas WhatsApp`, `Campanhas Email`, etc.

Para os leads de social seller, o sub-canal fica em `fonte_social_seller`
(Novo seguidor / DM / Comentário / Reação / Menção) — preservar pra análise
separada, fora do funil pago.

> Garantir que o lead pago **sempre** receba `fonte_de_lead = 'Tráfego pago'`
> (pode ser default do form da LP), e o de social seller `= 'Fábrica de Contatos'`.

---

## 6. Backfill retroativo (cuidado)

O time vai backfillar retroativo. Dois alertas:
1. Os negócios pré-jan/2026 têm **nomes mas não IDs**; o cruzamento com gasto
   por ID não vai existir pra eles (só por nome, que é frágil). Tratar o
   histórico como "melhor esforço" e considerar a atribuição confiável a partir
   do go-live da captura nova.
2. **Não** backfillar `fonte_de_lead = 'Tráfego pago'` em negócio que veio de
   fábrica de contatos/indicação — isso inflaria o CAC pago com venda orgânica.

---

## 7. LGPD

O snippet coleta `fbclid`, cookies da Meta e (no servidor) IP/UA — isso é dado
pessoal. Requisitos:
- Banner de consentimento na LP antes de disparar pixel/captura.
- Base legal registrada; hash de e-mail/telefone quando esses dados forem pro CAPI.
- Política de retenção dos campos de tracking.

---

## 8. Critérios de aceite (QA antes de declarar consertado)

1. Subir um anúncio de teste com o template da seção 2 → clicar → preencher o
   form da LP → conferir no Zoho que o Deal nasceu com `utm_source=meta`,
   `utm_medium=paid`, `utm_campaign` = nome real, **`campaign_id`/`adset_id`/`ad_id` preenchidos** e **`fb_click_id` no formato `fb.1.<ts>.<fbclid>`**.
2. Navegar LP → VSL → checkout antes de enviar o form → a origem **sobrevive** (cookie/localStorage).
3. Segundo clique de outra campanha → `*_last` atualiza, primeiro toque **não** muda.
4. Lead criado por social seller → `fonte_de_lead = 'Fábrica de Contatos'`, sem UTM, **não** aparece no CAC pago.
5. Rodar a COQL de cobertura (abaixo) 48h depois e ver a taxa subir de ~0%.

```sql
-- cobertura de atribuição nos negócios novos (rodar no COQL do Zoho)
select COUNT(id) from Deals
where Created_Time >= 'AAAA-MM-DDT00:00:00-03:00' and campaign_id is not null
```

---

## 9. O que vem depois (não é deste passo)

Com a captura consertada e a cobertura subindo, seguem os passos 3–5 do plano:
sync do gasto da Meta por ID, dashboard de CAC real / ROAS real / ciclo médio por
campanha, e conversão offline pro Meta CAPI quando o Deal vira "Ganho". Tudo lendo
o Zoho como banco de atribuição — sem precisar de Postgres/track.js próprio no MVP.
