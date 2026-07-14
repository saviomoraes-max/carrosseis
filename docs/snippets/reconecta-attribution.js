/*
 * reconecta-attribution.js  (captura de atribuicao v1)
 * ----------------------------------------------------------------------------
 * Cola este script no <head> de TODAS as paginas do funil pago (landing pages,
 * VSL, pagina de captura). Ele resolve o problema que matou a atribuicao no
 * Zoho: captura origem do anuncio + IDs + fbclid e injeta nos campos ocultos
 * do formulario que cria o negocio.
 *
 * O que ele faz:
 *  1. Le os parametros da URL (utm_*, campaign_id, adset_id, ad_id, placement,
 *     fbclid, gclid) na chegada.
 *  2. Le os cookies do Pixel da Meta (_fbp / _fbc); se faltar _fbc mas houver
 *     fbclid, reconstroi o fbc no formato fb.1.<timestamp>.<fbclid>.
 *  3. Persiste tudo em cookie de 1a parte (dominio raiz) + localStorage por
 *     90 dias, sobrevivendo a navegacao multi-pagina/multi-subdominio.
 *  4. Guarda PRIMEIRO toque (grava 1x, nunca sobrescreve) e ULTIMO toque
 *     (sempre sobrescreve) separadamente, casando com os campos do Zoho.
 *  5. Preenche os <input type=hidden> do formulario (nomes = api_name do Zoho)
 *     na carga e de novo no submit.
 *
 * NAO requer dependencia. ~5kb. Comentarios em PT-BR (padrao do projeto).
 */
(function () {
  "use strict";

  // === CONFIG (ajuste conforme o ambiente) ===========================
  var CONFIG = {
    // Dominio raiz pro cookie sobreviver entre subdominios.
    // Ex.: ".reconectaoficial.com.br". Deixe "" pra usar o host atual.
    cookieDomain: "",
    cookieDays: 90,
    // Se true, cria os inputs ocultos que faltarem no form automaticamente.
    autoCreateHiddenInputs: true
  };

  var KEY_FIRST = "rc_attr_first"; // primeiro toque
  var KEY_LAST = "rc_attr_last";   // ultimo toque

  // Parametros lidos da URL (chave = nome do parametro na query string).
  var URL_PARAMS = [
    "utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term",
    "campaign_id", "adset_id", "ad_id", "placement", "gclid"
  ];

  // Mapa: chave interna -> api_name do campo no Zoho.
  // FIRST = campos de primeiro toque; LAST = campos *_last (ultimo toque).
  var MAP_FIRST = {
    utm_source: "utm_source",
    utm_medium: "utm_medium",
    utm_campaign: "utm_campaign",
    utm_content: "utm_content",
    utm_term: "utm_term",
    campaign_id: "campaign_id",
    ad_id: "ad_id",
    placement: "ad_placement",
    fb_click_id: "fb_click_id" // fbc reconstruido a partir do fbclid
  };
  var MAP_LAST = {
    utm_source: "utm_source_last",
    utm_medium: "utm_medium_last",
    utm_campaign: "utm_campaign_last",
    utm_content: "utm_content_last",
    utm_term: "utm_term_last",
    campaign_id: "id_campaign_last",
    adset_id: "id_adset_last",
    ad_id: "id_ad_last",
    dt_last_utm: "dt_last_utm"
  };

  // === Utilitarios ===================================================
  function qs(name) {
    var m = new RegExp("[?&]" + name + "=([^&#]*)").exec(location.search);
    return m ? decodeURIComponent(m[1].replace(/\+/g, " ")) : "";
  }
  function getCookie(name) {
    var m = document.cookie.match("(^|;)\\s*" + name + "\\s*=\\s*([^;]+)");
    return m ? decodeURIComponent(m.pop()) : "";
  }
  function setCookie(name, value, days) {
    var d = new Date();
    d.setTime(d.getTime() + days * 864e5);
    var dom = CONFIG.cookieDomain ? "; domain=" + CONFIG.cookieDomain : "";
    document.cookie = name + "=" + encodeURIComponent(value) +
      "; expires=" + d.toUTCString() + "; path=/" + dom + "; SameSite=Lax";
  }
  function readStore(key) {
    try {
      var v = localStorage.getItem(key) || getCookie(key);
      return v ? JSON.parse(v) : null;
    } catch (e) { return null; }
  }
  function writeStore(key, obj) {
    var s = JSON.stringify(obj);
    try { localStorage.setItem(key, s); } catch (e) {}
    setCookie(key, s, CONFIG.cookieDays);
  }

  // === 1-3. Coleta e persistencia ====================================
  var now = Date.now();
  var current = {};
  for (var i = 0; i < URL_PARAMS.length; i++) {
    var v = qs(URL_PARAMS[i]);
    if (v) current[URL_PARAMS[i]] = v;
  }

  // fbc: usa cookie _fbc; senao reconstroi do fbclid.
  var fbclid = qs("fbclid");
  var fbc = getCookie("_fbc");
  if (!fbc && fbclid) fbc = "fb.1." + now + "." + fbclid;
  if (fbc) current.fb_click_id = fbc;

  // _fbp tambem e capturado (util pro CAPI). Hoje NAO ha campo no Zoho;
  // se o time criar um campo "fbp", inclua no MAP_FIRST.
  var fbp = getCookie("_fbp");
  if (fbp) current.fbp = fbp;

  current.dt_last_utm = new Date(now).toISOString();

  // So conta como "toque" real se veio com origem de anuncio.
  var hasTouch = !!(current.utm_source || current.campaign_id || fbclid);

  var last = readStore(KEY_LAST) || {};
  if (hasTouch) { last = current; writeStore(KEY_LAST, last); }

  var first = readStore(KEY_FIRST);
  if (!first && hasTouch) { first = current; writeStore(KEY_FIRST, first); }
  first = first || {};

  // === 5. Preenchimento do formulario ================================
  function setHidden(form, fieldName, value) {
    if (value == null || value === "") return;
    var el = form.querySelector('[name="' + fieldName + '"]');
    if (!el && CONFIG.autoCreateHiddenInputs) {
      el = document.createElement("input");
      el.type = "hidden";
      el.name = fieldName;
      form.appendChild(el);
    }
    if (el) el.value = value;
  }
  function fillForm(form) {
    var k;
    for (k in MAP_FIRST) if (MAP_FIRST.hasOwnProperty(k)) setHidden(form, MAP_FIRST[k], first[k]);
    for (k in MAP_LAST) if (MAP_LAST.hasOwnProperty(k)) setHidden(form, MAP_LAST[k], last[k]);
  }
  function fillAll() {
    var forms = document.querySelectorAll("form");
    for (var i = 0; i < forms.length; i++) {
      fillForm(forms[i]);
      // Reforca no submit (caso o form seja montado/alterado dinamicamente).
      forms[i].addEventListener("submit", function () { fillForm(this); });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", fillAll);
  } else {
    fillAll();
  }

  // Expoe pra debug/integracoes (ex.: enviar via fetch num form custom).
  window.RCAttribution = { first: first, last: last, current: current };
})();
