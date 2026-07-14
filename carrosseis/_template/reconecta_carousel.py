"""
RECONECTA editorial carousel — módulo core reutilizável.

Fornece tudo que é compartilhado entre carrosséis:
- Paleta editorial luxury (near-black + ivory + gold + burgundy accent)
- Escala tipográfica (output 1080x1350 → viewport 420x525)
- Helpers para @font-face (Alga + Grift)
- Componentes primitivos (masthead, arrow, thin_line, real_example_tag)
- Shell HTML com IG frame e swipe interativo (render_carousel)
- Data URI helpers pra imagens

Uso no build.py de um carrossel:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent / "_template"))
    from reconecta_carousel import *

    slide1 = f'''<div class="slide" ...>...</div>'''
    ...
    html = render_carousel([slide1, slide2, ...], caption="...")
    Path("carousel.html").write_text(html, encoding="utf-8")
"""
import base64
from pathlib import Path

# ============================================================
# PALETA EDITORIAL LUXURY
# ============================================================
BG_BLACK = "#0F0505"          # primário escuro (slides dark)
BG_WINE = "#1A0808"           # wine-black para layering
BG_BURGUNDY = "#4A0A0A"       # burgundy escuro para accent panels
ACCENT = "#6B0F0F"            # burgundy brilhante (tags, pills, pop em slides cream)
IVORY = "#EDE3CE"             # ivory quente (cards, texto em fundo escuro)
IVORY_DEEP = "#D9CCAE"        # ivory mais escuro para layering
TEXT_DARK = "#1A0F0A"         # coffee-brown (texto em fundo claro)
TEXT_LIGHT = "#EDE3CE"        # ivory (texto em fundo escuro)
TEXT_MUTED = "#8A7F6D"        # muted grey-brown
GOLD = "#B8965A"              # champagne gold (detalhes finos, accent em dark)
POP = "#C9252D"               # crimson pop — usar só em 1 palavra por slide max


# ============================================================
# ESCALA TIPOGRÁFICA
# Sizes em "output px" (1080x1350). Renderização em 420x525.
# S = scale factor = 1080 / 420 ≈ 2.5714
# ============================================================
S = 2.5714


def px(output_px: int) -> str:
    """Converte px do output final pra CSS px do viewport."""
    return f"{round(output_px / S, 1)}px"


SZ_HERO = px(120)        # Alga SemiBold headline hero
SZ_HERO_SM = px(96)      # Alga secundário (CTA final)
SZ_TITLE_LG = px(72)     # Grift Black título grande
SZ_TITLE = px(60)        # Grift Black título padrão
SZ_SUB = px(44)          # Grift subtítulo
SZ_BODY = px(32)         # Grift corpo padrão
SZ_SMALL = px(26)        # Grift menor
SZ_LABEL = px(20)        # labels intermediários
SZ_MICRO = px(16)        # micro labels (masthead, small caps)


# ============================================================
# DATA URI (fontes + imagens)
# ============================================================
def data_uri(path: Path, mime: str) -> str:
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"


def image_uri(path) -> str:
    """Embute imagem como data URI. Detecta mime pelo sufixo."""
    path = Path(path)
    ext = path.suffix.lower().lstrip(".")
    mime_map = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp",
    }
    return data_uri(path, mime_map.get(ext, "image/png"))


def _font_face(family: str, weight: int, style: str, font_dir: Path, filename: str) -> str:
    path = font_dir / filename
    ext = filename.split(".")[-1].lower()
    mime = "font/otf" if ext == "otf" else "font/ttf"
    fmt = "opentype" if ext == "otf" else "truetype"
    uri = data_uri(path, mime)
    return (
        f"@font-face{{font-family:'{family}';font-weight:{weight};"
        f"font-style:{style};src:url({uri}) format('{fmt}');}}"
    )


def load_fonts(font_dir: Path = None) -> str:
    """
    Retorna CSS @font-face embutindo Alga + Grift.
    Se font_dir=None, usa ./fonts/ dentro do template.
    """
    if font_dir is None:
        font_dir = Path(__file__).parent / "fonts"
    font_dir = Path(font_dir)
    return "".join([
        _font_face("Alga", 600, "normal", font_dir, "Alga-SemiBold.otf"),
        _font_face("Grift", 900, "normal", font_dir, "Grift-Black.ttf"),
        _font_face("Grift", 900, "italic", font_dir, "Grift-BlackItalic.ttf"),
        _font_face("Grift", 400, "normal", font_dir, "Grift-Regular.ttf"),
        _font_face("Grift", 400, "italic", font_dir, "Grift-Italic.ttf"),
    ])


# ============================================================
# COMPONENTES PRIMITIVOS
# ============================================================
def arrow(color: str = GOLD, size: int = 22) -> str:
    """Seta horizontal estilo editorial (→)."""
    return (
        f'<svg width="{size}" height="{int(size*0.42)}" viewBox="0 0 40 14" '
        f'style="display:inline-block;vertical-align:middle;margin-left:8px;">'
        f'<path d="M1 7 L36 7 M30 2 L37 7 L30 12" stroke="{color}" '
        f'stroke-width="1.2" fill="none" stroke-linecap="round"/></svg>'
    )


def thin_line(color: str = GOLD, width: str = "40px") -> str:
    """Linha decorativa fina estilo editorial."""
    return f'<div style="width:{width};height:1px;background:{color};"></div>'


def masthead(left: str, right: str, *, cream_bg: bool = False) -> str:
    """
    Topo da slide: label esquerda + label direita, small caps tracking 3px.
    Ajusta cores automaticamente pra fundo escuro (default) ou claro.
    """
    if cream_bg:
        lc = "rgba(26,15,10,0.5)"
        rc = ACCENT
    else:
        lc = "rgba(237,227,206,0.55)"
        rc = GOLD
    return (
        f'<div style="display:flex;justify-content:space-between;align-items:center;">'
        f"<span style=\"font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;text-transform:uppercase;color:{lc};\">{left}</span>"
        f"<span style=\"font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;color:{rc};text-transform:uppercase;\">{right}</span>"
        f"</div>"
    )


def real_example_tag(text: str, color: str = GOLD) -> str:
    """Tag 'EXEMPLO REAL · ...' com bullet, pra indicar imagem de exemplo."""
    return (
        f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">'
        f'<div style="width:6px;height:6px;border-radius:50%;background:{color};"></div>'
        f"<p style=\"font-family:'Grift';font-weight:900;font-size:{SZ_MICRO};letter-spacing:2.5px;text-transform:uppercase;color:{color};\">{text}</p>"
        f"</div>"
    )


def divider_with_label(label: str, color: str = GOLD) -> str:
    """Divisor horizontal com label centralizado ('— VOCÊ PRECISA —')."""
    return (
        f'<div style="display:flex;align-items:center;gap:14px;">'
        f'<div style="flex:1;height:1px;background:{color}55;"></div>'
        f"<span style=\"font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;text-transform:uppercase;color:{color};\">{label}</span>"
        f'<div style="flex:1;height:1px;background:{color}55;"></div>'
        f"</div>"
    )


# ============================================================
# HTML SHELL — IG frame + swipe script
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
    """
    Monta o HTML final com todas as slides dentro do IG frame.

    slides: lista de strings HTML (cada uma um <div class="slide">...)
    handle/subtitle: exibidos no header do IG
    caption: texto abaixo das actions
    font_faces: CSS @font-face — se None, carrega do fonts/ do template
    """
    if font_faces is None:
        font_faces = load_fonts()

    total = len(slides)
    dots = "".join(
        f'<span class="dot{" active" if i == 0 else ""}"></span>'
        for i in range(total)
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
  html,body{{background:{BG_BLACK};min-height:100vh;display:flex;align-items:center;justify-content:center;padding:40px 20px;font-family:'Grift',sans-serif;color:{TEXT_DARK}}}

  .ig-frame{{width:420px;max-width:420px;background:#fff;border-radius:12px;box-shadow:0 24px 60px rgba(0,0,0,0.12);overflow:hidden}}
  .ig-header{{display:flex;align-items:center;justify-content:space-between;padding:12px 14px;border-bottom:1px solid #EFEFEF}}
  .ig-user{{display:flex;align-items:center;gap:10px}}
  .ig-avatar{{width:34px;height:34px;border-radius:50%;background:{BG_BLACK};display:flex;align-items:center;justify-content:center;color:{GOLD};font-family:'Alga';font-style:italic;font-weight:600;font-size:18px;border:2px solid #fff;box-shadow:0 0 0 2px {BG_BLACK}}}
  .ig-handle{{font-size:13px;font-weight:600;color:#262626;font-family:'Grift'}}
  .ig-sub{{font-size:11px;color:#8E8E8E;font-family:'Grift'}}
  .ig-more{{font-size:18px;color:#262626;letter-spacing:1px}}

  .carousel-viewport{{position:relative;width:420px;aspect-ratio:4/5;overflow:hidden;cursor:grab;user-select:none}}
  .carousel-viewport:active{{cursor:grabbing}}
  .carousel-track{{display:flex;width:100%;height:100%;transition:transform 350ms cubic-bezier(0.22,1,0.36,1);will-change:transform}}
  .slide{{flex:0 0 420px;width:420px;height:100%;position:relative;overflow:hidden}}

  .ig-dots{{display:flex;justify-content:center;gap:4px;padding:10px 0 4px;background:#fff}}
  .ig-dots .dot{{width:5px;height:5px;border-radius:50%;background:#C7C7C7}}
  .ig-dots .dot.active{{background:{BG_BLACK}}}
  .ig-actions{{display:flex;align-items:center;gap:14px;padding:6px 14px 2px;background:#fff}}
  .ig-actions .spacer{{flex:1}}
  .ig-actions svg{{color:#262626}}
  .ig-caption{{padding:4px 14px 12px;font-size:12px;line-height:1.4;color:#262626;background:#fff;font-family:'Grift'}}
  .ig-caption .handle{{font-weight:700}}
  .ig-caption .ts{{display:block;color:#8E8E8E;font-size:10px;text-transform:uppercase;letter-spacing:0.3px;margin-top:4px}}

  em{{font-style:italic}}
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
