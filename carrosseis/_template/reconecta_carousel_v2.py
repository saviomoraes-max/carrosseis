"""
RECONECTA editorial carousel v2 — sistema visual extraído do Figma master.

Especificação completa em ../primitivas.json (v2.0).
Figma master: https://www.figma.com/design/Umktc72a6ZMfPhmNnew6TB/Design-referencia-claude

Uso típico em build.py:

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent / "_template"))
    from reconecta_carousel_v2 import *

    BASE = Path(__file__).parent
    IMG = BASE / "img"

    slide1 = slide_A_hero_perfil(
        image_uri=image_uri(IMG / "hero.jpg"),
        headline="A Coca-Cola está tentando vender água com outro nome?",
        subtitle="A estratégia dos três zeros que pode redefinir um ícone global",
    )
    slide2 = slide_B_text_only_short(
        headline="Refrigerante ou água com marca?",
        body="A Coca-Cola lançou na Europa a Triple Z..."
    )
    ...
    html = render_carousel([slide1, slide2, ...], caption="...")
    Path("carousel.html").write_text(html, encoding="utf-8")

Mapeamento primitiva ↔ Figma:
- A: Futurista 1 (hero com perfil@)
- B: Futurista 2 (text-only body 64px)
- C: Futurista 3 (cream) e 9 (dark) — 2 imagens stacked
- D: Futurista 4 (cream text+body+image)
- E: Futurista 5 (image full-bleed + texto bottom)
- F: Futurista 6 e 8 (text-only body 48px)
- G: Futurista 7 (single image grande)
- H: Futurista 10 (text+image+text)
"""
import base64
from pathlib import Path


# ============================================================
# PALETA (Figma master 2026-05-07)
# ============================================================
BG_DARK = "#2d0000"
BG_CREAM = "#f2ddb6"
BG_LIGHT = "#f5f5f5"
BG_ACCENT = "#ff4d00"
POP_HEADLINE = "#f0d28a"  # champagne / off-gold — vermelho abolido como ênfase tipográfica em 2026-05-18
POP_FOOTER_CREAM = "#ff1717"  # estrutural, footer text em fundo cream — não usar como ênfase
TEXT_LIGHT = "#f5f5f5"
TEXT_DARK = "#040416"
FOOTER_BG = "rgba(4,4,22,0.05)"


# ============================================================
# TIPOGRAFIA — sizes em "output px" (1080x1350). Render em 420x525.
# S = 1080/420 ≈ 2.5714
# ============================================================
S = 2.5714


def px(output_px: float) -> str:
    """Converte px do output (1080-coord) pra CSS px do viewport (420-coord)."""
    return f"{round(output_px / S, 2)}px"


# Hero (Alga)
SZ_HERO_LARGE = px(128)
SZ_HERO_COMPACT = px(95)

# Body (Inter)
SZ_BODY_DENSE = px(64)
SZ_BODY_LARGE = px(48)
SZ_BODY_DEFAULT = px(40)
SZ_BODY_MID = px(38)
SZ_BODY_COMPACT = px(36)

# Componentes
SZ_HANDLE = px(28)
SZ_FOOTER = px(18)
SZ_INFO = px(11)


# ============================================================
# RADIUS & BORDER
# ============================================================
IMG_RADIUS = px(60)
IMG_BORDER = f"1px solid {TEXT_LIGHT}"
FOOTER_RADIUS = px(32)


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
    """Embute Alga + Inter como @font-face. Default usa _template/fonts/."""
    if font_dir is None:
        font_dir = Path(__file__).parent / "fonts"
    font_dir = Path(font_dir)
    return "".join([
        _font_face("Alga", 500, "normal", font_dir, "Alga-SemiBold.otf"),
        _font_face("Alga", 600, "normal", font_dir, "Alga-SemiBold.otf"),
        _font_face("Inter", 500, "normal", font_dir, "Inter-Medium.ttf"),
        _font_face("Inter", 700, "normal", font_dir, "Inter-Bold.ttf"),
    ])


# ============================================================
# ASSETS DEFAULT (carregam do _template/ se existirem)
# ============================================================
_TEMPLATE_DIR = Path(__file__).parent


def _load_default(filename):
    p = _TEMPLATE_DIR / filename
    return image_uri(p) if p.exists() else None


DEFAULT_GRAIN_URI = _load_default("grain.png")
DEFAULT_AVATAR_URI = _load_default("default_avatar.png")
DEFAULT_VERIFIED_URI = _load_default("verified_badge.png")


# ============================================================
# ICONES INLINE (SVG)
# ============================================================
def arrow_svg(color: str = TEXT_LIGHT) -> str:
    """Seta horizontal → do footer (path extraído do Figma)."""
    return (
        f'<svg viewBox="0 0 31.5656 26" xmlns="http://www.w3.org/2000/svg" '
        f'style="width:{px(21)};height:{px(26)};display:block;">'
        f'<path d="M28.4386 13.7071C28.8291 13.3166 28.8291 12.6834 28.4386 12.2929'
        f'L22.0746 5.92893C21.6841 5.53841 21.051 5.53841 20.6604 5.92893C20.2699 6.31946 '
        f'20.2699 6.95262 20.6604 7.34315L26.3173 13L20.6604 18.6569C20.2699 19.0474 '
        f'20.2699 19.6805 20.6604 20.0711C21.051 20.4616 21.6841 20.4616 22.0746 20.0711'
        f'L28.4386 13.7071ZM-2.02644e-07 13V14H27.7315V13V12H-2.02644e-07V13Z" '
        f'fill="{color}"/></svg>'
    )


# ============================================================
# UNIVERSAIS — aparecem em TODOS os slides (1-10)
# ============================================================
def grains_overlay(grain_uri: str = None) -> str:
    """Overlay de noise full-bleed, tile 200x200, opacity 0.32."""
    uri = grain_uri or DEFAULT_GRAIN_URI
    if uri is None:
        return ""  # silencioso se asset não existir
    tile = px(200)
    return (
        f'<div style="position:absolute;inset:0;background-image:url({uri});'
        f'background-size:{tile} {tile};background-repeat:repeat;'
        f'opacity:0.32;pointer-events:none;z-index:2;"></div>'
    )


def info_bar(color: str = TEXT_LIGHT, top: int = 33) -> str:
    """'RECONECTA' top-right. Canto top-left fica VAZIO."""
    return (
        f'<div style="position:absolute;top:{px(top)};left:{px(38)};'
        f'width:{px(1004)};height:{px(16)};z-index:5;">'
        f'<p style="position:absolute;right:0;top:0;font-family:\'Inter\';'
        f'font-weight:700;font-size:{SZ_INFO};text-transform:uppercase;'
        f'color:{color};margin:0;letter-spacing:0;">RECONECTA</p>'
        f"</div>"
    )


def _pill(text: str, text_color: str, top: int, width: int) -> str:
    """Pill base — texto + seta alinhados à direita, sem asterisco."""
    track = px(2.52)
    return (
        f'<div style="position:absolute;top:{px(top)};left:50%;'
        f'transform:translateX(-50%);width:{px(width)};height:{px(58)};'
        f'padding:{px(16)} {px(25)};background:{FOOTER_BG};'
        f'border:1px solid {TEXT_LIGHT};border-radius:{FOOTER_RADIUS};'
        f"display:flex;align-items:center;justify-content:flex-end;"
        f'box-sizing:border-box;z-index:5;">'
        f'<div style="display:flex;gap:{px(22)};align-items:center;">'
        f"<span style=\"font-family:'Inter';font-weight:700;font-size:{SZ_FOOTER};"
        f'letter-spacing:{track};color:{text_color};white-space:nowrap;'
        f'text-transform:uppercase;">{text}</span>'
        f"<span style=\"font-family:'Inter';font-weight:700;font-size:{SZ_FOOTER};"
        f'letter-spacing:{track};color:{text_color};">/</span>'
        f"<div>{arrow_svg(text_color)}</div>"
        f"</div></div>"
    )


def footer_pill(text_color: str = TEXT_LIGHT, top: int = 1246, width: int = 1004) -> str:
    """Pill 'ARRASTE PARA O LADO  /  →' — usado em todos os slides exceto o CTA final."""
    return _pill("ARRASTE PARA O LADO", text_color, top, width)


def cta_pill(text: str = "CLIQUE NO LINK DA BIO", text_color: str = TEXT_LIGHT) -> str:
    """CTA pill compacta inline — width fit-content, padding apertado, alinhamento via parent flex.

    NÃO é absolute positioned. Usada inline dentro de slide_I_cta como 3º item da pilha.
    Para CTA full-width (ex: ads), usar _pill() diretamente.
    """
    track = px(2.52)
    return (
        f'<div style="display:inline-flex;align-items:center;gap:{px(18)};'
        f'padding:{px(14)} {px(22)};background:{FOOTER_BG};'
        f'border:1px solid {TEXT_LIGHT};border-radius:{FOOTER_RADIUS};'
        f'box-sizing:border-box;">'
        f"<span style=\"font-family:'Inter';font-weight:700;font-size:{SZ_FOOTER};"
        f'letter-spacing:{track};color:{text_color};white-space:nowrap;'
        f'text-transform:uppercase;">{text}</span>'
        f"<span style=\"font-family:'Inter';font-weight:700;font-size:{SZ_FOOTER};"
        f'letter-spacing:{track};color:{text_color};">/</span>'
        f"<div>{arrow_svg(text_color)}</div>"
        f"</div>"
    )


# ============================================================
# PRIMITIVA A — HERO COM PERFIL (Futurista 1)
# ============================================================
def slide_A_hero_perfil(
    image_uri: str,
    headline: str,
    subtitle: str,
    avatar_uri: str = None,
    handle: str = "@oleonardorosso",
    verified_uri: str = None,
    grain_uri: str = None,
) -> str:
    """Slide 1 hero — única primitiva que carrega bloco perfil/@."""
    avatar = avatar_uri or DEFAULT_AVATAR_URI
    verified = verified_uri or DEFAULT_VERIFIED_URI
    return f"""
<div class="slide" style="background:{BG_ACCENT};position:relative;overflow:hidden;">
  <img src="{image_uri}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;z-index:1;" alt="">
  <div style="position:absolute;inset:0;background:linear-gradient(210deg, rgba(0,0,0,0) 22.39%, rgb(0,0,0) 63.48%);z-index:3;"></div>
  {grains_overlay(grain_uri)}
  {info_bar(TEXT_LIGHT)}
  <div style="position:absolute;top:{px(684)};left:{px(48)};width:{px(983)};display:flex;flex-direction:column;gap:{px(37)};z-index:5;">
    <div style="display:flex;gap:{px(18)};align-items:center;">
      <img src="{avatar}" style="width:{px(57)};height:{px(57)};border-radius:50%;object-fit:cover;display:block;" alt="">
      <p style="font-family:'Inter';font-weight:500;font-size:{SZ_HANDLE};color:{TEXT_LIGHT};letter-spacing:{px(-1.68)};margin:0;white-space:nowrap;">{handle}</p>
      <div style="width:{px(33)};height:{px(38)};overflow:hidden;position:relative;">
        <img src="{verified}" style="position:absolute;width:1031.62%;height:189.47%;left:-930.96%;top:-44.74%;max-width:none;display:block;" alt="">
      </div>
    </div>
    <p style="font-family:'Alga';font-weight:600;font-size:{SZ_HERO_COMPACT};color:{POP_HEADLINE};line-height:0.97;letter-spacing:{px(-5.7)};margin:0;width:{px(965)};">{headline}</p>
    <p style="font-family:'Inter';font-weight:700;font-size:{SZ_BODY_DEFAULT};color:{TEXT_LIGHT};line-height:1.24;letter-spacing:{px(-0.97)};margin:0;width:{px(838)};">{subtitle}</p>
  </div>
  {footer_pill(TEXT_LIGHT, top=1246, width=983)}
</div>
"""


# ============================================================
# HERO IMAGEM-NO-TOPO + FADE RECUADO  (padrão preferido — validado 2026-05-20, AD004)
# Variante de slide 1 mais agradável: imagem grande no topo, fade que só começa
# por volta de ~50% (rosto/sujeito aparece bem) e bloco perfil+headline+subtitle
# ancorado mais embaixo (~55% da altura). Cantos superiores VAZIOS (sem info_bar)
# — regra fixa do slide 1. Use ESTE hero por padrão em carrosséis novos.
# ============================================================
def slide_hero_image_top(
    image_uri: str,
    headline: str,
    subtitle: str,
    *,
    handle: str = "@oleonardorosso",
    img_h: int = 900,
    text_top: int = 740,
    object_position: str = "center 28%",
    headline_size: int = 72,
    headline_color: str = "#f3deb9",
    avatar_uri: str = None,
    verified_uri: str = None,
    grain_uri: str = None,
) -> str:
    """HERO imagem-no-topo + fade recuado. headline aceita HTML (<br/>, <span italic>).
    Os stops do fade são percentuais (escalam com img_h). Reduza text_top pra subir o
    bloco, aumente img_h pra mostrar mais imagem."""
    avatar = avatar_uri or DEFAULT_AVATAR_URI
    verified = verified_uri or DEFAULT_VERIFIED_URI
    if image_uri:
        layer = (
            f'<img src="{image_uri}" style="position:absolute;top:0;left:0;width:100%;'
            f'height:{px(img_h)};object-fit:cover;object-position:{object_position};'
            f'display:block;z-index:1;" alt="">'
        )
    else:
        layer = (
            f'<div style="position:absolute;top:0;left:0;width:100%;height:{px(img_h)};'
            f'background:linear-gradient(135deg,#3a0a0a,#2d0000);display:flex;align-items:center;'
            f'justify-content:center;z-index:1;"><span style="font-family:\'Inter\';font-weight:700;'
            f'font-size:{px(34)};color:rgba(245,245,245,0.32);letter-spacing:{px(2)};'
            f'text-transform:uppercase;">coloque a imagem do hero</span></div>'
        )
    return f"""
<div class="slide" style="background:{BG_DARK};position:relative;overflow:hidden;">
  {layer}
  <div style="position:absolute;top:0;left:0;width:100%;height:{px(img_h)};background:linear-gradient(180deg, rgba(45,0,0,0) 0%, rgba(45,0,0,0) 50%, rgba(45,0,0,0.04) 58%, rgba(45,0,0,0.14) 65%, rgba(45,0,0,0.28) 72%, rgba(45,0,0,0.44) 79%, rgba(45,0,0,0.62) 85%, rgba(45,0,0,0.80) 90%, rgba(45,0,0,0.94) 95%, {BG_DARK} 99%);z-index:2;"></div>
  {grains_overlay(grain_uri)}
  <div style="position:absolute;top:{px(text_top)};left:{px(48)};width:{px(984)};display:flex;flex-direction:column;gap:{px(34)};z-index:5;">
    <div style="display:flex;gap:{px(18)};align-items:center;">
      <img src="{avatar}" style="width:{px(57)};height:{px(57)};border-radius:50%;object-fit:cover;display:block;" alt="">
      <p style="font-family:'Inter';font-weight:500;font-size:{SZ_HANDLE};color:{TEXT_LIGHT};letter-spacing:{px(-1.68)};margin:0;white-space:nowrap;">{handle}</p>
      <div style="width:{px(33)};height:{px(38)};overflow:hidden;position:relative;">
        <img src="{verified}" style="position:absolute;width:1031.62%;height:189.47%;left:-930.96%;top:-44.74%;max-width:none;display:block;" alt="">
      </div>
    </div>
    <p style="font-family:'Alga';font-weight:600;font-size:{px(headline_size)};color:{headline_color};line-height:1.04;letter-spacing:{px(-3.4)};margin:0;width:{px(984)};">{headline}</p>
    <p style="font-family:'Inter';font-weight:500;font-size:{px(30)};color:{TEXT_LIGHT};line-height:1.4;letter-spacing:{px(-0.4)};margin:0;width:{px(900)};opacity:0.92;">{subtitle}</p>
  </div>
  {footer_pill(TEXT_LIGHT, top=1246)}
</div>
"""


# ============================================================
# PRIMITIVA B — TEXT-ONLY com body 64px (Futurista 2)
# ============================================================
def slide_B_text_only_short(headline: str, body: str, grain_uri: str = None) -> str:
    return f"""
<div class="slide" style="background:{BG_DARK};position:relative;overflow:hidden;">
  {grains_overlay(grain_uri)}
  {info_bar(TEXT_LIGHT)}
  <p style="position:absolute;top:{px(127)};left:{px(38)};width:{px(904)};font-family:'Alga';font-weight:500;font-size:{SZ_HERO_LARGE};color:{POP_HEADLINE};line-height:1.04;letter-spacing:{px(-7.68)};margin:0;z-index:5;">{headline}</p>
  <p style="position:absolute;top:{px(730)};left:{px(38)};width:{px(904)};font-family:'Inter';font-weight:500;font-size:{SZ_BODY_DENSE};color:{TEXT_LIGHT};line-height:1.44;letter-spacing:{px(-1.28)};margin:0;z-index:5;white-space:pre-wrap;">{body}</p>
  {footer_pill(TEXT_LIGHT, top=1256)}
</div>
"""


# ============================================================
# PRIMITIVA C — DUAL IMAGE STACKED (Futurista 3 cream / 9 dark)
# ============================================================
def slide_C_dual_image(
    img_top: str,
    img_bottom: str,
    cream: bool = False,
    grain_uri: str = None,
) -> str:
    bg = BG_CREAM if cream else BG_DARK
    info_color = BG_DARK if cream else TEXT_LIGHT
    footer_color = POP_FOOTER_CREAM if cream else TEXT_LIGHT
    return f"""
<div class="slide" style="background:{bg};position:relative;overflow:hidden;">
  {grains_overlay(grain_uri)}
  {info_bar(info_color)}
  <div style="position:absolute;top:{px(137)};left:{px(38)};width:{px(1004)};display:flex;flex-direction:column;gap:{px(74)};z-index:4;">
    <div style="width:{px(1004)};height:{px(474)};border-radius:{IMG_RADIUS};border:{IMG_BORDER};overflow:hidden;">
      <img src="{img_top}" style="width:100%;height:100%;object-fit:cover;display:block;" alt="">
    </div>
    <div style="width:{px(1004)};height:{px(474)};border-radius:{IMG_RADIUS};border:{IMG_BORDER};overflow:hidden;">
      <img src="{img_bottom}" style="width:100%;height:100%;object-fit:cover;display:block;" alt="">
    </div>
  </div>
  {footer_pill(footer_color, top=1246, width=983)}
</div>
"""


# ============================================================
# PRIMITIVA D — TEXT + BODY + IMAGE em fundo cream (Futurista 4)
# ============================================================
def slide_D_text_body_image_cream(
    headline: str,
    body: str,
    image_uri: str,
    grain_uri: str = None,
) -> str:
    return f"""
<div class="slide" style="background:{BG_CREAM};position:relative;overflow:hidden;">
  {grains_overlay(grain_uri)}
  {info_bar(BG_ACCENT, top=29)}
  <div style="position:absolute;top:{px(113)};left:{px(48)};width:{px(970)};display:flex;flex-direction:column;gap:{px(48)};z-index:5;">
    <p style="font-family:'Alga';font-weight:500;font-size:{SZ_HERO_LARGE};color:{POP_HEADLINE};line-height:1.04;letter-spacing:{px(-7.68)};margin:0;">{headline}</p>
    <p style="font-family:'Inter';font-weight:500;font-size:{SZ_BODY_MID};color:{TEXT_DARK};line-height:1.44;letter-spacing:{px(-0.76)};margin:0;">{body}</p>
    <div style="width:{px(970)};height:{px(523)};border-radius:{IMG_RADIUS};border:{IMG_BORDER};overflow:hidden;">
      <img src="{image_uri}" style="width:100%;height:100%;object-fit:cover;display:block;" alt="">
    </div>
  </div>
  {footer_pill(POP_FOOTER_CREAM, top=1246)}
</div>
"""


# ============================================================
# PRIMITIVA E — IMAGE FULL-BLEED + texto bottom (Futurista 5)
# ============================================================
def slide_E_image_bg_text_bottom(
    image_uri: str,
    headline: str,
    body: str,
    grain_uri: str = None,
    *,
    text_top: int = 654,
    headline_size: str = None,
    body_size: str = None,
    gap: int = 53,
) -> str:
    """Slide 5 padrão. Overrides opcionais quando copy é mais densa que o
    spec do Figma — headline_size pode cair pra SZ_HERO_COMPACT (95px)
    e body_size pode cair pra SZ_BODY_COMPACT (36px) ou customizado."""
    h_size = headline_size or SZ_HERO_LARGE
    b_size = body_size or SZ_BODY_MID
    return f"""
<div class="slide" style="background:{BG_LIGHT};position:relative;overflow:hidden;">
  <img src="{image_uri}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;z-index:1;" alt="">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg, rgba(0,0,0,0) 8.37%, #000 73.111%);z-index:3;"></div>
  {grains_overlay(grain_uri)}
  {info_bar(TEXT_LIGHT, top=35)}
  <div style="position:absolute;top:{px(text_top)};left:{px(48)};width:{px(927)};display:flex;flex-direction:column;gap:{px(gap)};z-index:5;">
    <p style="font-family:'Alga';font-weight:500;font-size:{h_size};color:{POP_HEADLINE};line-height:1.04;letter-spacing:{px(-7.68)};margin:0;">{headline}</p>
    <p style="font-family:'Inter';font-weight:500;font-size:{b_size};color:{TEXT_LIGHT};line-height:1.44;letter-spacing:{px(-0.76)};margin:0;width:{px(906)};">{body}</p>
  </div>
  {footer_pill(TEXT_LIGHT, top=1246)}
</div>
"""


# ============================================================
# PRIMITIVA F — TEXT-ONLY com body 48px (Futurista 6 e 8)
# ============================================================
def slide_F_text_only_large(
    headline: str,
    body: str,
    headline_top: int = 117,
    body_top: int = 763,
    grain_uri: str = None,
    *,
    headline_size: str = None,
    headline_width: int = 889,
    body_size: str = None,
    body_width: int = 865,
    letter_spacing: str = None,
) -> str:
    """Slide F padrão. Overrides opcionais quando copy é densa:
    - headline_size = SZ_HERO_COMPACT (95px) pra headlines que wrappam em 3+ linhas
    - body_size = SZ_BODY_MID (38px) ou SZ_BODY_COMPACT (36px) pra body denso
    - widths podem ser ampliadas (até 1004px) pra evitar wrap excessivo
    - letter_spacing: o default -7.68px é calibrado pro headline gigante (128px);
      ao REDUZIR headline_size, passe um tracking proporcional (ex. px(-2)) senão as letras se esmagam"""
    h_size = headline_size or SZ_HERO_LARGE
    b_size = body_size or SZ_BODY_LARGE
    hl_ls = letter_spacing or px(-7.68)
    return f"""
<div class="slide" style="background:{BG_DARK};position:relative;overflow:hidden;">
  {grains_overlay(grain_uri)}
  {info_bar(TEXT_LIGHT)}
  <p style="position:absolute;top:{px(headline_top)};left:{px(38)};width:{px(headline_width)};font-family:'Alga';font-weight:500;font-size:{h_size};color:{POP_HEADLINE};line-height:1.04;letter-spacing:{hl_ls};margin:0;z-index:5;">{headline}</p>
  <p style="position:absolute;top:{px(body_top)};left:{px(38)};width:{px(body_width)};font-family:'Inter';font-weight:500;font-size:{b_size};color:{TEXT_LIGHT};line-height:1.44;letter-spacing:{px(-0.96)};margin:0;z-index:5;">{body}</p>
  {footer_pill(TEXT_LIGHT, top=1246)}
</div>
"""


# ============================================================
# PRIMITIVA G — SINGLE BIG IMAGE (Futurista 7)
# ============================================================
def slide_G_single_image(image_uri: str, grain_uri: str = None) -> str:
    return f"""
<div class="slide" style="background:{BG_DARK};position:relative;overflow:hidden;">
  {grains_overlay(grain_uri)}
  {info_bar(TEXT_LIGHT, top=29)}
  <div style="position:absolute;top:{px(137)};left:{px(38)};width:{px(1004)};height:{px(1048)};border-radius:{IMG_RADIUS};border:{IMG_BORDER};overflow:hidden;z-index:4;">
    <img src="{image_uri}" style="width:100%;height:100%;object-fit:cover;display:block;" alt="">
  </div>
  {footer_pill(TEXT_LIGHT, top=1246)}
</div>
"""


# ============================================================
# PRIMITIVA H — TEXT + IMAGE + TEXT (Futurista 10)
# ============================================================
def slide_H_text_image_text(
    headline: str,
    image_uri: str,
    body: str,
    grain_uri: str = None,
) -> str:
    return f"""
<div class="slide" style="background:{BG_DARK};position:relative;overflow:hidden;">
  {grains_overlay(grain_uri)}
  {info_bar(TEXT_LIGHT)}
  <div style="position:absolute;top:{px(74)};left:{px(33)};width:{px(970)};display:flex;flex-direction:column;gap:{px(41)};z-index:5;">
    <p style="font-family:'Alga';font-weight:500;font-size:{SZ_HERO_LARGE};color:{POP_HEADLINE};line-height:1.04;letter-spacing:{px(-7.68)};margin:0;width:{px(760)};">{headline}</p>
    <div style="width:{px(970)};height:{px(445)};border-radius:{IMG_RADIUS};border:{IMG_BORDER};overflow:hidden;">
      <img src="{image_uri}" style="width:100%;height:100%;object-fit:cover;display:block;" alt="">
    </div>
    <p style="font-family:'Inter';font-weight:500;font-size:{SZ_BODY_COMPACT};color:{TEXT_LIGHT};line-height:1.44;letter-spacing:{px(0.33)};margin:0;width:{px(970)};">{body}</p>
  </div>
  {footer_pill(TEXT_LIGHT, top=1246, width=1009)}
</div>
"""


# ============================================================
# PRIMITIVA I — CTA FINAL (último slide do carrossel)
# Mesma estrutura de slide_F (text-only) MAS com cta_pill no lugar do footer_pill.
# ============================================================
def slide_I_cta(
    headline: str,
    body: str,
    cta_text: str = "CLIQUE NO LINK DA BIO",
    grain_uri: str = None,
) -> str:
    """CTA final — headline + body + cta_pill compacta numa pilha vertical-center,
    left-aligned, gap 32px entre cada elemento."""
    return f"""
<div class="slide" style="background:{BG_DARK};position:relative;overflow:hidden;">
  {grains_overlay(grain_uri)}
  {info_bar(TEXT_LIGHT)}
  <div style="position:absolute;top:50%;left:{px(38)};transform:translateY(-50%);width:{px(1004)};display:flex;flex-direction:column;gap:{px(32)};align-items:flex-start;z-index:5;">
    <p style="font-family:'Alga';font-weight:500;font-size:{SZ_HERO_LARGE};color:{POP_HEADLINE};line-height:1.04;letter-spacing:{px(-7.68)};margin:0;width:{px(889)};">{headline}</p>
    <p style="font-family:'Inter';font-weight:500;font-size:{SZ_BODY_LARGE};color:{TEXT_LIGHT};line-height:1.44;letter-spacing:{px(-0.96)};margin:0;width:{px(865)};">{body}</p>
    {cta_pill(cta_text, TEXT_LIGHT)}
  </div>
</div>
"""


# ============================================================
# SHELL HTML — IG frame + swipe interativo
# ============================================================
def render_carousel(
    slides: list,
    *,
    handle: str = "mentoriareconecta",
    subtitle: str = "Patrocinado",
    caption: str = "",
    font_faces: str = None,
    title: str = "Carrossel RECONECTA",
) -> str:
    """Monta HTML final com IG frame + slides + swipe."""
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
  html,body{{background:{BG_DARK};min-height:100vh;display:flex;align-items:center;justify-content:center;padding:40px 20px;font-family:'Inter',sans-serif;color:{TEXT_LIGHT}}}

  .ig-frame{{width:420px;max-width:420px;background:#fff;border-radius:12px;box-shadow:0 24px 60px rgba(0,0,0,0.12);overflow:hidden}}
  .ig-header{{display:flex;align-items:center;justify-content:space-between;padding:12px 14px;border-bottom:1px solid #EFEFEF}}
  .ig-user{{display:flex;align-items:center;gap:10px}}
  .ig-avatar{{width:34px;height:34px;border-radius:50%;background:{BG_DARK};display:flex;align-items:center;justify-content:center;color:{TEXT_LIGHT};font-family:'Alga';font-style:italic;font-weight:600;font-size:18px;border:2px solid #fff;box-shadow:0 0 0 2px {BG_DARK}}}
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
  const viewport=document.querySelector('.carousel-viewport');
  const track=document.querySelector('.carousel-track');
  const dots=document.querySelectorAll('.ig-dots .dot');
  const total={total};
  let index=0,startX=0,currentX=0,dragging=false;
  function setIndex(i){{
    index=Math.max(0,Math.min(total-1,i));
    track.style.transform=`translateX(${{-index*420}}px)`;
    dots.forEach((d,k)=>d.classList.toggle('active',k===index));
  }}
  viewport.addEventListener('pointerdown',e=>{{dragging=true;startX=e.clientX;currentX=e.clientX;track.style.transition='none';viewport.setPointerCapture(e.pointerId)}});
  viewport.addEventListener('pointermove',e=>{{if(!dragging)return;currentX=e.clientX;const dx=currentX-startX;track.style.transform=`translateX(${{-index*420+dx}}px)`}});
  viewport.addEventListener('pointerup',()=>{{if(!dragging)return;dragging=false;track.style.transition='transform 350ms cubic-bezier(0.22,1,0.36,1)';const dx=currentX-startX;if(dx<-40&&index<total-1)setIndex(index+1);else if(dx>40&&index>0)setIndex(index-1);else setIndex(index)}});
  viewport.addEventListener('pointercancel',()=>{{dragging=false;setIndex(index)}});
  setIndex(0);
}})();
</script>

</body>
</html>
"""
