#!/usr/bin/env python3
"""Gera PNG por página de um PDF (pra revisar antes do preview). Usa o Quartz do macOS, sem pip."""
import sys, pathlib
import Quartz
from Foundation import NSURL
pdf, out = sys.argv[1], pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
doc = Quartz.PDFDocument.alloc().initWithURL_(NSURL.fileURLWithPath_(pdf))
n = doc.pageCount()
for i in range(n):
    page = doc.pageAtIndex_(i)
    img = page.thumbnailOfSize_forBox_((1080, 1920), Quartz.kPDFDisplayBoxMediaBox)
    tiff = img.TIFFRepresentation()
    rep = Quartz.NSBitmapImageRep.imageRepWithData_(tiff)
    png = rep.representationUsingType_properties_(Quartz.NSPNGFileType, None)
    png.writeToFile_atomically_(str(out / f"pag{i+1:03d}.png"), True)
print(f"{n} páginas em {out}")
