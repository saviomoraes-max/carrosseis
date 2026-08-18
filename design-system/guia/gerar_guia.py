# -*- coding: utf-8 -*-
import base64, os
SP = os.path.dirname(os.path.abspath(__file__))
FT = "/Users/saviomoraes/reconecta/design-system/fontes/google"

def b64(p):
    return base64.b64encode(open(p, "rb").read()).decode()

def face(fam, arq, peso):
    return (f"@font-face{{font-family:'{fam}';font-weight:{peso};font-style:normal;"
            f"font-display:block;src:url(data:font/ttf;base64,{b64(os.path.join(FT,arq))}) "
            f"format('truetype');}}")

FONTES = "".join([
    face("ArchivoBlack", "ArchivoBlack-Regular.ttf", 400),
    face("Figtree", "Figtree-Regular.ttf", 400),
    face("Figtree", "Figtree-Bold.ttf", 700),
])

LAYOUTS = [
    ("Capa", "Abre a apresentação. Título grande e uma linha que promete o que a pessoa leva daqui."),
    ("Abertura de seção", "Avisa que começou uma parte nova. Serve de respiro entre blocos longos."),
    ("Afirmação", "Uma frase sozinha na tela, pra pesar. Se você precisa de duas, são dois slides."),
    ("Dado", "Um número grande e o que ele significa. O número é o herói, o texto explica."),
    ("Lista", "Três ou quatro itens curtos. Se cada item tem quatro linhas, não é lista, é parede."),
    ("Comparação", "Antes e depois lado a lado. O contraste faz o argumento sozinho."),
    ("Foto", "Imagem grande com título por cima. Clique na imagem pra trocar pela sua."),
    ("Encerramento", "A única coisa que precisa ficar, mais o próximo passo."),
]

def cards():
    out = []
    for i, (nome, txt) in enumerate(LAYOUTS, 1):
        img = b64(os.path.join(SP, "slides", f"slide{i}.png"))
        out.append(
            f'<figure class="card">'
            f'<img src="data:image/png;base64,{img}" alt="Layout {nome}" loading="lazy">'
            f'<figcaption><h3>{nome}</h3><p>{txt}</p></figcaption></figure>')
    return "\n".join(out)

HTML = f"""<title>Apresentação RECONECTA</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
{FONTES}
:root{{
  --ground:#2d0000; --panel:#3a0606; --deep:#0f0e0e;
  --display:#faf0dd; --body:#ececec; --muted:#bda49b;
  --accent:#ff2222; --champagne:#f2ddb6;
  --rule:rgba(250,240,221,.15);
  --display-face:'ArchivoBlack',system-ui,sans-serif;
  --body-face:'Figtree',system-ui,sans-serif;
}}
html{{-webkit-text-size-adjust:100%}}
body{{background:var(--ground);color:var(--body);
  font-family:var(--body-face);font-size:17px;line-height:1.6;
  -webkit-font-smoothing:antialiased}}
.wrap{{max-width:1040px;margin:0 auto;padding:0 28px}}
.prosa{{max-width:65ch}}
.wrap.prosa{{max-width:1040px}}
.wrap.prosa>*{{max-width:65ch}}

h1,h2,h3{{font-family:var(--display-face);font-weight:400;
  text-transform:uppercase;letter-spacing:-.015em;text-wrap:balance;
  color:var(--display);line-height:1.04}}
h1{{font-size:clamp(38px,7vw,68px)}}
h2{{font-size:clamp(24px,3.6vw,34px)}}
h3{{font-size:18px;letter-spacing:-.005em}}
p+p{{margin-top:14px}}
:focus-visible{{outline:2px solid var(--champagne);outline-offset:3px;border-radius:3px}}

.rotulo{{font-family:var(--body-face);font-weight:700;font-size:12px;
  letter-spacing:.17em;text-transform:uppercase;color:var(--muted)}}

header{{padding:88px 0 56px;border-bottom:1px solid var(--rule)}}
header .rotulo{{margin-bottom:20px}}
header p.sub{{margin-top:22px;font-size:20px;max-width:56ch}}
header .semi{{margin-top:18px;color:var(--champagne);font-weight:700;font-size:17px}}

section{{padding:64px 0;border-bottom:1px solid var(--rule)}}
section>.wrap>h2{{margin-bottom:26px}}

ol.passos{{list-style:none;display:flex;flex-direction:column;gap:0;margin-top:8px}}
ol.passos li{{display:grid;grid-template-columns:64px 1fr;gap:22px;
  padding:26px 0;border-top:1px solid var(--rule)}}
ol.passos li:first-child{{border-top:0}}
.num{{font-family:var(--display-face);font-size:34px;color:var(--accent);
  line-height:1;font-variant-numeric:tabular-nums}}
.passo-txt h3{{margin-bottom:8px}}
.passo-txt p{{color:var(--muted)}}
.menu{{display:inline-block;background:var(--panel);border:1px solid var(--rule);
  border-radius:6px;padding:3px 11px;color:var(--champagne);font-weight:700;
  font-size:15px;white-space:nowrap}}

.aviso{{margin-top:28px;border-left:3px solid var(--accent);background:var(--panel);
  border-radius:0 10px 10px 0;padding:18px 22px}}
.aviso strong{{color:var(--display)}}
.aviso p{{color:var(--muted)}}

.regra{{background:var(--deep);border-bottom:1px solid var(--rule);
  padding:80px 0;text-align:center}}
.regra p{{font-family:var(--display-face);text-transform:uppercase;
  font-size:clamp(22px,3.8vw,40px);line-height:1.08;color:var(--display);
  max-width:22ch;margin:0 auto;letter-spacing:-.015em}}
.regra .depois{{font-family:var(--body-face);text-transform:none;font-size:17px;
  color:var(--muted);max-width:52ch;margin:22px auto 0;letter-spacing:0;line-height:1.6}}

.grade{{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));
  gap:26px;margin-top:30px}}
.card{{background:var(--panel);border:1px solid var(--rule);border-radius:12px;
  overflow:hidden}}
.card img{{display:block;width:100%;height:auto;border-bottom:1px solid var(--rule)}}
.card figcaption{{padding:16px 18px 20px}}
.card figcaption h3{{margin-bottom:6px}}
.card figcaption p{{font-size:15px;color:var(--muted);line-height:1.5}}

dl.faq{{margin-top:8px}}
dl.faq div{{padding:22px 0;border-top:1px solid var(--rule)}}
dl.faq div:first-child{{border-top:0}}
dl.faq dt{{font-weight:700;color:var(--display);margin-bottom:7px}}
dl.faq dd{{color:var(--muted);max-width:68ch}}
.grita{{color:var(--accent);font-weight:700}}
code{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:14px;
  background:var(--panel);color:var(--champagne);padding:2px 7px;border-radius:5px}}

.admin{{background:var(--deep)}}
.admin h2{{font-size:clamp(20px,2.6vw,26px)}}
.admin .prosa{{color:var(--muted)}}
.admin ol{{margin:18px 0 0 20px;color:var(--muted);max-width:62ch}}
.admin ol li{{padding:5px 0}}
.admin ul.check{{list-style:none;margin-top:16px;max-width:62ch}}
.admin ul.check li{{padding:8px 0 8px 30px;position:relative;color:var(--muted);
  border-top:1px solid var(--rule)}}
.admin ul.check li:first-child{{border-top:0}}
.admin ul.check li::before{{content:"";position:absolute;left:3px;top:15px;
  width:11px;height:6px;border-left:2px solid var(--champagne);
  border-bottom:2px solid var(--champagne);transform:rotate(-45deg)}}

.tabela-rolo{{overflow-x:auto;margin-top:22px}}
table{{border-collapse:collapse;min-width:520px;width:100%;font-size:15.5px}}
th,td{{text-align:left;padding:12px 20px 12px 0;border-bottom:1px solid var(--rule);
  vertical-align:top}}
th{{color:var(--muted);font-weight:700;font-size:12px;letter-spacing:.14em;
  text-transform:uppercase}}
td strong{{color:var(--champagne);font-weight:700}}

footer{{padding:56px 0 90px;color:var(--muted);font-size:15px}}
@media print{{
  body{{font-size:10.5pt;line-height:1.5}}
  header{{padding:10px 0 22px}}
  h1{{font-size:32pt}}
  h2{{font-size:17pt}}
  section{{padding:24px 0}}
  .regra{{padding:30px 0}}
  .regra p{{font-size:19pt}}
  /* 2 colunas fixas: 1 coluna deixava meia pagina vazia */
  .grade{{grid-template-columns:1fr 1fr;gap:12px;margin-top:16px}}
  .card figcaption{{padding:10px 12px 13px}}
  .card figcaption p{{font-size:9pt}}
  /* so os blocos pequenos evitam quebra; secao inteira NAO — isso criava
     paginas quase vazias */
  .card,ol.passos li,dl.faq div,.aviso,.admin ul.check li{{break-inside:avoid}}
  .wrap{{padding:0 7mm}}
}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important;transition:none!important}}}}
footer p+p{{margin-top:10px}}
</style>

<header><div class="wrap">
  <p class="rotulo">Design System &middot; Reconecta</p>
  <h1>Apresentação<br>Reconecta</h1>
  <p class="sub">Um modelo pronto pra qualquer pessoa do time montar uma apresentação
  da marca sem precisar escolher cor, fonte ou espaçamento.</p>
  <p class="semi">Feito no Google Apresentações. Nada pra instalar, nada pra baixar.</p>
</div></header>

<section><div class="wrap prosa">
  <h2>Como começar</h2>
  <ol class="passos">
    <li><span class="num">1</span><div class="passo-txt">
      <h3>Abra o modelo</h3>
      <p>Está na pasta compartilhada do time, no Drive.</p></div></li>
    <li><span class="num">2</span><div class="passo-txt">
      <h3>Faça uma cópia</h3>
      <p><span class="menu">Arquivo &rarr; Fazer uma cópia</span></p></div></li>
    <li><span class="num">3</span><div class="passo-txt">
      <h3>Escreva</h3>
      <p>O design já está lá. Você só troca o texto.</p></div></li>
  </ol>
  <div class="aviso">
    <p><strong>Faça a cópia antes de escrever qualquer coisa.</strong>
    O arquivo do Drive é o modelo do time inteiro &mdash; a cópia é que é sua.</p>
  </div>
</div></section>

<div class="regra">
  <p>Você não escolhe cor nem fonte. Escolhe o tipo de slide e digita o texto.</p>
  <p class="depois">O design já está dentro de cada layout. Pra trocar o tipo de um slide:
  <span class="menu">Slide &rarr; Aplicar layout</span></p>
</div>

<section><div class="wrap">
  <h2>Os oito layouts</h2>
  <p class="prosa" style="color:var(--muted)">Sua cópia já vem com um slide de exemplo
  de cada um, preenchido com conteúdo de verdade. Olhe, entenda, apague os que não usar.
  Existe também um nono, o <strong style="color:var(--champagne)">Livre</strong>: fundo da
  marca e o resto por sua conta &mdash; use só quando nenhum dos oito servir.</p>
  <div class="grade">{cards()}</div>
</div></section>

<section><div class="wrap">
  <h2>Quando alguma coisa trava</h2>
  <dl class="faq">
    <div><dt>O texto não cabe no slide.</dt>
      <dd><span class="grita">Não diminua a fonte.</span> Corte a copy. Um slide com
      texto miúdo não é um slide cheio, é um slide ilegível. Se não couber mesmo,
      vira dois slides.</dd></div>
    <div><dt>Quero destacar uma palavra.</dt>
      <dd>Use cor, nunca itálico e nunca um peso mais fino. E só um vermelho por slide:
      dois destaques na mesma tela se cancelam.</dd></div>
    <div><dt>Não acho o layout que eu quero.</dt>
      <dd><span class="menu">Slide &rarr; Aplicar layout</span> mostra os nove, com os
      nomes em português. Se aparecer nome em inglês ou uma lista diferente, você está
      num arquivo que não veio do modelo &mdash; comece de novo pela cópia.</dd></div>
    <div><dt>Preciso trocar a foto do slide Foto.</dt>
      <dd>Clique na imagem e substitua. O título e a legenda ficam por cima dela,
      já posicionados.</dd></div>
    <div><dt>Quero mudar uma cor do modelo.</dt>
      <dd>Não mude no slide. Cor, tamanho e regra da marca só mudam num lugar, o
      arquivo de tokens do sistema &mdash; e aí valem pra tudo, inclusive pros
      carrosséis. Fala com quem cuida do sistema.</dd></div>
  </dl>
</div></section>

<section><div class="wrap">
  <h2>Por que essas fontes</h2>
  <p class="prosa" style="color:var(--muted)">A marca tem duas famílias porque tem dois
  destinos. O que a gente renderiza aqui dentro usa as fontes licenciadas; o que o time
  edita no Apresentações usa as do catálogo do Google &mdash; e é por isso que você não
  precisa instalar nada.</p>
  <div class="tabela-rolo"><table>
    <thead><tr><th>Pista</th><th>Display</th><th>Corpo</th><th>Rótulo</th></tr></thead>
    <tbody>
      <tr><td><strong>Licenciada</strong><br><span style="color:var(--muted);font-size:14px">
        carrossel, PDF &mdash; renderizado por nós</span></td>
        <td>Dx Monstral</td><td>Grift</td><td>Inter</td></tr>
      <tr><td><strong>Google</strong><br><span style="color:var(--muted);font-size:14px">
        Apresentações &mdash; editado pelo time</span></td>
        <td>Archivo Black</td><td>Figtree</td><td>Inter</td></tr>
    </tbody>
  </table></div>
  <p class="prosa" style="margin-top:22px;color:var(--muted)">As duas de baixo foram
  escolhidas medindo largura contra as de cima: o Archivo Black tem o mesmo desenho do
  Dx Monstral, e o Figtree fica a 2% da largura do Grift. De longe ninguém nota a troca.</p>
</div></section>

<section class="admin"><div class="wrap">
  <h2>Para quem administra</h2>
  <p class="prosa">O time não precisa ler esta parte. O <code>.pptx</code> do repositório
  é a fonte; o arquivo do Drive é a cópia viva.</p>
  <ol>
    <li>Baixe <strong style="color:var(--champagne)">design-system/pptx/RECONECTA-modelo.pptx</strong></li>
    <li>Arraste pro Drive, numa pasta compartilhada com o time</li>
    <li>Botão direito &rarr; Abrir com &rarr; Google Apresentações</li>
    <li>Arquivo &rarr; Salvar como Apresentações Google</li>
    <li>Compartilhe a pasta como <strong style="color:var(--champagne)">Leitor</strong>
      &mdash; leitor consegue fazer cópia e ninguém edita o original sem querer</li>
  </ol>
  <p class="prosa" style="margin-top:30px;color:var(--display);font-weight:700">
    A conversão pro Apresentações já foi verificada em 18 de agosto de 2026:</p>
  <ul class="check">
    <li>Os títulos estão em caixa alta</li>
    <li>A fonte dos títulos é Archivo Black, não Arial</li>
    <li>O corpo é Figtree</li>
    <li>Slide &rarr; Aplicar layout mostra os nove nomes em português</li>
    <li>O 73% do slide Dado está vermelho</li>
    <li>O fundo bordô está certo, não preto nem branco</li>
  </ul>
  <p class="prosa" style="margin-top:24px">Refaça essa conferência sempre que regerar o
  <code>.pptx</code>. A conversão é boa, mas não é garantida entre versões.</p>
</div></section>

<footer><div class="wrap prosa">
  <p>Esta página está escrita nas mesmas duas fontes do modelo: títulos em Archivo Black,
  texto em Figtree. O que você está lendo é o sistema.</p>
  <p>Tudo vive em <code>design-system/</code> no repositório do time.</p>
</div></footer>
"""

saida = os.path.join(SP, "guia-apresentacao.html")
open(saida, "w").write(HTML)
print("gerado:", saida, "—", round(os.path.getsize(saida)/1024), "KB")
