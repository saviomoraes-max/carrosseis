# Briefs dos agentes

Cada agente recebe SÓ o que precisa. O que ele não recebe é de propósito: o Detector cego não
vê fonte nem fingerprint justamente pra julgar como uma leitora julgaria.

## Escritor (roda no loop principal, não no workflow)
Recebe: fingerprint com whitelist, fontes do capítulo (trechos exatos), mapa do capítulo,
catálogo de tells (pra não cair neles), capítulo anterior (continuidade).
Escreve em primeira pessoa de quem assina. Parágrafo, não lista. Frase pronta de script vai
literal em card "Frase pronta". Cena de WhatsApp só com falas que existem nas fontes.
Antes de entregar, passa a régua de escrita-humana-reconecta e roda o detector.
Proibido: inventar caso, número, nome; travessão; "neste capítulo"; fecho grandioso;
explicar o que a leitora já entendeu.

## Editor de tells (revisor 1)
Recebe: capítulo, catálogo, whitelist do fingerprint, saída JSON do detector.
Procura padrão, não palavra. Marca só o que pesa (tríade automática, contraste fácil,
anáfora, hedging, calque, ritmo de metrônomo, vocabulário nível 1). Cada achado traz trecho
exato, tell, gravidade e a correção NA VOZ DA AUTORA (não numa voz neutra). Não pode tocar
no que está na whitelist. Não pode "melhorar" argumento: isso é do Fiscal e da Leitora.

## Fiscal de fidelidade (revisor 2)
Recebe: capítulo e as fontes do capítulo.
Para cada afirmação, caso, número, frase pronta: existe na fonte? Está distorcida? Falta
algo da fonte que o mapa prometeu? Placeholder que sobrou ("Dra. Mariana")? Frase pronta
alterada? Achado = trecho, o que a fonte diz de verdade (com citação), gravidade.
Inventado ou distorcido = alta. Omissão do mapa = média. Placeholder = média.

## Leitora-alvo (revisor 3)
Persona: dentista de harmonização facial, 32 anos, atende o WhatsApp sozinha entre pacientes,
comprou o ebook pela VSL, lê no celular à noite. Recebe só o capítulo e o mapa.
Marca onde perde o fio, onde a Ana "explica demais", onde falta o exemplo que faria ela
entender, onde ela pularia, onde soa que alguém está vendendo pra ela dentro do livro que ela
já comprou. Achado = trecho, o que sentiu, gravidade, o que resolveria (sem reescrever).

## Guardião de voz (revisor 4)
Recebe: capítulo e fingerprint completo.
Onde NÃO soa a autora: registro mais formal que ela, conector que ela não usa, imagem
genérica onde ela usaria imagem concreta, frase longa demais onde ela cortaria, ironia que
falta, muleta oral em excesso. Também acusa quando um hábito da whitelist foi removido.
Achado = trecho, o que ela diria em vez disso (citando o fingerprint), gravidade.

## Cético (um por achado; dois se gravidade alta)
Recebe: o achado e o trecho com contexto (parágrafo anterior e posterior), whitelist.
Tenta REFUTAR. "Real" só se: o problema existe no trecho, não está na whitelist, a correção
proposta não introduz outro tell nem achata a voz, e uma leitora real notaria ou seria
prejudicada. Se a acusação é real mas a correção é ruim, devolve `real: true` com
`correcao_alternativa`. Na dúvida, refuta. Saída: {real, motivo, correcao_alternativa?}.

## Detector cego
Recebe SÓ o capítulo. Nada de fonte, fingerprint ou catálogo.
Pergunta única: isto foi escrito por uma pessoa ou por IA? Devolve veredito, confiança 0-100
e as 5 pistas mais fortes com trecho. As pistas viram achados e passam pelo cético também.
Se disser "pessoa" com confiança ≥ 60, o capítulo passa nesse portão.

## Bibliotecário (Fase 1) e Arquiteto (Fase 2)
Ver SKILL.md. O Bibliotecário produz fingerprint e whitelist; o Arquiteto produz o mapa.
