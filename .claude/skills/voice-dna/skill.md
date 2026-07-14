---
name: voice-dna
description: >
  Analisa, valida e gera copy no tom de voz da marca RECONECTA.
  Três modos: (A) extrai padrões de voz de amostras reais → salva em dna.md,
  (B) valida copy novo contra o DNA salvo, (C) gera copy guiado pelo DNA.
  Acionar quando o usuário mandar amostras de texto para análise, pedir
  validação de copy, ou pedir geração de texto no tom RECONECTA.
---

# Skill: voice-dna

Captura, preserva e aplica a voz da marca RECONECTA em qualquer copy.

## Triggers

- "analisa esse texto / essas amostras"
- "como é a voz do RECONECTA?"
- "valida esse copy"
- "esse texto está no tom certo?"
- "escreve no tom RECONECTA"
- "gera copy com a voz da marca"
- Qualquer envio de amostras de texto para análise

## Arquivo de referência

DNA salvo em: `.claude/skills/voice-dna/dna.md`
Sempre ler esse arquivo antes de validar ou gerar copy.

---

## MODO A — Extração de DNA (quando o usuário envia amostras)

Objetivo: ler as amostras e montar um perfil de voz preciso e acionável.

### Dimensões a extrair

**1. Tom geral**
- Posicionamento no espectro: direto ↔ suave / provocador ↔ acolhedor / técnico ↔ emocional
- Qual é a postura de quem fala? (professor, par, mentor, desafiador)

**2. Estrutura de frase**
- Tamanho médio das frases (curtas, médias, longas, misto)
- Padrão de abertura: afirmação? pergunta? dado? contradição?
- Padrão de fechamento: convite? afirmação forte? pergunta reflexiva?
- Uso de listas vs. parágrafos corridos

**3. Vocabulário e léxico**
- Palavras e expressões recorrentes (listar literalmente)
- Palavras nunca usadas / que destoa do tom
- Uso de jargão técnico: sim, não, quando?
- Pronomes predominantes: você / a gente / profissional

**4. Ritmo e cadência**
- Como a tensão é construída? (problema → agravamento → virada → solução)
- Onde vem o gancho — início, meio ou fim?
- Uso de repetição intencional, paralelismo, antítese

**5. Padrões emocionais**
- Qual emoção é acionada? (ambição, medo de perder, pertencimento, orgulho)
- Como a transformação é descrita? (antes/depois, dor/alívio, erro/acerto)

**6. Proibições identificadas**
- O que nunca aparece nas amostras de alto desempenho

### Output da extração

Após analisar todas as amostras:
1. Apresentar ao usuário um resumo do DNA com exemplos diretos das amostras
2. Pedir confirmação: "Esse perfil representa bem a voz da marca?"
3. Após confirmação, **sobrescrever** `.claude/skills/voice-dna/dna.md` com o DNA validado
4. Confirmar: "DNA salvo. Vou usar esse perfil em todos os carrosséis daqui em diante."

---

## MODO B — Validação de copy

Objetivo: auditar um texto entregue contra o DNA salvo.

### Processo

1. Ler `dna.md`
2. Ler o copy a ser validado
3. Avaliar cada dimensão do DNA e atribuir um score (✓ alinhado / △ parcial / ✗ divergente)
4. Para cada divergência (△ ou ✗), apontar:
   - O trecho específico que destoa
   - Por que destoa (qual regra do DNA quebra)
   - Sugestão de reescrita no tom correto

### Formato de saída

```
DIAGNÓSTICO DE VOZ
──────────────────
Tom geral:       ✓ alinhado
Estrutura:       △ parcial — [trecho] → sugestão
Vocabulário:     ✗ divergente — [trecho] → sugestão
Ritmo:           ✓ alinhado
Padrão emocional: ✓ alinhado

SCORE GERAL: 8/10

REESCRITAS SUGERIDAS:
[trecho original]
→ [versão ajustada]
```

---

## MODO C — Geração de copy guiada

Objetivo: criar copy novo que soa autenticamente RECONECTA.

### Processo

1. Ler `dna.md` antes de escrever qualquer linha
2. Receber do usuário: tema + estrutura de slide (ex: "slide 3, miolo dark, sobre o erro de apresentar o plano cedo")
3. Gerar o copy aplicando ativamente cada dimensão do DNA:
   - Tom e postura identificados
   - Tamanho e abertura de frase conforme padrão
   - Vocabulário recorrente quando natural
   - Ritmo e tensão conforme padrão extraído
4. Ao entregar, indicar quais elementos do DNA foram aplicados (brief interno, não mostrar ao usuário — só mostrar o copy)

### Integração com carrossel-reconecta

Na **FASE 4 (Copy)** do workflow de carrosséis:
- Sempre ler `dna.md` antes de escrever qualquer slide
- Aplicar o DNA como briefing de voz implícito
- Após escrever os slides, rodar internamente o MODO B para auto-validar antes de apresentar ao usuário

---

## Regras gerais

- Nunca gerar copy sem ler `dna.md` primeiro (se existir)
- Se `dna.md` estiver vazio ou ausente, avisar o usuário e oferecer o MODO A
- Não resumir o DNA — usar os padrões literalmente, não interpretativamente
- Ao atualizar o DNA, nunca apagar amostras anteriores — acrescentar e reconciliar
