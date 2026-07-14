"""
RECONECTA — helper compartilhado pra ads quadrados 1080x1080.

Diferenças do feed (1080x1350):
- Viewport 420x420 → output 1080x1080
- SEM info_bar (masthead)
- SEM footer_pill
- CTA final padrão: "TOQUE NO BOTÃO" (sem handles do Instagram)
- Hero compacto: imagem reduzida pra ~50% do slide, fade smooth, copy embaixo

Uso típico em build_ads.py:

    import sys
    from pathlib import Path
    sys.path.insert(0, "/Users/saviomoraes/reconecta/carrosseis/_template")
    from reconecta_carousel_v2 import (
        px, image_uri, grains_overlay,
        BG_DARK, BG_CREAM, TEXT_LIGHT, TEXT_DARK, POP_HEADLINE, SZ_HANDLE,
        DEFAULT_AVATAR_URI, DEFAULT_VERIFIED_URI,
    )
    from ads_v2 import (
        hero_ads, cta_botao_ads, render_ads_html, export_ads_pngs,
        HEADLINE_CREAM, VIEW_W, VIEW_H, SCALE,
    )

    slide1 = hero_ads(hero_uri, headline_html="...", subtitle="...")
    slide_cta = cta_botao_ads(headline_html="...")
    slides = [slide1, ..., slide_cta]
    html = render_ads_html(slides, title="...")
    export_ads_pngs(html, out_paths)
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from reconecta_carousel_v2 import (  # noqa: E402
    px, load_fonts, grains_overlay,
    BG_DARK, BG_CREAM, BG_LIGHT, BG_ACCENT,
    TEXT_LIGHT, TEXT_DARK, POP_HEADLINE,
    SZ_HANDLE,
    DEFAULT_AVATAR_URI, DEFAULT_VERIFIED_URI,
)


VIEW_W = 420
VIEW_H = 420
SCALE = 1080 / 420  # 2.5714

HEADLINE_CREAM = "#f3deb9"


# ============================================================
# HERO ADS — composição editorial full-bleed
# - Imagem cobre 100% do slide (não 50-60% como antes)
# - Gradiente cinematográfico em 3 zonas:
#     • 0-45%   imagem limpa (foto respira)
#     • 45-70%  tint progressivo
#     • 70-100% bloco escuro pra legibilidade do texto
# - Texto bottom-anchored com hierarquia editorial:
#     • régua vermelha 60px × 2px (acento editorial)
#     • HEADLINE massivo (default 90px, line-height 0.98)
#     • subtitle como kicker
#     • perfil @ na base (chip discreto)
# - Cantos superiores VAZIOS (regra do hero — sem masthead).
# ============================================================
def hero_ads(
    hero_uri: str | None,
    *,
    headline_html: str,
    subtitle: str = "",
    object_position: str = "center 28%",
    headline_size: int = 90,
    subtitle_size: int = 28,
    headline_width: int = 1000,
    handle: str = "@oleonardorosso",
    bg: str = BG_DARK,
    headline_color: str = HEADLINE_CREAM,
    text_block_top: int = 620,
    rule_color: str = POP_HEADLINE,
    gradient_start: int = 45,  # % onde o gradiente começa
) -> str:
    """Slide 1 padrão. Foto FULL BLEED + gradiente cinematográfico + texto editorial.

    `text_block_top` controla onde o bloco de texto começa (Y em px output, 0-1080).
    Default 620 = ~57% da altura → headline sobre o terço inferior da foto.
    """
    if hero_uri:
        hero_layer = (
            f'<img src="{hero_uri}" style="position:absolute;inset:0;width:100%;'
            f'height:100%;object-fit:cover;object-position:{object_position};'
            f'display:block;z-index:1;" alt="">'
        )
    else:
        hero_layer = (
            f'<div style="position:absolute;inset:0;'
            f'background:linear-gradient(135deg,#3a0a0a,#2d0000);display:flex;'
            f'align-items:center;justify-content:center;z-index:1;">'
            f'<span style="font-family:\'Inter\';font-weight:700;font-size:{px(34)};'
            f'color:rgba(245,245,245,0.32);letter-spacing:{px(2)};text-transform:uppercase;">'
            f'coloque img/hero</span></div>'
        )

    # Gradiente cinematográfico — duas camadas pra realismo:
    # 1. Tint global suave pra unidade cromática (vinho)
    # 2. Vignette inferior pesado pra legibilidade do texto
    g0 = gradient_start
    g1 = g0 + 12
    g2 = g0 + 22
    g3 = g0 + 32
    g4 = g0 + 42
    g5 = g0 + 50
    fade = (
        "linear-gradient(180deg,"
        "rgba(45,0,0,0) 0%,"
        f"rgba(45,0,0,0) {g0}%,"
        f"rgba(45,0,0,0.05) {g1}%,"
        f"rgba(45,0,0,0.16) {g2}%,"
        f"rgba(45,0,0,0.36) {g3}%,"
        f"rgba(45,0,0,0.62) {g4}%,"
        f"rgba(45,0,0,0.86) {g5}%,"
        f"rgba(45,0,0,0.96) {min(g5+6,100)}%,"
        f"{bg} 100%)"
    )

    # Vignette sutil nas bordas verticais pra dar profundidade cinema
    vignette = (
        "radial-gradient(ellipse 80% 60% at 50% 35%, "
        "rgba(0,0,0,0) 60%, rgba(0,0,0,0.18) 100%)"
    )

    subtitle_block = (
        f'<p style="font-family:\'Inter\';font-weight:500;font-size:{px(subtitle_size)};'
        f'color:{TEXT_LIGHT};line-height:1.34;letter-spacing:{px(-0.3)};margin:0;'
        f'width:{px(min(headline_width, 980))};opacity:0.92;">{subtitle}</p>'
        if subtitle else ""
    )

    # Acento editorial: régua vermelha curta (60 × 2 px output)
    rule = (
        f'<div style="width:{px(60)};height:{px(3)};background:{rule_color};'
        f'border-radius:{px(2)};margin-bottom:{px(8)};"></div>'
    )

    # Perfil discreto no rodapé do slide
    profile_chip = (
        f'<div style="position:absolute;left:{px(40)};bottom:{px(44)};'
        f'display:flex;gap:{px(14)};align-items:center;z-index:6;">'
        f'<img src="{DEFAULT_AVATAR_URI}" style="width:{px(48)};height:{px(48)};'
        f'border-radius:50%;object-fit:cover;display:block;" alt="">'
        f'<p style="font-family:\'Inter\';font-weight:500;font-size:{px(26)};'
        f'color:{TEXT_LIGHT};letter-spacing:{px(-1.2)};margin:0;'
        f'white-space:nowrap;opacity:0.92;">{handle}</p>'
        f'<div style="width:{px(28)};height:{px(32)};overflow:hidden;position:relative;">'
        f'<img src="{DEFAULT_VERIFIED_URI}" style="position:absolute;'
        f'width:1031.62%;height:189.47%;left:-930.96%;top:-44.74%;'
        f'max-width:none;display:block;" alt=""></div>'
        f'</div>'
    )

    return f"""
<div class="slide" style="background:{bg};position:relative;overflow:hidden;">
  {hero_layer}
  <div style="position:absolute;inset:0;background:{fade};z-index:2;"></div>
  <div style="position:absolute;inset:0;background:{vignette};z-index:3;pointer-events:none;"></div>
  {grains_overlay()}
  <div style="position:absolute;top:{px(text_block_top)};left:{px(40)};right:{px(40)};display:flex;flex-direction:column;gap:{px(22)};z-index:5;">
    {rule}
    <p style="font-family:'Alga';font-weight:600;font-size:{px(headline_size)};color:{headline_color};line-height:0.98;letter-spacing:{px(-4.2)};margin:0;max-width:{px(headline_width)};">{headline_html}</p>
    {subtitle_block}
  </div>
  {profile_chip}
</div>
"""


# ============================================================
# CTA ADS — TOQUE NO BOTÃO (padrão de todo ad)
# Sem handles do Instagram. Sem footer.
# ============================================================
def cta_botao_ads(
    *,
    headline_html: str,
    bg: str = BG_DARK,
    headline_color: str = POP_HEADLINE,
    headline_size: int = 76,
    label_eyebrow: str = "Próximo passo",
    botao_color: str = POP_HEADLINE,
) -> str:
    """Slide CTA final padronizado. Headline + box TOQUE NO BOTÃO.

    `botao_color` colore só a palavra BOTÃO. Default = champagne (POP_HEADLINE);
    em fundo cream o champagne fica ilegível, então passe um vermelho escuro
    (ex: "#8a0a0a") pra contraste forte."""
    return f"""
<div class="slide" style="background:{bg};position:relative;overflow:hidden;">
  {grains_overlay()}
  <div style="position:absolute;top:50%;left:{px(38)};transform:translateY(-50%);width:{px(1004)};display:flex;flex-direction:column;gap:{px(52)};z-index:5;">
    <p style="font-family:'Inter';font-weight:700;font-size:{px(25)};color:{HEADLINE_CREAM};letter-spacing:{px(3.4)};text-transform:uppercase;margin:0;opacity:0.72;">{label_eyebrow}</p>
    <p style="font-family:'Alga';font-weight:600;font-size:{px(headline_size)};color:{headline_color};line-height:1.04;letter-spacing:{px(-3.4)};margin:0;">{headline_html}</p>
    <div style="background:{HEADLINE_CREAM};border-radius:{px(20)};padding:{px(30)} {px(34)};display:flex;align-items:center;justify-content:space-between;gap:{px(20)};">
      <div style="display:flex;flex-direction:column;gap:{px(8)};">
        <span style="font-family:'Inter';font-weight:700;font-size:{px(22)};letter-spacing:{px(2.8)};text-transform:uppercase;color:{BG_DARK};opacity:0.78;">Aqui embaixo</span>
        <span style="font-family:'Alga';font-weight:600;font-style:italic;font-size:{px(56)};line-height:0.95;color:{BG_DARK};letter-spacing:{px(-1.6)};">
          TOQUE NO <em style="color:{botao_color};font-style:italic;">BOTÃO</em>
        </span>
      </div>
      <svg viewBox="0 0 48 48" style="width:{px(72)};height:{px(72)};flex-shrink:0;display:block;">
        <circle cx="24" cy="24" r="22" fill="{POP_HEADLINE}"/>
        <path d="M18 14 L30 24 L18 34" stroke="{BG_DARK}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      </svg>
    </div>
  </div>
</div>
"""


# ============================================================
# HTML SHELL — viewport 420x420, sem IG frame
# ============================================================
def render_ads_html(slides: list, *, title: str = "RECONECTA ADS", bg: str = BG_DARK) -> str:
    font_faces = load_fonts()
    total = len(slides)
    slides_html = "".join(slides)
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
  {font_faces}
  *{{margin:0;padding:0;box-sizing:border-box}}
  html,body{{background:{bg};min-height:100vh;display:flex;align-items:center;justify-content:center;padding:0;margin:0;font-family:'Inter',sans-serif;color:{TEXT_LIGHT};overflow:hidden}}
  .carousel-viewport{{position:relative;width:{VIEW_W}px;height:{VIEW_H}px;aspect-ratio:1/1;overflow:hidden;background:{bg}}}
  .carousel-track{{display:flex;width:100%;height:100%;transition:none;will-change:transform}}
  .slide{{flex:0 0 {VIEW_W}px;width:{VIEW_W}px;height:{VIEW_H}px;position:relative;overflow:hidden}}
  em{{font-style:italic}}
</style>
</head>
<body>
<div class="carousel-viewport">
  <div class="carousel-track">
    {slides_html}
  </div>
</div>
<script>
(function(){{
  const track=document.querySelector('.carousel-track');
  const total={total};
  window.__goToSlide = (i)=>{{
    i=Math.max(0,Math.min(total-1,i));
    track.style.transform=`translateX(${{-i*{VIEW_W}}}px)`;
  }};
  window.__totalSlides = total;
  window.__goToSlide(0);
}})();
</script>
</body>
</html>
"""


# ============================================================
# EXPORT — playwright render a 1080x1080
# ============================================================
async def _export_async(html: str, out_paths: list):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": VIEW_W, "height": VIEW_H},
            device_scale_factor=SCALE,
        )
        await page.set_content(html, wait_until="networkidle")
        await page.wait_for_timeout(2500)
        total = len(out_paths)
        for i, out_path in enumerate(out_paths):
            await page.evaluate(f"window.__goToSlide({i})")
            await page.wait_for_timeout(300)
            out_path = Path(out_path)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            await page.screenshot(
                path=str(out_path),
                clip={"x": 0, "y": 0, "width": VIEW_W, "height": VIEW_H},
            )
            print(f"  [{i+1}/{total}] {out_path.name}")
        await browser.close()


def export_ads_pngs(html: str, out_paths: list):
    """Renderiza o HTML e exporta cada slide como PNG 1080x1080."""
    asyncio.run(_export_async(html, out_paths))
