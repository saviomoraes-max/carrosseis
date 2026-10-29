#!/usr/bin/env python3
"""Monta o livro inteiro num arquivo só, na ordem de leitura, pra quem vai LER e não revisar.

O manuscrito é quinze arquivos e as cercas ::: são sintaxe de compilador. Um leitor não vê
nada disso: vê capítulo atrás de capítulo, com a frase pronta destacada e o diálogo em
turnos. Este script produz esse objeto, que é o que uma banca precisa receber.

Uso: python3 livro_continuo.py ebooks/<slug>
"""
import json, re, sys, pathlib

def desmontar(corpo):
    """Troca cerca de bloco por rótulo legível, preservando o texto na ordem."""
    linhas, out, i = corpo.split("\n"), [], 0
    while i < len(linhas):
        ln = linhas[i]
        if ln.startswith(":::"):
            tipo = ln[3:].strip(); j = i + 1; dentro = []
            while j < len(linhas) and linhas[j].strip() != ":::":
                dentro.append(linhas[j]); j += 1
            base = tipo.split()[0] if tipo else ""
            if base == "frase":
                out.append("    FRASE PRONTA — " + " ".join(x.strip() for x in dentro if x.strip()))
            elif base == "cena":
                out.append("    [conversa de WhatsApp]")
                for x in dentro:
                    if x.strip(): out.append("      " + x.strip())
            elif base == "caso":
                out.append("    [cartão de objeção]")
                rot = {"ela": "ELA MANDA", "perde": "SE RESPONDER ASSIM, PERDE", "responde": "O QUE CONTINUA A CONVERSA"}
                for x in dentro:
                    m = re.match(r"^(ela|perde|responde):\s*(.*)$", x.strip(), re.I)
                    if m: out.append(f"      {rot[m.group(1).lower()]}: {m.group(2)}")
            elif base == "evite":
                out.append("    O QUE EVITAR — " + " ".join(x.strip() for x in dentro if x.strip()))
            elif base in ("punch", "pergunta"):
                rot = "FRASE EM PÁGINA INTEIRA" if base == "punch" else "PERGUNTA EM ABERTO"
                out.append(f"    {rot} — " + " ".join(x.strip() for x in dentro if x.strip()))
            elif base == "grafico":
                out.append(f"    [gráfico: {tipo[len('grafico'):].strip() or 'sem tipo'}]")
                for x in dentro:
                    if x.strip(): out.append("      " + x.strip())
            i = j + 1; continue
        out.append(ln); i += 1
    return "\n".join(out)

def main():
    raiz = pathlib.Path(sys.argv[1])
    L = json.loads((raiz / "livro.json").read_text())
    arqs = {p.name.split("-")[0]: p for p in (raiz / "manuscrito").glob("*.md")}
    partes = {p["de"]: p for p in L.get("partes", [])}
    out = [f'# {L["titulo"]}', "", L["titulo_capa"].replace("\\n", " "), "", L["subtitulo"], "",
           "Ebook pago, vendido pela página da VSL. A leitora é doutora de harmonização facial",
           "e lê no celular. O livro é narrado em primeira pessoa pela fundadora da clínica.", ""]
    n_pal = 0
    for e in L["sumario"]:
        num = e["numero"]
        if num in partes:
            pa = partes[num]
            out += ["", "=" * 78, f'{pa["rotulo"].upper()} · {pa["titulo"].upper()}', "=" * 78, ""]
        arq = arqs.get(num)
        if not arq: continue
        txt = arq.read_text(encoding="utf-8")
        m = re.match(r"\A---\n(.*?)\n---\n", txt, re.S)
        meta = {}
        if m:
            for l in m.group(1).splitlines():
                if ":" in l:
                    k, v = l.split(":", 1); meta[k.strip()] = v.strip().strip('"')
            txt = txt[m.end():]
        txt = re.sub(r"^# .*$", "", txt, flags=re.M)
        rot = "ANEXO" if num.isalpha() else "CAPÍTULO"
        out += ["", "-" * 78, f'{rot} {num} · {meta.get("titulo", "")}',
                f'   {meta.get("subtitulo", "")}', "-" * 78, "", desmontar(txt).strip(), ""]
        n_pal += len(re.findall(r"[\wÀ-ÿ]+", txt))
    doc = re.sub(r"\n{3,}", "\n\n", "\n".join(out))
    saida = raiz / "render" / "livro-continuo.md"
    saida.write_text(doc, encoding="utf-8")
    print(f"{saida}  ({n_pal} palavras, {len(L['sumario'])} blocos)")

if __name__ == "__main__":
    main()
