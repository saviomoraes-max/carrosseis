# Gera os 4 artboards 9:16 (1080x1920) do ebook no Reconecta Design System (dossiê). Reexecutar após mudar valores.
import pathlib, json
b64 = pathlib.Path("tmp/ttmod.b64").read_text().strip()
HEAD = '''<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap">
  <style>
    @font-face { font-family: "TT Modernoir"; src: url("data:font/ttf;base64,FONTB64") format("truetype"); font-weight: 700; font-style: normal; }
    body { margin: 0; background: #161616; }
    a { color: #eece66; } a:hover { color: #eed9bd; }
  </style>
</helmet>
'''.replace("FONTB64", b64)
TAIL = '</x-dc>\n</body>\n</html>\n'
MONO = "font-family: 'Space Mono', ui-monospace, Menlo, monospace;"
DISP = "font-family: 'TT Modernoir', Impact, sans-serif;"
BODY = "font-family: Inter, -apple-system, 'Helvetica Neue', Arial, sans-serif;"
W_, H_ = 1080, 1920
# escala 9:16 nativa: chrome do sistema; leitura no celular (1080 -> ~390px) pede corpo 38px
BODY_PX, BODY_LH = 38, 1.45; H2 = 66; PUNCH = 78; FRASE = 44; SUB = 33; KICK = 22; STACK = 42

def rec_hud(hud):
    return f'''<div style="position: absolute; left: 64px; top: 70px; width: 11px; height: 11px; border-radius: 50%; background-color: #d3111a;"></div>
<span style="position: absolute; left: 84px; top: 62px; {MONO} font-weight: 400; font-size: 20px; line-height: 100%; letter-spacing: 0.16em; color: rgba(238,217,189,0.8); text-transform: uppercase; white-space: nowrap;">REC</span>
<span style="position: absolute; right: 64px; top: 63px; {MONO} font-weight: 400; font-size: 18px; line-height: 100%; letter-spacing: 0.18em; color: rgba(238,206,102,0.65); text-transform: uppercase; white-space: nowrap; text-align: right;">{hud}</span>
'''
BARS = [[0,2],[7,3],[15,1],[21,2],[28,3],[36,2],[43,1],[49,3],[57,2],[64,1],[70,2],[77,3],[85,1],[91,2]]
def barcode():
    return '<div style="position: relative; width: 128px; height: 34px;">' + "".join(f'<div style="position: absolute; left: {l}px; top: 0px; width: {w}px; height: 34px; background-color: rgba(238,217,189,0.8);"></div>' for l,w in BARS) + '</div>'
def slugspan(t): return f'<span style="{MONO} font-weight: 400; font-size: 18px; line-height: 100%; letter-spacing: 0.14em; color: rgba(238,217,189,0.62); text-transform: uppercase; white-space: nowrap;">{t}</span>'
def rodape(slug, num=None, bc=True):
    return f'''<div style="position: absolute; left: 64px; right: 64px; bottom: 64px; display: flex; align-items: flex-end; justify-content: space-between;">
  <div style="display: flex; flex-direction: column; gap: 16px;">{barcode() if bc else ""}{slugspan(slug)}</div>
  {slugspan(num) if num else ""}
</div>
'''
def kicker(t, size=KICK, color="#eece66"):
    return f'<span style="{MONO} font-weight: 400; font-size: {size}px; line-height: 100%; letter-spacing: 0.22em; color: {color}; text-transform: uppercase; white-space: pre-line;">{t}</span>'
def p(t): return f'<p style="margin: 0; {BODY} font-weight: 400; font-size: {BODY_PX}px; line-height: {BODY_LH}; color: rgba(238,217,189,0.9);">{t}</p>'
def disp(t, size, color="#eed9bd", extra=""): return f'<span style="{DISP} font-weight: 700; font-size: {size}px; line-height: 0.98; color: {color}; text-transform: uppercase; white-space: pre-line; {extra}">{t}</span>'
def sp(h=STACK): return f'<div style="height: {h}px;"></div>'
ENF = 'style="color: #eece66;"'
SLUG = "Script 715 · Ana Luiza · Reconecta"
def page(inner): return HEAD + f'<div style="position: relative; width: {W_}px; height: {H_}px; overflow: hidden; background-color: #161616;">\n{inner}</div>\n' + TAIL

capa = page(rec_hud("Caso Nº 715 · Atendimento") + f'''
  <div style="position: absolute; left: 64px; top: 220px; width: 952px; display: flex; flex-direction: column; align-items: flex-start;">
    {kicker("Arquivo confidencial · WhatsApp")}{sp(22)}
    {disp("Script 715", 220)}{sp(30)}
    {disp("7 passos para 1 consulta\na cada 5 contatos.", 78)}{sp(36)}
    <span style="{BODY} font-weight: 500; font-size: {SUB}px; line-height: 1.32; color: rgba(238,217,189,0.9); width: 820px; white-space: pre-line;">O script de atendimento que a gente usa nas clínicas da mentoria, do primeiro oi ao comprovante do PIX.</span>
  </div>
  <div style="position: absolute; left: 64px; bottom: 210px; display: flex; flex-direction: column; gap: 14px;">{kicker("Por", 18, "rgba(238,206,102,0.65)")}{disp("Ana Luiza", 52)}</div>
  <img src="logo-cream.svg" style="position: absolute; right: 64px; bottom: 200px; width: 140px; height: auto; display: block;">
  {rodape("Script 715 · Reconecta · 2026")}
''')

abertura = page(rec_hud("Script 715 · Passo 03 / 07") + f'''
  {disp("03", 640, "rgba(238,217,189,0.12)", "position: absolute; left: 56px; top: 260px; line-height: 0.85;")}
  <div style="position: absolute; left: 64px; bottom: 260px; width: 952px; display: flex; flex-direction: column; align-items: flex-start;">
    {kicker("Prova nº 03 · Passo 3 de 7")}{sp(22)}
    {disp("Presente\ninaceitável.", 120)}{sp(30)}
    <span style="{BODY} font-weight: 500; font-size: {SUB}px; line-height: 1.32; color: rgba(238,217,189,0.9); width: 760px; white-space: pre-line;">Onde a paciente para de achar que dá pra deixar pra depois.</span>
  </div>
  {rodape(SLUG, "22")}
''')

def miolo(chrome=True, num="23"):
    return page((rec_hud("Script 715 · Passo 03 / 07") if chrome else "") + f'''
  <div style="position: absolute; left: 64px; top: 150px; width: 952px; display: flex; flex-direction: column; align-items: flex-start;">
    {kicker("Passo 03 · Presente inaceitável", 18, "rgba(238,206,102,0.65)")}{sp(36)}
    {disp("A pergunta que ninguém faz.", H2)}{sp(30)}
    <div style="display: flex; flex-direction: column; gap: 28px; width: 952px;">
      {p("Eu vou te contar uma coisa que eu vi acontecer nas mais de três mil clínicas que passaram por aqui. A paciente chega no WhatsApp, descreve a papada, a flacidez, o bigode chinês, e a gente responde explicando o procedimento. Parece atendimento. Não é.")}
      {p(f'O problema dela <span {ENF}>não começou hoje</span>. Aquela papada tá lá há dois, três anos. Então a pergunta que importa não é "o que você quer resolver". É: <span {ENF}>por que agora?</span>')}
    </div>
    {sp(48)}
    <div style="display: flex; flex-direction: column; gap: 18px; width: 952px;">
      {kicker("Frase pronta", 18)}
      <span style="{BODY} font-weight: 500; font-size: {FRASE}px; line-height: 1.36; color: #eed9bd;">"Posso estar enganada, mas parece que isso não começou agora. Antes não parecia ser uma prioridade, e agora parece ser. Aconteceu alguma coisa?"</span>
    </div>
    {sp(48)}
    <div style="display: flex; flex-direction: column; gap: 28px; width: 952px;">
      {p("Repara que eu não afirmei nada. Eu deixei ela me contar. E quando ela conta, ela se convence sozinha de que não dá mais pra esperar. Isso é o passo inteiro.")}
    </div>
    {sp(48)}
    {disp("Quem faz a pergunta\nconduz a conversa.", PUNCH)}
  </div>
  {rodape(SLUG, num, bc=chrome)}
''')

pathlib.Path("Capa.dc.html").write_text(capa)
pathlib.Path("Abertura.dc.html").write_text(abertura)
pathlib.Path("Main.dc.html").write_text(miolo(True))
pathlib.Path("MioloDiscreto.dc.html").write_text(miolo(False))
c = json.loads(pathlib.Path("canvas.json").read_text())
xs = {"Capa.dc.html":0, "Abertura.dc.html":1180, "Main.dc.html":2360, "MioloDiscreto.dc.html":3540}
for a in c["artboards"]:
    a["x"] = xs[a["file"]]; a["w"] = W_; a["h"] = H_
c["annotations"][0]["text"] = c["annotations"][0]["text"].replace("A4 em 794×1123.", "Formato 9:16 em 1080×1920 (leitura no celular).")
pathlib.Path("canvas.json").write_text(json.dumps(c, ensure_ascii=False, indent=2))
print("artboards 9:16 ok")
