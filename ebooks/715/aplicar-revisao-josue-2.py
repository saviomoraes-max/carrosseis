#!/usr/bin/env python3
"""Segunda rodada da revisão humana do Josué (16/set/2026), sobre o PDF de 15/set.

Origem: `revisao/humana/script-715-atualizado-rodada2.pdf` (6 riscos com texto digitado) e
`revisao/humana/audio-josue-rodada2.txt` (transcrito no ElevenLabs Scribe). O áudio confirma o
escopo: "são seis correções só", nas páginas 6 (duas), 8, 29, 40 e 131. Nada de estrutura.

A da página 40 ("Em que momentos" -> "Em quais momentos") é frase literal do framework e foi
decidida à parte; se entrou, está no fim desta lista.

Uso:  python3 aplicar-revisao-josue-2.py [--conferir]
Depois:  render_pdf.py . --provas  e  livro_continuo.py .
"""
import pathlib, sys

C01 = "manuscrito/01-a-salinha-do-financeiro.md"
C03 = "manuscrito/03-passo-1-conexao.md"
C04 = "manuscrito/04-passo-2-situacao.md"
AA = "manuscrito/A-cola-de-uma-pagina.md"
AB = "manuscrito/B-banco-de-perguntas.md"

# (arquivo, texto atual, texto novo) — cada texto atual precisa aparecer UMA vez
TROCAS = [
    (C01, "que ia levar “facada”.", "que ia levar uma “facada”."),                                # p6
    (C01, "que tinha se formado quando eu falei com a doutora",
          "que tinha se formado de quando eu tinha falado com a doutora"),                         # p6
    (C01, "como paciente. Como vendedora eu vi", "como paciente. Já como vendedora eu vi"),        # p8
    # p29. ajuste: ele riscou "oi," e digitou "Olá"; a vírgula fica, senão a fala emenda
    (C03, "só um “oi, quero mais informações”", "só um “Olá, quero mais informações”"),
    (AA, "ela responde completo e emocional", "ela responde de forma completa e emocional"),       # p131
    # p40: frase literal do framework. O Sávio liberou em 16/set, porque troca uma palavra e não
    # mexe no que a frase pede. Vai nos dois lugares em que ela aparece, pra não divergir
    (C04, "Em que momentos você percebe", "Em quais momentos você percebe"),
    (AB, "Em que momentos você percebe", "Em quais momentos você percebe"),
]


def main():
    raiz = pathlib.Path(__file__).resolve().parent
    conferir = "--conferir" in sys.argv
    problemas = []
    for arq, velho, novo in TROCAS:
        achou = (raiz / arq).read_text().count(velho)
        if achou != 1:
            problemas.append(f"{arq}: esperava 1 ocorrência de {velho[:60]!r}, achei {achou}")
    if problemas:
        print("NÃO APLICADO. O manuscrito não bate com a revisão:")
        for x in problemas: print("  -", x)
        raise SystemExit(1)
    if conferir:
        print(f"ok: as {len(TROCAS)} trocas batem com o manuscrito. Rode sem --conferir pra aplicar.")
        return
    for arq, velho, novo in TROCAS:
        p = raiz / arq
        p.write_text(p.read_text().replace(velho, novo))
    print(f"aplicado: {len(TROCAS)} trocas em {len({a for a, _, _ in TROCAS})} arquivos")

if __name__ == "__main__":
    main()
