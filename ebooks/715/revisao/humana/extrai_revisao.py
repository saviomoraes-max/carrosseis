import pymupdf, json, sys
doc = pymupdf.open("/Users/saviomoraes/Downloads/script-715 com correções.pdf")

def chars_in(page, quads):
    raw = page.get_text("rawdict")
    out = []
    lines_hit = []
    for b in raw["blocks"]:
        for l in b.get("lines", []):
            lt = "".join(c["c"] for s in l["spans"] for c in s["chars"])
            hit = False
            for s in l["spans"]:
                for c in s["chars"]:
                    x0,y0,x1,y1 = c["bbox"]; cx=(x0+x1)/2; cy=(y0+y1)/2
                    for q in quads:
                        r = q.rect
                        if r.x0-0.5 <= cx <= r.x1+0.5 and r.y0-0.5 <= cy <= r.y1+0.5:
                            out.append((round(cy), c["bbox"][0], c["c"])); hit=True; break
            if hit: lines_hit.append(lt)
    out.sort()
    return "".join(c for _,_,c in out), lines_hit

items = []
for pno, page in enumerate(doc):
    ann = {a.xref: a for a in page.annots()}
    carets = {x:a for x,a in ann.items() if a.type[1]=="Caret"}
    used_hl = set()
    strikes = [a for a in ann.values() if a.type[1]=="StrikeOut"]
    for s in strikes:
        quads = s.vertices
        qs = [pymupdf.Quad(quads[i:i+4]) for i in range(0,len(quads),4)]
        txt, lines = chars_in(page, qs)
        irt = s.irt_xref
        rep = carets[irt].info.get("content","") if irt in carets else None
        items.append(dict(pag=pno+1, tipo="troca", riscado=txt, novo=rep, linhas=lines, y=round(s.rect.y0), x=round(s.rect.x0)))
    for h in [a for a in ann.values() if a.type[1]=="Highlight"]:
        quads = h.vertices
        qs = [pymupdf.Quad(quads[i:i+4]) for i in range(0,len(quads),4)]
        txt, lines = chars_in(page, qs)
        cor = h.colors.get("stroke")
        roxo = cor and cor[2] > 0.9
        items.append(dict(pag=pno+1, tipo="realce-roxo" if roxo else "realce", texto=txt, linhas=lines, y=round(h.rect.y0), x=round(h.rect.x0)))
items.sort(key=lambda d:(d["pag"], d["y"], d["x"]))
json.dump(items, open("revisao-josue.json","w"), ensure_ascii=False, indent=1)
for d in items:
    if d["tipo"]=="troca":
        print(f'p{d["pag"]:>3} TROCA  [{d["riscado"]}] -> [{d["novo"]}]   || {" / ".join(d["linhas"])}')
    else:
        print(f'p{d["pag"]:>3} {d["tipo"].upper():12} [{d["texto"]}]   || {" / ".join(d["linhas"])[:160]}')
