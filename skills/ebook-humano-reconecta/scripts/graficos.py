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
  bifurca           uma situação e dois caminhos; 1ª linha a situação, demais "V|X | o que faz | no que dá"
  convergem         caminhos diferentes com o MESMO fim; linhas "Rótulo | o que acontece" e "=> desfecho"
  escala            régua de dois extremos com o ponto do meio aceso; uma linha "A | meio | B"
  ordem             sequência vertical numerada, pra quando a ORDEM é o conteúdo; uma linha por item
  indice            índice de seções pra consulta rápida; uma linha por seção, "Seção | nota" opcional
  mapa              ligação item → destino com o fio no meio; linhas "texto | Destino"

O `rail` também aceita CONJUNTO de passos ("rail 1,2,6,7"), pra desenhar caminho curto: os
passos pulados ficam apagados e o fio entre eles vira tracejado.

Quem quebra entre páginas (ver DIVISIVEIS no template.html): ordem, indice, sinais, mapa.
Os outros são indivisíveis de propósito, porque quebrar separa par de célula ou de leitura.
"""
import html, re

PASSOS = ["Conexão", "Situação", "Presente inaceitável", "Qualificação", "Transição", "Apresentação", "Fechamento"]
CREAM, CREAM62, CREAM28, GOLD, GOLD65, RED, INK = "#eed9bd", "rgba(238,217,189,.62)", "rgba(238,217,189,.28)", "#eece66", "rgba(238,206,102,.65)", "#d3111a", "#161616"

def _e(s): return html.escape(s.strip(), quote=False)
def _enf(s):  # «ênfase» → gold
    return re.sub(r"«(.+?)»", r'<span class="enf">\1</span>', _e(s))
def _split(ln): return [p.strip() for p in ln.split("|")]

def rail(atual=0, mini=False):
    """Trilho dos 7 passos. `atual` aceita um número (o passo aceso, os anteriores em
    percorrido) ou um conjunto de números, pra desenhar caminho curto: `rail 1,2,6,7`
    acende só esses quatro e apaga o resto, que é o que o anexo C faz."""
    conjunto = atual if isinstance(atual, (set, frozenset, list, tuple)) else None
    atual = 0 if conjunto else atual
    W = 952; n = 7; x0, x1 = 62, W - 62; step = (x1 - x0) / (n - 1); y = 46; r = 24
    H = 70 if mini else 150
    out = [f'<svg class="g-svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
           f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{CREAM28}" stroke-width="1.5"/>']
    if conjunto:
        acesos = sorted(int(v) for v in conjunto)
        for a, b in zip(acesos, acesos[1:]):
            xa = x0 + (a - 1) * step; xb = x0 + (b - 1) * step
            tracejado = ' stroke-dasharray="4 7"' if b - a > 1 else ''
            out.append(f'<line x1="{xa:.1f}" y1="{y}" x2="{xb:.1f}" y2="{y}" stroke="{GOLD65}" stroke-width="1.5"{tracejado}/>')
    for i in range(n):
        x = x0 + i * step
        if conjunto:
            on = (i + 1) in {int(v) for v in conjunto}; done = False
        else:
            on = (i + 1) == atual; done = (i + 1) < atual
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
    """Aceita VÁRIAS linhas NEG e POS. Antes guardava só a última de cada uma, e a leitora
    via UMA frase enquanto o parágrafo ao lado declarava três: perda silenciosa, do mesmo
    tipo que já fez um capítulo inteiro sumir do PDF."""
    neg, pos = [], []
    for l in corpo:
        m = re.match(r"^\s*(NEG|POS)\s*:\s*(.*)$", l)
        if m:
            (neg if m.group(1) == "NEG" else pos).append(m.group(2).strip())
    if not neg and not pos:
        raise SystemExit("ERRO no gráfico 'leituras': nenhuma linha NEG: ou POS: reconhecida.")
    frases = lambda xs: "".join(f'<p>“{_enf(x)}”</p>' for x in xs)
    return (f'<div class="g g-leit">'
            f'<div class="lin"><i class="dot red"></i><div><span class="lbl">Leitura negativa</span>{frases(neg)}</div></div>'
            f'<div class="lin"><i class="dot gold"></i><div><span class="lbl">Leitura positiva</span>{frases(pos)}</div></div></div>')

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

# ---------------------------------------------------------------------------
# Tipos de 10/set: o texto do livro descreve MUITO caminho (se isso, então
# aquilo), e caminho desenhado se lê no celular numa olhada. Todos seguem a
# mesma regra dos anteriores: só texto, hairline, ponto e barra.
# ---------------------------------------------------------------------------

def _forquilha(W=952, H=54, cima=1, baixo=2, gap=40):
    """Conector em hairline: desce do bloco de cima e abre (ou fecha) pra N colunas.

    O x de cada perna é o CENTRO REAL da coluna do grid, com o gap descontado. Dividir a
    largura em quartos erra dez pixels, e dez pixels de desalinho aparecem no papel."""
    meio = W / 2
    def qx(n, i):
        col = (W - gap * (n - 1)) / n
        return i * (col + gap) + col / 2
    out = [f'<svg class="g-svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">']
    if cima == 1:
        out.append(f'<line x1="{meio}" y1="0" x2="{meio}" y2="{H/2:.0f}" stroke="{CREAM28}" stroke-width="1.5"/>')
        xs = [qx(baixo, i) for i in range(baixo)]
        out.append(f'<line x1="{xs[0]:.1f}" y1="{H/2:.0f}" x2="{xs[-1]:.1f}" y2="{H/2:.0f}" stroke="{CREAM28}" stroke-width="1.5"/>')
        for x in xs:
            out.append(f'<line x1="{x:.1f}" y1="{H/2:.0f}" x2="{x:.1f}" y2="{H}" stroke="{CREAM28}" stroke-width="1.5"/>')
    else:
        xs = [qx(cima, i) for i in range(cima)]
        for x in xs:
            out.append(f'<line x1="{x:.1f}" y1="0" x2="{x:.1f}" y2="{H/2:.0f}" stroke="{CREAM28}" stroke-width="1.5"/>')
        out.append(f'<line x1="{xs[0]:.1f}" y1="{H/2:.0f}" x2="{xs[-1]:.1f}" y2="{H/2:.0f}" stroke="{CREAM28}" stroke-width="1.5"/>')
        out.append(f'<line x1="{meio}" y1="{H/2:.0f}" x2="{meio}" y2="{H}" stroke="{CREAM28}" stroke-width="1.5"/>')
    out.append("</svg>")
    return "".join(out)

def bifurca(corpo):
    """Uma situação, dois caminhos, dois desfechos.

    Primeira linha: a situação. Demais: "V|X | o que você faz | no que dá".
    V pinta de dourado (o caminho que continua a conversa), X de vermelho.
    """
    linhas = [l for l in corpo if l.strip()]
    if not linhas: return ""
    situacao = linhas[0].strip()
    ramos = []
    for l in linhas[1:]:
        ps = _split(l)
        if len(ps) < 3: continue
        bom = ps[0].strip().upper() in ("V", "SIM", "OK")
        ramos.append((bom, ps[1], ps[2]))
    if not ramos: return ""
    cols = "".join(
        f'<div class="ramo"><p class="acao">{_enf(acao)}</p>'
        f'<div class="fim {"bom" if bom else "ruim"}"><i class="dot {"gold" if bom else "red"}"></i>'
        f'<span>{_enf(fim)}</span></div></div>' for bom, acao, fim in ramos)
    return (f'<div class="g g-bifurca"><div class="cond">{_enf(situacao)}</div>'
            f'{_forquilha(baixo=len(ramos))}<div class="ramos c{len(ramos)}">{cols}</div></div>')

def convergem(corpo):
    """Dois caminhos diferentes que terminam no MESMO lugar.

    Linhas "Rótulo | o que acontece", e a última começando com "=>" é o desfecho comum.
    """
    entradas, saida = [], ""
    for l in corpo:
        if not l.strip(): continue
        if l.strip().startswith("=>"):
            saida = l.strip()[2:].strip(); continue
        ps = _split(l)
        entradas.append((ps[0], ps[1] if len(ps) > 1 else ""))
    if not entradas: return ""
    cols = "".join(f'<div class="via"><span class="lbl">{_e(r)}</span><p>{_enf(x)}</p></div>' for r, x in entradas)
    return (f'<div class="g g-converge"><div class="vias c{len(entradas)}">{cols}</div>'
            f'{_forquilha(cima=len(entradas), baixo=1)}'
            f'<div class="fim"><i class="dot red"></i><p>{_enf(saida)}</p></div></div>')

def escala(corpo):
    """Régua com dois extremos e o ponto que a gente usa no meio."""
    ps = _split(" ".join(l for l in corpo if l.strip()))
    if len(ps) < 3: return ""
    W, y = 952, 34
    xs = [90, W / 2, W - 90]
    out = [f'<svg class="g-svg" viewBox="0 0 {W} 60" width="{W}" height="60">',
           f'<line x1="{xs[0]}" y1="{y}" x2="{xs[2]}" y2="{y}" stroke="{CREAM28}" stroke-width="1.5"/>']
    for i, x in enumerate(xs):
        meio = i == 1
        out.append(f'<circle cx="{x:.0f}" cy="{y}" r="{16 if meio else 9}" fill="{GOLD if meio else INK}" stroke="{GOLD if meio else CREAM62}" stroke-width="1.5"/>')
    out.append("</svg>")
    cels = "".join(f'<div class="p{i}{" meio" if i == 1 else ""}">{_enf(p)}</div>' for i, p in enumerate(ps[:3]))
    return f'<div class="g g-escala">{"".join(out)}<div class="rot">{cels}</div></div>'

def ordem(corpo):
    """Sequência vertical numerada em que a ORDEM é o conteúdo."""
    itens = [re.sub(r"^\s*[-*]\s*", "", l).strip() for l in corpo if l.strip()]
    rows = "".join(f'<div class="lin"><span class="n">{i+1}</span><p>{_enf(t)}</p></div>' for i, t in enumerate(itens))
    return f'<div class="g g-ordem">{rows}</div>'

def indice(corpo):
    """Índice de seções pra consulta rápida: a leitora acha o caso sem folhear."""
    itens = [_split(l) for l in corpo if l.strip()]
    rows = "".join(f'<div class="lin"><span class="n">{i+1:02d}</span><p>{_enf(it[0])}</p>'
                   f'<span class="nota">{_enf(it[1]) if len(it) > 1 else ""}</span></div>'
                   for i, it in enumerate(itens))
    return f'<div class="g g-indice">{rows}</div>'

def mapa(corpo):
    """Ligação item → destino, com o fio no meio. "pergunta | Passo 3"."""
    itens = [_split(l) for l in corpo if l.strip()]
    rows = "".join(f'<div class="lin"><p class="de">{_enf(it[0])}</p><div class="fio"></div>'
                   f'<span class="para">{_enf(it[1] if len(it) > 1 else "")}</span></div>' for it in itens)
    return f'<div class="g g-mapa">{rows}</div>'

def render(tipo, param, corpo):
    tipo = tipo.lower()
    if tipo == "rail":
        return rail([int(v) for v in param.split(",")] if param and "," in param else int(param or 0))
    if tipo == "funil": return funil()
    if tipo == "linha": return linha(corpo)
    if tipo == "duas": return duas(corpo)
    if tipo == "leituras": return leituras(corpo)
    if tipo == "sinais": return sinais(corpo, param or "Quando avançar")
    if tipo == "bastao": return bastao(corpo)
    if tipo == "grade": return grade(corpo)
    if tipo == "bifurca": return bifurca(corpo)
    if tipo == "convergem": return convergem(corpo)
    if tipo == "escala": return escala(corpo)
    if tipo == "ordem": return ordem(corpo)
    if tipo == "indice": return indice(corpo)
    if tipo == "mapa": return mapa(corpo)
    raise ValueError(f"grafico desconhecido: {tipo}")

CSS = """
.g{width:952px;margin:28px 0 60px 0}
.g .lbl{font-family:var(--mono);font-size:18px;letter-spacing:.18em;color:var(--gold-65);text-transform:uppercase;display:block;line-height:1}
.g .lbl.topo{margin-bottom:30px;color:var(--gold)}
.g .dot{display:inline-block;width:12px;height:12px;border-radius:50%;flex:none}
.g .dot.gold{background:var(--gold)} .g .dot.red{background:var(--red)}
.g-rail{margin:20px 0 52px 0} .g-rail.mini{margin:0}
.g-svg{display:block}
.g-linha{position:relative;display:flex;gap:28px;padding-top:8px}
.g-linha .trilho{position:absolute;left:24px;right:24px;top:31px;height:1.5px;background:rgba(238,217,189,.28)}
.g-linha .col{flex:1;display:flex;flex-direction:column;gap:14px}
.g-linha .no{width:48px;height:48px;border-radius:50%;border:1.5px solid var(--gold);background:var(--ink);display:flex;align-items:center;justify-content:center;position:relative}
.g-linha .no .n{font-family:var(--mono);font-size:16px;color:var(--gold);letter-spacing:.1em}
.g-linha .tit{font-family:var(--body);font-weight:600;font-size:34px;line-height:1.25;color:var(--cream);margin-top:6px;min-height:85px}
.g-linha .nota{font-family:var(--body);font-weight:400;font-size:30px;line-height:1.4;color:var(--cream-80)}
.g-duas{display:grid;grid-template-columns:1fr 1fr;column-gap:36px;row-gap:0}
.g-duas .hd{display:flex;align-items:center;gap:12px;padding-bottom:18px;border-bottom:1.5px solid rgba(238,217,189,.28)}
.g-duas .cel:empty{border-bottom:0;padding:0}
.g-duas .cel{font-family:var(--body);font-size:32px;line-height:1.4;color:var(--cream-90);padding:20px 0;border-bottom:1px solid rgba(238,217,189,.14)}
.g-leit .lin{display:flex;gap:22px;align-items:flex-start;padding:26px 0;border-top:1px solid rgba(238,217,189,.14)}
.g-leit .lin .dot{margin-top:6px}
.g-leit p{margin:14px 0 0 0;font-size:40px;line-height:1.35;font-weight:500;color:var(--cream)}
.g-leit p+p{margin-top:12px}
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

.g-bifurca .cond{font-family:var(--body);font-weight:600;font-size:34px;line-height:1.3;color:var(--cream);text-align:center;padding:24px 30px;border:1.5px solid rgba(238,217,189,.28);width:640px;margin:0 auto}
.g-bifurca .ramos{display:grid;column-gap:40px}
.g-bifurca .ramos.c2{grid-template-columns:1fr 1fr}
.g-bifurca .ramos.c3{grid-template-columns:1fr 1fr 1fr}
.g-bifurca .ramo{border:1.5px solid rgba(238,217,189,.28);display:flex;flex-direction:column}
.g-bifurca .acao{margin:0;flex:1;padding:22px 26px;font-size:31px;line-height:1.35;color:var(--cream-90)}
.g-bifurca .fim{display:flex;gap:16px;align-items:flex-start;padding:20px 26px;border-top:1.5px solid rgba(238,217,189,.28)}
.g-bifurca .fim .dot{margin-top:11px}
.g-bifurca .fim span{font-family:var(--body);font-weight:600;font-size:31px;line-height:1.3}
.g-bifurca .fim.bom{border-top-color:var(--gold)} .g-bifurca .fim.bom span{color:var(--gold)}
.g-bifurca .fim.ruim{border-top-color:var(--red)} .g-bifurca .fim.ruim span{color:rgba(238,217,189,.62)}
.g-converge .vias{display:grid;column-gap:40px}
.g-converge .vias.c2{grid-template-columns:1fr 1fr}
.g-converge .via{padding:22px 26px;border:1.5px solid rgba(238,217,189,.28)}
.g-converge .via p{margin:14px 0 0 0;font-size:31px;line-height:1.35;color:var(--cream-90)}
.g-converge .fim{display:flex;gap:20px;align-items:flex-start;width:700px;margin:0 auto;padding:24px 30px;border:1.5px solid rgba(211,17,26,.55)}
.g-converge .fim .dot{margin-top:12px}
.g-converge .fim p{margin:0;font-family:var(--body);font-weight:600;font-size:33px;line-height:1.3;color:var(--cream)}
.g-escala .rot{display:grid;grid-template-columns:1fr 1fr 1fr;column-gap:24px;margin-top:6px}
.g-escala .rot>div{font-size:29px;line-height:1.35;color:var(--cream-62)}
.g-escala .p0{text-align:left} .g-escala .p2{text-align:right}
.g-escala .meio{text-align:center;color:var(--gold);font-weight:600;font-size:33px}
.g-ordem .lin{display:flex;gap:26px;align-items:flex-start;padding:22px 0;border-top:1px solid rgba(238,217,189,.14)}
.g-ordem .lin:last-child{border-bottom:1px solid rgba(238,217,189,.14)}
.g-ordem .n{font-family:var(--disp);font-weight:700;font-size:48px;line-height:1;color:var(--gold);width:46px;flex:none}
.g-ordem p{margin:0;font-size:34px;line-height:1.35;color:var(--cream)}
.g-indice .lin{display:flex;gap:24px;align-items:baseline;padding:20px 0;border-top:1px solid rgba(238,217,189,.14)}
.g-indice .lin:last-child{border-bottom:1px solid rgba(238,217,189,.14)}
.g-indice .n{font-family:var(--mono);font-size:18px;letter-spacing:.16em;color:var(--gold-65);width:44px;flex:none}
.g-indice p{margin:0;flex:1;font-family:var(--body);font-weight:500;font-size:33px;line-height:1.3;color:var(--cream)}
.g-indice .nota{font-family:var(--mono);font-size:17px;letter-spacing:.08em;color:var(--cream-62);text-align:right}
.g-mapa .lin{display:flex;gap:22px;align-items:center;padding:20px 0;border-top:1px solid rgba(238,217,189,.14)}
.g-mapa .lin:last-child{border-bottom:1px solid rgba(238,217,189,.14)}
.g-mapa .de{margin:0;flex:1;font-size:30px;line-height:1.35;color:var(--cream-90)}
.g-mapa .fio{width:64px;height:1.5px;background:var(--gold-65);flex:none}
.g-mapa .para{font-family:var(--mono);font-size:18px;letter-spacing:.16em;color:var(--gold);text-transform:uppercase;white-space:nowrap;flex:none}
"""
