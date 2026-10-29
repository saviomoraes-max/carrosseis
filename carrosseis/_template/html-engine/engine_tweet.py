#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Carrossel em formato "print de tweet" — um tweet por slide, fundo claro.

Pedido do Sávio (15/10/2026): fundo claro, foto da Ana como avatar com nome e @,
um tweet por slide. Nome e foto vêm da conta real (@anadareconecta, nome
"Ana, da RECONECTA"; avatar = foto de perfil baixada pela Graph API).

Regras do formato:
  - nada de curtida/retweet/visualização: seria número inventado
  - selo de verificado só porque a conta É verificada (confirmado pelo Sávio, 15/10)
  - linha de data e hora embaixo do tweet ("quando" no autor ou no tweet)
  - slide 1 é a capa: mesma cara de tweet, letra maior
  - tweet com imagem (prova) mostra a imagem como mídia anexada, cantos redondos
  - tweet com VÍDEO ("video" + "poster"): o card é desenhado com o poster no lugar da
    mídia, a caixa é medida no navegador e o ffmpeg grava o vídeo exatamente ali, com
    os mesmos cantos redondos -> slide_N.mp4 (pedido do Sávio, 19/10: "um dos cards
    tem que ter um vídeo do desfile no mesmo estilo dos cards que tem foto")

Entrada (tweets.json):
  {"autor": {"nome": "...", "usuario": "...", "avatar": "img/avatar.jpg",
             "verificado": true, "quando": "10:24 AM · 15 de out de 2026"},
   "tweets": [{"t": "texto", "capa": true}, {"t": "texto", "img": "img/prova.png"}]}

Uso:
  python3 engine_tweet.py <tweets.json> <pasta_de_saida>
"""
import base64, html, json, os, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTES = os.path.join(os.path.dirname(AQUI), "fonts")
W, H = 1080, 1350
MARGEM = 84
LARGURA = W - 2 * MARGEM
PISO, TETO = 60, H - 60          # faixa segura do bloco
TOPO = 250                       # onde o cabeçalho começa, igual em todo slide


def _b64(p):
    return base64.b64encode(open(p, "rb").read()).decode()


def _uri(caminho, base):
    p = caminho if os.path.isabs(caminho) else os.path.join(base, caminho)
    if not os.path.exists(p):
        raise SystemExit(f"imagem faltando: {p}")
    ext = os.path.splitext(p)[1].lower().lstrip(".")
    return f"data:image/{'jpeg' if ext in ('jpg', 'jpeg') else ext};base64,{_b64(p)}"


def _fonte(familia, arq, peso):
    return (f"@font-face{{font-family:'{familia}';font-weight:{peso};"
            f"src:url(data:font/truetype;base64,{_b64(os.path.join(FONTES, arq))}) format('truetype');}}")


CSS = f"""
{_fonte('Inter', 'Inter-Regular.ttf', 400)}
{_fonte('Inter', 'Inter-Medium.ttf', 500)}
{_fonte('Inter', 'Inter-Bold.ttf', 700)}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#fff;}}
.slide{{position:relative;width:{W}px;height:{H}px;background:#ffffff;overflow:hidden;
  font-family:'Inter',sans-serif;color:#0f1419;}}
/* topo FIXO: o cabeçalho não pode pular de altura entre um slide e outro ao arrastar */
.bloco{{position:absolute;left:{MARGEM}px;width:{LARGURA}px;top:{TOPO}px;}}
.cab{{display:flex;align-items:center;gap:26px;margin-bottom:38px;}}
.av{{width:118px;height:118px;border-radius:50%;object-fit:cover;flex-shrink:0;}}
.nome{{font-weight:700;font-size:40px;line-height:1.15;letter-spacing:-.01em;}}
.user{{font-weight:400;font-size:36px;line-height:1.2;color:#536471;margin-top:4px;}}
.txt{{font-weight:400;font-size:56px;line-height:1.3;letter-spacing:-.012em;
  white-space:pre-wrap;word-wrap:break-word;}}
.capa .txt{{font-size:74px;line-height:1.2;letter-spacing:-.02em;font-weight:500;}}
/* print largo e de letra miúda: a mídia vaza a coluna pra ganhar leitura */
.midia{{display:block;width:calc(100% + 2*{MARGEM-24}px);margin-left:-{MARGEM-24}px;margin-top:40px;border-radius:30px;
  border:1.5px solid #cfd9de;overflow:hidden;background:#f7f9f9;}}
.midia img{{display:block;width:100%;height:auto;}}
.capa.com-midia .txt{{font-size:60px;line-height:1.22;}}  /* capa com foto: letra menor pra caber a foto */
.midia.estreita{{width:fit-content;margin-left:auto;margin-right:auto;}}
.midia.estreita img{{width:auto;}}
.linha-nome{{display:flex;align-items:center;gap:8px;}}
.selo{{width:42px;height:42px;flex-shrink:0;}}
.quando{{font-weight:400;font-size:34px;line-height:1.2;color:#536471;margin-top:40px;}}
"""


# selo de verificado do X (o desenho público do ícone, azul #1d9bf0)
SELO = ('<svg class="selo" viewBox="0 0 22 22"><path fill="#1d9bf0" d="M20.396 11c-.018-.646-.215-1.275-.57-1.816'
        '-.354-.54-.852-.972-1.438-1.246.223-.607.27-1.264.14-1.897-.131-.634-.437-1.218-.882-1.687-.47-.445-1.053-.75'
        '-1.687-.882-.633-.13-1.29-.083-1.897.14-.273-.587-.704-1.086-1.245-1.44S11.647 1.62 11 1.604c-.646.017-1.273.213'
        '-1.813.568s-.969.854-1.24 1.44c-.608-.223-1.267-.272-1.902-.14-.635.13-1.22.436-1.69.882-.445.47-.749 1.055-.878'
        ' 1.688-.13.633-.08 1.29.144 1.896-.587.274-1.087.705-1.443 1.245-.356.54-.555 1.17-.574 1.817.02.647.218 1.276.574'
        ' 1.817.356.54.856.972 1.443 1.245-.224.606-.274 1.263-.144 1.896.13.634.433 1.218.877 1.688.47.443 1.054.747 1.687'
        '.878.633.132 1.29.084 1.897-.136.274.586.705 1.084 1.246 1.439.54.354 1.17.551 1.816.569.647-.016 1.276-.213 1.817'
        '-.567s.972-.854 1.245-1.44c.604.239 1.266.296 1.903.164.636-.132 1.22-.447 1.68-.907.46-.46.776-1.044.908-1.681s'
        '.075-1.299-.165-1.903c.586-.274 1.084-.705 1.439-1.246.354-.54.551-1.17.569-1.816zM9.662 14.85l-3.429-3.428 1.293'
        '-1.302 2.072 2.072 4.4-4.794 1.347 1.246z"/></svg>')


def html_tweet(tw, autor, base):
    av = _uri(autor["avatar"], base)
    # print alto (conversa empilhada): "img_altura" trava a altura e a mídia fica estreita
    if tw.get("video"):                       # o poster ocupa o lugar; o vídeo entra depois
        tw = dict(tw, img=tw["poster"])
    alt = tw.get("img_altura")
    corte = tw.get("midia_altura")            # quadrado 1080 (22/10): largura toda, altura fixa, foto cortada (cover)
    if corte:
        ajuste = "contain;background:#000" if tw.get("midia_conter") else "cover"   # conter: vídeo vertical como no X, barras pretas
        midia = (f'<div class="midia"><img src="{_uri(tw["img"], base)}" style="height:{corte}px;object-fit:{ajuste};'
                 f'object-position:{tw.get("midia_pos", "center")}"></div>' if tw.get("img") else "")
    else:
        midia = (f'<div class="midia{" estreita" if alt else ""}"><img src="{_uri(tw["img"], base)}"'
                 f'{f" style=\"height:{alt}px\"" if alt else ""}></div>' if tw.get("img") else "")
    capa = (" capa" if tw.get("capa") else "") + (" com-midia" if tw.get("capa") and tw.get("img") else "")
    q = tw.get("quando") or autor.get("quando")
    quando = f'<div class="quando">{html.escape(q)}</div>' if q else ""
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body><div class="slide{capa}"><div class="bloco">'
            f'<div class="cab"><img class="av" src="{av}"><div>'
            f'<div class="linha-nome"><div class="nome">{html.escape(autor["nome"])}</div>'
            f'{SELO if autor.get("verificado") else ""}</div>'
            f'<div class="user">@{html.escape(autor["usuario"])}</div></div></div>'
            f'<div class="txt"{f" style=\"font-size:{tw['fonte_px']}px\"" if tw.get("fonte_px") else ""}>{html.escape(tw["t"])}</div>{midia}'
            f'{quando}'
            f'</div></div></body></html>')


def gravar_video(png, video, cx, destino, raio=29, audio=False, conter=False):
    """Grava o vídeo na caixa medida do card (x,y,w,h), com cantos redondos; sem áudio, a não ser com "audio": true
    no tweet (anúncio com a Ana falando, 22/10)."""
    from PIL import Image, ImageDraw
    x, y, w, h = (int(round(cx[k])) for k in ("x", "y", "w", "h"))
    w -= w % 2; h -= h % 2
    mascara = destino.replace(".mp4", "_mascara.png")
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=raio, fill=255)
    m.save(mascara)
    enq = (f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:black" if conter
           else f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}")
    filtro = (f"[1:v]{enq},format=rgba[v];"
              f"[2:v]format=gray[m];[v][m]alphamerge[vm];[0:v][vm]overlay={x}:{y}:shortest=1,format=yuv420p[out]")
    # duração TRAVADA na do clipe: a imagem e a máscara entram em loop, e sem -t o ffmpeg
    # gravou sem parar (19/10: 183 MB em 10 min antes de eu matar o processo)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                          "csv=p=0", video], capture_output=True, text=True).stdout.strip()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-t", dur, "-loop", "1", "-framerate", "30", "-i", png,
                    "-i", video, "-loop", "1", "-i", mascara, "-filter_complex", filtro,
                    "-map", "[out]"] + (["-map", "1:a?", "-c:a", "aac", "-b:a", "192k"] if audio else ["-an"]) + ["-r", "30", "-t", dur, "-c:v", "libx264", "-crf", "17",
                    "-preset", "slow", "-movflags", "+faststart", destino], check=True)
    os.remove(mascara)
    return destino


def renderizar(json_path, saida):
    from playwright.sync_api import sync_playwright
    base = os.path.dirname(os.path.abspath(json_path))
    d = json.load(open(json_path, encoding="utf-8"))
    os.makedirs(saida, exist_ok=True)
    global H, TETO, TOPO, CSS
    if d.get("altura") and d["altura"] != H:      # anúncio 1080×1080 (22/10): mesma cara, topo proporcional
        novo_topo = d.get("topo", round(TOPO * d["altura"] / H))
        CSS = CSS.replace(f"height:{H}px", f"height:{d['altura']}px").replace(f"top:{TOPO}px", f"top:{novo_topo}px")
        TOPO = novo_topo; H = d["altura"]; TETO = H - 60
    avisos = []
    # regras de 26/10/2026 (Ana Luiza + Sávio): no máximo 8 cards e capa sempre com foto
    if len(d["tweets"]) > 8:
        avisos.append(f"{len(d['tweets'])} cards: o máximo é 8 (contando capa, prova e CTA)")
    if not (d["tweets"][0].get("img") or d["tweets"][0].get("video")):
        avisos.append("capa sem foto: o 1º card precisa de uma imagem que ilustre a frase da capa")
    # punchline de comparação = vício de IA (Sávio 26/10: "me dá asco"). Tolerância zero: avisa no render.
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "agente-carrosseis"))
        import re as _re, vicio_comparacao as _vc
        for _onde, _t in _vc.textos(json_path):
            _pl = _re.sub(r"\s*\n\s*", " ", _t)
            for _rx, _nome in _vc.PADROES:
                if _re.search(_rx, _pl, _re.I):
                    avisos.append(f"{_onde}: punchline de comparação [{_nome}] — REESCREVER")
    except ImportError:
        pass
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pg = nav.new_page(viewport={"width": W, "height": H})
        for i, tw in enumerate(d["tweets"], 1):
            pg.set_content(html_tweet(tw, d["autor"], base), wait_until="networkidle")
            r = pg.evaluate("(()=>{const b=document.querySelector('.bloco').getBoundingClientRect();"
                            "return {top:b.top,bottom:b.bottom}})()")
            if r["top"] < PISO or r["bottom"] > TETO:
                avisos.append(f"slide {i}: bloco fora da faixa segura (top {r['top']:.0f}, "
                              f"bottom {r['bottom']:.0f}) — ENCURTAR O TWEET")
            png = os.path.join(saida, f"slide_{i}.png")
            pg.locator(".slide").screenshot(path=png)
            if tw.get("video"):
                cx = pg.evaluate("(()=>{const r=document.querySelector('.midia img').getBoundingClientRect();"
                                 "return {x:r.left,y:r.top,w:r.width,h:r.height}})()")
                mp4 = gravar_video(png, os.path.join(base, tw["video"]), cx,
                                   os.path.join(saida, f"slide_{i}.mp4"), audio=bool(tw.get("audio")),
                                   conter=bool(tw.get("midia_conter")))
                print(f"ok slide_{i} (vídeo {os.path.basename(mp4)})")
            else:
                print(f"ok slide_{i}")
        nav.close()
    for a in avisos:
        print("  ⚠", a)
    print("sem avisos" if not avisos else f"{len(avisos)} aviso(s)")
    return avisos


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    renderizar(sys.argv[1], sys.argv[2])
