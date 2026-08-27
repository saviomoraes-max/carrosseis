# -*- coding: utf-8 -*-
"""
Engine HTML do carrossel RECONECTA — padrão validado (80% dos posts).

Replica fiel do design do Figma (arquivo fuIFq4fA94kKjvf2A7vhXo):
fundo bordô + grão, display Dx Monstral creme, corpo Grift, masthead/CTA Inter.
7 tipos de slide: hero · hero_b · photo · text · list · proof · cta.

hero_b = CAPA DO POST B (design novo do Sávio, Figma RqH8mGZh6JLe5qKl3fo3aw,
28/jul/26 — replicado por API + render-compare). Capa editorial de notícia:
foto full-bleed, scrim que satura em 84% (a foto sempre respira embaixo),
textura de ruído ISO em blend screen 32% (asset noise-b.jpg, recorte exato da
composição original), headline Inter 68px creme em CAIXA NORMAL com quebra
NATURAL (sem \\n obrigatório — filosofia oposta à do hero A) e ênfase por PESO
({palavra} vira Inter Black 900, NUNCA vermelho), marca "/ →" no rodapé.
Slides 2-6 do post B são idênticos aos do post A.

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
NOISE_B = os.path.join(HERE, "noise-b.jpg")   # textura da capa B (recorte exato do Figma)
# design C (Figma E1vW9mVqVHmLvttYmcOiVN, lido pela API em 17/ago/26):
# recortes exatos da geometria dos rects do frame (ver design-c-assets no SSD)
HC_ISO = os.path.join(HERE, "hc-iso.jpg")            # ISO Noise_03 — screen 32%
HC_HALFTONE = os.path.join(HERE, "hc-halftone.jpg")  # "10 1" halftone — color-dodge

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
# ---- design D "dossiê" (Reconecta Design System / Anúncios.fig — aprovado 27/ago,
# layout INVERTIDO pelo Sávio: chrome no topo, copy embaixo; substitui o design B) ----
D_PEARL    = "#EED9BD"  # texto principal
D_GOLD     = "#EECE66"  # kicker/HUD/ênfase (no D a ênfase «» vira dourado)
D_SCARLET  = "#D3111A"  # SÓ o ponto REC (nunca em texto)
D_OBSIDIAN = "#161616"  # fundo dos slides
D_BARS     = [3, 7, 3, 3, 10, 3, 6, 3, 3, 8, 3, 5, 10, 3]  # barcode do dossiê


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
        _font_face("Inter", "Inter-Regular.ttf", "400"),
        _font_face("Inter", "Inter-Medium.ttf", "500"),
        _font_face("Inter", "Inter-Bold.ttf", "700"),
        _font_face("Inter", "Inter-Black.ttf", "900"),
        _font_face("SubdaysTight", "SubdaysTight.ttf", "400"),
        # design D — TT Modernoir TRIAL (decisão do Sávio 27/ago: publicar com a
        # trial e trocar quando licenciar) + Space Mono (chrome do dossiê)
        _font_face("TTModernoir", "TT_Modernoir_Trial_Bold.ttf", "700"),
        _font_face("SpaceMono", "SpaceMono-Regular.ttf", "400"),
        _font_face("SpaceMono", "SpaceMono-Bold.ttf", "700"),
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


def _words_spans(text):
    """Cada palavra num <span class='w'> — a guarda de órfã da capa B agrupa os
    spans por linha renderizada (a quebra aqui é NATURAL, não art-directed)."""
    parts = []
    for tok in re.split(r"(\s+)", text):
        if not tok:
            continue
        if tok.isspace():
            parts.append(" ")
        else:
            parts.append(f'<span class="w">{html.escape(tok)}</span>')
    return "".join(parts)


def _inline_hb(text):
    """Marcação da capa B: {palavra} vira PESO (Inter Black 900), nunca cor —
    o design novo enfatiza por peso no mesmo creme. «» não existe aqui. \\n é
    respeitado se vier, mas a quebra padrão é natural (caixa de 894px)."""
    out = []
    for i, bloco in enumerate(text.split("\n")):
        if i:
            out.append("<br>")
        pos = 0
        for m in re.finditer(r"\{([^}]*)\}", bloco):
            out.append(_words_spans(bloco[pos:m.start()]))
            out.append(f'<span class="hb-em">{_words_spans(m.group(1))}</span>')
            pos = m.end()
        out.append(_words_spans(bloco[pos:]))
    return "".join(out)


def _inline_hc(text):
    """Marcação da capa C: {palavra} vira SUBLINHADO (textDecoration UNDERLINE do
    Figma). «» não existe aqui. \\n é respeitado se vier, mas a quebra padrão é
    natural (caixa de 894px, centrada)."""
    out = []
    for i, bloco in enumerate(text.split("\n")):
        if i:
            out.append("<br>")
        pos = 0
        for m in re.finditer(r"\{([^}]*)\}", bloco):
            out.append(_words_spans(bloco[pos:m.start()]))
            out.append(f'<span class="hc-em">{_words_spans(m.group(1))}</span>')
            pos = m.end()
        out.append(_words_spans(bloco[pos:]))
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
.center-wrap > .list-container, .center-wrap > .fecho,
.bottom-wrap > .punch, .bottom-wrap > .body{{width:100%;}}
/* hero-h fica SEM width: como flex item ele cresce até max-content e o
   align-items:center do wrap centraliza inclusive o sangramento além da margem
   (simétrico, como nas capas canônicas). width:100% aqui pendura a linha larga
   só pra direita — caso real 21/jul (AD003, ponto final na borda; o Sávio pegou).
   A régua de largura vive no fit (HERO_LINE_MAX_W), medida por Range no texto. */

.display{{font-family:'DxMonstral';color:{CREAM};text-transform:uppercase;
          line-height:.99;letter-spacing:0;}}
.hero-h{{font-size:98px;text-align:center;}}
/* quebra art-directed é lei: a linha nunca quebra no meio — a fonte desce até caber */
.hero-h .hl{{display:block;white-space:nowrap;}}
.punch{{font-size:60px;line-height:1.0;letter-spacing:-.005em;text-align:center;}}
.punch.left{{text-align:left;}}
/* quebra art-directed do punch é lei (como no hero): a linha nunca quebra no meio.
   Linha larga demais NÃO encolhe a fonte — o render acusa e a linha é REQUEBRADA.
   Caso real 21/jul: "SE VOCÊ QUER PARAR DE PERDER" não coube e o browser derrubou
   "PERDER" órfão em silêncio (AD005 SEM30, o Sávio pegou no preview). */
.punch .pl{{display:block;white-space:nowrap;}}
/* subheadline do hero: a VIRADA de registro embaixo da aspa (canon SEM25/AD002,
   "headline grande + itálico champagne embaixo"). Nunca embutir a virada como
   linha gigante da própria headline — desequilibra a pirâmide e encolhe a capa. */
.hero-sub{{font-family:'Grift';font-style:normal;font-weight:400;font-size:40px;
   line-height:1.25;color:{CHAMPAGNE};text-align:center;
   text-shadow:0 2px 14px rgba(10,2,2,.65);}}
.red{{color:{RED};}}
/* Ênfase champagne = SÓ COR. Nunca itálico, nunca peso menor (regra do Sávio,
   05/ago/26: "nunca mais coloque alguma palavra em itálico e numa fonte mais
   fina"). O defeito: .champ era italic sem font-weight, então dentro de uma
   headline 900 a palavra caía pra 400 — itálica E fininha no meio do display. */
.champ{{color:{CHAMPAGNE};font-style:normal;font-weight:inherit;}}

/* ---- CAPA B (design novo, Figma RqH8mGZh6JLe5qKl3fo3aw — medidas da API) ----
   headline: caixa de 894px (margens 93), Inter 68/82.3 ls -4.08px, creme #FAF0DE,
   caixa NORMAL (nunca uppercase), quebra NATURAL centrada; ênfase = peso 900.
   bloco ancorado embaixo: base do texto a 216px do rodapé, marca "/ →" fixa. */
.hb-wrap{{position:absolute;left:{MARGIN}px;right:{MARGIN}px;bottom:135px;
   display:flex;flex-direction:column;align-items:center;gap:30px;z-index:6;}}
.hb-h{{width:100%;font-family:'Inter';font-weight:400;font-size:68px;
   line-height:82.3px;letter-spacing:-4.08px;color:#faf0de;text-align:center;}}
.hb-em{{font-weight:900;}}
.hb-scrim{{position:absolute;inset:0;z-index:2;
   background:linear-gradient(180deg,rgba(26,0,1,0) 28.74%,rgba(26,0,1,.84) 69.86%);}}
.hb-noise{{position:absolute;inset:0;z-index:3;mix-blend-mode:screen;opacity:.32;
   background-size:1080px 1350px;pointer-events:none;}}
.hb-mark{{display:flex;align-items:center;gap:22px;height:40px;margin-left:-8px;}}
.hb-slash{{font-family:'Inter';font-weight:700;font-size:32.7px;
   letter-spacing:4.57px;color:{LABEL};line-height:40px;}}
.hb-arrow{{width:31px;height:3.6px;background:{LABEL};position:relative;}}
.hb-arrow::after{{content:'';position:absolute;right:-1px;top:-5.4px;width:11px;
   height:11px;border-top:3.6px solid {LABEL};border-right:3.6px solid {LABEL};
   transform:rotate(45deg);}}

/* ---- CAPA C (3º post/dia, Figma E1vW9mVqVHmLvttYmcOiVN — medidas da API) ----
   headline: caixa de 894px (margens 93), Subdays Tight 114/118.5 ls 2.28px, creme
   #FAF0DE, caixa NORMAL, quebra NATURAL centrada; ênfase = SUBLINHADO.
   camadas: bordô -> foto -> gradiente 94% (topo transparente -> #010A11) ->
   ISO screen 32% -> halftone color-dodge. Sem masthead, sem pill, sem grain A. */
.hc-wrap{{position:absolute;left:{MARGIN}px;right:{MARGIN}px;bottom:93px;
   display:flex;flex-direction:column;align-items:center;z-index:6;}}
.hc-h{{width:100%;font-family:'SubdaysTight';font-weight:400;font-size:114px;
   line-height:118.5px;letter-spacing:2.28px;color:#faf0de;text-align:center;}}
.hc-em{{text-decoration:underline;text-decoration-thickness:6px;
   text-underline-offset:14px;}}
.hc-grad{{position:absolute;inset:0;z-index:2;opacity:.94;
   background:linear-gradient(180deg,rgba(26,0,1,0) 28.74%,rgba(1,10,17,1) 69.86%);}}
.hc-iso{{position:absolute;inset:0;z-index:3;mix-blend-mode:screen;opacity:.32;
   background-size:1080px 1350px;pointer-events:none;}}
.hc-half{{position:absolute;inset:0;z-index:4;mix-blend-mode:color-dodge;
   background-size:1080px 1350px;pointer-events:none;}}

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

/* fecho da lista — o saldo, DEPOIS dos passos (forma do SEM25/AD003, s/r 3,95%:
   os scripts primeiro, e só então a frase que diz o que você acabou de fazer).
   Campo opcional "fecho" no slide list; sem ele nada muda. */
.fecho{{font-family:'Grift';font-weight:900;font-size:40px;line-height:1.12;
        color:{CHAMPAGNE};text-align:center;}}

/* callout (gancho pro próximo slide) */
.callout{{border:2px solid {RED};border-radius:14px;padding:30px 34px;
          font-family:'Grift';font-style:normal;font-weight:400;font-size:34px;
          line-height:1.35;color:{CHAMPAGNE};text-align:center;}}

/* cartão retangular de foto em slide interno (text/list) — pedido do Sávio
   27/ago no design D ("pouca imagem pra muito texto"): foto que CONVERSA com o
   slide, sempre LIMPA — imagem com texto embutido é vetada (confunde o leitor,
   caso pote Sallve). Disponível em qualquer design via campo "image". */
.photo-card{{width:100%;overflow:hidden;flex-shrink:0;}}
.photo-card img{{width:100%;height:100%;object-fit:cover;display:block;}}

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
    # cada linha art-directed vira bloco nowrap — o render mede e acusa linha
    # que não cabe (requebrar copy, nunca deixar o browser quebrar sozinho)
    lines = s["punch"].split("\n")
    inner = "".join(f'<span class="pl">{_inline(l)}</span>' for l in lines)
    return f'<div class="display punch{align}">{inner}</div>'


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
    # "sub" opcional: a virada de registro embaixo da aspa (itálico champagne).
    # Capa com aspa + comentário usa headline=aspa e sub=virada — nunca as duas
    # no mesmo bloco (a linha longa da virada desequilibra e encolhe a headline).
    sub = (f'<div class="hero-sub">{_inline(s["sub"])}</div>'
           if s.get("sub") else "")
    return (f'<div class="slide" style="background:{BG_HERO};">{photo}{scrim}'
            f'<div class="grain"></div>'
            f'<div class="bottom-wrap" style="bottom:88px;">{headline}{sub}'
            f'{_pill("RECONECTA")}</div></div>')


def slide_hero_b(s, base_dir):
    """Capa do POST B. Camadas na ordem do Figma: bordô -> foto full-bleed ->
    scrim (satura em 84%, a foto respira embaixo) -> ruído screen 32% ->
    headline + marca "/ ->". Sem masthead, sem pill, sem grain do padrão A."""
    img = _img_data(s.get("image"), base_dir)
    photo = f'<img class="photo" src="{img}">' if img else ""
    noise = (f'<div class="hb-noise" style="background-image:url('
             f'data:image/jpeg;base64,{_b64_file(NOISE_B)});"></div>'
             if os.path.exists(NOISE_B) else "")
    headline = f'<div class="hb-h">{_inline_hb(s["headline"])}</div>'
    mark = ('<div class="hb-mark"><span class="hb-slash">/</span>'
            '<span class="hb-arrow"></span></div>')
    return (f'<div class="slide" style="background:{BG_HERO};">{photo}'
            f'<div class="hb-scrim"></div>{noise}'
            f'<div class="hb-wrap">{headline}{mark}</div></div>')


def slide_hero_c(s, base_dir):
    """Capa do POST C (3º slot do dia). Camadas na ordem exata do Figma."""
    img = _img_data(s.get("image"), base_dir)
    photo = f'<img class="photo" src="{img}">' if img else ""
    iso = (f'<div class="hc-iso" style="background-image:url('
           f'data:image/jpeg;base64,{_b64_file(HC_ISO)});"></div>'
           if os.path.exists(HC_ISO) else "")
    half = (f'<div class="hc-half" style="background-image:url('
            f'data:image/jpeg;base64,{_b64_file(HC_HALFTONE)});"></div>'
            if os.path.exists(HC_HALFTONE) else "")
    headline = f'<div class="hc-h">{_inline_hc(s["headline"])}</div>'
    return (f'<div class="slide" style="background:{BG_HERO};">{photo}'
            f'<div class="hc-grad"></div>{iso}{half}'
            f'<div class="hc-wrap">{headline}</div></div>')


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


def _photo_card(s, base_dir):
    """Cartão retangular de foto (opcional) nos slides internos. Altura via
    "image_h" (default 420). Regra dura: NUNCA foto com texto embutido."""
    img = _img_data(s.get("image"), base_dir)
    if not img:
        return ""
    h = int(s.get("image_h", 420))
    return f'<div class="photo-card" style="height:{h}px"><img src="{img}"></div>'


def slide_text(s, base_dir):
    callout = (f'<div class="callout">{_inline(s["callout"])}</div>'
               if s.get("callout") else "")
    return (f'<div class="slide"><div class="grain"></div>{_mast()}'
            f'<div class="center-wrap">{_photo_card(s, base_dir)}'
            f'{_punch(s)}{_bodies(s)}{callout}</div></div>')


def slide_list(s, base_dir):
    items = ""
    for i, it in enumerate(s.get("items", []), 1):
        # tira numeração baked no título ("1. ", "2) ") — o engine já numera à esquerda
        title = re.sub(r'^\s*\d+[.)]\s+', '', it["title"])
        items += (f'<div class="item"><span class="num">{i}.</span>'
                  f'<div class="item-col">'
                  f'<div class="it-title">{_inline(title)}</div>'
                  f'<div class="it-body">{_inline(it["body"])}</div></div></div>')
    fecho = (f'<div class="fecho">{_inline(s["fecho"])}</div>'
             if s.get("fecho") else "")
    return (f'<div class="slide"><div class="grain"></div>{_mast()}'
            f'<div class="center-wrap">{_photo_card(s, base_dir)}{_punch(s)}'
            f'<div class="list-container">{items}</div>{fecho}</div></div>')


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


def _d_chrome(dmeta):
    """Chrome do design D (dossiê): REC + HUD na primeira linha, rodapé INVERTIDO
    pro topo logo abaixo (barcode + slug + contador) — ordem do Sávio, 27/ago.
    Injetado pelo build_html em TODO slide quando design == "d"."""
    dmeta = dmeta or {}
    week = dmeta.get("week") or ""
    hud = html.escape(dmeta.get("hud") or f"RECONECTA · SEM {week}".strip(" ·"))
    slug = html.escape(dmeta.get("slug") or "RECONECTA")
    idx, total = dmeta.get("idx"), dmeta.get("total")
    counter = (f'<div class="d-counter">{idx:02d} / {total:02d}</div>'
               if idx and total else "")
    bars = "".join(f'<i style="width:{w}px"></i>' for w in D_BARS)
    return (f'<div class="d-topscrim"></div>'
            f'<div class="d-rec"></div><div class="d-reclabel">REC</div>'
            f'<div class="d-hud">{hud}</div>'
            f'<div class="d-toprow"><div class="d-barcode">{bars}</div>'
            f'<div class="d-slug">{slug}</div>{counter}</div>')


def slide_hero_d(s, base_dir):
    """Capa do design D (dossiê INVERTIDO): foto full-bleed com scrim pesado
    embaixo, kicker + headline + sub ancorados no baixo com ~140px de respiro
    ("não literalmente colado no bottom"). O chrome vem do build_html. Casting:
    card de anúncio com texto embutido NUNCA vira fundo; a zona inferior da foto
    precisa aceitar o bloco de texto (regra do Sávio, 27/ago)."""
    img = _img_data(s.get("image"), base_dir)
    photo = f'<img class="photo" src="{img}">' if img else ""
    scrim = ('<div class="scrim" style="background:linear-gradient(180deg,'
             'rgba(12,11,11,.72) 0%,rgba(12,11,11,.28) 16%,rgba(12,11,11,0) 30%,'
             'rgba(12,11,11,.18) 46%,rgba(12,11,11,.66) 64%,'
             'rgba(12,11,11,.96) 100%);"></div>')
    kicker = (f'<div class="d-kicker">{_inline(s["kicker"])}</div>'
              if s.get("kicker") else "")
    lines = s["headline"].split("\n")
    inner = "".join(f'<span class="hl">{_inline(l)}</span>' for l in lines)
    headline = f'<div class="display hero-h d-h">{inner}</div>'
    sub = f'<div class="d-sub">{_inline(s["sub"])}</div>' if s.get("sub") else ""
    return (f'<div class="slide" style="background:{D_OBSIDIAN};">{photo}{scrim}'
            f'<div class="d-col">{kicker}{headline}{sub}</div></div>')


RENDERERS = {
    "hero": slide_hero, "hero_b": slide_hero_b, "hero_c": slide_hero_c,
    "hero_d": slide_hero_d,
    "photo": slide_photo,
    "text": slide_text, "list": slide_list, "proof": slide_proof, "cta": slide_cta,
}


def _skin_css(skin):
    """Skin dos slides INTERNOS por design do post. skin 'c': punch em Subdays
    (caixa normal — a copy C é escrita em caixa de frase), ênfase {vermelho} vira
    SUBLINHADO creme (o C não usa vermelho), grain A vira ISO screen 32%."""
    if skin == "d":
        # design D "dossiê" (substitui o B, 27/ago): Obsidian + Pearl/Gold,
        # TT Modernoir no display, Space Mono no chrome; ênfase «»/{} vira DOURADO
        # (vermelho é SÓ o ponto REC); sem grain, sem pill (o slug faz o papel).
        return (
            f".slide{{background:{D_OBSIDIAN} !important;}}"
            # o chrome do D desce até ~y168 (toprow); a faixa de centralização
            # dos internos precisa começar abaixo dele (caso slide 3, 27/ago:
            # cartão de 520px encostou no barcode)
            f".center-wrap{{padding-top:215px;padding-bottom:150px;"
            f"box-sizing:border-box;}}"
            f".display{{font-family:'TTModernoir';letter-spacing:0;}}"
            f".grain{{display:none;}}"
            f".pill{{display:none;}}"
            f".mast{{display:none;}}"  # o HUD do dossiê ocupa o topo-direita
            f".punch{{color:{D_PEARL};}}"
            f".champ{{color:{D_GOLD};font-style:normal;}}"
            f".red{{color:{D_GOLD};}}"
            f".item .num{{color:{D_GOLD};}}"
            f".callout{{border-color:{D_GOLD};}}"
            # véu no topo pra segurar o chrome sobre foto clara (caso slide 2
            # Sallve 27/ago: HUD dourado sumia no fundo creme)
            f".d-topscrim{{position:absolute;left:0;right:0;top:0;height:300px;"
            f"background:linear-gradient(180deg,rgba(12,11,11,.68) 0%,"
            f"rgba(12,11,11,.38) 55%,rgba(12,11,11,0) 100%);z-index:4;}}"
            f".d-rec{{position:absolute;left:64px;top:64px;width:11px;height:11px;"
            f"border-radius:50%;background:{D_SCARLET};z-index:5;}}"
            f".d-reclabel{{position:absolute;left:84px;top:58px;font-family:'SpaceMono';"
            f"font-size:20px;letter-spacing:.16em;color:rgba(238,217,189,.8);z-index:5;}}"
            f".d-hud{{position:absolute;right:64px;top:58px;font-family:'SpaceMono';"
            f"font-size:18px;letter-spacing:.18em;color:rgba(238,206,102,.65);"
            f"text-transform:uppercase;z-index:5;}}"
            f".d-toprow{{position:absolute;left:64px;right:64px;top:130px;display:flex;"
            f"align-items:flex-end;z-index:5;}}"
            f".d-barcode{{display:flex;align-items:flex-end;gap:4px;height:34px;}}"
            f".d-barcode i{{display:block;background:{D_PEARL};height:34px;}}"
            f".d-slug{{margin-left:26px;font-family:'SpaceMono';font-size:18px;"
            f"letter-spacing:.14em;color:rgba(238,217,189,.62);text-transform:uppercase;"
            f"padding-bottom:6px;}}"
            f".d-counter{{margin-left:auto;font-family:'SpaceMono';font-size:18px;"
            f"letter-spacing:.18em;color:rgba(238,206,102,.65);padding-bottom:6px;}}"
            f".d-col{{position:absolute;left:64px;bottom:140px;width:952px;z-index:4;}}"
            f".d-col .hero-h{{text-align:left;font-size:96px;color:{D_PEARL};}}"
            f".d-kicker{{font-family:'SpaceMono';font-size:22px;letter-spacing:.22em;"
            f"color:{D_GOLD};text-transform:uppercase;margin-bottom:22px;}}"
            f".d-sub{{font-family:'Inter';font-weight:500;font-size:33px;line-height:1.32;"
            f"color:rgba(238,217,189,.9);margin-top:30px;max-width:860px;}}"
        )
    if skin != "c":
        return ""
    iso = (f"url(data:image/jpeg;base64,{_b64_file(HC_ISO)})"
           if os.path.exists(HC_ISO) else "none")
    return (
        f".display{{font-family:'SubdaysTight';text-transform:none;"
        f"letter-spacing:.02em;}}"
        # títulos dos slides internos levemente maiores no C (Sávio, 25/ago:
        # SubdaysTight a 60px ficava ilegível); a headline da capa (hero_c) não
        # passa por .punch e segue nos 114px dela.
        f".punch{{font-size:68px;}}"
        f".red{{color:{CREAM};text-decoration:underline;"
        f"text-decoration-thickness:5px;text-underline-offset:12px;}}"
        f".grain{{background-image:{iso};mix-blend-mode:screen;opacity:.32;"
        f"background-size:1080px 1350px;}}"
        f".item .num{{color:{CHAMPAGNE};}}"
        f".callout{{border-color:{CHAMPAGNE};}}"
    )


def build_html(slide, base_dir, skin=None, dmeta=None):
    fn = RENDERERS[slide["type"]]
    body = fn(slide, base_dir)
    if skin == "d" and body.endswith("</div>"):
        # chrome do dossiê em TODO slide (REC + HUD + rodapé invertido no topo)
        body = body[:-len("</div>")] + _d_chrome(dmeta) + "</div>"
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>'
            f'{_fonts_css()}{_base_css()}{_skin_css(skin)}</style></head>'
            f'<body>{body}</body></html>')


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
# Régua de largura: as heroes canônicas (SEM29 campeãs) SANGRAM além da margem de
# 93px — travar nos 894px úteis encolhe a capa vs o benchmark (feedback do Sávio,
# 20/jul). A linha pode ir até HERO_LINE_MAX_W (respiro de ~44px de cada borda do
# canvas); o texto segue centrado, só sangra simétrico sobre a margem.
HERO_FIT_FLOOR = 60
HERO_LINE_MAX_W = 992
# guarda das linhas do punch: linha art-directed que não cabe no container NÃO
# encolhe a fonte (hierarquia tipográfica é fixa) — o render acusa e a linha é
# requebrada na copy. Sem isso o browser quebrava sozinho e derrubava palavra
# órfã em silêncio (caso "PERDER", AD005 SEM30, 21/jul).
_PUNCH_CHECK_JS = """() => {
  const punch = document.querySelector('.punch');
  if (!punch) return null;
  const lines = [...punch.querySelectorAll('.pl')];
  if (!lines.length) return null;
  const maxW = punch.getBoundingClientRect().width;
  const bad = [];
  lines.forEach(l => {
    const r = document.createRange();
    r.selectNodeContents(l);
    const w = r.getBoundingClientRect().width;
    if (w > maxW + 1) bad.push({text: l.textContent, w: Math.round(w), max: Math.round(maxW)});
  });
  return bad.length ? bad : null;
}"""

# guardas da CAPA B: aqui a quebra é NATURAL por design (caixa de 894px, como no
# Figma) — então não há fit de fonte (68px é constante do design). O que se vigia:
#   órfã   -> última linha com 1 palavra (feio em headline de notícia; REQUEBRAR
#             a copy ou editar — mesma doutrina do caso "PERDER" do punch)
#   linhas -> mais de 5 linhas = headline longa demais pra capa
#   larga  -> palavra única maior que a caixa (não quebra, estoura em silêncio)
_HERO_B_CHECK_JS = """() => {
  const h = document.querySelector('.hb-h') || document.querySelector('.hc-h');
  if (!h) return null;
  const ws = [...h.querySelectorAll('.w')];
  if (!ws.length) return null;
  const linhas = [];
  ws.forEach(w => {
    const r = w.getBoundingClientRect();
    const key = Math.round(r.top);
    let l = linhas.find(x => Math.abs(x.top - key) < 4);
    if (!l) { l = {top: key, words: [], right: r.right, left: r.left}; linhas.push(l); }
    l.words.push(w.textContent);
    l.right = Math.max(l.right, r.right);
    l.left = Math.min(l.left, r.left);
  });
  linhas.sort((a, b) => a.top - b.top);
  const maxW = h.getBoundingClientRect().width;
  const larga = linhas.filter(l => (l.right - l.left) > maxW + 1)
                      .map(l => l.words.join(' '));
  const ultima = linhas[linhas.length - 1];
  return {
    linhas: linhas.length,
    orfa: ultima.words.length === 1 ? ultima.words[0] : null,
    larga: larga.length ? larga : null,
  };
}"""

_HERO_FIT_JS = """() => {
  const h = document.querySelector('.hero-h');
  if (!h) return null;
  const lines = [...h.querySelectorAll('.hl')];
  if (!lines.length) return null;
  const MAXW = %d;
  const textW = (l) => {
    const r = document.createRange();
    r.selectNodeContents(l);
    return r.getBoundingClientRect().width;
  };
  const fits = () => lines.every(l => textW(l) <= MAXW + 1);
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
}""" % (HERO_LINE_MAX_W, HERO_FIT_FLOOR)


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
        skin = data.get("design")
        dmeta = {"hud": data.get("hud"), "slug": data.get("slug"),
                 "week": data.get("week"), "total": len(slides)}
        for idx, s in enumerate(slides, 1):
            dmeta["idx"] = idx
            page.set_content(build_html(s, base_dir, skin, dmeta),
                             wait_until="networkidle")
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
            # capa B: órfã / linhas demais / palavra larga = overflow (editar copy)
            hb = page.evaluate(_HERO_B_CHECK_JS)
            if hb:
                probs = []
                if hb.get("orfa"):
                    probs.append(f'órfã "{hb["orfa"]}" sozinha na última linha')
                if hb["linhas"] > 5:
                    probs.append(f'{hb["linhas"]} linhas (máx 5 na capa B)')
                if hb.get("larga"):
                    probs.append(f'linha estoura a caixa: {hb["larga"]}')
                if probs:
                    overflows.append({"slide": idx, "type": "hero_b", "problemas": probs})
                    for pr in probs:
                        print(f"⚠ CAPA-B slide_{idx}: {pr} — EDITAR a headline "
                              f"(trocar palavra/ordem; a fonte não encolhe).")
                else:
                    print(f"  capa B ok: {hb['linhas']} linha(s), sem órfã")
            # punch: linha art-directed que não cabe = overflow (requebrar copy)
            pbad = page.evaluate(_PUNCH_CHECK_JS)
            if pbad:
                overflows.append({"slide": idx, "type": "punch_line", "lines": pbad})
                for b in pbad:
                    print(f"⚠ PUNCH slide_{idx}: linha \"{b['text']}\" tem {b['w']}px "
                          f"e o container {b['max']}px — REQUEBRAR a linha (nunca "
                          f"deixar o browser quebrar sozinho).")
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
