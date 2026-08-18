# -*- coding: utf-8 -*-
"""
Gera o modelo de apresentação RECONECTA (16:9) a partir do núcleo canônico.

    python3 build_potx.py            # gera RECONECTA-modelo.pptx

Lê design-system/core/tokens.json — NÃO tem cor nem tamanho hardcoded aqui.
Pista tipográfica: google (Archivo Black + Figtree), porque o time edita o arquivo.
"""
import json, os, sys
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls, qn

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
TOKENS = json.load(open(os.path.join(RAIZ, "design-system", "core", "tokens.json")))

C = {k: v["hex"].lstrip("#").upper() for k, v in TOKENS["cor"].items()}
E = TOKENS["escala"]["apresentacao-16x9"]
PISTA = TOKENS["tipografia"]["pista"]["google"]
F_DISPLAY = PISTA["display"]["familia"]      # Archivo Black
F_CORPO = PISTA["corpo"]["familia"]          # Figtree
F_FORTE = "Figtree Black"
F_ROTULO = PISTA["rotulo"]["familia"]        # Inter

# canvas 16:9 padrão do PowerPoint: 13.333 x 7.5 pol = 960 x 540 pt
SLIDE_W_PT, SLIDE_H_PT = 960, 540
MARGEM = E["margem"]["pt"]                   # 70pt
COL_W = SLIDE_W_PT - 2 * MARGEM              # 820pt


def pt(v):
    return Pt(v)


# ---------------------------------------------------------------- tema
def aplicar_tema(prs):
    """Reescreve clrScheme e fontScheme do theme1.xml — é isso que faz o menu
    de cor e de fonte do PowerPoint já abrir na marca."""
    from pptx.opc.constants import RELATIONSHIP_TYPE as RT
    tema = prs.slide_master.part.part_related_by(RT.THEME)
    x = tema._element if hasattr(tema, "_element") else None
    from lxml import etree
    root = etree.fromstring(tema.blob)
    a = "{http://schemas.openxmlformats.org/drawingml/2006/main}"

    cores = [("dk1", C["fundo/escuro"]), ("lt1", C["texto/display"]),
             ("dk2", C["fundo/base"]),   ("lt2", C["texto/corpo"]),
             ("accent1", C["acento/critico"]), ("accent2", C["texto/enfase"]),
             ("accent3", C["fundo/hero"]),     ("accent4", C["texto/display"]),
             ("accent5", C["texto/corpo"]),    ("accent6", C["texto/rotulo"]),
             ("hlink", C["texto/enfase"]),     ("folHlink", C["texto/enfase"])]
    esquema = root.find(f".//{a}clrScheme")
    for nome, hexv in cores:
        no = esquema.find(f"{a}{nome}")
        if no is None:
            continue
        for filho in list(no):
            no.remove(filho)
        cor = etree.SubElement(no, f"{a}srgbClr")
        cor.set("val", hexv)

    for tag, fam in ((f"{a}majorFont", F_DISPLAY), (f"{a}minorFont", F_CORPO)):
        bloco = root.find(f".//{tag}")
        if bloco is None:
            continue
        latin = bloco.find(f"{a}latin")
        if latin is not None:
            latin.set("typeface", fam)

    tema._blob = etree.tostring(root, xml_declaration=True,
                                encoding="UTF-8", standalone=True)
    # python-pptx serializa via .blob; força o conteúdo novo
    tema._element = root
    return tema


def _blob_patch(tema):
    """python-pptx guarda XmlPart.blob a partir do _element; garante consistência."""
    pass


# ------------------------------------------------------- estilo de placeholder
def estilar(ph, *, tam, cor, fonte, caixa_alta=False, alinha="l",
            entrelinha=1.0, tracking=0, negrito=False, depois=0):
    """Escreve o lstStyle do placeholder — é ISSO que o slide herda do layout."""
    tx = ph.text_frame._txBody
    for antigo in tx.findall(qn("a:lstStyle")):
        tx.remove(antigo)
    xml = (
        f'<a:lstStyle {nsdecls("a")}>'
        f'<a:lvl1pPr algn="{alinha}" marL="0" indent="0">'
        f'<a:lnSpc><a:spcPct val="{int(entrelinha*100000)}"/></a:lnSpc>'
        f'<a:spcBef><a:spcPts val="0"/></a:spcBef>'
        f'<a:spcAft><a:spcPts val="{int(depois*100)}"/></a:spcAft>'
        f'<a:buNone/>'
        f'<a:defRPr sz="{int(tam*100)}" b="{1 if negrito else 0}" '
        f'cap="{"all" if caixa_alta else "none"}" spc="{int(tracking*100)}">'
        f'<a:solidFill><a:srgbClr val="{cor}"/></a:solidFill>'
        f'<a:latin typeface="{fonte}"/><a:cs typeface="{fonte}"/>'
        f'</a:defRPr></a:lvl1pPr></a:lstStyle>')
    lst = parse_xml(xml)
    body_pr = tx.find(qn("a:bodyPr"))
    body_pr.addnext(lst)
    # texto-guia
    return ph


def caixa(ph, x, y, w, h, ancora="t"):
    ph.left, ph.top, ph.width, ph.height = pt(x), pt(y), pt(w), pt(h)
    bp = ph.text_frame._txBody.find(qn("a:bodyPr"))
    bp.set("anchor", ancora)
    # o PowerPoint enfia 7,2pt de recuo por padrao; zera pra x bater com a margem
    for lado in ("lIns", "tIns", "rIns", "bIns"):
        bp.set(lado, "0")
    ph.text_frame.word_wrap = True


def guia(ph, texto):
    tf = ph.text_frame
    tf.text = texto


def fundo(obj, hexv):
    obj.background.fill.solid()
    obj.background.fill.fore_color.rgb = RGBColor.from_string(hexv)


def PH(layout, idx):
    """Placeholder pelo idx real — layout.placeholders[n] e POSICIONAL e as
    posicoes andam depois do limpar()."""
    for ph in layout.placeholders:
        if ph.placeholder_format.idx == idx:
            return ph
    raise KeyError(f"placeholder idx={idx} nao existe em {layout.name}")


def ao_fundo(shape):
    """Manda o shape pro fim da pilha (desenha primeiro) — spTree e z-order."""
    el = shape._element
    tree = el.getparent()
    tree.remove(el)
    tree.insert(2, el)   # depois de nvGrpSpPr e grpSpPr


def limpar(layout, manter_idx):
    """Remove placeholders de data/rodapé/número e os que não usamos."""
    for ph in list(layout.placeholders):
        if ph.placeholder_format.idx not in manter_idx:
            ph._element.getparent().remove(ph._element)


# ---------------------------------------------------------------- layouts
def montar(prs):
    m = prs.slide_master
    por_nome = {l.name: l for l in m.slide_layouts}

    # os que não servem pro nosso sistema
    for nome in ("Title and Vertical Text", "Vertical Title and Text"):
        if nome in por_nome:
            m.slide_layouts.remove(por_nome.pop(nome))

    fundo(m, C["fundo/base"])

    # ---- 1. CAPA -------------------------------------------------------
    L = por_nome["Title Slide"]; L.name = "Capa"
    fundo(L, C["fundo/base"]); limpar(L, {0, 1})
    t = PH(L, 0)
    caixa(t, MARGEM, 150, COL_W, 146, ancora="b")
    estilar(t, tam=E["display"]["pt"], cor=C["texto/display"], fonte=F_DISPLAY,
            caixa_alta=True, entrelinha=1.0, tracking=-0.9)
    guia(t, "Título da apresentação")
    s = PH(L, 1)
    caixa(s, MARGEM, 318, 640, 70)
    estilar(s, tam=E["subtitulo"]["pt"], cor=C["texto/corpo"], fonte=F_CORPO,
            entrelinha=1.35)
    guia(s, "Uma linha que promete o que a pessoa leva daqui.")

    # ---- 2. ABERTURA DE SEÇÃO -----------------------------------------
    L = por_nome["Section Header"]; L.name = "Abertura de seção"
    fundo(L, C["fundo/hero"]); limpar(L, {0, 1})
    r = PH(L, 1)
    caixa(r, MARGEM, 205, COL_W, 22)
    estilar(r, tam=E["rotulo"]["pt"], cor=C["texto/rotulo"], fonte=F_ROTULO,
            caixa_alta=True, tracking=1.76, negrito=True)
    guia(r, "Parte 01")
    t = PH(L, 0)
    caixa(t, MARGEM, 240, COL_W, 100)
    estilar(t, tam=E["punch"]["pt"], cor=C["texto/display"], fonte=F_DISPLAY,
            caixa_alta=True, entrelinha=1.04, tracking=-0.6)
    guia(t, "Nome da seção")

    # ---- 3. AFIRMAÇÃO --------------------------------------------------
    L = por_nome["Title Only"]; L.name = "Afirmação"
    fundo(L, C["fundo/base"]); limpar(L, {0})
    t = PH(L, 0)
    caixa(t, MARGEM, 140, COL_W, 260, ancora="ctr")
    estilar(t, tam=E["punch"]["pt"], cor=C["texto/display"], fonte=F_DISPLAY,
            caixa_alta=True, entrelinha=1.04, tracking=-0.6)
    guia(t, "A frase que a pessoa tem que levar embora")

    # ---- 4. DADO -------------------------------------------------------
    L = por_nome["Two Content"]; L.name = "Dado"
    fundo(L, C["fundo/escuro"]); limpar(L, {0, 1, 2})
    t = PH(L, 0)
    caixa(t, MARGEM, 120, COL_W, 95)
    estilar(t, tam=E["punch"]["pt"], cor=C["texto/display"], fonte=F_DISPLAY,
            caixa_alta=True, entrelinha=1.04, tracking=-0.6)
    guia(t, "O que o número prova")
    n = PH(L, 1)
    caixa(n, MARGEM, 240, 260, 130, ancora="ctr")
    estilar(n, tam=E["numero_heroi"]["pt"], cor=C["acento/critico"], fonte=F_DISPLAY,
            entrelinha=0.9, tracking=-2)
    guia(n, "73%")
    b = PH(L, 2)
    caixa(b, MARGEM + 290, 245, COL_W - 290, 130, ancora="ctr")
    estilar(b, tam=E["corpo"]["pt"], cor=C["texto/corpo"], fonte=F_CORPO,
            entrelinha=1.4)
    guia(b, "O que esse número quer dizer, em uma ou duas frases.")

    # ---- 5. LISTA ------------------------------------------------------
    L = por_nome["Title and Content"]; L.name = "Lista"
    fundo(L, C["fundo/base"]); limpar(L, {0, 1})
    t = PH(L, 0)
    caixa(t, MARGEM, 105, COL_W, 85)
    estilar(t, tam=E["punch"]["pt"], cor=C["texto/display"], fonte=F_DISPLAY,
            caixa_alta=True, entrelinha=1.04, tracking=-0.6)
    guia(t, "Título da lista")
    c = PH(L, 1)
    caixa(c, MARGEM, 215, COL_W, 250)
    estilar(c, tam=E["corpo"]["pt"], cor=C["texto/corpo"], fonte=F_CORPO,
            entrelinha=1.4, depois=E["gap_interno"]["pt"])
    guia(c, "Primeiro item — máximo duas linhas")

    # ---- 6. COMPARAÇÃO -------------------------------------------------
    L = por_nome["Comparison"]; L.name = "Comparação"
    fundo(L, C["fundo/base"]); limpar(L, {0, 1, 2, 3, 4})
    t = PH(L, 0)
    caixa(t, MARGEM, 105, COL_W, 85)
    estilar(t, tam=E["punch"]["pt"], cor=C["texto/display"], fonte=F_DISPLAY,
            caixa_alta=True, entrelinha=1.04, tracking=-0.6)
    guia(t, "O contraste")
    meia = (COL_W - 40) / 2
    for idx, x, rot, corpo_txt in ((1, MARGEM, "Antes", "O que acontece hoje."),
                                   (3, MARGEM + meia + 40, "Depois", "O que passa a acontecer.")):
        r = L.placeholders[idx]
        caixa(r, x, 215, meia, 24)
        estilar(r, tam=E["rotulo"]["pt"], cor=C["acento/critico"] if idx == 1
                else C["texto/enfase"], fonte=F_ROTULO, caixa_alta=True,
                tracking=1.76, negrito=True)
        guia(r, rot)
        b = L.placeholders[idx + 1]
        caixa(b, x, 252, meia, 190)
        estilar(b, tam=E["corpo"]["pt"], cor=C["texto/corpo"], fonte=F_CORPO,
                entrelinha=1.4, depois=E["gap_interno"]["pt"])
        guia(b, corpo_txt)

    # ---- 7. FOTO -------------------------------------------------------
    L = por_nome["Picture with Caption"]; L.name = "Foto"
    fundo(L, C["fundo/escuro"]); limpar(L, {0, 1, 2})
    p = PH(L, 1)
    caixa(p, 0, 0, SLIDE_W_PT, SLIDE_H_PT)
    ao_fundo(p)
    t = PH(L, 0)
    caixa(t, MARGEM, 350, COL_W, 80)
    estilar(t, tam=E["punch"]["pt"], cor=C["texto/display"], fonte=F_DISPLAY,
            caixa_alta=True, entrelinha=1.04, tracking=-0.6)
    guia(t, "Título sobre a foto")
    b = PH(L, 2)
    caixa(b, MARGEM, 440, 660, 50)
    estilar(b, tam=E["corpo"]["pt"], cor=C["texto/corpo"], fonte=F_CORPO,
            entrelinha=1.35)
    guia(b, "Uma linha de apoio.")

    # ---- 8. ENCERRAMENTO ----------------------------------------------
    L = por_nome["Content with Caption"]; L.name = "Encerramento"
    fundo(L, C["fundo/escuro"]); limpar(L, {0, 2})
    t = PH(L, 0)
    caixa(t, MARGEM, 175, COL_W, 140, ancora="b")
    estilar(t, tam=E["punch"]["pt"], cor=C["texto/display"], fonte=F_DISPLAY,
            caixa_alta=True, entrelinha=1.04, tracking=-0.6, alinha="ctr")
    guia(t, "A única coisa que fica")
    b = PH(L, 2)
    caixa(b, MARGEM, 340, COL_W, 50)
    estilar(b, tam=E["rotulo"]["pt"], cor=C["texto/rotulo"], fonte=F_ROTULO,
            caixa_alta=True, tracking=1.54, negrito=True, alinha="ctr")
    guia(b, "Próximo passo  /  →")

    # ---- 9. LIVRE ------------------------------------------------------
    L = por_nome["Blank"]; L.name = "Livre"
    fundo(L, C["fundo/base"]); limpar(L, set())

    ordem = ["Capa", "Abertura de seção", "Afirmação", "Dado", "Lista",
             "Comparação", "Foto", "Encerramento", "Livre"]
    atual = {l.name: l for l in m.slide_layouts}
    return [atual[n] for n in ordem if n in atual]


# ---------------------------------------------------------------- exemplo
EXEMPLOS = {
    # layout: { idx do placeholder: texto }   <- por IDX, nunca por posicao
    # Os titulos vao em CAIXA ALTA literal de proposito: o layout ja aplica
    # caixa alta, mas o Google Slides pode nao honrar esse atributo na
    # importacao. Assim o exemplo fica certo dos dois jeitos.
    "Capa": {0: "A AGENDA DO MILHÃO",
             1: "Três pacientes novos por semana. Quatro recorrências. "
                "O resto é consequência."},
    "Abertura de seção": {0: "O DIAGNÓSTICO", 1: "PARTE 01"},
    "Afirmação": {0: "O QUE TRAVA A AGENDA NÃO É CAPTAÇÃO"},
    "Dado": {0: "ONDE A CONTA VAZA", 1: "73%",
             2: "das doutoras que travam em 70k não têm problema de leads. "
                "Têm problema de retorno: o paciente some depois do primeiro "
                "procedimento."},
    "Lista": {0: "AS TRÊS ENGRENAGENS",
              1: "Primeira consulta que já agenda a próxima\n"
                 "Retorno tratado como parte do plano, não como recaída\n"
                 "Follow-up que chega antes do paciente sumir"},
    "Comparação": {0: "COMO A AGENDA MUDA",
                   1: "ANTES",
                   2: "A doutora vende o procedimento e espera o paciente voltar sozinho.",
                   3: "DEPOIS",
                   4: "A doutora vende o plano e o retorno já sai agendado da cadeira."},
    "Foto": {0: "ISSO ACONTECE NA CADEIRA", 2: "Não no anúncio."},
    "Encerramento": {0: "COMECE PELO RETORNO", 2: "PRÓXIMO PASSO  /  →"},
}


def preencher(prs, layouts):
    for L in layouts:
        mapa = EXEMPLOS.get(L.name)
        if not mapa:
            continue
        s = prs.slides.add_slide(L)
        for ph in s.placeholders:
            txt = mapa.get(ph.placeholder_format.idx)
            if txt is None:
                continue
            tf = ph.text_frame
            linhas = txt.split("\n")
            tf.text = linhas[0]
            for extra in linhas[1:]:
                tf.add_paragraph().text = extra


def main():
    prs = Presentation()
    prs.slide_width = Emu(int(13.3333 * 914400))
    prs.slide_height = Emu(int(7.5 * 914400))
    prs._element.find(qn("p:sldSz")).set("type", "screen16x9")
    aplicar_tema(prs)
    layouts = montar(prs)
    preencher(prs, layouts)
    saida = os.path.join(AQUI, "RECONECTA-modelo.pptx")
    prs.save(saida)
    print("gerado:", saida)
    print("layouts:", ", ".join(l.name for l in layouts))
    print("slides de exemplo:", len(prs.slides.__iter__.__self__._sldIdLst))
    return saida


if __name__ == "__main__":
    main()
