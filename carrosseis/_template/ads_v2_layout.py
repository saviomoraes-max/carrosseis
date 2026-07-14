"""
RECONECTA — helpers de LAYOUT pra ads quadrados 1080x1080 (a partir da SEM21).

Reaproveita o sistema visual v2 (cores, tipografia, grãos) mas RE-ANCORA o conteúdo
pro canvas quadrado (1080 de altura, vs 1350 do feed). Isto é TRANSFORMAÇÃO, não
squeeze: o conteúdo é recomposto pro quadrado, nunca espremido num eixo só.

Diferenças vs feed:
- SEM footer_pill (fica fora do canvas quadrado)
- SEM info_bar / masthead "RECONECTA" (regra de ads v2)
- conteúdo centralizado vertical (ou space-between) num bloco flex
- hero e CTA continuam vindo de ads_v2 (hero_ads / cta_botao_ads)

Uso típico em build_ads.py:
    sys.path.insert(0, "/Users/saviomoraes/reconecta/carrosseis/_template")
    from ads_v2_layout import sq_content, audit_export
    from ads_v2 import hero_ads, cta_botao_ads, render_ads_html

    # importa o build.py do feed pra reaproveitar copy + componentes + imagens
    import importlib.util
    spec = importlib.util.spec_from_file_location("feed", BASE / "build.py")
    feed = importlib.util.module_from_spec(spec); spec.loader.exec_module(feed)

    slide2 = sq_content([feed._kicker("A Cena"), ...], gap=22)
    ...
    html = render_ads_html(slides, title="...")
    audit_export(html, out_paths)   # exporta + audita bbox de cada slide
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from reconecta_carousel_v2 import (  # noqa: E402
    px, grains_overlay,
    BG_DARK, BG_CREAM, TEXT_LIGHT, SZ_HANDLE,
    DEFAULT_AVATAR_URI, DEFAULT_VERIFIED_URI,
)
from ads_v2 import VIEW_W, VIEW_H, SCALE  # noqa: E402

HEADLINE_CREAM = "#f3deb9"


def sq_hero(
    image_uri: str | None,
    headline_html: str,
    subtitle: str = "",
    *,
    handle: str = "@oleonardorosso",
    img_h: int = 580,
    text_top: int = 560,
    object_position: str = "center 22%",
    headline_size: int = 48,
    headline_color: str = HEADLINE_CREAM,
    headline_ls: float = -2.6,
    headline_lh: float = 1.06,
    subtitle_size: int = 26,
    gap: int = 26,
    left: int = 48,
    width: int = 984,
    subtitle_width: int = 900,
    bg: str = BG_DARK,
) -> str:
    """HERO quadrado: imagem no TOPO + fade recuado + perfil/headline/subtitle embaixo
    sobre fundo escuro limpo. Espelha o hero preferido do feed (sem texto sobre o rosto),
    re-ancorado pro canvas 1080x1080. Cantos superiores VAZIOS (regra do slide 1)."""
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
    fade = (
        "linear-gradient(180deg,"
        "rgba(45,0,0,0) 0%,"
        "rgba(45,0,0,0) 46%,"
        "rgba(45,0,0,0.06) 56%,"
        "rgba(45,0,0,0.18) 64%,"
        "rgba(45,0,0,0.34) 72%,"
        "rgba(45,0,0,0.54) 80%,"
        "rgba(45,0,0,0.74) 88%,"
        "rgba(45,0,0,0.90) 94%,"
        f"{bg} 100%)"
    )
    subtitle_block = (
        f'<p style="font-family:\'Inter\';font-weight:500;font-size:{px(subtitle_size)};'
        f'color:{TEXT_LIGHT};line-height:1.38;letter-spacing:{px(-0.4)};margin:0;'
        f'width:{px(subtitle_width)};opacity:0.92;">{subtitle}</p>'
        if subtitle else ""
    )
    return f"""
<div class="slide" style="background:{bg};position:relative;overflow:hidden;">
  {layer}
  <div style="position:absolute;top:0;left:0;width:100%;height:{px(img_h)};background:{fade};z-index:2;"></div>
  {grains_overlay()}
  <div style="position:absolute;top:{px(text_top)};left:{px(left)};width:{px(width)};display:flex;flex-direction:column;gap:{px(gap)};z-index:5;">
    <div style="display:flex;gap:{px(18)};align-items:center;">
      <img src="{DEFAULT_AVATAR_URI}" style="width:{px(57)};height:{px(57)};border-radius:50%;object-fit:cover;display:block;" alt="">
      <p style="font-family:'Inter';font-weight:500;font-size:{SZ_HANDLE};color:{TEXT_LIGHT};letter-spacing:{px(-1.68)};margin:0;white-space:nowrap;">{handle}</p>
      <div style="width:{px(33)};height:{px(38)};overflow:hidden;position:relative;">
        <img src="{DEFAULT_VERIFIED_URI}" style="position:absolute;width:1031.62%;height:189.47%;left:-930.96%;top:-44.74%;max-width:none;display:block;" alt="">
      </div>
    </div>
    <p style="font-family:'Alga';font-weight:600;font-size:{px(headline_size)};color:{headline_color};line-height:{headline_lh};letter-spacing:{px(headline_ls)};margin:0;width:{px(width)};">{headline_html}</p>
    {subtitle_block}
  </div>
</div>
"""


def sq_content(
    blocks: list,
    *,
    gap: int = 24,
    bg: str = BG_DARK,
    margin: int = 48,
    valign: str = "center",   # "center" | "between" | "start"
    top: int = 96,
    height: int = 904,
    align_items: str = "stretch",
) -> str:
    """Slide de conteúdo quadrado 1080x1080.

    blocks: lista de strings HTML, empilhadas numa flex column.
    valign="center" → centraliza verticalmente (ideal pra texto).
    valign="between" → distribui no eixo (space-between) dentro de [top, top+height].
    valign="start" → ancora no topo.
    margin: margem horizontal em px-output (1080-coord). 48 = padrão.
    """
    inner = "".join(blocks)
    width = 1080 - 2 * margin
    if valign == "center":
        container = (
            f"position:absolute;top:50%;left:{px(margin)};transform:translateY(-50%);"
            f"width:{px(width)};display:flex;flex-direction:column;gap:{px(gap)};"
            f"align-items:{align_items};z-index:5;"
        )
    else:
        justify = "space-between" if valign == "between" else "flex-start"
        container = (
            f"position:absolute;top:{px(top)};left:{px(margin)};width:{px(width)};"
            f"height:{px(height)};display:flex;flex-direction:column;"
            f"justify-content:{justify};gap:{px(gap)};align-items:{align_items};z-index:5;"
        )
    return f"""
<div class="slide" style="background:{bg};position:relative;overflow:hidden;">
  {grains_overlay()}
  <div style="{container}">
    {inner}
  </div>
</div>
"""


def sq_hero_full(
    image_uri,
    headline_html,
    subtitle="",
    *,
    handle="@oleonardorosso",
    object_position="center 14%",
    headline_size=60,
    headline_color=HEADLINE_CREAM,
    headline_ls=None,
    headline_lh=1.05,
    subtitle_size=29,
    clean_until=50,
    bottom=66,
    gap=24,
    left=56,
    width=968,
    subtitle_width=920,
    bg=BG_DARK,
):
    """HERO quadrado FULL-BLEED: imagem cobre TODO o slide + fade de baixo pra cima
    (imagem limpa no topo, escuro sólido onde o texto fica) + handle/headline/subtitle
    ancorados pela BASE. Sem faixa morta de bordô (diferente do sq_hero, que põe a foto
    numa faixa no topo e deixa vazio embaixo). Cantos superiores VAZIOS.

    clean_until: % da altura em que a foto fica LIMPA (fade transparente) — ajuste pra
    ficar logo ABAIXO do queixo da mulher, pra o fade nunca tampar o rosto. A partir daí
    começa uma rampa LONGA e suave que vira escuro pro texto ler. Tune por imagem.
    object_position: enquadra a foto pra o rosto cair no terço SUPERIOR (zona limpa)."""
    if image_uri:
        layer = (f'<img src="{image_uri}" style="position:absolute;inset:0;width:100%;height:100%;'
                 f'object-fit:cover;object-position:{object_position};display:block;z-index:1;" alt="">')
    else:
        layer = (f'<div style="position:absolute;inset:0;background:linear-gradient(135deg,#3a0a0a,#2d0000);'
                 f'display:flex;align-items:center;justify-content:center;z-index:1;">'
                 f'<span style="font-family:\'Inter\';font-weight:700;font-size:{px(34)};'
                 f'color:rgba(245,245,245,0.32);letter-spacing:{px(2)};text-transform:uppercase;">'
                 f'coloque a imagem do hero</span></div>')
    if headline_ls is None:
        headline_ls = -0.04 * headline_size
    # Fade transparente até clean_until% (preserva o rosto), depois rampa LONGA e eased
    # até escuro sólido ~20% mais abaixo. Nada de degrau duro e nada de tampar o rosto.
    r, g, b = 45, 0, 0
    c = clean_until
    s = min(c + 22, 95)
    span = max(s - c, 1)
    ease = [(0.0, 0.0), (0.12, 0.02), (0.24, 0.06), (0.36, 0.12), (0.47, 0.21),
            (0.57, 0.32), (0.66, 0.45), (0.74, 0.58), (0.81, 0.70), (0.88, 0.82),
            (0.94, 0.92), (1.0, 0.99)]
    curve = [(0, 0), (c, 0)] + [(c + span * f, a) for f, a in ease] + [(100, 1)]
    fade = ("linear-gradient(180deg," +
            ",".join(f"rgba({r},{g},{b},{round(a, 3)}) {max(0, min(round(p, 1), 100))}%" for p, a in curve) + ")")
    _tsh = f"text-shadow:0 {px(2)} {px(18)} rgba(0,0,0,0.55);"
    sub = (f'<p style="font-family:\'Inter\';font-weight:500;font-size:{px(subtitle_size)};'
           f'color:{TEXT_LIGHT};line-height:1.36;letter-spacing:{px(-0.4)};margin:0;{_tsh}'
           f'width:{px(subtitle_width)};opacity:0.95;">{subtitle}</p>') if subtitle else ""
    return f"""
<div class="slide" style="background:{bg};position:relative;overflow:hidden;">
  {layer}
  <div style="position:absolute;inset:0;background:{fade};z-index:2;"></div>
  {grains_overlay()}
  <div style="position:absolute;left:{px(left)};width:{px(width)};bottom:{px(bottom)};display:flex;flex-direction:column;gap:{px(gap)};z-index:5;">
    <div style="display:flex;gap:{px(18)};align-items:center;">
      <img src="{DEFAULT_AVATAR_URI}" style="width:{px(57)};height:{px(57)};border-radius:50%;object-fit:cover;display:block;" alt="">
      <p style="font-family:'Inter';font-weight:500;font-size:{SZ_HANDLE};color:{TEXT_LIGHT};letter-spacing:{px(-1.68)};margin:0;white-space:nowrap;">{handle}</p>
      <div style="width:{px(33)};height:{px(38)};overflow:hidden;position:relative;">
        <img src="{DEFAULT_VERIFIED_URI}" style="position:absolute;width:1031.62%;height:189.47%;left:-930.96%;top:-44.74%;max-width:none;display:block;" alt="">
      </div>
    </div>
    <p style="font-family:'Alga';font-weight:600;font-size:{px(headline_size)};color:{headline_color};line-height:{headline_lh};letter-spacing:{px(headline_ls)};margin:0;{_tsh}width:{px(width)};">{headline_html}</p>
    {sub}
  </div>
</div>
"""


# ============================================================
# EXPORT + AUDITORIA DE BBOX
# Mede, por slide, a extensão (top/bottom/left/right) de todo o conteúdo
# e sinaliza elementos a <EDGE px da borda (risco de corte).
# ============================================================
_AUDIT_JS = """
(slideIndex) => {
  const slides = document.querySelectorAll('.slide');
  const slide = slides[slideIndex];
  const sr = slide.getBoundingClientRect();
  let minT=1e9,maxB=-1e9,minL=1e9,maxR=-1e9;
  const isBackdrop = (c, r) =>
    (r.width >= 0.9*sr.width && r.height >= 0.9*sr.height) || // grains, gradiente
    (c.tagName==='IMG' && r.width >= 0.92*sr.width);          // imagem hero full-bleed (bleed proposital)
  const walk = (el) => {
    for (const c of el.children) {
      const r = c.getBoundingClientRect();
      const cs = getComputedStyle(c);
      const visible = cs.display!=='none' && cs.visibility!=='hidden' &&
                      r.width>0.5 && r.height>0.5;
      // só conta elementos folha-ish ou com texto/img direto, e NÃO backdrops full-bleed
      const hasText = c.childNodes && [...c.childNodes].some(
        n => n.nodeType===3 && n.textContent.trim().length>0);
      const isLeaf = c.tagName==='IMG' || c.tagName==='SVG' || hasText; // ignora divs decorativos vazios (gradiente, réguas)
      if (visible && isLeaf && !isBackdrop(c, r)) {
        minT=Math.min(minT, r.top-sr.top);
        maxB=Math.max(maxB, r.bottom-sr.top);
        minL=Math.min(minL, r.left-sr.left);
        maxR=Math.max(maxR, r.right-sr.left);
      }
      if (c.children.length>0 && !isBackdrop(c, r)) walk(c);
    }
  };
  walk(slide);
  const S = sr.width; // viewport px (420)
  return {minT, maxB, minL, maxR, S};
}
"""


async def _audit_export_async(html: str, out_paths: list, edge: float):
    from playwright.async_api import async_playwright

    flags = []
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
            m = await page.evaluate(_AUDIT_JS, i)
            scale = VIEW_W  # 420
            # converte pra px-output (1080) pra leitura
            f = lambda v: round(v / scale * 1080)
            top, bot, left, right = f(m["minT"]), f(m["maxB"]), f(m["minL"]), f(m["maxR"])
            edge_out = round(edge / scale * 1080)
            issues = []
            if m["minT"] < edge: issues.append(f"TOP={top}")
            if m["maxB"] > scale - edge: issues.append(f"BOTTOM={bot}(>{1080-edge_out})")
            if m["minL"] < edge: issues.append(f"LEFT={left}")
            if m["maxR"] > scale - edge: issues.append(f"RIGHT={right}(>{1080-edge_out})")
            tag = ("  ⚠ " + " ".join(issues)) if issues else "  ✓"
            if issues:
                flags.append((i + 1, issues))
            print(f"  [{i+1}/{total}] bbox out: T{top} B{bot} L{left} R{right}{tag}")

            out_path = Path(out_path)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            await page.screenshot(
                path=str(out_path),
                clip={"x": 0, "y": 0, "width": VIEW_W, "height": VIEW_H},
            )
        await browser.close()
    if flags:
        print(f"  ‼ {len(flags)} slide(s) com risco de borda: " +
              ", ".join(f"#{n}" for n, _ in flags))
    else:
        print("  ✓ nenhum elemento dentro da zona de risco de borda")
    return flags


def audit_export(html: str, out_paths: list, *, edge: float = 14.0):
    """Exporta cada slide como PNG 1080x1080 E audita a bbox do conteúdo.

    `edge` é a zona de risco em px-VIEWPORT (420). 14px ≈ 36px no output 1080.
    Imprime, por slide, a extensão do conteúdo e flags de borda.
    Retorna lista de (slide_num, issues) com risco.
    """
    return asyncio.run(_audit_export_async(html, out_paths, edge))
