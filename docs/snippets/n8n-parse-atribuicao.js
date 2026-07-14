// =============================================================================
// n8n Code node — "Parsear atribuição (lead-in -> Zoho Deal)"
// Modo: Run Once for All Items
// -----------------------------------------------------------------------------
// Recebe o payload do webhook /webhook/lead-in (formato enviado pela LP
// supercaso.com.br) e devolve os campos prontos pro Deal do Zoho, com os
// api_names exatos. Plugue a saída no seu node de create/upsert do Zoho e faça
// merge com os campos que você já preenche (qualificação, etc.).
//
// Resolve o que faltava: separa ID e nome das UTMs (formato ID_Texto),
// reconstrói o fb_click_id (fbc) a partir do fbclid, normaliza source/medium e
// marca fonte_de_lead = "Tráfego pago".
// =============================================================================

// Separa "120245620450500505_Nome da coisa" -> { id, name }
function splitIdText(v) {
  if (v == null) return { id: null, name: null };
  const s = String(v).trim();
  const m = s.match(/^(\d{6,})_+(.*)$/); // prefixo numérico (ID Meta) + underscore(s)
  if (m) return { id: m[1], name: m[2].trim() };
  return { id: null, name: s };
}

function norm(s) {
  return (s == null ? '' : String(s)).trim().toLowerCase();
}

const out = [];

for (const item of $input.all()) {
  const root = item.json || {};
  const b = root.body || root;
  const headers = root.headers || {};
  const f = b.form_data || {};
  const utm = b.utm_parameters || {};
  const other = b.other_parameters || {};
  const page = b.page_info || {};

  // --- UTMs (ID + nome) -----------------------------------------------------
  const camp = splitIdText(utm.utm_campaign);  // campanha
  const term = splitIdText(utm.utm_term);      // conjunto (adset)
  const content = splitIdText(utm.utm_content);// anúncio (ad)

  // --- Origem normalizada (tudo Meta) --------------------------------------
  let src = norm(utm.utm_source);
  if (['ig', 'instagram', 'fb', 'facebook', 'meta'].includes(src)) src = 'meta';
  if (!src) src = 'meta'; // fallback: veio de anúncio Meta
  let med = norm(utm.utm_medium);
  if (['cpc', 'ppc', 'paid', 'paid_social', 'cpm', 'social'].includes(med)) med = 'paid';
  if (!med) med = 'paid';

  // --- fb_click_id (fbc) a partir do fbclid --------------------------------
  const fbclid = utm.fbclid || other.fbclid || null;
  const tsMs = Date.parse(b.timestamp || '') || Date.now();
  const fbc = fbclid ? `fb.1.${tsMs}.${fbclid}` : null;

  // --- Dados pro CAPI futuro (hoje sem campo no Zoho; ver doc) --------------
  const capi = {
    fbclid: fbclid,
    fbc: fbc,
    ip: headers['x-real-ip'] || headers['x-forwarded-for'] || null,
    user_agent: page.user_agent || headers['user-agent'] || null,
    email: f.email || null,
    phone: f.phone_number || null,
    session_id: b.session_id || null,
  };

  // --- Campos do Deal no Zoho (api_names exatos) ---------------------------
  const deal = {
    // primeiro toque
    utm_source: src,
    utm_medium: med,
    utm_campaign: camp.name,
    utm_content: content.name,
    utm_term: term.name,
    campaign_id: camp.id,
    ad_id: content.id,
    ad_placement: other.placement || null,
    fb_click_id: fbc,
    // último toque (no primeiro contato recebe o mesmo valor)
    utm_source_last: src,
    utm_medium_last: med,
    utm_campaign_last: camp.name,
    utm_content_last: content.name,
    utm_term_last: term.name,
    id_campaign_last: camp.id,
    id_adset_last: term.id,
    id_ad_last: content.id,
    dt_last_utm: new Date(tsMs).toISOString(),
    // origem / classificação
    fonte_de_lead: 'Tráfego pago',
    funil_origem: b.funil_origem || null,
    lead_classification: f.classificado || null,
  };

  // remove chaves nulas (não sobrescrever no Zoho com vazio)
  for (const k of Object.keys(deal)) {
    if (deal[k] == null || deal[k] === '') delete deal[k];
  }

  out.push({ json: Object.assign({}, deal, { _capi: capi }) });
}

return out;
