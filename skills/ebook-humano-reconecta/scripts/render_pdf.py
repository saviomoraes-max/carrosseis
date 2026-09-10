#!/usr/bin/env python3
"""Compila ebooks/<slug>/manuscrito/*.md em PDF A4 no Reconecta Design System (dossiê: Obsidian, Pearl, Gold, REC).

Convenções do markdown do manuscrito:
  front matter YAML: numero ("03"), kicker ("Passo 3 de 7"), titulo, subtitulo, hud ("Script 715 · Passo 03 / 07"), prova ("Prova nº 03")
  # Título -> página de abertura (não repete no miolo) | ## Seção -> display | ### -> h3
  :::frase ... :::  frase pronta   :::punch ... :::  página inteira   :::pergunta ... :::  página inteira   :::cena ... ::: (balões ELA:/VOCÊ:)   :::evite ... :::   :::grafico <tipo> [param] ... ::: (ver graficos.py)
  «texto» ênfase Gold (só cor)     - item / 1. item listas só onde a estrutura pede
livro.json: arquivo, titulo, selo, titulo_capa (com \n), subtitulo, autor, kicker_capa, hud_capa, rodape, hud, ds (pasta do design system)
Uso: python3 render_pdf.py ebooks/<slug> [--so-html] [--provas]
"""
import shutil
import json, re, sys, pathlib, html, subprocess
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import graficos
RAIZ_SKILL = pathlib.Path(__file__).resolve().parent
DS_DEFAULT = "/Volumes/SSD kenipe/inbox/Reconecta Design System"

def front_matter(txt):
    m = re.match(r"^---\n(.*?)\n---\n", txt, re.S); meta = {}
    if m:
        for ln in m.group(1).splitlines():
            if ":" in ln: k, v = ln.split(":", 1); meta[k.strip()] = v.strip().strip('"').strip('“”')
        txt = txt[m.end():]
    return meta, txt

def inline(s):
    s = html.escape(s, quote=False)
    # [texto](url): o destino leva os UTMs, a leitora vê só o domínio. Num produto pago,
    # etiquetar o próprio ebook como "material-rico" na cara de quem comprou é o detalhe
    # que a banca chamou de pior do livro.
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
               lambda m: f'<a class="ref" href="{m.group(2)}">{m.group(1)}</a>', s)
    s = re.sub(r"«(.+?)»", r'<span class="enf">\1</span>', s)
    s = re.sub(r"\b(capítulo|Capítulo) (\d{1,2})\b", lambda m: f'<a class="ref" href="#cap-{int(m.group(2)):02d}">{m.group(1)} {m.group(2)}</a>', s)
    s = re.sub(r"\b(anexo|Anexo) ([A-D])\b", lambda m: f'<a class="ref" href="#cap-{m.group(2)}">{m.group(1)} {m.group(2)}</a>', s)
    return s

def bloco_cena(linhas):
    """Cena vira transcrição de WhatsApp: balão da paciente à esquerda, o seu à direita."""
    out = ['<div class="chat">']
    for ln in linhas:
        m = re.match(r"^(ELA|PACIENTE|VOCÊ|VOCE|DOUTORA):\s*(.*)$", ln.strip(), re.I)
        if not m: continue
        quem = m.group(1).upper(); voce = quem in ("VOCÊ", "VOCE", "DOUTORA")
        out.append(f'<div class="msg {"voce" if voce else "ela"}"><span class="kicker lbl">{"Você" if voce else "Paciente"}</span><p>{inline(m.group(2))}</p></div>')
    out.append("</div>"); return "\n".join(out)

def bloco_caso(linhas):
    """Catálogo de objeção vira cartão: o que ela manda, o que perde, o que continua.

    Antes isso era andaime em prosa ("A paciente diz X", "Se quiser perder a paciente:"),
    repetido a cada entrada. Como rótulo, some do texto medido e vira consulta rápida.
    """
    slots = {"ela": [], "perde": [], "responde": []}
    atual = None
    for ln in linhas:
        m = re.match(r"^(ela|perde|responde):\s*(.*)$", ln.strip(), re.I)
        if m:
            atual = m.group(1).lower(); slots[atual].append(m.group(2).strip())
        elif ln.strip() and atual:
            slots[atual][-1] += " " + ln.strip()
    if not slots["ela"] and not slots["responde"]:
        return ""
    linha = lambda cls, rot, ps: (f'<div class="lin {cls}"><span class="kicker lbl">{rot}</span>'
                                  + "".join(f"<p>{inline(x)}</p>" for x in ps) + "</div>") if ps else ""
    return ('<div class="caso">'
            + linha("ela", "Ela manda", slots["ela"])
            + linha("perde", "Se responder assim, perde", slots["perde"])
            + linha("responde", "O que continua a conversa", slots["responde"])
            + "</div>")

BLOCOS = {"frase", "cena", "caso", "punch", "pergunta", "grafico", "evite"}

def md_para_html(txt, nome_arquivo="?"):
    out, i, linhas = [], 0, txt.splitlines(); par, lista = [], None
    def fecha_par():
        nonlocal par
        if par: out.append("<p>" + inline(" ".join(par)) + "</p>"); par = []
    def fecha_lista():
        nonlocal lista
        if lista: out.append(f"</{lista}>"); lista = None
    while i < len(linhas):
        ln = linhas[i]
        if ln.startswith(":::"):
            fecha_par(); fecha_lista(); tipo = ln[3:].strip(); j = i + 1; corpo = []
            # Cerca de FECHAMENTO com texto colado na mesma linha ("::: E aí ela responde")
            # era engolida CALADA: o laço abaixo não a reconhecia como fechamento, seguia até
            # a cerca seguinte e comia o parágrafo e o bloco inteiro. Custou um capítulo
            # incompleto no PDF pago. A checagem tem de estar DENTRO do laço, que é onde a
            # linha malformada passa.
            while j < len(linhas) and linhas[j].strip() != ":::":
                if linhas[j].lstrip().startswith(":::"):
                    raise SystemExit(
                        f"ERRO em {nome_arquivo}: dentro do bloco ':::{tipo}' há uma linha que "
                        f"começa com ':::' e não é cerca de fechamento.\n"
                        f"  linha {j+1}: {linhas[j][:110]}\n"
                        f"  conserte pondo ':::' sozinho na linha e o texto no parágrafo de baixo.")
                corpo.append(linhas[j]); j += 1
            if j >= len(linhas):
                raise SystemExit(f"ERRO em {nome_arquivo}: bloco ':::{tipo}' aberto e nunca fechado.")
            if tipo == "cena": out.append(bloco_cena(corpo))
            elif tipo == "caso": out.append(bloco_caso(corpo))
            elif tipo == "frase":
                ps = "".join(f"<p>{inline(p.strip())}</p>" for p in "\n".join(corpo).split("\n\n") if p.strip())
                out.append(f'<div class="frase"><span class="kicker xs">Frase pronta</span>{ps}</div>')
            elif tipo == "punch": out.append(f'<div class="punch inteira" data-kicker="Prova">{inline(" ".join(c.strip() for c in corpo if c.strip()))}</div>')
            elif tipo == "pergunta": out.append(f'<div class="pergunta inteira" data-kicker="Pergunta em aberto">{inline(" ".join(c.strip() for c in corpo if c.strip()))}</div>')
            elif tipo.startswith("grafico"):
                partes = tipo.split(); out.append(graficos.render(partes[1] if len(partes) > 1 else "", " ".join(partes[2:]) if len(partes) > 2 else "", corpo))
            elif tipo == "evite": out.append('<div class="evite"><span class="kicker xs mute">O que evitar</span>' + md_para_html("\n".join(corpo), nome_arquivo) + "</div>")
            i = j + 1; continue
        if ln.startswith("# "): i += 1; continue
        if ln.startswith("## "): fecha_par(); fecha_lista(); out.append(f'<h2 class="disp">{inline(ln[3:])}</h2>'); i += 1; continue
        if ln.startswith("### "): fecha_par(); fecha_lista(); out.append(f"<h3>{inline(ln[4:])}</h3>"); i += 1; continue
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", ln)
        if m:
            fecha_par(); tag = "ol" if m.group(2)[0].isdigit() else "ul"
            if lista != tag: fecha_lista(); out.append(f"<{tag}>"); lista = tag
            out.append(f"<li>{inline(m.group(3))}</li>"); i += 1; continue
        if not ln.strip(): fecha_par(); fecha_lista(); i += 1; continue
        par.append(ln.strip()); i += 1
    fecha_par(); fecha_lista(); return "\n".join(out)

def chrome(hud): return f'<div class="rec-dot"></div><span class="rec">REC</span><span class="hud">{html.escape(hud)}</span>'
def rodape(slug, num="", bc=True):
    bars = "".join(f'<i style="left:{l}px;width:{w}px"></i>' for l, w in [[0,2],[7,3],[15,1],[21,2],[28,3],[36,2],[43,1],[49,3],[57,2],[64,1],[70,2],[77,3],[85,1],[91,2]])
    return f'<div class="rodape"><div class="col">{"<div class=\"barcode\">"+bars+"</div>" if bc else ""}<span class="slug">{html.escape(slug)}</span></div><span class="pn">{num}</span></div>'

def compilar(raiz, so_html=False, provas=False):
    raiz = pathlib.Path(raiz); L = json.loads((raiz / "livro.json").read_text()); ds = L.get("ds", DS_DEFAULT)
    tpl = (RAIZ_SKILL / "template.html").read_text(); slug = L["rodape"]; partes = []
    partes.append(f'''<section class="pg capa">{chrome(L["hud_capa"])}<div class="stack"><span class="kicker">{html.escape(L["kicker_capa"])}</span><div class="sp22"></div>
<span class="disp selo">{html.escape(L["selo"])}</span><div class="sp22"></div><span class="disp tit">{html.escape(L["titulo_capa"])}</span><div class="sp30"></div><span class="sub">{inline(L["subtitulo"])}</span></div>
{('<div class="autor"><span class="kicker sm">Por</span><span class="disp" style="font-size:52px">' + html.escape(L["autor"]) + "</span></div>") if L.get("autor") else ""}
<img class="logo" src="file://{ds}/assets/logo-cream.svg">{rodape(L.get("rodape_capa", slug), "", True)}</section>''')
    caps = sorted((raiz / "manuscrito").glob("*.md")); metas = [front_matter(c.read_text(encoding="utf-8")) for c in caps]
    # sumário vem do livro.json (mapa aprovado); capítulo já escrito ganha número de página, os outros ficam sem
    por_num = {m.get("numero",""): i for i, (m, _) in enumerate(metas)}
    plano = L.get("sumario") or [{"numero": m.get("numero",""), "titulo": m.get("titulo","")} for m, _ in metas]
    sum_html = "".join(f'<a class="lin" href="#cap-{html.escape(e["numero"])}"{(" data-cap=%d" % por_num[e["numero"]]) if e["numero"] in por_num else ""}><span class="n">{html.escape(e["numero"])}</span><span class="t"{"" if e["numero"] in por_num else " style=opacity:.45"}>{inline(e["titulo"])}</span><span class="pg-num"></span></a>' for e in plano)
    partes.append(f'<section class="pg sumario">{chrome(L["hud"])}<div class="conteudo"><span class="kicker sm topo">Sumário</span>{sum_html}</div>{rodape(slug, "", True)}</section>')
    # Páginas-marcador de parte: navegação, não conteúdo. Rótulo e título vêm do livro.json;
    # a lista de capítulos de cada parte é derivada do próprio sumário.
    divisoes = L.get("partes") or []
    nums_plano = [e["numero"] for e in plano]
    abre_parte = {}
    for j, pa in enumerate(divisoes):
        ini = nums_plano.index(pa["de"])
        fim = nums_plano.index(divisoes[j + 1]["de"]) if j + 1 < len(divisoes) else len(nums_plano)
        abre_parte[pa["de"]] = (pa, plano[ini:fim])

    for i, (m, corpo) in enumerate(metas):
        hud = m.get("hud", L["hud"]); num = m.get("numero", "")
        if num in abre_parte:
            pa, caps_parte = abre_parte[num]
            itens = "".join(f'<div class="it"><span class="n">{html.escape(e["numero"])}</span>'
                            f'<span class="t">{inline(e["titulo"])}</span></div>' for e in caps_parte)
            partes.append(f'<section class="pg parte">{chrome(L["hud"])}'
                f'<span class="marca">{html.escape(pa["rotulo"].split()[-1])}</span>'
                f'<div class="stack"><span class="kicker">{html.escape(pa["rotulo"])}</span><div class="sp22"></div>'
                f'<h1 class="disp">{inline(pa["titulo"])}</h1></div>'
                f'<div class="lista">{itens}</div>{rodape(slug, "", True)}</section>')
        partes.append(f'''<section class="pg abertura" id="cap-{html.escape(num)}" data-cap="{i}">{chrome(hud)}<span class="disp" style="position:absolute;left:56px;top:260px;font-size:640px;line-height:.85;color:rgba(238,217,189,.12)">{html.escape(num)}</span>
{('<div class="rail-abertura">' + graficos.rail(int(re.search(r"\d+", m.get("kicker","")).group()), mini=True) + '</div>') if re.match(r"(?i)^passo\s*\d+$", m.get("kicker","").strip()) else ''}
<div class="stack"><span class="kicker">{html.escape(m.get("prova", m.get("kicker","")))}</span><div class="sp22"></div><h1 class="disp">{inline(m.get("titulo",""))}</h1><div class="sp30"></div><span class="sub">{inline(m.get("subtitulo",""))}</span></div>{rodape(slug, "", True)}</section>''')
        partes.append(f'<div class="fonte" data-hud="{html.escape(hud)}" data-kicker="{html.escape(m.get("kicker",""))}" data-titulo="{html.escape(m.get("titulo",""))}">{md_para_html(corpo, caps[i].name)}</div>')
    cc = L.get("contracapa")
    if cc:
        partes.append(f'<section class="pg contracapa">{chrome(L["hud"])}'
            f'<div class="stack"><span class="kicker">{html.escape(cc["kicker"])}</span><div class="sp22"></div>'
            f'<h1 class="disp">{inline(cc["titulo"])}</h1><div class="sp30"></div>'
            f'<span class="sub">{inline(cc["texto"])}</span></div>'
            f'<div class="link"><a class="ref" href="{html.escape(cc["link"])}">{html.escape(cc.get("link_texto", cc["link"]))}</a></div>'
            f'<img class="logo" src="file://{ds}/assets/logo-cream.svg">'
            f'{rodape(L.get("rodape_capa", slug), "", True)}</section>')

    out = tpl
    for k, v in {"titulo": L["titulo"], "corpo": "\n".join(partes), "ds": "file://" + ds,
                 "rodape_json": json.dumps(slug, ensure_ascii=False), "hud_json": json.dumps(L["hud"], ensure_ascii=False), "css_graficos": graficos.CSS}.items():
        out = out.replace("{{"+k+"}}", v)
    rd = raiz / "render"; rd.mkdir(exist_ok=True); (rd / "livro.html").write_text(out, encoding="utf-8")

    # CONFERÊNCIA FONTE x RENDER. Nada no pipeline comparava as duas coisas, e por isso um
    # capítulo saiu incompleto no PDF pago sem nenhum instrumento acusar: o detector mede a
    # prosa do markdown, o linter mede o markdown, o leitor cego lê o markdown. Todos liam a
    # fonte. Se o render come um bloco, só um leitor humano descobre, e tarde.
    esperado, achado = {}, {}
    marca = {"frase": 'class="frase"', "cena": 'class="chat"', "caso": 'class="caso"',
             "evite": 'class="evite"', "punch": "class=\"punch", "pergunta": "class=\"pergunta",
             "grafico": 'class="g '}
    for c in caps:
        for ln in c.read_text(encoding="utf-8").split("\n"):
            if ln.startswith(":::") and ln.strip() != ":::":
                k = ln[3:].strip().split()[0]
                if k in marca: esperado[k] = esperado.get(k, 0) + 1
    for k, m in marca.items():
        achado[k] = out.count(m)
    faltando = {k: (esperado[k], achado.get(k, 0)) for k in esperado if achado.get(k, 0) < esperado[k]}
    if faltando:
        det = "; ".join(f"{k}: {e} no markdown, {a} no render" for k, (e, a) in faltando.items())
        raise SystemExit(f"ERRO: o render perdeu bloco pelo caminho ({det}). "
                         f"Quase sempre é cerca ':::' malformada. Não publique este PDF.")
    print("fonte x render: " + ", ".join(f"{k} {esperado[k]}" for k in sorted(esperado)))
    if so_html: return
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto((rd / "livro.html").resolve().as_uri()); pg.wait_for_selector("body[data-paginado]"); pg.wait_for_timeout(1200)
        if pg.evaluate("document.body.dataset.semDisplay === '1'"):
            raise SystemExit(
                "ERRO: a família \"TT Modernoir\" não está disponível pro Chromium, e o livro sairia\n"
                "  com a fonte de fallback sem avisar. Ative a TT Modernoir no Adobe Fonts\n"
                "  (app Creative Cloud > Fontes > Adicionar fontes) e rode de novo.")
        n = pg.evaluate("document.querySelectorAll('.pg').length")
        # Auditoria de ocupação: página de miolo quase vazia é órfã e some no olho de quem
        # folheia 130 provas. Páginas de abertura, parte, capa, sumário, contracapa e as
        # de frase inteira são vazias POR DESENHO e ficam fora da conta.
        orfas = pg.evaluate("""() => {
          const fora = ['capa','sumario','abertura','parte','contracapa','inteira-pg'];
          const out = [];
          [...document.querySelectorAll('.pg')].forEach((p, i) => {
            if (fora.some(c => p.classList.contains(c))) return;
            const c = p.querySelector('.conteudo'); if (!c) return;
            const u = c.lastElementChild; if (!u) { out.push([i + 1, 0]); return; }
            const ocupado = u.offsetTop + u.offsetHeight;
            const pct = ocupado / c.clientHeight;
            if (pct < 0.35) out.push([i + 1, Math.round(pct * 100)]);
          });
          return out;
        }""")
        # índice de página por capítulo, pra exportar a cola do anexo A separada
        indice = pg.evaluate("""() => {
          const pgs = [...document.querySelectorAll('.pg')]; const m = {};
          pgs.forEach((p, i) => { const ab = p.id && p.id.startsWith('cap-') ? p.id.slice(4) : null; if (ab && !(ab in m)) m[ab] = i; });
          return m;
        }""")
        pg.pdf(path=str(rd / f'{L["arquivo"]}.pdf'), width="1080px", height="1920px", print_background=True, prefer_css_page_size=True, margin={"top":"0","bottom":"0","left":"0","right":"0"})
        b.close()
    print("páginas:", n); print("pdf:", rd / f'{L["arquivo"]}.pdf')
    if orfas:
        print(f"ATENÇÃO: {len(orfas)} página(s) de miolo abaixo de 35% de ocupação:",
              ", ".join(f"pág {p} ({o}%)" for p, o in orfas))
    else:
        print("ocupação: nenhuma página de miolo órfã")
    if provas:
        prov = rd / "provas"; prov.mkdir(exist_ok=True)
        for f in prov.glob("pag*.png"): f.unlink()
        subprocess.run([sys.executable, str(RAIZ_SKILL / "provas_pdf.py"), str(rd / f'{L["arquivo"]}.pdf'), str(prov)], check=True)
        subprocess.run([sys.executable, str(RAIZ_SKILL / "preview_provas.py"), str(rd)], check=True)
        (rd / "indice-paginas.json").write_text(json.dumps(indice, ensure_ascii=False, indent=2))
        # A cola sai por cola_png.py: recortar página do PDF entregaria o corpo de leitura
        # (38px) numa peça que é de consulta rápida. É outra tipografia, outra montagem.
        subprocess.run([sys.executable, str(RAIZ_SKILL / "cola_png.py"), str(raiz)], check=True)

if __name__ == "__main__":
    a = sys.argv[1:]; compilar(a[0], so_html="--so-html" in a, provas="--provas" in a)
