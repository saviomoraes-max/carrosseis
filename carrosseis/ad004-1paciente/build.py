"""
Carrossel RECONECTA — AD004 — "1 paciente novo por dia sem gastar em tráfego".
7 slides. Aplica diretrizes de design padrão (hero fade smooth, tipografia generosa).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "_template"))
from reconecta_carousel import (
    BG_BLACK, BG_WINE, BG_BURGUNDY, ACCENT, IVORY, IVORY_DEEP,
    TEXT_DARK, TEXT_LIGHT, TEXT_MUTED, GOLD, POP,
    SZ_HERO, SZ_HERO_SM, SZ_TITLE_LG, SZ_TITLE, SZ_SUB, SZ_BODY, SZ_SMALL, SZ_LABEL, SZ_MICRO,
    arrow, thin_line, masthead, real_example_tag, divider_with_label, image_uri,
    render_carousel,
)

BASE = Path(__file__).parent
IMG = BASE / "img"

hero_uri = image_uri(IMG / "hero.jpg")
noise_uri = image_uri(IMG / "noise.png")
slide2_img = image_uri(IMG / "slide2.png")
slide4_img = image_uri(IMG / "slide4.png")
slide5_img = image_uri(IMG / "slide5.jpg")
slide6_img = image_uri(IMG / "slide6.png")


def real_tag_gold(text):
    """Tag 'EXEMPLO REAL · ...' gold pra dark slides."""
    return real_example_tag(text, color=GOLD)


def real_tag_burgundy(text):
    """Tag 'EXEMPLO REAL · ...' burgundy pra cream slides."""
    return real_example_tag(text, color=ACCENT)


# ============================================================
# SLIDE 1 — HERO (fade smooth full-bleed + noise)
# ============================================================
slide1 = f"""
<div class="slide" style="background:{BG_BLACK};position:relative;overflow:hidden;">
  <img src="{hero_uri}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center center;display:block;" alt="">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg, rgba(15,5,5,0.40) 0%, rgba(15,5,5,0.06) 22%, rgba(15,5,5,0.03) 42%, rgba(15,5,5,0.10) 56%, rgba(15,5,5,0.42) 64%, rgba(15,5,5,0.82) 70%, rgba(15,5,5,0.97) 76%, rgba(15,5,5,1) 82%, rgba(15,5,5,1) 100%);"></div>
  <div style="position:absolute;top:30px;left:34px;right:34px;z-index:3;">
    <div style="display:flex;justify-content:space-between;align-items:center;">
      <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;text-transform:uppercase;color:{POP};">RECONECTA</span>
      <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;color:{POP};text-transform:uppercase;">Edição 04</span>
    </div>
  </div>
  <div style="position:absolute;bottom:30px;left:34px;right:34px;z-index:3;">
    <div style="margin-bottom:14px;">{thin_line(POP, "52px")}</div>
    <h1 style="font-family:'Alga';font-weight:600;font-size:{SZ_TITLE};line-height:1.08;letter-spacing:-0.4px;color:{TEXT_LIGHT};margin-bottom:10px;">
      A gente mudou <em style="font-style:italic;color:{POP};">completamente</em> a forma de fazer anúncios e isso revelou por que a maioria das clínicas não cresce.
    </h1>
    <div style="display:flex;justify-content:flex-end;align-items:center;margin-top:14px;">{arrow(POP, 24)}</div>
  </div>
  <img src="{noise_uri}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0.6;mix-blend-mode:screen;pointer-events:none;z-index:2;" alt="">
</div>
"""


# ============================================================
# SLIDE 2 — CONTRASTE + DEPOIMENTO
# ============================================================
slide2 = f"""
<div class="slide" style="background:{BG_BLACK};position:relative;">
  <div style="position:absolute;top:30px;left:34px;right:34px;">{masthead("O contraste", "02")}</div>
  <div style="position:absolute;top:30px;bottom:30px;left:34px;right:34px;display:flex;flex-direction:column;justify-content:center;gap:16px;">
    <div>
      <div style="font-family:'Alga';font-weight:600;font-size:80px;line-height:0.7;color:{ACCENT};margin-bottom:4px;">"</div>
      <p style="font-family:'Grift';font-weight:900;font-size:{SZ_SUB};line-height:1.05;letter-spacing:-0.3px;color:{TEXT_LIGHT};margin-bottom:12px;">
        R$ 4 mil por mês para a <em style="font-style:italic;color:{GOLD};">agência</em> te entregar relatório bonito toda sexta, e a sua agenda continuar vazia.
      </p>
      <p style="font-family:'Grift';font-weight:400;font-size:{SZ_BODY};line-height:1.4;color:rgba(237,227,206,0.85);">
        Enquanto isso, tem doutora sem gestor, sem gerenciador <strong style="color:{GOLD};">faturando 100 mil/mês</strong>.
      </p>
    </div>
    <div>
      {real_tag_gold("Exemplo real · depoimento de aluna")}
      <div style="display:flex;justify-content:center;">
        <img src="{slide2_img}" style="max-width:100%;max-height:220px;width:auto;height:auto;display:block;border-radius:12px;box-shadow:0 8px 32px rgba(0,0,0,0.55), 0 0 0 1px rgba(237,227,206,0.08);" alt="Depoimento">
      </div>
    </div>
    <p style="font-family:'Alga';font-weight:600;font-style:italic;font-size:{SZ_BODY};line-height:1.3;color:{GOLD};">
      Mas como isso é possível?
    </p>
  </div>
</div>
"""


# ============================================================
# SLIDE 3 — TRÁFEGO AUTO-FINANCIADO (cream, matemática)
# ============================================================
slide3 = f"""
<div class="slide" style="background:{IVORY};position:relative;">
  <div style="position:absolute;top:30px;left:34px;right:34px;">{masthead("A matemática", "03", cream_bg=True)}</div>
  <div style="position:absolute;top:30px;bottom:30px;left:34px;right:34px;display:flex;flex-direction:column;justify-content:center;gap:16px;">
    <h2 style="font-family:'Grift';font-weight:900;font-size:{SZ_TITLE};line-height:1;letter-spacing:-0.4px;color:{TEXT_DARK};">
      O segredo do lucro na Harmonização é o <em style="font-style:italic;color:{ACCENT};">tráfego auto-financiado</em>.
    </h2>
    <div style="background:{BG_BLACK};border-radius:12px;padding:16px 18px;">
      <p style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:2.5px;text-transform:uppercase;color:{GOLD};margin-bottom:10px;">A matemática é simples e exata</p>
      <div style="display:flex;flex-direction:column;gap:6px;">
        <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.4;color:{IVORY};">
          <span style="color:{GOLD};">&bull;</span> Você investe <strong style="color:{GOLD};">R$ 200</strong> em anúncios.
        </p>
        <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.4;color:{IVORY};">
          <span style="color:{GOLD};">&bull;</span> Atrai um paciente que paga <strong style="color:{GOLD};">R$ 200</strong> na sua consulta.
        </p>
        <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.4;color:{IVORY};">
          <span style="color:{GOLD};">&bull;</span> Resultado: O custo para colocar o paciente na sua frente foi <strong style="color:{GOLD};">ZERO</strong>.
        </p>
      </div>
    </div>
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.4;color:{TEXT_DARK};opacity:0.85;">
      O lucro real acontece agora: você tem um paciente qualificado sentado no mocho para fechar um protocolo de <strong style="color:{ACCENT};">R$ 5k, R$ 10k ou R$ 20k</strong>, sem ter tirado um centavo do bolso para trazê&#8209;lo.
    </p>
    <div style="display:flex;align-items:center;justify-content:space-between;gap:10px;">
      <p style="font-family:'Alga';font-weight:600;font-style:italic;font-size:{SZ_SMALL};line-height:1.35;color:{ACCENT};">
        Como configurar sua máquina de agendamentos novos hoje mesmo
      </p>
      {arrow(ACCENT, 22)}
    </div>
  </div>
</div>
"""


# ============================================================
# SLIDE 4 — SUPER CASO + print IG
# ============================================================
slide4 = f"""
<div class="slide" style="background:{BG_BLACK};position:relative;">
  <div style="position:absolute;top:30px;left:34px;right:34px;">{masthead("O super caso", "04")}</div>
  <div style="position:absolute;top:30px;bottom:30px;left:34px;right:34px;display:flex;flex-direction:column;justify-content:center;gap:14px;">
    <div>
      <h2 style="font-family:'Grift';font-weight:900;font-size:{SZ_TITLE};line-height:1;letter-spacing:-0.4px;color:{TEXT_LIGHT};margin-bottom:10px;">
        Suba o seu melhor <em style="font-style:italic;color:{GOLD};">&ldquo;Antes e Depois&rdquo;</em> no feed.
      </h2>
      <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.4;color:rgba(237,227,206,0.85);margin-bottom:8px;">
        A verdade é que <strong style="color:{GOLD};">2 ou 3 casos bem apresentados</strong> podem carregar 90% do seu faturamento em tráfego, desde que você esqueça a técnica: Ninguém compra a marca do preenchedor, elas compram a confiança de que você resolve o problema delas.
      </p>
      <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.4;color:rgba(237,227,206,0.82);">
        A imagem certa segmenta o público melhor do que qualquer botão de interesse, atraindo quem pode pagar e afastando automaticamente quem só busca preço.
      </p>
    </div>
    <div>
      {real_tag_gold("Exemplo real · Super Caso no feed")}
      <div style="display:flex;justify-content:center;">
        <img src="{slide4_img}" style="max-width:100%;max-height:195px;width:auto;height:auto;display:block;border-radius:12px;box-shadow:0 8px 32px rgba(0,0,0,0.55), 0 0 0 1px rgba(237,227,206,0.08);" alt="Super caso IG">
      </div>
    </div>
    <div style="display:flex;align-items:center;justify-content:space-between;gap:10px;">
      <p style="font-family:'Alga';font-weight:600;font-style:italic;font-size:{SZ_SMALL};line-height:1.35;color:{GOLD};">
        Aperte os botões certos agora
      </p>
      {arrow(GOLD, 22)}
    </div>
  </div>
</div>
"""


# ============================================================
# SLIDE 5 — TURBINAR + print interface
# ============================================================
slide5 = f"""
<div class="slide" style="background:{BG_BLACK};position:relative;">
  <div style="position:absolute;top:30px;left:34px;right:34px;">{masthead("O turbinar", "05")}</div>
  <div style="position:absolute;top:30px;bottom:30px;left:34px;right:34px;display:flex;flex-direction:column;justify-content:center;gap:14px;">
    <div>
      <h2 style="font-family:'Grift';font-weight:900;font-size:{SZ_TITLE};line-height:1;letter-spacing:-0.4px;color:{TEXT_LIGHT};margin-bottom:10px;">
        Use o <em style="font-style:italic;color:{GOLD};">Turbinar</em> do jeito certo.
      </h2>
      <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.4;color:rgba(237,227,206,0.85);">
        Para negócio local, o Turbinar é mais rápido, dá menos trabalho e traz leads <strong style="color:{GOLD};">mais barato e qualificados</strong> que o Gerenciador.
      </p>
    </div>
    <div>
      {real_tag_gold("Interface · Instagram Turbinar")}
      <div>
        <img src="{slide5_img}" style="width:100%;height:auto;display:block;border-radius:12px;box-shadow:0 8px 32px rgba(0,0,0,0.55), 0 0 0 1px rgba(237,227,206,0.08);" alt="Print do impulsionar">
      </div>
    </div>
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.4;color:rgba(237,227,206,0.82);">
      Basta selecionar <strong style="color:{GOLD};">Visitas ao Perfil</strong> e usar um raio de localização curto (deixando mínimo 100 mil habitantes) para dominar sua região. Desative tudo que for &ldquo;Advantage&rdquo;.
    </p>
    <div style="display:flex;align-items:center;justify-content:space-between;gap:10px;">
      <p style="font-family:'Alga';font-weight:600;font-style:italic;font-size:{SZ_SMALL};line-height:1.35;color:{GOLD};">
        Acompanhe seus números apenas 1 vez na semana seguindo esse passo a passo
      </p>
      {arrow(GOLD, 22)}
    </div>
  </div>
</div>
"""


# ============================================================
# SLIDE 6 — NÚMEROS + DEPOIMENTO
# ============================================================
slide6 = f"""
<div class="slide" style="background:{BG_BLACK};position:relative;">
  <div style="position:absolute;top:30px;left:34px;right:34px;">{masthead("Os números", "06")}</div>
  <div style="position:absolute;top:30px;bottom:30px;left:34px;right:34px;display:flex;flex-direction:column;justify-content:center;gap:16px;">
    <div>
      <h2 style="font-family:'Grift';font-weight:900;font-size:{SZ_TITLE};line-height:1;letter-spacing:-0.4px;color:{TEXT_LIGHT};margin-bottom:10px;">
        Acompanhe toda semana: <em style="font-style:italic;color:{GOLD};">Investimento total</em> / Número de consultas pagas.
      </h2>
      <p style="font-family:'Grift';font-weight:400;font-size:{SZ_BODY};line-height:1.4;color:rgba(237,227,206,0.85);">
        A meta é pagar no máximo <strong style="color:{GOLD};">R$ 200 a R$ 500</strong> por consulta agendada. Se o tráfego se paga, você tem previsibilidade para investir mais e crescer sem medo.
      </p>
    </div>
    <div>
      {real_tag_gold("Exemplo real · resultado de aluna")}
      <div>
        <img src="{slide6_img}" style="width:100%;height:auto;display:block;border-radius:12px;box-shadow:0 8px 32px rgba(0,0,0,0.55), 0 0 0 1px rgba(237,227,206,0.08);" alt="Depoimento números">
      </div>
    </div>
    <div style="display:flex;align-items:center;justify-content:space-between;gap:10px;">
      <p style="font-family:'Alga';font-weight:600;font-style:italic;font-size:{SZ_BODY};line-height:1.3;color:{GOLD};">
        Quer o meu mapa completo?
      </p>
      {arrow(GOLD, 22)}
    </div>
  </div>
</div>
"""


# ============================================================
# SLIDE 7 — CTA FINAL (Comenta TURBINAR)
# ============================================================
slide7 = f"""
<div class="slide" style="background:{BG_BLACK};position:relative;display:flex;flex-direction:column;justify-content:space-between;padding:30px 34px;">
  {masthead("Próximo passo", "RECONECTA")}
  <div>
    <div style="margin-bottom:16px;">{thin_line(GOLD, "40px")}</div>
    <h2 style="font-family:'Alga';font-weight:600;font-size:{SZ_SUB};line-height:1.1;letter-spacing:-0.3px;color:{TEXT_LIGHT};">
      Eu preparei o <em style="font-style:italic;color:{GOLD};">passo a passo exato</em> para você rodar seu primeiro turbinar sozinha e buscar sua <em style="font-style:italic;color:{GOLD};">primeira consulta paga</em> ainda esta semana.
    </h2>
  </div>
  <div style="background:{IVORY};border-radius:12px;padding:18px 20px;">
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_BODY};line-height:1.35;color:{TEXT_DARK};margin-bottom:14px;">
      Comenta <strong>TURBINAR</strong> aqui embaixo que eu te mando o framework completo no seu direct.
    </p>
    <div style="display:inline-flex;align-items:center;gap:8px;padding:10px 18px;background:{BG_BLACK};border-radius:30px;">
      <span style="font-family:'Grift';font-weight:900;font-size:{SZ_MICRO};letter-spacing:1.5px;text-transform:uppercase;color:{GOLD};">Comenta TURBINAR</span>
      {arrow(GOLD, 18)}
    </div>
  </div>
  <div style="display:flex;justify-content:space-between;align-items:center;font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:2.5px;text-transform:uppercase;color:rgba(237,227,206,0.55);">
    <span>@oleonardorosso</span>
    <span>@mentoriareconecta</span>
  </div>
</div>
"""


# ============================================================
# RENDER
# ============================================================
slides = [slide1, slide2, slide3, slide4, slide5, slide6, slide7]

caption = (
    "Como ter 1 paciente novo por dia sem gastar 1 real de tráfego do próprio bolso. "
    "Comenta TURBINAR que te mando o framework completo no direct."
)

html = render_carousel(slides, caption=caption, title="RECONECTA — 1 paciente por dia")
(BASE / "carousel.html").write_text(html, encoding="utf-8")
print(f"OK — {len(slides)} slides escritos em carousel.html")
