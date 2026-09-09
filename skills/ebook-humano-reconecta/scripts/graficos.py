#!/usr/bin/env python3
"""Gráficos vetoriais (SVG/HTML) pro miolo do ebook, no vocabulário do Reconecta Design System:
só texto, hairline, ponto e barra. Sem ícone, sem ilustração, sem foto. Largura fixa 952px.

Sintaxe no markdown (bloco :::grafico <tipo> [param] ... :::):
  rail N            trilho dos 7 passos, passo N aceso (0 = nenhum)
  funil             5 contatos → 1 agendamento
  linha             linha do tempo horizontal; cada linha do corpo "Título | nota" (2 a 4 nós)
  duas              comparação em duas colunas; 1ª linha "Cabeçalho A | Cabeçalho B", demais "célula A | célula B"
  leituras          "NEG: frase" e "POS: frase" (como ela lê você)
  sinais            checklist; cada linha "- item"
  bastao            dois mini-diálogos lado a lado; linhas "ELA:"/"VOCÊ:" e "=> ELA" ou "=> VOCÊ" fecham cada coluna
  grade             grade numerada 2 colunas; cada linha "N | rótulo"
"""
import html, re

PASSOS = ["Conexão", "Situação", "Presente inaceitável", "Qualificação", "Transição", "Apresentação", "Fechamento"]
CREAM, CREAM62, CREAM28, GOLD, GOLD65, RED, INK = "#eed9bd", "rgba(238,217,189,.62)", "rgba(238,217,189,.28)", "#eece66", "rgba(238,206,102,.65)", "#d3111a", "#161616"

def _e(s): return html.escape(s.strip(), quote=False)
def _enf(s):  # «ênfase» → gold
    return re.sub(r"«(.+?)»", r'<span class="enf">\1</span>', _e(s))
def _split(ln): return [p.strip() for p in ln.split("|")]

def rail(atual=0, mini=False):
    W = 952; n = 7; x0, x1 = 44, W - 44; step = (x1 - x0) / (n - 1); y = 46; r = 24
    H = 70 if mini else 150
    out = [f'<svg class="g-svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
           f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{CREAM28}" stroke-width="1.5"/>']
    for i in range(n):
        x = x0 + i * step; on = (i + 1) == atual; done = (i + 1) < atual
        fill = GOLD if on else INK; stroke = GOLD if on else (CREAM62 if done else CREAM28)
        out.append(f'<circle cx="{x:.1f}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        out.append(f'<text x="{x:.1f}" y="{y+1}" text-anchor="middle" dominant-baseline="central" font-family="Space Mono" font-size="20" fill="{INK if on else (CREAM if done else CREAM62)}">{i+1}</text>')
        if not mini:
            nome = PASSOS[i].upper().split(" ")
            for k, palavra in enumerate(nome):
                out.append(f'<text x="{x:.1f}" y="{y + r + 34 + k*22}" text-anchor="middle" font-family="Space Mono" font-size="14" letter-spacing="1.5" fill="{GOLD if on else CREAM62}">{palavra}</text>')
    out.append("</svg>")
    return f'<div class="g g-rail{" mini" if mini else ""}">' + "".join(out) + "</div>"

def funil():
    W, H = 952, 200; r = 36; xs = [120 + i * 110 for i in range(5)]; y = 70
    out = [f'<svg class="g-svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">']
    for i, x in enumerate(xs):
        on = i == 4
        out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{GOLD if on else INK}" stroke="{GOLD if on else CREAM28}" stroke-width="1.5"/>')
    out.append(f'<text x="{xs[0]-r}" y="{y + r + 46}" font-family="Space Mono" font-size="18" letter-spacing="3" fill="{CREAM62}">5 CONTATOS</text>')
    out.append(f'<text x="{xs[4]+r}" y="{y + r + 46}" text-anchor="end" font-family="Space Mono" font-size="18" letter-spacing="3" fill="{GOLD}">1 AGENDAMENTO</text>')
    out.append(f'<text x="{xs[4]+r+60}" y="{y+8}" font-family="TT Modernoir" font-weight="700" font-size="72" fill="{CREAM}">7 PASSOS</text>')
    out.append(f'<text x="{xs[4]+r+62}" y="{y+40}" font-family="Space Mono" font-size="14" letter-spacing="2" fill="{CREAM62}">ENTRE UM E OUTRO</text>')
    out.append("</svg>")
    return '<div class="g g-funil">' + "".join(out) + "</div>"

def linha(corpo):
    itens = [_split(l) for l in corpo if l.strip()]
    cols = []
    for i, it in enumerate(itens):
        tit = it[0]; nota = it[1] if len(it) > 1 else ""
        cols.append(f'<div class="col"><div class="no"><span class="n">{i+1:02d}</span></div><div class="tit">{_enf(tit)}</div><div class="nota">{_enf(nota)}</div></div>')
    return f'<div class="g g-linha c{len(itens)}"><div class="trilho"></div>' + "".join(cols) + "</div>"

def duas(corpo):
    linhas = [_split(l) for l in corpo if l.strip()]
    if not linhas: return ""
    ha, hb = (linhas[0] + [""])[:2]
    rows = "".join(f'<div class="cel a">{_enf(a)}</div><div class="cel b">{_enf(b)}</div>' for a, b in [(r + [""])[:2] for r in linhas[1:]])
    return (f'<div class="g g-duas"><div class="hd a"><i class="dot gold"></i><span class="lbl">{_e(ha)}</span></div>'
            f'<div class="hd b"><i class="dot red"></i><span class="lbl">{_e(hb)}</span></div>{rows}</div>')

def leituras(corpo):
    neg = pos = ""
    for l in corpo:
        m = re.match(r"^\s*(NEG|POS)\s*:\s*(.*)$", l)
        if m:
            if m.group(1) == "NEG": neg = m.group(2)
            else: pos = m.group(2)
    return (f'<div class="g g-leit">'
            f'<div class="lin"><i class="dot red"></i><div><span class="lbl">Leitura negativa</span><p>“{_enf(neg)}”</p></div></div>'
            f'<div class="lin"><i class="dot gold"></i><div><span class="lbl">Leitura positiva</span><p>“{_enf(pos)}”</p></div></div></div>')

def sinais(corpo, titulo="Quando avançar"):
    itens = [re.sub(r"^\s*[-*]\s*", "", l) for l in corpo if l.strip()]
    rows = "".join(f'<div class="lin"><span class="n">{i+1:02d}</span><i class="box"></i><p>{_enf(t)}</p></div>' for i, t in enumerate(itens))
    return f'<div class="g g-sinais">{rows}</div>'

def bastao(corpo):
    colunas, atual = [], []
    for l in corpo:
        if not l.strip(): continue
        m = re.match(r"^\s*=>\s*(ELA|VOCÊ|VOCE)\s*$", l.strip(), re.I)
        if m:
            quem = m.group(1).upper(); voce = quem.startswith("VOC")
            colunas.append("".join(atual) + f'<div class="res {"voce" if voce else "ela"}"><i class="dot {"gold" if voce else "red"}"></i><span class="lbl">Bastão com {"você" if voce else "ela"}</span></div>')
            atual = []; continue
        m = re.match(r"^(ELA|PACIENTE|VOCÊ|VOCE|DOUTORA):\s*(.*)$", l.strip(), re.I)
        if m:
            quem = m.group(1).upper(); voce = quem in ("VOCÊ", "VOCE", "DOUTORA")
            atual.append(f'<div class="msg {"voce" if voce else "ela"}">{_enf(m.group(2))}</div>')
    if atual: colunas.append("".join(atual))
    return '<div class="g g-bastao">' + "".join(f'<div class="col">{c}</div>' for c in colunas) + "</div>"

def grade(corpo):
    itens = [_split(l) for l in corpo if l.strip()]
    cels = "".join(f'<div class="cel"><span class="n">{_e(it[0])}</span><p>{_enf(it[1] if len(it) > 1 else "")}</p></div>' for it in itens)
    return f'<div class="g g-grade">{cels}</div>'

def render(tipo, param, corpo):
    tipo = tipo.lower()
    if tipo == "rail": return rail(int(param or 0))
    if tipo == "funil": return funil()
    if tipo == "linha": return linha(corpo)
    if tipo == "duas": return duas(corpo)
    if tipo == "leituras": return leituras(corpo)
    if tipo == "sinais": return sinais(corpo, param or "Quando avançar")
    if tipo == "bastao": return bastao(corpo)
    if tipo == "grade": return grade(corpo)
    raise ValueError(f"grafico desconhecido: {tipo}")

CSS = """
.g{width:952px;margin:28px 0 60px 0}
.g .lbl{font-family:var(--mono);font-size:18px;letter-spacing:.18em;color:var(--gold-65);text-transform:uppercase;display:block;line-height:1}
.g .lbl.topo{margin-bottom:30px;color:var(--gold)}
.g .dot{display:inline-block;width:12px;height:12px;border-radius:50%;flex:none}
.g .dot.gold{background:var(--gold)} .g .dot.red{background:var(--red)}
.g-rail{margin:20px 0 52px 0} .g-rail.mini{margin:0}
.g-linha{position:relative;display:flex;gap:28px;padding-top:8px}
.g-linha .trilho{position:absolute;left:24px;right:24px;top:31px;height:1.5px;background:rgba(238,217,189,.28)}
.g-linha .col{flex:1;display:flex;flex-direction:column;gap:14px}
.g-linha .no{width:48px;height:48px;border-radius:50%;border:1.5px solid var(--gold);background:var(--ink);display:flex;align-items:center;justify-content:center;position:relative}
.g-linha .no .n{font-family:var(--mono);font-size:16px;color:var(--gold);letter-spacing:.1em}
.g-linha .tit{font-family:var(--body);font-weight:600;font-size:34px;line-height:1.25;color:var(--cream);margin-top:6px}
.g-linha .nota{font-family:var(--body);font-weight:400;font-size:30px;line-height:1.4;color:var(--cream-80)}
.g-duas{display:grid;grid-template-columns:1fr 1fr;column-gap:36px;row-gap:0}
.g-duas .hd{display:flex;align-items:center;gap:12px;padding-bottom:18px;border-bottom:1.5px solid rgba(238,217,189,.28)}
.g-duas .cel{font-family:var(--body);font-size:32px;line-height:1.4;color:var(--cream-90);padding:20px 0;border-bottom:1px solid rgba(238,217,189,.14)}
.g-leit .lin{display:flex;gap:22px;align-items:flex-start;padding:26px 0;border-top:1px solid rgba(238,217,189,.14)}
.g-leit .lin .dot{margin-top:6px}
.g-leit p{margin:14px 0 0 0;font-size:40px;line-height:1.35;font-weight:500;color:var(--cream)}
.g-sinais .lin{display:flex;gap:22px;align-items:flex-start;padding:20px 0;border-top:1px solid rgba(238,217,189,.14)}
.g-sinais .n{font-family:var(--mono);font-size:18px;letter-spacing:.14em;color:var(--gold-65);width:40px;padding-top:14px;flex:none}
.g-sinais .box{width:34px;height:34px;border:1.5px solid rgba(238,217,189,.45);flex:none;margin-top:9px}
.g-sinais p{margin:0;font-size:36px;line-height:1.4;color:var(--cream-90)}
.g-bastao{display:grid;grid-template-columns:1fr 1fr;gap:36px}
.g-bastao .col{display:flex;flex-direction:column;gap:14px}
.g-bastao .msg{font-family:var(--body);font-size:30px;line-height:1.38;color:var(--cream-90);padding:16px 20px;border:1.5px solid rgba(238,217,189,.28);max-width:92%}
.g-bastao .msg.ela{align-self:flex-start} .g-bastao .msg.voce{align-self:flex-end;border-color:rgba(238,206,102,.6);background:rgba(238,206,102,.06)}
.g-bastao .res{display:flex;align-items:center;gap:12px;margin-top:14px;padding-top:16px;border-top:1.5px solid rgba(238,217,189,.28)}
.g-bastao .res.voce .lbl{color:var(--gold)}
.g-grade{display:grid;grid-template-columns:1fr 1fr;column-gap:40px;row-gap:0}
.g-grade .cel{display:flex;gap:18px;align-items:baseline;padding:18px 0;border-top:1px solid rgba(238,217,189,.14)}
.g-grade .n{font-family:var(--disp);font-weight:700;font-size:56px;line-height:1;color:var(--gold-65);width:58px;flex:none}
.g-grade p{margin:0;font-size:32px;line-height:1.35;font-weight:500;color:var(--cream)}
"""
