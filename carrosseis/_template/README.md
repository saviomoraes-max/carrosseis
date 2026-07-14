# RECONECTA Carousel Template

Sistema reutilizável para gerar carrosséis editoriais RECONECTA (paleta burgundy/ivory/gold + Grift + Alga).

## Arquivos

- **`reconecta_carousel.py`** — módulo core. Paleta, fontes, helpers, HTML shell.
- **`reference.py`** — 8 patterns de slide prontos (hero, problema, nome-cream-card, ajuste-com-imagem, framework-3-steps, contraste, cta, etc.)
- **`fonts/`** — Alga SemiBold + Grift (Black, BlackItalic, Regular, Italic) embutidas em base64 via `load_fonts()`.
- **`export.py`** — script Playwright que lê `./carousel.html` e exporta slides 1080×1350 em `./slides/`.

## Como criar um novo carrossel

```bash
# 1. Criar pasta
mkdir /Users/saviomoraes/reconecta/carrosseis/<slug>
cd /Users/saviomoraes/reconecta/carrosseis/<slug>
mkdir img
cp ../_template/export.py .

# 2. Criar build.py (ver Template abaixo)

# 3. Rodar
python3 build.py && python3 export.py && open carousel.html
```

## Template mínimo de `build.py`

```python
"""Carrossel <tema>."""
import sys
from pathlib import Path

# Adiciona template ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "_template"))
from reconecta_carousel import *
from reference import (
    hero_dark_bgimage, hero_dark_clean, problem_dark, nome_cream_card,
    ajuste_dark_image, framework_3steps, contraste_dark, cta_final_dark,
)

BASE = Path(__file__).parent
IMG = BASE / "img"

# Compor slides usando patterns do reference ou HTML puro
slide1 = hero_dark_bgimage(
    image_path=IMG / "hero.jpg",
    label_l="RECONECTA", label_r="Edição 02",
    tag="Tema do carrossel",
    headline_alga='Headline <em style="font-style:italic;">principal</em>.',
    subtitle_grift='Subtítulo com <strong style="font-weight:900;color:#B8965A;">ênfase</strong>.',
)

slide2 = problem_dark(
    label_l="O Problema", label_r="02",
    headline_grift='Título <em style="font-style:italic;color:#B8965A;">bold</em>.',
    body_grift="Corpo explicando o problema.",
    cta="CTA que aponta pro próximo slide",
)

# ... demais slides

slides = [slide1, slide2, ...]

html = render_carousel(
    slides,
    caption="Legenda curta do Instagram. Arrasta →",
)
(BASE / "carousel.html").write_text(html, encoding="utf-8")
print(f"OK — {len(slides)} slides, {(BASE / 'carousel.html').stat().st_size/1024:.1f} KB")
```

## Paleta

| Token        | Hex       | Uso |
|--------------|-----------|-----|
| `BG_BLACK`   | #0F0505   | Fundo escuro principal |
| `BG_WINE`    | #1A0808   | Layering/cards escuros |
| `ACCENT`     | #6B0F0F   | Burgundy pop (em fundo claro) |
| `IVORY`      | #EDE3CE   | Cards cream, texto em fundo escuro |
| `GOLD`       | #B8965A   | Champagne accent (em fundo escuro) |
| `POP`        | #C9252D   | Crimson extremo — uma palavra por slide max |
| `TEXT_DARK`  | #1A0F0A   | Texto em fundo claro |
| `TEXT_LIGHT` | #EDE3CE   | Texto em fundo escuro |
| `TEXT_MUTED` | #8A7F6D   | Corpo secundário em fundo claro |

## Tipografia

Só 2 famílias. Use `SZ_*` em vez de valores fixos.

| Family          | Uso                            | Sizes principais |
|-----------------|--------------------------------|------------------|
| `'Alga'` 600    | Hero headlines, italic accents | `SZ_HERO` 120, `SZ_HERO_SM` 96 |
| `'Grift'` 900   | Títulos Grift Black            | `SZ_TITLE_LG` 72, `SZ_TITLE` 60 |
| `'Grift'` 400   | Body, subtítulos, labels       | `SZ_SUB` 44, `SZ_BODY` 32, `SZ_SMALL` 26, `SZ_LABEL` 20, `SZ_MICRO` 16 |

Todos em px do output 1080×1350 — `px()` já converte pro viewport 420.

## Componentes primitivos

- `masthead(left, right, cream_bg=False)` — topo com 2 labels
- `arrow(color, size)` — seta →
- `thin_line(color, width)` — divisor fino decorativo
- `real_example_tag(text)` — bullet + "EXEMPLO REAL · …"
- `divider_with_label(label)` — "— VOCÊ PRECISA —"

## Regras de copy

- Copy do usuário deve ser preservada — corrigir só ortografia
- Máx 1 palavra em `POP` crimson por slide
- Destacar palavras-chave com `<em style="font-style:italic;color:{GOLD};">palavra</em>` em fundo escuro, ou `color:{ACCENT}` em fundo claro
- Masthead sempre presente (RECONECTA/Edição NN ou O Problema/02 etc.)

## Regras de layout

- Slides 1 e 9 (hero + CTA) tendem a fundo escuro
- Slides 3 e 7 usam fundo cream pra variação visual
- Imagens de exemplo real: sempre com tag `real_example_tag("Exemplo real · …")` acima
- Cards de takeaway (tipo "você precisa"): sempre em ivory com texto dark
- Evitar espaço morto: usar `flex-direction:column;justify-content:space-between` no slide container, ou centralizar bloco principal com `position:absolute;inset:0;flex;justify-content:center`

## Export

`export.py` detecta automaticamente o número de slides no HTML. Basta rodar `python3 export.py` no diretório do carrossel.
