#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pulso de trends — motor determinístico do aviso de hora em hora no Slack.

Diferente do radar curado (radar-trends-quentes, 1x/dia, opus, ponte profunda),
este aqui é GENERALISTA e rápido: lê os trending topics do Twitter/X (Brasil +
Mundo), o "trending now" de busca do Google (Brasil) e as fofocas do Portal Leo
Dias, guarda estado entre as rodadas pra saber O QUE SUBIU / É NOVO (detector de
onda — foi o que faltou pra pegar o caso BTS cedo), e lidera o aviso com esses
destaques + uma nota curta da IA barata (haiku) nos temas quentes: por que
importa, se dá gancho pro nicho, e FLAG de tema sensível (o pulso SURFACE temas
sensíveis com o ângulo seguro, não descarta como o radar curado faz).

Todo trend/fofoca vira LINK clicável no aviso (Twitter -> busca no X; Google ->
notícia; Leo Dias -> artigo) pra dar pra ler na hora.

Fontes (todas grátis, validadas por curl 200 em 24/jul/26):
  - getdaytrends.com/brazil/   -> Twitter/X TT Brasil
  - getdaytrends.com/          -> Twitter/X TT Mundo
  - trends.google.com/trending/rss?geo=BR -> Google "trending now" Brasil (RSS)
  - portalleodias.com/feed/    -> fofocas do Portal Leo Dias (RSS)

O SHELL (run-trends-pulse.sh) é quem posta no Slack (lê token/canal do Keychain
e faz o curl) — aqui só montamos o payload Block Kit em arquivo. Assim o token
nunca passa pelo Python nem por arquivo de config.

Estado de velocidade: gravamos o board NOVO num arquivo .pending; o shell só o
promove pra trends-pulse-state.json DEPOIS de o Slack confirmar a entrega — assim
uma queda de Slack não "consome" os movers da hora (a onda reaparece na próxima).

Uso:
  python3 trends_pulse.py <caminho_payload.json>
Saída:
  - escreve o payload Block Kit em <caminho_payload.json> (se houver o que postar)
  - escreve o snapshot completo em data/trends-pulse.json
  - grava o estado seguinte em data/trends-pulse-state.json.pending (shell promove)
  - imprime 1 linha de resumo no stdout (o shell usa no log / fallback macOS)
  - exit 0 = payload pronto pra postar; exit 2 = nada a postar (fontes fora/erro)
"""
import json, os, re, sys, html, subprocess, unicodedata
import xml.etree.ElementTree as ET
from urllib.parse import quote

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # ~/reconecta
AGENTE = os.path.join(BASE, "agente-carrosseis")
DATA = os.path.join(AGENTE, "data")
STATE_PATH = os.path.join(DATA, "trends-pulse-state.json")
STATE_PENDING = STATE_PATH + ".pending"
SNAP_PATH = os.path.join(DATA, "trends-pulse.json")
RELEVANCE_PATH = os.path.join(AGENTE, "relevance-filter.json")

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

# Boards: br/mundo = Twitter TT; google = Google Trends; leo = fofoca Leo Dias
BOARDS_KEYS = ("br", "mundo", "google", "leo")
TOP_CONSIDER = {"br": 20, "mundo": 20, "google": 10, "leo": 10}
TOP_SHOW = {"br": 6, "mundo": 6, "google": 6, "leo": 5}
SUBINDO_MIN = 3      # subiu >= 3 posições = "subindo"
NOVO_DENTRO = {"br": 15, "mundo": 15, "google": 10, "leo": 10}  # só é "novo" se entrou até aqui
MAX_DESTAQUES = 8    # teto de itens que vão pra IA e pro topo do aviso
LEO_FEED = "https://portalleodias.com/feed/"

# Limites de tamanho (Slack rejeita section text > 3000 chars => no-post silencioso)
LIM_PORQUE, LIM_GANCHO, LIM_SENSIVEL, LIM_SECTION = 130, 160, 220, 2900

# Palavras-âncora do nicho (harmonização facial / clínica / estética). É só uma
# DICA pra puxar o item pra avaliação da IA — quem decide a ponte real é a IA.
NICHO_KW = [
    "harmoniz", "estetic", "botox", "preenchim", "bichectomia", "skinbooster",
    "hialuron", "acido hialur", "dentist", "odonto", "clinica", "rosto",
    "facial", "beleza", "autoestima", "plastica", "dermato", "filler",
    "bioestimulador", "sobrancelha", "colageno", "rejuvenesc", "lifting",
    "toxina", "labial", "papada", "microagulham", "bronzeamento", "peeling",
]


# ------------------------------------------------------------------ utilidades
def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def norm(s):
    """Normaliza pra comparar entre rodadas: minúsculo, sem acento, sem espaços extras."""
    return re.sub(r"\s+", " ", strip_accents(str(s or "")).lower()).strip()


def esc(s):
    """Escapa o mínimo pro mrkdwn do Slack (inclusive dentro de <url|texto>)."""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def trunc(s, n):
    s = str(s)
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def x_search(nome):
    """Link pra busca do trend no X (Twitter) — abre a conversa do trend."""
    return "https://x.com/search?q=" + quote(nome) + "&src=trend_click"


def link_for(nome, fonte, url_maps):
    """URL clicável do item conforme a fonte. None se não houver."""
    if fonte in ("br", "mundo"):
        return x_search(nome)
    return (url_maps.get(fonte) or {}).get(norm(nome))


def md_link(nome, fonte, url_maps):
    """<url|nome> se tiver URL, senão só o nome escapado."""
    u = link_for(nome, fonte, url_maps)
    return f"<{u}|{esc(nome)}>" if u else esc(nome)


def write_json_atomic(path, obj, indent=None):
    """Grava JSON de forma atômica (tmp + os.replace) pra não truncar em kill/disco."""
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=indent)
    os.replace(tmp, path)


def curl(url):
    """GET com User-Agent de browser. Devolve texto ou None (timeout/erro/HTTP!=2xx)."""
    try:
        p = subprocess.run(
            ["curl", "-sS", "-A", UA, "-L", "--max-time", "20",
             "-w", "\n__HTTP__%{http_code}", url],
            capture_output=True, text=True, timeout=30,
        )
        out = p.stdout
        m = re.search(r"__HTTP__(\d+)\s*$", out)
        code = int(m.group(1)) if m else 0
        body = out[: m.start()] if m else out
        if 200 <= code < 300 and body.strip():
            return body
    except Exception:
        pass
    return None


# ------------------------------------------------------------------- parsers
def parse_getdaytrends(html_text):
    """Extrai a lista 'Now' do getdaytrends: <td class="main">...<a .../trend/...>NOME</a>.
    Escopa ao board 'Now' (tabelas 'ranking trends') e descarta as tabelas secundárias
    'ranking top' (Most Tweeted / Longest Trending), que reiniciam a numeração."""
    if not html_text:
        return []
    cut = re.search(r'ranking\s+top', html_text)  # começo das tabelas secundárias
    if cut:
        html_text = html_text[: cut.start()]
    pat = re.compile(
        r'<td class="main"[^>]*>\s*<a [^>]*href="[^"]*/trend/[^"]*"[^>]*>(.*?)</a>',
        re.S,
    )
    nomes, vistos = [], set()
    for raw in pat.findall(html_text):
        nome = html.unescape(re.sub(r"<[^>]+>", "", raw)).strip()
        if not nome:
            continue
        k = norm(nome)
        if k in vistos:          # a página repete alguns trends em blocos secundários
            continue
        vistos.add(k)
        nomes.append(nome)
    return nomes


def parse_google_rss(xml_text):
    """[{nome, trafego, noticia, url}] do RSS 'trending now' do Google."""
    if not xml_text:
        return []
    try:
        root = ET.fromstring(xml_text.encode("utf-8", "replace"))
    except Exception:
        return []
    ns = {"ht": "https://trends.google.com/trending/rss"}
    itens = []
    for it in root.findall(".//item"):
        titulo = (it.findtext("title") or "").strip()
        if not titulo:
            continue
        traf = (it.findtext("ht:approx_traffic", default="", namespaces=ns) or "").strip()
        noticia, url = "", ""
        n = it.find("ht:news_item", ns)
        if n is not None:
            noticia = (n.findtext("ht:news_item_title", default="", namespaces=ns) or "").strip()
            url = (n.findtext("ht:news_item_url", default="", namespaces=ns) or "").strip()
        if not url:
            url = (it.findtext("link") or "").strip()
        if not url:
            url = "https://www.google.com/search?q=" + quote(titulo)
        itens.append({"nome": titulo, "trafego": traf, "noticia": noticia, "url": url})
    return itens


def parse_leodias(xml_text):
    """[{nome(título), url(link), quando(pubDate)}] do RSS do Portal Leo Dias.
    Pula horóscopo (não é fofoca)."""
    if not xml_text:
        return []
    try:
        root = ET.fromstring(xml_text.encode("utf-8", "replace"))
    except Exception:
        return []
    itens = []
    for it in root.findall(".//item"):
        titulo = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        if not titulo or not link:
            continue
        cats = [norm(c.text) for c in it.findall("category") if c.text]
        if any("horoscopo" in c for c in cats):
            continue
        pub = (it.findtext("pubDate") or "").strip()
        itens.append({"nome": titulo, "url": link, "quando": pub})
    return itens


# ------------------------------------------------------------- estado/velocidade
def carregar_estado():
    try:
        return json.load(open(STATE_PATH, encoding="utf-8"))
    except Exception:
        return None


def rank_map(lista):
    """De ['a','b',...] pra {norm(nome): posicao(1-based)}."""
    return {norm(x): i + 1 for i, x in enumerate(lista)}


def classificar(board_key, nomes_atual, estado_prev):
    """Devolve dict {norm: {'nome','rank','tag','delta'}} só pros MOVERS (novo/subindo)."""
    prev = rank_map(estado_prev.get(board_key, [])) if estado_prev else {}
    if not prev:
        return {}  # sem baseline (1ª rodada OU board que falhou antes) => nada é novo/subindo
    movers = {}
    limite_novo = NOVO_DENTRO[board_key]
    for i, nome in enumerate(nomes_atual[: TOP_CONSIDER[board_key]]):
        rank = i + 1
        k = norm(nome)
        if k not in prev:
            if rank <= limite_novo:
                movers[k] = {"nome": nome, "rank": rank, "tag": "novo", "delta": 0}
        else:
            delta = prev[k] - rank  # positivo = subiu
            if delta >= SUBINDO_MIN:
                movers[k] = {"nome": nome, "rank": rank, "tag": "subindo", "delta": delta}
    return movers


def match_nicho(nomes, extra_text_por_nome=None):
    """Devolve set de norm(nome) que batem numa âncora do nicho (nome + texto extra)."""
    hits = set()
    for nome in nomes:
        blob = norm(nome)
        if extra_text_por_nome and nome in extra_text_por_nome:
            blob += " " + norm(extra_text_por_nome[nome])
        if any(kw in blob for kw in NICHO_KW):
            hits.add(norm(nome))
    return hits


# ------------------------------------------------------------------- IA (haiku)
def anotar_com_ia(candidatos, relevance):
    """
    candidatos: [{'nome','fonte','rank','tag'}]. Devolve {norm(nome): {...}} com
    por_que/gancho/sensivel. Resiliente: qualquer falha -> {} (posta sem nota).
    """
    if not candidatos:
        return {}
    dores = relevance.get("dores_nucleo", [])
    quem = (relevance.get("publico", {}) or {}).get("quem", "")
    linhas = "\n".join(
        f'- "{c["nome"]}" (fonte: {c["fonte"]}, posição {c["rank"]}, sinal: {c["tag"]})'
        for c in candidatos
    )
    prompt = f"""Você é o filtro de um radar de conteúdo para um público específico. NÃO use ferramentas, responda direto.

PÚBLICO: {quem}
DORES DO PÚBLICO:
{chr(10).join('- ' + d for d in dores)}

Abaixo, trending topics do Twitter, do Google e fofocas do Leo Dias que estão em alta AGORA. Para CADA um, devolva:
- "tema": o nome exato como veio.
- "por_que": em <=90 caracteres, o que é / por que está em alta (se você não sabe o que é, escreva "?").
- "gancho": "sim: <a dor exata que dá pra conectar>" SÓ se der pra ligar numa dor SEM torcer o sentido; senão "nao".
- "sensivel": "nao" OU "sim: <o que há de sensível> | angulo: <como abordar com respeito>". Marque sensível quando envolver tragédia, morte, doença, ataque a grupo (xenofobia, homofobia, racismo, gordofobia), política partidária ou exposição de pessoa real. O ângulo seguro é sempre solidariedade / a mecânica do fenômeno, NUNCA deboche ou julgamento.

TRENDS:
{linhas}

Responda SOMENTE um array JSON, sem markdown, sem texto antes ou depois. Um objeto por trend, na mesma ordem."""
    try:
        p = subprocess.run(
            ["claude", "-p", prompt,
             "--model", "haiku",
             "--permission-mode", "bypassPermissions",
             "--allowedTools", "",
             "--max-budget-usd", "0.30"],
            capture_output=True, text=True, timeout=120,
        )
        txt = p.stdout.strip()
    except Exception:
        return {}
    # tira cercas ```json e pega do primeiro [ ao último ]
    txt = re.sub(r"^```[a-zA-Z]*", "", txt).strip().strip("`").strip()
    a, b = txt.find("["), txt.rfind("]")
    if a == -1 or b == -1 or b <= a:
        return {}
    try:
        arr = json.loads(txt[a : b + 1])
    except Exception:
        return {}
    out = {}
    for item in arr:
        if isinstance(item, dict) and item.get("tema"):
            out[norm(item["tema"])] = item
    return out


# ------------------------------------------------------------------- Block Kit
FONTE_LABEL = {"br": "BR", "mundo": "Mundo", "google": "Google BR", "leo": "Leo Dias"}


def emoji_para(cand, nota):
    if nota and str(nota.get("sensivel", "nao")).lower().startswith("sim"):
        return "🚩"
    if nota and str(nota.get("gancho", "nao")).lower().startswith("sim"):
        return "🎯"
    tag = cand.get("tag")
    if tag == "subindo":
        return "🔺"
    if tag == "novo":
        return "🆕"
    if tag == "nicho":
        return "🎯"
    return "•"


def tag_label(cand):
    tag = cand.get("tag")
    if tag == "subindo":
        return f"subindo +{cand.get('delta', 0)}"
    if tag == "novo":
        return "novo"
    if tag == "nicho":
        return "nicho"
    return "em alta"


def sec_mrkdwn(text):
    """section mrkdwn com teto de 3000 chars do Slack (corta se passar)."""
    return {"type": "section", "text": {"type": "mrkdwn", "text": trunc(text, LIM_SECTION)}}


def montar_blocks(destaques, notas, boards, url_maps, quando_fmt, fontes_fora, primeira):
    blocks = [{
        "type": "header",
        "text": {"type": "plain_text", "text": trunc(f"📡 Pulso de trends — {quando_fmt}", 150), "emoji": True},
    }]

    if destaques:
        titulo = "*🔥 Destaques desta hora*" if not primeira else "*🔥 Panorama inicial (primeira leitura)*"
        linhas = [titulo]
        for c in destaques:
            nota = notas.get(norm(c["nome"]))
            em = emoji_para(c, nota)
            nome_md = md_link(c["nome"], c["fonte"], url_maps)
            fonte_lbl = FONTE_LABEL.get(c["fonte"], c["fonte"])
            loc = fonte_lbl if c["fonte"] == "leo" else f'{fonte_lbl} #{c["rank"]}'
            cab = f'{em} *{nome_md}*  _{tag_label(c)}_ · {loc}'
            corpo = ""
            if nota:
                pq = str(nota.get("por_que", "")).strip()
                if pq and pq != "?":
                    corpo += f'\n{esc(trunc(pq, LIM_PORQUE))}'
                g = str(nota.get("gancho", "nao")).strip()
                if g.lower().startswith("sim"):
                    corpo += f'\n_gancho:_ {esc(trunc(g[4:].strip() or g, LIM_GANCHO))}'
                s = str(nota.get("sensivel", "nao")).strip()
                if s.lower().startswith("sim"):
                    corpo += f'\n⚠️ _{esc(trunc(s[4:].strip() or s, LIM_SENSIVEL))}_'
            linhas.append(cab + corpo)
        blocks.append(sec_mrkdwn("\n\n".join(linhas)))
    else:
        blocks.append(sec_mrkdwn("Sem grandes movimentos na última hora. Placar atual abaixo."))

    blocks.append({"type": "divider"})

    # placar compacto do Twitter + Google (nomes curtos, inline com link)
    board_txt = []
    for key in ("br", "mundo", "google"):
        nomes = boards.get(key, [])[: TOP_SHOW[key]]
        if nomes:
            linked = [md_link(n, key, url_maps) for n in nomes]
            board_txt.append(f'*{FONTE_LABEL[key]}:* ' + "  ·  ".join(linked))
    if board_txt:
        blocks.append(sec_mrkdwn("\n".join(board_txt)))

    # fofoca do Leo Dias em bloco próprio (manchetes longas, uma por linha)
    leo = boards.get("leo", [])[: TOP_SHOW["leo"]]
    if leo:
        linhas_leo = ["*🗞️ Fofoca — Leo Dias:*"]
        linhas_leo += [f'• {md_link(n, "leo", url_maps)}' for n in leo]
        blocks.append(sec_mrkdwn("\n".join(linhas_leo)))

    rodape = ("getdaytrends + Google Trends + Portal Leo Dias · leitura automática de hora "
              "em hora · detalhes: agente-carrosseis/data/trends-pulse.json")
    if fontes_fora:
        rodape += "  ·  ⚠️ fora: " + ", ".join(fontes_fora)
    blocks.append({"type": "context",
                   "elements": [{"type": "mrkdwn", "text": trunc(rodape, LIM_SECTION)}]})
    return blocks


# ------------------------------------------------------------------------ main
def main():
    payload_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        AGENTE, "logs", ".trends-pulse-payload.json")
    os.makedirs(DATA, exist_ok=True)

    try:
        relevance = json.load(open(RELEVANCE_PATH, encoding="utf-8"))
    except Exception:
        relevance = {}

    # 1) fetch + parse
    br = parse_getdaytrends(curl("https://getdaytrends.com/brazil/"))
    mundo = parse_getdaytrends(curl("https://getdaytrends.com/"))
    g_itens = parse_google_rss(curl("https://trends.google.com/trending/rss?geo=BR"))
    google = [g["nome"] for g in g_itens]
    g_noticia = {g["nome"]: g.get("noticia", "") for g in g_itens}
    leo_itens = parse_leodias(curl(LEO_FEED))
    leo = [x["nome"] for x in leo_itens]

    fontes_fora = []
    if not br:
        fontes_fora.append("Twitter BR")
    if not mundo:
        fontes_fora.append("Twitter Mundo")
    if not google:
        fontes_fora.append("Google BR")
    if not leo:
        fontes_fora.append("Leo Dias")

    if not br and not mundo and not google and not leo:
        print("FALHA_FONTES: nenhuma fonte respondeu")
        return 2

    boards = {"br": br, "mundo": mundo, "google": google, "leo": leo}
    url_maps = {
        "google": {norm(g["nome"]): g["url"] for g in g_itens},
        "leo": {norm(x["nome"]): x["url"] for x in leo_itens},
    }

    # 2) velocidade (novo/subindo) vs estado anterior
    estado_prev = carregar_estado()
    primeira = estado_prev is None
    movers = {}
    for key in BOARDS_KEYS:
        for k, v in classificar(key, boards[key], estado_prev).items():
            v = dict(v, fonte=key)
            # se já existe (mesmo trend em boards diferentes), fica com o de maior sinal
            if k not in movers or v.get("delta", 0) > movers[k].get("delta", 0):
                movers[k] = v

    # 3) candidatos do nicho (qualquer board), viram destaque mesmo sem subir.
    # Leo Dias entra aqui: é a fonte celebridade×estética (tipo o caso Vini Jr).
    nicho_keys = set()
    nicho_keys |= match_nicho(br)
    nicho_keys |= match_nicho(mundo)
    nicho_keys |= match_nicho(google, extra_text_por_nome=g_noticia)
    nicho_keys |= match_nicho(leo)

    # monta a lista de destaques: movers primeiro, depois nicho, depois (1ª rodada) topo
    destaques, usados = [], set()

    def add(cand):
        k = norm(cand["nome"])
        if k in usados:
            return
        usados.add(k)
        destaques.append(cand)

    # ordena movers: novos e quem subiu mais primeiro, priorizando posição alta
    def heat(v):
        base = 100 if v["tag"] == "novo" else 50 + v.get("delta", 0) * 5
        return base + (TOP_CONSIDER[v["fonte"]] - v["rank"])
    for v in sorted(movers.values(), key=heat, reverse=True):
        add(v)

    # itens do nicho (marcados como 'nicho' se ainda não entraram como mover)
    def achar_cand_nicho(k):
        for key in ("google", "leo", "br", "mundo"):  # google/leo primeiro (trazem contexto)
            for i, nome in enumerate(boards[key][: TOP_CONSIDER[key]]):
                if norm(nome) == k:
                    return {"nome": nome, "fonte": key, "rank": i + 1, "tag": "nicho"}
        return None
    for k in nicho_keys:
        if k in usados:
            continue
        c = achar_cand_nicho(k)
        if c:
            add(c)

    # 1ª rodada (sem base): sem movers, então mostra o topo pra dar o que anotar
    if primeira and not destaques:
        for key, n in (("leo", 2), ("google", 2), ("br", 2), ("mundo", 2)):
            for i, nome in enumerate(boards[key][:n]):
                add({"nome": nome, "fonte": key, "rank": i + 1, "tag": "topo"})

    destaques = destaques[:MAX_DESTAQUES]

    # 4) anotação da IA (haiku) só nos destaques
    notas = anotar_com_ia(
        [{"nome": c["nome"], "fonte": FONTE_LABEL.get(c["fonte"], c["fonte"]),
          "rank": c["rank"], "tag": c["tag"]} for c in destaques],
        relevance,
    )

    # 5) monta payload Block Kit
    agora = os.environ.get("PULSE_NOW_OVERRIDE")  # só pra teste determinístico
    if agora:
        quando_fmt = agora
        ts = agora
    else:
        from datetime import datetime
        n = datetime.now()
        quando_fmt = n.strftime("%d/%m %Hh%M")
        ts = n.strftime("%Y-%m-%d %H:%M")

    blocks = montar_blocks(destaques, notas, boards, url_maps, quando_fmt, fontes_fora, primeira)
    canal = os.environ.get("PULSE_SLACK_CHANNEL", "")
    n_dest = len(destaques)
    resumo = (f"{n_dest} destaque(s); topo BR: {br[0] if br else '—'}"
              if n_dest else f"sem movimento; topo BR: {br[0] if br else '—'}")
    payload = {
        "channel": canal,
        "text": trunc(f"📡 Pulso de trends — {esc(resumo)}", 2900),
        "unfurl_links": False,
        "unfurl_media": False,
        "blocks": blocks,
    }
    try:
        write_json_atomic(payload_path, payload)
    except Exception as e:
        print(f"FALHA_PAYLOAD: {e}")
        return 2

    # 6) snapshot (debug, todo run) + estado NOVO no .pending (shell promove após Slack ok).
    # Preserva a última leitura boa de cada board: se uma fonte falhou agora, não
    # apaga o baseline de velocidade (senão a fonte volta e vira tudo "novo" falso).
    estado_novo = {"rodado_em": ts}
    for k in BOARDS_KEYS:
        atual = boards[k][: TOP_CONSIDER[k]]
        if atual:
            estado_novo[k] = atual
        elif estado_prev and estado_prev.get(k):
            estado_novo[k] = estado_prev[k]
        else:
            estado_novo[k] = []
    snapshot = {
        "rodado_em": ts,
        "resumo": resumo,
        "destaques": [dict(c, nota=notas.get(norm(c["nome"])),
                           url=link_for(c["nome"], c["fonte"], url_maps)) for c in destaques],
        "boards": {k: boards[k][: TOP_CONSIDER[k]] for k in BOARDS_KEYS},
        "google_detalhe": g_itens[: TOP_CONSIDER["google"]],
        "leo_detalhe": leo_itens[: TOP_CONSIDER["leo"]],
        "fontes_fora": fontes_fora,
    }
    try:
        write_json_atomic(SNAP_PATH, snapshot, indent=2)
    except Exception:
        pass
    try:
        write_json_atomic(STATE_PENDING, estado_novo)
    except Exception:
        pass

    print(resumo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
