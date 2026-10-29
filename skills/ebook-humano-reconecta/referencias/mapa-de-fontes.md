# Mapa de fontes

De onde veio cada coisa do catálogo, o que cada repositório faz melhor, o que copiamos, o que descartamos e por quê. Clones em `refs/`. Licença confirmada lendo o arquivo LICENSE de cada um.

## Fonte primária

### Wikipedia: "Signs of AI writing" (`refs/wikipedia_signs_of_ai_writing.wiki`)

O que é: guia de campo do WikiProject AI Cleanup, com exemplos reais tirados de artigos e discussões da Wikipedia, em revisão contínua (a cópia é de setembro de 2026). É a raiz de todos os cinco repositórios abaixo.

O que faz melhor: exemplos reais e datados; a distinção entre "sinal" e "prova"; a seção "Ineffective indicators" (gramática perfeita, prosa formal, conectivo isolado, falta de citação não provam nada); a seção "Signs of human writing / Syntax" (verbo simples, superlativo definitivo, hedge humano, construção prolixa isolada são mais comuns em texto humano); a cronologia do vocabulário por era de modelo (2023 "delve", 2024 "showcasing", 2025 "highlighting"); e a nota de que a escola italiana ensina a evitar repetição de palavra, o que vale igual pra escola brasileira.

O que copiamos: as famílias Content, Language and grammar e Style inteiras, traduzidas pro contexto de ebook; a regra do cluster; a lista de indicadores ineficazes (virou parte das guardas de falso positivo); os sinais de texto humano.

O que descartamos: tudo sobre wikitext, Markdown dentro de wikitext, citações quebradas, DOI, categorias, edit summaries, AfC, user pages, comentários de talk page e os fingerprints de citação de cada chatbot. Não se aplicam a manuscrito de ebook; só o `utm_source=chatgpt.com` e os tokens `citeturn0search0` entraram no tell 5.11 como resíduo forense.

Licença: CC BY-SA 4.0 (texto da Wikipedia). Uso aqui é derivado com atribuição; o catálogo cita a seção de origem em cada tell.

## Repositórios (todos MIT)

### blader/humanizer (`refs/blader_humanizer/`)

Autor e licença: Siqi Chen, MIT, 2025. Versão 3.0.0 do SKILL.md.

O que é: o skill original de humanização, 25 padrões em 5 famílias (Staging, Rhythm by rule, Inflation and borrowed authority, Formatting by rule, Leftovers), ordenados do mais forte pro mais fraco, com a marcação "weak alone" nos que precisam de companhia.

O que faz melhor: a tese de que os hábitos estruturais persistem entre versões de modelo e o vocabulário muda; a ordenação por força de evidência; a regra "every sentence you keep must add something the reader did not already have"; a seção "When not to act"; a regra de que a amostra de voz do autor sobrepõe o skill (inclusive a regra do travessão).

O que copiamos: as cinco famílias (viraram as famílias 1 a 5 do catálogo, com a família 1 renomeada "Encenar em vez de afirmar"); a escala de gravidade (um avistamento vs. companhia); os tells 1 a 25 quase todos, adaptados; a precedência do fingerprint; a proibição de inventar fato.

O que descartamos: a lista de vocabulário em inglês (substituída pela tabela PT-BR); o tell 21 (aspas curvas) como estava, porque em PT-BR publicado aspas curvas são norma (virou o tell 4.9, invertido); o tell 25 (escrever sobre a versão anterior) por ser de documentação de código.

### jooray/humanizer (`refs/jooray_humanizer/`)

Autor e licença: fork do blader (LICENSE mantém Siqi Chen, MIT, 2025), versão 2.12.5, mantido por jooray. 54 padrões.

O que é: a linhagem anterior do blader, mais extensa, com 44 padrões gerais e uma seção dedicada a eslovaco e tcheco (§45 a §54).

O que faz melhor: a seção eslovaca. É o único repositório que trata uma língua não inglesa como sistema próprio, com a tese "most AI text in them is an English draft in disguise". Ela mostra como um tell inglês chega calcado (§47 cópula "predstavuje", §48 gerúndio/transgressivo, §49 vocabulário calcado, §50 spam de pronome e possessivo, §51 ordem de palavras inglesa, §52 deriva de registro, §53 tipografia e números, §54 empréstimos nem sobre nem subtraduzidos) e o que NÃO marcar naquela língua (passiva reflexiva, frase longa, partículas de fala). Também: §36 "Performed rigor and candor" (o mais completo sobre candor encenado), §41 teste do embaralhamento, §42 conectivo empilhado com contagem, §43 enumeração hedgeada, §44 esteira, §1 "significance stamp" e "graded verdict", a regra de contar o cluster uma vez, e o "Detect mode" sem porcentagem de probabilidade.

O que copiamos: o modelo inteiro da seção eslovaca, transposto pro PT-BR como famílias 6 e 7 do catálogo (cópula "representa" = "predstavuje"; rider de gerúndio = transgressivo; "você" em toda frase = spam de pronome; "lhe"/mesóclise = deriva de registro; números e datas = §53; estrangeirismo vs. jargão do campo = §54); os §36, §41 a §44; a lista de guardas de falso positivo; o "PERSONALITY AND SOUL" (virou "Sinais de texto humano").

O que descartamos: tudo que é específico de eslovaco e tcheco (aspas „…“, pomlčka, diacríticos ď ť ň, "nielen… ale aj"); os modos de invocação e o formato de saída, que a skill principal define de outro jeito (workflow com cético).

Nota: o README do jooray ainda aponta o badge pro blader/humanizer; os dois compartilham LICENSE e origem. Tratamos o blader 3.0.0 como a versão enxuta e o jooray 2.12.5 como a versão extensa da mesma linhagem.

### conorbronsdon/avoid-ai-writing (`refs/conorbronsdon_avoid-ai-writing/`)

Autor e licença: Conor Bronsdon, MIT, 2026. Empacotamento OpenAI contribuído por Mamdouh Aboammar sob a mesma licença (NOTICE.md).

O que é: o maior catálogo (74 categorias em `references/patterns.md`), com detector determinístico em JavaScript (`detector/patterns.js`, 54 tipos), tabela de vocabulário em 3 camadas (Tier 1A frequência, 1B clareza, Tier 2 cluster, Tier 3 densidade, mais 10 frases de Tier 3), perfis de contexto (linkedin, blog, technical-blog, investor-email, docs, casual) com matriz de tolerância, e perfis de voz.

O que faz melhor: a taxonomia do vocabulário em três níveis com a separação honesta entre "marcador de IA" e "edição de clareza" (1A vs. 1B: "presenting a wordiness fix as authorship evidence is the error this split exists to prevent"); o `CATEGORIES.md`, que documenta quais regras são regex e quais são julgamento (e por que várias tentativas de detector foram revertidas); os tells de registro social e conversacional (fake-casual register, social endorsement closers, lingering-attention claims, launch-copy introductions, recap-flattery opener, wall-of-text replies); os tells de crypto/infra (real/actual inflation, moral-adjective category errors, transformation crutch, false agency); a insistência em que estrutura pesa mais que vocabulário ("Structure is the #1 detection signal"); a advertência contra polir demais.

O que copiamos: o modelo de três níveis (virou "Vocabulário PT-BR em 3 níveis"); a distinção 1A/1B (no catálogo, o Editor não conta "vale ressaltar" como prova de IA quando aparece sozinho em texto de autora que escreve formal; é edição de clareza); os tells de emoção anunciada, etiqueta de importância, novidade inflada, falsa amplitude por template, cenário imaginado, lista de substantivos nus, colon-reveal, negation chains, stranded auxiliary, same-opener runs; a lógica do `CATEGORIES.md` vai orientar o `padroes_ptbr.json` (o que é regex, o que é cético).

O que descartamos: os perfis de contexto (o ebook tem um contexto só, e o fingerprint da autora substitui o perfil de voz); tudo de crypto, DePIN, dev-blog boilerplate, hashtag stuffing e launch-copy, que não aparecem em ebook de mentoria; o detector JS em si (o nosso é Python e em português); as carve-outs de list-item em Markdown com travessão, porque a casa proíbe travessão em qualquer posição.

### gregorymm/humanize-text (`refs/gregorymm_humanize-text/`)

Autor e licença: Gregory Muryn-Mukha, MIT, 2026.

O que é: plugin de Claude Code voltado a UX copy, microcopy e marketing, com 7 categorias pontuadas de 1 a 10 (total 70, convertido em "Human Score" em porcentagem), integração com Figma e leitura de screenshot.

O que faz melhor: a categoria "UX Copy Quality" (clareza sobre esperteza, especificidade sobre abstração, leitor como sujeito da frase, comprimento adequado ao contexto, ritmo natural); a tabela de troca de buzzword de produto (seamless, empower, unlock, elevate, leverage, robust, streamline); a lista de "AI pleasantries" (hope this finds you well, happy to help, feel free to, don't hesitate, excited to share) que ninguém mais listava; a regra "if fewer than 4 rows, write it as a sentence"; o alerta "don't swap one AI word for another".

O que copiamos: as pleasantries (viraram o tell 6.15, cortesia de e-mail traduzida); a regra da tabela pequena (4.8); a regra "leitora como sujeito" reforçando o 7.2 e o 7.3; o princípio de que a IA regride à média e troca detalhe específico por elogio genérico.

O que descartamos: a pontuação numérica por categoria e o "Human Score" (a skill principal usa detector com nota 0 a 100 mais veredito de agente cético; um percentual de humanidade por categoria dá falsa precisão, como o jooray argumenta no Detect mode); toda a integração com Figma e screenshot; a permissão de 1 travessão por página em UI text (a casa é zero).

### luquiluke/claude-book-skill (`refs/luquiluke_claude-book-skill/`)

Autor e licença: Lucas Slater (luquiluke), MIT, 2026.

O que é: estúdio de livro de não ficção em seis agentes (Librarian, Researcher, Writer, Editor, Reviewer, Compiler), com fingerprint quantificado de estilo do autor, whitelist de hábitos, fact sheet por capítulo, e um companheiro de língua pra espanhol (`references/lang/es.md`) com voseo rioplatense.

O que faz melhor: a arquitetura de precedência (fingerprint do autor acima das regras; whitelist com evidência de 3 ou mais ocorrências no corpus); o `writing-rules.md` com as cinco famílias e a seção "Compression" ("over-explanation is the most reliable AI tell of all, and no banned-word list catches it"); e principalmente o `es.md`, que é o modelo mais próximo do que o PT-BR precisava: vocabulário vetado em espanhol, muletillas ("Cabe destacar", "En la era digital", "No solo X sino también Y, la firma más delatora del español IA"), hedges, e a seção 4 de calcos do inglês com tabela calco/espanhol real ("hacer sentido", "tomar acción", "asumir por suponer", "eventualmente por finalmente", "al final del día", "es acerca de"), com a observação de que "sobrevivem aos filtros de vocabulário porque cada palavra é legítima; só o uso é estrangeiro". A seção 5 e 6 (variante regional como lei, jamais misturar tratamento) deu a base do tell 7.7.

O que copiamos: a precedência do fingerprint e a whitelist (já estão na skill principal, Fase 1); a compressão (tell 2.6); os openers de gerúndio sem sujeito (7.1); a tabela de calques como formato (família 6 inteira segue esse molde); "cabe destacar / vale la pena mencionar" (5.3); a proibição de mistura de tratamento (7.7); a checagem de números e convenções locais (6.18).

O que descartamos: o pipeline de seis agentes e a compilação em .docx (a skill principal tem o próprio workflow e compila em PDF); o voseo e tudo específico de espanhol; o orçamento de "2 travessões por capítulo" (a casa é zero); o emoji de aviso em claims sem fonte (a casa usa front matter com fontes e o Fiscal de fidelidade).

### ThomasHoussin/Claude-Book (`refs/ThomasHoussin_Claude-Book/`)

Autor e licença: Thomas Houssin, MIT, 2025.

O que é: framework multiagente pra escrever romance com Claude Code: bíblia permanente (estilo, estrutura, personagens, universo), estado transitório por capítulo, timeline, agentes de planejamento, escrita, lint de estilo, revisão de personagem e continuidade, mais um skill "perplexity-improver" pra reduzir clichê e padrão de IA, com loop de até 3 iterações e build de EPUB.

O que faz melhor: a separação entre bíblia (não muda durante a escrita) e estado (versionado por capítulo); o loop de revisão com limite de iterações; a continuidade como agente próprio. É o antecessor que o luquiluke cita como fonte da "bible-style continuity, validation loops".

O que copiamos: nada do catálogo de tells (o repositório não tem catálogo de tells; o perplexity-improver é sobre perplexidade estatística de ficção, não padrões nomeados). A ideia de bíblia permanente vs. estado por capítulo já vive na skill principal como `fontes/` e `fingerprint` (permanentes) vs. `manuscrito/` e `revisao/NN/` (por capítulo).

O que descartamos: tudo de ficção (personagens, universo, sinopse, beats), o build em PowerShell e o EPUB. Não é fonte do catálogo; fica em `refs/` pela arquitetura de agentes.

## Skills locais absorvidas

### escrita-humana-reconecta (`~/.claude/skills/escrita-humana-reconecta/SKILL.md`)

10 tells em PT-BR no tom da casa (contraste fácil, anáfora de enfeite, muleta "mas quando", tudo em lista, ficar em cima do muro, fecho grandioso, explicar demais, ritmo de metrônomo, achismo embalado, travessão reflexivo), mais calibração de voz e princípios. É a régua curta. O catálogo não contradiz nenhum dos 10; cada um virou um tell numerado com origem citada (1.1, 2.2, 4.3, 5.4, 1.2, 2.6, 2.4, 3.3, 2.3). A muleta "mas quando" não ganhou tell próprio: entra como variante em 1.7 (objeção fantasma) e 5.12 (concessão falsa). O princípio "leia procurando o padrão, não a palavra" e o alerta "se poderia ter sido escrito por qualquer marca sobre qualquer produto, ainda não tem voz" fecham o catálogo.

### voice-dna (`~/.claude/skills/voice-dna/dna.md`)

DNA de voz RECONECTA de 30/04/2026. Forneceu as guardas de falso positivo mais importantes: antítese e repetição intencional como recurso central (guardas de 1.1, 1.3, 2.2); listas de 3 a 4 itens com paralelismo quando deliberadas (guarda de 2.1); "você" dominante e "doutora" como vocativo (guardas de 7.2 e 7.7); "virada de chave" como termo da casa (guarda de 3.1); "diagnóstico que libera culpa" como distinto de bajulação (guarda de 5.9); fecho típico "Faz essas alterações e me conta como foi" (conserto de 5.6); proibições (travessão, emoji, "high ticket", saudação vaga, vender procedimento, promessa sem prova).

Discrepância registrada: o dna.md lista "ecossistema" no cluster de vocabulário de marca (seção 3) e usa a palavra no padrão emocional de pertencimento (seção 5). A instrução desta skill veta "ecossistema". Prevalece o veto no ebook; substitutos no catálogo: "comunidade", "a turma", "a casa", "acompanhamento". Quem revisar o dna.md deve alinhar.

### reconecta-copywriting / banco-de-termos (`~/.claude/skills/reconecta-copywriting/referencias/banco-de-termos.md`)

Termos do método (Fábrica de Contatos, Agenda Fechada, Paciente que Investe, Supercaso, Framework 715, Presente Inaceitável, Futuro Perfeito, Invisibilidade Estratégica, Cardápio de Serviços, Derretimento Facial, Lente do Profissional vs. Lente do Paciente), posicionamento por contraste (sistema de captação, não funil; case real com nome, cidade, número e prazo, não "prova social"), duas camadas de palavras proibidas (hype de headline; jargão de marketing com substituto) e frases-assinatura validadas. Forneceu: os termos [marca] da tabela de vocabulário; a régua de prova (conserto de 3.3, 3.9, 1.10); a guarda de "resultado real / case real" (3.10); a guarda dos rótulos proprietários (3.11); a lente da paciente (7.8); as frases-assinatura como intocáveis (guarda de 1.4).

Nota: o próprio banco usa a sigla "HOF" no cabeçalho e numa nota interna. Isso é vocabulário de bastidor; no texto que a leitora lê, a regra é "harmonização facial", sempre, nunca "HOF" nem "orofacial" (memória `feedback_termo_harmonizacao_facial`, e a instrução desta skill).

## O que o catálogo tem que nenhuma fonte tinha

As famílias 6 (calques do inglês) e 7 (tradução de registro) em português do Brasil. O jooray deu o método (eslovaco), o luquiluke deu o molde (espanhol), e os exemplos, as guardas e a gravidade em PT-BR são observação própria a partir dessas duas e do corpus de ebook de vendas pra harmonização facial. Onde um tell não tem repositório de origem, o catálogo diz "observação própria do PT-BR" e cita o tell inglês mais próximo.
