---
name: reconecta-design-tokens
description: Estende e mantém os design tokens da RECONECTA. Use ao adicionar cor, tamanho, espaçamento ou regra nova ao sistema, ou ao levar os tokens da marca pra um projeto novo (Tailwind, CSS, PPTX, engine de render).
---

# Design tokens — RECONECTA

## A regra que rege tudo

**Existe um único lugar onde um valor da marca existe:**

```
~/reconecta/design-system/core/tokens.json
```

Cor, escala tipográfica, margem, raio e as leis da marca saem daí. Nenhum outro
arquivo deve repetir um hex. Projeto novo **consome** o núcleo; não copia.

> Versões anteriores desta skill traziam uma paleta própria de Tailwind
> (`#6b0f0f` / `#d3111a` / `#eece66`) que **contradizia** o sistema real.
> Foi removida em 18/ago/2026 — a paleta vencedora é a que está no `tokens.json`.

## Antes de mexer

1. Leia o `tokens.json` inteiro.
2. Veja se o valor que você quer já existe com outro nome semântico.
3. Só então adicione.

## Quando criar token novo

**Crie** se: aparece 3+ vezes, representa decisão de design intencional, e vai
mudar junto se a marca mudar.
**Não crie** se: é one-off de um componente experimental.

## Nomenclatura

O núcleo usa **nome semântico, não nome de cor**: `fundo/base`, `texto/enfase`,
`acento/critico`. Nunca `vermelho-500` nem `bordo-2`. O nome diz o **papel**, e
é por isso que trocar a marca inteira é trocar um arquivo.

Ao estender, siga o mesmo padrão: `{categoria}/{papel}`.

## Levando os tokens pra um projeto

**Tailwind v4** — gere o bloco `@theme` a partir do `tokens.json`, não escreva à
mão. Prefixo `--color-*` gera `bg-*`, `text-*`, `border-*`; `--text-*` tamanho;
`--spacing-*`, `--radius-*`, `--shadow-*` idem. Sem `tailwind.config.js` em v4.

**PPTX** — já existe: `design-system/pptx/build_potx.py` lê o núcleo e gera o
modelo. Use de exemplo pra qualquer gerador novo.

**Carrossel** — `carrosseis/_template/html-engine/engine.py`. Ainda tem a paleta
embutida no topo do arquivo; quando for mexer nele, migre pra ler o `tokens.json`.

## Anti-padrões

- Duplicar a paleta com outros nomes em outro arquivo.
- Valor cru no HTML/slide (`style="color:#ff2222"`) em vez de token.
- Token one-off usado num lugar só.
- Mudar cor direto no artefato (slide, carrossel) em vez de no núcleo.

## Verificação

Mudou o núcleo? Regere e **olhe** o que depende dele:

```bash
./.venv-ds/bin/python design-system/pptx/build_potx.py
```

Depois exporte em PDF e confira os 8 slides. Token quebrado se espalha por todo
material que o time fizer depois.
