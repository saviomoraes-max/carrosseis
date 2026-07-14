"""
Carrossel RECONECTA — editorial premium minimalist.
Paleta: near-black + ivory + gold accent. Fontes: Alga SemiBold + Grift Black/Regular.
Copy: fiel ao texto original do usuario, com correcoes ortograficas aplicadas
(acentuacao: voce, nao, atrair, Quanto, diagnostico, clinica, nomes complexos).

Layout: cada slide distribui elementos com flex space-between em 3 zonas
(topo-masthead / meio-headline+corpo / rodape-CTA) para evitar espaco morto.
"""
import base64
from pathlib import Path

BASE = Path(__file__).parent
IMG_DIR = BASE / "img"
FONT_DIR = BASE / "fonts"
OUT = BASE / "carousel.html"


def data_uri(path: Path, mime: str) -> str:
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"


def font_face(family: str, weight: int, style: str, filename: str) -> str:
    path = FONT_DIR / filename
    ext = filename.split(".")[-1].lower()
    mime = "font/otf" if ext == "otf" else "font/ttf"
    fmt = "opentype" if ext == "otf" else "truetype"
    uri = data_uri(path, mime)
    return (
        f"@font-face{{font-family:'{family}';font-weight:{weight};"
        f"font-style:{style};src:url({uri}) format('{fmt}');}}"
    )


font_faces = "".join(
    [
        font_face("Alga", 600, "normal", "Alga-SemiBold.otf"),
        font_face("Grift", 900, "normal", "Grift-Black.ttf"),
        font_face("Grift", 900, "italic", "Grift-BlackItalic.ttf"),
        font_face("Grift", 400, "normal", "Grift-Regular.ttf"),
        font_face("Grift", 400, "italic", "Grift-Italic.ttf"),
    ]
)

bio_uri = data_uri(IMG_DIR / "bio.png", "image/png")
dest_uri = data_uri(IMG_DIR / "destaques.png", "image/png")
fixa_uri = data_uri(IMG_DIR / "fixados.png", "image/png")
hero_uri = data_uri(IMG_DIR / "hero.jpg", "image/jpeg")

# === Paleta editorial luxury ===
BG_BLACK = "#0F0505"
BG_WINE = "#1A0808"
ACCENT = "#6B0F0F"
IVORY = "#EDE3CE"
TEXT_DARK = "#1A0F0A"
TEXT_LIGHT = "#EDE3CE"
TEXT_MUTED = "#8A7F6D"
GOLD = "#B8965A"

TOTAL = 9
S = 2.5714

def px(output_px: int) -> str:
    return f"{round(output_px / S, 1)}px"


SZ_HERO = px(120)
SZ_HERO_SM = px(96)
SZ_TITLE = px(60)
SZ_TITLE_LG = px(72)
SZ_SUB = px(44)
SZ_BODY = px(32)
SZ_SMALL = px(26)
SZ_LABEL = px(20)
SZ_MICRO = px(16)


def arrow(color: str, size: int = 22) -> str:
    return (
        f'<svg width="{size}" height="{int(size*0.42)}" viewBox="0 0 40 14" '
        f'style="display:inline-block;vertical-align:middle;margin-left:8px;">'
        f'<path d="M1 7 L36 7 M30 2 L37 7 L30 12" stroke="{color}" '
        f'stroke-width="1.2" fill="none" stroke-linecap="round"/></svg>'
    )


def thin_line(color: str = GOLD, width: str = "40px") -> str:
    return f'<div style="width:{width};height:1px;background:{color};"></div>'


def masthead(left: str, right: str, left_color: str = None, right_color: str = None) -> str:
    lc = left_color or "rgba(237,227,206,0.55)"
    rc = right_color or GOLD
    return f"""
    <div style="position:absolute;top:30px;left:34px;right:34px;display:flex;justify-content:space-between;align-items:center;">
      <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;text-transform:uppercase;color:{lc};">{left}</span>
      <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;color:{rc};text-transform:uppercase;">{right}</span>
    </div>
    """


# ============================================================
# SLIDE 1 — HERO
# Copy: "Os 5 ajustes no seu perfil que separam quem fatura
#       15k de quem fatura 100k mensais."
# ============================================================
slide1 = f"""
<div class="slide" style="background:{BG_BLACK};position:relative;">

  <!-- Foto de fundo -->
  <img src="{hero_uri}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;" alt="">

  <!-- Overlay escuro: topo dim para masthead, meio claro para a foto respirar, rodape escuro para o hero text. -->
  <div style="position:absolute;inset:0;background:linear-gradient(180deg, rgba(15,5,5,0.8) 0%, rgba(15,5,5,0.45) 15%, rgba(15,5,5,0.25) 40%, rgba(15,5,5,0.6) 62%, rgba(15,5,5,0.92) 82%, rgba(15,5,5,0.95) 100%);z-index:1;"></div>

  <!-- Vinheta sutil nas bordas -->
  <div style="position:absolute;inset:0;background:radial-gradient(ellipse at center, transparent 30%, rgba(15,5,5,0.45) 100%);z-index:2;"></div>

  <!-- Conteúdo: masthead no topo, hero+arrow agrupados no rodapé -->
  <div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:space-between;padding:30px 34px;z-index:3;">

    <div style="display:flex;justify-content:space-between;align-items:center;">
      <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;text-transform:uppercase;color:{TEXT_LIGHT};text-shadow:0 1px 4px rgba(0,0,0,0.6);">RECONECTA</span>
      <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;color:{GOLD};text-transform:uppercase;text-shadow:0 1px 4px rgba(0,0,0,0.6);">Edição 01</span>
    </div>

    <!-- Grupo inferior: hero + arrow (puxados pra baixo) -->
    <div>
      <div style="margin-bottom:22px;">{thin_line(GOLD, "52px")}</div>
      <h1 style="font-family:'Alga';font-weight:600;font-size:{SZ_HERO};line-height:0.92;letter-spacing:-0.8px;color:{TEXT_LIGHT};margin-bottom:22px;text-shadow:0 2px 12px rgba(0,0,0,0.7);">
        Os <em style="font-style:italic;">5 ajustes</em><br>no seu <em style="font-style:italic;">perfil.</em>
      </h1>
      <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SUB};line-height:1.28;color:{TEXT_LIGHT};text-shadow:0 1px 6px rgba(0,0,0,0.7);margin-bottom:26px;">
        Que separam quem fatura <strong style="font-weight:900;color:{GOLD};">R$15k</strong> de quem fatura <strong style="font-weight:900;color:{GOLD};">R$100k</strong> mensais.
      </p>
      <div style="display:flex;justify-content:flex-end;">
        {arrow("rgba(237,227,206,0.75)", 22)}
      </div>
    </div>

  </div>

</div>
"""

# ============================================================
# SLIDE 2 — PROBLEMA
# Copy original (fiel): longo, dois blocos.
# ============================================================
slide2 = f"""
<div class="slide" style="background:{BG_BLACK};display:flex;flex-direction:column;justify-content:space-between;padding:30px 34px;">

  <!-- Top: masthead -->
  <div style="display:flex;justify-content:space-between;align-items:center;">
    <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;text-transform:uppercase;color:rgba(237,227,206,0.55);">O Problema</span>
    <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;color:{GOLD};">02</span>
  </div>

  <!-- Headline + body -->
  <div>
    <div style="font-family:'Alga';font-weight:600;font-size:100px;line-height:0.8;color:{ACCENT};margin-bottom:6px;">"</div>
    <h2 style="font-family:'Grift';font-weight:900;font-size:{SZ_TITLE};line-height:1;letter-spacing:-0.4px;color:{TEXT_LIGHT};margin-bottom:16px;">
      Seu perfil fala <em style="font-style:italic;color:{GOLD};">procedimento.</em><br>Por isso o paciente pede <em style="font-style:italic;color:{GOLD};">desconto.</em>
    </h2>
    {thin_line(GOLD, "38px")}
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.45;color:rgba(237,227,206,0.82);margin-top:14px;">
      Quando sua vitrine mostra <em style="font-style:italic;">"botox, preenchimento, bioestimulador"</em> como prateleira de supermercado, o paciente age como consumidor: <strong style="font-weight:900;color:{IVORY};">compara preço, pede o mais barato, fecha com quem cobrar menos.</strong>
    </p>
  </div>

  <!-- Bottom CTA -->
  <div>
    {thin_line("rgba(184,150,90,0.3)", "100%")}
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};color:{IVORY};margin-top:14px;line-height:1.4;">
      Aqui estão os <strong style="font-weight:900;color:{GOLD};">5 ajustes imediatos</strong> para mudar esse jogo ainda hoje {arrow(GOLD, 20)}
    </p>
  </div>

</div>
"""

# ============================================================
# SLIDE 3 — AJUSTE 01 · O NOME (cream)
# ============================================================
slide3 = f"""
<div class="slide" style="background:{IVORY};display:flex;flex-direction:column;justify-content:space-between;padding:30px 34px;">

  <!-- Top -->
  <div style="display:flex;justify-content:space-between;align-items:center;">
    <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;text-transform:uppercase;color:{TEXT_DARK};opacity:0.5;">Ajuste 01</span>
    <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;color:{ACCENT};text-transform:uppercase;">Nome</span>
  </div>

  <!-- Headline + sub -->
  <div>
    <h2 style="font-family:'Grift';font-weight:900;font-size:{SZ_TITLE_LG};line-height:0.98;letter-spacing:-0.5px;color:{TEXT_DARK};margin-bottom:18px;">
      Seu nome é<br>sua maior <em style="font-style:italic;color:{ACCENT};">marca.</em>
    </h2>
    {thin_line(GOLD, "38px")}
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.45;color:{TEXT_DARK};opacity:0.82;margin-top:14px;">
      <em style="font-style:italic;">Apelido</em>, <em style="font-style:italic;">diminutivo</em> e <em style="font-style:italic;">nome complexo</em> queimam sua autoridade antes da paciente ler sua bio.
    </p>
  </div>

  <!-- Fórmula -->
  <div style="background:{BG_BLACK};border-radius:12px;padding:18px 20px;">
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:2.5px;text-transform:uppercase;color:{GOLD};margin-bottom:8px;">Use a fórmula</p>
    <p style="font-family:'Alga';font-weight:600;font-size:{SZ_SUB};color:{IVORY};line-height:1.15;">Nome + Sobrenome <span style="color:{GOLD};">|</span> Harmonização Facial</p>
  </div>

  <!-- Exemplos reais (cards de perfil evidenciados) -->
  <div>
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
      <div style="width:20px;height:1px;background:{ACCENT};"></div>
      <p style="font-family:'Grift';font-weight:900;font-size:{SZ_MICRO};letter-spacing:2.5px;text-transform:uppercase;color:{ACCENT};">Exemplos reais no Instagram</p>
    </div>
    <div style="display:flex;flex-direction:column;gap:6px;">
      <div style="background:rgba(107,15,15,0.08);border-left:2px solid {ACCENT};border-radius:6px;padding:8px 12px;">
        <p style="font-family:'Grift';font-weight:900;font-size:{SZ_SMALL};color:{ACCENT};line-height:1.1;">@dra.carolinebarreto</p>
        <p style="font-family:'Alga';font-weight:600;font-size:{SZ_SMALL};color:{TEXT_DARK};line-height:1.15;">Caroline Barreto <span style="color:{GOLD};">|</span> Harmonização Facial</p>
      </div>
      <div style="background:rgba(107,15,15,0.08);border-left:2px solid {ACCENT};border-radius:6px;padding:8px 12px;">
        <p style="font-family:'Grift';font-weight:900;font-size:{SZ_SMALL};color:{ACCENT};line-height:1.1;">@dramichelineklein</p>
        <p style="font-family:'Alga';font-weight:600;font-size:{SZ_SMALL};color:{TEXT_DARK};line-height:1.15;">Micheline Klein <span style="color:{GOLD};">|</span> Harmonização Facial</p>
      </div>
    </div>
  </div>

</div>
"""

# ============================================================
# SLIDE 4 — AJUSTE 02 · A BIO
# "Quanto mais informacao mais objecao. A sua BIO precisa evidenciar: [5 itens]"
# ============================================================
slide4 = f"""
<div class="slide" style="background:{BG_BLACK};display:flex;flex-direction:column;justify-content:space-between;padding:30px 34px;">

  <div style="display:flex;justify-content:space-between;align-items:center;">
    <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;text-transform:uppercase;color:rgba(237,227,206,0.55);">Ajuste 02</span>
    <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;color:{GOLD};text-transform:uppercase;">Bio</span>
  </div>

  <!-- Headline + sub -->
  <div>
    <h2 style="font-family:'Grift';font-weight:900;font-size:{SZ_TITLE};line-height:1;letter-spacing:-0.4px;color:{TEXT_LIGHT};margin-bottom:14px;">
      Sua BIO não é <em style="font-style:italic;color:{GOLD};">currículo.</em>
    </h2>
    <p style="font-family:'Alga';font-weight:600;font-style:italic;font-size:{SZ_SMALL};color:{IVORY};line-height:1.4;">
      É a resposta de 3 segundos para: <span style="color:{GOLD};">"por que essa doutora e não outra?"</span>
    </p>
  </div>

  <!-- Lista 5 itens (novo) -->
  <div style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};color:{TEXT_LIGHT};line-height:1.45;">
    <div style="display:flex;gap:12px;padding:3px 0;"><span style="color:{GOLD};font-family:'Alga';font-style:italic;min-width:20px;">i.</span><span><strong style="font-weight:900;">Propósito</strong> &mdash; o que você entrega (não o que você faz)</span></div>
    <div style="display:flex;gap:12px;padding:3px 0;"><span style="color:{GOLD};font-family:'Alga';font-style:italic;min-width:20px;">ii.</span><span><strong style="font-weight:900;">Problema específico</strong> que você resolve</span></div>
    <div style="display:flex;gap:12px;padding:3px 0;"><span style="color:{GOLD};font-family:'Alga';font-style:italic;min-width:20px;">iii.</span><span><strong style="font-weight:900;">Formação + registro</strong> (CRO/CRM + especialização)</span></div>
    <div style="display:flex;gap:12px;padding:3px 0;"><span style="color:{GOLD};font-family:'Alga';font-style:italic;min-width:20px;">iv.</span><span><strong style="font-weight:900;">Cidade e estado</strong></span></div>
    <div style="display:flex;gap:12px;padding:3px 0;"><span style="color:{GOLD};font-family:'Alga';font-style:italic;min-width:20px;">v.</span><span><strong style="font-weight:900;">CTA com link direto</strong> do WhatsApp</span></div>
  </div>

  <!-- Imagem bio com tag EXEMPLO REAL -->
  <div>
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
      <div style="width:6px;height:6px;border-radius:50%;background:{GOLD};"></div>
      <p style="font-family:'Grift';font-weight:900;font-size:{SZ_MICRO};letter-spacing:2.5px;text-transform:uppercase;color:{GOLD};">Exemplo real · Perfil de harmonizadora</p>
    </div>
    <div style="background:{BG_WINE};border:1px solid rgba(184,150,90,0.3);border-radius:6px;padding:14px 16px;">
      <img src="{bio_uri}" style="width:100%;height:auto;display:block;" alt="Bio exemplo real">
    </div>
  </div>

</div>
"""

# ============================================================
# SLIDE 5 — AJUSTE 03 · OS DESTAQUES
# "Nada de capas... coloque a melhor foto... [5 destaques]"
# ============================================================
slide5 = f"""
<div class="slide" style="background:{BG_BLACK};display:flex;flex-direction:column;justify-content:space-between;padding:30px 34px;">

  <div style="display:flex;justify-content:space-between;align-items:center;">
    <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;text-transform:uppercase;color:rgba(237,227,206,0.55);">Ajuste 03</span>
    <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;color:{GOLD};text-transform:uppercase;">Destaques</span>
  </div>

  <!-- Headline + sub -->
  <div>
    <h2 style="font-family:'Grift';font-weight:900;font-size:{SZ_TITLE};line-height:1;letter-spacing:-0.4px;color:{TEXT_LIGHT};margin-bottom:12px;">
      Colocar capa do <em style="font-style:italic;color:{GOLD};">Canva</em> nos destaques mata o seu perfil.
    </h2>
    {thin_line(GOLD, "38px")}
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};color:rgba(237,227,206,0.82);margin-top:12px;line-height:1.45;">
      Ícone genérico + palavrinha é o assassino silencioso do seu perfil. A capa é a <strong style="font-weight:900;color:{IVORY};">foto real</strong> que mostra o que tem dentro.
    </p>
  </div>

  <!-- Lista 5 destaques -->
  <div style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};color:{TEXT_LIGHT};line-height:1.55;">
    <div style="display:flex;gap:10px;padding:3px 0;"><span style="color:{GOLD};font-family:'Alga';font-style:italic;font-weight:600;min-width:16px;">1.</span><span><strong style="font-weight:900;">Antes e Depois</strong> &middot; resultados e feedbacks</span></div>
    <div style="display:flex;gap:10px;padding:3px 0;"><span style="color:{GOLD};font-family:'Alga';font-style:italic;font-weight:600;min-width:16px;">2.</span><span><strong style="font-weight:900;">Experiência</strong> &middot; café, ambiente, recepção</span></div>
    <div style="display:flex;gap:10px;padding:3px 0;"><span style="color:{GOLD};font-family:'Alga';font-style:italic;font-weight:600;min-width:16px;">3.</span><span><strong style="font-weight:900;">Bastidores</strong> &middot; você como protagonista do trabalho</span></div>
    <div style="display:flex;gap:10px;padding:3px 0;"><span style="color:{GOLD};font-family:'Alga';font-style:italic;font-weight:600;min-width:16px;">4.</span><span><strong style="font-weight:900;">Localização</strong> &middot; localização no Maps</span></div>
    <div style="display:flex;gap:10px;padding:3px 0;"><span style="color:{GOLD};font-family:'Alga';font-style:italic;font-weight:600;min-width:16px;">5.</span><span><strong style="font-weight:900;">Lifestyle</strong> &middot; viagens e experiências pessoais</span></div>
  </div>

  <!-- Imagem destaques com tag EXEMPLO REAL -->
  <div>
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
      <div style="width:6px;height:6px;border-radius:50%;background:{GOLD};"></div>
      <p style="font-family:'Grift';font-weight:900;font-size:{SZ_MICRO};letter-spacing:2.5px;text-transform:uppercase;color:{GOLD};">Exemplo real · Destaques bem feitos</p>
    </div>
    <div style="background:{BG_WINE};border:1px solid rgba(184,150,90,0.3);border-radius:6px;padding:12px 14px;">
      <img src="{dest_uri}" style="width:100%;height:auto;display:block;" alt="Destaques exemplo real">
    </div>
  </div>

</div>
"""

# ============================================================
# SLIDE 6 — AJUSTE 04 · CASOS FIXADOS
# ============================================================
slide6 = f"""
<div class="slide" style="background:{BG_BLACK};display:flex;flex-direction:column;justify-content:space-between;padding:30px 34px;">

  <div style="display:flex;justify-content:space-between;align-items:center;">
    <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;text-transform:uppercase;color:rgba(237,227,206,0.55);">Ajuste 04</span>
    <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;color:{GOLD};text-transform:uppercase;">Casos fixados</span>
  </div>

  <!-- Headline + sub -->
  <div>
    <h2 style="font-family:'Grift';font-weight:900;font-size:{SZ_TITLE};line-height:1;letter-spacing:-0.4px;color:{TEXT_LIGHT};margin-bottom:12px;">
      Fixe <em style="font-style:italic;color:{GOLD};">3 casos.</em><br>Do mesmo <em style="font-style:italic;color:{GOLD};">problema.</em>
    </h2>
    {thin_line(GOLD, "38px")}
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.45;color:rgba(237,227,206,0.82);margin-top:12px;">
      Se quer atrair <em style="font-style:italic;color:{GOLD};">full face feminino</em>, fixe 3 full face femininos. Misturar procedimentos dilui sua autoridade e confunde quem chega.
    </p>
  </div>

  <!-- Critério para escolher -->
  <div>
    <p style="font-family:'Grift';font-weight:900;font-size:{SZ_MICRO};letter-spacing:2.5px;text-transform:uppercase;color:{GOLD};margin-bottom:10px;">Critério para escolher os 3</p>
    <div style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};color:{TEXT_LIGHT};line-height:1.45;">
      <div style="display:flex;gap:10px;padding:3px 0;"><span style="color:{GOLD};font-family:'Alga';font-style:italic;min-width:18px;">i.</span><span><strong style="font-weight:900;">Mesmo problema</strong> resolvido (ex: derretimento facial)</span></div>
      <div style="display:flex;gap:10px;padding:3px 0;"><span style="color:{GOLD};font-family:'Alga';font-style:italic;min-width:18px;">ii.</span><span><strong style="font-weight:900;">Mesmo perfil</strong> de paciente (idade, gênero, queixa)</span></div>
      <div style="display:flex;gap:10px;padding:3px 0;"><span style="color:{GOLD};font-family:'Alga';font-style:italic;min-width:18px;">iii.</span><span><strong style="font-weight:900;">Resultado evidente</strong> em 1 segundo</span></div>
    </div>
  </div>

  <!-- Imagem antes/depois com tag -->
  <div>
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
      <div style="width:6px;height:6px;border-radius:50%;background:{GOLD};"></div>
      <p style="font-family:'Grift';font-weight:900;font-size:{SZ_MICRO};letter-spacing:2.5px;text-transform:uppercase;color:{GOLD};">Exemplo real · Full face feminino</p>
    </div>
    <div style="border:1px solid rgba(184,150,90,0.3);border-radius:6px;overflow:hidden;height:170px;">
      <img src="{fixa_uri}" style="width:100%;height:100%;object-fit:cover;display:block;" alt="Casos fixados exemplo real">
    </div>
  </div>

</div>
"""

# ============================================================
# SLIDE 7 — AJUSTE 05 · O CONTEÚDO (cream)
# Copy: "O que voce coloca no feed... Exemplo: A Murielle..."
# ============================================================
slide7 = f"""
<div class="slide" style="background:{IVORY};position:relative;">

  <!-- Masthead absoluto no topo -->
  <div style="position:absolute;top:30px;left:34px;right:34px;display:flex;justify-content:space-between;align-items:center;z-index:2;">
    <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;text-transform:uppercase;color:{TEXT_DARK};opacity:0.5;">Ajuste 05</span>
    <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;color:{ACCENT};text-transform:uppercase;">Conteúdo</span>
  </div>

  <!-- Conteudo central -->
  <div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;gap:14px;padding:30px 34px;">

    <div>
      <h2 style="font-family:'Grift';font-weight:900;font-size:{SZ_TITLE};line-height:1;letter-spacing:-0.4px;color:{TEXT_DARK};margin-bottom:14px;">
        Poste <em style="font-style:italic;color:{ACCENT};">transformação</em>,<br>não técnica.
      </h2>
      <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.4;color:{TEXT_DARK};opacity:0.82;">
        Cada post técnico vira <strong style="font-weight:900;">munição</strong> para a paciente chegar <strong style="font-weight:900;">ditando tratamento</strong> e <strong style="font-weight:900;">barganhando preço</strong>.
      </p>
    </div>

    <!-- Framework 3 passos -->
    <div>
      <p style="font-family:'Grift';font-weight:900;font-size:{SZ_MICRO};letter-spacing:2.5px;text-transform:uppercase;color:{ACCENT};margin-bottom:10px;">Estrutura que funciona em qualquer post</p>

      <div style="display:flex;flex-direction:column;gap:6px;">
        <div style="display:flex;gap:10px;align-items:baseline;">
          <span style="font-family:'Alga';font-style:italic;font-weight:600;font-size:{SZ_SUB};color:{ACCENT};line-height:1;min-width:26px;">i.</span>
          <div style="flex:1;">
            <p style="font-family:'Grift';font-weight:900;font-size:{SZ_SMALL};color:{TEXT_DARK};line-height:1.2;">O problema dela</p>
            <p style="font-family:'Alga';font-style:italic;font-weight:600;font-size:{SZ_SMALL};color:{TEXT_DARK};opacity:0.75;line-height:1.3;">"rosto redondo, pesado, sem definição"</p>
          </div>
        </div>
        <div style="display:flex;gap:10px;align-items:baseline;">
          <span style="font-family:'Alga';font-style:italic;font-weight:600;font-size:{SZ_SUB};color:{ACCENT};line-height:1;min-width:26px;">ii.</span>
          <div style="flex:1;">
            <p style="font-family:'Grift';font-weight:900;font-size:{SZ_SMALL};color:{TEXT_DARK};line-height:1.2;">O desejo dela</p>
            <p style="font-family:'Alga';font-style:italic;font-weight:600;font-size:{SZ_SMALL};color:{TEXT_DARK};opacity:0.75;line-height:1.3;">"queria uma face mais leve e definida"</p>
          </div>
        </div>
        <div style="display:flex;gap:10px;align-items:baseline;">
          <span style="font-family:'Alga';font-style:italic;font-weight:600;font-size:{SZ_SUB};color:{ACCENT};line-height:1;min-width:26px;">iii.</span>
          <div style="flex:1;">
            <p style="font-family:'Grift';font-weight:900;font-size:{SZ_SMALL};color:{TEXT_DARK};line-height:1.2;">A transformação</p>
            <p style="font-family:'Alga';font-style:italic;font-weight:600;font-size:{SZ_SMALL};color:{TEXT_DARK};opacity:0.75;line-height:1.3;">"revertemos os sinais, ela ficou maravilhosa"</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Exemplo real Murielle -->
    <div style="background:{BG_BLACK};border-radius:10px;padding:14px 18px;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <div style="width:6px;height:6px;border-radius:50%;background:{GOLD};"></div>
        <p style="font-family:'Grift';font-weight:900;font-size:{SZ_MICRO};letter-spacing:2.5px;text-transform:uppercase;color:{GOLD};">Exemplo real · Legenda Murielle</p>
      </div>
      <p style="font-family:'Alga';font-weight:600;font-style:italic;font-size:{SZ_MICRO};line-height:1.45;color:{IVORY};">
        "A Murielle sofria com derretimento facial, que deixava seu rosto redondo e pesado. Queria uma face mais leve e definida &mdash; e foi exatamente o que entregamos. Ela ficou maravilhosa."
      </p>
    </div>

  </div>

</div>
"""

# ============================================================
# SLIDE 8 — REFORÇO
# Copy: "Para faturar 100k voce nao precisa... Voce precisa se posicionar..."
# ============================================================
slide8 = f"""
<div class="slide" style="background:{BG_BLACK};display:flex;flex-direction:column;justify-content:space-between;padding:30px 34px;">

  <div style="display:flex;justify-content:space-between;align-items:center;">
    <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;text-transform:uppercase;color:rgba(237,227,206,0.55);">A verdade</span>
    <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;color:{GOLD};text-transform:uppercase;">Conclusão</span>
  </div>

  <!-- Headline + texto "não precisa" sem caixa -->
  <div>
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_LABEL};letter-spacing:3px;text-transform:uppercase;color:{GOLD};margin-bottom:14px;">Para faturar R$100k por mês</p>
    <h2 style="font-family:'Alga';font-weight:600;font-size:{SZ_HERO_SM};line-height:0.95;letter-spacing:-0.5px;color:{TEXT_LIGHT};margin-bottom:20px;">
      Você <em style="font-style:italic;color:{ACCENT};">não</em> precisa.
    </h2>
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_BODY};line-height:1.45;color:rgba(237,227,206,0.82);">
      Postar <em style="font-style:italic;">todo dia</em>, ser <em style="font-style:italic;">famosa</em> ou <em style="font-style:italic;">influencer</em>.
    </p>
  </div>

  <!-- Divisor dourado -->
  <div style="display:flex;align-items:center;gap:14px;">
    <div style="flex:1;height:1px;background:rgba(184,150,90,0.35);"></div>
    <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;text-transform:uppercase;color:{GOLD};">Você precisa</span>
    <div style="flex:1;height:1px;background:rgba(184,150,90,0.35);"></div>
  </div>

  <!-- Bloco PRECISA em cream (o takeaway-chave) -->
  <div style="background:{IVORY};border-radius:12px;padding:22px 24px;">
    <p style="font-family:'Alga';font-weight:600;font-style:italic;font-size:{SZ_SUB};line-height:1.25;color:{TEXT_DARK};">
      Se posicionar para ser vista como <em>autoridade</em> na resolução de <em>um único problema</em>.
    </p>
  </div>

  <!-- Bottom CTA -->
  <div style="text-align:right;">
    <span style="font-family:'Alga';font-style:italic;font-weight:600;font-size:{SZ_SMALL};color:{GOLD};">Quer aplicar? {arrow(GOLD, 18)}</span>
  </div>

</div>
"""

# ============================================================
# SLIDE 9 — CTA FINAL
# "Faz essas alteracoes... Se voce quer um diagnostico... clica no link da bio..."
# Sem círculo R, distribuição vertical.
# ============================================================
slide9 = f"""
<div class="slide" style="background:{BG_BLACK};display:flex;flex-direction:column;justify-content:space-between;padding:30px 34px;">

  <div style="display:flex;justify-content:space-between;align-items:center;">
    <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;text-transform:uppercase;color:rgba(237,227,206,0.55);">Próximo passo</span>
    <span style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:3px;color:{GOLD};text-transform:uppercase;">RECONECTA</span>
  </div>

  <!-- Chamada emocional -->
  <div>
    <div style="margin-bottom:18px;">{thin_line(GOLD, "40px")}</div>
    <h2 style="font-family:'Alga';font-weight:600;font-size:{SZ_HERO_SM};line-height:0.95;letter-spacing:-0.4px;color:{TEXT_LIGHT};margin-bottom:14px;">
      Faz essas <em style="font-style:italic;color:{GOLD};">alterações</em> e me conta como foi.
    </h2>
  </div>

  <!-- CTA principal -->
  <div style="background:{IVORY};border-radius:12px;padding:20px 22px;">
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:2.5px;text-transform:uppercase;color:{ACCENT};margin-bottom:10px;">Sessão estratégica gratuita</p>
    <p style="font-family:'Grift';font-weight:400;font-size:{SZ_SMALL};line-height:1.4;color:{TEXT_DARK};margin-bottom:14px;">
      Se você quer um diagnóstico do que mais pode estar travando o crescimento da sua clínica hoje, <strong style="font-weight:900;">clica no link da bio</strong> e aplica para uma sessão estratégica gratuita com o nosso time.
    </p>
    <div style="display:inline-flex;align-items:center;gap:8px;padding:10px 18px;background:{BG_BLACK};border-radius:30px;">
      <span style="font-family:'Grift';font-weight:900;font-size:{SZ_MICRO};letter-spacing:1.5px;text-transform:uppercase;color:{GOLD};">Link na bio</span>
      {arrow(GOLD, 18)}
    </div>
  </div>

  <!-- Handles bottom -->
  <div style="display:flex;justify-content:space-between;align-items:center;font-family:'Grift';font-weight:400;font-size:{SZ_MICRO};letter-spacing:2.5px;text-transform:uppercase;color:rgba(237,227,206,0.55);">
    <span>@oleonardorosso</span>
    <span>@mentoriareconecta</span>
  </div>

</div>
"""

slides = [slide1, slide2, slide3, slide4, slide5, slide6, slide7, slide8, slide9]


html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Carrossel RECONECTA — Editorial</title>
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
        <div class="ig-handle">mentoriareconecta</div>
        <div class="ig-sub">Patrocinado</div>
      </div>
    </div>
    <div class="ig-more">&middot;&middot;&middot;</div>
  </div>

  <div class="carousel-viewport">
    <div class="carousel-track">
      {''.join(slides)}
    </div>
  </div>

  <div class="ig-actions">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg>
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"/></svg>
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
    <div class="spacer"></div>
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2z"/></svg>
  </div>

  <div class="ig-dots">
    {''.join('<span class="dot' + (' active' if i==0 else '') + '"></span>' for i in range(TOTAL))}
  </div>

  <div class="ig-caption">
    <span class="handle">mentoriareconecta</span> Os 5 ajustes no seu perfil que separam quem fatura R$15k de quem fatura R$100k. Arrasta &rarr;
    <span class="ts">2 horas atrás</span>
  </div>
</div>

<script>
(function(){{
  const viewport=document.querySelector('.carousel-viewport');
  const track=document.querySelector('.carousel-track');
  const dots=document.querySelectorAll('.ig-dots .dot');
  const total={TOTAL};
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

OUT.write_text(html, encoding="utf-8")
size_kb = OUT.stat().st_size / 1024
print(f"OK — carousel.html gerado ({size_kb:.1f} KB)")
