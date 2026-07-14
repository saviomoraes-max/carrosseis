"""
bg_slide.py — Helpers de slide com imagem de fundo + fade overlay.

Usa a paleta oficial da brand-guidelines (2026-05):
- Cream     #F2DDB6
- Dark red  #3D0A0A
- Red       #FF3939
- Blue      #26428B

Sente livre pra usar junto com os helpers legados do reconecta_carousel.py
(masthead, render_carousel, etc.).
"""
import base64
from pathlib import Path
from typing import Literal

# ============================================================
# PALETA brand-guidelines 2026-05
# ============================================================
R_CREAM     = "#F2DDB6"
R_DARK_RED  = "#3D0A0A"
R_RED       = "#FF3939"
R_BLUE      = "#26428B"
R_MID_GRAY  = "#b0aea5"
R_LIGHT_GRAY = "#e8e6dc"


# ============================================================
# DATA URI helpers (imagem como base64)
# ============================================================
def image_uri(path) -> str:
    path = Path(path)
    ext = path.suffix.lower().lstrip(".")
    mime_map = {
        "jpg":  "image/jpeg",
        "jpeg": "image/jpeg",
        "png":  "image/png",
        "webp": "image/webp",
    }
    mime = mime_map.get(ext, "image/png")
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"


# ============================================================
# FADE OVERLAY CSS
# ============================================================
FadeDirection = Literal["bottom_to_middle", "top_to_middle", "none"]


def _fade_gradient(direction: FadeDirection, color: str, strength: float = 1.0) -> str:
    """
    Constrói um linear-gradient da base 100% opaca → 0% no meio do slide.
    Smooth ease-out via múltiplos stops pra não criar borda dura.

    `strength` controla a opacidade no extremo (default 1.0 = solid full).
    Mantido como param caso queira fade mais sutil em casos específicos.
    """
    if direction == "none":
        return "none"
    rgb = _hex_to_rgb(color)

    def c(o):
        return f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {round(o * strength, 3)})"

    to = "top" if direction == "bottom_to_middle" else "bottom"
    # Curva ease-out: solid até 5%, transição smooth, 0% exato no meio (50%)
    return (
        f"linear-gradient(to {to}, "
        f"{c(1.00)} 0%, "
        f"{c(1.00)} 5%, "
        f"{c(0.92)} 12%, "
        f"{c(0.78)} 22%, "
        f"{c(0.55)} 32%, "
        f"{c(0.30)} 41%, "
        f"{c(0.10)} 47%, "
        f"{c(0.00)} 50%)"
    )


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


# ============================================================
# MASTHEAD com paleta nova
# ============================================================
def masthead_recon(
    left: str = "RECONECTA",
    right: str = "",
    *,
    on_cream: bool = False,
) -> str:
    """
    Topo do slide com paleta brand-guidelines.
    Slide 1: passar `right=""` deixa o canto superior direito vazio (regra fixa).
    """
    if on_cream:
        lc, rc = "rgba(61,10,10,0.65)", R_RED
    else:
        lc, rc = "rgba(242,221,182,0.95)", R_CREAM
    sz = "7.4px"  # px(19) — viewport 420 (output 1080 ~19px)
    style_l = (f"font-family:'Grift';font-weight:400;font-size:{sz};"
               f"letter-spacing:3px;text-transform:uppercase;color:{lc};")
    style_r = (f"font-family:'Grift';font-weight:400;font-size:{sz};"
               f"letter-spacing:3px;text-transform:uppercase;color:{rc};")
    right_html = f'<span style="{style_r}">{right}</span>' if right else "<span></span>"
    return (
        f'<div style="display:flex;justify-content:space-between;align-items:center;">'
        f'<span style="{style_l}">{left}</span>'
        f'{right_html}'
        f'</div>'
    )


# ============================================================
# ANCHOR POSITIONING
# ============================================================
TextAnchor = Literal[
    "bottom_left", "bottom_center", "bottom_right",
    "top_left", "top_center", "top_right",
    "center", "lower_third",
]


def _anchor_to_css(anchor: TextAnchor) -> str:
    """Converte um anchor pra CSS de posicionamento absoluto dentro do slide."""
    base = "position:absolute;"
    pad  = "padding:38px 32px;"
    if anchor == "bottom_left":
        return f"{base}{pad}left:0;right:0;bottom:0;"
    if anchor == "bottom_center":
        return f"{base}{pad}left:0;right:0;bottom:0;text-align:center;"
    if anchor == "bottom_right":
        return f"{base}{pad}left:0;right:0;bottom:0;text-align:right;"
    if anchor == "top_left":
        return f"{base}{pad}left:0;right:0;top:48px;"
    if anchor == "top_center":
        return f"{base}{pad}left:0;right:0;top:48px;text-align:center;"
    if anchor == "top_right":
        return f"{base}{pad}left:0;right:0;top:48px;text-align:right;"
    if anchor == "center":
        return (f"{base}{pad}left:0;right:0;top:50%;"
                f"transform:translateY(-50%);text-align:center;")
    if anchor == "lower_third":
        # Ancora no bloco inferior do slide (~33% bottom)
        return f"{base}{pad}left:0;right:0;bottom:0;height:42%;"

    return f"{base}{pad}left:0;right:0;bottom:0;"


# ============================================================
# COMPONENTE PRINCIPAL — bg_image_slide
# ============================================================
def bg_image_slide(
    *,
    image_path,
    masthead_right: str = "",
    masthead_left: str = "RECONECTA",
    text_html: str = "",
    text_anchor: TextAnchor = "lower_third",
    fade_direction: FadeDirection = "bottom_to_middle",
    fade_color: str = R_DARK_RED,
    fade_strength: float = 1.0,
    object_position: str = "center 30%",
    is_hero: bool = False,
) -> str:
    """
    Slide com imagem de fundo + fade overlay + masthead + bloco de texto.

    Use pra slides 1, 3, 4, 6 (com background image).

    Args:
        image_path: Path da imagem (será embutida via data URI)
        masthead_right: número do slide ou label do canto direito.
                        Slide 1 (hero): SEMPRE "" — canto direito vazio é regra fixa.
                        Use is_hero=True pra forçar essa garantia.
        is_hero: se True (slide 1), masthead_right é forçado a "".
        text_anchor: posição do bloco de texto. "lower_third" é padrão pro slide 1.
        fade_direction: "bottom_to_middle" (default) ou "top_to_middle".
                        Fade vai de 100% opacidade na base/topo a 0% no meio.
        fade_color: cor do overlay (padrão R_DARK_RED).
        fade_strength: opacidade no extremo (0.0–1.0). Default 1.0 = solid full.
                       Reduza só pra casos onde quiser ver imagem na base.
        object_position: CSS object-position pra reframe da bg image.
                         Default "center 30%" enquadra rosto/upper body bem.

    Returns:
        HTML string de uma div.slide.
    """
    # is_hero suprime o masthead inteiro: ambos os cantos superiores vazios
    # (regra fixa, ver memory feedback_hero_masthead.md)
    suppress_masthead = is_hero
    if is_hero:
        masthead_right = ""
    img_uri    = image_uri(image_path)
    main_fade  = _fade_gradient(fade_direction, fade_color, fade_strength)
    anchor_css = _anchor_to_css(text_anchor)

    masthead_layer = "" if suppress_masthead else (
        f'<div style="position:absolute;top:24px;left:32px;right:32px;z-index:4;">'
        f'{masthead_recon(masthead_left, masthead_right)}'
        f'</div>'
    )

    text_layer = (
        f'<div style="{anchor_css}z-index:4;color:{R_CREAM};">'
        f'{text_html}'
        f'</div>'
    ) if text_html else ""

    main_fade_layer = (
        f'<div style="position:absolute;inset:0;background:{main_fade};'
        f'z-index:2;pointer-events:none;"></div>'
        if fade_direction != "none" else ""
    )

    return (
        f'<div class="slide" style="flex:0 0 420px;width:420px;height:100%;'
        f'position:relative;overflow:hidden;background:{fade_color};">'
        f'<img src="{img_uri}" alt="" '
        f'style="position:absolute;inset:0;width:100%;height:100%;'
        f'object-fit:cover;object-position:{object_position};z-index:1;" />'
        f'{main_fade_layer}'
        f'{masthead_layer}'
        f'{text_layer}'
        f'</div>'
    )


# ============================================================
# COMPONENTE PRINCIPAL — solid_slide
# ============================================================
def solid_slide(
    *,
    bg_color: str = R_DARK_RED,
    masthead_right: str = "",
    masthead_left: str = "RECONECTA",
    text_html: str = "",
    text_anchor: TextAnchor = "center",
) -> str:
    """
    Slide com fundo sólido (sem imagem). Use pra slides 2, 5, 7
    (alternar dark_red/cream).
    """
    on_cream = bg_color.upper() == R_CREAM.upper()
    text_color = R_DARK_RED if on_cream else R_CREAM
    anchor_css = _anchor_to_css(text_anchor)

    masthead_layer = (
        f'<div style="position:absolute;top:24px;left:32px;right:32px;z-index:3;">'
        f'{masthead_recon(masthead_left, masthead_right, on_cream=on_cream)}'
        f'</div>'
    )

    text_layer = (
        f'<div style="{anchor_css}color:{text_color};">'
        f'{text_html}'
        f'</div>'
    ) if text_html else ""

    return (
        f'<div class="slide" style="flex:0 0 420px;width:420px;height:100%;'
        f'position:relative;overflow:hidden;background:{bg_color};">'
        f'{masthead_layer}'
        f'{text_layer}'
        f'</div>'
    )


# ============================================================
# Standalone debug: gera 1 slide de exemplo e salva HTML
# ============================================================
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("uso: bg_slide.py <imagem_de_teste.jpg> [output.html]")
        sys.exit(1)

    img = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("bg_slide_test.html")

    SZ_HERO_SM = "37px"  # px(96) com S=2.5714
    SZ_BODY    = "12.4px"
    sample_text = (
        f'<p style="font-family:\'Grift\';font-weight:400;font-size:8px;'
        f'letter-spacing:2.5px;text-transform:uppercase;color:{R_RED};'
        f'margin-bottom:12px;">TESTE BG SLIDE</p>'
        f'<h1 style="font-family:\'Alga\';font-weight:600;font-size:{SZ_HERO_SM};'
        f'line-height:0.95;color:{R_CREAM};letter-spacing:-1px;">'
        f'Imagem de fundo com <em style="font-style:italic;color:{R_RED};">fade</em> '
        f'até o meio.</h1>'
        f'<p style="font-family:\'Grift\';font-weight:400;font-size:{SZ_BODY};'
        f'line-height:1.4;color:{R_CREAM};opacity:0.85;margin-top:14px;'
        f'max-width:340px;">Texto ancorado no terço inferior. Fade smooth, '
        f'sem shadow duro.</p>'
    )
    slide = bg_image_slide(
        image_path=img,
        is_hero=True,                # slide 1: canto direito vazio (regra fixa)
        text_html=sample_text,
        text_anchor="lower_third",
    )

    # Carrega fontes do template
    sys.path.insert(0, str(Path(__file__).parent))
    from reconecta_carousel import load_fonts
    fonts = load_fonts()

    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>{fonts}*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:{R_DARK_RED};display:flex;align-items:center;justify-content:center;
min-height:100vh;font-family:'Grift';}}em{{font-style:italic}}
.slide{{aspect-ratio:4/5;}}</style></head>
<body>{slide}</body></html>"""
    out.write_text(html, encoding="utf-8")
    print(f"OK — escrito em {out}")
