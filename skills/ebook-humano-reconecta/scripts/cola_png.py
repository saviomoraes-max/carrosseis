#!/usr/bin/env python3
"""Exporta a cola do anexo A como PNG 1080x1920 solto, pra salvar no celular.

O anexo A ocupa 6 páginas no PDF porque o corpo do livro é 38px. A cola é outra
peça: mesma tipografia, corpo menor, feita pra consulta rápida e não pra leitura.
TODO o texto sai do próprio manuscrito, literal. Nada é reescrito aqui.

Uso: python3 cola_png.py ebooks/<slug> [--por-pagina 4]
"""
import json, re, sys, pathlib, html

RAIZ = pathlib.Path(__file__).resolve().parent
DS_DEFAULT = "/Volumes/SSD kenipe/inbox/Reconecta Design System"

def enfase(s):
    s = html.escape(s)
    return re.sub(r"«(.+?)»", r'<span class="enf">\1</span>', s)

def parsear(txt):
    """Devolve [{rotulo, blocos:[(tipo, texto)]}] na ORDEM do anexo.

    Nada do anexo é descartado: descrição, frase pronta, nota entre frases e sinal
    de avanço saem todos, na sequência em que a autora escreveu.
    """
    corpo = re.sub(r"\A---\n.*?\n---\n", "", txt, flags=re.S)
    corpo = re.sub(r"^:::grafico[^\n]*\n.*?^:::[ \t]*$", "", corpo, flags=re.S | re.M)
    corpo = re.sub(r"^# .*$", "", corpo, flags=re.M)
    passos, atual = [], None
    i, linhas = 0, corpo.split("\n")
    while i < len(linhas):
        ln = linhas[i].strip()
        m = re.match(r"^«(.+?)»\s*(.*)$", ln)
        if m:
            if atual: passos.append(atual)
            atual = {"rotulo": m.group(1).rstrip("."), "blocos": []}
            if m.group(2).strip(): atual["blocos"].append(("desc", m.group(2).strip()))
        elif ln == ":::frase" and atual is not None:
            j, buf = i + 1, []
            while j < len(linhas) and linhas[j].strip() != ":::":
                if linhas[j].strip(): buf.append(linhas[j].strip())
                j += 1
            atual["blocos"].append(("frase", " ".join(buf))); i = j
        elif ln and atual is not None and not ln.startswith(":::"):
            tipo = "sinal" if re.match(r"^(Avança|Sucesso)\b", ln) else "nota"
            atual["blocos"].append((tipo, ln))
        i += 1
    if atual: passos.append(atual)
    return passos

CSS = """
:root{--ink:#161616;--cream:#eed9bd;--cream-90:rgba(238,217,189,.9);--cream-70:rgba(238,217,189,.7);
--cream-62:rgba(238,217,189,.62);--gold:#eece66;--gold-65:rgba(238,206,102,.65);--red:#d3111a;
--disp:"TT Modernoir",Impact,sans-serif;--mono:"Space Mono",ui-monospace,monospace;--body:Inter,-apple-system,Arial,sans-serif}
*{box-sizing:border-box}
body{margin:0;background:var(--ink);color:var(--cream-90);font-family:var(--body);-webkit-print-color-adjust:exact}
.pg{width:1080px;height:1920px;position:relative;overflow:hidden;background:var(--ink)}
.rec-dot{position:absolute;left:64px;top:70px;width:11px;height:11px;border-radius:50%;background:var(--red)}
.rec{position:absolute;left:84px;top:62px;font-family:var(--mono);font-size:20px;letter-spacing:.16em;color:rgba(238,217,189,.8);text-transform:uppercase}
.hud{position:absolute;right:64px;top:63px;font-family:var(--mono);font-size:18px;letter-spacing:.18em;color:var(--gold-65);text-transform:uppercase}
.cab{position:absolute;left:64px;top:150px;width:952px}
.kicker{font-family:var(--mono);font-size:20px;letter-spacing:.22em;color:var(--gold);text-transform:uppercase;display:block;margin-bottom:18px}
h1{font-family:var(--disp);font-weight:700;font-size:86px;line-height:.98;color:var(--cream);text-transform:uppercase;margin:0}
.corpo{position:absolute;left:64px;top:340px;width:952px;height:1400px;display:flex;flex-direction:column;gap:48px;justify-content:space-between}
.passo{display:flex;flex-direction:column;gap:15px}
.rot{font-family:var(--body);font-weight:600;font-size:38px;color:var(--cream);line-height:1.2}
.rot .n{font-family:var(--mono);font-size:22px;letter-spacing:.16em;color:var(--gold-65);margin-right:14px}
.desc{font-size:28px;line-height:1.35;color:var(--cream-62);margin:0}\n.nota{font-size:25px;line-height:1.38;color:var(--cream-70);margin:0}
.fr{border-left:3px solid var(--gold);padding-left:22px;display:flex;flex-direction:column;gap:10px}
.fr p{margin:0;font-size:32px;line-height:1.38;color:var(--cream);font-weight:500}
.sinal{font-family:var(--mono);font-size:22px;line-height:1.45;letter-spacing:.03em;color:var(--gold-65);text-transform:none}
.rodape{position:absolute;left:64px;right:64px;bottom:64px;display:flex;align-items:flex-end;justify-content:space-between}
.slug,.pn{font-family:var(--mono);font-size:18px;letter-spacing:.14em;color:var(--cream-62);text-transform:uppercase}
"""

def pagina(L, passos, idx, total, titulo):
    itens = ""
    for p in passos:
        rot = p["rotulo"]
        m = re.match(r"^(\d+)\.\s*(.+)$", rot)
        n, nome = (m.group(1), m.group(2)) if m else ("", rot)
        partes, frases = [], []
        def descarrega():
            if frases:
                partes.append('<div class="fr">' + "".join(f"<p>{enfase(f)}</p>" for f in frases) + "</div>")
                frases.clear()
        for tipo, txt in p["blocos"]:
            if tipo == "frase":
                frases.append(txt)
            else:
                descarrega()
                cls = {"desc": "desc", "nota": "nota", "sinal": "sinal"}[tipo]
                partes.append(f'<div class="{cls}">{enfase(txt)}</div>')
        descarrega()
        itens += (f'<div class="passo"><div class="rot">{("<span class=n>"+n+"</span>") if n else ""}'
                  f'{enfase(nome)}</div>{"".join(partes)}</div>')
    return (f'<div class="pg"><div class="rec-dot"></div><span class="rec">REC</span>'
            f'<span class="hud">{html.escape(L["hud"])}</span>'
            f'<div class="cab"><span class="kicker">A cola · {idx} de {total}</span><h1>{enfase(titulo)}</h1></div>'
            f'<div class="corpo">{itens}</div>'
            f'<div class="rodape"><span class="slug">{html.escape(L["rodape"])}</span>'
            f'<span class="pn">{idx}/{total}</span></div></div>')

def main():
    raiz = pathlib.Path(sys.argv[1])
    L = json.loads((raiz / "livro.json").read_text()); ds = L.get("ds", DS_DEFAULT)
    arq = next(raiz.glob("manuscrito/A-*.md"))
    passos = parsear(arq.read_text(encoding="utf-8"))
    rd = raiz / "render"; rd.mkdir(exist_ok=True)
    css = CSS.replace("{ds}", "file://" + ds)
    doc = lambda corpo: (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
        f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap">'
        f'<style>{css}</style></head><body>{corpo}</body></html>')

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})

        # 1. medir cada passo isolado, com a tipografia real
        (rd / "cola-medida.html").write_text(doc(pagina(L, passos, 1, 1, L["titulo"])), encoding="utf-8")
        pg.goto((rd / "cola-medida.html").resolve().as_uri()); pg.wait_for_timeout(1500)
        alturas = pg.evaluate("() => [...document.querySelectorAll('.passo')].map(e => e.offsetHeight)")
        util, gap = pg.evaluate("() => document.querySelector('.corpo').clientHeight"), 48

        # 2. empacotar. Guloso puro descobre quantas páginas são necessárias; depois
        #    reempacota mirando a média, senão a última página fica com um passo só
        #    e o space-between abre um buraco no meio dela.
        def empacotar(teto):
            grupos, atual, alto = [], [], 0
            for passo, h in zip(passos, alturas):
                extra = h + (gap if atual else 0)
                if atual and alto + extra > min(teto, util):
                    grupos.append(atual); atual, alto = [passo], h
                else:
                    atual.append(passo); alto += extra
            if atual: grupos.append(atual)
            return grupos
        n_min = len(empacotar(util))
        total_h = sum(alturas) + gap * (len(alturas) - 1)
        grupos = empacotar(util)
        for alvo in range(int(total_h / n_min), util + 1, 20):
            tentativa = empacotar(alvo)
            if len(tentativa) == n_min:
                grupos = tentativa; break

        # 3. render final
        pgs = "".join(pagina(L, g, i + 1, len(grupos), L["titulo"]) for i, g in enumerate(grupos))
        (rd / "cola.html").write_text(doc(pgs), encoding="utf-8")
        pg.goto((rd / "cola.html").resolve().as_uri()); pg.wait_for_timeout(1500)
        if not pg.evaluate("""document.fonts.check('700 100px "TT Modernoir"')"""):
            raise SystemExit('ERRO: a família "TT Modernoir" não está disponível. Ative no '
                             'Creative Cloud (Fontes) e rode de novo, senão a cola sai com a fonte errada.')
        sobra = pg.evaluate("""() => [...document.querySelectorAll('.corpo')].map(c => {
            const u = c.lastElementChild; return c.clientHeight - (u ? u.offsetTop + u.offsetHeight : 0); })""")
        saida = rd / "cola"; saida.mkdir(exist_ok=True)
        for f in saida.glob("*.png"): f.unlink()
        for i, el in enumerate(pg.query_selector_all(".pg"), 1):
            el.screenshot(path=str(saida / f'cola-{L["arquivo"]}-{i:02d}.png'))
        b.close()
    (rd / "cola-medida.html").unlink(missing_ok=True)
    print(f'{len(passos)} passos -> {len(grupos)} png em {saida}')
    for i, s in enumerate(sobra, 1):
        print(f"  pagina {i}: {'ESTOUROU ' + str(-s) + 'px' if s < 0 else f'folga {s}px'}")

if __name__ == "__main__":
    main()
