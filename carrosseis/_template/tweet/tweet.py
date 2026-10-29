#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post estilo Twitter do @anadareconecta, do zero ao export, num comando só.

Empacotado pro time em 29/10/2026 (pedido do Sávio: "empacote esse processo e suba no git
pra eu compartilhar com o time e eles conseguirem fazer o design estilo twitter também").
O passo a passo completo (tema, copy, fotos, regras) está na skill
.claude/skills/carrossel-tweet/SKILL.md. Aqui é só a parte mecânica.

Uso:
  python3 tweet.py novo "Textão da Consulta Antecipada" [--data 2026-10-28] [--hora 12:00] [--ad AD004]
      -> cria SEM{xx}/AD{nnn} - <Título> Twitter/ com tweets.json de 8 cards, avatar, copy.md, legenda.txt
  python3 tweet.py render <pasta_do_post>
      -> slides/slide_N.png (+ .mp4 se tiver card de vídeo) e roda os detectores
  python3 tweet.py exportar <pasta_do_post>
      -> [DD] [SS] [ADnnn_N] - Título.png na raiz da pasta + _folha.png (post exportado é imutável)

Onde o post é criado: no SSD (/Volumes/SSD kenipe/estáticos/novos) se ele estiver montado;
senão em ./producao na raiz do repo (gitignorada), como manda o CLAUDE.md.
"""
import argparse, datetime as dt, glob, json, os, re, shutil, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))   # carrosseis/_template/tweet -> raiz
MOTOR = os.path.join(os.path.dirname(AQUI), "html-engine")
AGENTE = os.path.join(REPO, "agente-carrosseis")
SSD = "/Volumes/SSD kenipe/estáticos/novos"
RAIZ = SSD if os.path.isdir(SSD) else os.path.join(REPO, "producao")
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
PENDENTE = "ESCREVER"   # marca de card não escrito; o render recusa enquanto existir

AUTOR = {"nome": "Ana, da RECONECTA", "usuario": "anadareconecta",
         "avatar": "img/avatar-ana.jpg", "verificado": True}
CTA = ("Se você quer que o meu time analise o seu cenário atual e te mostre o mapa claro pra também "
       "ter 10-60 novos pacientes todo mês, comenta SUPERCASO.")

# esqueleto de 8 cards (regra de 26/10: história em 1 card, o resto é processo; máximo 8)
ESQUELETO = [
    {"capa": True, "img": "img/capa.png",
     "t": f"{PENDENTE}: capa, a frase que para o dedo. SEM ponto final"},
    {"t": f"{PENDENTE}: o caso em UM card (o que aconteceu, a frase que o processo responde)"},
    {"t": f"{PENDENTE}: processo, passo 1 (o que a comercial/doutora faz e por quê)"},
    {"t": f"{PENDENTE}: processo, passo 2"},
    {"t": f"{PENDENTE}: processo, passo 3 (pelo menos um card com frase pronta colável)"},
    {"t": f"{PENDENTE}: a objeção que a leitora vai ter (“Ai, Ana, mas e se…?”) e a resposta"},
    {"t": "Olha o que uma aluna mandou no grupo:", "img": "img/prova-1.png"},
    {"t": CTA},
]

COPY_MD = """# {sem} · {ad} · {titulo} (formato Twitter) — {quando}

**Regras:** história em 1 card, resto é processo; foto na capa; ≤8 cards; zero punchline de comparação.
**Fonte:** {pendente} Reel da Ana (data, link, alcance, envios, saves) + caminho da transcrição.
**Frase pronta:** {pendente} de qual card, e se é verbatim do Reel.
**Foto da capa:** {pendente} quem é (atriz/influenciadora/meme), de onde veio, se já foi usada antes.
**Prova:** {pendente} arquivo de origem, o que foi borrado, resultado do prints_usados.py.

(Depois do render, colar aqui o texto de cada card, como em SEM44/AD004.)
"""


def semana(d):
    return f"SEM{d.isocalendar()[1]:02d}"


def quando(d, hora):
    h, m = (int(x) for x in hora.split(":"))
    sufixo = "AM" if h < 12 else "PM"
    h12 = h % 12 or 12
    return f"{h12}:{m:02d} {sufixo} · {d.day} de {MESES[d.month - 1]} de {d.year}"


def proximo_ad(pasta_sem):
    usados = [int(m.group(1)) for p in glob.glob(os.path.join(pasta_sem, "AD*"))
              if (m := re.match(r"AD(\d+)", os.path.basename(p)))]
    return f"AD{(max(usados) + 1 if usados else 1):03d}"


def novo(a):
    d = dt.date.fromisoformat(a.data) if a.data else dt.date.today()
    sem = semana(d)
    pasta_sem = os.path.join(RAIZ, sem)
    os.makedirs(pasta_sem, exist_ok=True)
    ad = a.ad or proximo_ad(pasta_sem)
    if glob.glob(os.path.join(pasta_sem, ad + " *")):
        raise SystemExit(f"{ad} já existe em {pasta_sem}: post novo = AD novo (nunca sobrescrever)")
    titulo_pasta = " ".join(w[:1].upper() + w[1:] for w in a.titulo.split())
    pasta = os.path.join(pasta_sem, f"{ad} - {titulo_pasta} Twitter")
    os.makedirs(os.path.join(pasta, "img"))
    os.makedirs(os.path.join(pasta, "slides"))
    shutil.copy2(os.path.join(AQUI, "avatar-ana.jpg"), os.path.join(pasta, "img", "avatar-ana.jpg"))
    q = quando(d, a.hora)
    json.dump({"ad": ad, "titulo": a.titulo, "data": d.isoformat(),
               "autor": dict(AUTOR, quando=q), "tweets": ESQUELETO},
              open(os.path.join(pasta, "tweets.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(os.path.join(pasta, "legenda.txt"), "w", encoding="utf-8").write("")
    open(os.path.join(pasta, "copy.md"), "w", encoding="utf-8").write(
        COPY_MD.format(sem=sem, ad=ad, titulo=a.titulo, quando=q, pendente=PENDENTE + ":"))
    open(os.path.join(pasta, "ORIGEM.txt"), "w", encoding="utf-8").write(
        f"Ver copy.md. Motor: engine_tweet.py (via carrosseis/_template/tweet/tweet.py). "
        f"Data/hora no tweet: {q}.\n")
    print(pasta)
    print("falta: img/capa.png (foto da capa), img/prova-1.png (print anonimizado), "
          "os textos marcados ESCREVER no tweets.json e a legenda.txt")


def _detector(script, *args):
    r = subprocess.run([sys.executable, os.path.join(AGENTE, script), *args], capture_output=True, text=True)
    saida = (r.stdout + r.stderr).strip()
    return r.returncode, saida


def render(a):
    pasta = os.path.abspath(a.pasta)
    tj = os.path.join(pasta, "tweets.json")
    d = json.load(open(tj, encoding="utf-8"))
    faltando = [i for i, t in enumerate(d["tweets"], 1) if PENDENTE in t.get("t", "")]
    if faltando:
        raise SystemExit(f"cards ainda com {PENDENTE}: {faltando}")
    sys.path.insert(0, MOTOR)
    import engine_tweet
    avisos = list(engine_tweet.renderizar(tj, os.path.join(pasta, "slides")))
    leg = os.path.join(pasta, "legenda.txt")
    if not open(leg, encoding="utf-8").read().strip():
        avisos.append("legenda.txt vazia: a legenda é entregue junto com o post")
    else:
        cod, out = _detector("vicio_comparacao.py", leg)
        print("legenda / punchline de comparação:", out.splitlines()[-1] if out else "?")
        if cod:
            avisos.append("legenda com punchline de comparação:\n" + out)
        cod, out = _detector("legenda_padrao.py", leg)
        print("legenda / repetição com as últimas semanas:", out.splitlines()[-1] if out else "?")
        if "reciclada" in out:
            avisos.append("legenda repete frase de legenda recente:\n" + out)
    print()
    if avisos:
        print(f"{len(avisos)} aviso(s): corrigir e renderizar de novo antes de exportar")
        sys.exit(1)
    print("render limpo. Agora ABRA cada slide em slides/ e confira no olho antes de exportar.")


def exportar(a):
    from PIL import Image
    pasta = os.path.abspath(a.pasta)
    d = json.load(open(os.path.join(pasta, "tweets.json"), encoding="utf-8"))
    data = dt.date.fromisoformat(d["data"])
    ad, titulo = d["ad"], d["titulo"]
    pre = f"[{data.day:02d}] [{data.isocalendar()[1]:02d}] [{ad}_"
    if glob.glob(os.path.join(glob.escape(pasta), glob.escape(pre) + "*")):
        raise SystemExit("este post já foi exportado. Post exportado é imutável: post novo = pasta nova + AD novo")
    pngs = []
    for i in range(1, len(d["tweets"]) + 1):
        for ext in (".mp4", ".png"):          # card de vídeo exporta o .mp4
            src = os.path.join(pasta, "slides", f"slide_{i}{ext}")
            if os.path.exists(src):
                dst = os.path.join(pasta, f"{pre}{i}] - {titulo}{ext}")
                shutil.copy2(src, dst)
                print(os.path.basename(dst))
                break
        else:
            raise SystemExit(f"slide_{i} não renderizado: rode o render antes")
        pngs.append(os.path.join(pasta, "slides", f"slide_{i}.png"))
    # folha de conferência: todos os cards lado a lado, pra olhar a sequência de uma vez
    ims = [Image.open(p).convert("RGB") for p in pngs]
    w, h = 270, round(270 * ims[0].height / ims[0].width)
    cols = 4
    folha = Image.new("RGB", (cols * w + (cols + 1) * 12, ((len(ims) + cols - 1) // cols) * (h + 12) + 12), "#d0d4d8")
    for n, im in enumerate(ims):
        folha.paste(im.resize((w, h), Image.LANCZOS), (12 + (n % cols) * (w + 12), 12 + (n // cols) * (h + 12)))
    folha.save(os.path.join(pasta, "_folha.png"))
    print("_folha.png")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("novo")
    n.add_argument("titulo")
    n.add_argument("--data", help="dia da publicação, AAAA-MM-DD (padrão: hoje)")
    n.add_argument("--hora", default="12:00", help="hora da publicação, HH:MM (o tweet sai às 12h na grade)")
    n.add_argument("--ad", help="ADnnn; padrão: o próximo livre na semana")
    n.set_defaults(f=novo)
    r = sub.add_parser("render")
    r.add_argument("pasta")
    r.set_defaults(f=render)
    e = sub.add_parser("exportar")
    e.add_argument("pasta")
    e.set_defaults(f=exportar)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
