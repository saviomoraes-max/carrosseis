#!/usr/bin/env python3
"""As DUAS correções de metodologia que dependem da decisão do Sávio.

NÃO RODE SEM A DECISÃO DELE. Cinco bancas seguidas acharam essas duas frases, sempre no
mesmo lugar e sempre com o mesmo diagnóstico, e a decisão registrada até aqui é MANTER,
porque a redação é literal do framework e do manual de perguntas.

O que mudou na 6ª e na 7ª banca é a natureza do argumento. Antes era erro de leitura, que
quase ninguém repara. Agora a leitora-alvo descreveu outra coisa: ela COPIOU a frase pra
mandar e travou. Ou seja, o defeito não fica no livro, ele sai no WhatsApp da clínica.

As duas correções mudam CONECTIVO, não conteúdo:

  1. A apresentação. "vai te ajudar com o [problema] E parar de se sentir [x]" põe a
     doutora como quem para de se sentir mal, porque "parar" coordena com "vai te ajudar"
     debaixo do mesmo "vai". Vira "PRA VOCÊ parar de se sentir [x]".
     (Não use "e a parar": cruza duas regências sob o mesmo "ajudar" e trunca no WhatsApp.)

  2. A transição. "desde [tempo]" pede marco, não duração. O livro manda preencher com o
     que a paciente disse, e o exemplo do próprio livro é "tem uns dois anos que eu reparo",
     então sai "desde dois anos". Vira "há [tempo]", que é o que o anexo B JÁ escreve.

Nenhuma das duas altera o que o script diz, a ordem dos passos, os colchetes ou a doutrina.

Uso:  python3 aplicar-correcao-metodologia.py [--conferir]
Depois:  python3 ~/.claude/skills/ebook-humano-reconecta/scripts/render_pdf.py . --provas
"""
import pathlib, sys

# (arquivo, texto atual, texto novo, quantas ocorrências esperar)
TROCAS = [
    # 1. apresentação — 4 lugares
    ("manuscrito/08-passo-6-apresentacao.md",
     "vai te ajudar com essa região do queixo que tá te incomodando e parar de se sentir com vontade de se esconder nas fotos.",
     "vai te ajudar com essa região do queixo que tá te incomodando pra você parar de se sentir com vontade de se esconder nas fotos.", 1),
    ("manuscrito/08-passo-6-apresentacao.md",
     "vai te ajudar com o [problema] e parar de se sentir [como está se sentindo].",
     "vai te ajudar com o [problema] pra você parar de se sentir [como está se sentindo].", 1),
    ("manuscrito/A-cola-de-uma-pagina.md",
     "vai te ajudar com o [problema] e parar de se sentir [como está se sentindo].",
     "vai te ajudar com o [problema] pra você parar de se sentir [como está se sentindo].", 1),
    ("manuscrito/B-banco-de-perguntas.md",
     "vai te ajudar com a [dor trazida] e parar de se sentir [sentimento informado].",
     "vai te ajudar com a [dor trazida] pra você parar de se sentir [sentimento informado].", 1),

    # 2. transição — 3 lugares (o anexo B já está certo com "há [tempo informado]")
    ("manuscrito/07-passo-5-transicao.md",
     "e de já estar desde uns dois anos sentindo assim",
     "e de já estar há uns dois anos sentindo assim", 1),
    ("manuscrito/07-passo-5-transicao.md",
     "e de já estar desde [tempo] sentindo assim",
     "e de já estar há [tempo] sentindo assim", 1),
    ("manuscrito/07-passo-5-transicao.md",
     "3 | «desde [tempo]» · ela mesma te deu, no passo dois",
     "3 | «há [tempo]» · ela mesma te deu, no passo dois", 1),
    ("manuscrito/A-cola-de-uma-pagina.md",
     "e de já estar desde [tempo] sentindo assim",
     "e de já estar há [tempo] sentindo assim", 1),
]

def main():
    raiz = pathlib.Path(__file__).resolve().parent
    conferir = "--conferir" in sys.argv
    problemas = []
    for arq, velho, novo, n in TROCAS:
        p = raiz / arq
        t = p.read_text()
        achou = t.count(velho)
        if achou != n:
            problemas.append(f"{arq}: esperava {n} ocorrência(s) de {velho[:50]!r}, achei {achou}")
    if problemas:
        print("NÃO APLICADO. O manuscrito mudou desde que este patch foi escrito:")
        for x in problemas: print("  -", x)
        raise SystemExit(1)
    if conferir:
        print(f"ok: as {len(TROCAS)} trocas batem com o manuscrito. Rode sem --conferir pra aplicar.")
        return
    for arq, velho, novo, n in TROCAS:
        p = raiz / arq
        p.write_text(p.read_text().replace(velho, novo))
        print("ok ", arq, "→", novo[:60])
    print("\nAplicado. Agora:")
    print("  python3 ~/.claude/skills/ebook-humano-reconecta/scripts/render_pdf.py . --provas")
    print("  python3 ~/.claude/skills/ebook-humano-reconecta/scripts/livro_continuo.py .")

if __name__ == "__main__":
    main()
