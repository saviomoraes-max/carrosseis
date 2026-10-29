#!/usr/bin/env python3
"""A revisão humana do Josué (14/set/2026), aplicada ao manuscrito.

Origem: `revisao/humana/script-715-com-correcoes.pdf` (89 riscos com texto digitado e 3 realces
roxos) e `revisao/humana/audio-josue.txt`. O texto de cada anotação foi extraído com PyMuPDF para
`revisao/humana/revisao-josue.json`, e cada troca abaixo cita a página do PDF anotado.

Decisões do Sávio em 15/set, antes de aplicar:
  - numeração: "Capítulo" em tudo, "Prova nº" sai (o revisor achou confuso misturar os dois);
  - as três frases prontas literais da metodologia que o revisor mexeu FICAM literais:
    "Em que momentos" (cap 04 e anexo B), "procurar por [procedimento]" (anexo B) e
    "Vou te explicar como funciona. Antes, ... antes de vermos a disponibilidade" (cap 11, citada
    no cap 08). Não estão nesta lista de propósito.

Onde a digitação do revisor tinha erro, vale a intenção e o erro não entra. Cada caso está marcado
com "ajuste:" no comentário da troca.

Uso:  python3 aplicar-revisao-josue.py [--conferir]
Depois:  render_pdf.py . --provas  e  livro_continuo.py .
"""
import pathlib, sys

M = "manuscrito/"
C01 = M + "01-a-salinha-do-financeiro.md"
C02 = M + "02-vender-o-que-ela-ja-quer-comprar.md"
C03 = M + "03-passo-1-conexao.md"
C04 = M + "04-passo-2-situacao.md"
C05 = M + "05-passo-3-presente-inaceitavel.md"
C06 = M + "06-passo-4-qualificacao.md"
C07 = M + "07-passo-5-transicao.md"
C08 = M + "08-passo-6-apresentacao.md"
C09 = M + "09-passo-7-fechamento.md"
C10 = M + "10-objecao-nao-e-um-nao.md"
C11 = M + "11-o-manual-de-respostas.md"
C12 = M + "12-doutora-e-vendedora-tambem.md"
AA = M + "A-cola-de-uma-pagina.md"
AB = M + "B-banco-de-perguntas.md"
AC = M + "C-paciente-modelo.md"

# (arquivo, texto atual, texto novo) — cada texto atual precisa aparecer UMA vez
TROCAS = [
    # --- capítulo 01 ---
    # p5: "Chegamos juntos", "em um plano", "Tive", "Até aí, tudo normal"
    (C01, "A gente chega junto num plano de tratamento, um plano de seis meses. Tem alguma dúvida ou outra durante a consulta, tudo normal. E aí,",
          "Chegamos juntos em um plano de tratamento, um plano de seis meses. Tive alguma dúvida ou outra durante a consulta. Até aí, tudo normal. E aí,"),
    (C01, "fico numa área de espera", "fico em uma área de espera"),                                      # p5
    (C01, "A consulta | «Realmente eu encontrei a solução pro meu problema.»",
          "A consulta | «Realmente eu encontrei a solução para o meu problema.»"),                         # p5, gráfico
    (C01, "A recepção | «E se esse negócio for muito caro? Será que é prioridade agora?»",
          "A recepção | «E se for muito caro? Será que é prioridade agora?»"),                             # p5, gráfico
    # p5, gráfico. ajuste: o revisor digitou "coro"; o idiomatismo é "couro"
    (C01, "A salinha do financeiro | «Vão arrancar o couro aqui de mim.»",
          "A salinha do financeiro | «Vão arrancar meu couro aqui.»"),
    # p6: só realçado, sem texto. Segue o gráfico da página anterior pra frase não mudar entre as duas
    (C01, "já remete a “vão arrancar o couro aqui de mim”, porque", "já remete a “vão arrancar meu couro aqui”, porque"),
    (C01, "Eu ia lá no caminho e tá lá a salinha do financeiro e eu sabia que ia levar facada.",
          "Eu estava indo a caminho da salinha do financeiro e eu sabia que ia levar “facada”."),          # p6
    (C01, "tinha se formado até eu falar com a doutora", "tinha se formado quando eu falei com a doutora"),  # p6
    # p6. ajuste: o texto digitado era "para o meu" sobre "pro"; o "meu" já estava lá
    (C01, "a solução pro meu problema”, aquilo", "a solução para o meu problema”, aquilo"),
    (C01, "me trazido a solução pras dores", "me trazido a solução para as dores"),                     # p7
    (C01, "Porque eu já tava completamente na emoção.", "Porque eu já estava completamente na emoção."),  # p7
    # p7: realce roxo = ênfase (a casa não usa negrito; ênfase é cor, «»). "Pensei", sem "esse negócio"
    (C01, "Foi ter saído, ter esperado, ter pensado.\n\nFalei, cara, e se esse negócio for muito caro?",
          "Foi ter saído, ter esperado, «ter pensado».\n\nPensei, e se for muito caro?"),
    (C01, "uma encenação pra poder fechar", "uma encenação para poder fechar"),                         # p8
    (C01, "Foi assim que eu me senti, de paciente. De vendedora eu vi outra coisa, e essa parte fica pro capítulo 12.",
          "Foi assim que eu me senti, como paciente. Como vendedora eu vi outra coisa, e essa parte fica para o capítulo 12."),  # p8
    (C01, "porque a gente tá com muita gente indo pra casa pensar.”", "porque estamos com muita gente indo pra casa pensar.”"),  # p9
    # p10. ajuste: "pra clínica" é "pra a clínica"; o artigo entra
    (C01, "Quem manda mensagem pra clínica já quer alguma coisa.", "Quem manda mensagem para a clínica já quer alguma coisa."),

    # --- capítulo 02 ---
    (C02, "de cidades de tamanhos muito diferentes, de idades muito diferentes, de formações diferentes. E eu",
          "de cidades de tamanhos muito diferentes, de idades e formações muito diferentes. E eu"),        # p13
    (C02, "o volume de leads baixou esse mês, essa primeira semana aqui de setembro.",
          "o volume de leads abaixou esse mês, nessa primeira semana de setembro."),                       # p13
    # p17. ajuste: digitado "o que a gente quer que a paciente saia", "sem se sentir que",
    # "empurraram a consulta a nela" e "caso ... se resolve". Entra a intenção com a concordância certa
    (C02, "o que a gente quer é a paciente sair da conversa querendo marcar sem ninguém ter empurrado, se o problema que ela trouxe se resolve com a consulta.",
          "o que a gente quer é que a paciente saia da conversa querendo marcar, sem sentir que “empurraram a consulta nela”, caso o problema que ela trouxe se resolva com a consulta."),
    (C02, "e o script foi escrito pra essa pessoa.", "e o script foi escrito para essa pessoa."),        # p18
    # p18. ajuste: "exemplo:" daria dois dois-pontos na mesma frase (a citação já termina em ":")
    (C02, "na terceira pessoa, tipo “até pra entender", "na terceira pessoa, por exemplo, “até pra entender"),
    (C02, "«1.» O atendimento é pra entender se aquela pessoa", "«1.» O atendimento é para entender se aquela pessoa"),  # p19
    # p19: "entrar para agendar", "pula para o fechamento" e realce roxo na frase inteira.
    # O "entra pra agendar" do meio não foi riscado; vira "para" pra não trocar de forma dentro da mesma frase
    (C02, "Parece a mesma coisa que entrar pra agendar, mas na conversa não é, porque quem entra pra agendar pula pro fechamento e a paciente sente que você só está querendo vender.",
          "Parece a mesma coisa que entrar para agendar, mas na conversa não é, «porque quem entra para agendar pula para o fechamento e a paciente sente que você só está querendo vender»."),
    (C02, "“E você tem horário para quando?”, entendeu? E quando é você", "“E você tem horário para quando?” E quando é você"),  # p19
    (C02, "é repetir a palavra que ela usou e perguntar", "é «repetir a palavra que ela usou» e perguntar"),  # p20, roxo
    (C02, "e você fica olhando pro visto azul.", "e você fica olhando para o visto azul."),              # p21

    # --- capítulo 03 ---
    (C03, "Quando você diz pra paciente que primeiro", "Quando você diz para a paciente que primeiro"),  # p27, ajuste: artigo
    (C03, "porque antes ela tá assim, dura igual uma pedra, uma porta", "porque antes ela estava “dura igual uma pedra”, uma porta"),  # p27
    (C03, "E a resistência é isso, ó: ela esquiva", "E a resistência é isso: ela esquiva"),              # p28
    (C03, "ela me responde “o que que é o preço?”.", "ela me responde “qual é o preço?”."),              # p28
    (C03, "só um “oi, queria informações”, tem uma", "só um “oi, quero mais informações”, tem uma"),    # p29
    (C03, "é agendamento garantido e pular pro fechamento.", "é agendamento garantido e pular para o fechamento."),  # p30
    (C03, "porque agenda sempre aberta é clínica que pega qualquer uma", "porque agenda sempre aberta é sinal de clínica que pega qualquer uma"),  # p32

    # --- capítulo 04 ---
    (C04, "que eu mais vejo dar errado, gente. Um dos", "que eu mais vejo dar errado. Um dos"),          # p36
    (C04, "A gente sabe do que ela tá falando, sabe? E aí", "A gente sabe do que ela tá falando? E aí"),  # p37, como digitado
    (C04, "Acho que vale a pena a gente perguntar", "Acredito que vale a pena a gente perguntar"),      # p40
    (C04, "o seguinte quando tô atendendo:", "o seguinte, quando estou atendendo:"),                    # p43
    (C04, "a palavra dela: ó, você perguntou", "a palavra dela: você perguntou"),                      # p44
    # a mesma frase foi riscada no anexo B (p137); aqui fica igual pra não divergir entre as duas
    (C04, "As primeiras servem pra clarear a palavra que ela usou. A gente pega", "As primeiras servem para clarear a palavra que ela usou. A gente pega"),

    # --- capítulo 05 ---
    (C05, "a paciente olha pro problema que ela já tinha", "a paciente olha para o problema que ela já tinha"),  # p47
    (C05, "essa convicção pros próximos passos e vai empurrar.", "essa convicção para os próximos passos e vai “empurrar”."),  # p54

    # --- capítulo 06 ---
    (C06, "Você não apresentou nada ainda, gente. E a paciente", "Você não apresentou nada ainda. E a paciente"),  # p57
    (C06, "ou o três. Volta.", "ou o três. Então volta."),                                             # p62
    (C06, "vai me ajudar a resolver”. E acontece quando", "vai me ajudar a resolver”. Isso acontece quando"),  # p62

    # --- capítulo 07 ---
    # p66. ajuste: digitado "para os"; "problema" está no singular
    (C07, "E dizer por que, pro problema dela, a consulta", "E dizer por que, para o problema dela, a consulta"),
    (C07, "e eu acho que fazem diferença", "e eu acredito que fazem diferença"),                       # p68

    # --- capítulo 08 ---
    (C08, "a apresentação é curta, gente: quem", "a apresentação é curta: quem"),                      # p72
    (C08, "Seis erros, e eu quero comentar dois.", "Existem seis erros, mas eu gostaria de comentar dois."),  # p74
    (C08, "passa a vir pro procedimento", "passa a vir para o procedimento"),                          # p74
    # p75: vírgula depois de "pediu" e "é porque" sobre o "e". ajuste: "é porque" transformaria as três
    # causas da leitura negativa (framework, p.9) numa causa só; entram as vírgulas, a lista fica
    (C08, "do que ela pediu e solução que não resolve o problema dela e porque a gente qualificou",
          "do que ela pediu, e solução que não resolve o problema dela, e porque a gente qualificou"),
    (C08, "a solução certa pro problema que ela trouxe", "a solução certa para o problema que ela trouxe"),  # p75

    # --- capítulo 09 ---
    (C09, "Ser o próximo passo óbvio pra resolver o problema.", "O próximo passo óbvio para resolver o problema."),  # p80
    (C09, "a resposta pra isso. Essa lista, ponto importante, é o script inteiro, gente. O fechamento colhe",
          "a resposta pra isso. O fechamento colhe"),                                                   # p85

    # --- capítulo 10 ---
    (C10, "eu sei o que tem atrás, porque", "eu sei o que tem por trás, porque"),                      # p90
    (C10, "“vou pensar”: pensar no quê. E a direção", "“vou pensar”: pensar no quê? E a direção"),      # p92
    # p93. ajuste: digitado "por já falado" e "Vocês não tem"; aspas retas viram curvas
    (C10, "Ó, gente, eu não sei quantos maridos que eu tive na minha vida de ter falado “não, tenho que ver com meu marido”. Os maridos, o tanto de marido que essas mulheres criam.",
          "Olha, gente, eu já nem sei quantos maridos eu tive na minha vida por já ter falado “não, tenho que ver com o meu marido”. Vocês não têm noção do tanto de “maridos” que essas mulheres criam."),
    (C10, "Olha as duas respostas pro “vou pensar”", "Olha as duas respostas para o “vou pensar”"),    # p94
    (C10, "E com o seu 200 na mão", "E com os seus R$ 200 na mão"),                                   # p95

    # --- capítulo 11 ---
    (C11, "Eu organizei por família de objeção", "Eu organizei por tipo de objeção"),                  # p99
    (C11, "você diz numa linha e segue", "você diz em uma linha e segue"),                             # p100
    (C11, "O preço não é a objeção real. Gente, o que incomoda", "O preço não é a objeção real. O que incomoda"),  # p105

    # --- capítulo 12 ---
    (C12, "E de vendedora, o que eu vi foi isso", "E como vendedora, o que eu vi foi isso"),            # p121
    (C12, "No WhatsApp o número vai pra paciente cedo demais.", "No WhatsApp o número vai para a paciente cedo demais."),  # p122
    # o gráfico da página seguinte repete a frase; fica igual à prosa
    (C12, "No WhatsApp | O número vai pra paciente «cedo demais»", "No WhatsApp | O número vai para a paciente «cedo demais»"),
    (C12, "A regra da casa pra reabrir conversa", "A regra da casa para reabrir conversa"),            # p124

    # --- anexos ---
    (AA, "Resposta vaga é cortina: algum passo", "Resposta vaga é cortina de fumaça: algum passo"),     # p133
    (AB, "As primeiras servem pra clarear a palavra que ela usou.\n", "As primeiras servem para clarear a palavra que ela usou.\n"),  # p137
    (AC, "Tudo que eu te mostrei até aqui é pra paciente que chegou", "Tudo que eu te mostrei até aqui é para a paciente que chegou"),  # p143
    (AC, "Essa paciente tá quentinha, tá morna ali. Tá só esperando", "Essa paciente já está quente ou morna. Tá só esperando"),  # p143
    (AC, "e é ele inteiro que está aqui", "e é ele que está aqui"),                                   # p143
    (AC, "Quem veio pelo quiz, que é o formulário de perguntas que ela responde antes de cair no seu WhatsApp, chega",
          "Quem veio pelo quiz (que é o formulário de perguntas que ela responde antes de cair no seu WhatsApp) chega"),  # p145
    # p146: só realçado, sem texto; é o mesmo "pro" que ele trocou em todas as outras onze vezes
    (AC, "é caso pro feed", "é caso para o feed"),
]

# --- numeração: "Capítulo" em tudo (decisão do Sávio, 15/set) ---
# "Prova nº" sai. Nos capítulos de passo o rótulo vira capítulo, e o passo fica no campo `passo`,
# que é de onde o render tira o trilho da abertura.
PROVA_TEMA = {"01": "O caso que abriu este arquivo", "02": "O princípio",
              "10": "Objeções", "11": "Respostas", "12": "Diagnóstico"}
for num, tema in PROVA_TEMA.items():
    arq = next(pathlib.Path(__file__).resolve().parent.glob(f"manuscrito/{num}-*.md")).relative_to(pathlib.Path(__file__).resolve().parent)
    TROCAS.append((str(arq), f'prova: "Prova nº {num} · {tema}"', f'prova: "Capítulo {num} · {tema}"'))
for passo in range(1, 8):
    cap = f"{passo + 2:02d}"
    arq = next(pathlib.Path(__file__).resolve().parent.glob(f"manuscrito/{cap}-passo-*.md")).relative_to(pathlib.Path(__file__).resolve().parent)
    TROCAS.append((str(arq),
        f'kicker: "Passo {passo:02d}"\nprova: "Prova nº {cap} · Passo {passo} de 7"',
        f'kicker: "Capítulo {cap}"\npasso: "{passo}"\nprova: "Capítulo {cap} · Passo {passo} de 7"'))
    TROCAS.append((str(arq), f'hud: "Script 715 · Passo {passo:02d} / 07"', f'hud: "Script 715 · Capítulo {cap} · Passo {passo}/7"'))


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
