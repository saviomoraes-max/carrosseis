---
name: brand-guidelines
description: Aplica a identidade visual oficial da RECONECTA (cor e tipografia) a qualquer artefato que se beneficie do look-and-feel da marca. Use quando cor de marca, tipografia, formatação visual ou padrão de design da empresa forem relevantes.
license: Complete terms in LICENSE.txt
---

# RECONECTA — identidade visual

## Onde os valores vivem

**Esta skill não guarda cor nem tamanho.** A fonte de verdade é:

```
~/reconecta/design-system/core/tokens.json
```

**Leia esse arquivo antes de aplicar qualquer cor ou fonte.** Ele traz as 8 cores
com nome semântico, as duas pistas de tipografia, a escala por formato e as leis
da marca. Se o que você precisa não estiver lá, o valor não existe — pergunte,
não invente.

> Versões anteriores desta skill traziam uma paleta própria
> (`#3D0A0A`, `#FF3939`, `#26428B`, títulos em Alga) que **contradizia** o
> sistema real e nunca foi usada em produção. Foi removida em 18/ago/2026,
> depois de um comparativo visual entre as três paletas concorrentes da casa.

## Como escolher a pista tipográfica

O `tokens.json` define duas, e a escolha depende de **onde o arquivo vai viver**:

- **licenciada** (Dx Monstral + Grift + Inter) — para o que nós renderizamos:
  carrossel, PDF, vídeo. As fontes estão em `carrosseis/_template/fonts/`.
  São comerciais: nunca redistribuir.
- **google** (Archivo Black + Figtree + Inter) — para o que o time edita:
  Google Apresentações, PPTX, e qualquer máquina sem as licenciadas.
  Estão em `design-system/fontes/google/`, são OFL.

Na dúvida entre as duas: se um humano vai abrir e editar o arquivo, use a pista
**google**.

## Leis que não são numéricas

Estão em `tokens.json` no campo `leis`, e valem em todo artefato:

- Ênfase é só **cor** — nunca itálico, nunca peso mais fino.
- Um acento crítico (vermelho) por peça. Dois se cancelam.
- Nunca encolher o texto pra caber a copy. A trava é a copy.
- Sem travessão nem hífen no meio de frase.
- Nada sobrepõe nada, nada encosta na borda.
- Sempre "harmonização facial" — nunca "HOF", nunca "orofacial".
- O inimigo é comum, nunca a doutora.

## Apresentações

Não monte deck do zero. O modelo com os 9 layouts já existe em
`design-system/pptx/RECONECTA-modelo.pptx`, e o time trabalha nele pelo
**Google Apresentações**. Ver `design-system/README.md`.
