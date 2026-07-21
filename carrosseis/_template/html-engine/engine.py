# -*- coding: utf-8 -*-
"""
Engine HTML do carrossel RECONECTA — padrão validado (80% dos posts).

Replica fiel do design do Figma (arquivo fuIFq4fA94kKjvf2A7vhXo):
fundo bordô + grão, display Dx Monstral creme, corpo Grift, masthead/CTA Inter.
6 tipos de slide: hero · photo · text · list · proof · cta.

LAYOUT (regras do usuário, 30/jun):
- GAP de 32px entre TODOS os elementos (título→corpo, corpo→corpo, entre itens, etc.).
- Conteúdo dos slides de fundo (text/list/proof/cta) VERTICALMENTE CENTRALIZADO.
- Slides de foto (hero/photo) com o texto ancorado embaixo, sobre o scrim.
- Nenhum elemento sobrepõe outro (o punch nunca encosta nos prints).

Uso:
    python3 engine.py copy.json out_dir/      # renderiza os 6 PNGs 1080x1350

Marcação inline na copy:
    {texto}  -> ênfase VERMELHA (#ff2222)
    «texto»  -> ênfase CHAMPAGNE itálico (#f2ddb6)
    \\n       -> quebra de linha art-directed
"""
import base64, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "fonts")
GRAIN = os.path.join(HERE, "..", "grain.png")

W, H = 1080, 1350
MARGIN = 93
GAP = 32                 # gap único entre elementos (regra do usuário)
CONTENT_W = W - 2 * MARGIN
# Faixa vertical segura: clareira igual em cima e embaixo. Em cima limpa o
# masthead (top 73 + ~24 = ~97 -> 130 dá ~33px de respiro); simétrico mantém o
# centro do conteúdo no centro do canvas (675), o look que o usuário aprovou.
# Conteúdo curto centraliza igual; conteúdo alto fica preso na faixa (nunca sob
# o masthead). O que não couber na faixa é SINALIZADO (não encolhe, não corta calado).
SAFE_V = 130
BAND_H = H - 2 * SAFE_V   # 1090 — faixa de centralização confortável (ideal)
# Limite de COLISÃO real: o masthead vai até ~y96; o punch precisa de ~14px de
# respiro. Conteúdo centrado (no centro 675) só encosta no masthead quando passa
# de ~1130px de altura. Entre BAND_H e OVERFLOW_LIMIT o conteúdo centra apertado
# mas LIMPO (sem colisão, sem corte) — verificado a olho. Acima disso = quebrado.
OVERFLOW_LIMIT = H - 2 * 110   # 1130 — acima disso o flag dispara

# ---- paleta (design-spec.md) ----
BG_TEXT   = "#2d0000"   # bordô profundo (slides de texto)
BG_DARK   = "#0f0e0e"   # quase-preto (photo + cta)
BG_HERO   = "#6b0f0f"   # atrás da foto do hero
CREAM     = "#faf0dd"   # display / punch
CHAMPAGNE = "#f2ddb6"   # ênfase
BODY      = "#ececec"   # corpo
RED       = "#ff2222"   # números, destaque, borda do callout
LABEL     = "#f5f5f5"   # masthead / cta


def _b64_font(fname):
    with open(os.path.join(FONTS, fname), "rb") as f:
        return base64.b64encode(f.read()).decode()


def _b64_file(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def _font_face(family, fname, weight="400", style="normal"):
    ext = "opentype" if fname.lower().endswith(".otf") else "truetype"
    return (f"@font-face{{font-family:'{family}';font-weight:{weight};"
            f"font-style:{style};src:url(data:font/{ext};base64,{_b64_font(fname)}) "
            f"format('{ext}');}}")


def _fonts_css():
    faces = [
        _font_face("DxMonstral", "DxMonstral-Regular.otf"),
        _font_face("Grift", "Grift-Regular.ttf", "400"),
        _font_face("Grift", "Grift-Italic.ttf", "400", "italic"),
        _font_face("Grift", "Grift-Black.ttf", "900"),
        _font_face("Grift", "Grift-BlackItalic.ttf", "900", "italic"),
        _font_face("Inter", "Inter-Medium.ttf", "500"),
        _font_face("Inter", "Inter-Bold.ttf", "700"),
    ]
    return "\n".join(faces)


def _inline(text):
    """Escapa HTML e aplica marcação inline {vermelho}, «champagne» e \\n."""
    out, i, n = [], 0, len(text)
    while i < n:
        c = text[i]
        if c == "{":
            j = text.find("}", i)
            if j != -1:
                out.append(f'<span class="red">{html.escape(text[i+1:j])}</span>')
                i = j + 1
                continue
        if c == "«":
            j = text.find("»", i)
            if j != -1:
                out.append(f'<span class="champ">{html.escape(text[i+1:j])}</span>')
                i = j + 1
                continue
        if c == "\n":
            out.append("<br>")
            i += 1
            continue
        out.append(html.escape(c))
        i += 1
    return "".join(out)


def _img_data(path, base_dir):
    if not path:
        return None
    p = path if os.path.isabs(path) else os.path.join(base_dir, path)
    if not os.path.exists(p):
        return None
    ext = os.path.splitext(p)[1].lstrip(".").lower() or "png"
    if ext == "jpg":
        ext = "jpeg"
    return f"data:image/{ext};base64,{_b64_file(p)}"


def _noise_uri():
    """Film grain fino via SVG feTurbulence — crisp, alta definição, leve."""
    svg = ("<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'>"
           "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' "
           "numOctaves='2' stitchTiles='stitch'/>"
           "<feColorMatrix type='saturate' values='0'/></filter>"
           "<rect width='100%' height='100%' filter='url(#n)'/></svg>")
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


# ----------------------------------------------------------------------------
# CSS base
# ----------------------------------------------------------------------------
def _base_css():
    noise = _noise_uri()
    return f"""
*{{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;
   text-rendering:geometricPrecision;}}
html,body{{width:{W}px;height:{H}px;}}
.slide{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{BG_TEXT};}}
.grain{{position:absolute;inset:0;background-image:url({noise});
        background-size:220px 220px;opacity:.12;mix-blend-mode:overlay;
        pointer-events:none;z-index:5;}}
.photo{{position:absolute;inset:0;object-fit:cover;width:100%;height:100%;z-index:1;}}
.scrim{{position:absolute;inset:0;z-index:2;}}
.mast{{position:absolute;top:73px;right:{MARGIN}px;z-index:7;
       font-family:'Grift';font-weight:900;font-size:19px;letter-spacing:.16em;
       color:{BODY};text-transform:uppercase;}}

/* conteúdo dos slides de fundo: centralizado na FAIXA SEGURA (clareira igual em
   cima/embaixo), gap único de 32px. Conteúdo alto nunca colide com o masthead. */
.center-wrap{{position:absolute;left:{MARGIN}px;right:{MARGIN}px;
   top:{SAFE_V}px;bottom:{SAFE_V}px;
   display:flex;flex-direction:column;justify-content:center;align-items:center;
   gap:{GAP}px;z-index:6;}}
/* conteúdo dos slides de foto: ancorado embaixo, sobre o scrim */
.bottom-wrap{{position:absolute;left:{MARGIN}px;right:{MARGIN}px;
   display:flex;flex-direction:column;align-items:center;gap:{GAP}px;z-index:6;}}
.center-wrap > .punch, .center-wrap > .body, .center-wrap > .callout,
.center-wrap > .list-container,
.bottom-wrap > .punch, .bottom-wrap > .body{{width:100%;}}
/* hero-h é flex item: sem width explícito ele cresce até max-content (linha nowrap
   estoura o canvas e o fit mede scrollWidth==clientWidth e não encolhe — caso real
   20/jul, hero Vini Jr). width:100% devolve a régua dos 894px úteis ao fit. */
.bottom-wrap > .hero-h{{width:100%;}}

.display{{font-family:'DxMonstral';color:{CREAM};text-transform:uppercase;
          line-height:.99;letter-spacing:0;}}
.hero-h{{font-size:98px;text-align:center;}}
/* quebra art-directed é lei: a linha nunca quebra no meio — a fonte desce até caber */
.hero-h .hl{{display:block;white-space:nowrap;}}
.punch{{font-size:60px;line-height:1.0;letter-spacing:-.005em;text-align:center;}}
.punch.left{{text-align:left;}}
.red{{color:{RED};}}
.champ{{color:{CHAMPAGNE};font-family:'Grift';font-style:italic;}}

.body{{font-family:'Grift';font-weight:400;font-size:34px;line-height:1.4;
       color:{BODY};text-align:center;}}

/* botão outline (pill) — hero e cta, mesmo componente */
.pill{{display:inline-flex;align-items:center;gap:16px;border:1px solid {LABEL};
       border-radius:20px;padding:14px 28px;}}
.pill .txt{{font-family:'Inter';font-weight:700;font-size:18px;letter-spacing:.14em;
            color:{LABEL};text-transform:uppercase;}}
.pill .sep{{font-family:'Inter';font-weight:500;font-size:20px;color:{LABEL};opacity:.85;}}
.pill .arrow{{width:30px;height:2px;background:{LABEL};position:relative;}}
.pill .arrow::after{{content:'';position:absolute;right:0;top:-4px;width:9px;height:9px;
                     border-top:2px solid {LABEL};border-right:2px solid {LABEL};
                     transform:rotate(45deg);}}

/* lista numerada — gap de 32px dentro do item (título→corpo) e entre itens */
.list-container{{width:100%;display:flex;flex-direction:column;gap:{GAP}px;}}
.item{{position:relative;padding-left:84px;}}
.item .num{{position:absolute;left:0;top:0;font-family:'Grift';font-weight:900;
            font-size:34px;color:{RED};line-height:1.0;}}
.item-col{{display:flex;flex-direction:column;gap:{GAP}px;}}
.it-title{{font-family:'Grift';font-weight:900;font-size:34px;color:{CREAM};line-height:1.05;}}
.it-body{{font-family:'Grift';font-weight:400;font-size:34px;line-height:1.35;color:{BODY};}}

/* callout (gancho pro próximo slide) */
.callout{{border:2px solid {RED};border-radius:14px;padding:30px 34px;
          font-family:'Grift';font-style:italic;font-weight:400;font-size:34px;
          line-height:1.35;color:{CHAMPAGNE};text-align:center;}}

/* prova social — prints whatsapp num bloco próprio (nunca sobrepõe o punch) */
.prints-block{{position:relative;width:100%;height:820px;}}
.print{{position:absolute;z-index:6;border-radius:14px;overflow:hidden;max-height:360px;
        box-shadow:0 18px 50px rgba(0,0,0,.45);}}
.print img{{display:block;width:100%;height:auto;}}
.print.empty{{background:#d9d9d9;height:190px;}}
"""


# ----------------------------------------------------------------------------
# componentes
# ----------------------------------------------------------------------------
def _mast():
    return '<div class="mast">RECONECTA</div>'


def _pill(label):
    return (f'<span class="pill"><span class="txt">{label}</span>'
            f'<span class="sep">/</span><span class="arrow"></span></span>')


def _punch(s):
    align = " left" if s.get("align") == "left" else ""
    return f'<div class="display punch{align}">{_inline(s["punch"])}</div>'


def _bodies(s):
    return "".join(f'<div class="body">{_inline(b)}</div>' for b in s.get("body", []))


# ----------------------------------------------------------------------------
# slides
# ----------------------------------------------------------------------------
def slide_hero(s, base_dir):
    img = _img_data(s.get("image"), base_dir)
    photo = f'<img class="photo" src="{img}">' if img else ""
    # fx opcionais de legibilidade (por slide, retrocompatível):
    #   scrim:"strong" | dim:0..1 (véu uniforme) | spot:true (radial atrás do texto)
    #   shadow:true (halo escuro nas letras)
    fx = s.get("fx") or {}
    if fx.get("scrim") == "strong":
        grad = ('rgba(20,4,4,.12) 0%,rgba(20,4,4,.16) 34%,rgba(20,4,4,.74) 64%,'
                'rgba(20,4,4,.92) 100%')
    else:
        grad = ('rgba(20,4,4,.05) 0%,rgba(20,4,4,0) 38%,rgba(20,4,4,.55) 78%,'
                'rgba(20,4,4,.82) 100%')
    scrim = f'<div class="scrim" style="background:linear-gradient(180deg,{grad});"></div>'
    if fx.get("dim"):
        scrim += f'<div class="scrim" style="background:rgba(15,8,8,{fx["dim"]});"></div>'
    if fx.get("spot"):
        scrim += ('<div class="scrim" style="background:radial-gradient(ellipse 64% 36% at 50% 72%,'
                  'rgba(15,6,6,.72) 0%,rgba(15,6,6,.42) 55%,rgba(15,6,6,0) 100%);"></div>')
    hstyle = (' style="text-shadow:0 4px 26px rgba(10,2,2,.85),0 2px 10px rgba(10,2,2,.6);"'
              if fx.get("shadow") else '')
    # cada linha art-directed vira um bloco nowrap: o fit (render) ajusta o corpo
    # da fonte pra linha mais longa caber inteira — nunca quebra no meio da linha
    lines = s["headline"].split("\n")
    inner = "".join(f'<span class="hl">{_inline(l)}</span>' for l in lines)
    headline = f'<div class="display hero-h"{hstyle}>{inner}</div>'
    return (f'<div class="slide" style="background:{BG_HERO};">{photo}{scrim}'
            f'<div class="grain"></div>'
            f'<div class="bottom-wrap" style="bottom:88px;">{headline}'
            f'{_pill("RECONECTA")}</div></div>')


def slide_photo(s, base_dir):
    img = _img_data(s.get("image"), base_dir)
    # sem foto ainda (placeholder): centraliza como text pra não ficar void preto no topo.
    # com foto: texto ancorado embaixo sobre o scrim (layout final).
    if not img:
        return (f'<div class="slide" style="background:{BG_DARK};">'
                f'<div class="grain"></div>{_mast()}'
                f'<div class="center-wrap">{_punch(s)}{_bodies(s)}</div></div>')
    scrim = ('<div class="scrim" style="background:linear-gradient(180deg,'
             'rgba(15,14,14,.05) 0%,rgba(15,14,14,0) 30%,rgba(15,14,14,.72) 62%,'
             'rgba(15,14,14,.95) 100%);"></div>')
    return (f'<div class="slide" style="background:{BG_DARK};">'
            f'<img class="photo" src="{img}">{scrim}'
            f'<div class="grain"></div>{_mast()}'
            f'<div class="bottom-wrap" style="bottom:104px;">{_punch(s)}'
            f'{_bodies(s)}</div></div>')


def slide_text(s, base_dir):
    callout = (f'<div class="callout">{_inline(s["callout"])}</div>'
               if s.get("callout") else "")
    return (f'<div class="slide"><div class="grain"></div>{_mast()}'
            f'<div class="center-wrap">{_punch(s)}{_bodies(s)}{callout}</div></div>')


def slide_list(s, base_dir):
    items = ""
    for i, it in enumerate(s.get("items", []), 1):
        # tira numeração baked no título ("1. ", "2) ") — o engine já numera à esquerda
        title = re.sub(r'^\s*\d+[.)]\s+', '', it["title"])
        items += (f'<div class="item"><span class="num">{i}.</span>'
                  f'<div class="item-col">'
                  f'<div class="it-title">{_inline(title)}</div>'
                  f'<div class="it-body">{_inline(it["body"])}</div></div></div>')
    return (f'<div class="slide"><div class="grain"></div>{_mast()}'
            f'<div class="center-wrap">{_punch(s)}'
            f'<div class="list-container">{items}</div></div></div>')


def slide_proof(s, base_dir):
    # cards espalhados/rotacionados DENTRO do bloco (coords relativas ao bloco)
    defaults = [
        {"x": 0,   "y": 0,   "w": 545, "rot": -2.5},
        {"x": 175, "y": 235, "w": 565, "rot": 2},
        {"x": 15,  "y": 470, "w": 555, "rot": -2},
    ]
    custom = s.get("positions") or []
    cfgs = [custom[i] if i < len(custom)
            else defaults[i] if i < len(defaults)
            else {"x": 40, "y": 360, "w": 560, "rot": 0}
            for i in range(len(s.get("prints", [])))]
    # centraliza o GRUPO na horizontal: a cascata mantém o stagger entre cards,
    # mas o conjunto fica no meio do bloco (nunca encostado num canto)
    if cfgs:
        block_w = W - 2 * MARGIN
        min_x = min(c["x"] for c in cfgs)
        max_x = max(c["x"] + c["w"] for c in cfgs)
        off = round((block_w - (max_x - min_x)) / 2 - min_x)
        cfgs = [{**c, "x": c["x"] + off} for c in cfgs]
    prints = ""
    for p, cfg in zip(s.get("prints", []), cfgs):
        img = _img_data(p, base_dir)
        inner = f'<img src="{img}">' if img else ""
        empty = "" if img else " empty"
        style = (f'left:{cfg["x"]}px;top:{cfg["y"]}px;width:{cfg["w"]}px;'
                 f'transform:rotate({cfg["rot"]}deg);')
        prints += f'<div class="print{empty}" style="{style}">{inner}</div>'
    # altura do bloco por-slide (retrocompatível): prints curtos (bolhas de 1 linha)
    # deixam a faixa de 820px meio vazia → center-wrap centra um bloco todo no topo.
    # setar "block_h" faz o bloco abraçar o conteúdo e o center-wrap centra de verdade.
    bh = s.get("block_h")
    # block_h explícito = altura travada (data-fixed impede o auto-fit do render);
    # sem block_h, o render mede a borda real dos prints e abraça o conteúdo,
    # senão o espaço morto do bloco fixo empurra o slide inteiro pro topo.
    bstyle = f' style="height:{bh}px;" data-fixed="1"' if bh else ""
    return (f'<div class="slide"><div class="grain"></div>{_mast()}'
            f'<div class="center-wrap">{_punch(s)}'
            f'<div class="prints-block"{bstyle}>{prints}</div></div></div>')


def slide_cta(s, base_dir):
    cta = s.get("cta", "TOQUE NO LINK DA BIO")
    return (f'<div class="slide" style="background:{BG_DARK};">'
            f'<div class="grain"></div>'
            f'<div class="center-wrap">{_punch(s)}{_pill(html.escape(cta))}</div></div>')


RENDERERS = {
    "hero": slide_hero, "photo": slide_photo, "text": slide_text,
    "list": slide_list, "proof": slide_proof, "cta": slide_cta,
}


def build_html(slide, base_dir):
    fn = RENDERERS[slide["type"]]
    body = fn(slide, base_dir)
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>'
            f'{_fonts_css()}{_base_css()}</style></head><body>{body}</body></html>')


def build_preview(slides, out_dir, base_dir):
    """Página HTML com os 6 slides renderizados em grid — pra revisar no navegador."""
    rel = os.path.relpath(out_dir, base_dir)
    cards = []
    for i, s in enumerate(slides, 1):
        png = os.path.join(out_dir, f"slide_{i}.png")
        v = int(os.path.getmtime(png)) if os.path.exists(png) else 0  # cache-buster
        cards.append(
            f'<figure><img src="{rel}/slide_{i}.png?v={v}">'
            f'<figcaption>slide {i} · {s.get("type","")}</figcaption></figure>')
    css = ("body{margin:0;background:#141414;color:#eee;padding:28px;"
           "font-family:-apple-system,Inter,Helvetica,sans-serif;}"
           "h1{font:600 14px/1 Inter,sans-serif;letter-spacing:.1em;color:#f2ddb6;"
           "text-transform:uppercase;margin:0 0 22px;}"
           ".grid{display:flex;flex-wrap:wrap;gap:22px;}"
           "figure{margin:0;width:300px;}"
           "figure img{width:300px;height:auto;display:block;border-radius:8px;"
           "box-shadow:0 10px 34px rgba(0,0,0,.5);}"
           "figcaption{font-size:12px;color:#9a9a9a;margin-top:8px;text-align:center;}")
    return (f'<!doctype html><html><head><meta charset="utf-8"><title>Preview</title>'
            f'<style>{css}</style></head><body><h1>Preview · {len(slides)} slides</h1>'
            f'<div class="grid">{"".join(cards)}</div></body></html>')


# JS que mede a altura natural do bloco de conteúdo (do topo do 1º filho à base
# do último). Se passar da faixa segura, o conteúdo não cabe — overflow real.
_MEASURE_JS = """() => {
  const w = document.querySelector('.center-wrap');
  if (!w) return null;
  const kids = [...w.children];
  if (!kids.length) return 0;
  const top = Math.min(...kids.map(k => k.getBoundingClientRect().top));
  const bot = Math.max(...kids.map(k => k.getBoundingClientRect().bottom));
  return Math.round(bot - top);
}"""

# fit do bloco de prints (proof): abraça a borda real dos cards (rotação inclusa)
# pro center-wrap centrar o conteúdo de verdade — espaço morto no bloco fixo era o
# que puxava o slide pro terço superior. block_h explícito (data-fixed) é respeitado.
_PROOF_FIT_JS = """() => {
  const b = document.querySelector('.prints-block');
  if (!b || b.dataset.fixed) return null;
  const prints = [...b.querySelectorAll('.print')];
  if (!prints.length) return null;
  const bt = b.getBoundingClientRect().top;
  const tops = prints.map(p => p.getBoundingClientRect().top - bt);
  const minTop = Math.min(...tops);
  if (minTop > 0) prints.forEach(p => {
    p.style.top = (parseFloat(p.style.top || '0') - minTop) + 'px';
  });
  const bottom = Math.max(...prints.map(p => p.getBoundingClientRect().bottom));
  const h = Math.ceil(bottom - bt);
  b.style.height = h + 'px';
  return h;
}"""

# fit da headline do hero: desce o corpo (passo 2px) até a linha art-directed mais
# longa caber inteira. Piso de 60px: abaixo disso é problema de COPY (requebrar as
# linhas), não de fonte — o piso libera o wrap pra não cortar e o render avisa.
HERO_FIT_FLOOR = 60
_HERO_FIT_JS = """() => {
  const h = document.querySelector('.hero-h');
  if (!h) return null;
  const lines = [...h.querySelectorAll('.hl')];
  if (!lines.length) return null;
  const fits = () => lines.every(l => l.scrollWidth <= h.clientWidth + 1);
  let size = parseFloat(getComputedStyle(h).fontSize);
  while (!fits() && size > %d) {
    size -= 2;
    h.style.fontSize = size + 'px';
  }
  if (!fits()) {
    lines.forEach(l => l.style.whiteSpace = 'normal');
    return {size: size, floor_hit: true};
  }
  return {size: size, floor_hit: false};
}""" % HERO_FIT_FLOOR


def render(copy_path, out_dir):
    from playwright.sync_api import sync_playwright
    base_dir = os.path.dirname(os.path.abspath(copy_path))
    data = json.load(open(copy_path, encoding="utf-8"))
    os.makedirs(out_dir, exist_ok=True)
    slides = data["slides"]
    overflows = []  # slides cujo conteúdo não cabe na faixa segura
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": H},
                                device_scale_factor=1)
        for idx, s in enumerate(slides, 1):
            page.set_content(build_html(s, base_dir), wait_until="networkidle")
            page.wait_for_timeout(120)
            # hero: garante quebra art-directed intacta (fonte desce até caber)
            fit = page.evaluate(_HERO_FIT_JS)
            if fit:
                if fit["floor_hit"]:
                    overflows.append({"slide": idx, "type": "hero_fit",
                                      "size": fit["size"], "floor": HERO_FIT_FLOOR})
                    print(f"⚠ HERO slide_{idx}: linha mais longa não coube nem a "
                          f"{fit['size']}px — REQUEBRAR a headline em linhas mais curtas.")
                elif fit["size"] < 98:
                    print(f"  hero fit: headline a {fit['size']}px pra honrar as quebras")
            # proof: bloco de prints abraça o conteúdo real antes da centralização
            pfit = page.evaluate(_PROOF_FIT_JS)
            if pfit is not None:
                print(f"  proof fit: bloco de prints a {pfit}px")
            # checa overflow nos slides de fundo (têm .center-wrap). O flag dispara
            # no limite de COLISÃO (1130), não na faixa de conforto (1090): entre os
            # dois o conteúdo centra apertado mas limpo.
            ch = page.evaluate(_MEASURE_JS)
            if ch is not None and ch > OVERFLOW_LIMIT:
                over = ch - OVERFLOW_LIMIT
                overflows.append({"slide": idx, "type": s.get("type"),
                                  "content_h": ch, "limit": OVERFLOW_LIMIT, "over_px": over})
                print(f"⚠ OVERFLOW slide_{idx} ({s.get('type')}): "
                      f"conteúdo {ch}px > limite {OVERFLOW_LIMIT}px — colide/corta ~{over}px. "
                      f"ENCURTAR A COPY (não encolher fonte).")
            out = os.path.join(out_dir, f"slide_{idx}.png")
            page.locator(".slide").screenshot(path=out)
            print("ok", out)
        browser.close()
    # marcador durável: nunca deixa overflow virar corte silencioso
    marker = os.path.join(out_dir, "_overflow.json")
    if overflows:
        json.dump(overflows, open(marker, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        print(f"⚠ {len(overflows)} slide(s) com overflow — ver {marker}")
    elif os.path.exists(marker):
        os.remove(marker)  # limpa marcador antigo quando tudo cabe
    # preview HTML pra revisar no navegador (sempre)
    prev = os.path.join(base_dir, "preview.html")
    open(prev, "w", encoding="utf-8").write(build_preview(slides, out_dir, base_dir))
    print("preview", prev)
    return overflows


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    render(sys.argv[1], sys.argv[2])
