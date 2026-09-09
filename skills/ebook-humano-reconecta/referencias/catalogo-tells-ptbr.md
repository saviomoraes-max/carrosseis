# Catálogo de tells de IA em português do Brasil

Referência do Escritor, do Editor de tells, do cético e do `detector_ptbr.py`. Leitura antes de redigir capítulo, consulta durante a revisão.

## A tese

IA escrevendo em português quase sempre está escrevendo em inglês por baixo. O modelo raciocina nos padrões da língua em que foi mais treinado e emite palavras em português. O resultado é um rascunho inglês traduzido: as viradas retóricas são as do inglês, as locuções são decalcadas, a ordem das palavras é a inglesa, o "você" aparece em toda frase porque o inglês não deixa cair o sujeito. Essa é a tese do jooray/humanizer para eslovaco e tcheco (§45 a §54 daquele skill) e do luquiluke/claude-book-skill para espanhol (lang/es.md, seção 4, "calcos del inglés, el tell más grave"). Vale igual pro PT-BR.

Consequência prática: consertar só o vocabulário (trocar "crucial" por "importante") deixa o texto com a mesma cara. O que denuncia é a estrutura (encenação, ritmo, inflação) e a tradução (calques, registro). As famílias 1 a 5 vêm do corpus internacional (Wikipedia e os cinco repositórios). As famílias 6 e 7 são o que nenhuma skill pública cobre pra português.

## Como pesar

Um tell sozinho raramente prova nada. Uma pessoa escreve "além disso" e usa uma antítese. O que acusa é o cluster: três ou quatro tells de famílias diferentes no mesmo parágrafo. Regra herdada do blader (§"When not to act") e da Wikipedia (seção "Ineffective indicators").

Gravidade neste catálogo:

- alta: um avistamento já justifica edição. Quase nenhuma pessoa escreve isso de propósito.
- média: conta em dupla. Precisa de companhia de outro tell no mesmo trecho.
- baixa: só entra na conta em cluster de três ou mais, ou em densidade.

Contar o cluster uma vez. Se um travessão, uma tríade e um negrito caem na mesma frase, é um tell forte, não três (jooray, "Detection guidance").

O que fica fora do catálogo: capa de carrossel, headline de anúncio e título de capítulo têm regime próprio (regra de capa da casa: pergunta, antítese literal, reframe). Este catálogo mira o miolo do ebook, a prosa que a leitora lê por dez minutos seguidos.

Regra de precedência: o fingerprint da autora (Fase 1) manda. Se a whitelist diz que ela usa "virada de chave" toda semana, o Editor não corta. O catálogo é filtro negativo; a voz é o alvo positivo. Mesma regra do luquiluke ("style-profile.md outranks this file").

Regras da marca que valem por cima de tudo: sempre "harmonização facial", nunca "HOF" nem "orofacial". Nunca "high ticket", "engajamento", "algoritmo", "solução", "ecossistema", "conteúdo", "funil", "mindset" (banco-de-termos e instrução desta skill; ver nota sobre "ecossistema" no mapa de fontes).

Formato de cada tell: nome, origem (pra rastrear), como aparece em português com exemplos do tipo que uma IA escreveria num ebook de vendas pra dentistas e biomédicas de harmonização facial, o conserto, a guarda de falso positivo e a gravidade. Nos exemplos sobre travessão, o caractere aparece como [travessão] porque este arquivo não pode conter nenhum.

---

## Família 1: Encenar em vez de afirmar

A frase sinaliza importância em vez de acrescentar um fato. É a família mais frequente nos modelos atuais e a que mais sobrevive a uma revisão superficial.

### 1.1 Contraste fácil ("não é X, é Y")

Origem: blader §1; Wikipedia "Negative parallelisms" (três subtipos: "not just X but also Y", "not X but Y", "X rather than Y"); escrita-humana-reconecta tell 1; luquiluke es.md ("no solo X, sino también Y, la firma más delatora del español IA").

Como aparece:
> Não é sobre técnica. É sobre posicionamento.
> A paciente não quer só um procedimento, ela quer uma transformação.
> Isso não significa que você deva baixar o preço. Significa que você precisa mudar quem te procura.
> Mais do que uma consulta, uma experiência.

A metade negativa nomeia algo que ninguém afirmou, só pra metade positiva parecer maior. A forma partida em duas frases ("Isso não significa X. Significa Y.") e a cauda negativa ("..., sem barganha") são a mesma coisa.

Conserto:
> Quem te procura pelo procedimento pede desconto. Quem te procura pelo problema resolvido pergunta quando tem horário.
> Você não precisa baixar o preço. Precisa mudar quem te procura: e isso começa pelo que o seu perfil mostra.

Guarda de falso positivo: a antítese é recurso central da voz RECONECTA (dna.md, seção 4: "Paciente não barganha com quem ela enxerga como única. Ela barganha com quem ela enxerga como opção."). Ela fica quando as duas metades carregam informação e quando aparece uma vez por capítulo, na posição de frase-frame. Vira tique na terceira vez na mesma página ou quando a metade negativa é boneco de palha. Frase-assinatura do banco de termos ("Técnica não enche agenda. Posicionamento enche.") é literal e intocável.

Gravidade: alta (em cluster de duas ou mais por página), média (isolada).

### 1.2 Fecho de uma linha que repete o parágrafo

Origem: blader §2; jooray §32; escrita-humana-reconecta tell 6 ("fecho grandioso"); conor "Manufactured punchlines".

Como aparece:
> [parágrafo explicando a consulta paga] É simples assim.
> [parágrafo sobre agenda] E é isso que separa quem cresce de quem sobrevive.
> Leia isso de novo.
> Deixa isso assentar por um segundo.

A linha pede que a leitora pause numa afirmação em vez de acrescentar algo. Quando o mesmo fecho aparece depois de várias seções ("Esse é o ponto.", "É aí que a mágica acontece."), é regra, não escolha.

Conserto: cortar o fecho e terminar no último fato concreto. Se a seção precisa de fim, o fim é o número, o nome ou a instrução: "Ela cobrou 300 reais na primeira consulta paga. Em março, 47 delas."

Guarda: uma frase curta carrega ênfase quando traz fato novo. "Ela nunca mais deu desconto." depois de um caso é fecho legítimo. O tell é o fecho que só reafirma.

Gravidade: alta (quando repete o parágrafo), média (uma vez por capítulo).

### 1.3 Fragmentos em rajada

Origem: blader §2; jooray §11 e §32 ("staccato contrast", "The 'Not X' pattern"); conor "Negation chains" e "Staccato drama".

Como aparece:
> Sem desconto. Sem promoção. Sem barganha. Só paciente que investe.
> Ela não postou mais um antes e depois. Não pediu avaliação. Não implorou. Ela posicionou.
> Agenda cheia. Ticket alto. Recorrência garantida.

Três ou mais fragmentos da mesma forma, cada um posando de revelação. A rajada encena decisão; os itens raramente carregam informação própria.

Conserto: manter um fragmento que mereça a ênfase e devolver o resto pra frase com verbo. "Ela parou de postar antes e depois. No lugar, mostrou o caso inteiro da paciente de 52 anos que voltou a tirar foto de perfil. Em duas semanas, seis consultas pagas."

Guarda: a repetição intencional é recurso da casa (dna.md, seção 4: "Mais uma dentista que posta botox. Mais uma biomédica que posta preenchimento. Mais uma clínica com antes e depois genérico."). Uma rajada por capítulo, com itens que enumeram coisas diferentes, é voz. Duas rajadas no mesmo capítulo, ou uma rajada de negativas, é regra. Enumeração factual dentro de frase ("a consulta não tem desconto, não tem parcelamento em doze vezes e não tem brinde") é lista, não drama.

Gravidade: alta (duas ou mais rajadas por capítulo), média (uma).

### 1.4 Frase que soa profunda (aforismo de fôrma)

Origem: blader §3; jooray §28 e §33; conor "Aphorism formulas" e "Persuasive-authority tropes".

Como aparece:
> Posicionamento é a moeda da confiança.
> A agenda é o espelho do seu posicionamento.
> No fundo, a questão real é a sua relação com o próprio valor.
> Desconto é uma armadilha.
> O que realmente importa é a percepção.

"X é a moeda de Z", "X é o espelho de Y", "a verdadeira questão é", "no fundo", "o que realmente importa": uma afirmação comum vestida de verdade escondida. A fantasia não acrescenta detalhe.

Conserto: substituir a fôrma pela afirmação concreta. "Paciente que confia paga sem perguntar preço. Ela confia quando viu o caso inteiro antes de mandar mensagem."

Guarda: as frases-assinatura validadas no banco de termos ("Você não perdeu essa paciente pro concorrente. Você perdeu pro silêncio.", "Quem se justifica, perde.") são da casa e entram literais, na posição de frame antes do CTA (dna.md, seção 2). O tell é o aforismo novo, cunhado pela IA na hora, com a fôrma "X é o Y de Z".

Gravidade: alta (aforismo novo), nenhuma (frase-assinatura da casa).

### 1.5 Corrida de aproximação antes do ponto

Origem: blader §4; jooray §29; conor "'Let's' constructions" e "Signposting"; luquiluke §4 ("Let's explore / dive into").

Como aparece:
> Vamos mergulhar no que faz uma consulta paga funcionar.
> Aqui vai o que você precisa saber sobre recorrência.
> Antes de continuar, é importante entender o contexto.
> Vamos por partes.
> Sem mais delongas:

A autora anuncia o ponto em vez de fazer o ponto. Em português, "vamos explorar", "vamos entender", "vamos por partes" e "aqui vai" são as formas mais comuns.

Conserto: apagar a corrida e começar pela afirmação. "Consulta paga funciona por um motivo só: quem pagou 300 reais pra sentar na sua cadeira já decidiu que você é a pessoa certa."

Guarda: um "vamos combinar uma coisa" dentro de parágrafo de conversa é oralidade legítima. O tell é o anúncio autônomo antes de um ponto rotineiro.

Gravidade: alta.

### 1.6 Candor encenado

Origem: blader §4 (staged candor); jooray §36 ("Performed rigor and candor") e §49 (a versão calcada em eslovaco: "povedzme si to na rovinu"); conor "Narrated candor" e "Fake-casual register".

Como aparece:
> Vou ser sincera com você: a maioria das doutoras não sabe cobrar.
> Sendo bem honesta, isso não é sobre técnica.
> A verdade é que ninguém te ensinou isso na faculdade.
> Olha, eu sei que dói ouvir isso.
> Vale a pena ser precisa aqui: recorrência não é a paciente decidir voltar.
> Vou dizer o que ninguém diz em voz alta.

A escritora anuncia que está sendo honesta, precisa ou corajosa em vez de ser. O preâmbulo certifica a frase seguinte, que quase sempre é comum. "Vou ser sincera" implica que o resto do livro não foi.

Conserto: apagar o certificado e manter a afirmação. "A maioria das doutoras não sabe cobrar. Ninguém ensinou. A grade da faculdade tem 40 horas de anatomia e zero de conversa de preço."

Guarda: "olha" e "sinceramente" no meio de frase falada são oralidade. O tell é o preâmbulo autônomo antes de um ponto comum. Uma confissão real com conteúdo ("eu cobrei 150 reais por dois anos porque tinha medo de ouvir não") fica: é a confissão, não o anúncio dela.

Gravidade: alta.

### 1.7 Discutindo com ninguém (objeção fantasma)

Origem: blader §5; jooray §37 ("Argument residue"); conor "False concession structure".

Como aparece:
> Não estou dizendo que técnica não importa.
> Alguém pode argumentar que cobrar consulta afasta paciente, mas...
> Para deixar claro: isso não é uma crítica a quem faz promoção.
> Uma abordagem tentadora seria baixar o preço da primeira sessão.

O texto responde a uma objeção que não aparece em lugar nenhum, ou rejeita uma opção que ninguém propôs. Sobra de um rascunho em que o modelo passou por mais de uma posição.

Conserto: cortar a defesa e afirmar a posição. Se a defesa esconde uma afirmação real, afirmar só ela. "Cobrar a consulta afasta quem ia pedir desconto. É pra isso que serve."

Guarda: a objeção real do avatar é matéria-prima da casa e fica, nomeada: "já contratou gestor de tráfego que prometeu lead qualificado e se decepcionou" (banco-de-termos, camada B) é objeção que a leitora carrega de verdade. Ela pode e deve ser respondida em cheio. O tell é a objeção genérica que só existe pra ser derrubada.

Gravidade: alta (duas ou mais rejeições seguidas), média (uma).

### 1.8 Pergunta retórica como transição ou fecho

Origem: conor "Rhetorical question openers" e "Stacked rhetorical questions"; luquiluke es.md ("preguntas retóricas en cadena", "¿El resultado? ¿La clave?"); escrita-humana-reconecta tell 6.

Como aparece:
> O resultado? Agenda vazia na segunda-feira.
> E o que isso significa pra você?
> Qual o problema disso? Simples.
> Você sabe cobrar? Sabe apresentar um plano? Sabe sustentar o preço quando a paciente hesita?
> [fim de capítulo] E você, está pronta pra dar o próximo passo?

A pergunta atrasa o ponto, ou finge diálogo, ou fecha o capítulo com um convite vazio. A forma "O resultado?" com resposta em fragmento é a mais frequente em PT-BR.

Conserto: responder a pergunta em vez de fazê-la. "Ela fez isso e a segunda-feira ficou vazia." Fim de capítulo termina no fato ou na instrução: "Faz essa mudança na bio hoje e me conta o que a próxima paciente perguntou."

Guarda: pergunta que a leitora de fato se faz, colocada na boca dela, é espelhamento da dor (dna.md, seção 5: "você já sentiu que..."). A regra da capa admite pergunta. Uma pergunta genuína por capítulo, com resposta desenvolvida, fica. Cadeia de três perguntas seguidas, ou pergunta de encerramento, cai.

Gravidade: alta (cadeia ou fecho), média (uma de transição).

### 1.9 Revelação por dois-pontos

Origem: jooray §35 ("Colon-reveal constructions"); conor "Infomercial engagement hooks" ("The catch?", "The kicker?", "Plot twist:").

Como aparece:
> O detalhe: ela cobrava 300 reais.
> O melhor de tudo: não precisa de tráfego pago.
> E aí vem a parte que ninguém te conta: a consulta é a venda.
> Spoiler: não é o preço.
> Plot twist: a paciente queria pagar mais.

Um sintagma nominal, dois-pontos, e uma revelação teatral em minúscula. A informação comum vira reveal.

Conserto: frase normal. "Ela cobrava 300 reais na primeira consulta." "Isso funciona sem tráfego pago."

Guarda: dois-pontos introduzindo explicação ou lista é pontuação normal e este arquivo usa. O tell é o gancho de infomercial ("o melhor:", "o detalhe:", "spoiler:") antes de um fato comum.

Gravidade: alta ("spoiler", "plot twist", "a parte que ninguém te conta"), média ("o detalhe:", "o melhor:").

### 1.10 Cenário imaginado no lugar do argumento

Origem: conor "Speculative scenario openers" ("Imagine a world where...").

Como aparece:
> Imagine uma clínica onde a agenda fecha sozinha e você só atende quem já decidiu.
> Pense num cenário em que cada paciente indica outras três.
> Visualize acordar na segunda com a semana inteira preenchida.

O cenário faz a persuasão e nenhuma prova é oferecida. É lista de desejos com moldura de hipótese.

Conserto: trocar o cenário pelo caso real com nome, cidade, número e prazo (regra do banco de termos, seção 2). "A Karollyne, em cidade de 17 mil habitantes, fechou 200 mil no ano com a agenda desse jeito. O que ela fez está no capítulo 4."

Guarda: a técnica do Futuro Perfeito (banco-de-termos) pede que a paciente descreva a vida sem o problema; um trecho de script de consulta que diz "me descreve como seria" é instrução de método, não cenário de venda. O tell é o "imagine" dirigido à leitora do ebook pra substituir prova.

Gravidade: média.

### 1.11 Emoção anunciada e etiqueta de importância

Origem: conor "Emotional flatline", "Self-labeling significance", "Confidence calibration phrases", "Lingering-attention claims"; jooray §1 ("the graded verdict").

Como aparece:
> O que mais me surpreendeu foi a resposta das pacientes.
> A parte mais interessante é que ela não mudou o preço.
> Esse último ponto é o contraintuitivo.
> Curiosamente, as doutoras mais técnicas são as que menos cobram.
> Não consigo parar de pensar nessa frase da aluna.
> E o resultado foi bem claro.

A escritora avisa como a leitora deve se sentir ("surpreendente", "interessante", "curiosamente") ou aponta pra um item da própria lista e o etiqueta ("esse é o contraintuitivo") em vez de escrever de um jeito que a leitora sinta sozinha. "Curiosamente" e "interessantemente" são decalques diretos de "interestingly".

Conserto: apresentar a coisa e deixar que ela surpreenda. "As três doutoras com mais curso na turma eram as três que cobravam menos: 180, 200 e 220 reais a consulta."

Guarda: emoção com dono e com causa fica: "fiquei com raiva quando vi o print, porque era a terceira vez no mês". O tell é a emoção sem corpo, usada como introdução de lista.

Gravidade: média.

---

## Família 2: Ritmo por regra

Tríade, anáfora, travessão e frase do mesmo tamanho aplicados em tudo, peça ou não o sentido. Uma pessoa faz qualquer um desses de propósito; o tell é a uniformidade.

### 2.1 Tríade forçada

Origem: blader §6; Wikipedia "Rule of three"; jooray §10; conor "Compulsive rule of three" e "Colon into a triple"; jooray §49 (a tríade em uma só respiração, separada por vírgula).

Como aparece:
> Uma consulta bem conduzida gera confiança, autoridade e recorrência.
> Ela precisa de clareza, coragem e método.
> O perfil precisa mostrar: quem você é, o que resolve e pra quem.
> Sem agenda, sem previsibilidade, sem paz.

Ideias em três pra soar completo, tenha ou não o sentido três partes. Adjetivo, adjetivo e adjetivo; ou três exemplos paralelos; ou três fatos curtos seguidos de uma lição.

Conserto: checar se cada item acrescenta ideia distinta. Se não, ficar com o mais forte e desenvolver. "Uma consulta bem conduzida faz a paciente voltar. É a recorrência que enche a Agenda do Milhão: 3 pacientes novas por semana e 4 retornos."

Guarda: dna.md (seção 2) pede listas com 3 a 4 itens de mesma estrutura sintática quando a lista é deliberada, com critérios claros. Lista de passos de um método com três passos reais é lista, não tríade. O tell é a tríade de adjetivos abstratos dentro da prosa, ou a terceira tríade na mesma página.

Gravidade: média (uma em prosa), alta (três ou mais por capítulo).

### 2.2 Anáfora de enfeite e mesma abertura

Origem: blader §7; jooray §12; escrita-humana-reconecta tell 2; conor "Same-opener sentence runs".

Como aparece:
> Ela sabia fazer. Ela sabia entregar. Ela só não sabia cobrar.
> Você precisa de um sistema. Você precisa de um script. Você precisa de constância.
> Talvez o problema seja a cidade. Talvez seja o preço. Talvez seja o Instagram.

Várias frases seguidas começando pelo mesmo sujeito porque a repetição foi tratada por regra, não por ouvido.

Conserto: fundir, mudar o sujeito ou começar pela ação. "Ela sabia fazer e sabia entregar. Cobrar, não."

Guarda: anáfora com propósito, uma vez por capítulo, é recurso ("Mais uma dentista... Mais uma biomédica..."). A frase sobrevivente ainda pode começar com "ela". O tell é a anáfora que não faz trabalho persuasivo, ou a segunda no mesmo capítulo.

Gravidade: média.

### 2.3 Travessão como conector universal

Origem: blader §8; Wikipedia "Overuse of em dashes"; jooray §15 e §46; escrita-humana-reconecta tell 10; dna.md seção 8 (proibição da marca); memória `feedback_sem_travessao`.

Como aparece:
> A paciente [travessão] aquela que pede desconto [travessão] não é o seu problema.
> Ela cobrou 300 reais [travessão] e ninguém reclamou.
> Posicionamento [travessão] não técnica [travessão] é o que enche agenda.
> Consulta paga [hífen solto] a reunião de vendas da clínica [hífen solto] fecha o plano.

O travessão deixa a escritora pular a decisão de como duas orações se relacionam. O hífen com espaço dos dois lados fazendo o mesmo papel é a versão preguiçosa e conta igual. Em PT-BR o travessão em prosa corrida é menos nativo do que em inglês: o uso tradicional é diálogo e aposto formal.

Conserto: vírgula, ponto, dois-pontos ou parênteses, ou reescrever. "A paciente que pede desconto não é o seu problema." "Ela cobrou 300 reais e ninguém reclamou."

Guarda: o travessão de diálogo transcrito ("[travessão] Doutora, quanto custa?") é ortografia correta em português e fica quando o livro reproduz fala. Fora disso, regra da casa é zero: portão do manuscrito é grep com zero ocorrências. Hífen dentro de palavra composta ("bem-sucedida", "pré-consulta") não é travessão.

Gravidade: alta (regra da marca, sem exceção fora de diálogo).

### 2.4 Metrônomo (frases e parágrafos do mesmo tamanho)

Origem: escrita-humana-reconecta tell 8; conor "Rhythm and uniformity" ("structure is the #1 detection signal"); luquiluke §6 ("three same-length sentences in a row"); Wikipedia "Signs of human writing / Syntax".

Como aparece: parágrafos de três frases, frases de 15 a 25 palavras, o capítulo inteiro. Nenhuma frase de três palavras. Nenhuma de quarenta. O texto pode ser lido por um leitor de tela sem soar estranho.

Conserto: quebrar de propósito. Uma frase curta. Depois uma longa, que leva a leitora por uma vírgula a mais antes de parar, com um aparte no meio, e só então fecha. Parágrafo de uma linha depois de um de dez.

Guarda: em português, frase longa com duas ou três subordinadas é normal e legível, mais do que em inglês. Picar tudo em frases curtas pra "parecer humano" produz a rajada do 1.3. O alvo é variação, não frase curta. O fingerprint da autora dá a distribuição real; a IA tende a média uniforme.

Gravidade: média (é sinal estatístico, precisa de capítulo inteiro pra pesar).

### 2.5 Blocos intercambiáveis (teste do embaralhamento)

Origem: jooray §41 ("Structural uniformity", "the reshuffle test"); conor "Paragraph-reshuffle immunity".

Como aparece: seções de tamanho quase igual, cada uma com sua lista de três, cada uma com uma frase de recapitulação no fim. Trocar o segundo e o quarto parágrafo de lugar não quebra nada.

Conserto: uma seção com dois parágrafos, outra com seis, conforme o que há pra dizer. Cada parágrafo depende do anterior: "por isso", "e foi aí que", "só que". Cortar a recapitulação: a leitora acabou de ler a seção.

Guarda: capítulo de referência (banco de perguntas, script de consulta) é lista mesmo, e os itens são intercambiáveis por natureza. O teste é pra prosa argumentativa.

Gravidade: alta (é o tell que nenhuma edição de frase corrige).

### 2.6 Esteira (repetir a ideia com outras palavras)

Origem: jooray §44 ("Treadmill effect"); luquiluke §7 ("Compression", "over-explanation is the most reliable AI tell of all"); escrita-humana-reconecta tell 7 ("explicar demais"); conor "Treadmill effect / low information density".

Como aparece:
> A consulta paga muda a relação. Quando a paciente investe antes de sentar na cadeira, o vínculo é outro. O simples ato de pagar pela avaliação já reposiciona a conversa. É a diferença entre triagem e reunião de vendas.

Quatro frases, uma ideia. Depois de contar um caso, explicar a lição que o caso já contou.

Conserto: perguntar o que cada frase acrescenta. Ficar com a mais clara. "Consulta paga não é triagem. É a reunião em que você apresenta o plano de tratamento e fecha."

Guarda: repetição pedagógica, uma vez, em palavras da leitora depois das palavras técnicas, é didática da casa ("sempre explicar o pilar ao mencionar", dna.md seção 3). O tell é a terceira reformulação.

Gravidade: alta (quando o corte de metade não perde informação).

### 2.7 Variação elegante (ciclar sinônimos)

Origem: Wikipedia "Lexical diversity/elegant variation"; jooray §12; conor "Synonym cycling".

Como aparece:
> A profissional precisa entender isso. A doutora que não cobra perde. A especialista que se posiciona ganha. A dentista que segue o método fecha a agenda.

Quatro nomes para a mesma pessoa em quatro frases, ou "o método", "o sistema", "a abordagem", "a estratégia" para a mesma coisa.

Conserto: um nome para uma coisa. "Doutora" é o pronome de segunda pessoa da casa (dna.md, seção 3) e pode repetir. "Fábrica de Contatos" é sempre "Fábrica de Contatos".

Guarda: a escola brasileira ensina a evitar repetição de palavra, e muita gente escreve assim de propósito (a Wikipedia nota o mesmo sobre a escola italiana). O tell é a variação que confunde o referente ou que troca o termo proprietário por sinônimo genérico ("o sistema" no lugar de "Fábrica de Contatos").

Gravidade: baixa (sozinha), média (quando troca termo proprietário).

### 2.8 Contraste no auxiliar

Origem: conor "Stranded auxiliary contrast" ("The tool died; the data didn't.").

Como aparece:
> A técnica ela tinha. O posicionamento, não.
> A concorrente baixou o preço. Ela não.
> O curso ensinou anatomia. Cobrança, não.

Uma reviravolta que pousa num "não" solto. Uma vez é frase boa. Como ritmo recorrente é assinatura de modelo.

Conserto: racionar. Se o capítulo já tem uma, escrever a próxima por extenso. "A concorrente baixou o preço pra 150. Ela manteve 300 e explicou por quê na própria bio."

Guarda: uma por capítulo é estilo. Só a densidade separa voz de tique.

Gravidade: baixa.

---

## Família 3: Inflação e autoridade emprestada

O fato de baixo costuma ser sólido. A tarefa é tirar a roupa.

### 3.1 Significado inflado

Origem: blader §13; Wikipedia "Undue emphasis on significance, legacy, and broader trends"; jooray §1; conor "Significance inflation" e "Generic future-narrative closers".

Como aparece:
> A consulta paga marca um divisor de águas na carreira de qualquer profissional.
> Esse foi um passo fundamental na jornada dela rumo ao posicionamento de elite.
> Cobrar pela avaliação representa uma mudança de paradigma no mercado da estética.
> O cenário da harmonização facial está em constante evolução.

Um detalhe comum é dito marcar uma mudança, provar um legado ou prometer um futuro.

Conserto: manter o fato e cortar o significado. "Ela começou a cobrar 300 reais pela consulta em fevereiro. Em abril tinha 31 consultas pagas no mês."

Guarda: "virada de chave" é termo da casa (dna.md, cluster Transformação) e pode nomear o momento em que a doutora mudou de prática, desde que o momento tenha nome e data. O tell é "divisor de águas", "mudança de paradigma", "marco" sem o fato embaixo.

Gravidade: alta.

### 3.2 Carimbo de importância no fim da frase

Origem: jooray §1 ("The appended significance stamp": "and that matters", "and the difference matters"); conor "Consequence-free explanation" ("This matters because").

Como aparece:
> As duas fazem o mesmo procedimento, e a diferença importa: uma cobra a consulta, a outra não.
> Ela mudou o nome do perfil, e isso faz toda a diferença.
> Isso importa porque é fundamental.
> E isso não é detalhe.

Uma oração pendurada no fim da frase pra avisar que a frase contou. Não traz informação: dá nota à frase a que está presa.

Conserto: cortar o carimbo. Se a fonte diz por que importa, colocar a consequência no lugar. "Uma cobra a consulta e fecha 1 plano a cada 3. A outra faz avaliação grátis e fecha 1 a cada 12."

Guarda: frase que diz que algo importa e em seguida diz o que decorre disso está trabalhando. O tell é o carimbo nu.

Gravidade: alta.

### 3.3 Autoridade vaga

Origem: blader §17; Wikipedia "Vague attributions and overgeneralization of opinions"; conor "Vague attributions" e "Vague third-party validation"; memória `feedback_nunca_inventar_dados`.

Como aparece:
> Especialistas apontam que a consulta paga aumenta a taxa de fechamento.
> Estudos mostram que pacientes valorizam mais o que pagam.
> O mercado reconhece que posicionamento é o novo diferencial.
> Segundo pesquisas recentes, 80% das profissionais não sabem precificar.

Uma autoridade sem nome sustenta a afirmação. O número sem fonte é o pior caso: o modelo inventa a estatística.

Conserto: nomear a fonte ou cortar a atribuição e afirmar. Régua da casa (banco-de-termos, seção 2): prova é nome, cidade, número e prazo. "A Déborah, em Vitória, passou de 1 fechamento a cada 10 avaliações grátis pra 1 a cada 3 consultas pagas, entre março e junho." Sem dado real na pasta `fontes/`, sem dado.

Guarda: "na minha experiência", "aposto que", "o que eu vi nas 400 mentoradas" é opinião com dono, e fica (escrita-humana-reconecta tell 9). A falta de citação, sozinha, não é tell: a maior parte do que se escreve não tem fonte. O tell é o "especialistas" e o número redondo sem origem.

Gravidade: alta (número sem fonte), média (autoridade vaga sem número).

### 3.4 Lista de prestígio e "presença ativa"

Origem: Wikipedia "Canned emphasis on notability, attribution, and media coverage"; blader §17 (prestige list); conor "Notability name-dropping".

Como aparece:
> Já foi citada pela Forbes, Exame e Veja.
> Mantém presença ativa nas redes sociais, com mais de 100 mil seguidores.
> Reconhecida por veículos nacionais e regionais.
> Com formação nas melhores instituições do país.

Uma lista de nomes escora a pessoa; a lista de veículos e a contagem de seguidores estão no lugar do que ela disse ou fez.

Conserto: um caso com contexto. "Em 2025 ela deu uma aula no Momento Reconecta sobre como fechou a agenda de Natal em cidade de 40 mil habitantes." Se não há contexto, cortar a lista.

Guarda: nome e cidade de uma mentorada com número é prova, não prestígio. O tell é o rol de logotipos.

Gravidade: média.

### 3.5 Rider de gerúndio no fim da frase

Origem: blader §15; Wikipedia "Superficial analyses"; jooray §3 e §48 (o modelo eslovaco: "transgressive and participle padding"); conor "Superficial -ing analyses".

Como aparece:
> Ela passou a cobrar a consulta, garantindo previsibilidade, reforçando sua autoridade e consolidando seu posicionamento.
> O Supercaso apresenta o problema da paciente, gerando identificação e fortalecendo a conexão.
> Isso reduz objeções, contribuindo para uma agenda mais qualificada.

Uma oração em -ndo é parafusada num fato simples pra soar mais fundo. O verbo favorito em PT-BR é "garantindo", seguido de "reforçando", "contribuindo para", "gerando", "proporcionando", "permitindo", "possibilitando", "fortalecendo", "consolidando", "demonstrando", "evidenciando".

Conserto: manter o fato. Se o rider tem afirmação real, promover a frase própria. "Ela passou a cobrar a consulta. Quem paga 300 reais pra sentar já decidiu que ela é a pessoa certa, e isso apareceu na taxa de fechamento: 1 em 3."

Guarda: gerúndio de ação simultânea real ("ela entrou na sala segurando o iPad") é gramática, não rider. O tell é o gerúndio de significado abstrato pendurado depois da vírgula.

Gravidade: alta (é um dos tells mais denunciadores em PT-BR, porque a escrita brasileira espontânea usa pouco esse gerúndio de análise).

### 3.6 Linguagem de vitrine

Origem: blader §16; Wikipedia "Promotional and advertisement-like language"; jooray §4; conor "Promotional language"; gregorymm 2c.

Como aparece:
> Um método robusto e abrangente, desenvolvido para profissionais que buscam excelência.
> Uma abordagem inovadora e de ponta para o mercado da estética.
> Referência no mercado, com resultados expressivos e comprovados.
> Um ecossistema completo de suporte.

O texto lê como folheto. "Robusto", "abrangente", "de ponta", "inovador", "referência", "excelência", "expressivo", "comprovado" são o kit.

Conserto: dizer o que a coisa é. "O método tem quatro etapas. A primeira é tirar da cabeça a ideia de que sua cidade é pequena demais."

Guarda: "elite" é palavra de tom da marca ("posicionamento de elite", banco-de-termos) e "exclusivo" é uma das cinco palavras-chave de tom; ficam quando são posicionamento, caem quando são hype de headline. O tell é o adjetivo de brochura sem fato.

Gravidade: alta.

### 3.7 Fugir do "é" e do "tem" (cópula evitada)

Origem: blader §18; Wikipedia "Avoidance of basic copulatives"; jooray §8 e §47 (o modelo eslovaco: "predstavuje", que em português é "representa"); conor "Copula avoidance"; gregorymm 3a.

Como aparece:
> A consulta paga representa um diferencial competitivo.
> O Supercaso se configura como a principal ferramenta de atração.
> A clínica conta com três salas e dispõe de equipamento de ponta.
> O método se destaca por sua abordagem prática.
> A agenda fechada constitui o objetivo final.
> Recorrência refere-se ao retorno programado da paciente.

"Representa", "se configura como", "conta com", "dispõe de", "se destaca por", "constitui", "refere-se a", "oferece", "apresenta", "possui" no lugar de "é" e "tem". "Representa" é o pior e mais confiável.

Conserto: "é", "tem", "faz". "A consulta paga é o diferencial." "A clínica tem três salas." "Recorrência é a paciente voltar porque você marcou o retorno antes de ela sair."

Guarda: "conta com" em frase falada ("pode contar comigo") é outra coisa. "Possui" em texto jurídico ou clínico é registro nativo. O tell é a densidade: três "representa/constitui/dispõe" na mesma página.

Gravidade: alta ("representa", "se configura como", "constitui"), média ("conta com", "possui", "oferece").

### 3.8 Conexão vaga

Origem: blader §14; Wikipedia "Vague expression of connection or association".

Como aparece:
> Ela está ligada a projetos de educação em harmonização facial.
> O resultado está associado a uma mudança de posicionamento.
> Profissionais relacionadas ao método relatam crescimento.

O texto diz que duas coisas se ligam sem dizer como. "Ligado a", "associado a", "relacionado com", "vinculado a" escondem se ela fundou, deu aula, foi aluna ou só curtiu um post.

Conserto: nomear a relação que a fonte dá. "Ela dá aula de conversa de preço na mentoria desde 2024." Se a fonte não diz, manter o vago em vez de inventar o papel.

Guarda: "associado a" em contexto clínico ("edema associado ao procedimento") é termo técnico.

Gravidade: média.

### 3.9 Promessa sem prova

Origem: dna.md seção 8 ("Promessa sem prova social ou dado concreto" é proibição completa); banco-de-termos camada A ("Fature R$100k", "qualquer profissional consegue", "% em headline"); gregorymm 4b ("specificity over abstraction").

Como aparece:
> Resultados expressivos em poucas semanas.
> Crescimento exponencial da agenda.
> Qualquer profissional consegue aplicar e ver retorno imediato.
> Aumente seu faturamento de forma consistente.

Adjetivo no lugar de número. "Expressivo", "exponencial", "imediato", "consistente", "significativo" são a roupa de uma promessa que não tem caso embaixo.

Conserto: um caso, com nome, cidade, número e prazo, ou nada. "A Rosso, em Chapecó, saiu de 70 mil pra 200 mil por mês em 14 meses." Sem caso na pasta de fontes, a frase sai.

Guarda: promessa é o negócio; o ebook vende. O que a casa exige é a prova adjacente (memória `feedback_prova_obrigatoria_reuso_liberado`: depoimento volta em todo post de aplicação). O tell é a promessa órfã.

Gravidade: alta.

### 3.10 Intensificador oco ("real", "verdadeiro", "genuíno")

Origem: conor "'Real/actual' adjective inflation", "Hollow intensifiers"; jooray §36 (asserted specificity: "specific", "particular", "precise").

Como aparece:
> Uma verdadeira transformação na forma de atender.
> Resultados reais para profissionais reais.
> Uma conexão genuína com a paciente.
> Isso realmente funciona.
> Existe um motivo específico pra isso.

"Real", "verdadeiro", "genuíno", "autêntico" grudados num substantivo abstrato sugerem que o resto do mercado é falso, sem dizer o que faz este ser o verdadeiro. "Específico" promete o detalhe e a frase não entrega.

Conserto: tirar o adjetivo e pôr a coisa específica. "A paciente conta o que a incomoda antes de você falar de procedimento. É assim que a conversa muda."

Guarda: "resultado real" e "case real" são termos da casa (banco-de-termos, seção 2) quando vêm seguidos de nome, cidade, número e prazo. Aí "real" está fazendo trabalho: separa o caso nomeado do "resultado típico" que a casa proíbe. O tell é o "real" sozinho. Contraste nomeado também fica: "resultado real, não print de simulação".

Gravidade: média.

### 3.11 Novidade inflada e rótulo inventado

Origem: conor "Novelty inflation" ("the failure mode nobody's naming", "a problem nobody talks about", "invented labels"); jooray §33.

Como aparece:
> O erro silencioso que ninguém fala sobre precificação.
> O que ninguém te conta sobre consulta paga.
> Isso é o que eu chamo de "paradoxo da competência".
> Existe um fenômeno que batizei de "síndrome da agenda vazia".

Reivindica escassez de conhecimento onde não há, ou cunha um termo no meio da frase e nunca o define.

Conserto: descrever o mecanismo em vez de batizá-lo. Se o nome é da casa, definir na primeira vez em linguagem simples (regra do dna.md: "sempre explicar o pilar ao mencionar"). "Invisibilidade Estratégica é isso: você existe, tem caso, atende bem, e o mercado te vê como mais uma que faz harmonização facial."

Guarda: os termos proprietários (Invisibilidade Estratégica, Presente Inaceitável, Cardápio de Serviços, Derretimento Facial) são rótulos legítimos porque têm definição e uso recorrente. "O que ninguém te conta" pode aparecer numa capa de carrossel pela regra de capa; no miolo do ebook cai.

Gravidade: alta (rótulo cunhado sem definição), média ("ninguém fala").

### 3.12 Falsa amplitude ("de X a Y", "seja você X ou Y")

Origem: Wikipedia e jooray §13 ("False ranges"); conor "Template phrases" ("Whether you're X or Y"); luquiluke es.md ("desde X hasta Y decorativo").

Como aparece:
> Seja você recém-formada ou com vinte anos de clínica, o método funciona.
> Da bio ao pós-consulta, tudo precisa comunicar posicionamento.
> De cidade pequena a capital, o problema é o mesmo.
> Tanto a dentista quanto a biomédica, tanto a iniciante quanto a experiente.

Extremos emparelhados pra soar amplo. "Seja você X ou Y" quer dizer "todo mundo", e a casa tem frase sobre isso: "Se você fala com todo mundo, você não se comunica com ninguém" (banco-de-termos, frases-assinatura).

Conserto: escolher a leitora. "Este livro é pra quem já atende bem e ainda ouve 'vou pensar' no fim da consulta."

Guarda: "O problema nunca foi a cidade" é frase validada da casa e aborda a objeção da cidade pequena de frente. Aí o contraste tem alvo. O tell é a faixa decorativa.

Gravidade: média.

### 3.13 Analogia empilhada

Origem: conor "Notability name-dropping / historical analogy stacking"; dna.md seção 2 (a analogia externa forte, única: Joshua Bell no metrô).

Como aparece:
> Assim como a Apple, a Nike e a Tesla, você precisa vender uma ideia, não um produto.
> É como um restaurante estrelado, uma grife de luxo ou um consultório em Nova York.

Três analogias de passagem que substituem o argumento. Nenhuma é desenvolvida.

Conserto: uma analogia, levada até o fim. "Joshua Bell tocou um Stradivarius no metrô de Washington e arrecadou 32 dólares. Três dias antes, o ingresso pra ouvir o mesmo violino custava 100. Talento sem posicionamento é música de 3 milhões tocada no metrô."

Guarda: a analogia externa forte, única e desenvolvida, é abertura típica da casa. O tell é a montagem de três.

Gravidade: média.

---

## Família 4: Formatação por regra

Template e editor visual também produzem formatação limpa. O tell é decoração em todo item.

### 4.1 Negrito decorativo

Origem: blader §19; Wikipedia "Overuse of boldface"; jooray §16; memória `feedback_tom_de_comunicacao` (cortar bold ceremonial).

Como aparece: "consulta paga", "plano de tratamento", "posicionamento" em negrito toda vez que aparecem; a frase de efeito de cada parágrafo em negrito; "Dica:" em negrito.

Conserto: tirar o negrito. Se algo é importante o bastante pra destacar, reestruturar a frase pra começar por ele. No design da casa, ênfase é só cor, mesmo peso (memória `feedback_nunca_italico_nem_peso_menor`), no máximo uma por página.

Guarda: nome de termo na primeira aparição, uma vez, pode receber destaque. O tell é o negrito em toda ocorrência.

Gravidade: alta.

### 4.2 Lista com rótulo em negrito e dois-pontos

Origem: blader §19 (labeled list); Wikipedia "Inline-header vertical lists"; jooray §17; conor "Inline-header lists" e "List-label periods".

Como aparece:
> - Posicionamento: defina quem você atende.
> - Consulta paga: cobre pela avaliação.
> - Recorrência: marque o retorno antes de ela sair.

Cada item com etiqueta, dois-pontos e uma frase que repete a etiqueta.

Conserto: prosa quando a etiqueta não carrega informação própria. "Primeiro você define quem atende. Depois cobra pela avaliação. E antes de a paciente sair da sala, o retorno já está marcado."

Guarda: banco de perguntas, script de consulta e checklist são listas de verdade e ficam em lista. O tell é a lista onde caberia parágrafo.

Gravidade: alta.

### 4.3 Tudo em lista

Origem: escrita-humana-reconecta tell 4; luquiluke §5 ("bullets only where the chapter template calls for them"); conor "Excessive bullet lists" e "Bullet lists of bare noun phrases"; Wikipedia "Rule of three" (listas enlatadas).

Como aparece: capítulo com cinco listas de bullets, cada uma com itens de quatro palavras sem verbo ("Agenda previsível", "Paciente qualificada", "Ticket consistente", "Menos objeções"). Lista de "benefícios". Lista de "pontos-chave" no fim.

Conserto: texto de gente anda em parágrafo. Uma lista de benefícios vira um parágrafo que argumenta os benefícios. Item de lista, quando fica, é afirmação checável ("Em março ela fechou 9 planos de tratamento em 14 consultas").

Guarda: a estrutura do ebook pode ter seções de referência (perguntas da consulta, o script de WhatsApp, a cola do Framework 715). Aí lista é a forma certa. Regra prática: 8 ou mais bullets em 200 palavras é sinal; 3 ou mais subtítulos em 300 palavras também (conor "Excessive structure").

Gravidade: alta (em prosa argumentativa), nenhuma (em seção de referência).

### 4.4 Título Com Todas As Iniciais Maiúsculas

Origem: blader §20; Wikipedia "Title case"; jooray §18 e §53 (em línguas sem title case nativo, a regra é absoluta).

Como aparece:
> ## Como Estruturar Uma Consulta Que Vende
> ## Os Três Pilares Do Posicionamento De Elite

Português não tem title case. Norma editorial brasileira é caixa baixa com só a primeira letra e os nomes próprios em maiúscula. Iniciais maiúsculas em cada palavra é hábito inglês que sobreviveu à tradução.

Conserto: "Como estruturar uma consulta que vende".

Guarda: nome de produto ou pilar registrado ("Agenda do Milhão", "Fábrica de Contatos", "Presente Inaceitável") mantém as maiúsculas próprias. Título de capa de carrossel segue o design system, não este catálogo.

Gravidade: alta.

### 4.5 Emoji e seta como marcador

Origem: blader §20; Wikipedia "Emoji as formatting"; jooray §19; dna.md seção 8 (proibido nos slides).

Como aparece: emoji abrindo subtítulo ou bullet; a seta como marcador de item; o check verde antes de cada passo; o foguete no CTA. (Este arquivo não reproduz os caracteres de propósito.)

Conserto: remover. Sem exceção no ebook.

Guarda: nenhuma no miolo. Em legenda de post a casa tem regras próprias.

Gravidade: alta.

### 4.6 Cabeçalho genérico e cabeçalho repetido na primeira frase

Origem: blader §24; jooray §30; conor "Excessive structure" ("Overview", "Key Points", "Conclusion"); Wikipedia "'Awards and recognition' section" e "Headings only containing other headings"; luquiluke §5 (no recap endings).

Como aparece:
> ## Introdução
> ## Considerações finais
> ## Pontos-chave
> ## Desafios e oportunidades
> ## Precificação
> Precificar é essencial.
> Quando a paciente pergunta o preço...

Cabeçalho que não diz nada específico, e cabeçalho seguido de uma linha que só o repete antes do conteúdo real.

Conserto: cabeçalho que conta algo ("Por que 300 reais e não 150"). Apagar a frase-eco. Fim de capítulo sem "Considerações finais": termina no último fato ou na instrução.

Guarda: o mapa de capítulos aprovado (Fase 2) pode fixar um esqueleto repetido, com seções de mesmo nome em capítulos de mesma função. Aí o nome repetido é design, não default.

Gravidade: alta ("Introdução", "Conclusão", "Considerações finais"), média (frase-eco).

### 4.7 Linha horizontal entre seções e seção só de subseções

Origem: Wikipedia "Thematic breaks between sections", "Headings only containing other headings", "Skipping heading levels"; blader §20.

Como aparece: "---" depois de cada seção; um H2 sem texto que só abriga três H3; capítulo que pula do H1 pro H3.

Conserto: tirar as linhas; dar um parágrafo ao H2 ou promover os H3. Este arquivo usa linhas horizontais entre famílias porque é referência de consulta, não prosa.

Guarda: separador entre capítulos no template de PDF é design.

Gravidade: média.

### 4.8 Tabela pequena onde cabe frase

Origem: Wikipedia "Unusual use of tables"; gregorymm 5d ("if fewer than 4 rows, write it as a sentence").

Como aparece: tabela de duas linhas comparando "avaliação grátis" e "consulta paga"; tabela com "Métrica | Valor" pra dois números.

Conserto: frase. "Avaliação grátis fechava 1 em 12. Consulta paga fecha 1 em 3."

Guarda: tabela de referência (a régua de Super Validado / Validado / Reprovado por custo de seguidor, o banco de termos) é legítima e útil. Quatro linhas ou mais com colunas que a leitora vai consultar: tabela.

Gravidade: baixa.

### 4.9 Aspas: o que é e o que não é tell em PT-BR

Origem: blader §21; Wikipedia "Curly quotation marks and apostrophes"; jooray §20 e §45 (aspas nativas não são artefato); conor "Formatting".

Em português publicado, aspas curvas (“ ”) são a norma tipográfica; Word, Docs e macOS curvam sozinhos. Aspas curvas não são tell em PT-BR.

O que é tell (baixo): mistura de aspas curvas e retas no mesmo texto, sinal de que o texto passou por colagem de chat e correção parcial; aspas simples como aspas principais ('assim'), que é convenção inglesa; a aspa de fechamento inglesa depois de uma abertura de outro sistema.

Conserto: uniformizar pro padrão do template de PDF.

Gravidade: baixa.

### 4.10 Lista de substantivos nus

Origem: conor "Bullet lists of bare noun phrases".

Como aparece:
> - Agenda previsível
> - Paciente qualificada
> - Ticket consistente
> - Menos objeções
> - Mais recorrência

Cinco ou mais itens, cada um adjetivo mais substantivo, sem verbo, mesmo tamanho, nenhum checável. É a forma que o modelo assume quando pedem "benefícios".

Conserto: prosa, ou itens que afirmam algo verificável. "Depois do método, a segunda-feira dela abre com 4 retornos já marcados e 3 consultas pagas novas."

Guarda: lista de itens de verdade (materiais, etapas nomeadas de um protocolo) pode ser de substantivos. O tell é a simetria: se todos têm a mesma forma e o mesmo comprimento, é fôrma.

Gravidade: alta.

### 4.11 Recapitulação no fim da seção

Origem: luquiluke §5 ("no recap endings"); Wikipedia "Section summaries" (histórico, "In summary", "In conclusion"); jooray §41; conor "Acknowledgment loops".

Como aparece:
> Em resumo, neste capítulo vimos que a consulta paga...
> Como vimos, o posicionamento é a base de tudo.
> Recapitulando: três passos.

A leitora acabou de ler a seção.

Conserto: cortar. A seção termina no ponto ou faz ponte pra próxima ideia.

Guarda: um livro de método pode ter, no fim, uma página única de "a cola" com os passos em lista, se o mapa de capítulos previu. Isso é referência, não recap.

Gravidade: alta.

---

## Família 5: Sobras de chatbot e hedging

Resto de conversa, andaime de raciocínio e qualificador empilhado. Quase tudo aqui se remove sem reescrever.

### 5.1 Resíduo de conversa

Origem: blader §22; Wikipedia "Collaborative communication"; jooray §21 e §23; conor "Chatbot artifacts", "Sycophantic tone", "Acknowledgment loops", "Recap-flattery opener"; gregorymm 7.

Como aparece:
> Espero que este material te ajude!
> Claro! Aqui está um capítulo sobre precificação.
> Ótima pergunta.
> Segue abaixo o passo a passo.
> Se quiser, posso detalhar cada etapa.
> Você está absolutamente certa em pensar assim.

Cumprimento, elogio, oferta ou despedida de chatbot que ficou no texto que deveria ficar em pé sozinho. É o tell mais certo da lista e o mais fácil de deixar passar quando embrulha conteúdo real.

Conserto: tirar o embrulho, manter o conteúdo.

Guarda: nenhuma. Saudação de carta ("Doutora,") é outra coisa e é anterior aos chatbots.

Gravidade: alta.

### 5.2 Narração do próprio texto

Origem: luquiluke §4 e §5 ("the book doesn't narrate itself", "as mentioned earlier"); luquiluke es.md ("Como mencionamos anteriormente", "Como hemos visto"); Wikipedia "Collaborative communication" (o exemplo "In this section, we will discuss").

Como aparece:
> Neste capítulo, vamos explorar os três pilares da consulta.
> Como mencionamos anteriormente, a bio não é currículo.
> Ao longo deste ebook, você vai descobrir...
> A seguir, apresentaremos o método.
> Mais adiante veremos como aplicar.

O livro anuncia o que vai fazer, ou aponta pro que já fez, em vez de fazer.

Conserto: fazer. "A consulta tem três partes. A primeira é a pergunta que abre a dor: o que te faz achar isso importante agora, e não antes?"

Guarda: uma ponte curta pra outro capítulo, com número ("o script está no capítulo 6"), é serviço à leitora. O tell é a narração de sumário.

Gravidade: alta.

### 5.3 Certificado de importância

Origem: Wikipedia "Didactic disclaimers" (histórico: "it's important to note", "worth noting"); jooray §24 e §36 ("the worth-saying certificate"); luquiluke es.md ("Cabe destacar", "Es importante mencionar", "Vale la pena mencionar"); conor "Hollow intensifiers" e "Vague endorsement (worth [verb]ing)".

Como aparece:
> Vale ressaltar que a consulta paga não é para todo perfil.
> É importante destacar que cada caso é único.
> Cabe mencionar que o valor pode variar.
> Não podemos deixar de lembrar que...
> É fundamental entender que...
> Vale a pena notar que...
> Vale lembrar: ...

A escritora decide que uma afirmação merece ser feita e então a faz. Escrever já tinha decidido isso. "Vale ressaltar" é provavelmente o tell lexical mais frequente do PT-BR de IA; "vale a pena mencionar" é decalque de "worth mentioning".

Conserto: cortar o certificado, manter a afirmação. "A consulta paga não é para todo perfil. Se o seu Instagram ainda é um cardápio de serviços, cobrar a avaliação vai esvaziar a agenda."

Guarda: aviso com conteúdo real (limite de escopo, ressalva de segurança clínica, correção) fica. O tell é a oração cujo único conteúdo é avisar que uma afirmação vem aí.

Gravidade: alta.

### 5.4 Hedge empilhado e muro

Origem: blader §9; jooray §25; luquiluke §3 (hedge words) e es.md §3; conor "Hedge-stacked predictions", "Parenthetical hedging"; escrita-humana-reconecta tell 5 ("ficar em cima do muro").

Como aparece:
> Isso pode, em alguns casos, potencialmente aumentar a taxa de fechamento.
> De certa forma, o preço talvez influencie um pouco a percepção.
> Depende. Cada caso é um caso. Desde que bem aplicado, o método tende a funcionar.
> Possivelmente, em determinadas situações, seria interessante considerar...

Cada qualificador cancela o seguinte até a frase não afirmar nada. "Depende", "cada caso é um caso", "desde que bem aplicado" é a versão de quem não se comprometeu.

Conserto: tomar posição. Se a posição tem ressalva real, dizer a ressalva com nome. "Cobrar consulta funciona. Não funciona pra quem ainda tem bio de cardápio: aí a paciente não sabe pelo que está pagando."

Guarda: "talvez" e "costuma" isolados são hábito humano. Ressalva clínica ou legal fica. O tell é a pilha ("pode potencialmente em alguns casos") e o muro sem nome.

Gravidade: alta (pilha ou muro), baixa (um "talvez").

### 5.5 Enumeração hedgeada como abertura

Origem: jooray §43 ("Hedged-enumeration openers": "There are several factors to consider", um dos separadores mais claros do corpus HC3).

Como aparece:
> Existem diversos fatores a considerar na hora de definir o valor da consulta.
> Há várias maneiras de estruturar a agenda.
> De modo geral, depende de uma série de variáveis.

Anuncia que considerações existem em vez de dar a resposta.

Conserto: resposta primeiro. "O valor da consulta é 10% do plano médio que você fecha. Plano de 3 mil, consulta de 300."

Guarda: se uma lista de fato segue, a lista é a resposta e abre a seção.

Gravidade: alta.

### 5.6 Conclusão genérica e otimista

Origem: blader §13 (send-off); jooray §26; Wikipedia "Outline-like conclusions about challenges and future prospects"; conor "Generic conclusions", "Generic future-narrative closers", "Social endorsement closers".

Como aparece:
> O futuro da sua clínica está nas suas mãos.
> O céu é o limite.
> Agora é com você. Boa sorte nessa jornada!
> Apesar dos desafios, o mercado segue cheio de oportunidades para quem se posiciona.
> Salve este capítulo e volte nele sempre que precisar.

Fecho que serviria pra qualquer livro sobre qualquer coisa.

Conserto: terminar no último fato concreto ou na instrução, que é o fecho típico da casa: "Faz essas alterações e me conta como foi." (dna.md, seção 2).

Guarda: CTA com urgência sutil e ação específica é fim legítimo. O tell é o fecho genérico.

Gravidade: alta.

### 5.7 Disclaimer de conhecimento e lacuna preenchida

Origem: blader §23; Wikipedia "Knowledge-cutoff disclaimers and speculation about gaps in sources"; jooray §22; conor "Cutoff disclaimers" e "Speculative gap-filling"; memória `feedback_nunca_inventar_dados`.

Como aparece:
> Embora não existam dados oficiais sobre o mercado de harmonização facial no interior, estima-se que...
> Não há informações detalhadas sobre o caso, mas provavelmente ela começou cobrando pouco.
> Com base nas informações disponíveis, é possível supor que...

Admite que não achou a fonte e preenche com palpite plausível. Numa versão de ebook, o palpite vira "dado".

Conserto: dizer o que a fonte não mostra, ou cortar. Nunca apresentar palpite como fato. Regra da skill: o que não está em `fontes/` não entra.

Guarda: nenhuma.

Gravidade: alta.

### 5.8 Cadeia de raciocínio vazada

Origem: jooray §38 ("Reasoning-chain artifacts"); conor "Reasoning chain artifacts".

Como aparece:
> Primeiro, vamos analisar o problema. Depois, a solução.
> Passo 1: entender o contexto. Passo 2: definir a estratégia.
> Agora que estabelecemos isso, podemos avançar.
> Pensando bem, o ponto é o seguinte.

O modelo narra o próprio procedimento como se fosse o conteúdo.

Conserto: apagar o andaime, manter a conclusão na voz da autora.

Guarda: passos numerados de um método (Framework 715, as 4 etapas) são conteúdo, não andaime.

Gravidade: alta.

### 5.9 Bajulação e culpa zero

Origem: Wikipedia e jooray §23 ("Sycophantic tone"); conor "Sycophantic tone"; dna.md seção 1 (o tom é "desafiador-mentor", "você não está errada, você está mal-equipada").

Como aparece:
> Você já é uma profissional incrível, só precisa de um empurrãozinho.
> Parabéns por ter chegado até aqui!
> Você merece uma agenda cheia.
> Não se culpe, você está fazendo o seu melhor.

Elogio genérico à leitora que substitui o diagnóstico.

Conserto: o diagnóstico que tira a culpa da pessoa e põe no método, que é outra coisa: "Você atende bem. O problema é que o seu perfil fala procedimento, e por isso a paciente pede desconto."

Guarda: "diagnóstico que libera culpa" é emoção número 2 do arco da casa (dna.md, seção 5). Ele nomeia o erro e dá o certo em seguida. O tell é o elogio sem diagnóstico e o "parabéns" de chatbot.

Gravidade: alta ("parabéns por chegar até aqui"), média (elogio genérico).

### 5.10 Conectivo empilhado

Origem: jooray §42 ("Connective tissue pile-up"); Wikipedia "Transition words (in isolation)" (só o empilhamento conta); conor "Transition phrases"; luquiluke es.md §2.

Como aparece:
> Além disso, a consulta paga filtra. Ademais, ela posiciona. Dessa forma, a agenda muda. Nesse sentido, o método...
> Por fim, vale lembrar que...
> Sendo assim, diante disso, nesse contexto...

"Além disso", "ademais", "outrossim", "nesse sentido", "dessa forma", "diante disso", "nesse contexto", "sendo assim", "por fim", "em suma", "vale lembrar" abrindo três frases seguidas. "Nesse sentido" e "dessa forma" são o "moreover / furthermore" traduzido; "ademais" e "outrossim" são a versão bacharelesca que ninguém fala.

Conserto: contar. Mais de um conectivo de abertura por parágrafo, ou o mesmo duas vezes na seção, quer dizer que a ordem das frases deveria estar carregando a lógica. Apagar o conectivo, ou começar parágrafo novo. "A consulta paga filtra quem ia pedir desconto e, de quebra, posiciona. A agenda muda em um mês."

Guarda: um "além disso" por seção é normal. "Só que", "e aí", "mas" são conectores de fala e sinal humano.

Gravidade: alta (três seguidos ou "outrossim"), baixa (um).

### 5.11 Placeholder e resíduo forense

Origem: jooray §40 ("Forensic residue"); Wikipedia "Phrasal templates and placeholder text", "utm_source"; conor "Unfilled placeholders", "Chatbot citation markup leaks", "AI-tool URL parameters".

Como aparece: "[Nome da doutora]", "[inserir caso]", "Dra. Fulana", "XX%", "2026-XX-XX", "utm_source=chatgpt.com" num link, "citeturn0search0", caractere invisível (U+200B), homoglifo cirílico no meio de palavra.

Conserto: preencher com conteúdo da fonte ou apagar a frase. Regra da skill (Fase 0): placeholder da fonte ("Dra. Mariana") vira "a doutora" ou o nome real da transcrição. Normalizar pra texto NFC limpo antes de compilar.

Guarda: nenhuma. Isso é prova, não indício.

Gravidade: alta.

### 5.12 Concessão falsa

Origem: conor "False concession structure" ("While X is impressive, Y remains a challenge"); jooray §37.

Como aparece:
> Embora a técnica seja importante, o posicionamento continua sendo um desafio.
> Apesar de o mercado ter evoluído, a precificação ainda é um ponto de atenção.

As duas metades são vagas. Soa equilibrado sem pesar nada.

Conserto: concessão específica ou lado escolhido. "A técnica você tem. O que falta é a frase que abre a conversa de preço, e ela está na página seguinte."

Guarda: concessão com conteúdo real dos dois lados fica.

Gravidade: média.

---

## Família 6: Calques do inglês

A família que nenhuma skill pública cobre pra português. Cada palavra aqui é português legítimo; só o uso é estrangeiro. Por isso sobrevive a qualquer filtro de vocabulário. O Editor e o detector procuram estas formas de propósito.

### 6.1 "Ser sobre" ("não é sobre X, é sobre Y")

Origem: calque de "to be about"; escrita-humana-reconecta tell 1 (o exemplo "Não é sobre vender, é sobre conectar"); luquiluke es.md §4 ("es acerca de" vira "se trata de").

Como aparece:
> Não é sobre técnica. É sobre posicionamento.
> Harmonização facial não é sobre volume, é sobre proporção.
> Isso é sobre a paciente se sentir vista.

"Sobre" em português introduz assunto ("um post sobre botox"). "X é sobre Y" no sentido de "X consiste em Y" é inglês.

Conserto: "não se trata de", "a questão não é", ou afirmar direto. "Técnica não enche agenda. Posicionamento enche." "O que a paciente compra é se sentir vista."

Guarda: "sobre" como assunto é português normal. Uma antítese por capítulo fica pelas regras da voz, mas a forma preferida é "não é X. É Y." sem o "sobre".

Gravidade: alta.

### 6.2 "No final do dia" e "em última instância"

Origem: calque de "at the end of the day" e "ultimately"; luquiluke es.md §4 ("al final del día" vira "a fin de cuentas"); conor "Transition phrases".

Como aparece:
> No final do dia, o que importa é a paciente voltar.
> Ao final do dia, é tudo posicionamento.
> Em última análise, a agenda reflete o perfil.

Conserto: "no fim das contas", ou cortar a locução, que quase sempre está antecedendo um fecho de uma linha (1.2). "A paciente volta quando o retorno já saiu marcado."

Guarda: "no fim do dia" literal, quando a frase é sobre o expediente ("ela fechava o caixa no fim do dia"), é português.

Gravidade: alta.

### 6.3 "Em um mundo onde", "em um cenário", "na era digital", "nos dias de hoje"

Origem: calque de "in a world where", "in today's landscape", "in the digital age"; luquiluke es.md §2 ("En la era digital", "En el vertiginoso mundo actual", "Hoy en día como apertura de relleno"); conor "Formulaic openings" e "In today's [X]".

Como aparece:
> Em um mundo onde todo mundo posta antes e depois, o que te diferencia?
> No cenário atual da estética, posicionamento é indispensável.
> Na era digital, o paciente pesquisa antes de agendar.
> Nos dias de hoje, com o mercado cada vez mais competitivo...

Contexto amplo antes do ponto. O primeiro parágrafo do capítulo é o lugar preferido.

Conserto: cortar e começar pelo fato ou pela cena. "Abre o Instagram. Cinco perfis de harmonização facial na sua cidade. Quatro deles postaram um antes e depois hoje."

Guarda: nenhuma pra abertura de capítulo. No meio do texto, "hoje" com data ou dado específico ("em 2025 a Anvisa...") é contexto real.

Gravidade: alta.

### 6.4 "Enquanto" concessivo

Origem: calque de "while X, Y"; observação própria do PT-BR (em português, "enquanto" é temporal: "enquanto ela atende, o telefone toca").

Como aparece:
> Enquanto a técnica é importante, o posicionamento é decisivo.
> Enquanto algumas profissionais preferem promoção, outras investem em autoridade.
> Enquanto o preço atrai, é a confiança que fecha.

Conserto: duas frases, ou "embora" só quando a concessão importa. "A técnica importa. O que decide é o posicionamento." "Preço atrai quem pergunta preço. Confiança fecha."

Guarda: "enquanto" temporal ("enquanto você atende, a Fábrica de Contatos agenda") e "enquanto" de contraste simultâneo de fato ("enquanto ela cobrava 150, a colega cobrava 400") são português.

Gravidade: alta.

### 6.5 Falsos amigos de sentido: "eventualmente", "assumir", "realizar"

Origem: calque de "eventually", "assume", "realize"; luquiluke es.md §4 ("eventualmente por finalmente", "asumir por suponer", "actualmente por en realidad").

Como aparece:
> Eventualmente a paciente vai perceber o valor.
> Podemos assumir que ela já pesquisou o preço.
> Ela realizou que estava cobrando pouco.
> Atualmente, o que ela vende é confiança.

Em português, "eventualmente" é "de vez em quando"; "assumir" é "tomar pra si"; "realizar" é "executar"; "atualmente" é "hoje em dia". Os sentidos "no fim", "supor", "perceber", "na verdade" são inglês.

Conserto: "uma hora a paciente percebe", "pode supor que", "ela se deu conta de que", "na verdade".

Guarda: "assumir a clínica", "realizar o procedimento", "eventualmente aparece uma paciente assim" são os sentidos nativos e ficam.

Gravidade: alta ("realizou que", "eventualmente" no sentido de "no fim"), média ("assumir que").

### 6.6 Verbos de negócio emprestados: "endereçar", "suportar", "performar", "entregar", "impactar"

Origem: calque de "address", "support", "perform", "deliver", "impact"; luquiluke es.md §4 ("soportar por apoyar"); banco-de-termos (jargão de gestor de tráfego que o avatar desconfia).

Como aparece:
> Precisamos endereçar a objeção de preço.
> O método suporta profissionais de qualquer cidade.
> O perfil não está performando.
> O Supercaso entrega identificação.
> Isso impacta diretamente o faturamento.

Conserto: "resolver / responder a objeção", "funciona pra / serve pra", "o perfil não está rendendo / não está trazendo consulta", "o Supercaso faz a paciente se reconhecer", "isso mexe no faturamento / muda o faturamento".

Guarda: "entregar" com objeto concreto ("entregar o plano impresso") e "suportar" no sentido de aguentar ("não suporta mais dar desconto") são nativos. "Impactar" é nível 1 do vocabulário: quase sempre cai.

Gravidade: alta ("endereçar", "performar"), média ("entregar", "impactar", "suportar" figurado).

### 6.7 Locuções decalcadas: "tomar ação", "decisão informada", "ter em mente", "tirar vantagem de", "fazer parte do processo"

Origem: calque de "take action", "informed decision", "keep in mind", "take advantage of", "part of the process"; luquiluke es.md §4 ("tomar acción" vira "actuar").

Como aparece:
> Chegou a hora de tomar ação.
> Ajude a paciente a tomar uma decisão informada.
> Tenha em mente que o valor comunica.
> Tire vantagem da recorrência.
> Ouvir não faz parte do processo.

Conserto: "agir / fazer", "a paciente decidir sabendo o que está comprando", "lembra que o valor comunica", "aproveitar a recorrência", "ouvir não é do jogo".

Guarda: "ter em mente" já está bastante aclimatado no português escrito; conta só em cluster. "Tomar ação" e "decisão informada" caem sempre.

Gravidade: alta ("tomar ação"), média (as demais).

### 6.8 "Eis o porquê", "aqui está a coisa", "a questão é a seguinte"

Origem: calque de "here's why", "here's the thing", "the thing is"; blader §4; conor "Infomercial engagement hooks".

Como aparece:
> Ela não fecha. Eis o porquê.
> Aqui está a coisa: ninguém te ensinou a cobrar.
> A questão é a seguinte.
> E aqui vai a parte importante.
> Isso é o porquê de a paciente sumir.

"Isso é o porquê" (this is why) é a forma mais denunciadora: em português se diz "por isso".

Conserto: apagar o gancho; "por isso". "Ela não fecha porque a conversa de preço começa na hora errada." "Por isso a paciente some."

Guarda: "a questão é que" no meio de fala, colado à explicação, é oral. O tell é o gancho em frase própria.

Gravidade: alta.

### 6.9 "Mergulhar", "mergulho profundo", "desvendar", "desmistificar", "explorar"

Origem: calque de "dive in", "deep dive", "unpack", "demystify", "explore"; luquiluke es.md §1 ("sumergirse", "desentrañar"); conor Tier 1A.

Como aparece:
> Vamos mergulhar fundo na precificação.
> Um mergulho profundo no funcionamento da consulta.
> Neste capítulo, vamos desvendar os segredos da recorrência.
> Vamos desmistificar a consulta paga.
> Vamos explorar as possibilidades.

Conserto: cortar o verbo de anúncio (1.5) e começar. "A consulta paga funciona assim."

Guarda: "explorar" em sentido próprio ("explorar a região") e "mergulhar" literal são normais. Como abertura de seção, caem.

Gravidade: alta.

### 6.10 "Jornada", "navegar", "pavimentar o caminho", "ao longo do caminho", "trajetória"

Origem: calque de "journey", "navigate", "pave the way", "along the way"; luquiluke es.md §1 ("un viaje metafórico", "navegar metafórico", "embarcarse en"); conor Tier 1A e Tier 2.

Como aparece:
> Sua jornada rumo à agenda fechada começa aqui.
> Como navegar as objeções da paciente.
> Isso pavimentou o caminho para a recorrência.
> Ao longo do caminho, você vai encontrar resistência.
> A jornada da paciente começa no Instagram.

Conserto: nomear o processo ou cortar. "A agenda fecha em quatro etapas." "Como responder à objeção de preço." "Depois disso a recorrência ficou fácil." "A paciente chega pelo Instagram, manda mensagem, e a conversa que vem aí é o Framework 715."

Guarda: "trajetória" pra carreira de uma pessoa, uma vez, é português. "Jornada de trabalho" é outro sentido. O tell é "jornada" como metáfora de processo, e "navegar" transitivo.

Gravidade: alta.

### 6.11 "Desbloquear", "empoderar", "elevar", "alavancar", "potencializar", "escalar"

Origem: calque de "unlock", "empower", "elevate", "leverage", "scale"; luquiluke es.md §1 ("apalancar", "potenciar", "empoderar"); gregorymm 1 (swap table); banco-de-termos ("escalar o negócio" vira "crescer sem trabalhar mais").

Como aparece:
> Desbloqueie o potencial da sua clínica.
> Empodere-se como especialista.
> Eleve o nível da sua consulta.
> Alavanque sua autoridade com o Supercaso.
> Potencialize seus resultados.
> Escale sua clínica sem contratar.

Conserto: "destrave a agenda" (só se o fingerprint da autora usa), "assuma o lugar de especialista", "melhore a consulta", "use o Supercaso pra virar referência", "aumente o faturamento", "cresça sem trabalhar mais".

Guarda: "escalar" em sentido próprio (escalar a equipe do dia) fica. "Destravar" é mais nativo que "desbloquear" e é nível 3, mas "destrave seu potencial" cai igual.

Gravidade: alta.

### 6.12 Estrangeirismo cru onde há palavra da casa, e sobretradução do jargão do campo

Origem: jooray §54 ("Loanwords: neither over-translated nor under-translated", "match the field, not the dictionary"); banco-de-termos camada B; dna.md seção 3 (proibições); memória `feedback_termo_harmonizacao_facial`.

Subtradução (inglês cru onde a casa tem palavra):
> Os insights dessa call mudaram meu mindset.
> Precisamos de mais leads no topo do funil.
> A paciente high ticket não pede desconto.
> O engagement caiu depois que o algoritmo mudou.

Conserto: "o que ela entendeu nessa conversa mudou o que ela acredita", "mais paciente com perfil chegando no sistema de captação", "a paciente que investe não pede desconto", "menos gente respondendo depois que o Instagram mudou a entrega".

Sobretradução (formal demais onde o campo fala de outro jeito):
> A aplicação de toxina botulínica tipo A na região frontal.
> A harmonização orofacial (HOF) é o conjunto de procedimentos...
> A cliente que busca rejuvenescimento.

Conserto: o campo diz "botox" como nome comum e a casa diz "harmonização facial", nunca "HOF" nem "orofacial". A casa diz "paciente", nunca "cliente". E o jargão técnico só aparece pra ser descartado: "Ninguém quer bioestimulador. As pessoas querem o fim do rosto derretido." (dna.md, seção 3).

Guarda: termo que a leitora usa e que não tem tradução em uso ("stories", "Reels", "Direct", "print", "skincare", "antes e depois") fica. "Follow-up" a casa já usou em título; fica quando é a palavra da leitora, e "follow-up agressivo" nunca. "Call" e "closer" são vocabulário interno de CRM, não de ebook.

Gravidade: alta (termos vetados pela marca), média (estrangeirismo genérico).

### 6.13 "Consistente" por "constante" e "efetivo" por "eficaz"

Origem: calque de "consistent" e "effective"; observação própria do PT-BR.

Como aparece:
> Poste de forma consistente.
> Consistência é o segredo da agenda cheia.
> Uma abordagem efetiva para converter.
> Isso é mais efetivo do que promoção.

Em português, "consistente" é coerente ou sólido ("argumento consistente", "massa consistente"); "efetivo" é real, concreto ("cargo efetivo", "controle efetivo"). Os sentidos "regular" e "que funciona" são inglês.

Conserto: "toda semana, sem falhar", "constância", "um jeito que funciona", "funciona mais do que promoção".

Guarda: "resultado efetivo" no sentido de "concreto" e "argumento consistente" são os usos nativos.

Gravidade: média.

### 6.14 "Comprometida com", "apaixonada por", "focada em entregar"

Origem: calque de "committed to", "passionate about", "focused on delivering"; blader §16 ("commitment to"); gregorymm 2c.

Como aparece:
> Uma profissional comprometida com a excelência.
> Apaixonada por transformar sorrisos.
> Focada em entregar resultados naturais.
> Dedicada a proporcionar a melhor experiência.

Vitrine de bio de LinkedIn. Diz atitude no lugar de fato.

Conserto: o que ela faz. "Atende 12 pacientes por semana, todas por consulta paga, e o retorno sai marcado antes de a paciente levantar da cadeira."

Guarda: nenhuma na prosa. Em bio de Instagram a casa tem fórmula própria (ver reconecta-copywriting).

Gravidade: alta.

### 6.15 Cortesia de e-mail traduzida

Origem: calque de "feel free to", "don't hesitate to", "I hope this finds you well", "excited to share", "happy to help"; gregorymm 7 ("AI pleasantries").

Como aparece:
> Sinta-se à vontade para adaptar o script.
> Não hesite em cobrar o que você vale.
> Espero que este material te encontre bem.
> Estou muito animada para compartilhar este método com você.
> Fico feliz em ajudar.

Conserto: "adapta o script como quiser", "cobra o que você vale", cortar, cortar, cortar.

Guarda: nenhuma. "Não hesite" nunca foi português falado.

Gravidade: alta.

### 6.16 "Testemunho de", "ressoar com", "alinhado com", "conectar com"

Origem: calque de "testament to", "resonate with", "align with", "connect with"; Wikipedia AI vocabulary ("testament", "align with"); conor Tier 2 ("resonate").

Como aparece:
> Um verdadeiro testemunho da dedicação dela.
> Uma mensagem que ressoa com a paciente.
> Um perfil alinhado com o posicionamento.
> Conectar com o público de forma autêntica.

Conserto: "mostra o quanto ela se dedicou", "uma mensagem que bate com o que a paciente sente", "um perfil que combina com o que você cobra", "falar com a paciente de um jeito que ela se reconheça".

Guarda: "alinhado" em sentido próprio (procedimento alinhado com a indicação clínica) fica. "Testamento de" em vez de "testemunho de" é a versão mais grosseira e é prova de tradução literal.

Gravidade: alta ("testamento de", "ressoar com"), média ("alinhado com", "conectar com").

### 6.17 "Dito isso", "isso dito", "tendo dito isso"

Origem: calque de "that said", "having said that"; conor "Transition phrases" ("That said / That being said").

Como aparece:
> Dito isso, nem toda paciente vai aceitar.
> Isso dito, o método funciona.
> Tendo dito isso, vamos ao próximo ponto.

"Dito isso" já circula no português escrito e conta só em cluster. "Isso dito" e "tendo dito isso" são tradução literal.

Conserto: "mas", "só que", "agora,". "Só que nem toda paciente vai aceitar."

Guarda: um "dito isso" por capítulo passa.

Gravidade: alta ("isso dito", "tendo dito isso"), baixa ("dito isso").

### 6.18 Números, datas e maiúsculas de inglês

Origem: jooray §53 ("Typography and number conventions"); luquiluke es.md checklist ("coma decimal, mil millones, jamás billones"); observação própria do PT-BR.

Como aparece:
> 1,000 pacientes; R$ 2,500.00; 5.5 mil
> Setembro 7, 2026; 7 de Setembro
> 10 % de desconto
> A Dentista, a Biomédica, o Instagram, a Harmonização Facial
> 'consulta paga' (aspas simples como principal)

Regras brasileiras: ponto de milhar e vírgula decimal (1.000; R$ 2.500,00; 5,5 mil); dia de mês de ano, mês em minúscula (7 de setembro de 2026); porcentagem colada (10%); nomes de profissão e substantivos comuns em minúscula; aspas duplas como principais.

Conserto: aplicar as regras acima em toda ocorrência antes de compilar.

Guarda: "R$15k" e "200k" são a forma que a casa escreve valor em copy (dna.md usa "protocolo de R$15k"); ficam quando o fingerprint da autora usa. Nome de pilar da casa mantém maiúsculas.

Gravidade: média (é tipografia, mas em cluster denuncia pipeline de tradução).

---

## Família 7: Tradução de registro

Não é vocabulário nem retórica: é a gramática do inglês vazando na do português. Sujeito em toda frase, possessivo em tudo, passiva, nominalização, advérbio na posição inglesa, formalidade de manual.

### 7.1 Gerúndio de abertura sem sujeito

Origem: luquiluke §1 ("subjectless participle openers: 'Building on this idea,'"); jooray §48.

Como aparece:
> Tendo isso em mente, vamos ao valor da consulta.
> Considerando o cenário atual, a consulta paga se torna indispensável.
> Olhando para a sua agenda, fica claro o problema.
> Falando em preço, existe um erro comum.
> Partindo desse princípio, o próximo passo é...

Oração em -ndo abrindo a frase, sem sujeito, fazendo papel de transição. Em inglês é "Building on this", "Looking at your schedule". Em português falado ninguém abre frase assim.

Conserto: cortar a abertura ou virar frase com sujeito. "O valor da consulta é 10% do plano." "Abre a sua agenda. O problema está ali: quatro avaliações grátis na terça e nenhum retorno marcado."

Guarda: gerúndio narrativo com sujeito próprio ("Ela entrou na sala rindo") é normal.

Gravidade: alta.

### 7.2 "Você" a cada frase e possessivo em tudo

Origem: jooray §50 ("Pronoun and possessive spam": em língua pro-drop, o pronome escrito é ênfase, não gramática); observação própria do PT-BR (o português deixa cair o sujeito e o possessivo óbvio).

Como aparece:
> Você abre a sua agenda. Você olha os seus horários. Você percebe que a sua semana está vazia. Você precisa mudar a sua estratégia.
> Sua clínica, seus pacientes, sua equipe, seu faturamento.

Toda frase com "você" e todo substantivo com "seu/sua". É o inglês, que não deixa cair "you" e "your", falando devagar com estrangeiro.

Conserto: deixar cair o que é óbvio. "Abre a agenda. Olha os horários. A semana está vazia, e o que precisa mudar não é o preço."

Guarda: "você" como pronome dominante é regra da voz (dna.md, seção 3), e "doutora" como vocativo também. O tell é a repetição mecânica em frases seguidas e o possessivo redundante ("sua clínica" quando não há outra clínica na frase).

Gravidade: alta (é um dos calques mais denunciadores porque português espontâneo não faz isso).

### 7.3 Passiva e "está sendo"

Origem: blader §11; jooray §14; conor "Subjectless fragments and agentless passives"; jooray "What NOT to flag" (a passiva reflexiva é registro nativo em texto administrativo).

Como aparece:
> Foi identificado que a maioria das profissionais não cobra a consulta.
> É recomendado que o retorno seja agendado antes da saída da paciente.
> A consulta está sendo cobrada por poucas clínicas.
> Os resultados são alcançados quando o método é seguido.

Quem faz some. "Está sendo" é a passiva progressiva do inglês e não existe no português falado.

Conserto: ativa, com dono. "A maioria das doutoras não cobra a consulta." "Marca o retorno antes de ela sair." "Pouca clínica cobra consulta."

Guarda: "recomenda-se" em protocolo clínico, bula ou nota técnica é o registro certo daquele texto. Em ebook de voz direta, fica frio e cai. Passiva quando o agente é irrelevante ("a lei foi aprovada em 2024") é português.

Gravidade: alta ("está sendo", "foi identificado que"), média (passiva comum).

### 7.4 Nominalização

Origem: observação própria do PT-BR a partir de blader §18 (verbos simples), conor "Copula avoidance" e luquiluke §7 (compressão). O inglês corporativo nominaliza e a tradução carrega.

Como aparece:
> A implementação de um sistema de captação permite a obtenção de previsibilidade.
> A realização da consulta paga resulta na qualificação da paciente.
> A construção de autoridade passa pela apresentação de casos.
> O estabelecimento de um processo de retorno garante a recorrência.

Verbo virou substantivo, e a frase ficou sem gente. "Implementação", "realização", "obtenção", "construção", "estabelecimento", "apresentação", "qualificação", "consolidação" são a marca.

Conserto: verbo com sujeito. "Quando você monta a Fábrica de Contatos, a agenda fica previsível." "Cobra a consulta e a paciente que senta é a que já decidiu." "Autoridade vem de mostrar caso."

Guarda: substantivo abstrato que nomeia coisa nomeável ("a consulta", "o plano de tratamento") é normal. O tell é a cadeia "a X de Y de Z" com dois ou mais substantivos em -ção na mesma frase.

Gravidade: alta (duas ou mais nominalizações em -ção na frase), média (uma).

### 7.5 Formal demais: "lhe", ênclise de manual, mesóclise, "prezada"

Origem: jooray §52 ("Register drift between ty and vy"); luquiluke es.md §5 e §6 (variante e tratamento como lei; "vos tienes" é erro); dna.md seção 3 ("você" direto; nunca linguagem corporativa fria).

Como aparece:
> Isso vai lhe ajudar a cobrar melhor.
> Faça-o hoje mesmo.
> Inscreva-se e receba o material.
> Prezada doutora, apresentar-lhe-ei o método.
> Trata-se, portanto, de uma mudança de mentalidade.

"Lhe" e a ênclise de imperativo ("faça-o", "diga-lhe", "contate-nos") são registro de manual e de tradução; o brasileiro fala "te" e "faz isso". Mesóclise é tell de gravidade máxima: ninguém escreve assim fora de concurso.

Conserto: "isso vai te ajudar a cobrar", "faz isso hoje", "se inscreve", "doutora,", "é uma mudança no que você acredita".

Guarda: "trata-se", "torna-se", "sabe-se" são padrão escrito e passam sozinhos; contam em cluster com "portanto", "ademais" e passiva. O fingerprint decide o grau de oralidade: se a autora escreve "se inscreve" e "me conta", o Editor mantém a próclise.

Gravidade: alta (mesóclise, "lhe" em texto de "você", "faça-o"), baixa ("trata-se").

### 7.6 Advérbio na posição inglesa e "isso é o porquê"

Origem: jooray §51 ("English word order carried through translation"); observação própria do PT-BR.

Como aparece:
> Ela rapidamente percebeu que o preço estava baixo.
> Isso claramente mostra o problema.
> Eu realmente acredito que consulta paga funciona.
> Você simplesmente precisa cobrar.
> Isso é o porquê de a paciente sumir.

O advérbio entre sujeito e verbo é ordem inglesa ("she quickly realized"). Em português o advérbio vai depois do verbo ou no fim, e "realmente/simplesmente/claramente" antes do verbo são intensificadores ocos.

Conserto: "ela percebeu rápido", "isso mostra o problema", "consulta paga funciona", "cobra e pronto", "por isso a paciente some".

Guarda: "só" e "já" antes do verbo são português ("ela só cobrou 150"). O tell é o advérbio em -mente entre sujeito e verbo, e "isso é o porquê".

Gravidade: alta ("isso é o porquê"), média (advérbio em -mente entre sujeito e verbo).

### 7.7 Deriva de tratamento

Origem: jooray §52; luquiluke es.md §5 ("jamás mezclar sistemas de tratamiento").

Como aparece:
> Você precisa cobrar. Tu sabes disso. Te falta coragem, e isso lhe custa caro. Vocês, doutoras, merecem mais.

Mistura "você" com "tu", "te" com "lhe", singular com "vocês" quando fala com uma leitora. O inglês "you" não ancora nada, e o modelo escorrega.

Conserto: "você" e "te", segunda pessoa singular, do começo ao fim. "Doutora" no vocativo. "Ela" ao narrar caso de aluna (dna.md, seção 3).

Guarda: "você" com "te" é o padrão brasileiro falado e não é mistura. O tell é "tu" conjugado, "lhe" e a oscilação singular/plural.

Gravidade: alta.

### 7.8 Vender procedimento em vez de transformação (a lente errada)

Origem: dna.md seção 8 ("Vender procedimento" é proibição completa); banco-de-termos ("Lente do Profissional vs. Lente do Paciente"; Supercaso: "NUNCA citar procedimento/ml/técnica na legenda"); memória `feedback_supercaso_so_metodologia`.

Como aparece:
> 30 unidades de toxina na região frontal e 2 ml de ácido hialurônico no terço médio.
> Protocolo de bioestimulador em três sessões.
> Oferecemos harmonização facial completa com as melhores técnicas.

Não é calque de língua, é calque de lente: a IA escreve pela lente do profissional porque é o que o corpus técnico tem. A leitora do ebook precisa aprender a escrever pela lente da paciente, e o ebook tem que dar o exemplo.

Conserto: "Ela voltou a tirar foto de perfil sem esconder metade do rosto." O procedimento aparece pra ser descartado: "Ninguém quer bioestimulador. As pessoas querem o fim do rosto derretido."

Guarda: capítulo que ensina a conduzir a consulta pode citar o nome do procedimento como o que a doutora fala, contrapondo com o que a paciente ouve (a tabela das duas lentes do banco de termos). O tell é o ebook inteiro falando em ml.

Gravidade: alta.

### 7.9 Frase em português, alma em inglês (o teste da retradução)

Origem: síntese das famílias 6 e 7; jooray (introdução da seção eslovaca: "an English draft in disguise").

Teste do Editor quando um parágrafo parece limpo e ainda assim soa estranho: retraduzir mentalmente pro inglês. Se a frase em inglês sai perfeita e natural, e a em português sai dura, o parágrafo é tradução.

> Você precisa entender que o seu posicionamento é o que vai fazer a diferença no final do dia.
> (You need to understand that your positioning is what will make the difference at the end of the day.)

Conserto: escrever a frase como se contasse no áudio de WhatsApp pra uma mentorada. "O que decide é o posicionamento. Não é a técnica, doutora, é o lugar que você ocupa na cabeça da paciente."

Guarda: nenhuma. É um teste, não um tell isolado; serve pra confirmar cluster.

Gravidade: alta (quando o teste confirma três ou mais frases seguidas).

---

## Vocabulário PT-BR em 3 níveis

Regras herdadas do conor (três camadas: sempre, em cluster, em densidade) e do jooray §49 (a lista calcada: "one 'kľúčový' is nothing; three in a paragraph, next to a 'svedčí o'... is the tell"). Cada entrada cobre as formas flexionadas (verbo, substantivo, adjetivo, advérbio em -mente).

Nível 1: quase sempre IA. Trocar ao avistar. Nível 2: suspeito em densidade; dois ou mais no mesmo parágrafo pedem reescrita. Nível 3: só conta em combinação com tells estruturais ou quando o texto está saturado.

Termos proibidos pela marca (banco-de-termos, dna.md, instrução desta skill) estão marcados com [marca] e caem sempre, independentemente do nível.

### Nível 1: quase sempre IA

| Termo | Substituto que uma pessoa usaria |
|---|---|
| mergulhar / mergulho profundo (figurado) | cortar; "olhar de perto", "entrar em" |
| desbloquear (potencial, resultados) | "destravar" só se a autora usa; senão nomear o que muda |
| potencializar | aumentar, multiplicar, fazer render mais |
| alavancar | usar, aproveitar |
| empoderar / empoderamento | dar autonomia; "assumir o lugar de especialista" |
| jornada (figurado) | caminho, processo, ou nomear as etapas |
| navegar (objeções, o mercado) | lidar com, atravessar, responder |
| robusto (figurado) | sólido, forte, que aguenta |
| abrangente | completo |
| holístico | completo, do começo ao fim |
| vale ressaltar / vale destacar / cabe destacar | cortar, afirmar direto |
| é importante notar / é importante destacar | cortar |
| vale a pena mencionar / vale mencionar | cortar |
| no final do dia / ao final do dia | no fim das contas; ou cortar |
| em última análise / em última instância | no fim; ou cortar |
| em um mundo onde / em um cenário onde | cortar, começar pelo fato |
| na era digital / nos dias de hoje / no mundo atual / no cenário atual | cortar |
| nesse sentido | cortar; ou "por isso" |
| dessa forma / desta forma (como abertura) | cortar; "assim", "aí" |
| ademais / outrossim | "e", "além disso" (uma vez) |
| vamos explorar / vamos mergulhar / vamos entender / vamos por partes | cortar, começar |
| impactar / impacto (figurado) | afetar, mexer com, mudar |
| insights [marca: jargão] | sacadas, o que ela entendeu, percepções |
| transformador(a) | nomear a mudança com número |
| crucial | decisivo; ou cortar |
| fundamental (repetido) | uma vez por capítulo; senão "o que decide", "a base" |
| abordagem | jeito, método, caminho |
| estratégico / estratégia (em excesso) | plano, o que fazer; uma vez por página |
| resultados expressivos / significativos | o número |
| crescimento exponencial | o número e o prazo |
| sinergia | cortar; dizer o que junta com o quê |
| paradigma / mudança de paradigma | nomear o que mudou |
| divisor de águas | "o que mudou foi X, em tal mês" |
| marco (figurado) | o fato datado |
| legado | o que ficou, nomeado |
| referência no mercado / referência em | o caso que prova |
| de ponta / estado da arte | nomear a técnica ou cortar |
| inovador / disruptivo | descrever o que é novo |
| sem costuras / de forma fluida / seamless | sem atrito, sem tropeço; ou cortar |
| melhores práticas | o que funciona |
| acionável | prático, que dá pra fazer amanhã |
| aprendizados (substantivo) | lições, o que ficou |
| testemunho de / testamento de (figurado) | mostra, prova |
| ressoar com | bater com, tocar, fazer sentido pra |
| endereçar (problema, objeção) | resolver, responder, tratar |
| performar / performance (de perfil, de post) | render, ir bem, trazer consulta |
| tomar ação | agir, fazer |
| decisão informada | decidir sabendo o que compra |
| eis o porquê / aqui está o porquê / isso é o porquê | "por isso" |
| aqui está a coisa / a questão é a seguinte | cortar |
| spoiler: / plot twist: | cortar |
| sinta-se à vontade para | pode; "como quiser" |
| não hesite em | "me chama", "cobra" |
| espero que este material te encontre bem | cortar |
| estou animada para compartilhar | cortar |
| curiosamente / interessantemente | cortar |
| isso dito / tendo dito isso | mas, só que |
| não é sobre X, é sobre Y (forma com "sobre") | "não é X. É Y." (uma por capítulo) ou afirmar |
| enquanto (concessivo: "enquanto X é importante, Y") | duas frases; "X importa. O que decide é Y." |
| realizar (por perceber) | perceber, se dar conta |
| eventualmente (por "no fim") | uma hora, com o tempo, no fim |
| comprometida com a excelência / apaixonada por | o que ela faz, com número |
| ecossistema [marca] | comunidade, a turma, a casa, acompanhamento |
| high ticket / alto ticket [marca] | paciente que investe, protocolo de R$15k, paciente de valor |
| engajamento / engajar [marca] | resposta, comentário, gente respondendo, voltar |
| algoritmo [marca] | o Instagram, a entrega |
| solução [marca] | sistema, método, o que resolve (nomear) |
| conteúdo [marca] | post, Supercaso, o que você publica |
| funil / pipeline [marca] | sistema de captação |
| lead / lead qualificado [marca] | paciente com perfil, contato |
| mindset [marca] | o que você acredita; Repositório de Crença |
| escalar (o negócio) [marca] | crescer sem trabalhar mais |
| tráfego qualificado [marca] | paciente que chega qualificado |
| presença digital [marca] | sistema que converte seguidor em paciente |
| pacote [marca] | plano de tratamento |
| pitch de vendas [marca] | como apresentar o plano |
| HOF / harmonização orofacial [marca] | harmonização facial, sempre |
| cliente [marca] | paciente |

### Nível 2: suspeito em densidade (dois ou mais no mesmo parágrafo)

| Termo | Substituto que uma pessoa usaria |
|---|---|
| elevar (o nível, a experiência) | melhorar, subir |
| destravar | ok uma vez; senão nomear |
| fomentar | criar, estimular |
| proporcionar | dar |
| viabilizar | tornar possível, deixar dar certo |
| possibilitar / permitir (como rider) | "e aí X acontece" |
| garantir (como rider: ", garantindo X") | frase própria com o fato |
| otimizar | melhorar, ajustar |
| maximizar | tirar o máximo de, aumentar |
| agregar valor / gerar valor / entrega de valor | dizer o que entrega |
| consistente / consistência (por regular) | constante, toda semana, constância |
| efetivo (por eficaz) | que funciona, eficaz |
| assumir (por supor) | supor, partir de |
| suportar (por apoiar) | sustentar, dar suporte, aguentar |
| entregar (resultado, valor) | dar, gerar, trazer |
| alinhado com / alinhar | combinar com, bater com |
| conectar com / conexão (figurado) | falar com, chegar em, vínculo |
| autêntico / autenticidade | ser você; ou cortar |
| essencial / vital / primordial / imprescindível | um por capítulo; senão "o que decide" |
| chave (fator-chave, ponto-chave, peça-chave) | o que decide, principal |
| relevante / relevância | que importa; ou nomear por quê |
| robustez / solidez (figurado) | o fato |
| protagonista / protagonismo | assumir o lugar; ou cortar |
| ressignificar | mudar o sentido de; ou cortar |
| zona de conforto | cortar; nomear o hábito |
| propósito (como cliché) | o que você quer; ou cortar |
| descomplicar | explicar, simplificar |
| desvendar / desmistificar | explicar, mostrar como funciona |
| pavimentar o caminho | abrir caminho |
| ao longo do caminho | no meio disso, enquanto isso |
| ponto de virada / virada de jogo | "virada de chave" (termo da casa) ou o fato |
| game changer | cortar; nomear o que mudou |
| a boa notícia é que | uma por capítulo |
| não se preocupe | fica tranquila (se a autora fala assim) |
| ter em mente | lembra que |
| tirar vantagem de | aproveitar |
| dito isso | uma por capítulo |
| além disso (abrindo frase) | uma por seção |
| por fim / por último, mas não menos importante | "e"; ou nada |
| em suma / em resumo / concluindo / para finalizar | cortar |
| note que / observe que / perceba que | cortar |
| lembre-se de que | lembra que; ou cortar |
| de forma geral / geralmente / normalmente / tipicamente | cortar (hedge) |
| basicamente / essencialmente | cortar |
| relativamente | cortar |
| certamente / sem dúvida / sem sombra de dúvida / é inegável que | cortar |
| não é segredo que / todos sabemos que / como bem sabemos | cortar |
| mais do que X, Y / muito além de X | afirmar Y |
| seja você X ou Y | escolher a leitora |
| tanto X quanto Y (encadeado) | listar ou escolher |
| representa (por é) | é |
| se configura como / constitui / se caracteriza por | é |
| conta com / dispõe de / possui / oferece (por tem) | tem |
| se destaca por | o fato |
| refere-se a | é |
| ligado a / associado a / relacionado com (papel vago) | nomear a relação |
| real / verdadeiro / genuíno (adjetivo oco) | cortar ou seguir com nome, cidade, número e prazo |
| específico / determinado (sem o específico) | dar o específico |
| baseado em dados / orientado a dados | com o número |
| experiência (do paciente, premium) | o que a paciente sente, nomeado |
| premium / alto padrão / de alto nível | de elite (termo da casa) ou o fato |
| exclusivo (como hype de headline) | ok como posicionamento; cair como hype |

### Nível 3: só conta em combinação

| Termo | Substituto que uma pessoa usaria |
|---|---|
| importante | ok; trocar se repetir três vezes na página |
| processo | ok; nomear a etapa quando der |
| ferramenta (figurado) | ok; "o Supercaso", "o script" |
| construir (autoridade, relação) | ok; "virar referência", "criar vínculo" |
| gerar (resultados, confiança) | ok; "trazer", "fazer nascer" |
| desenvolver (habilidade) | ok; "aprender", "treinar" |
| implementar | montar, aplicar, colocar pra rodar |
| aplicar | ok |
| nicho | ok; "quem você atende" |
| público-alvo / público | ok; "a paciente que você quer" |
| posicionamento (solto) [marca: vincular a ação] | sempre com o que fazer |
| autoridade | ok; provar com caso |
| valor (percebido) | ok em dose; "o que ela acha que vale" |
| diferencial | ok uma vez; senão o fato |
| resultado | ok; com número |
| método / sistema | ok; termos da casa |
| feedback | retorno, o que a paciente disse |
| follow-up | ok se a leitora fala assim; nunca "follow-up agressivo" |
| foco / focar | ok |
| cada vez mais | ok em dose |
| ou seja / isto é | ok; uma por parágrafo |
| uma vez que (causal) | porque, já que |
| através de (por meio de) | ok |
| a partir de | ok |
| inclusive | ok |
| então (abrindo frase) | ok; é fala |
| trata-se de / torna-se | ok sozinho; conta com "portanto" e passiva |
| portanto / logo / assim sendo | ok um por seção |
| entretanto / todavia / contudo | "mas", "só que" se a autora fala assim |
| bem como | "e" |
| visando | "pra" |
| mediante | "com", "por" |
| de modo a | "pra" |
| a fim de | "pra" |

Contagem: 78 entradas no nível 1, 62 no nível 2, 34 no nível 3. Total 174.

---

## Sinais de texto humano em PT-BR

O positivo. Quando o Editor vê isso, deixa em paz; a whitelist do fingerprint protege. Fontes: blader ("Keep the details that carry the writer's voice"), jooray ("Signs of human writing (preserve these)"), Wikipedia ("Signs of human writing / Syntax"), conor ("Rhythm and uniformity", "Over-polishing"), escrita-humana-reconecta ("Princípios").

- Elipse. A ponte óbvia foi cortada e a leitora preenche sozinha. "Cobrou 300. Ninguém reclamou. Em abril, 47."
- Frase de três palavras depois de uma de trinta. Variação real de tamanho, não frase curta por sistema.
- Opinião com dono. "Eu acho", "na minha experiência", "aposto que", "eu não faria". O modelo é neutro por padrão; gente tem lado.
- Contradição admitida. "Eu falo pra cobrar caro e eu mesma demorei dois anos pra fazer isso." Sentimento misturado e não resolvido é assinatura humana (jooray: "mixed feelings and unresolved tension").
- Detalhe concreto inútil. O nome da rua da primeira clínica, a marca do iPad de 10 mil reais que virou enfeite, a hora em que a mensagem chegou. Detalhe que não prova nada e por isso ninguém inventaria.
- Piada de situação. Humor que só funciona naquele contexto, não piada de fôrma.
- Referência ao próprio corpo, dia, cansaço. "Escrevi isso entre duas consultas." "Tô com a voz rouca de tanto gravar."
- Pergunta que não é retórica. Uma pergunta que a autora não sabe responder e diz que não sabe.
- Correção no meio da frase. "(quer dizer, quase; teve uma que reclamou)". O modelo raramente se interrompe.
- Gíria datada e referência de época que mapeia pra um ano e um grupo: nome de trend do Instagram do mês, meme do momento. O modelo atrasa um ano.
- Frase com "é", "tem", "fez", "usou", "tentou", "morreu". Verbo simples onde a IA põe "possui", "realizou", "utilizou", "buscou", "veio a falecer" (Wikipedia, "Syntax").
- Superlativo com nome: "a única da cidade que cobra consulta", "a primeira da turma a fechar 100 mil". O modelo evita definitivo; gente afirma.
- Conector de fala no começo da frase: "só que", "e aí", "mas", "aí", "então". O modelo escreve "no entanto", "dessa forma".
- Próclise e oralidade brasileira: "me conta", "se inscreve", "te falo", "a gente". A escrita de manual põe "conte-me".
- Palavra da casa no lugar da palavra do mercado: "agenda fechada" (não "agenda cheia"), "paciente que investe", "queimando dinheiro", "sangrando", "barganhando" (dna.md, seção 3).
- Frase longa com três subordinadas que respira e chega inteira. Português aguenta; picar tudo em fragmentos é tell.
- Frase-assinatura literal da casa na posição de frame, uma por capítulo.
- Repetição da palavra certa. "Consulta" quatro vezes no parágrafo porque é sobre consulta. Sem sinônimo de escola.
- Escolha editorial que a autora consegue explicar. "Cortei o caso da Márcia porque ela pediu." Quem escreveu sabe por quê (Wikipedia, "Ability to explain one's own editorial choices").
- Imperfeição deixada. Uma frase que começa com "E". Uma vírgula a mais. Texto polido demais empurra o perfil estatístico pra IA (conor, "Over-polishing").

Regra de ouro pro Editor: se o parágrafo poderia ter sido escrito por qualquer mentoria sobre qualquer produto, ele ainda não tem voz. Se tem um detalhe que só aquela autora saberia, tem.
