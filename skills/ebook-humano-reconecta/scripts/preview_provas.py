#!/usr/bin/env python3
"""Monta render/preview.html com todas as páginas (PNG das provas) em grade e abre no navegador."""
import sys, pathlib, subprocess, time
rd = pathlib.Path(sys.argv[1]).resolve()
prov = rd / "provas"; pngs = sorted(prov.glob("pag*.png")); v = int(time.time())
cards = "".join(f'<figure><img src="provas/{p.name}?v={v}"><figcaption>{p.stem}</figcaption></figure>' for p in pngs)
html = f'''<!doctype html><meta charset="utf-8"><title>Provas · {rd.parent.name}</title>
<style>body{{margin:0;background:#111;color:#eee;font:13px Inter,sans-serif;padding:20px}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:18px}}
figure{{margin:0}} img{{width:100%;display:block;box-shadow:0 6px 30px rgba(0,0,0,.6)}} figcaption{{padding:6px 2px;opacity:.7}}
h1{{font-weight:400;font-size:16px;margin:0 0 14px}}</style>
<h1>{rd.parent.name} · {len(pngs)} páginas · {time.strftime("%d/%m %H:%M")}</h1><div class="g">{cards}</div>'''
out = rd / "preview.html"; out.write_text(html, encoding="utf-8")
subprocess.run(["open", str(out)]); print(out)
