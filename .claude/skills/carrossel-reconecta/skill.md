---
name: carrossel-reconecta
description: >
  Cria carrosséis RECONECTA em lote para Instagram. Analisa top performers da conta,
  gera N carrosséis com ângulos e hooks diferentes, trata imagens via Adobe for Creativity,
  busca provas sociais no Slack, monta build.py com o template editorial e exporta slides
  prontos (1080×1350px feed + 1080×1080px ads). Acionar quando o usuário pedir carrosséis
  novos, "gera os carrosséis da semana", ou qualquer variação de criação em lote RECONECTA.
---

# Skill: carrossel-reconecta

Orquestra a criação em lote de carrosséis RECONECTA com base nos top performers do Instagram.
O usuário só define quantidade — eu analiso o que performa, gero ângulos e hooks diferentes.

## Trigger
- "Cria 10 carrosséis"
- "Gera os carrosséis da semana"
- "Quero N carrosséis novos"
- Qualquer variação de pedido em lote sem tema definido

---

## FASE -1 — Carregar configuração (obrigatório, uma vez por sessão)

Antes de qualquer coisa, ler o arquivo de configuração do agente para obter os paths desta sessão:

```bash
cat "{REPO_ROOT}/agentes/carrossel/agente.config.json"
```

Onde `{REPO_ROOT}` é o diretório raiz do repositório reconecta (working directory atual).

Extrair e usar os valores:
- `BASE` → diretório raiz do agente no SSD (onde ficam bank/, SEM{xx}/, etc.)
- `TEMPLATE_DIR` → caminho do módulo `_template` do repo
- `NOISE_SRC` → caminho do noise.png
- `PYTHON` → interpretador Python a usar

Se `agente.config.json` não existir, orientar o usuário a criá-lo seguindo `agentes/carrossel/SETUP.md`.

Definir a partir do config:
```
BASE_SSD   = {BASE}
AGENTE_CLI = {BASE}/agente_carrosseis.py
TEMPLATE   = {TEMPLATE_DIR}
PYTHON     = {PYTHON}
```

---

## CTA — definir caso a caso com o usuário

Não há CTA fixo para feed. Alinhar com o usuário antes de fechar cada carrossel.

Opções válidas:
- `COMENTE "SUPERCASO"` — padrão quando não há outro objetivo específico
- `SALVA ESSE POST` — quando o slide é referência prática que o leitor vai consultar depois
- `COMENTE [PALAVRA]` — quando há lead magnet específico (definir a palavra com o usuário)
- `MANDA UMA DM` — quando o próximo passo é conversa direta
- Link na bio — quando há landing page ou lead magnet vinculado
- Pergunta aberta — quando o objetivo é comentário e engajamento

CTA dos ads 1080×1080: sempre `TOQUE NO BOTÃO` (fixo, sem exceção).

---

## Workflow completo

### FASE 0 — Análise Instagram (uma vez por sessão)

1. Chamar `mcp__claude_ai_INSTAGRAM__buscar_posts`
2. Calcular score de cada post: `score = likes + (comments × 3) + (saves × 5)`
3. Separar top 10 por score
4. Para cada post do top 10, extrair:
   - Tema central
   - Ângulo/hook usado
   - Estrutura do copy (como começou, como terminou)
5. Com base nos top 10, gerar **N variações com ângulos e hooks diferentes** dos originais:
   - Mesmo tema → perspectiva diferente (ex: top performer foi "o erro de X" → novo ângulo: "por que X acontece")
   - Contra-intuitividade: inverter a premissa do post que performou
   - Especificidade: pegar um subtema do post que performou e aprofundar
   - Prova social: transformar resultado de aluno em carrossel educativo
6. Apresentar a lista de N temas+ângulos gerados ao usuário para aprovação antes de montar

---

### FASE 1 — Provas sociais via Slack

> Usar Slack MCP para buscar prints de resultados de alunos antes de montar cada carrossel.

1. Buscar mensagens no canal de provas sociais da empresa (canal a confirmar com usuário na 1ª vez)
2. Filtrar mensagens com anexos de imagem (screenshots de WhatsApp, resultados)
3. Para cada imagem relevante, ler o conteúdo e indexar: `{ arquivo, resultado_descrito, tema_relacionado }`
4. Na montagem de cada carrossel, cruzar o tema com os resultados indexados e escolher o mais relevante
5. Baixar o arquivo do Slack para `provas_sociais/` e usar no slide PROVA

**Fallback:** se Slack não autenticado ou canal sem prints, verificar `{BASE}/provas_sociais/` local.

---

### FASE 2 — Preparação (por carrossel)

1. Definir semana ISO: `SEM{xx}`
2. Definir slug em kebab-case do tema (ex: `erro-financeiro-dentista`)
3. Definir número AD: próximo sequencial com base na pasta (`AD001`, `AD002`...)
4. Escolher categoria de imagem pelo tema:

| Tema | Categoria |
|---|---|
| Resultados, lifestyle, faturamento, agenda cheia | influenciadora |
| Técnica, metodologia, SUPERCASO, erros clínicos | atriz |
| Mindset, posicionamento, preço, autoridade | atriz |
| Redes sociais, captação, Instagram | influenciadora |
| Empate: qual tem mais disponível | — |

5. Criar estrutura:
   ```bash
   {PYTHON} "{AGENTE_CLI}" criar --semana SEM{xx} --slug {slug}
   ```

---

### FASE 3 — Imagem (padrão vinci: orgânica > banco)

> **REGRA VINCI:** A hero deve ser foto orgânica do Leonardo — selfie, ambiente real, celular, sem produção pesada. Banco de imagens é fallback quando não há foto disponível.

> SEMPRE chamar `adobe_mandatory_init` antes de qualquer tool Adobe.

**Prioridade 1 — Foto orgânica do Leonardo (preferencial)**

Perguntar ao usuário: "Você tem uma foto do Leonardo para a hero deste carrossel? (selfie, bastidor, viagem, escritório)"

Se sim: o usuário deposita em `img/hero.jpg` dentro da pasta do carrossel e segue direto para o pipeline Adobe abaixo.

**Prioridade 2 — Banco de imagens (fallback)**

Usar apenas se o usuário não tiver foto orgânica disponível:

1. Selecionar do banco:
   ```bash
   {PYTHON} "{AGENTE_CLI}" selecionar --categoria {categoria}
   ```
2. Marcar usada após download:
   ```bash
   {PYTHON} "{AGENTE_CLI}" marcar-usada --id {img_id} --carrossel {ADnum-slug}
   ```

**Pipeline de tratamento Adobe (aplicar em qualquer caso)**

1. `adobe_mandatory_init()`
2. Se foto orgânica local: fazer upload para o Adobe primeiro
3. Pipeline em sequência, passando `outputUrl` de um para o próximo:
   - `image_crop_and_resize` → `output: "4:5"`, `fit: "reframe"`, `focus: "upper_body"`
   - `image_apply_auto_tone` → usando URL do passo anterior
   - `image_adjust_color_temperature` → `a: 20, b: 55, luminance: 48` (grading quente, paleta burgundy)
4. Baixar resultado:
   ```bash
   {PYTHON} "{AGENTE_CLI}" baixar \
     --url {presignedAssetUrl_final} \
     --destino "{BASE}/SEM{xx}/{slug}/img/hero.jpg"
   ```

---

### FASE 4 — Copy (padrões vinci obrigatórios)

Anatomia consolidada pós-vinci:

```
Slide 1       HERO    → foto orgânica + promessa irresistível + subtitle de entrega
Slide 2       PROVA   → dado/case/autoridade que convence a continuar
Slides 3..N-2 MIOLO   → conteúdo de valor + acionáveis práticos
Slide N-1     INSIGHT → síntese / virada / frase-frame (obrigatório)
Slide N       CTA     → caso a caso, alinhar com o usuário antes de fechar
```

**Regra 0 — Voz da copywriter (não-negociável, senão sai robótico)**

Antes de escrever, ler `{REPO_ROOT}/agente-carrosseis/voice-dna.md` e aplicar os **5 dispositivos**: (1) frase pronta exata (aspas, colável) em cada slide de entrega; (2) contraste seco / one-liner disruptivo; (3) detalhe concreto inesperado (hora/número/objeto); (4) monólogo interno + punch; (5) número escalado (3,5,7, não redondo). Regra de ouro: **ENCENAR a cena, nunca EXPLICAR o conceito**. Se ler como "IA descrevendo um conceito" (abstrato, genérico, sem fala literal), reescrever. (Aprendizado 01/jul: âncora de tema/gancho/estrutura NÃO basta — a especificidade viva é o que separa "parece IA" de "parece a copywriter".)

**Regra 1 — Subtitle da hero = promessa concreta de entrega**

Não poético, não temático. Completar "Você vai aprender..." ou "Um guia para...".
- Válido: "Um guia neurocientífico para acabar com a auto sabotagem"
- Inválido: "A verdade que ninguém te contou" (sem entrega clara)

Se o subtitle não estiver prometendo entrega explícita, refaz.

**Regra 2 — Slide 2 = prova que vale continuar (nunca problema)**

Tipos válidos:
- Dado concreto (número, estatística, pesquisa)
- Resultado real (case, transformação de aluno)
- Autoridade (citação, credencial, experiência específica)
- Quebra de objeção (anti-tese surpreendente)
- Virada de chave (insight contra-intuitivo)

Anti-padrão: "Você sente X dor?" ou qualquer coisa que aprofunde o problema sem dar evidência.

**Regra 3 — Insight obrigatório antes do CTA**

Todo carrossel tem slide de insight. Não é opcional. Deve entregar:
- Síntese poderosa do que foi mostrado, OU
- Virada de perspectiva que reorganiza tudo que veio antes, OU
- Frase-frame que o leitor vai querer salvar/printar

**Regras gerais de copy:**
- Sem travessão (—) ou hífen no meio de frase: usar ponto ou vírgula
- Sem emojis nos slides
- Ângulo diferente dos top performers (não copiar, derivar)
- Usar tom/estrutura dos top performers como referência, não como template

---

### FASE 5 — Build e preview

1. Escrever `build.py` com o template de `{REPO_ROOT}/agentes/carrossel/build_template.py.txt`
   - O template detecta automaticamente o TEMPLATE_DIR via agente.config.json
2. Executar:
   ```bash
   {PYTHON} "{AGENTE_CLI}" build --dir "{BASE}/SEM{xx}/{slug}"
   ```
3. Abrir preview:
   ```bash
   open "{BASE}/SEM{xx}/{slug}/carousel.html"
   ```
4. Aguardar aprovação do usuário antes de renomear e seguir pro próximo

---

### FASE 6 — Renomeação após aprovação

```bash
{PYTHON} "{AGENTE_CLI}" renomear \
  --dir "{BASE}/SEM{xx}/{slug}" \
  --ano {aa} --sem {ss} --num {ADnum} --titulo "{Titulo Curto}"
```

Formato final: `[26] [18] [AD005_1] - Titulo Do Carrossel.png`

---

### FASE 7 — Versão ads 1080×1080 (após 7+ aprovados)

Quando o usuário aprovar o 7º carrossel (ou qualquer múltiplo de 7):

1. Listar todos os carrosséis aprovados na semana atual
2. Para cada um, executar:
   ```bash
   {PYTHON} "{AGENTE_CLI}" build --dir {pasta_carrossel}
   ```
   Ou, se o `build_ads.py` existe na pasta:
   ```bash
   {PYTHON} build_ads.py
   ```
3. CTA fixo em todos os ads: **`TOQUE NO BOTÃO`** (sem exceção, sem sugestão alternativa)
4. Export e renomear com sufixo `_ad`: `[26] [18] [AD005_1ad] - Titulo.png`

---

## Regras visuais (sempre aplicar, sem exceção)

- Fontes: **Alga** (hero/cta) + **Grift** (todo o resto)
- Paleta: `#0F0505` · `#EDE3CE` · `#B8965A` · `#6B0F0F`
- Crimson `#C9252D`: máximo 1 palavra por slide
- Slides 1 e N: dark. Slide 3 (ou equivalente): cream para quebrar ritmo
- Masthead sempre presente no topo
- Noise overlay na hero (noise.png copiado automaticamente pelo `criar`)
- Sem progress bars, chevrons de swipe ou emojis

## Nomenclatura de saída

```
Feed:  [AA] [SS] [AD00N_M]    - Titulo.png
Ads:   [AA] [SS] [AD00N_Mad]  - Titulo.png
```
