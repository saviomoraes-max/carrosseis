# UTMify: Inventário Técnico Completo + Especificação de Clone Interno (RECONECTA / ML Educação)

> Documento técnico v1.0 — 2026-06-03. Baseado no inventário coletado por frota de pesquisadores. Onde a evidência é fraca, está marcado **[incerto]**. Onde é inferência de mercado (não confirmada em fonte primária da UTMify), está marcado **[inferência]**.

---

## 1. O que é a UTMify (resumo executivo)

A **UTMify** (UTMIFY TECNOLOGIA LTDA, fundador citado: Marcio Valim) é um **rastreador de vendas para tráfego pago**, nascido no nicho de infoprodutos/e-commerce/dropshipping BR. Tagline: *"Trackeie suas vendas de forma precisa"*. A proposta de valor é centralizar **num único painel** duas coisas que normalmente vivem separadas:

1. **A origem de cada venda** (qual campanha/conjunto/anúncio/criativo gerou) — capturada via **parâmetros UTM** + `src`/`sck` dos checkouts BR.
2. **O resultado financeiro real** dessa origem (faturamento, lucro, ROI, ROAS, CPA) — cruzando a venda com o **gasto importado das contas de anúncio**.

O slogan operacional é *"otimizar e escalar sem abrir o Facebook"*: a UTMify replica um mini-gerenciador (editar budget/bidcap, pausar, duplicar, regras automáticas) dentro do próprio painel.

**Mecanismo essencial (a tese central deste documento):** apesar do marketing de *"rastreamento server-side completo"* e *"Pixel 2.0"*, a UTMify é, na prática, um **capturador-de-UTM (first-party JS) + agregador de pedidos por webhook**, com **atribuição por correspondência direta de parâmetro** (single-touch efetivo, last-click na prática). Ela **não** é um motor de atribuição multi-touch configurável. A conversão que ela registra é o **webhook de checkout instantâneo** (Kiwify, Hotmart, etc.). Há uma camada adicional de **Pixel próprio (`pixel.js`) que reenvia eventos server-side ao Meta CAPI / TikTok**, mas o detalhe de deduplicação por `event_id` não está documentado publicamente **[incerto]**.

**Implicação direta para a RECONECTA:** a UTMify foi desenhada para um mundo onde *clique → checkout → conversão* acontece em minutos. O caso RECONECTA é o oposto: *clique → lead → qualificação → closer → Deal ganho no Zoho* ao longo de **dias**. Um clone fiel da UTMify **não serve** sem adaptação. O clone interno precisa atribuir a origem do anúncio até o **Deal ganho no Zoho** (atribuição de ciclo longo / lead-to-sale), calcular **CAC real** (não ROAS do Meta) e mandar **conversões offline** de volta ao Meta via CAPI. Ver Seção 7.

---

## 2. Inventário completo de funcionalidades

Legenda de confiança: **A** = evidência forte / **M** = média / **B** = baixa / **[inf]** = inferência.

### 2.1 Módulo Dashboard

| Funcionalidade | Descrição | Como funciona (técnico) | Conf. |
|---|---|---|---|
| Dashboard de Resumo | Tela principal consolidada: faturamento, lucro, gasto, ROI/ROAS, CPA, vendas. "Tudo sem abrir o Facebook" | Cards/widgets de métricas agregadas alimentados por vendas (webhook) × gasto (contas de anúncio) | A |
| Dashboard editável (drag-and-drop) | Usuário monta o próprio painel | Aba Resumo → ícone de lápis → busca métrica → arrasta → salva | A |
| Múltiplos dashboards | Vários dashboards independentes (por produto/conta/checkout). Funcionam como "múltiplas contas dentro da conta" | Aba Resumo → Avançado → Novo Dashboard. Cada um com abas isoladas (Resumo, Campanhas, Integrações, Taxas) e webhooks segmentados | A |
| Filtros do dashboard | Data, conta de anúncio, plataforma, produto (combináveis) | Filtros no topo; tooltip por métrica no hover | A |
| Gráficos analíticos | Vendas por tipo de pagamento, por produto, por fonte/origem | Visualizações no Resumo além de cards/tabelas | A |
| Gráfico temporal | Vendas/faturamento ao longo do tempo | Tipo exato de gráfico não confirmado | M |
| Comparação entre períodos | Comparar dois períodos | Nenhuma fonte oficial descreve explicitamente | B |
| App mobile nativo (iOS/Android) | Mesmas funções do painel: resumo, campanhas, budget/bidcap, regras, KPIs em tempo real | App nativo | A |

### 2.2 Módulo Atribuição / Tracking

| Funcionalidade | Descrição | Como funciona (técnico) | Conf. |
|---|---|---|---|
| Script de UTMs first-party (`latest.js`) | Snippet JS instalado em todas as páginas do funil. Captura UTM (+`src`/`sck`) na chegada e propaga até o checkout | `<script src="https://cdn.utmify.com.br/scripts/utms/latest.js" data-utmify-prevent-subids async defer>` (v2.3.12). Lê query string, persiste, injeta nos links/iframe do checkout | A |
| Persistência/propagação | Mantém UTMs em navegação multi-página/multi-domínio | Cookie/localStorage (storage exato **não publicado**) | M / [inf] |
| Parâmetros `src` e `sck` | Origem geral (`src`) e canal/afiliado (`sck`) dos checkouts BR | Passam na URL do checkout e voltam no payload em `trackingParameters` | A |
| Atribuição por correspondência de parâmetro | Casa UTM/`src`/`sck` do pedido com estrutura de campanha. Single-touch efetivo | Sem modelo estatístico; cada pedido carrega 1 conjunto de UTMs | A |
| Modelo first vs last click | Não há seletor público de modelo | Provável last-touch (script sobrescreve com último UTM) | B / [inf] |
| Janela de atribuição | Não há janela configurável estilo Meta | "Janela" = vida útil do storage no dispositivo | B / [inf] |
| Deduplicação | Mesmo pedido em vários status → upsert pelo `orderId` | Dedup por `orderId` (não por `event_id` Meta) | A (orderId) / B (event_id) |
| Diagnóstico de vendas não rastreadas | Lista vendas sem atribuição: UTMs Inválidas, UTMs Vazias, Outras Fontes (SMS/WhatsApp) | Mostra valores incorretos de `utm_campaign`/`medium`/`content` | A |
| Pixel próprio (`pixel.js`) + CAPI | Captura PageView/ViewContent/AddToCart/InitiateCheckout/Lead/Purchase no browser → endpoint UTMify → ponte server-side p/ Meta CAPI e TikTok | `window.pixelId`; lê `_fbc`/`_fbp` (FB), `_ttp`/`ttp` (TikTok); reconstrói `_fbc` de `fbclid`; IP via ipify; país via ipapi.co; hash SHA-256 p/ advanced matching; `POST https://tracking.utmify.com.br/tracking/v1` com `event_name`, `event_id`, `client_ip_address`, `client_user_agent` | A (existe) / M (mecanismo CAPI/dedupe) |
| Ciclo de vida do pedido por status | Aprovada, pendente, recusada, reembolso, chargeback, cancelado | Cada update reenviado → upsert | A |
| Estados pré-aprovação (PIX/boleto gerado) | Vendas pendentes separadas das pagas | Checkout envia evento "gerado/pendente"; API aceita `pending` | A |
| Upsell / order bump | Pedidos adicionais atribuídos à mesma origem | Sem campo `isUpsell` confirmado em fonte primária | B / [inf] |
| Atribuição de vendas recuperadas | UTMify **rastreia** (não dispara) recuperação de carrinho/PIX/boleto | Vendas recuperadas chegam como "Outras Fontes"/UTM vazia; doc orienta taguear | M |

### 2.3 Módulo UTM Builder / Gestão de Links

| Funcionalidade | Descrição | Como funciona | Conf. |
|---|---|---|---|
| UTM Builder no painel | Campos estruturados (URL destino + 5 UTMs) → monta a URL final copiável | Concatena parâmetros na query string | A |
| Encurtador via Bitly | Encurta links mantendo UTMs intactas | **Não é proprietário**: usa Access Token do Bitly do usuário | M |
| Padronização de nomenclatura | Evita duplicação/erro nos relatórios | Herança de nomes via macros dinâmicas + boas práticas (minúsculas, sem espaço/acento, hífen). "Templates travados" não confirmados | M |
| Centralização de links/atribuição | Links + UTMs + vendas num dashboard | Link é a chave de junção venda↔origem | A |

### 2.4 Módulo Integrações de Anúncio (Ad Platforms)

| Funcionalidade | Descrição | Como funciona | Conf. |
|---|---|---|---|
| Meta Ads (mais maduro) | Template UTM dinâmico p/ campo "Parâmetros de URL" | Template literal: `utm_source=FB&utm_campaign={{campaign.name}}\|{{campaign.id}}&utm_medium={{adset.name}}\|{{adset.id}}&utm_content={{ad.name}}\|{{ad.id}}&utm_term={{placement}}`. **Não usar `\| # & ?`** na nomenclatura | A |
| Google Ads (ValueTrack) | Template com macros do Google + concat com cloaker via `&` | `{lpurl}?utm_source=google&utm_campaign={campaignid}&utm_medium={adgroupid}&utm_content={creative}&utm_term={placement}&keyword={keyword}&device={device}&network={network}`; cloaker: `&senhasecreta=...` | A |
| TikTok Ads | Integração parcial/recente. Doc conflita (troubleshooting lista como "sem integração"; changelog diz "métricas TikTok adicionadas") | Atribuição via UTM manual; sync de métrica recente | M |
| Kwai Ads | Suporte raso. "Regras p/ Kwai com ativação de Pixels/Webhooks/credenciais" vs "sem integração" | Via UTM + webhook; sync de gasto incerto | B |
| Conexão de contas de anúncio | Puxa gasto + estrutura de campanha (Meta/Google/TikTok) | A UTMify **puxa o gasto** da conta (não recebe via API de venda). Mecanismo exato (OAuth vs API relatórios) não documentado | A (existe) / M (mecanismo) |
| Múltiplas contas de anúncio | Conecta vários perfis/contas e consolida | Aba Integrações → Adicionar perfil | A |
| Sync de custo/ROAS/CPA | Cruza gasto com vendas atribuídas | Por campanha e agregado | A |
| Gestão de campanha (mini-gerenciador) | Editar budget, editar bidcap Meta, ativar/desativar (em massa), escalar/desligar pelo relatório | Propaga ao gerenciador via conexão da conta | A |
| Duplicar campanha entre contas | Clonar campanha lucrativa p/ outra conta com 1 clique | — | A |
| Regras automatizadas | Pausar/escalar por critério (ex.: ROAS < X → pausar) | Gatilho por métrica → ação. Condições finas não confirmadas | M |
| Reenvio de conversão (CAPI) | "Dados 100% precisos reenviados às fontes" | Pixel UTMify ↔ Pixel Meta; eventos server-side. Endpoint/eventos/dedupe não detalhados publicamente | M |
| Extensão Chrome ("Rastreador de Orçamento") | Sobrepõe métricas (lucro, gasto, ROI, vendas) no gerenciador; registra horário de alterações | Injeta colunas no Meta | A |

### 2.5 Módulo Integrações de Checkout

**Padrão:** Integrações → Webhooks → (Adicionar Webhook | Credenciais API). Gera URL de webhook e/ou token; cola no postback do checkout. Setup vendido como <5 min.

**Lista completa de plataformas nomeadas** (página oficial `app.utmify.com.br/integracoes` + docs de parceiros):

> Kiwify · Hotmart · Eduzz · Monetizze · Cakto · AppMax · Yampi · PerfectPay · Braip · Ticto · Guru (Digital Manager Guru) · Pepper · Doppus · Kirvano · Hubla · Lastlink · Greenn · Payt · Zippify · SuitPay · Adoorei · BuyGoods · OctusPay · Cartpanda · Slatpay · TriboPay · WooCommerce · Digistore24 · Logzz · MundPay · Clickbank · DiamondPay · Systeme.io · Disrupty · Pantherfy · Orbita · Vega · IExperience · Shopify · Xgrow · TheMembers · CentralCart · HeroSpark · Stripe · NuvemShop · PagTrust · NitroPagamentos · GGCheckout · OnProfit · Everflow
>
> **"Em breve" (à época):** Zouti · Ativopay · Maxweb

| Funcionalidade | Descrição | Como funciona | Conf. |
|---|---|---|---|
| Integração nativa por plataforma | Conectores prontos por webhook/credencial | Painel gera URL/token → cola no checkout (ex.: Monetizze: Ferramentas→Postback; Pepper: Integrações→Traqueamento) | A |
| Atributos `data-utmify-*` por plataforma | Ajusta o script por checkout de destino | Cartpanda: `prevent-xcod-sck prevent-subids ignore-iframe is-cartpanda`; Doppus: `+plus-signal`; ClickBank: `is-click-bank`; BuyGoods: `prevent-xcod-sck`. Outros: `replace-links`, `fast-start`, `fix-shopify-theme`, `is-stripe`, `is-everflow`, `prevent-click-ids-fallback` | A |
| Status recebidos | paid · pending · refunded · chargeback · canceled | Plataforma escolhe quais disparar | A |
| Multi-pagamento | PIX, cartão, boleto | Método no payload; normaliza num relatório | A |
| Reenvio/recuperação de vendas | Reprocessar vendas antigas (documentado p/ Ticto) | Reprocessa via webhook. Detalhes não totalmente extraídos | M |
| Pixel/script de UTMs por plataforma de página | WordPress/Elementor, Inlead, RockFunnels, Cakto Quiz, Atomicat, Typebot | Instala pixel + script no head/footer | A |

### 2.6 Módulo Relatórios e Métricas

| Funcionalidade | Descrição | Conf. |
|---|---|---|
| Abas Campanhas / Conjuntos / Anúncios | Métricas por nível (vendas, CPA, lucro, gasto, ROI), colunas ordenáveis, status de rastreio | A |
| Relatório por origem/UTM | Atribuição por source/medium/campaign/content/term | A |
| Filtros | Nome campanha, status, data de cadastro, conta, plataforma, produto | A |
| Filtro de período | Seletor de intervalo de datas | A |
| Glossário amplo de métricas | Ver Seção 4 | A |
| Métricas de saúde financeira | Faturamento líquido, vendas pendentes, taxa de reembolso, taxa de chargeback, ARPU | A |
| Configuração de taxas/impostos | Imposto (sobre bruto) × Taxa (sobre líquido); % ou fixo por venda. Tutorial "Imposto do Meta Ads" | A |

### 2.7 Módulo API / Webhooks

| Funcionalidade | Descrição | Detalhe técnico | Conf. |
|---|---|---|---|
| Orders API | Endpoint REST único para enviar pedidos | `POST https://api.utmify.com.br/api-credentials/orders`; headers `Content-Type: application/json` + `x-api-token: <token>` | A |
| Credenciais de API | Token nomeado por integração | Integrações → Webhooks → Credenciais API → Adicionar → copiar API TOKEN | A |
| Webhooks inbound por plataforma | URL única colada no postback | Integrações → Webhooks → Adicionar Webhook → selecionar plataforma → Criar | A |
| Sem endpoint de ad-spend | Gasto é **puxado** das contas, não recebido via API | — | A |
| n8n / Make / Zapier | **Sem node nativo**; integração via HTTP Request genérico | n8n: HTTP Request POST p/ Orders API; gatilho = node Webhook | A |
| MCP (Model Context Protocol) | Acesso de agentes de IA aos dados em tempo real | Auth/escopo não detalhados | B |
| Central de Ajuda / docs | Webhook & Credencial, Integrações via API, Pixel, Scripts UTM, Orders API | Artigos JS-rendered (muitos 404 ao fetch) | M |

**Payload canônico da Orders API** (confirmado via integração HeroSpark):

```json
{
  "isTest": false,
  "status": "paid",
  "orderId": "ABC123",
  "platform": "HeroSpark",
  "createdAt": "2026-06-01 10:00:00",
  "approvedDate": "2026-06-01 10:05:00",
  "refundedAt": null,
  "paymentMethod": "pix",
  "customer": { "name": "...", "email": "...", "phone": "...", "country": "BR", "document": "00000000000", "ip": "1.2.3.4" },
  "products": [ { "id": "...", "name": "...", "planId": "...", "planName": "...", "quantity": 1, "priceInCents": 1800000 } ],
  "commission": { "totalPriceInCents": 1800000, "gatewayFeeInCents": 90000, "userCommissionInCents": 1710000 },
  "trackingParameters": { "sck": null, "src": null, "utm_term": "...", "utm_medium": "...", "utm_source": "...", "utm_content": "...", "utm_campaign": "..." }
}
```
Valores monetários **em centavos**. `document` sem pontos/traços. Valores `null` permitidos.

### 2.8 Módulo Gestão de Conta

| Funcionalidade | Descrição | Conf. |
|---|---|---|
| Colaboradores | Adicional pago R$39,90/colaborador; convite pendente até aceite | A (existe) / M (preço) |
| Permissões por dashboard ("Editar Ativos") | Restringe o que cada colaborador vê/gerencia por dashboard. Sem roles nomeadas (admin/editor/viewer) | A |
| Múltiplos dashboards = sub-contas | Não há workspaces formais; cada dashboard = conta isolada | A |
| Segurança | Criptografia ponta a ponta + 2FA | A (claim) |
| Notificações | "Novo sistema de notificações" (release notes); gatilho não confirmado | B |
| Cobrança por volume | Planos escalam por **vendas aprovadas rastreadas/ciclo**. Só venda aprovada conta o limite | A (modelo) / B (tiers) |
| Faixas observadas | R$89,91 · 96,67 · 99,90 · 199,90 · 299,90 · até 475,05 (Reclame Aqui; via Asaas) | B |
| Garantia 7 dias | Reembolso integral incondicional; cancelamento sem multa | A |
| White-label | **Não há evidência** de white-label/revenda p/ agência | A (ausência) |

### 2.9 Módulo Avançado

| Funcionalidade | Descrição | Conf. |
|---|---|---|
| Detecção automática de origem no script | `getTrackingSource` classifica meta/google/kwai/tiktok/taboola lendo `utm_source`/`src`/`utm_term`; extrai `adId` de `utm_content` | A |
| Injeção de ID em links WhatsApp | Reescreve `wa.me`; injeta ID do anúncio no texto via caracteres unicode invisíveis (zero-width / `UnicodeHasher`); pode randomizar nº (`window.phones`) | A |
| Integração VTurb / VSL players | `api.vturb.com.br` | A |
| Advanced matching | SHA-256 (js-sha256) de `external_id` etc. p/ CAPI | A |
| Onboarding | Criar conta → conectar Meta/Google → conectar checkout → instalar script | A |

---

## 3. Como o rastreamento funciona por dentro (o core engine)

### 3.1 Fluxo passo a passo (clique → venda) na UTMify

```
[1] ANÚNCIO (Meta/Google)
    URL de destino = LP limpa
    Campo "Parâmetros de URL" = template UTM dinâmico
      Meta substitui {{campaign.id}} etc. NA ENTREGA
        │
        ▼
[2] CHEGADA NA LANDING PAGE
    latest.js carrega no <head>
      • lê query string: utm_*, src, sck, fbclid, gclid, ttclid
      • getTrackingSource() classifica fonte (meta/google/kwai/tiktok/taboola)
      • extrai adId de utm_content
      • PERSISTE em cookie/localStorage (first-party)   [inf. de storage]
        │
        ▼  (navega LP → VSL → página de captura → checkout, possivelmente outro domínio)
[3] PROPAGAÇÃO
    latest.js em CADA página:
      • reanexa UTMs aos links internos (data-utmify-replace-links)
      • injeta UTMs/src/sck na URL do checkout / iframe / campos ocultos
      • injeta ID em wa.me via zero-width unicode
    Em paralelo (se instalado): pixel.js dispara PageView/ViewContent/InitiateCheckout
      → POST tracking.utmify.com.br/tracking/v1 → ponte CAPI p/ Meta
        │
        ▼
[4] FECHAMENTO NO CHECKOUT
    Checkout grava UTMs/src/sck JUNTO ao pedido (server-side, na plataforma)
        │
        ▼
[5] WEBHOOK / POSTBACK S2S  (independe de cookie do browser nesse momento)
    A cada mudança de status (pending→paid→refunded→chargeback→canceled):
      POST https://api.utmify.com.br/api-credentials/orders
        header x-api-token
        body: order + customer + products + commission + trackingParameters
        │
        ▼
[6] ATRIBUIÇÃO (matching)
    UTMify faz UPSERT por orderId (dedup de pedido)
    Casa trackingParameters → estrutura campanha/conjunto/anúncio (importada das contas)
    1 conjunto de UTMs por venda = SINGLE-TOUCH efetivo (last-click prov.)
        │
        ▼
[7] CRUZAMENTO COM CUSTO
    Gasto puxado das contas de anúncio × vendas atribuídas
    → CPA / ROAS / ROI / lucro por nível
        │
        ▼
[8] REENVIO DE CONVERSÃO (CAPI)  [mecanismo de dedupe não confirmado]
    Purchase server-side → Meta/Google p/ otimizar algoritmo
        │
        ▼
[9] DASHBOARD
    Cards + abas Campanhas/Conjuntos/Anúncios + diagnóstico de não-rastreadas
```

### 3.2 Pontos técnicos do core engine

- **Parâmetros UTM:** os 5 padrão (`source/medium/campaign/term/content`) + os BR `src` (origem geral) e `sck` (canal/afiliado, usado p/ comissionamento). O truque granular é codificar `nome|id` em cada UTM via macro do Meta — assim cada UTM carrega *tanto o nome legível quanto o ID estável* da estrutura.
- **First-party cookie / storage:** UTMify **não publica** se usa cookie, localStorage ou sessionStorage. O comportamento exigido (script em **todas** as páginas, atributos `ignore-iframe`) confirma que ela persiste e reinjeta. **[inferência]**: provável cookie first-party de 1ª parte no domínio do funil + localStorage como fallback.
- **Server-side:** o registro da venda é 100% server-side (webhook do gateway). É isso que torna a venda **resiliente a iOS/ITP/adblock** — o cookie só precisava sobreviver até o *fechamento*, não até o disparo do webhook.
- **Deduplicação:** dois níveis distintos e **não confundir**: (a) dedup de **pedido** por `orderId` (upsert a cada status) — confirmado; (b) dedup de **evento Pixel×CAPI** por `event_id` na Meta — **não confirmado** que a UTMify implemente. O `event_id` aparece no `pixel.js`, mas se ele é casado client+server para a Meta deduplicar é **[incerto]**.
- **Janela de atribuição:** não existe janela em dias configurável. A "janela" real = vida útil do storage. Se expira/é limpo antes da compra → venda não atribuída.
- **Modelo de atribuição:** single-touch, **last-click efetivo** (o último UTM gravado no fechamento vence). Sem multi-touch, sem first-click configurável. **[inferência marcada como tal pela própria pesquisa]**.

---

## 4. Métricas e fórmulas

| Métrica | Definição UTMify | Fórmula |
|---|---|---|
| **Faturamento Bruto** | Soma das vendas antes de deduções | `Σ (preço_venda)` ou `nº vendas × preço` |
| **Faturamento Líquido** | Receita após taxas e impostos | `Bruto − taxas − impostos` |
| **Gasto (Ad Spend)** | Investimento em mídia (puxado das contas) | importado por campanha/conta |
| **Lucro / Lucro Líquido** | Receita menos todos os custos | `Receita − (gasto + taxas + impostos + custos)` |
| **ROI** | Retorno sobre o investimento total | `(Receita − Investimento total) / Investimento total` *(a UTMify descreve como "receita − investimento"; o ROI percentual padrão divide pelo investimento)* |
| **ROAS** | Retorno sobre gasto com anúncios | `Receita / Gasto com mídia` |
| **CPA / CAC** | Custo por aquisição | `Gasto / nº de vendas (aquisições)` |
| **CPC** | Custo por clique | `Gasto / nº de cliques` |
| **Ticket Médio** | Valor médio por venda | `Faturamento total / nº de vendas` |
| **ARPU** | Receita média por usuário | `Receita / nº de usuários (clientes)` |
| **Margem Bruta** | Eficiência operacional | `Lucro bruto / Faturamento` |
| **Margem Líquida** | Resultado final | `Lucro líquido / Faturamento` |
| **Taxa de Reembolso** | % de vendas reembolsadas | `nº reembolsadas / nº aprovadas` |
| **Taxa de Chargeback** | % de chargeback | `nº chargebacks / nº aprovadas` |
| **Vendas Pendentes** | PIX/boleto gerado, aguardando | contagem por status `pending` |

> **Nota crítica para a RECONECTA (ver Seção 7):** essas fórmulas pressupõem que "venda" = transação de checkout. No caso high-ticket, "venda" = **Deal ganho no Zoho**, e o **CAC real** = `gasto Meta / nº de Deals ganhos atribuídos`, com receita = `valor do Deal`. O ROAS do Meta (que conta leads/checkouts) é uma métrica-vaidade aqui.

---

## 5. Modelo de dados proposto (para o clone)

PostgreSQL no Railway. Entidades principais (campos-chave; tipos resumidos):

### `clicks` — toque no anúncio / chegada na LP (ingestão)
| Campo | Tipo | Nota |
|---|---|---|
| `click_id` (PK) | uuid | gerado server-side ou first-party |
| `received_at` | timestamptz | |
| `utm_source/medium/campaign/content/term` | text | |
| `campaign_id`, `adset_id`, `ad_id` | text | extraídos de `nome\|id` |
| `src`, `sck` | text | BR |
| `fbclid`, `gclid`, `ttclid` | text | click IDs das plataformas |
| `fbp`, `fbc` | text | cookies Meta (p/ CAPI matching) |
| `landing_url`, `referrer` | text | |
| `ip`, `user_agent` | text/inet | p/ advanced matching |
| `consent_state` | jsonb | LGPD |
| `anon_id` | text | first-party id persistido no browser |

### `identities` — ponte anon_id ↔ pessoa (resolve ciclo longo)
| Campo | Tipo | Nota |
|---|---|---|
| `identity_id` (PK) | uuid | |
| `anon_id` | text | do click |
| `email_hash`, `phone_hash` | text | SHA-256 normalizado |
| `zoho_contact_id`, `zoho_lead_id` | text | |
| `first_seen`, `last_seen` | timestamptz | |

### `leads` — lead capturado (form/WhatsApp)
| Campo | Tipo | Nota |
|---|---|---|
| `lead_id` (PK) | uuid | |
| `created_at` | timestamptz | |
| `email`, `phone`, `name` | text | |
| `attributed_click_id` (FK) | uuid | atribuição de **entrada** |
| `zoho_lead_id` | text | |
| `source_channel` | text | meta/google/whatsapp/organic |
| `evolution_contact`, `chatwoot_conversation_id` | text | |

### `deals` — Deal do Zoho (a CONVERSÃO real)
| Campo | Tipo | Nota |
|---|---|---|
| `deal_id` (PK) | uuid | |
| `zoho_deal_id` | text | id no Zoho |
| `lead_id` (FK) | uuid | |
| `attributed_click_id` (FK) | uuid | origem do anúncio |
| `stage` | text | etapa do funil |
| `status` | text | open/won/lost (Perdidos→Reengajamento) |
| `amount_cents` | bigint | valor do Deal |
| `won_at`, `lost_at` | timestamptz | |
| `closer_id` | text | atribuição de closer |
| `cycle_days` | int | won_at − click.received_at |
| `capi_sent_at` | timestamptz | conversão offline enviada ao Meta |

### `ad_spend` — gasto importado (Meta/Google)
| Campo | Tipo | Nota |
|---|---|---|
| `id` (PK) | bigserial | |
| `date` | date | granularidade diária |
| `platform` | text | meta/google |
| `account_id`, `campaign_id`, `adset_id`, `ad_id` | text | |
| `spend_cents` | bigint | |
| `impressions`, `clicks` | int | |

### `campaigns` / `adsets` / `ads` — estrutura espelhada das contas
Hierarquia com `id`, `name`, `parent_id`, `status`, `last_synced_at`.

### `events` — eventos enviados ao CAPI (auditoria + dedup)
| Campo | Tipo | Nota |
|---|---|---|
| `event_id` (PK) | uuid | usado na dedup Meta |
| `event_name` | text | Lead / Purchase / Schedule |
| `entity_type`, `entity_id` | text/uuid | lead/deal |
| `sent_at`, `capi_response` | timestamptz/jsonb | |
| `match_quality` | numeric | EMQ retornado | 

### `fees_taxes` — regras de taxa/imposto
`scope` (imposto/taxa), `type` (% ou fixo), `value`, `applies_to` (produto/plataforma).

**Relacionamentos-chave:** `click → identity → lead → deal`. A coluna `attributed_click_id` em `deals` é o **coração da atribuição de ciclo longo** — diferente da UTMify, onde a atribuição mora dentro do pedido de checkout.

---

## 6. Arquitetura do clone interno (encaixe no stack RECONECTA)

```
                          ┌──────────────────────────────────────────────┐
                          │  TRÁFEGO (Meta Ads majoritário, Google)       │
                          │  template UTM dinâmico no "Parâmetros de URL"  │
                          └───────────────┬──────────────────────────────┘
                                          │ clique
                                          ▼
              ┌───────────────────────────────────────────────────────────┐
   INGESTÃO   │  Landing page / VSL / quiz                                 │
   DE CLIQUES │  track.js (first-party, servido via Cloudflare Worker)     │
              │   • lê utm_*, src, sck, fbclid, gclid, fbp/fbc             │
              │   • grava anon_id (cookie 1st-party no domínio reconecta)  │
              │   • POST /collect  → sGTM (Stape) ou endpoint próprio      │
              └───────────────┬───────────────────────────────────────────┘
                              │  (server-side, domínio próprio via Cloudflare)
                              ▼
              ┌───────────────────────────────────────────────────────────┐
   sGTM/STAPE │  Server-side GTM (já existente)                            │
              │   • valida + enriquece (IP, geo)                          │
              │   • encaminha p/ clicks (Postgres) e Meta CAPI (PageView/  │
              │     Lead client+server c/ event_id p/ dedupe)             │
              └───────────────┬───────────────────────────────────────────┘
                              ▼
   STORE      ┌───────────────────────────────────────────────────────────┐
   (Railway)  │  PostgreSQL: clicks, identities, leads, deals, ad_spend,   │
              │  campaigns/adsets/ads, events, fees_taxes                  │
              └───┬───────────────┬───────────────────┬───────────────────┘
                  │               │                   │
   INTEGRAÇÕES    │               │                   │
   (n8n workflows)│               │                   │
                  ▼               ▼                   ▼
        ┌─────────────┐  ┌─────────────────┐  ┌──────────────────────────┐
        │ Meta/Google │  │ Zoho CRM (Deals)│  │ Evolution + Chatwoot     │
        │ Marketing   │  │ COQL/webhooks:  │  │ lead entra por WhatsApp; │
        │ API:        │  │ • lead criado   │  │ casa phone_hash →        │
        │ • ad_spend  │  │ • Deal mudou    │  │ identity/lead            │
        │ • estrutura │  │   stage/won/lost│  │                          │
        └─────────────┘  └────────┬────────┘  └──────────────────────────┘
                                  │ Deal GANHO = conversão real
                                  ▼
   PROCESSAMENTO  ┌──────────────────────────────────────────────────────┐
   DE ATRIBUIÇÃO  │  Worker de atribuição (n8n cron OU serviço Node):    │
                  │  1. liga lead → click (por anon_id/email/phone hash) │
                  │  2. liga Deal → lead → click (attributed_click_id)   │
                  │  3. calcula cycle_days, CAC real, ROAS real          │
                  │  4. dispara CONVERSÃO OFFLINE p/ Meta CAPI           │
                  │     (Purchase/Lead com fbc/fbp/hash, event_id dedupe)│
                  └───────────────────────┬──────────────────────────────┘
                                          ▼
   DASHBOARD      ┌──────────────────────────────────────────────────────┐
                  │  App interno (Next.js já existe em /video-editor      │
                  │  stack — reaproveitar) lendo Postgres:                │
                  │   • Resumo (CAC real, lucro, ROAS real, ciclo médio)  │
                  │   • Campanhas/Conjuntos/Anúncios → Deals ganhos       │
                  │   • Funil: clique→lead→qualificado→Deal ganho         │
                  │   • Diagnóstico de não-atribuídos                    │
                  └──────────────────────────────────────────────────────┘
```

**Decisões de encaixe:**
- **Ingestão de cliques:** servir `track.js` por **Cloudflare Worker** num subdomínio próprio (ex.: `t.reconectaoficial.com`) → cookie first-party de 1ª parte (não bloqueado por ITP como 3rd-party). O endpoint `/collect` pode ser o próprio sGTM (Stape) já existente, evitando reinventar.
- **sGTM/Stape:** reaproveitar para PageView/Lead client+server e como ponte CAPI — **não duplicar** infra de CAPI; a parte nova é a **conversão offline (Deal ganho)** que o GTM não cobre nativamente.
- **Zoho como fonte da verdade da conversão:** workflow n8n com **trigger/polling COQL** detecta `Deal` mudando para ganho. O `Deal` precisa carregar (em campo custom) o `anon_id`/`click_id` ou ao menos `fbclid`+email/phone p/ resolver atribuição.
- **n8n** orquestra todas as integrações (sync de gasto, sync de Deal, envio CAPI), respeitando o CLAUDE.md: node de tratamento de erro + notificação, validação de payload, delay em loops grandes, checar instância Evolution antes de enviar.
- **Banco:** PostgreSQL Railway é o store único.
- **Dashboard:** reaproveitar a stack Next.js que já existe no repositório (`video-editor`) ou um app dedicado.

---

## 7. Adaptação crítica para o caso high-ticket

Esta é **a diferença central** vs a UTMify. A UTMify casa UTM↔pedido **no instante do checkout**. Na RECONECTA, o instante do checkout **não existe**: existe um *lead* hoje e um *Deal ganho* daqui a vários dias, fechado por um closer no Zoho.

### 7.1 Atribuição de ciclo longo (clique → lead → Deal ganho)

O problema: o cookie/anon_id que carrega a origem do anúncio precisa **sobreviver** o tempo todo e ser **religado** ao Deal que nasce no CRM. Estratégia em 3 elos:

1. **Clique → Lead:** no `/collect`, gravar `anon_id` first-party. Quando o lead preenche form / abre WhatsApp, capturar `anon_id` (campo oculto no form) e, no mínimo, `email`+`phone`+`fbclid`. Persistir `attributed_click_id` no `lead`.
2. **Lead → Deal:** ao criar o Lead/Deal no Zoho, gravar em **campos custom** do Deal: `anon_id`, `click_id`, `fbclid`, `utm_*`. (Zoho é centrado em Deals — então os campos de tracking vivem no Deal.) Quando o closer ganha o Deal, o `attributed_click_id` já está lá.
3. **Resolução de identidade (fallback):** quando o `anon_id` se perde (lead veio por outro device/WhatsApp orgânico), casar por `email_hash`/`phone_hash` contra `identities`. Sem match → "não atribuído / Outras Fontes" (mesma categoria que a UTMify usa).

**Janela de atribuição** precisa ser **longa** (ex.: 30–90 dias), ao contrário do checkout instantâneo. Cookie first-party de longa duração + persistência no CRM resolvem isso (o Deal "lembra" a origem mesmo que o cookie expire).

### 7.2 CAC real vs ROAS do Meta

- **ROAS do Meta** otimiza por *leads* ou *Initiate Checkout* — métrica-vaidade aqui, porque um lead barato pode nunca virar Deal.
- **CAC real** = `gasto Meta atribuído / nº de Deals GANHOS atribuídos` (por campanha/conjunto/anúncio).
- **ROAS real** = `Σ valor dos Deals ganhos / gasto Meta` da mesma origem.
- O dashboard deve mostrar, por nível de anúncio: cliques → leads → leads qualificados → Deals ganhos → **CAC real** → **ROAS real** → **ciclo médio (dias)**. Isso é exatamente o que o Meta sozinho **não** consegue ver.

### 7.3 Conversões offline para o Meta (CAPI)

Como a "compra" acontece no Zoho (não num checkout), o Meta precisa receber a conversão via **CAPI com evento offline**:

- Quando `Deal` → ganho, n8n dispara `POST` ao **Meta Conversions API** com:
  - `event_name`: `Purchase` (ou um custom `DealWon`); `Lead` quando o lead entra; `Schedule` quando agenda call.
  - `action_source`: `system_generated` / `crm`.
  - `event_time`: do ganho (Meta aceita até ~7 dias retroativos no CAPI padrão; para janelas maiores usar **Offline Conversions / event_time** dentro do limite — **[validar limite atual]**).
  - **Match keys**: `em` (email hash), `ph` (phone hash), `fbc`, `fbp`, `client_ip_address`, `client_user_agent`, `external_id` — tudo SHA-256 onde exigido. Quanto mais keys, maior o **EMQ (Event Match Quality)**.
  - `value` = valor do Deal, `currency` = BRL.
  - `event_id` único por evento → **dedup** se o mesmo evento também chega por outro caminho.
- Isso ensina o algoritmo do Meta a otimizar por **quem realmente vira cliente high-ticket**, não por leads baratos — o ganho estratégico mais alto do projeto.

> Resumo da Seção 7: o clone interno **inverte** a UTMify — em vez de "pedido carrega UTM", é "Deal carrega UTM, e o ganho do Deal é a conversão que volta pro Meta".

---

## 8. Roadmap de build em fases

| Fase | Escopo | Entregáveis | Esforço aprox. |
|---|---|---|---|
| **MVP** (atribuição read-only) | Provar o elo clique→lead→Deal e o CAC real, sem otimização automática | `track.js` via Cloudflare Worker + cookie first-party; `/collect` reaproveitando sGTM; tabelas `clicks/identities/leads/deals`; campos custom de tracking no Zoho; workflow n8n: Zoho Deal-won → grava `deals`; sync diário de `ad_spend` (Meta Marketing API); dashboard básico (Resumo + tabela por campanha com CAC/ROAS real e ciclo médio) | ~2–3 semanas (1 dev) |
| **v1** (CAPI + funil + diagnóstico) | Fechar o loop com o Meta e dar visibilidade de funil | Conversões offline p/ Meta CAPI (`Lead` + `DealWon`) com advanced matching e `event_id`; resolução de identidade por email/phone hash (fallback); aba Funil (clique→lead→qualificado→ganho); diagnóstico de não-atribuídos (UTM vazia/inválida/outras fontes); integração Evolution/Chatwoot p/ leads de WhatsApp; regras de taxa/imposto; múltiplos dashboards | ~3–4 semanas |
| **v2** (otimização + escala) | Camada operacional estilo UTMify + robustez | Sync da estrutura completa de campanhas Google Ads; regras automatizadas (alertar/pausar por CAC alto) via Meta API; alertas (Evolution/Slack) de CAC fora da meta; UTM Builder interno + padronização de nomenclatura; encurtador (Bitly ou próprio); permissões por dashboard p/ time de tráfego; backfill/reprocessamento de vendas perdidas; app mobile/PWA **[opcional]** | ~4–6 semanas |

**Princípio de fasing:** a Fase MVP já entrega o valor #1 (CAC real por campanha) sem tocar em automação de campanha. A automação (pausar/escalar) é a parte mais arriscada e fica na v2, atrás de validação humana — coerente com o CLAUDE.md ("nunca modificar produção sem confirmar").

---

## 9. Riscos e pontos de atenção

| Risco | Detalhe | Mitigação |
|---|---|---|
| **LGPD / consentimento** | `track.js` coleta IP, UA, e religa a pessoa via email/phone. Base legal e consentimento são obrigatórios | Banner de consentimento gating do `track.js`; `consent_state` no `clicks`; hash de PII em repouso; política de retenção; DPA com Meta |
| **iOS / ITP / perda de cookie** | Safari limita cookie first-party JS a ~7 dias; ciclo high-ticket é mais longo | Cookie **server-set** via Cloudflare Worker (HttpOnly, dura mais que JS-set); **CRM como fonte da verdade** da atribuição (o Deal guarda a origem, independe do cookie) |
| **Match quality do CAPI (EMQ)** | Conversão offline sem boas match keys = Meta ignora/credita mal | Capturar `fbc`/`fbp` no clique e propagar até o Deal; enviar email+phone+IP+UA hasheados; monitorar EMQ no Events Manager |
| **Janela do CAPI offline** | Meta tem limite de retroatividade de `event_time` | **[validar limite atual]**; se o ciclo exceder, enviar com `event_time` no limite e marcar como conversão tardia |
| **Custo de infra** | Volume 100+ leads/dia × eventos; Postgres Railway + Workers | Particionar `clicks` por data; agregações materializadas p/ dashboard; sGTM Stape já cobre boa parte |
| **Manutenção de integrações** | Meta/Zoho mudam API; n8n quebra silenciosamente | Node de erro + notificação obrigatório (CLAUDE.md); testes contra dados reais; versionar payloads |
| **Atribuição multi-touch** | Single-touch (como a UTMify) subestima topo de funil em ciclo longo | MVP single-touch (last-click); v2 pode registrar **todos** os toques (`clicks` já guarda histórico) p/ análise multi-touch posterior |
| **Qualidade do dado do Zoho** | Se o Deal não tiver os campos de tracking preenchidos, atribuição falha | Tornar os campos custom obrigatórios na criação do Deal; validação no n8n |
| **Confiabilidade do webhook/polling Zoho** | Deal ganho pode não disparar | Polling COQL de reconciliação diária além do webhook |

---

## 10. Lacunas da pesquisa e o que validar manualmente

**Da própria UTMify (para fidelidade do clone):**
1. **Storage exato** do `latest.js` (cookie vs localStorage vs sessionStorage) e duração. → abrir o JS minificado de `cdn.utmify.com.br/scripts/utms/latest.js`.
2. **Modelo de atribuição formal** (first vs last click) e regra de sobrescrita. → testar no painel logado.
3. **Janela de atribuição** em dias (se existe). → painel logado.
4. **Deduplicação Pixel×CAPI por `event_id`**: a UTMify casa client+server p/ a Meta deduplicar? Quais eventos reenvia (Purchase/Lead)? Endpoint exato pós-`tracking/v1`. → doc oficial da API (Scribd 878608978) + Events Manager.
5. **Sync de gasto**: OAuth da conta de anúncio vs API de relatórios. → painel logado, aba Integrações.
6. **Macros exatos** dos artigos JS-rendered: `/article/1019` (Meta), `/article/1041` + `/article/1056` (Google + cloaker), `/article/1049` (todas as funcionalidades), `/category/102` (Primeiros Passos). Os templates da Seção 2.4 vieram de docs de parceiros, **confirmar literal**.
7. **TikTok/Kwai**: status real de integração (conflito documental). → changelog do app + painel.
8. **Encurtador**: confirmar se há nativo além do Bitly, ou se houve conflação Bitly-token × UTMify-token nas SERPs.
9. **Templates de nomenclatura travados**: existem ou são só boas práticas? → painel.
10. **Tiers de preço / limites por plano** (dashboards, contas de anúncio, usuários). → página `/precos` é SPA; abrir logado.
11. **Sistema de notificações**: gatilhos reais. → release notes / painel.
12. **MCP**: auth, escopo, por dashboard ou conta. → não detalhado em nenhuma fonte.
13. **Campo `isUpsell`/marcação de order bump**: confirmar em fonte primária.

**Do lado RECONECTA (para o build):**
14. **Limite atual de retroatividade do Meta CAPI offline** (event_time) — crítico p/ ciclo longo.
15. **Quais campos custom já existem no Zoho Deals** p/ tracking (anon_id, fbclid, utm_*) ou precisam ser criados — verificar via `getFields` no módulo Deals.
16. **Como o lead chega hoje** (form de LP? direto no WhatsApp/Evolution?) — define onde capturar o `anon_id`.
17. **Política de consentimento LGPD atual** do funil RECONECTA.
18. **Volume real** (leads/dia, Deals/mês) p/ dimensionar Postgres e custo CAPI.

---

*Fim do documento. Caminho sugerido para versionar este spec no repositório: `/Users/saviomoraes/reconecta/docs/utmify-clone-spec.md` (não criado automaticamente — confirme se deseja gravar).*

---

## Apêndice A — Fontes consultadas (pesquisa multi-agente)

- https://utmify.com.br/
- https://utmify.help.center/
- https://utmify.help.center/article/1024-possiveis-solucoes-para-o-problema-de-trackeamento-de-vendas
- https://utmify.help.center/category/112-integracoes-via-api
- https://apps.apple.com/br/app/utmify/id6504533155
- https://play.google.com/store/apps/details?id=com.utmify.app
- https://chromewebstore.google.com/detail/rastreador-de-or%C3%A7amento-u/jgfeljaoffdaipeeppompjepphhilhdf
- https://herospark.com/blog/utmify-para-o-infoprodutor-e-como-integrar-com-a-herospark/
- https://meutrabalhodigital.com/utmify-como-ganhar-dinheiro/amp/
- https://help.onprofit.com.br/pt/article/como-integrar-com-a-utmify-17am6k7/
- https://help.monetizze.com.br/books/integracoes/page/integracao-utmify
- https://ajuda.cakto.com.br/pt/article/como-integrar-o-utmify-1qmynsz/
- https://www.tiktok.com/@utmify.com.br/video/7530066489957797128
- https://ytscribe.com/v/rctXMXus0nE
- https://utmify.help.center/article/1024-voce-esta-tendo-vendas-nao-trackeadas
- https://utmify.help.center/article/1079-o-que-e-webhook-e-credencial-de-api
- https://utmify.help.center/article/1060-como-instalar-o-script-de-utms-na-shopify
- https://utmify.help.center/article/1058-como-instalar-o-script-de-utms-no-wordpress
- https://ajuda.herospark.com/hc/pt-br/articles/1744833649-como-integrar-hero_spark-com-utmify
- https://help.cartpanda.com/pt-br/article/s2s-postback-13wi92k/
- https://ajuda.kiwify.com.br/pt-br/article/como-passar-parametros-de-rastreamento-na-url-do-checkout-src-utm-tags-entre-outros-1spiptc/
- https://octuspay.zendesk.com/hc/en-us/articles/14280224952733-How-to-Use-Tracking-Parameters-UTM-SRC-SCK-to-Enhance-Monitoring-and-Analysis-of-Online-Campaigns
- https://rifei.com.br/ajuda/integracoes/como-enviar-initiate-checkout-ic-para-a-utmify
- https://www.scribd.com/document/878608978/Documentac-a-o-API-UTMify
- https://www.scribd.com/document/881783867/Utmify-Utms-Script
- https://app.utmify.com.br/integracoes/
- https://utmify.help.center/article/1049-conheca-todas-as-funcionalidades-da-utmify-para-potencializar-sua-operacao
- https://utmify.help.center/article/1019-como-instalar-o-codigo-de-utms-nos-seus-anuncios-do-facebook
- https://utmify.help.center/article/1041-aprenda-a-configurar-o-codigo-de-utms-nos-seus-anuncios-do-googleads
- https://utmify.help.center/article/1056-copy-of-configurando-o-codigo-de-utms-do-google-ads-parametros-do-seu-cloaker
- https://utmify.help.center/category/102-primeiros-passos-na-utmify
- https://ajuda.themembers.com.br/pt-br/article/como-integrar-o-seu-checkout-com-a-utmify-14klfvz/
- https://ajuda.xgrow.com/pt-br/article/integracao-utmify-jy3qin/
- https://escoladomarketing.digital/otimizacao-de-campanhas-com-ia/
- https://utmify.help.center/category/103-configuracao-de-utms
- https://meutrabalhodigital.com/utmify-como-ganhar-dinheiro/
- https://www.rogerioramalhodigital.com.br/post/pixel-api-de-conversao-e-utms
- https://www.youtube.com/watch?v=1XTZthWF7ag
- https://www.youtube.com/watch?v=mGdVUf93DBk
- https://utmify.help.center/category/119-webhook-credencial-de-api
- https://utmify.help.center/category/103-configurando-o-script-de-utms-em-minhas-paginas
- https://utmify.help.center/article/1082-como-reenviar-vendas-da-ticto-para-a-utmify
- https://ajuda.pepper.com.br/pt-br/article/como-integrar-a-utmify-com-a-pepper-1pielal/
- https://ajuda.tribopay.com.br/pt-br/article/como-integrar-com-a-utmify-9h8ocb/
- https://docs.centralcart.com.br/widgets/utmify
- https://ajuda.disrupty.com.br/docs/como-integrar-com-a-utmify/
- https://utmify.help.center/article/1057-glossario-de-metricas
- https://utmify.help.center/article/1028-como-editar-o-meu-dashboard-e-adicionar-novas-metricas
- https://utmify.help.center/article/1027-duvidas-frequentes
- https://apps.apple.com/us/app/utmify/id6504533155
- https://chrome-stats.com/d/jgfeljaoffdaipeeppompjepphhilhdf
- https://utmify.help.center/category/114-pixel-utmify
- https://utmify.help.center/article/1070-como-instalar-o-pixel-da-utmify-no-wordpress
- https://cdn.utmify.com.br/scripts/utms/latest.js
- https://cdn.utmify.com.br/scripts/pixel/pixel.js
- https://github.com/lLucasSantana/Teste-Pratico-Utmify
- https://app.utmify.com.br/precos/
- https://app.utmify.com.br/termos-e-condicoes/
- https://utmify.help.center/category/118-conta-e-assinatura
- https://www.reclameaqui.com.br/empresa/utmify-tecnologia/lista-reclamacoes/
- https://utmify.help.center/article/1091-como-adicionar-colaboradores-em-minha-utmify
- https://app.utmify.com.br/register/
- https://www.linkedin.com/company/utmify
- https://pickscribe.com/v/rctXMXus0nE
- https://www.youtube.com/watch?v=fGQVqlcGfTg
- https://www.youtube.com/watch?v=Led7EF3iV4s
- https://www.youtube.com/watch?v=Xz-W29fRU6I
- https://www.youtube.com/watch?v=IGfQnZzNsA8
- https://www.youtube.com/watch?v=gxnKue6Uvbw
- https://www.youtube.com/watch?v=bBz3id02dps
- https://www.youtube.com/watch?v=sfphDMQ14os
- https://www.youtube.com/watch?v=10O_kuPS1v0
- https://www.youtube.com/watch?v=GvidjTflNNk
- https://utmize.help.center/article/1038-kiwify-como-vincular
- https://utmize.help.center/article/1058-hotmart-como-vincular
- https://utmize.help.center/article/1057-kirvano-como-vincular
- https://utmify.help.center/article/1035-aprenda-a-configurar-o-trackeamento-das-suas-vendas-do-whatsapp-na-utmify
- https://utmify.help.center/article/1050-principais-duvidas-em-relacao-ao-trackeamento-do-whatsapp-na-utmify
- https://utmify.help.center/category/113-utmify-whatsapp
- https://www.npmjs.com/package/utmify
- https://www.semrush.com/website/utmify.com.br/competitors/
- https://www.similarweb.com/pt/website/app.utmify.com.br/
- https://www.trackbee.io/how-it-works
- https://www.trackbee.io/
- https://apps.shopify.com/track-bee
- https://www.redtrack.io/redtrack-vs-hyros/
- https://www.weberlo.com/reviews/redtrack-vs-voluum
- https://voluum.com/traffic-distribution-ai/
- https://voluum.com/affiliate-marketing-software/
- https://cbweb.net/compare/hyros-vs-redtrack-vs-voluum/
- https://utmify.help.center/article/1030-conectei-o-meu-webhook-mas-minhas-vendas-nao-estao-aparecendo-por-qual-motivo
- https://app.utmify.com.br
- https://utmify.help.center/article/1048-configurando-o-codigo-de-utms-do-metaads-parametros-do-seu-cloaker
- https://chrome-stats.com/d/com.utmify.app
- https://www.reclameaqui.com.br/empresa/utmify-tecnologia/
- https://utmify.com.br/integracoes (HTTP 404 - URL pedida nao existe)
- https://app.utmify.com.br/integracoes/ (pagina real, JS-rendered; lista via SERP)
- https://utmify.com.br/ (homepage oficial)
- https://api.utmify.com.br/api-credentials/orders (endpoint da API)
- https://ajuda.cakto.com.br/pt/category/integracoes-1bdui8u/
- https://docs.centralcart.com.br/widgets/utmify (host nao resolveu no fetch)
- https://help.utmify.com.br (alvo solicitado — ECONNREFUSED, nao acessivel)
- https://utmify.help.center/article/1057-glossario-de-metricas (404 no fetch; titulo via SERP)
- https://utmify.help.center/article/1019-como-instalar-o-codigo-de-utms-nos-seus-anuncios-do-facebook (404 na verificacao)
- https://utmify.help.center/article/1048-configurando-o-codigo-de-utms-do-metaads-parametros-do-seu-cloaker (404 na verificacao)
- https://utmify.help.center/category/109-problema-de-trackeamento
- https://utmify.help.center/article/1057-glossario-de-metricas (404 na verificacao)
- https://app.utmify.com.br/
- https://v0.app/chat/sales-trigger-for-utmfy-h2PQ2KZVY3d
- https://utmify.help.center/category/114-pixel
- https://www.tiktok.com/@utmify.com.br/video/7568346471615958280
- https://apps.apple.com/eg/app/utmify/id6504533155
- https://onprofit.com.br/
- https://help.monetizze.com.br/books/integracoes/page/ferramentas-de-integracao
- https://r.jina.ai/https://app.utmify.com.br/precos/
- https://www.reclameaqui.com.br/empresa/utmify-tecnologia/sobre/
- https://utmify.help.center/category/111-faqs
- https://www.tiktok.com/@utmify.com.br/video/7509998373286595845
- https://www.reclameaqui.com.br/utmify-tecnologia/solicitacao-de-cancelamento-e-estorno-do-plano-utmify-contratado-online_1d3URM3nCPz1E_4w/
- https://app.utmify.com.br/precos/ (pagina oficial de precos — SPA renderizado em JS; nao legivel por fetch estatico, tabela de planos nao extraida)
- https://www.utmify.com.br/termos-e-condicoes/ (termos — trial de 7 dias e reembolso integral, via snippet de busca)
- https://meutrabalhodigital.com/utmify-como-ganhar-dinheiro/ (artigo/afiliado de terceiros — garantia incondicional de 7 dias, planos por porte, contagem so de transacoes aprovadas)
- https://www.reclameaqui.com.br/empresa/utmify-tecnologia/lista-reclamacoes/ (Reclame Aqui — valores R$89,91 / R$96,67 / R$99,90; cobranca recorrente; reclamacoes de reembolso e cobranca indevida; pagina retorna 403 no fetch, dados via snippet de busca)
- https://apps.apple.com/br/app/utmify/id6504533155 (App Store — app listado como Gratis, sem precos de assinatura in-app expostos)
- https://developers.facebook.com/docs/marketing-api/get-started/authorization
- https://developers.facebook.com/docs/permissions/reference/
- https://mwm.ai/apps/utmify/6504533155
- https://utmify.help.center/article/1041-como-instalar-o-codigo-de-utms-nos-meus-anuncios-do-google-ads
- https://developers.google.com/google-ads/api/docs/api-policy/developer-token
- https://developers.google.com/google-ads/api/rest/auth
- https://www.chili.com.br/blog/noticias/google-analytics-passa-a-permitir-importacao-automatica-de-custos-de-anuncios-do-meta-e-tiktok/

## Apêndice B — Lacunas sinalizadas pelo crítico de completude

- MODELO DE NEGOCIO / PRICING: o inventario nao tem NADA sobre como a UTMify cobra (planos, faixas de preco, limite de pedidos trackeados/mes, periodo de teste gratis, cobranca por volume vs flat). Pra clonar e essencial saber a estrutura de monetizacao e os limites por plano.
- BACKEND / STACK / INFRAESTRUTURA: zero informacao sobre a arquitetura de servidor (linguagem, banco de dados, fila de processamento de webhooks, como aguentam o volume de eventos em tempo real). Sem isso o 'como construir' fica so na camada de cliente. Endpoints conhecidos (api.utmify.com.br, tracking.utmify.com.br, cdn.utmify.com.br) sugerem servicos separados mas nada confirmado.
- ENDPOINT DE TRACKING DO PIXEL (payload e resposta): conhece-se a URL https://tracking.utmify.com.br/tracking/v1 e que recebe POST com event_name/event_id/client_ip/client_user_agent, mas o SCHEMA COMPLETO do payload do pixel.js, a resposta do servidor, e como esse evento server-side e reenviado pra Meta CAPI / TikTok Events API (qual access_token, qual pixel_id, dedupe com event_id) NAO esta confirmado. E o coracao do 'server-side tracking' e esta vago.
- MECANISMO DE IMPORTACAO DE GASTO (ad spend): repetidamente marcado como 'nao documentado' se e via OAuth + Meta Marketing API / Google Ads API / TikTok Marketing API ou outro. Pra clonar precisa saber EXATAMENTE como conecta a conta (OAuth scopes, frequencia de sync, qual endpoint de insights puxa gasto/impressoes/cliques).
- EDICAO/GESTAO DE CAMPANHA DENTRO DA UTMify: afirma que edita budget/bidcap, liga/desliga e duplica campanha, mas nao confirma que isso usa a Meta Marketing API de escrita (POST em /act_{id}/campaigns etc.), quais permissoes/escopos OAuth sao necessarios (ads_management), e se ha aprovacao de App Review da Meta. Isso e barreira tecnica e de compliance enorme pra um clone.
- REGRAS AUTOMATIZADAS (motor de automacao): so se sabe que 'pausa por ROAS abaixo de X'. Faltam: quais metricas sao condicionaveis, operadores suportados, frequencia de avaliacao (cron/intervalo), acoes possiveis alem de pausar/escalar, e se roda server-side continuamente.
- FUNCIONAMENTO DO SCRIPT latest.js (internals): tem-se versao 2.3.12 e lista de data-* attrs, mas o MECANISMO DE PERSISTENCIA exato (cookie vs localStorage vs sessionStorage, nome das chaves, TTL) e marcado como inferencia. Pra clonar o tracking de funil multi-dominio isso precisa ser confirmado por leitura do JS minificado.
- MODELO DE ATRIBUICAO (first vs last click) e JANELA: ambos marcados explicitamente como inferencia/'nao publicado'. Um cloner precisa decidir a regra de sobrescrita de UTM e a janela; saber o que a UTMify realmente faz (lendo o script) fecha a duvida.
- DEDUPLICACAO COM A META (event_id): incerto se o pixel.js gera um event_id que e reusado no evento server-side pra dedupe Pixel+CAPI. O inventario diz que pixel.js monta event_id, mas nao confirma que o mesmo event_id e enviado tanto client quanto server pra dedupe. Critico pra nao contar conversao 2x.
- NIVEIS DE PERMISSAO DE COLABORADORES: artigo retornou 404; nao se sabe se ha papeis (admin/viewer/editor), permissao por dashboard, ou acesso de agencia multi-cliente. Importante pro modelo SaaS de equipe.
- ONBOARDING / CRIACAO DE CONTA / LIMITES DE WORKSPACE: nao ha info sobre cadastro, verificacao, quantos dashboards/contas de anuncio/webhooks por plano, e se ha conceito de 'workspace' ou 'organizacao' multi-conta.
- RATE LIMITS E IDEMPOTENCIA DA ORDERS API: o payload e conhecido, mas faltam rate limits, codigos de resposta/erros, validacao de campos, e se o upsert por orderId tem chave de idempotencia. Necessario pra um clone aceitar webhooks em escala sem duplicar.
- TIKTOK e KWAI - status real de sync de gasto: marcado como ambiguo/incerto. Pra um clone, definir se TikTok Ads tem importacao de custo real ou so atribuicao por UTM muda o escopo.
- GOOGLE/META UTM MACROS exatos via artigo oficial: o inventario tem os macros mas em parte vem de integradores terceiros e os artigos oficiais (article/1019, 1041) retornaram 404/JS-render. Vale confirmar a string oficial.
- GRAFICOS e COMPARACAO DE PERIODO: tipo de grafico no Resumo e existencia de comparacao periodo-vs-periodo marcados como nao confirmados.
- WEBHOOK PAYLOAD POR PLATAFORMA: sabe-se que o token e colado no checkout, mas como a UTMify NORMALIZA payloads diferentes (Hotmart vs Kiwify vs Cartpanda tem schemas distintos) num modelo unico de pedido NAO esta documentado. Pra clonar 38 integracoes nativas isso e o trabalho pesado real.

---

*Gerado por pesquisa multi-agente (workflow `utmify-deep-research`, 37 agentes, 16 páginas lidas, 7 buscas de lacuna) — 2026-06-03.*
