"""
RECONECTA — módulo compartilhado pra carrosséis no formato 1080x1080 (ads).

Reusa paleta, tipografia, fontes e helpers do `reconecta_carousel.py` (formato feed
1080x1350), mas renderiza em viewport quadrado 420x420 (output 1080x1080).

Uso típico dentro de um build_ads.py na pasta do carrossel:

    import sys
    from pathlib import Path
    sys.path.insert(0, "/Users/saviomoraes/reconecta/carrosseis/_template")

    import importlib.util
    spec = importlib.util.spec_from_file_location("build_feed", Path(__file__).parent / "build.py")
    feed = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(feed)

    from ads_carousel import cta_slide, render_ads_html, export_ads_pngs

    slides = feed.slides[:-1] + [cta_slide()]  # troca último slide pelo CTA padrão
    html = render_ads_html(slides, title="...")
    export_ads_pngs(html, out_dir=..., filenames=[...])

Cada build_ads.py é self-contained pra rodar `python3 build_ads.py`.
"""
import asyncio
import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from reconecta_carousel import (  # noqa: E402
    BG_BLACK, BG_WINE, BG_BURGUNDY, ACCENT, IVORY, IVORY_DEEP,
    TEXT_DARK, TEXT_LIGHT, TEXT_MUTED, GOLD, POP,
    SZ_HERO, SZ_HERO_SM, SZ_TITLE_LG, SZ_TITLE, SZ_SUB, SZ_BODY, SZ_SMALL, SZ_LABEL, SZ_MICRO,
    arrow, thin_line, load_fonts,
)


# ============================================================
# DIMENSÕES DO VIEWPORT SQUARE
# ============================================================
VIEW_W = 420
VIEW_H = 420
SCALE = 1080 / 420  # 2.5714 — output 1080x1080


# ============================================================
# CTA SLIDE PADRÃO (último slide de TODO ads)
# Copy fixa: "Se quer saber mais do que está sendo feito e
# também quer ter 10-60 novos pacientes todo santo mês TOQUE NO BOTÃO"
# ============================================================
def cta_slide() -> str:
    return f"""
<div class="slide" style="background:{BG_BLACK};position:relative;display:flex;flex-direction:column;justify-content:space-between;padding:30px 34px;overflow:hidden;">

  <!-- Masthead -->
  <div style="display:flex;justify-content:space-between;align-items:center;">
    <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;text-transform:uppercase;color:rgba(237,227,206,0.55);">Próximo passo</span>
    <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;color:{GOLD};text-transform:uppercase;">RECONECTA</span>
  </div>

  <!-- Bloco central: lead + CTA -->
  <div>
    <div style="margin-bottom:16px;">{thin_line(GOLD, "48px")}</div>
    <p style="font-family:'Alga';font-weight:600;font-size:{SZ_SUB};line-height:1.18;color:{TEXT_LIGHT};margin-bottom:20px;">
      Se quer saber mais do que está sendo feito e também quer ter
      <em style="font-style:italic;color:{GOLD};">10-60 novos pacientes</em>
      todo santo mês&hellip;
    </p>

    <!-- Botão CTA -->
    <div style="background:{IVORY};border-radius:14px;padding:20px 22px;display:flex;align-items:center;justify-content:space-between;gap:14px;">
      <div>
        <p style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:2.5px;text-transform:uppercase;color:{ACCENT};margin-bottom:4px;">Aqui embaixo</p>
        <p style="font-family:'Alga';font-weight:600;font-style:italic;font-size:{SZ_HERO_SM};line-height:0.95;color:{TEXT_DARK};letter-spacing:-0.3px;">
          TOQUE NO <em style="color:{ACCENT};">BOTÃO</em>
        </p>
      </div>
      <div style="flex-shrink:0;">
        <svg width="48" height="48" viewBox="0 0 48 48" fill="none" style="display:block;">
          <circle cx="24" cy="24" r="22" fill="{ACCENT}"/>
          <path d="M18 14 L30 24 L18 34" stroke="{IVORY}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        </svg>
      </div>
    </div>
  </div>

  <!-- Handles rodapé -->
  <div style="display:flex;justify-content:space-between;align-items:center;font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:2.5px;text-transform:uppercase;color:rgba(237,227,206,0.55);">
    <span>@oleonardorosso</span>
    <span>@mentoriareconecta</span>
  </div>

</div>
"""


# ============================================================
# HTML SHELL — sem IG frame (ads só precisam do slide cru)
# ============================================================
def render_ads_html(slides: list, *, title: str = "RECONECTA ADS") -> str:
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
  html,body{{background:{BG_BLACK};min-height:100vh;display:flex;align-items:center;justify-content:center;padding:0;margin:0;font-family:'Grift',sans-serif;color:{TEXT_DARK};overflow:hidden}}

  .carousel-viewport{{position:relative;width:{VIEW_W}px;height:{VIEW_H}px;aspect-ratio:1/1;overflow:hidden;background:{BG_BLACK}}}
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
async def _export_ads_async(html: str, out_paths: list):
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": VIEW_W, "height": VIEW_H},
            device_scale_factor=SCALE,
        )
        await page.set_content(html, wait_until="networkidle")
        await page.wait_for_timeout(2500)  # aguarda fontes renderizarem

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
    """
    Renderiza o HTML e exporta cada slide como PNG 1080x1080 nos paths fornecidos.
    `out_paths` deve ter exatamente o mesmo tamanho que o número de slides no HTML.
    """
    asyncio.run(_export_ads_async(html, out_paths))
