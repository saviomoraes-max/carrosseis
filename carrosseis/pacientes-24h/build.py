"""
Carrossel RECONECTA — "Como transformar seguidores em pacientes em 24h".
Edição 02. 7 slides. Copy fiel ao briefing (sem paráfrases ou acréscimos).
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
wpp_uri = image_uri(IMG / "slide3.png")
noise_uri = image_uri(IMG / "noise.png")


# ============================================================
# SLIDE 1 — HERO
# Split editorial: foto no topo + bloco dark sólido embaixo com a headline.
# Garante legibilidade total do título.
# ============================================================
slide1 = f"""
<div class="slide" style="background:{BG_BLACK};display:flex;flex-direction:column;position:relative;">
  <div style="height:58%;position:relative;overflow:hidden;">
    <img src="{hero_uri}" style="width:100%;height:100%;object-fit:cover;object-position:center top;display:block;" alt="">
    <div style="position:absolute;inset:0;background:linear-gradient(180deg, rgba(15,5,5,0.55) 0%, rgba(15,5,5,0.15) 22%, rgba(15,5,5,0.05) 55%, rgba(15,5,5,0.75) 95%, rgba(15,5,5,1) 100%);"></div>
    <div style="position:absolute;top:30px;left:34px;right:34px;z-index:3;">
      {masthead("RECONECTA", "Edição 02")}
    </div>
  </div>
  <div style="flex:1;background:{BG_BLACK};padding:26px 34px 30px;display:flex;flex-direction:column;justify-content:space-between;">
    <div>
      <div style="margin-bottom:16px;">{thin_line(GOLD, "52px")}</div>
      <h1 style="font-family:'Alga';font-weight:600;font-size:{SZ_HERO_SM};line-height:0.98;letter-spacing:-0.6px;color:{TEXT_LIGHT};">
        Como transformar novos <em style="font-style:italic;color:{GOLD};">seguidores</em> em pacientes agendados em até 24 hrs.
      </h1>
    </div>
    <div style="display:flex;justify-content:flex-end;align-items:center;">{arrow(GOLD, 24)}</div>
  </div>
  <img src="{noise_uri}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0.6;mix-blend-mode:screen;pointer-events:none;z-index:2;" alt="">
</div>
"""


# ============================================================
# SLIDE 2 — A JANELA (dark)
# Copy exata: 2 blocos de texto.
# ============================================================
slide2 = f"""
<div class="slide" style="background:{BG_BLACK};display:flex;flex-direction:column;justify-content:space-between;padding:30px 34px;">
  {masthead("A janela", "02")}
  <div>
    <div style="font-family:'Alga';font-weight:600;font-size:100px;line-height:0.8;color:{ACCENT};margin-bottom:8px;">"</div>
    <h2 style="font-family:'Grift';font-weight:900;font-size:{SZ_TITLE};line-height:1.02;letter-spacing:-0.4px;color:{TEXT_LIGHT};margin-bottom:16px;">
      Ninguém segue ninguém <em style="font-style:italic;color:{GOLD};">por acaso</em>.
    </h2>
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.5;color:rgba(237,227,206,0.88);margin-bottom:12px;">
      Cada pessoa que te seguiu viu algo no seu perfil que tocou em algo que ela já sente.
    </p>
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.5;color:rgba(237,227,206,0.88);">
      Mas se você esperar ela chamar no direct, o interesse esfria em <strong style="color:{GOLD};">48 horas</strong>. Em menos de 7 dias, ela já esqueceu de você.
    </p>
  </div>
  <div style="display:flex;justify-content:flex-end;">{arrow(GOLD, 22)}</div>
</div>
"""


# ============================================================
# SLIDE 3 — PROVA REAL (dark + whatsapp screenshot)
# ============================================================
slide3 = f"""
<div class="slide" style="background:{BG_BLACK};position:relative;">
  <div style="position:absolute;top:30px;left:34px;right:34px;">{masthead("Prova real", "03")}</div>
  <div style="position:absolute;top:30px;bottom:30px;left:34px;right:34px;display:flex;flex-direction:column;justify-content:center;gap:22px;">
    <div>
      <h2 style="font-family:'Grift';font-weight:900;font-size:{SZ_TITLE};line-height:1.02;letter-spacing:-0.4px;color:{TEXT_LIGHT};margin-bottom:10px;">
        Abordar não é <em style="font-style:italic;color:{GOLD};">incomodar</em>.
      </h2>
      {thin_line(GOLD, "38px")}
      <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.48;color:rgba(237,227,206,0.85);margin-top:12px;margin-bottom:10px;">
        A crença de que você &ldquo;tá sendo chata&rdquo; é o que separa quem agenda
        <strong style="color:{IVORY};">mínimo 1 paciente por dia</strong> de quem fica esperando mensagem nova chegar.
      </p>
      <p style="font-family:'Alga';font-weight:600;font-style:italic;font-size:{SZ_SMALL};line-height:1.35;color:{GOLD};">
        E quem já entendeu isso está vivendo essa realidade aqui:
      </p>
    </div>
    <div style="background:{IVORY};border:1px solid rgba(184,150,90,0.3);border-radius:8px;padding:12px 14px;">
      <img src="{wpp_uri}" style="width:100%;height:auto;display:block;border-radius:4px;" alt="Conversa real">
    </div>
  </div>
</div>
"""


# ============================================================
# SLIDE 4 — A REGRA DE OURO (dark)
# ============================================================
slide4 = f"""
<div class="slide" style="background:{BG_BLACK};display:flex;flex-direction:column;justify-content:space-between;padding:30px 34px;">
  {masthead("A regra de ouro", "04")}
  <div>
    <h2 style="font-family:'Grift';font-weight:900;font-size:{SZ_TITLE};line-height:1;letter-spacing:-0.4px;color:{TEXT_LIGHT};margin-bottom:14px;">
      A primeira mensagem <em style="font-style:italic;color:{GOLD};">não é pra vender</em>.
    </h2>
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.48;color:rgba(237,227,206,0.88);margin-bottom:10px;">
      Não é pra agendar. Não é pra passar valor. Não é pra oferecer nada.
    </p>
    <p style="font-family:'Alga';font-weight:600;font-style:italic;font-size:{SZ_SUB};line-height:1.15;color:{IVORY};margin-bottom:12px;">
      O único objetivo é receber uma resposta.
    </p>
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.48;color:rgba(237,227,206,0.82);">
      Quando você escreve pra vender, a mensagem vem junto com o bafo de vendedor. Ele sente em 2 segundos e ignora. Quando você escreve pra conversar, ele responde. E é ali que tudo começa.
    </p>
  </div>
  <div>
    {thin_line("rgba(184,150,90,0.3)", "100%")}
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};color:{IVORY};margin-top:12px;line-height:1.4;">
      Faça isso para conseguir <strong style="color:{GOLD};">70% de respostas</strong> nas suas próximas abordagens. {arrow(GOLD, 20)}
    </p>
  </div>
</div>
"""


# ============================================================
# SLIDE 5 — TÉCNICA 01: PERFIL ABERTO (cream card)
# ============================================================
exemplos_abertos = [
    "Adorei seu colar nessa foto! Onde você comprou?",
    "Vi que você esteve em Campos do Jordão. Foi ao Capivari?",
    "Seu corte tá incrível. Onde você costuma cortar?",
]
bubbles_abertos = "".join(
    f"""<div style="background:rgba(107,15,15,0.08);border-left:2px solid {ACCENT};border-radius:6px;padding:9px 12px;">
          <p style="font-family:'Alga';font-weight:600;font-style:italic;font-size:{SZ_SMALL};color:{TEXT_DARK};line-height:1.25;">&ldquo;{ex}&rdquo;</p>
        </div>"""
    for ex in exemplos_abertos
)

slide5 = f"""
<div class="slide" style="background:{IVORY};position:relative;">
  <div style="position:absolute;top:30px;left:34px;right:34px;">{masthead("Técnica 01", "05", cream_bg=True)}</div>
  <div style="position:absolute;top:30px;bottom:30px;left:34px;right:34px;display:flex;flex-direction:column;justify-content:center;gap:26px;">
    <div>
      <p style="font-family:'Grift';font-weight:400;font-size:{SZ_LABEL};letter-spacing:2.5px;text-transform:uppercase;color:{ACCENT};margin-bottom:10px;">Se o perfil é aberto</p>
      <h2 style="font-family:'Grift';font-weight:900;font-size:{SZ_TITLE_LG};line-height:0.98;letter-spacing:-0.5px;color:{TEXT_DARK};margin-bottom:10px;">
        Elogio sincero <em style="font-style:italic;color:{ACCENT};">+</em> pergunta.
      </h2>
      <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.45;color:{TEXT_DARK};opacity:0.82;">
        Procura uma coisa real que te chamou atenção, e faça uma pergunta relacionada a isso.
      </p>
    </div>
    <div>
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
        <div style="width:20px;height:1px;background:{ACCENT};"></div>
        <p style="font-family:'Grift';font-weight:900;font-size:{SZ_MICRO};letter-spacing:2.5px;text-transform:uppercase;color:{ACCENT};">Exemplos reais</p>
      </div>
      <div style="display:flex;flex-direction:column;gap:8px;">{bubbles_abertos}</div>
    </div>
  </div>
</div>
"""


# ============================================================
# SLIDE 6 — TÉCNICA 02: PERFIL FECHADO (dark)
# ============================================================
exemplos_fechados = [
    "Você por aqui?",
    "Acho que vi você ontem no [local conhecido da cidade]. Era você mesmo?",
    "Sua cara é super familiar. A gente se conhece de onde?",
]
bubbles_fechados = "".join(
    f"""<div style="background:rgba(237,227,206,0.06);border-left:2px solid {GOLD};border-radius:6px;padding:9px 12px;">
          <p style="font-family:'Alga';font-weight:600;font-style:italic;font-size:{SZ_SMALL};color:{IVORY};line-height:1.25;">&ldquo;{ex}&rdquo;</p>
        </div>"""
    for ex in exemplos_fechados
)

slide6 = f"""
<div class="slide" style="background:{BG_BLACK};position:relative;">
  <div style="position:absolute;top:30px;left:34px;right:34px;">{masthead("Técnica 02", "06")}</div>
  <div style="position:absolute;top:30px;bottom:30px;left:34px;right:34px;display:flex;flex-direction:column;justify-content:center;gap:26px;">
    <div>
      <p style="font-family:'Grift';font-weight:400;font-size:{SZ_LABEL};letter-spacing:2.5px;text-transform:uppercase;color:{GOLD};margin-bottom:10px;">Se o perfil é fechado</p>
      <h2 style="font-family:'Grift';font-weight:900;font-size:{SZ_TITLE_LG};line-height:0.98;letter-spacing:-0.5px;color:{TEXT_LIGHT};margin-bottom:10px;">
        Abordagem intrigante <em style="font-style:italic;color:{GOLD};">+</em> curiosidade.
      </h2>
      <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.45;color:rgba(237,227,206,0.8);">
        Você não consegue observar nada. Então a abordagem vira uma pergunta que desperta curiosidade, sem ser invasiva.
      </p>
    </div>
    <div>
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
        <div style="width:20px;height:1px;background:{GOLD};"></div>
        <p style="font-family:'Grift';font-weight:900;font-size:{SZ_MICRO};letter-spacing:2.5px;text-transform:uppercase;color:{GOLD};">Exemplos reais</p>
      </div>
      <div style="display:flex;flex-direction:column;gap:8px;">{bubbles_fechados}</div>
    </div>
  </div>
</div>
"""


# ============================================================
# SLIDE 7 — CTA FINAL
# ============================================================
slide7 = f"""
<div class="slide" style="background:{BG_BLACK};display:flex;flex-direction:column;justify-content:space-between;padding:30px 34px;">
  {masthead("Próximo passo", "RECONECTA")}
  <div>
    <div style="margin-bottom:16px;">{thin_line(GOLD, "40px")}</div>
    <h2 style="font-family:'Alga';font-weight:600;font-size:{SZ_HERO_SM};line-height:0.98;letter-spacing:-0.5px;color:{TEXT_LIGHT};margin-bottom:14px;">
      A primeira mensagem é só o <em style="font-style:italic;color:{GOLD};">começo</em>.
    </h2>
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.45;color:rgba(237,227,206,0.82);">
      O que você faz depois que ela responde é o que transforma a conversa em paciente agendada.
    </p>
  </div>
  <div style="background:{IVORY};border-radius:12px;padding:18px 20px;">
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.4;color:{TEXT_DARK};margin-bottom:12px;">
      Existe um <strong>framework completo</strong> que vai desde a primeira mensagem até o agendamento confirmado no WhatsApp, com taxa de resposta de <strong>7 em cada 10</strong>.
    </p>
    <div style="display:inline-flex;align-items:center;gap:8px;padding:10px 18px;background:{BG_BLACK};border-radius:30px;margin-bottom:8px;">
      <span style="font-family:'Grift';font-weight:900;font-size:{SZ_MICRO};letter-spacing:1.5px;text-transform:uppercase;color:{GOLD};">Comenta FÁBRICA</span>
      {arrow(GOLD, 18)}
    </div>
    <p style="font-family:'Alga';font-weight:600;font-style:italic;font-size:{SZ_SMALL};color:{TEXT_DARK};opacity:0.75;">
      que eu te envio ele agora mesmo.
    </p>
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
    "Como transformar novos seguidores em pacientes agendados em até 24 hrs. "
    "Comenta FÁBRICA que eu te envio o framework completo."
)

html = render_carousel(slides, caption=caption, title="RECONECTA — Pacientes em 24h")
(BASE / "carousel.html").write_text(html, encoding="utf-8")
print(f"OK — {len(slides)} slides escritos em carousel.html")
