"""
Carrossel RECONECTA — AD003 — "Agradeça quando o lead disser 'vou pensar'".
9 slides. Copy fiel ao briefing (sem paráfrases).
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


# ============================================================
# HELPER — slide de script de objeção (slides 3-7)
# Layout consistente: objeção como headline + card vermelho (errado) + card dourado (certo)
# ============================================================
def script_slide(*, numero, label_l, objecao, errado, porque, certo):
    """
    numero: número do slide (3-7)
    label_l: ex "Script 01"
    objecao: a fala do lead (string com aspas)
    errado: a resposta que perde
    porque: explicação curta de porque não funciona
    certo: a resposta que continua a conversa
    """
    return f"""
<div class="slide" style="background:{BG_BLACK};position:relative;">
  <div style="position:absolute;top:30px;left:34px;right:34px;">{masthead(label_l, f"0{numero}")}</div>
  <div style="position:absolute;top:30px;bottom:30px;left:34px;right:34px;display:flex;flex-direction:column;justify-content:center;gap:14px;">
    <div>
      <div style="font-family:'Alga';font-weight:600;font-size:80px;line-height:0.7;color:{ACCENT};margin-bottom:2px;">"</div>
      <h2 style="font-family:'Grift';font-weight:900;font-size:{SZ_SUB};line-height:1.05;letter-spacing:-0.3px;color:{TEXT_LIGHT};">
        {objecao}
      </h2>
    </div>

    <div style="background:rgba(201,37,45,0.07);border-left:2px solid {POP};border-radius:6px;padding:14px 16px;">
      <p style="font-family:'Grift';font-weight:900;font-size:{SZ_MICRO};letter-spacing:1.5px;text-transform:uppercase;color:{POP};margin-bottom:8px;">
        &times; Se quiser perder o lead
      </p>
      <p style="font-family:'Alga';font-weight:600;font-style:italic;font-size:{SZ_BODY};line-height:1.3;color:{IVORY};margin-bottom:10px;">
        &ldquo;{errado}&rdquo;
      </p>
      <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.45;color:rgba(237,227,206,0.78);">
        <strong style="color:rgba(237,227,206,0.95);">Porque não funciona:</strong> {porque}
      </p>
    </div>

    <div style="background:rgba(184,150,90,0.08);border-left:2px solid {GOLD};border-radius:6px;padding:14px 16px;">
      <p style="font-family:'Grift';font-weight:900;font-size:{SZ_MICRO};letter-spacing:1.5px;text-transform:uppercase;color:{GOLD};margin-bottom:8px;">
        &check; Se quiser continuar a conversa
      </p>
      <p style="font-family:'Alga';font-weight:600;font-style:italic;font-size:{SZ_BODY};line-height:1.3;color:{IVORY};">
        &ldquo;{certo}&rdquo;
      </p>
    </div>
  </div>
</div>
"""


# ============================================================
# SLIDE 1 — HERO
# ============================================================
slide1 = f"""
<div class="slide" style="background:{BG_BLACK};position:relative;overflow:hidden;">
  <img src="{hero_uri}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center top;display:block;" alt="">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg, rgba(15,5,5,0.5) 0%, rgba(15,5,5,0.12) 14%, rgba(15,5,5,0.03) 30%, rgba(15,5,5,0.12) 42%, rgba(15,5,5,0.38) 54%, rgba(15,5,5,0.7) 66%, rgba(15,5,5,0.92) 78%, rgba(15,5,5,1) 90%, rgba(15,5,5,1) 100%);"></div>
  <div style="position:absolute;top:30px;left:34px;right:34px;z-index:3;">
    {masthead("RECONECTA", "Edição 03")}
  </div>
  <div style="position:absolute;bottom:30px;left:34px;right:34px;z-index:3;">
    <div style="margin-bottom:14px;">{thin_line(GOLD, "52px")}</div>
    <h1 style="font-family:'Alga';font-weight:600;font-size:{SZ_HERO_SM};line-height:0.98;letter-spacing:-0.6px;color:{TEXT_LIGHT};margin-bottom:12px;">
      Agradeça quando o lead disser <em style="font-style:italic;color:{GOLD};">&ldquo;vou pensar.&rdquo;</em>
    </h1>
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_BODY};line-height:1.4;color:rgba(237,227,206,0.88);">
      Porque é ali que a venda finalmente começa.
    </p>
    <div style="display:flex;justify-content:flex-end;align-items:center;margin-top:14px;">{arrow(GOLD, 24)}</div>
  </div>
  <img src="{noise_uri}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0.6;mix-blend-mode:screen;pointer-events:none;z-index:2;" alt="">
</div>
"""


# ============================================================
# SLIDE 2 — INTRO / PROBLEMA
# ============================================================
slide2 = f"""
<div class="slide" style="background:{BG_BLACK};position:relative;">
  <div style="position:absolute;top:30px;left:34px;right:34px;">{masthead("A objeção", "02")}</div>
  <div style="position:absolute;top:30px;bottom:30px;left:34px;right:34px;display:flex;flex-direction:column;justify-content:center;gap:14px;">
    <div>
      <div style="font-family:'Alga';font-weight:600;font-size:80px;line-height:0.7;color:{ACCENT};margin-bottom:4px;">"</div>
      <h2 style="font-family:'Grift';font-weight:900;font-size:{SZ_TITLE};line-height:1;letter-spacing:-0.4px;color:{TEXT_LIGHT};margin-bottom:10px;">
        Objeção <em style="font-style:italic;color:{GOLD};">não é rejeição</em>.
      </h2>
      <p style="font-family:'Grift';font-weight:400;font-size:{SZ_BODY};line-height:1.4;color:rgba(237,227,206,0.88);">
        É um pedido de mais informação ou um sinal de que ainda não geramos valor suficiente.
      </p>
    </div>
    <div>
      {thin_line(GOLD, "38px")}
      <p style="font-family:'Grift';font-weight:400;font-size:{SZ_BODY};line-height:1.4;color:rgba(237,227,206,0.85);margin-top:12px;">
        Você perde o lead no momento da reação: quando ele questiona, sua ansiedade sobe, você tenta convencer, entrega a informação rápido demais e&hellip; perde o controle da conversa.
      </p>
    </div>
    <div style="background:rgba(184,150,90,0.08);border-left:2px solid {GOLD};border-radius:6px;padding:14px 16px;">
      <p style="font-family:'Alga';font-weight:600;font-style:italic;font-size:{SZ_BODY};line-height:1.3;color:{IVORY};">
        Toda objeção se resolve devolvendo a pergunta. Não é manipulação, é conduzir o foco de volta para o problema que trouxe o paciente até você.
      </p>
    </div>
    <div style="display:flex;align-items:center;justify-content:space-between;gap:10px;">
      <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.4;color:rgba(237,227,206,0.82);">
        Arraste para o lado e use os <strong style="color:{GOLD};">5 scripts</strong> que invertem objeções e salvam agendamentos.
      </p>
      {arrow(GOLD, 22)}
    </div>
  </div>
</div>
"""


# ============================================================
# SLIDES 3-7 — OS 5 SCRIPTS
# ============================================================
slide3 = script_slide(
    numero=3,
    label_l="Script 01",
    objecao='&ldquo;Quanto custa a consulta?&rdquo;',
    errado="A consulta custa R$200.",
    porque="Por que você vai passar a informação sobre o valor da consulta se você nem sabe se o que ele está buscando ele vai encontrar na consulta?",
    certo="Claro que posso te passar o valor da consulta. Antes, pra gente entender se a Dra vai conseguir te ajudar no seu caso, como você entende que a consulta vai te ajudar?",
)

slide4 = script_slide(
    numero=4,
    label_l="Script 02",
    objecao='&ldquo;Ah, é paga? Achei que fosse gratuita, vamos deixar para depois.&rdquo;',
    errado="É paga, mas o valor é abatido do procedimento.",
    porque="você tá negociando o preço antes de ter construído valor. Soa como desespero.",
    certo="Claro, sem problemas. Pra gente encerrar aqui também, como você entendeu que a consulta com a Dra vai te ajudar a resolver [problema]?",
)

slide5 = script_slide(
    numero=5,
    label_l="Script 03",
    objecao='&ldquo;Só queria uma ideia de preço mesmo.&rdquo;',
    errado="Os procedimentos começam a partir de R$ X.",
    porque="responder com um número tira totalmente o foco do valor real e coloca o paciente numa comparação de preços. A pessoa vai comparar com base em algo que ela não entende, e provavelmente vai embora sem nem saber se esse procedimento seria indicado no caso dela.",
    certo="Claro, posso te passar uma estimativa de valores. Antes, só pra gente entender se possivelmente a Dra. vai conseguir te ajudar no seu caso, o que exatamente te fez buscar esse tipo de procedimento agora?",
)

slide6 = script_slide(
    numero=6,
    label_l="Script 04",
    objecao='&ldquo;Vou pensar e qualquer coisa te aviso.&rdquo;',
    errado="Tudo bem, fico à disposição!",
    porque="essa frase encerra a conversa e transfere o controle para o lead, que provavelmente nunca mais vai voltar. Você perde a chance de entender o que ainda está impedindo a decisão.",
    certo="Claro! Pra gente encerrar aqui também — como você entendeu que a consulta com a Dra vai te ajudar a resolver [problema]?",
)

slide7 = script_slide(
    numero=7,
    label_l="Script 05",
    objecao='&ldquo;Vou ver com meu marido e te aviso.&rdquo;',
    errado="Ok, fico no aguardo!",
    porque="você transfere a responsabilidade da decisão para alguém que nem participou da conversa e que provavelmente não entende o que o lead realmente está sentindo.",
    certo="Claro, faz total sentido querer conversar com quem a gente confia. Posso te perguntar uma coisa? Você acha que ele não te apoiaria nessa decisão agora?",
)


# ============================================================
# SLIDE 8 — REVELAÇÃO DO PADRÃO
# ============================================================
slide8 = f"""
<div class="slide" style="background:{BG_BLACK};position:relative;">
  <div style="position:absolute;top:30px;left:34px;right:34px;">{masthead("O padrão", "08")}</div>
  <div style="position:absolute;top:30px;bottom:30px;left:34px;right:34px;display:flex;flex-direction:column;justify-content:center;gap:18px;">
    <div>
      <div style="margin-bottom:14px;">{thin_line(GOLD, "52px")}</div>
      <h2 style="font-family:'Alga';font-weight:600;font-size:{SZ_HERO_SM};line-height:0.98;letter-spacing:-0.5px;color:{TEXT_LIGHT};">
        Percebe o <em style="font-style:italic;color:{GOLD};">padrão</em>?
      </h2>
    </div>
    <div>
      <p style="font-family:'Grift';font-weight:400;font-size:{SZ_BODY};line-height:1.45;color:rgba(237,227,206,0.88);margin-bottom:14px;">
        Em toda objeção, a resposta que <strong style="color:{POP};">perde</strong> entrega informação.
      </p>
      <p style="font-family:'Grift';font-weight:400;font-size:{SZ_BODY};line-height:1.45;color:rgba(237,227,206,0.88);">
        A resposta que <strong style="color:{GOLD};">fecha</strong> devolve a pergunta e traz a conversa de volta pro problema dela.
      </p>
    </div>
    <div style="background:rgba(184,150,90,0.08);border-left:2px solid {GOLD};border-radius:6px;padding:16px 18px;">
      <p style="font-family:'Alga';font-weight:600;font-style:italic;font-size:{SZ_BODY};line-height:1.35;color:{IVORY};">
        Se você reagir com ansiedade, pressa ou justificativa, vai perder o lead. Mas se responder com curiosidade e direção, você reconquista a conversa e o agendamento.
      </p>
    </div>
  </div>
</div>
"""


# ============================================================
# SLIDE 9 — CTA FINAL
# ============================================================
slide9 = f"""
<div class="slide" style="background:{BG_BLACK};position:relative;display:flex;flex-direction:column;justify-content:space-between;padding:30px 34px;">
  {masthead("Próximo passo", "RECONECTA")}
  <div>
    <div style="margin-bottom:16px;">{thin_line(GOLD, "40px")}</div>
    <h2 style="font-family:'Alga';font-weight:600;font-size:{SZ_HERO_SM};line-height:0.98;letter-spacing:-0.5px;color:{TEXT_LIGHT};">
      Salva esse carrossel para aplicar <em style="font-style:italic;color:{GOLD};">já</em> no seu próximo atendimento.
    </h2>
  </div>
  <div style="background:{IVORY};border-radius:12px;padding:18px 20px;">
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_BODY};line-height:1.4;color:{TEXT_DARK};margin-bottom:16px;">
      E se você tem uma <strong>objeção que não apareceu aqui</strong>, a que mais trava sua conversão, deixa nos comentários que eu faço questão de te apoiar nessa condução.
    </p>
    <div style="display:inline-flex;align-items:center;gap:8px;padding:10px 18px;background:{BG_BLACK};border-radius:30px;">
      <span style="font-family:'Grift';font-weight:900;font-size:{SZ_MICRO};letter-spacing:1.5px;text-transform:uppercase;color:{GOLD};">Deixa nos comentários</span>
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
slides = [slide1, slide2, slide3, slide4, slide5, slide6, slide7, slide8, slide9]

caption = (
    "Agradeça quando o lead disser 'vou pensar'. Porque é ali que a venda finalmente começa. "
    "Salva pra aplicar no próximo atendimento."
)

html = render_carousel(slides, caption=caption, title="RECONECTA — Agradeça vou pensar")
(BASE / "carousel.html").write_text(html, encoding="utf-8")
print(f"OK — {len(slides)} slides escritos em carousel.html")
