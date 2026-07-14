"""
Patterns de slide do carrossel RECONECTA — referência visual pronta pra copiar/adaptar.

Cada função abaixo retorna um string HTML de um tipo de slide. Não é uma API
rígida — é um "cardápio" de composições que funcionam. Quando for montar um
carrossel novo, olhe essas funções, copie o que couber no briefing e ajuste copy.

Os patterns cobrem:
  - hero_dark_bgimage()   → capa com foto de fundo + overlay + masthead + headline Alga
  - hero_dark_clean()     → capa sem foto, típica de abertura editorial
  - problem_dark()        → slide escuro com aspa decorativa + headline Grift + body + CTA
  - nome_cream_card()     → slide creme com fórmula em pill escuro + cards de exemplos reais
  - ajuste_dark_image()   → ajuste com foto (exemplo real) ancorada no rodapé
  - ajuste_cream()        → ajuste sobre fundo creme (tipo slide 7)
  - framework_3steps()    → 3 passos (i./ii./iii.) com quote Alga italic em cada
  - contraste_dark()      → "não precisa / você precisa" com cream card pro takeaway
  - cta_final_dark()      → fechamento: headline Alga + cream card com CTA button

Paleta:
  BG_BLACK      fundo escuro padrão
  IVORY         fundo claro / cards cremes
  ACCENT        burgundy brilhante (pop em fundo claro)
  GOLD          champagne (accent em fundo escuro)
  POP           crimson (uso extremo, uma palavra)

Tipografia (de SZ_HERO a SZ_MICRO em px() — já em CSS px pro viewport 420).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from reconecta_carousel import (
    BG_BLACK, BG_WINE, ACCENT, IVORY, TEXT_DARK, TEXT_LIGHT, TEXT_MUTED, GOLD, POP,
    SZ_HERO, SZ_HERO_SM, SZ_TITLE_LG, SZ_TITLE, SZ_SUB, SZ_BODY, SZ_SMALL, SZ_LABEL, SZ_MICRO,
    arrow, thin_line, masthead, real_example_tag, divider_with_label, image_uri,
)


# ============================================================
# 1) HERO COM FOTO DE FUNDO (tipo slide 1 do perfil-100k)
# ============================================================
def hero_dark_bgimage(*, image_path, label_l, label_r, tag, headline_alga, subtitle_grift):
    """
    image_path: caminho da imagem (jpg/png) — será embutida base64
    tag: small-caps label dourado acima do headline (ex: "Os 5 ajustes")
    headline_alga: HTML pra Alga SemiBold (use <em> pra itálicos)
    subtitle_grift: HTML pra subtítulo (use <strong style="color:{GOLD};"> pra ênfases)
    """
    uri = image_uri(image_path)
    return f"""
<div class="slide" style="background:{BG_BLACK};position:relative;">
  <img src="{uri}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;" alt="">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg, rgba(15,5,5,0.8) 0%, rgba(15,5,5,0.45) 15%, rgba(15,5,5,0.25) 40%, rgba(15,5,5,0.6) 62%, rgba(15,5,5,0.92) 82%, rgba(15,5,5,0.95) 100%);z-index:1;"></div>
  <div style="position:absolute;inset:0;background:radial-gradient(ellipse at center, transparent 30%, rgba(15,5,5,0.45) 100%);z-index:2;"></div>
  <div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:space-between;padding:30px 34px;z-index:3;">
    {masthead(label_l, label_r).replace('color:rgba(237,227,206,0.55)', f'color:{TEXT_LIGHT};text-shadow:0 1px 4px rgba(0,0,0,0.6)').replace(f'color:{GOLD}', f'color:{GOLD};text-shadow:0 1px 4px rgba(0,0,0,0.6)')}
    <div>
      <div style="margin-bottom:22px;">{thin_line(GOLD, "52px")}</div>
      <p style="font-family:'Grift';font-weight:400;font-size:{SZ_LABEL};letter-spacing:3px;text-transform:uppercase;color:{GOLD};margin-bottom:14px;">{tag}</p>
      <h1 style="font-family:'Alga';font-weight:600;font-size:{SZ_HERO};line-height:0.92;letter-spacing:-0.8px;color:{TEXT_LIGHT};margin-bottom:22px;text-shadow:0 2px 12px rgba(0,0,0,0.7);">{headline_alga}</h1>
      <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SUB};line-height:1.28;color:{TEXT_LIGHT};text-shadow:0 1px 6px rgba(0,0,0,0.7);margin-bottom:26px;">{subtitle_grift}</p>
      <div style="display:flex;justify-content:flex-end;">{arrow("rgba(237,227,206,0.75)", 22)}</div>
    </div>
  </div>
</div>
"""


# ============================================================
# 2) HERO LIMPO (sem foto)
# ============================================================
def hero_dark_clean(*, label_l, label_r, tag, headline_alga, subtitle_grift):
    return f"""
<div class="slide" style="background:{BG_BLACK};display:flex;flex-direction:column;justify-content:space-between;padding:30px 34px;">
  {masthead(label_l, label_r)}
  <div>
    <div style="margin-bottom:22px;">{thin_line(GOLD, "52px")}</div>
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_LABEL};letter-spacing:3px;text-transform:uppercase;color:{GOLD};margin-bottom:18px;">{tag}</p>
    <h1 style="font-family:'Alga';font-weight:600;font-size:{SZ_HERO};line-height:0.92;letter-spacing:-0.8px;color:{TEXT_LIGHT};margin-bottom:22px;">{headline_alga}</h1>
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SUB};line-height:1.28;color:rgba(237,227,206,0.78);">{subtitle_grift}</p>
  </div>
  <div style="display:flex;justify-content:flex-end;">{arrow("rgba(237,227,206,0.55)", 22)}</div>
</div>
"""


# ============================================================
# 3) PROBLEMA (dark com aspa decorativa)
# ============================================================
def problem_dark(*, label_l, label_r, headline_grift, body_grift, cta):
    """
    headline_grift: HTML com Grift Black, use <em style="font-style:italic;color:{GOLD};"> pra palavras-chave
    body_grift: HTML com Grift 400, pode usar <strong>
    cta: HTML curto — ex: "Os <strong>5 ajustes imediatos</strong> para mudar ainda hoje"
    """
    return f"""
<div class="slide" style="background:{BG_BLACK};display:flex;flex-direction:column;justify-content:space-between;padding:30px 34px;">
  {masthead(label_l, label_r)}
  <div>
    <div style="font-family:'Alga';font-weight:600;font-size:100px;line-height:0.8;color:{ACCENT};margin-bottom:6px;">"</div>
    <h2 style="font-family:'Grift';font-weight:900;font-size:{SZ_TITLE};line-height:1;letter-spacing:-0.4px;color:{TEXT_LIGHT};margin-bottom:16px;">{headline_grift}</h2>
    {thin_line(GOLD, "38px")}
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.45;color:rgba(237,227,206,0.82);margin-top:14px;">{body_grift}</p>
  </div>
  <div>
    {thin_line("rgba(184,150,90,0.3)", "100%")}
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};color:{IVORY};margin-top:14px;line-height:1.4;">{cta} {arrow(GOLD, 20)}</p>
  </div>
</div>
"""


# ============================================================
# 4) NOME / CREAM CARD COM FÓRMULA (tipo slide 3)
# ============================================================
def nome_cream_card(*, label_l, label_r, headline, subtitle, formula_label, formula, examples):
    """
    examples: lista de tuplas (handle, nome_completo) — cards evidenciados em burgundy
    """
    ex_html = "".join(
        f"""<div style="background:rgba(107,15,15,0.08);border-left:2px solid {ACCENT};border-radius:6px;padding:8px 12px;">
          <p style="font-family:'Grift';font-weight:900;font-size:{SZ_SMALL};color:{ACCENT};line-height:1.1;">{h}</p>
          <p style="font-family:'Alga';font-weight:600;font-size:{SZ_SMALL};color:{TEXT_DARK};line-height:1.15;">{n}</p>
        </div>"""
        for h, n in examples
    )
    return f"""
<div class="slide" style="background:{IVORY};display:flex;flex-direction:column;justify-content:space-between;padding:30px 34px;">
  {masthead(label_l, label_r, cream_bg=True)}
  <div>
    <h2 style="font-family:'Grift';font-weight:900;font-size:{SZ_TITLE_LG};line-height:0.98;letter-spacing:-0.5px;color:{TEXT_DARK};margin-bottom:14px;">{headline}</h2>
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.45;color:{TEXT_DARK};opacity:0.82;">{subtitle}</p>
  </div>
  <div style="background:{BG_BLACK};border-radius:12px;padding:18px 20px;">
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:2.5px;text-transform:uppercase;color:{GOLD};margin-bottom:8px;">{formula_label}</p>
    <p style="font-family:'Alga';font-weight:600;font-size:{SZ_SUB};color:{IVORY};line-height:1.15;">{formula}</p>
  </div>
  <div>
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
      <div style="width:20px;height:1px;background:{ACCENT};"></div>
      <p style="font-family:'Grift';font-weight:900;font-size:{SZ_MICRO};letter-spacing:2.5px;text-transform:uppercase;color:{ACCENT};">Exemplos reais no Instagram</p>
    </div>
    <div style="display:flex;flex-direction:column;gap:6px;">{ex_html}</div>
  </div>
</div>
"""


# ============================================================
# 5) AJUSTE COM IMAGEM (tipo slide 4 ou 5)
# Texto no topo + imagem com tag "EXEMPLO REAL" no rodapé
# ============================================================
def ajuste_dark_image(*, label_l, label_r, headline, subtitle, list_items, image_path, example_tag, cream_image_bg=False):
    """
    list_items: lista de (bold_text, plain_text) — renderiza como lista numerada romana
    example_tag: texto após "Exemplo real ·" (ex: "Perfil de harmonizadora")
    cream_image_bg: se True, image container em cream (pra screenshots dark do IG)
    """
    uri = image_uri(image_path)
    items_html = "".join(
        f'<div style="display:flex;gap:12px;padding:4px 0;">'
        f"<span style=\"color:{GOLD};font-family:'Alga';font-style:italic;min-width:20px;\">{chr(105) + 'i.' if idx > 0 else 'i.'}</span>"
        f"<span><strong style=\"font-weight:900;\">{b}</strong> {p}</span>"
        f"</div>"
        for idx, (b, p) in enumerate(list_items)
    )
    # fix: proper roman numerals
    romans = ["i.", "ii.", "iii.", "iv.", "v.", "vi.", "vii."]
    items_html = "".join(
        f'<div style="display:flex;gap:12px;padding:4px 0;">'
        f"<span style=\"color:{GOLD};font-family:'Alga';font-style:italic;min-width:20px;\">{romans[i]}</span>"
        f"<span><strong style=\"font-weight:900;\">{b}</strong> {p}</span>"
        f"</div>"
        for i, (b, p) in enumerate(list_items)
    )
    img_bg = IVORY if cream_image_bg else BG_WINE
    return f"""
<div class="slide" style="background:{BG_BLACK};display:flex;flex-direction:column;justify-content:space-between;padding:30px 34px;">
  {masthead(label_l, label_r)}
  <div>
    <h2 style="font-family:'Grift';font-weight:900;font-size:{SZ_TITLE};line-height:1;letter-spacing:-0.4px;color:{TEXT_LIGHT};margin-bottom:14px;">{headline}</h2>
    <p style="font-family:'Alga';font-weight:600;font-style:italic;font-size:{SZ_SMALL};color:{IVORY};line-height:1.4;">{subtitle}</p>
  </div>
  <div style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};color:{TEXT_LIGHT};line-height:1.45;">
    {items_html}
  </div>
  <div>
    {real_example_tag(example_tag)}
    <div style="background:{img_bg};border:1px solid rgba(184,150,90,0.3);border-radius:6px;padding:14px 16px;">
      <img src="{uri}" style="width:100%;height:auto;display:block;" alt="Exemplo real">
    </div>
  </div>
</div>
"""


# ============================================================
# 6) FRAMEWORK 3 STEPS (tipo slide 7 do perfil-100k)
# ============================================================
def framework_3steps(*, label_l, label_r, headline, body, framework_label, steps, exemplo_label, exemplo_quote, cream_bg=True):
    """
    steps: lista de (titulo_passo, quote_italica) — 3 itens
    """
    romans = ["i.", "ii.", "iii."]
    title_color = TEXT_DARK if cream_bg else TEXT_LIGHT
    accent_color = ACCENT if cream_bg else GOLD
    body_color = TEXT_DARK if cream_bg else TEXT_LIGHT
    body_opacity = "0.82" if cream_bg else "0.85"
    steps_html = "".join(
        f'<div style="display:flex;gap:10px;align-items:baseline;">'
        f"<span style=\"font-family:'Alga';font-style:italic;font-weight:600;font-size:{SZ_SUB};color:{accent_color};line-height:1;min-width:26px;\">{romans[i]}</span>"
        f'<div style="flex:1;">'
        f"<p style=\"font-family:'Grift';font-weight:900;font-size:{SZ_SMALL};color:{body_color};line-height:1.2;\">{t}</p>"
        f"<p style=\"font-family:'Alga';font-style:italic;font-weight:600;font-size:{SZ_SMALL};color:{body_color};opacity:0.75;line-height:1.3;\">{q}</p>"
        f"</div></div>"
        for i, (t, q) in enumerate(steps)
    )
    return f"""
<div class="slide" style="background:{IVORY if cream_bg else BG_BLACK};position:relative;">
  <div style="position:absolute;top:30px;left:34px;right:34px;display:flex;justify-content:space-between;align-items:center;z-index:2;">
    <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;text-transform:uppercase;color:{title_color};opacity:0.5;">{label_l}</span>
    <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;color:{accent_color};text-transform:uppercase;">{label_r}</span>
  </div>
  <div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;gap:14px;padding:30px 34px;">
    <div>
      <h2 style="font-family:'Grift';font-weight:900;font-size:{SZ_TITLE};line-height:1;letter-spacing:-0.4px;color:{title_color};margin-bottom:14px;">{headline}</h2>
      <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.4;color:{body_color};opacity:{body_opacity};">{body}</p>
    </div>
    <div>
      <p style="font-family:'Grift';font-weight:900;font-size:{SZ_MICRO};letter-spacing:2.5px;text-transform:uppercase;color:{accent_color};margin-bottom:10px;">{framework_label}</p>
      <div style="display:flex;flex-direction:column;gap:6px;">{steps_html}</div>
    </div>
    <div style="background:{BG_BLACK if cream_bg else BG_WINE};border-radius:10px;padding:14px 18px;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <div style="width:6px;height:6px;border-radius:50%;background:{GOLD};"></div>
        <p style="font-family:'Grift';font-weight:900;font-size:{SZ_MICRO};letter-spacing:2.5px;text-transform:uppercase;color:{GOLD};">{exemplo_label}</p>
      </div>
      <p style="font-family:'Alga';font-weight:600;font-style:italic;font-size:{SZ_MICRO};line-height:1.45;color:{IVORY};">{exemplo_quote}</p>
    </div>
  </div>
</div>
"""


# ============================================================
# 7) CONTRASTE "não precisa / você precisa" (tipo slide 8)
# ============================================================
def contraste_dark(*, label_l, label_r, supra_label, headline_alga, nao_precisa_body, precisa_takeaway, cta="Quer aplicar?"):
    return f"""
<div class="slide" style="background:{BG_BLACK};display:flex;flex-direction:column;justify-content:space-between;padding:30px 34px;">
  {masthead(label_l, label_r)}
  <div>
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_LABEL};letter-spacing:3px;text-transform:uppercase;color:{GOLD};margin-bottom:14px;">{supra_label}</p>
    <h2 style="font-family:'Alga';font-weight:600;font-size:{SZ_HERO_SM};line-height:0.95;letter-spacing:-0.5px;color:{TEXT_LIGHT};margin-bottom:20px;">{headline_alga}</h2>
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_BODY};line-height:1.45;color:rgba(237,227,206,0.82);">{nao_precisa_body}</p>
  </div>
  {divider_with_label("Você precisa")}
  <div style="background:{IVORY};border-radius:12px;padding:22px 24px;">
    <p style="font-family:'Alga';font-weight:600;font-style:italic;font-size:{SZ_SUB};line-height:1.25;color:{TEXT_DARK};">{precisa_takeaway}</p>
  </div>
  <div style="text-align:right;">
    <span style="font-family:'Alga';font-style:italic;font-weight:600;font-size:{SZ_SMALL};color:{GOLD};">{cta} {arrow(GOLD, 18)}</span>
  </div>
</div>
"""


# ============================================================
# 8) CTA FINAL (tipo slide 9)
# ============================================================
def cta_final_dark(*, label_l, label_r, headline_alga, cta_label, cta_body, button_text, handles):
    """
    headline_alga: ex "Faz essas <em>alterações</em> e me conta como foi."
    handles: tupla (left, right) — ex ("@oleonardorosso", "@mentoriareconecta")
    """
    return f"""
<div class="slide" style="background:{BG_BLACK};display:flex;flex-direction:column;justify-content:space-between;padding:30px 34px;">
  {masthead(label_l, label_r)}
  <div>
    <div style="margin-bottom:18px;">{thin_line(GOLD, "40px")}</div>
    <h2 style="font-family:'Alga';font-weight:600;font-size:{SZ_HERO_SM};line-height:0.95;letter-spacing:-0.4px;color:{TEXT_LIGHT};">{headline_alga}</h2>
  </div>
  <div style="background:{IVORY};border-radius:12px;padding:20px 22px;">
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:2.5px;text-transform:uppercase;color:{ACCENT};margin-bottom:10px;">{cta_label}</p>
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.4;color:{TEXT_DARK};margin-bottom:14px;">{cta_body}</p>
    <div style="display:inline-flex;align-items:center;gap:8px;padding:10px 18px;background:{BG_BLACK};border-radius:30px;">
      <span style="font-family:'Grift';font-weight:900;font-size:{SZ_MICRO};letter-spacing:1.5px;text-transform:uppercase;color:{GOLD};">{button_text}</span>
      {arrow(GOLD, 18)}
    </div>
  </div>
  <div style="display:flex;justify-content:space-between;align-items:center;font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:2.5px;text-transform:uppercase;color:rgba(237,227,206,0.55);">
    <span>{handles[0]}</span>
    <span>{handles[1]}</span>
  </div>
</div>
"""
