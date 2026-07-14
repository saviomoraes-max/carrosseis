"""
RECONECTA editorial carousel v3 — sistema visual extraído do Figma master v3.

Especificação completa em ../primitivas_v3.json (v3.0).
Figma master v3: https://www.figma.com/design/fuIFq4fA94kKjvf2A7vhXo (AD001 "Como fazer depoimento", 7 frames)

O QUE MUDOU DO v2 PRO v3
- Fundo: bordô profundo #2d0000 com grão (era multi-fundo cream/dark).
- Headline: Alga champagne #f2ddb6 (mantém a família, virou o único display).
- CORPO: agora é Grift (era Inter). Inter ficou só no footer e no @handle.
- Capa: masthead central "powered by RECONECTA" (Instrument Serif itálico + Grift Black).
- Demais slides: label "RECONECTA" no canto superior direito (Grift).
- Componentes novos recorrentes: caixa de callout (fill #1d0f09 + borda 1px #ff0000,
  raio 21) e footer pill "ARRASTE PARA O LADO" com sparkle + seta.
- Margens laterais 93px; footer pill a 93px da base; corpo Grift 35px / lh 1.25.

Uso típico em build.py:

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent / "_template"))
    from reconecta_carousel_v3 import *

    BASE = Path(__file__).parent
    IMG = BASE / "img"

    s1 = slide_hero(
        image=image_uri(IMG / "hero.jpg"),
        headline="Quando for postar um antes/depois, faça isso",
        handle="@oleonardorosso",
    )
    s2 = slide_photo(
        image=image_uri(IMG / "s2.jpg"),
        headline="Apresente a paciente",
        body="diga a idade e as queixas reais dela, usando as palavras exatas que ela usou no consultório.",
    )
    s3 = slide_photo(
        image=image_uri(IMG / "s3.jpg"),
        headline="Enquanto você narra as dores da paciente",
        body="vá **marcando visualmente no vídeo** as áreas do rosto que precisavam ser trabalhadas.",
        callout="**Mantenha a simplicidade**: Esqueça termos técnicos ou roteiros mega elaborados. Foque na queixa e no plano.",
    )
    s4 = slide_text(
        headline="Apresente a solução",
        body="através do seu método exclusivo (ex: Método ELEV ou Beauty Review).",
        callout="Mostre **apenas o DEPOIS** primeiro (para chocar e fixar o ápice da transformação).",
        note="Em seguida, mostre o Antes e Depois lado a lado para a comparação final.",
    )
    s7 = slide_cta(
        headline="Quer ver exemplos reais desse vídeo na prática?",
        body="Comenta CASO que eu te envio agora mesmo por Direct.",
        cta="COMENTA CASO",
    )

    html = render_carousel([s1, s2, s3, s4, ...], caption="...")
    Path("carousel.html").write_text(html, encoding="utf-8")

Mapeamento primitiva ↔ Figma (AD001):
- slide_hero  : Frame 1 (foto full-bleed + perfil@ + headline)
- slide_photo : Frames 2, 3, 5 (foto + headline + corpo [+ callout])
- slide_text  : Frames 4, 6 (só texto: headline + corpo [+ callout] [+ nota itálica])
- slide_cta   : Frame 7 (só texto + pill compacta de CTA)
"""
import base64
import re
from pathlib import Path

# ============================================================
# PALETA (Figma master v3 — 2026-06-02)
# ============================================================
BG_DARK = "#340909"          # bordô canônico (fundo de todo slide) — tom quente como renderiza no Figma (a fill #2d0000 + grão sobe pra ~#340909)
HERO_FADE = "#1a0001"        # cor do fade da capa (mais escuro que o bordô)
HEADLINE = "#f2ddb6"         # champagne — TODA headline Alga e notas itálicas
BODY = "#ececec"             # off-white — corpo Grift e texto de callout
LIGHT = "#f5f5f5"            # footer, @handle, bordas, sparkle, seta
CALLOUT_BG = "#1d0f09"       # fill da caixa de callout (marrom muito escuro)
CALLOUT_BORDER = "#ff0000"   # borda fina (1px) vermelha da caixa
FOOTER_BG = "rgba(4,4,22,0.05)"
FOOTER_BORDER = "#f5f5f5"
LABEL = "#ececec"            # label "RECONECTA" no topo

# ============================================================
# GEOMETRIA — coords em "output px" (1080x1350). Render em 420x525.
# S = 1080/420 ≈ 2.5714
# ============================================================
S = 2.5714
W, H = 1080, 1350
MARGIN = 93                  # margem lateral (texto começa em x=93)
CONTENT_W = W - 2 * MARGIN   # 894
FOOTER_TOP = 1199            # topo do footer pill
FOOTER_H = 58                # altura do footer pill
GAP = 24                     # gap padrão entre headline/corpo/callout
PHOTO_CONTENT_BOTTOM = 1175  # base do bloco de conteúdo em slide com foto (24px acima do footer)


def px(output_px: float) -> str:
    """Converte px do output (1080-coord) pra CSS px do viewport (420-coord)."""
    return f"{round(output_px / S, 3)}px"


# ============================================================
# TIPOGRAFIA — sizes em output px
# ============================================================
SZ_HEAD = 88                 # headline default (Alga)
SZ_HEAD_HERO = 95            # headline da capa
SZ_BODY = 35                 # corpo (Grift), lh 1.25
SZ_LABEL = 18.6              # "RECONECTA" topo (Grift)
SZ_MASTHEAD = 28             # "powered by RECONECTA"
SZ_HANDLE = 28               # @handle (Inter)
SZ_FOOTER = 18               # texto do footer (Inter)
LH_BODY = 1.25
LH_HEAD = 1.1                # leading da headline (Figma ~0.97–1.18; 1.1 é o equilíbrio)


# ============================================================
# DATA URI helpers (fontes + imagens)
# ============================================================
def data_uri(path, mime: str) -> str:
    p = Path(path)
    b64 = base64.b64encode(p.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"


def image_uri(path) -> str:
    p = Path(path)
    ext = p.suffix.lower().lstrip(".")
    mime_map = {
        "jpg": "image/jpeg", "jpeg": "image/jpeg",
        "png": "image/png", "webp": "image/webp",
        "svg": "image/svg+xml", "gif": "image/gif",
    }
    return data_uri(p, mime_map.get(ext, "image/png"))


def _font_face(family, weight, style, font_dir, filename):
    p = font_dir / filename
    ext = filename.split(".")[-1].lower()
    mime = "font/otf" if ext == "otf" else "font/ttf"
    fmt = "opentype" if ext == "otf" else "truetype"
    uri = data_uri(p, mime)
    return (
        f"@font-face{{font-family:'{family}';font-weight:{weight};"
        f"font-style:{style};src:url({uri}) format('{fmt}');}}"
    )


def load_fonts(font_dir=None) -> str:
    """Embute as fontes do v3 como @font-face.

    Grift só tem Regular(400)+Italic e Black(900). Pesos 500/600/700 do corpo
    são sintetizados pelo Chromium (font-synthesis) — por isso o Black ganha a
    família 'GriftBlack' própria, pra o 700 inline NÃO saltar pro 900.
    """
    if font_dir is None:
        font_dir = Path(__file__).parent / "fonts"
    font_dir = Path(font_dir)
    return "".join([
        _font_face("Alga", 600, "normal", font_dir, "Alga-SemiBold.otf"),
        _font_face("Alga", 700, "normal", font_dir, "Alga-SemiBold.otf"),
        _font_face("Grift", 400, "normal", font_dir, "Grift-Regular.ttf"),
        _font_face("Grift", 400, "italic", font_dir, "Grift-Italic.ttf"),
        _font_face("GriftBlack", 900, "normal", font_dir, "Grift-Black.ttf"),
        _font_face("GriftBlack", 900, "italic", font_dir, "Grift-BlackItalic.ttf"),
        _font_face("Inter", 500, "normal", font_dir, "Inter-Medium.ttf"),
        _font_face("Inter", 700, "normal", font_dir, "Inter-Bold.ttf"),
        _font_face("Instrument Serif", 400, "italic", font_dir, "InstrumentSerif-Italic.ttf"),
    ])


# default assets do template (avatar + selo verificado + grão)
_TPL = Path(__file__).parent
DEFAULT_AVATAR = _TPL / "default_avatar.png"
VERIFIED_BADGE = _TPL / "verified_badge.png"
GRAIN = _TPL / "grain.png"


# ============================================================
# RICH TEXT — converte **negrito** em <b> (Grift 700 sintético)
# ============================================================
def _rich(text: str) -> str:
    parts = re.split(r"\*\*(.+?)\*\*", text)
    out = []
    for i, seg in enumerate(parts):
        if i % 2 == 1:
            out.append(f'<b style="font-weight:700;">{seg}</b>')
        else:
            out.append(seg)
    return "".join(out)


# ============================================================
# SVGs — sparkle (esquerda do pill) e seta (direita)
# ============================================================
def _sparkle(size=24, color=LIGHT):
    s = px(size)
    return (
        f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" '
        f'style="flex:0 0 auto;">'
        f'<path d="M12 0 C12.8 6.4 17.6 11.2 24 12 C17.6 12.8 12.8 17.6 12 24 '
        f'C11.2 17.6 6.4 12.8 0 12 C6.4 11.2 11.2 6.4 12 0 Z" fill="{color}"/></svg>'
    )


def _arrow(color=LIGHT):
    w = px(26)
    h = px(16)
    return (
        f'<svg width="{w}" height="{h}" viewBox="0 0 26 16" fill="none" '
        f'style="flex:0 0 auto;">'
        f'<path d="M1 8 H24 M17 1 L24 8 L17 15" stroke="{color}" stroke-width="1.6" '
        f'stroke-linecap="round" stroke-linejoin="round"/></svg>'
    )


def _verified(size=33):
    """Selo verificado azul (SVG limpo, sem branding de terceiros)."""
    s = px(size)
    return (
        f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" '
        f'style="margin-left:{px(8)};flex:0 0 auto;">'
        f'<path fill="#1d9bf0" d="M22.25 12c0-1.43-.88-2.67-2.19-3.34.46-1.39.2-2.9-.81-3.91'
        f's-2.52-1.27-3.91-.81c-.66-1.31-1.91-2.19-3.34-2.19s-2.67.88-3.33 2.19c-1.4-.46-2.91-.2-3.92.81'
        f's-1.26 2.52-.8 3.91c-1.31.67-2.2 1.91-2.2 3.34s.89 2.67 2.2 3.34c-.46 1.39-.21 2.9.8 3.91'
        f's2.52 1.26 3.91.81c.67 1.31 1.91 2.19 3.34 2.19s2.68-.88 3.34-2.19c1.39.45 2.9.2 3.91-.81'
        f's1.27-2.52.81-3.91c1.31-.67 2.19-1.91 2.19-3.34z"/>'
        f'<path fill="#fff" d="M10.6 15.4l-3-3 1.2-1.2 1.8 1.8 4-4 1.2 1.2z"/></svg>'
    )


# ============================================================
# COMPONENTES COMPARTILHADOS
# ============================================================
def _hex_rgba(hexv, a):
    h = hexv.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{a})"


def _grain():
    """Camada de grão sobre todo o slide. grain.png é ruído quase branco; 'soft-light'
    clareia/aquece o bordô uniformemente (inclusive nas áreas escuras) sem estourar."""
    uri = image_uri(GRAIN)
    return (
        f'<div style="position:absolute;inset:0;background-image:url({uri});'
        f'background-size:cover;opacity:0.35;mix-blend-mode:soft-light;'
        f'pointer-events:none;z-index:4;"></div>'
    )


def _top_label():
    """Label 'RECONECTA' no canto superior direito (Grift 600)."""
    return (
        f'<div style="position:absolute;top:{px(71)};right:{px(MARGIN)};'
        f"font-family:'Grift';font-weight:600;font-size:{px(SZ_LABEL)};"
        f'letter-spacing:{px(0.19)};color:{LABEL};z-index:5;">RECONECTA</div>'
    )


def _masthead():
    """'powered by RECONECTA' centralizado no topo (capa)."""
    return (
        f'<div style="position:absolute;top:{px(93)};left:0;right:0;text-align:center;'
        f'z-index:5;color:{HEADLINE};font-size:{px(SZ_MASTHEAD)};line-height:1;">'
        f"<span style=\"font-family:'Instrument Serif';font-style:italic;font-weight:400;\">powered by </span>"
        f"<span style=\"font-family:'GriftBlack';font-weight:900;\">RECONECTA</span></div>"
    )


def _footer(label="ARRASTE PARA O LADO"):
    """Footer pill full-width: [sparkle ............ LABEL / →]."""
    txt = (
        f"<span style=\"font-family:'Inter';font-weight:700;font-size:{px(SZ_FOOTER)};"
        f'letter-spacing:{px(2.52)};color:{LIGHT};">{label}</span>'
    )
    sep = (
        f"<span style=\"font-family:'Inter';font-weight:700;font-size:{px(SZ_FOOTER)};"
        f'color:{LIGHT};margin:0 {px(14)};">/</span>'
    )
    return (
        f'<div style="position:absolute;left:{px(MARGIN)};width:{px(CONTENT_W)};'
        f'top:{px(FOOTER_TOP)};height:{px(FOOTER_H)};border-radius:{px(FOOTER_H/2)};'
        f'background:{FOOTER_BG};border:{px(1)} solid {FOOTER_BORDER};'
        f'display:flex;align-items:center;justify-content:flex-end;'
        f'padding:0 {px(25)};z-index:5;box-sizing:border-box;">'
        f'<div style="display:flex;align-items:center;">{txt}{sep}{_arrow()}</div>'
        f"</div>"
    )


def _cta_pill(label="COMENTA CASO"):
    """Pill compacta de CTA (slide final): [sparkle LABEL /]."""
    txt = (
        f"<span style=\"font-family:'Inter';font-weight:700;font-size:{px(SZ_FOOTER)};"
        f'letter-spacing:{px(2.52)};color:{LIGHT};margin:0 {px(12)};">{label}</span>'
    )
    sep = (
        f"<span style=\"font-family:'Inter';font-weight:700;font-size:{px(SZ_FOOTER)};"
        f'color:{LIGHT};">/</span>'
    )
    return (
        f'<div style="display:inline-flex;align-items:center;'
        f'height:{px(54)};border-radius:{px(27)};background:{FOOTER_BG};'
        f'border:{px(1)} solid {FOOTER_BORDER};padding:0 {px(26)};box-sizing:border-box;">'
        f'{txt}{sep}</div>'
    )


def _callout(text: str):
    """Caixa de callout: fill escuro + borda 1px vermelha, raio 21, padding 40/55."""
    return (
        f'<div style="width:{px(CONTENT_W)};background:{CALLOUT_BG};'
        f'border:{px(1)} solid {CALLOUT_BORDER};border-radius:{px(21)};'
        f'padding:{px(36)} {px(55)};box-sizing:border-box;">'
        f"<p style=\"font-family:'Grift';font-weight:500;font-size:{px(SZ_BODY)};"
        f'line-height:{LH_BODY};color:{BODY};margin:0;">{_rich(text)}</p></div>'
    )


def _headline(text: str, size: float, lh: float = LH_HEAD, ls: float = 0):
    # white-space:pre-wrap honra quebras manuais (\n) como no Figma e ainda wrappa o resto
    return (
        f"<p style=\"font-family:'Alga';font-weight:700;font-size:{px(size)};"
        f'line-height:{lh};letter-spacing:{px(ls)};color:{HEADLINE};margin:0;'
        f'width:{px(CONTENT_W)};white-space:pre-wrap;\">{text}</p>'
    )


def _body(text: str, weight=400, color=BODY, size=SZ_BODY):
    return (
        f"<p style=\"font-family:'Grift';font-weight:{weight};font-size:{px(size)};"
        f'line-height:{LH_BODY};color:{color};margin:0;width:{px(CONTENT_W)};'
        f'white-space:pre-wrap;">{_rich(text)}</p>'
    )


def _note(text: str):
    """Nota itálica champagne (ex.: slide 4)."""
    return (
        f"<p style=\"font-family:'Grift';font-weight:400;font-style:italic;"
        f'font-size:{px(SZ_BODY)};line-height:{LH_BODY};color:{HEADLINE};margin:0;'
        f'width:{px(CONTENT_W)};white-space:pre-wrap;">{_rich(text)}</p>'
    )


# Rampas de fade SUAVES (multi-stop) — sem linha dura. (pct, alpha) de cima pra baixo.
PHOTO_STOPS = [(0, 0), (30, 0), (44, 0.18), (54, 0.48), (64, 0.78), (74, 0.94), (86, 1)]
HERO_STOPS = [(0, 0), (32, 0), (47, 0.20), (58, 0.55), (68, 0.84), (78, 0.96), (88, 1)]


def _fade_css(color, stops):
    parts = ", ".join(f"{_hex_rgba(color, a)} {p}%" for p, a in stops)
    return f"linear-gradient(180deg, {parts})"


def _photo_layer(image: str, *, fade_color=BG_DARK, focal="50% 35%", zoom=1.0, stops=None):
    """Foto full-bleed + gradiente SUAVE pra base.
    `focal` = object-position (crop fino, dentro da folga do cover).
    `zoom` = escala com âncora na BASE: sobe o conteúdo e fecha o crop no rosto.
             zoom=1.5 ≈ subir ~50% (a folga do cover é pequena, ~7%; só o zoom sobe de verdade)."""
    if stops is None:
        stops = PHOTO_STOPS
    return (
        f'<img src="{image}" style="position:absolute;inset:0;width:100%;height:100%;'
        f'object-fit:cover;object-position:{focal};transform:scale({zoom});'
        f'transform-origin:50% 100%;z-index:1;">'
        f'<div style="position:absolute;inset:0;z-index:2;background:{_fade_css(fade_color, stops)};"></div>'
    )


def _slide(inner: str, bg=BG_DARK):
    return f'<div class="slide" style="background:{bg};">{inner}</div>'


def _stack_bottom(items, bottom=PHOTO_CONTENT_BOTTOM, gap=GAP):
    """Bloco de conteúdo ancorado pela base (cresce pra cima)."""
    body = "".join(items)
    return (
        f'<div style="position:absolute;left:{px(MARGIN)};width:{px(CONTENT_W)};'
        f'bottom:{px(H - bottom)};display:flex;flex-direction:column;'
        f'align-items:flex-start;gap:{px(gap)};z-index:5;">{body}</div>'
    )


def _stack_center(items, center_y=660, gap=GAP):
    """Bloco de conteúdo centralizado na vertical (slides só-texto), levemente acima do meio."""
    body = "".join(items)
    return (
        f'<div style="position:absolute;left:{px(MARGIN)};width:{px(CONTENT_W)};'
        f'top:{px(center_y)};transform:translateY(-50%);display:flex;flex-direction:column;'
        f'align-items:flex-start;gap:{px(gap)};z-index:5;">{body}</div>'
    )


def _stack_top(items, top_y, gap=GAP):
    """Bloco ancorado pelo topo (slide de CTA fica no terço superior)."""
    body = "".join(items)
    return (
        f'<div style="position:absolute;left:{px(MARGIN)};width:{px(CONTENT_W)};'
        f'top:{px(top_y)};display:flex;flex-direction:column;'
        f'align-items:flex-start;gap:{px(gap)};z-index:5;">{body}</div>'
    )


# ============================================================
# SLIDES PÚBLICOS
# ============================================================
def slide_hero(image, headline, *, handle="@oleonardorosso", avatar=None,
               verified=True, headline_size=SZ_HEAD_HERO, focal="50% 30%",
               lh_head=0.97, ls_head=-5.7):
    """Capa: foto full-bleed, masthead central, linha de perfil + headline embaixo.
    `lh_head`/`ls_head`: o default é tracking fechado pra frase curta; afrouxe (ex. lh=1.05, ls=-1.5)
    quando a headline for longa."""
    av = avatar or image_uri(DEFAULT_AVATAR)
    badge = _verified() if verified else ""
    identity = (
        f'<div style="display:flex;align-items:center;gap:{px(16)};">'
        f'<img src="{av}" style="width:{px(57)};height:{px(57)};border-radius:50%;'
        f'object-fit:cover;">'
        f"<span style=\"font-family:'Inter';font-weight:500;font-size:{px(SZ_HANDLE)};"
        f'letter-spacing:{px(-1.68)};color:{LIGHT};">{handle}</span>{badge}</div>'
    )
    head = _headline(headline, headline_size, lh=lh_head, ls=ls_head)
    block = (
        f'<div style="position:absolute;left:{px(MARGIN)};width:{px(CONTENT_W)};'
        f'bottom:{px(H - 1165)};display:flex;flex-direction:column;'
        f'align-items:flex-start;gap:{px(30)};z-index:5;">{identity}{head}</div>'
    )
    inner = (
        _photo_layer(image, fade_color=HERO_FADE, focal=focal, stops=HERO_STOPS)
        + _grain() + _masthead() + block + _footer()
    )
    return _slide(inner)


def slide_photo(image, headline, body, *, callout=None, focal="50% 32%", zoom=1.0,
                headline_size=SZ_HEAD, lh_head=LH_HEAD, body_weight=400, body_size=SZ_BODY):
    """Foto full-bleed + headline + corpo (+ callout opcional). Conteúdo na base.
    `focal` = object-position (crop fino). `zoom` = sobe/fecha o crop no rosto (âncora base)
    em slides com muito texto pra o rosto não ser tampado (ex. zoom=1.5 sobe ~50%)."""
    items = [_headline(headline, headline_size, lh=lh_head), _body(body, weight=body_weight, size=body_size)]
    if callout:
        items.append(_callout(callout))
    # com callout o bloco encosta no footer (y≈1175); sem callout fica mais alto (y≈1110)
    bottom = 1175 if callout else 1110
    inner = (
        _photo_layer(image, focal=focal, zoom=zoom)
        + _grain() + _top_label() + _stack_bottom(items, bottom=bottom) + _footer()
    )
    return _slide(inner)


def slide_text(headline, body, *, callout=None, note=None,
               headline_size=SZ_HEAD, lh_head=LH_HEAD, body_weight=400,
               body_size=SZ_BODY, center_y=660):
    """Só texto sobre bordô: headline + corpo (+ callout) (+ nota itálica). Centralizado.
    `body_size` < 35 pra copy densa que não cabe."""
    items = [_headline(headline, headline_size, lh=lh_head), _body(body, weight=body_weight, size=body_size)]
    if callout:
        items.append(_callout(callout))
    if note:
        items.append(_note(note))
    inner = _grain() + _top_label() + _stack_center(items, center_y=center_y) + _footer()
    return _slide(inner)


def slide_proof(headline, images, *, headline_size=58, lh_head=1.08, center_y=690):
    """Prova social: headline champagne + N screenshots de depoimento empilhados como cards."""
    cards = "".join(
        f'<img src="{im}" style="width:100%;display:block;border-radius:{px(16)};'
        f'border:{px(1)} solid rgba(245,245,245,0.12);box-shadow:0 {px(8)} {px(24)} rgba(0,0,0,0.28);">'
        for im in images
    )
    block = (
        f'<div style="position:absolute;left:{px(MARGIN)};width:{px(CONTENT_W)};'
        f'top:{px(center_y)};transform:translateY(-50%);display:flex;flex-direction:column;'
        f'align-items:flex-start;gap:{px(28)};z-index:5;">'
        f'{_headline(headline, headline_size, lh=lh_head)}'
        f'<div style="display:flex;flex-direction:column;gap:{px(18)};width:100%;">{cards}</div>'
        f'</div>'
    )
    inner = _grain() + _top_label() + block + _footer()
    return _slide(inner)


def slide_cta(headline, body, *, cta="COMENTA CASO",
              headline_size=SZ_HEAD, lh_head=LH_HEAD):
    """Slide final: headline + corpo + pill compacta de CTA. Centralizado, sem footer full."""
    items = [
        _headline(headline, headline_size, lh=lh_head),
        _body(body),
        f'<div style="margin-top:{px(8)};">{_cta_pill(cta)}</div>',
    ]
    # CTA fica no terço superior (como no Figma), não centralizado
    inner = _grain() + _top_label() + _stack_top(items, top_y=336)
    return _slide(inner)


# ============================================================
# WRAPPER — IG frame + swipe (idêntico ao v2; export.py compatível)
# ============================================================
def render_carousel(slides: list, *, handle="oleonardorosso",
                    subtitle="Patrocinado", caption="", font_faces=None,
                    title="Carrossel RECONECTA v3") -> str:
    if font_faces is None:
        font_faces = load_fonts()
    total = len(slides)
    dots = "".join(
        f'<span class="dot{" active" if i == 0 else ""}"></span>' for i in range(total)
    )
    slides_html = "".join(slides)
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
  {font_faces}
  *{{margin:0;padding:0;box-sizing:border-box}}
  html,body{{background:{BG_DARK};min-height:100vh;display:flex;align-items:center;justify-content:center;padding:40px 20px;font-family:'Grift',sans-serif;color:{BODY}}}
  .ig-frame{{width:420px;max-width:420px;background:#fff;border-radius:12px;box-shadow:0 24px 60px rgba(0,0,0,0.12);overflow:hidden}}
  .ig-header{{display:flex;align-items:center;justify-content:space-between;padding:12px 14px;border-bottom:1px solid #EFEFEF}}
  .ig-user{{display:flex;align-items:center;gap:10px}}
  .ig-avatar{{width:34px;height:34px;border-radius:50%;background:{BG_DARK};display:flex;align-items:center;justify-content:center;color:{LIGHT};font-family:'GriftBlack';font-weight:900;font-size:16px;border:2px solid #fff;box-shadow:0 0 0 2px {BG_DARK}}}
  .ig-handle{{font-size:13px;font-weight:700;color:#262626;font-family:'Inter'}}
  .ig-sub{{font-size:11px;color:#8E8E8E;font-family:'Inter'}}
  .ig-more{{font-size:18px;color:#262626;letter-spacing:1px}}
  .carousel-viewport{{position:relative;width:420px;aspect-ratio:4/5;overflow:hidden;cursor:grab;user-select:none}}
  .carousel-viewport:active{{cursor:grabbing}}
  .carousel-track{{display:flex;width:100%;height:100%;transition:transform 350ms cubic-bezier(0.22,1,0.36,1);will-change:transform}}
  .slide{{flex:0 0 420px;width:420px;height:100%;position:relative;overflow:hidden}}
  .ig-dots{{display:flex;justify-content:center;gap:4px;padding:10px 0 4px;background:#fff}}
  .ig-dots .dot{{width:5px;height:5px;border-radius:50%;background:#C7C7C7}}
  .ig-dots .dot.active{{background:{BG_DARK}}}
  .ig-actions{{display:flex;align-items:center;gap:14px;padding:6px 14px 2px;background:#fff}}
  .ig-actions .spacer{{flex:1}}
  .ig-actions svg{{color:#262626}}
  .ig-caption{{padding:4px 14px 12px;font-size:12px;line-height:1.4;color:#262626;background:#fff;font-family:'Inter'}}
  .ig-caption .handle{{font-weight:700}}
  .ig-caption .ts{{display:block;color:#8E8E8E;font-size:10px;text-transform:uppercase;letter-spacing:0.3px;margin-top:4px}}
</style>
</head>
<body>
<div class="ig-frame">
  <div class="ig-header">
    <div class="ig-user">
      <div class="ig-avatar">R</div>
      <div>
        <div class="ig-handle">{handle}</div>
        <div class="ig-sub">{subtitle}</div>
      </div>
    </div>
    <div class="ig-more">&middot;&middot;&middot;</div>
  </div>
  <div class="carousel-viewport">
    <div class="carousel-track">
      {slides_html}
    </div>
  </div>
  <div class="ig-actions">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg>
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"/></svg>
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
    <div class="spacer"></div>
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2z"/></svg>
  </div>
  <div class="ig-dots">{dots}</div>
  <div class="ig-caption">
    <span class="handle">{handle}</span> {caption}
    <span class="ts">2 horas atrás</span>
  </div>
</div>
<script>
(function(){{
  const track=document.querySelector('.carousel-track');
  const slides=document.querySelectorAll('.slide');
  const dots=document.querySelectorAll('.ig-dots .dot');
  let idx=0;const n=slides.length;
  function go(i){{idx=Math.max(0,Math.min(n-1,i));track.style.transform='translateX('+(-idx*420)+'px)';dots.forEach((d,k)=>d.classList.toggle('active',k===idx));}}
  let sx=0,dragging=false;
  const vp=document.querySelector('.carousel-viewport');
  vp.addEventListener('pointerdown',e=>{{dragging=true;sx=e.clientX;}});
  window.addEventListener('pointerup',e=>{{if(!dragging)return;dragging=false;const dx=e.clientX-sx;if(dx<-40)go(idx+1);else if(dx>40)go(idx-1);}});
  vp.addEventListener('click',e=>{{const r=vp.getBoundingClientRect();if(e.clientX-r.left>r.width/2)go(idx+1);else go(idx-1);}});
}})();
</script>
</body>
</html>"""
