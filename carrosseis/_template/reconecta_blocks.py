# -*- coding: utf-8 -*-
"""
RECONECTA blocks — camada de blocos ricos sobre o reconecta_carousel_v2.

PADRÃO dos carrosséis novos (canon ATUAL: SEM24/AD005 "Cheiro de Vendedor",
validado pelo Sávio em 2026-06-11; canon anterior: SEM22/AD002 "Anuncio Mais Feio").
A ideia é NUNCA mais cair num "slide_F com bloco de texto chapado". Todo slide
deve compor headline (Alga cream com quebras manuais) + corpo em PARÁGRAFOS +
elementos visuais (cards, chips, kickers, ícones, punchline em Alga itálico).

Uso típico:
    from reconecta_blocks import *
    s1 = slide_hero(hero_uri, "Linha 1<br/>Linha 2", subtitle="...")
    s2 = slide_text([kicker("O QUE ACONTECEU"), para("..."), quote_card("..."), punch("...")])
    s3 = slide_text([headline("Título"), row([chip("a"), chip("b")]), para("...")])
    html = render_carousel([s1, s2, ...], caption="...")

Princípios visuais (do AD002):
- Headline: Alga 600, cor cream #f3deb9, quebras manuais com <br/>, tracking proporcional.
- Corpo: Inter 500, quebrado em parágrafos curtos (nunca um muro de texto).
- Ênfase: inline emph() champagne OU punchline punch() em Alga itálico champagne.
- Listas/enumerações da copy viram cards (num_card) ou chips (chip) — preserva as
  palavras, só dá tratamento visual.
- Imagens: full-bleed com fade ULTRA-SUAVE (15 stops) + leve zoom (scale 1.12-1.15).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from reconecta_carousel_v2 import (  # noqa
    px, image_uri, render_carousel,
    grains_overlay, info_bar, footer_pill, cta_pill,
    DEFAULT_AVATAR_URI, DEFAULT_VERIFIED_URI,
    BG_DARK, BG_CREAM, BG_LIGHT, BG_ACCENT, TEXT_LIGHT, TEXT_DARK,
    POP_HEADLINE, POP_FOOTER_CREAM,
    SZ_HANDLE, SZ_FOOTER, SZ_INFO,
    IMG_RADIUS, IMG_BORDER, FOOTER_RADIUS,
)

# ── paleta de apoio ──────────────────────────────────────────────────────────
HEADLINE_CREAM = "#f3deb9"            # cream quente das headlines (canon AD002)
MUTED = "rgba(245,245,245,0.60)"
CARD_BG = "rgba(243,222,185,0.05)"
CARD_BORDER = "rgba(243,222,185,0.16)"
_BG_RGB = (45, 0, 0)                  # = BG_DARK #2d0000


# ── fade ultra-suave (15 stops) pra imagem -> bordô ──────────────────────────
def smooth_fade(start=20, rgb=_BG_RGB):
    """Gradiente vertical eased de transparente (até `start`%) até o bordô sólido.
    start menor = escurece mais cedo (use ~8 quando o texto fica logo abaixo da foto)."""
    r, g, b = rgb
    curve = [(0, 0), (start, 0), (start + 8, 0.01), (start + 15, 0.03),
             (start + 22, 0.06), (start + 29, 0.11), (start + 35, 0.17),
             (start + 41, 0.25), (start + 47, 0.35), (start + 53, 0.47),
             (start + 59, 0.59), (start + 65, 0.71), (start + 71, 0.83),
             (start + 77, 0.93), (100, 1)]
    parts = [f"rgba({r},{g},{b},{a}) {min(p,100)}%" for p, a in curve]
    return "linear-gradient(180deg," + ",".join(parts) + ")"


# ── tipografia ───────────────────────────────────────────────────────────────
def headline(html, size=76, color=HEADLINE_CREAM, ls=None, lh=1.05, weight=600, width=980):
    """Alga cream. `html` aceita <br/> pra quebra manual. Tracking proporcional (~-4%)."""
    if ls is None:
        ls = -0.04 * size
    return (
        f"<p style=\"font-family:'Alga';font-weight:{weight};font-size:{px(size)};color:{color};"
        f"line-height:{lh};letter-spacing:{px(ls)};margin:0;width:{px(width)};\">{html}</p>"
    )


# PISO DE LEGIBILIDADE: corpo nunca abaixo de 33 (output 1080). Se a copy não couber,
# REESTRUTURE/divida o slide, NÃO encolha o texto. Sávio reclamou disso em todo post.
def para(html, size=33, color=TEXT_LIGHT, weight=500, lh=1.42, ls=-0.4, width=960):
    return (
        f"<p style=\"font-family:'Inter';font-weight:{weight};font-size:{px(size)};color:{color};"
        f"line-height:{lh};letter-spacing:{px(ls)};margin:0;width:{px(width)};\">{html}</p>"
    )


def punch(html, size=40, color=HEADLINE_CREAM, lh=1.18, ls=None, width=970):
    """Punchline em Alga itálico champagne — o destaque emocional do slide."""
    if ls is None:
        ls = -0.024 * size
    return (
        f"<p style=\"font-family:'Alga';font-weight:600;font-style:italic;font-size:{px(size)};"
        f"color:{color};line-height:{lh};letter-spacing:{px(ls)};margin:0;width:{px(width)};\">{html}</p>"
    )


def kicker(text, color=HEADLINE_CREAM):
    """Rótulo de seção em caixa-alta com tracking (acima do conteúdo)."""
    return (
        f"<p style=\"font-family:'Inter';font-weight:700;font-size:{px(22)};color:{color};"
        f"letter-spacing:{px(2.6)};text-transform:uppercase;margin:0;\">{text}</p>"
    )


def emph(text, color=HEADLINE_CREAM):
    """Ênfase inline (champagne, bold) dentro de um para()/punch()."""
    return f'<strong style="font-weight:700;color:{color};">{text}</strong>'


# ── ícones de linha (stroke champagne) ───────────────────────────────────────
def icon(d, size=30, color=HEADLINE_CREAM, sw=1.8):
    return (
        f'<svg viewBox="0 0 24 24" width="{px(size)}" height="{px(size)}" fill="none" '
        f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" '
        f'style="display:block;flex:0 0 auto;">{d}</svg>'
    )

ICONS = {
    "image": '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="8.5" cy="10" r="1.5"/><path d="M21 16l-5-5-9 9"/>',
    "doc": '<path d="M7 2.8h6.5L18 7v14a.8.8 0 0 1-.8.8H7a.8.8 0 0 1-.8-.8V3.6A.8.8 0 0 1 7 2.8z"/><path d="M13.5 2.8V7H18"/><line x1="9" y1="12.5" x2="15" y2="12.5"/><line x1="9" y1="15.8" x2="15" y2="15.8"/>',
    "gear": '<circle cx="12" cy="12" r="2.6"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09a1.65 1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09a1.65 1.65 0 0 0 1.51-1 1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
    "money": '<line x1="12" y1="1.8" x2="12" y2="22.2"/><path d="M17 5.5H9.7a3.4 3.4 0 0 0 0 6.8h4.6a3.4 3.4 0 0 1 0 6.8H6"/>',
    "eye_off": '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>',
    "check": '<path d="M20 6L9 17l-5-5"/>',
    "x": '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>',
    "mic": '<rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10a7 7 0 0 0 14 0"/><line x1="12" y1="17" x2="12" y2="22"/><line x1="8" y1="22" x2="16" y2="22"/>',
    "award": '<circle cx="12" cy="8" r="6"/><path d="M8.5 13.5L7 22l5-3 5 3-1.5-8.5"/>',
    "location": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "quote": '<path d="M7 7h4v4c0 3-2 5-4 5"/><path d="M14 7h4v4c0 3-2 5-4 5"/>',
    "arrow": '<path d="M5 12h14"/><path d="M12 5l7 7-7 7"/>',
    "heart": '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 1 0-7.8 7.8l1 1L12 21l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8z"/>',
    "star": '<path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 18.2 6.1 20.5l1.2-6.5L2.5 9.4l6.6-.9L12 2.5z"/>',
    "play": '<path d="M6 4.5v15l13-7.5-13-7.5z"/>',
    "eye": '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>',
    "sparkle": '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9L12 3z"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4"/>',
}


def ico(name, size=30, color=HEADLINE_CREAM, sw=1.8):
    return icon(ICONS.get(name, ""), size=size, color=color, sw=sw)


# ── containers visuais ───────────────────────────────────────────────────────
def row(items, gap=12):
    """Linha flex-wrap (chips, preços, etc.)."""
    return f'<div style="display:flex;flex-wrap:wrap;gap:{px(gap)};">' + "".join(items) + "</div>"


def chip(text, name=None, isize=26):
    """Pill com texto (e ícone opcional)."""
    ic = (ico(name, isize) if name else "")
    g = f"gap:{px(14)};" if name else ""
    return (
        f'<div style="display:inline-flex;align-items:center;{g}padding:{px(11)} {px(20)};'
        f"background:{CARD_BG};border:1px solid {CARD_BORDER};border-radius:{px(40)};\">{ic}"
        f"<span style=\"font-family:'Inter';font-weight:600;font-size:{px(26)};color:{TEXT_LIGHT};"
        f'letter-spacing:{px(-0.3)};">{text}</span></div>'
    )


def crossed_chip(text):
    """Chip com preço/termo riscado (line-through champagne)."""
    return (
        f'<div style="display:inline-flex;align-items:center;padding:{px(10)} {px(20)};'
        f'background:rgba(245,245,245,0.05);border:1px solid rgba(245,245,245,0.22);border-radius:{px(40)};">'
        f"<span style=\"font-family:'Inter';font-weight:700;font-size:{px(28)};color:rgba(245,245,245,0.55);"
        f'letter-spacing:{px(-0.3)};text-decoration:line-through;text-decoration-color:{POP_HEADLINE};'
        f'text-decoration-thickness:{px(3)};">{text}</span></div>'
    )


def num_card(num, label, desc):
    """Card numerado pra regras/passos (número Alga champagne + label + desc)."""
    return (
        f'<div style="display:flex;gap:{px(20)};padding:{px(18)} {px(24)};background:{CARD_BG};'
        f'border:1px solid {CARD_BORDER};border-radius:{px(16)};align-items:flex-start;">'
        f"<span style=\"font-family:'Alga';font-weight:600;font-size:{px(44)};color:{POP_HEADLINE};"
        f'line-height:0.95;min-width:{px(60)};letter-spacing:{px(-1.0)};">{num}</span>'
        f'<div style="display:flex;flex-direction:column;gap:{px(5)};flex:1;">'
        f"<span style=\"font-family:'Inter';font-weight:700;font-size:{px(28)};color:{HEADLINE_CREAM};"
        f'letter-spacing:{px(-0.3)};line-height:1.2;">{label}</span>'
        f"<span style=\"font-family:'Inter';font-weight:500;font-size:{px(25)};color:{TEXT_LIGHT};"
        f'line-height:1.42;letter-spacing:{px(-0.2)};">{desc}</span></div></div>'
    )


def icon_card(name, html, isize=34):
    """Card com ícone à esquerda + texto (aceita emph inline)."""
    return (
        f'<div style="display:flex;gap:{px(20)};align-items:flex-start;padding:{px(22)} {px(26)};'
        f'background:{CARD_BG};border:1px solid {CARD_BORDER};border-radius:{px(20)};">'
        f'<div style="margin-top:{px(4)};">{ico(name, isize)}</div>'
        f"<span style=\"font-family:'Inter';font-weight:500;font-size:{px(28)};color:{TEXT_LIGHT};"
        f'line-height:1.42;letter-spacing:{px(-0.3)};flex:1;">{html}</span></div>'
    )


def check_item(text, name="check", color=POP_HEADLINE, size=28):
    """Item de lista leve (sem caixa): ícone champagne + texto. Pra checklists/bullets."""
    return (
        f'<div style="display:flex;gap:{px(16)};align-items:flex-start;">'
        f'<div style="margin-top:{px(5)};">{ico(name, 28, color)}</div>'
        f"<span style=\"font-family:'Inter';font-weight:500;font-size:{px(size)};color:{TEXT_LIGHT};"
        f'line-height:1.4;letter-spacing:{px(-0.3)};flex:1;">{text}</span></div>'
    )


def check_list(items, name="check", gap=16):
    """Coluna de check_item com gap pequeno."""
    body = "".join(check_item(t, name=name) for t in items)
    return f'<div style="display:flex;flex-direction:column;gap:{px(gap)};width:100%;">{body}</div>'


def quote_card(text, size=34):
    """Citação destacada: borda esquerda champagne + Alga itálico cream."""
    return (
        f'<div style="padding:{px(24)} {px(32)};background:{CARD_BG};border:1px solid {CARD_BORDER};'
        f'border-left:{px(5)} solid {POP_HEADLINE};border-radius:{px(16)};">'
        f"<p style=\"font-family:'Alga';font-weight:500;font-style:italic;font-size:{px(size)};"
        f'color:{HEADLINE_CREAM};line-height:1.3;letter-spacing:{px(-0.6)};margin:0;">{text}</p></div>'
    )


def depo_card(path):
    """Screenshot de depoimento como card branco arredondado."""
    if path is None:
        return (
            f'<div style="width:{px(1004)};height:{px(240)};border-radius:{px(40)};border:{IMG_BORDER};'
            f'background:rgba(245,245,245,0.05);display:flex;align-items:center;justify-content:center;">'
            f"<span style=\"font-family:'Inter';font-weight:700;font-size:{px(22)};color:rgba(245,245,245,0.4);"
            f'text-transform:uppercase;letter-spacing:{px(1.5)};">depoimento</span></div>'
        )
    return (
        f'<div style="width:{px(1004)};border-radius:{px(40)};border:{IMG_BORDER};overflow:hidden;background:#f5f5f5;">'
        f'<img src="{image_uri(path)}" style="width:100%;display:block;" alt=""></div>'
    )


# ── blocos visuais ricos (slides SEM foto não podem ser texto chapado) ───────
def seclabel(text, name=None):
    """Rótulo de seção em pill com ícone (dá estrutura visual ao slide de texto)."""
    ic = f'<div style="display:flex;">{ico(name, 22, POP_HEADLINE)}</div>' if name else ""
    return (f'<div style="display:inline-flex;align-items:center;gap:{px(10)};padding:{px(9)} {px(18)};'
            f'background:{CARD_BG};border:1px solid {CARD_BORDER};border-radius:{px(40)};">{ic}'
            f"<span style=\"font-family:'Inter';font-weight:700;font-size:{px(20)};color:{HEADLINE_CREAM};"
            f'letter-spacing:{px(2.4)};text-transform:uppercase;">{text}</span></div>')


def bad_card(text):
    """Card negativo (X apagado) — o erro / o que NÃO funciona."""
    return (f'<div style="display:flex;gap:{px(16)};align-items:flex-start;padding:{px(18)} {px(24)};width:{px(940)};'
            f'background:rgba(245,245,245,0.03);border:1px solid rgba(245,245,245,0.12);border-radius:{px(16)};">'
            f'<div style="margin-top:{px(2)};">{ico("x", 28, "rgba(245,245,245,0.45)")}</div>'
            f"<span style=\"font-family:'Inter';font-weight:500;font-size:{px(32)};color:rgba(245,245,245,0.72);"
            f'line-height:1.4;letter-spacing:{px(-0.3)};flex:1;">{text}</span></div>')


def good_card(text):
    """Card positivo (✓ champagne, borda esquerda) — a virada / o que funciona."""
    return (f'<div style="display:flex;gap:{px(16)};align-items:flex-start;padding:{px(18)} {px(24)};width:{px(940)};'
            f'background:rgba(240,210,138,0.08);border:1px solid rgba(240,210,138,0.28);'
            f'border-left:{px(4)} solid {POP_HEADLINE};border-radius:{px(16)};">'
            f'<div style="margin-top:{px(2)};">{ico("check", 28, POP_HEADLINE)}</div>'
            f"<span style=\"font-family:'Inter';font-weight:600;font-size:{px(32)};color:{HEADLINE_CREAM};"
            f'line-height:1.4;letter-spacing:{px(-0.3)};flex:1;">{text}</span></div>')


def chip_hi(text):
    """Chip destacado champagne."""
    return (f'<div style="display:inline-flex;align-items:center;padding:{px(11)} {px(22)};'
            f'background:rgba(240,210,138,0.12);border:1px solid rgba(240,210,138,0.36);border-radius:{px(40)};">'
            f"<span style=\"font-family:'Inter';font-weight:700;font-size:{px(27)};color:{HEADLINE_CREAM};"
            f'letter-spacing:{px(-0.3)};">{text}</span></div>')


def from_to(bad, good):
    """Linha 'de X (riscado) -> para Y (destacado)'."""
    return (f'<div style="display:flex;align-items:center;gap:{px(14)};flex-wrap:wrap;">'
            + crossed_chip(bad) + f'<div style="display:flex;">{ico("arrow", 30, POP_HEADLINE)}</div>'
            + chip_hi(good) + '</div>')


def transition_pill(text):
    """Barra de virada/gancho (Alga itálico champagne com seta)."""
    return (f'<div style="display:inline-flex;align-items:center;gap:{px(16)};padding:{px(16)} {px(26)};'
            f'background:rgba(240,210,138,0.10);border:1px solid rgba(240,210,138,0.30);border-radius:{px(18)};">'
            f'<div style="display:flex;">{ico("arrow", 26, POP_HEADLINE)}</div>'
            f"<span style=\"font-family:'Alga';font-weight:600;font-style:italic;font-size:{px(34)};color:{POP_HEADLINE};"
            f'letter-spacing:{px(-0.6)};line-height:1.1;">{text}</span></div>')


def feat_card(name, label, desc):
    """Card com ícone + label cream em negrito + descrição (lentes/listas)."""
    return icon_card(name, f'<strong style="font-weight:700;color:{HEADLINE_CREAM};">'
                           f'{label}:</strong> {desc}', isize=32)


# ── slides ───────────────────────────────────────────────────────────────────
def slide_hero(image, headline_html, subtitle="", *, handle="@oleonardorosso",
               img_h=900, headline_size=82, headline_lh=1.06, headline_ls=None,
               subtitle_size=34, object_position="center 38%", scale=1.15,
               fade_start=20, text_top=None, content_bottom=1182, text_scrim=0.0):
    """Capa cinematográfica: foto full-bleed (zoom + fade ultra-suave) + perfil@ +
    headline cream (quebras manuais) + subtitle. Cantos superiores VAZIOS.

    POSIÇÃO (padrão): o bloco @+headline+subtitle é ANCORADO PELA BASE — a borda de
    baixo fica fixa em `content_bottom` (~66px acima do footer) e o bloco CRESCE PRA
    CIMA. Isso garante que NUNCA sobre uma faixa morta de bordô no terço inferior,
    seja a headline curta (2 linhas) ou longa (4-5 linhas). Headline grande por
    padrão (82). NÃO encolher a headline pra "caber"; quebre manualmente com <br/> e
    deixe ela crescer pra dentro da imagem.
    Compat: passar `text_top` explícito volta ao modo antigo (ancorado pelo topo).
    text_scrim (0..1): reforço de escurecimento na faixa do texto quando a imagem
    invade muito embaixo e atrapalha a leitura (ex. 0.7)."""
    if image:
        layer = (
            f'<div style="position:absolute;top:0;left:0;width:100%;height:{px(img_h)};overflow:hidden;z-index:1;">'
            f'<img src="{image}" style="width:100%;height:100%;object-fit:cover;object-position:{object_position};'
            f'transform:scale({scale});display:block;" alt=""></div>'
        )
    else:
        layer = (
            f'<div style="position:absolute;top:0;left:0;width:100%;height:{px(img_h)};'
            f'background:linear-gradient(135deg,#3a0a0a,#2d0000);display:flex;align-items:center;'
            f'justify-content:center;z-index:1;"><span style="font-family:\'Inter\';font-weight:700;'
            f"font-size:{px(34)};color:rgba(245,245,245,0.32);letter-spacing:{px(2)};"
            f'text-transform:uppercase;">coloque img/hero.jpg</span></div>'
        )
    sub = para(subtitle, size=subtitle_size, lh=1.34, ls=-0.5, width=940) if subtitle else ""
    _r, _g, _b = _BG_RGB
    scrim = ""
    if text_scrim:
        scrim = (
            f'<div style="position:absolute;inset:0;z-index:3;pointer-events:none;'
            f'background:linear-gradient(180deg,rgba({_r},{_g},{_b},0) 44%,'
            f'rgba({_r},{_g},{_b},{round(text_scrim*0.35,3)}) 56%,'
            f'rgba({_r},{_g},{_b},{round(text_scrim*0.72,3)}) 68%,'
            f'rgba({_r},{_g},{_b},{text_scrim}) 80%,'
            f'rgba({_r},{_g},{_b},{text_scrim}) 100%);"></div>'
        )
    return f"""
<div class="slide" style="background:{BG_DARK};position:relative;overflow:hidden;">
  {layer}
  <div style="position:absolute;top:0;left:0;width:100%;height:{px(img_h)};background:{smooth_fade(fade_start)};z-index:2;"></div>
  {scrim}
  {grains_overlay()}
  <div style="position:absolute;{(f'top:{px(text_top)};' if text_top is not None else f'bottom:{px(1350 - content_bottom)};')}left:{px(60)};width:{px(960)};display:flex;flex-direction:column;gap:{px(28)};z-index:5;">
    <div style="display:flex;gap:{px(18)};align-items:center;">
      <img src="{DEFAULT_AVATAR_URI}" style="width:{px(57)};height:{px(57)};border-radius:50%;object-fit:cover;display:block;" alt="">
      <p style="font-family:'Inter';font-weight:500;font-size:{SZ_HANDLE};color:{TEXT_LIGHT};letter-spacing:{px(-1.68)};margin:0;white-space:nowrap;">{handle}</p>
      <div style="width:{px(33)};height:{px(38)};overflow:hidden;position:relative;">
        <img src="{DEFAULT_VERIFIED_URI}" style="position:absolute;width:1031.62%;height:189.47%;left:-930.96%;top:-44.74%;max-width:none;display:block;" alt="">
      </div>
    </div>
    {headline(headline_html, size=headline_size, lh=headline_lh, ls=headline_ls, width=960)}
    {sub}
  </div>
  {footer_pill(TEXT_LIGHT, top=1246)}
</div>
"""


def bottom_fade(solid_at=62, rgb=_BG_RGB, ramp=30):
    """Fade de baixo pra cima com easing SIMÉTRICO (smoothstep): gentil no começo E
    no fim — sem 'degrau' ao entrar na imagem nem ao virar sólido.
    A imagem fica LIMPA acima de (solid_at - ramp)%; a rampa suave dura `ramp` pontos;
    bordô SÓLIDO a partir de solid_at%.
    IMPORTANTE pra não tampar o rosto: (solid_at - ramp) tem que cair ABAIXO do queixo
    da modelo. Se o fade estiver subindo no rosto, NÃO é só diminuir ramp — suba a foto
    (object_position maior) pra dar folga abaixo do rosto, e mantenha solid_at ~2-4pts
    acima da 1ª linha de texto."""
    r, g, b = rgb
    c = solid_at
    s = max(c - ramp, 0)
    span = (c - s) or 1
    ts = [0.0, 0.08, 0.16, 0.24, 0.32, 0.40, 0.48, 0.56, 0.64, 0.72, 0.80, 0.88, 0.94, 1.0]
    stops = [(0, 0.0), (s, 0.0)]
    for t in ts:
        a = 3 * t * t - 2 * t * t * t            # smoothstep: ease-in-out simétrico
        stops.append((s + t * span, round(a, 3)))
    stops += [(min(c, 100), 1.0), (100, 1.0)]
    parts = [f"rgba({r},{g},{b},{a}) {max(0,min(round(p,2),100))}%" for p, a in stops]
    return "linear-gradient(180deg," + ",".join(parts) + ")"


def slide_photo(image, children, *, object_position="center 38%", scale=1.15,
                solid_at=62, content_bottom=1185, width=984, gap=22, info=True,
                top_scrim=0.0, fade_ramp=30, shift_y=0):
    """PADRÃO foto: imagem de fundo full-bleed VISÍVEL no topo + fade de baixo pra cima +
    conteúdo concentrado no TERÇO INFERIOR (ancorado pela base, cresce pra cima).
    Calibrar solid_at pra fechar sólido ~40px ACIMA da 1ª linha de texto (nunca faixa
    de bordô chapado no meio). top_scrim (0..1): vinheta de 220px no topo pro masthead
    RECONECTA ler sobre área clara da foto (ex. 0.55) — canon SEM24/AD005.
    shift_y (px, espaço 1080): desloca a foto verticalmente ALÉM do limite do
    object_position (negativo = SOBE). Use quando object_position já está em 0%/100% e
    ainda precisa subir/descer a imagem. A área exposta embaixo fica sob o fade/texto
    (bordô), então não cria buraco visível."""
    if image:
        tf = f"translateY({px(shift_y)}) scale({scale})" if shift_y else f"scale({scale})"
        layer = (
            f'<img src="{image}" style="position:absolute;inset:0;width:100%;height:100%;'
            f'object-fit:cover;object-position:{object_position};transform:{tf};display:block;z-index:1;" alt="">'
        )
    else:
        layer = (
            f'<div style="position:absolute;inset:0;background:linear-gradient(135deg,#3a0a0a,#2d0000);'
            f'display:flex;align-items:flex-start;justify-content:center;padding-top:{px(120)};z-index:1;">'
            f"<span style=\"font-family:'Inter';font-weight:700;font-size:{px(32)};color:rgba(245,245,245,0.30);\">coloque a imagem</span></div>"
        )
    r, g, b = _BG_RGB
    topo = ""
    if top_scrim:
        topo = (f'<div style="position:absolute;top:0;left:0;width:100%;height:{px(220)};'
                f'background:linear-gradient(180deg,rgba({r},{g},{b},{top_scrim}) 0%,'
                f'rgba({r},{g},{b},{round(top_scrim * 0.55, 3)}) 45%,rgba({r},{g},{b},0) 100%);'
                f'z-index:2;"></div>')
    ib = info_bar(TEXT_LIGHT) if info else ""
    inner = "".join(children)
    return f"""
<div class="slide" style="background:{BG_DARK};position:relative;overflow:hidden;">
  {layer}
  <div style="position:absolute;inset:0;background:{bottom_fade(solid_at, ramp=fade_ramp)};z-index:2;"></div>
  {topo}
  {grains_overlay()}
  {ib}
  <div style="position:absolute;left:{px(48)};width:{px(width)};bottom:{px(1350 - content_bottom)};display:flex;flex-direction:column;gap:{px(gap)};align-items:flex-start;z-index:5;">{inner}</div>
  {footer_pill(TEXT_LIGHT, top=1246)}
</div>
"""


def slide_photo_text(image, children, *, scrim=0.60, object_position="center 35%",
                     scale=1.12, anchor="center", top=140, gap=24, width=984,
                     info=True, footer=True):
    """Foto de FUNDO full-bleed escurecida por um scrim (pro texto ler em cima dela).
    Use quando o slide tem bastante texto MAS você quer a imagem como pano de fundo
    (diferente do slide_photo, que põe a foto no topo e o texto numa faixa embaixo)."""
    if image:
        layer = (
            f'<img src="{image}" style="position:absolute;inset:0;width:100%;height:100%;'
            f'object-fit:cover;object-position:{object_position};transform:scale({scale});display:block;z-index:1;" alt="">'
        )
    else:
        layer = (
            f'<div style="position:absolute;inset:0;background:linear-gradient(135deg,#3a0a0a,#2d0000);z-index:1;"></div>'
        )
    r, g, b = _BG_RGB
    s2 = min(scrim + 0.18, 1)
    s3 = min(scrim + 0.34, 1)
    scrim_css = (
        f"linear-gradient(180deg,rgba({r},{g},{b},{scrim}) 0%,rgba({r},{g},{b},{scrim}) 34%,"
        f"rgba({r},{g},{b},{s2}) 60%,rgba({r},{g},{b},{s3}) 80%,{BG_DARK} 100%)"
    )
    ib = info_bar(TEXT_LIGHT) if info else ""
    foot = footer_pill(TEXT_LIGHT, top=1246) if footer else ""
    pos = "top:50%;transform:translateY(-50%);" if anchor == "center" else f"top:{px(top)};"
    inner = "".join(children)
    return f"""
<div class="slide" style="background:{BG_DARK};position:relative;overflow:hidden;">
  {layer}
  <div style="position:absolute;inset:0;background:{scrim_css};z-index:2;"></div>
  {grains_overlay()}
  {ib}
  <div style="position:absolute;{pos}left:{px(48)};width:{px(width)};display:flex;flex-direction:column;gap:{px(gap)};align-items:flex-start;z-index:5;">{inner}</div>
  {foot}
</div>
"""


def slide_text(children, *, anchor="center", top=130, gap=24, width=984, footer=True, info=True):
    """Slide só-texto: pilha de blocos (headline/kicker/para/cards/chips/punch).
    anchor='center' (default) centraliza na vertical; 'top' ancora em `top`."""
    inner = "".join(children)
    if anchor == "center":
        pos = "top:50%;transform:translateY(-50%);"
    else:
        pos = f"top:{px(top)};"
    ib = info_bar(TEXT_LIGHT) if info else ""
    foot = footer_pill(TEXT_LIGHT, top=1246) if footer else ""
    return f"""
<div class="slide" style="background:{BG_DARK};position:relative;overflow:hidden;">
  {grains_overlay()}
  {ib}
  <div style="position:absolute;{pos}left:{px(48)};width:{px(width)};display:flex;flex-direction:column;gap:{px(gap)};align-items:flex-start;z-index:5;">{inner}</div>
  {foot}
</div>
"""


def slide_cta(children, *, gap=28, width=984):
    """CTA final: pilha centralizada, SEM footer (use cta_pill dentro de children)."""
    return slide_text(children, anchor="center", gap=gap, width=width, footer=False)
