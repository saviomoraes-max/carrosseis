# Script 715 · ideias pra leitura mais interessante

Estado: 09/set/2026. O que já entrou no render e o que depende de decisão do Sávio.

## Já feito nesta rodada (render v2, 121 páginas)

1. Respiro: parágrafo com 40px embaixo, entrelinha 1.5, mais ar sob o kicker. Página caiu de ~200 pra ~140 palavras.
2. Cena vira transcrição de WhatsApp: balão da paciente à esquerda, o seu à direita (dourado).
3. Trilho dos 7 passos no topo da abertura de cada passo (o passo do capítulo aceso).
4. "Como ela lê você" vira quadro: ponto vermelho (leitura negativa) e ponto dourado (positiva), frase literal do framework.
5. "Quando avançar" vira checklist numerado com caixas (itens literais do framework).
6. Frase-prova em página inteira (kicker "Prova") e pergunta final de cada capítulo em página inteira (kicker "Pergunta em aberto", rótulo do próprio DS).
7. Gráficos: linha do tempo da salinha (cap. 1), duas salinhas (cap. 1), funil 5 contatos → 1 agendamento (cap. 2), grade das 8 bases (cap. 2), bastão com ela × bastão com você (cap. 2), os 3 passos do fechamento (cap. 9), objeção real × cortina de fumaça (cap. 10), trilho completo na cola (anexo A).
8. Frase pronta com fio dourado à esquerda; "o que evitar" com fio vermelho.

Tudo vetor e texto, no vocabulário do DS (Space Mono, hairline, ponto, barra). Sem ícone, sem ilustração, sem foto.

## Feito na rodada de 09/set (render v3, 137 páginas)

9. **Páginas-marcador entre as partes (era a proposta B).** Quatro divisórias: Antes do
   script (01-02), Os sete passos (03-09), Objeção e resposta (10-11), Pra usar no dia
   (12 + anexos). Cada uma lista os capítulos da parte, então funciona como sumário local.
   Os rótulos são navegação, não doutrina: nenhuma afirmação nova entrou.
10. **Contracapa (era a I).** O convite e o link do CTA, com o texto LITERAL do capítulo 12.
11. **Barra de progresso no rodapé (era a G).** Hairline com a posição da leitora no livro.
12. **Cola exportada como PNG (era a E).** `render/cola/` tem três telas 1080×1920 geradas
    por `cola_png.py`, com tipografia própria de consulta rápida. Recortar página do PDF não
    servia: entregava o corpo de leitura de 38px e perdia as notas entre as frases pontas
    ("a chave PIX vai numa mensagem separada"). O empacotamento é medido no browser, não
    chutado, então nada estoura o rodapé.
13. **Capítulo 11 em cartão (era a A, e ficou melhor que a proposta).** Duas colunas não cabem
    em 9:16. Virou cartão vertical com três slots rotulados: ELA MANDA, SE RESPONDER ASSIM,
    PERDE (vermelho) e O QUE CONTINUA A CONVERSA (dourado). Como o andaime virou rótulo, o
    detector do capítulo caiu de 40 pra 22 sem trocar uma palavra — a conversão é provada
    neutra por contagem de palavras.
14. **O render se audita.** Toda compilação reporta página de miolo abaixo de 35% de ocupação.
    As páginas vazias por desenho (abertura, parte, capa, sumário, contracapa, frase inteira)
    ficam fora da conta.

## Propostas (a validar)

~~A. Cap. 11 em duas colunas~~ — FEITO, como cartão (item 13). Duas colunas não cabem em 9:16. Era: "se quiser perder" (vermelho) × "se quiser continuar" (dourado). Hoje é prosa + card; em coluna vira consulta rápida no celular.
~~B. Páginas-marcador~~ — FEITO (item 9). Era: Parte 1 (caps 1-2, a tese), Parte 2 (caps 3-9, os 7 passos), Parte 3 (caps 10-11, objeções), Parte 4 (cap. 12 + anexos). Uma página escura com o número da parte gigante, como a abertura de capítulo.
C. Um caso completo em balões, do "quanto custa" ao comprovante, como anexo C. Precisa de fonte: uma conversa real anonimizada (canal de depoimentos no Slack) ou um roteiro que a Ana aprove. Não invento.
D. Anexo B também indexado "pelo que ela disse": a paciente escreveu X → você responde Y. Hoje é por etapa.
~~E. Cola em PNG~~ — FEITO (item 12). Era: 1080×1920 separado, pra doutora salvar no celular e abrir sem o PDF.
F. Links internos no PDF: sumário clicável e toda menção "capítulo 11" vira link. Custo baixo no render.
~~G. Barra de progresso~~ — FEITO (item 11). Era: (hairline com a posição), além do "Passo 03/07" do HUD.
H. Glossário de uma página: bastão, cortina de fumaça, presente inaceitável, leitura, transição.
~~I. Contracapa~~ — FEITO (item 10). Era: (hoje o link está solto no cap. 12).
J. Áudio: se a Ana gravar cada capítulo, QR/link na abertura. Fecha o problema de voz de vez.
K. Carimbos tipográficos nas aberturas ("Caso aberto", "Arquivo confidencial"), no vocabulário dos kickers do DS. Só se não pesar.

## O que NÃO vou fazer sem fonte

Exercícios, contas, metas ou casos que não estejam nos PDFs ou na fala da Ana. O exercício das 20 conversas saiu por isso.

## Ainda de pé, e o que cada uma custa

- **C (caso completo em balões)** e **J (áudio da Ana por capítulo)** dependem dela: fonte
  nova ou gravação. Não invento conversa.
- **D (anexo B indexado pelo que ela disse)**, **H (glossário)** e **K (carimbos)** são
  trabalho de render sem fonte nova. O glossário é o mais arriscado: definição inventada já
  passou por quatro rodadas neste livro uma vez (ver `paridade-de-juri.md`), então só entra
  com cada verbete literal de fonte.
- **F (links internos)** já está feito desde 08/set: sumário clicável e toda menção a
  "capítulo N" e "anexo A/B" vira link no PDF.
