---
name: reconecta-design-tokens
description: Gerencia e estende design tokens (cores, tipografia, espaçamento, sombras, raios) no setup Tailwind v4 dos projetos Reconecta. Use quando o usuário pedir para adicionar/modificar tokens em src/input.css, criar typography scale, definir spacing system, adicionar variantes de tema, ou estender o design system além da paleta atual. A paleta de cores da marca já está configurada.
---

# Skill: Design tokens — Reconecta (Tailwind v4)

Esta skill gerencia o design system em projetos Reconecta usando o sistema `@theme` do Tailwind v4. A paleta de cores já está configurada — use esta skill para estender com outros tipos de tokens ou criar novos sistemas semelhantes.

## Quando invocar

- Usuário pede: "adicione typography scale", "define o spacing", "cria os tokens de sombra", "adiciona um novo token"
- Antes de construir componentes que precisam de tokens consistentes (botões, cards, modais)
- Quando o usuário pergunta sobre convenções de nomenclatura de tokens

## Stack e convenções do projeto

- **Tailwind v4** com tokens definidos via `@theme` em `src/input.css`
- **Não usa `tailwind.config.js`** (config é em CSS, não JS, em v4)
- Build: `npm run build` (minified) e `npm run dev` (watch)
- HTML estático (sem framework)

## Convenção de nomenclatura

Padrão da paleta atual: `--color-{família}-{variante}`
- Famílias: `primary`, `secondary`, `surface`, `tertiary` (+ `base`: branco/preto)
- Variantes: `light`, `light-hover`, `light-active`, `normal`, `normal-hover`, `normal-active`, `dark`, `dark-hover`, `dark-active`, `darker`

**Para novos tokens, mantenha o mesmo padrão**:
- `--{categoria}-{nome}-{escala/variante}`
- kebab-case sempre
- Português ou inglês, mas consistente dentro da mesma categoria

## Como adicionar tokens

Todos os tokens vão em `@theme { ... }` dentro de `src/input.css`. Tailwind v4 gera utilities automaticamente baseado nos prefixos:

| Prefixo CSS | Gera utility |
|------------|-------------|
| `--color-*` | `bg-*`, `text-*`, `border-*`, `ring-*`, etc. |
| `--font-*` | `font-*` |
| `--text-*` | `text-*` (tamanho) |
| `--spacing-*` | `p-*`, `m-*`, `gap-*`, etc. |
| `--radius-*` | `rounded-*` |
| `--shadow-*` | `shadow-*` |
| `--breakpoint-*` | breakpoints customizados |
| `--leading-*` | `leading-*` |
| `--tracking-*` | `tracking-*` |

### Exemplo: typography scale

```css
@theme {
  /* Fontes */
  --font-sans: "Inter", system-ui, sans-serif;
  --font-display: "Playfair Display", serif;

  /* Escala tipográfica modular (1.25 — Major Third) */
  --text-xs: 0.75rem;       /* 12px */
  --text-sm: 0.875rem;      /* 14px */
  --text-base: 1rem;        /* 16px */
  --text-lg: 1.25rem;       /* 20px */
  --text-xl: 1.5625rem;     /* 25px */
  --text-2xl: 1.953rem;     /* 31px */
  --text-3xl: 2.441rem;     /* 39px */
  --text-4xl: 3.052rem;     /* 49px */
  --text-5xl: 3.815rem;     /* 61px */

  /* Line-heights */
  --leading-tight: 1.15;
  --leading-snug: 1.3;
  --leading-normal: 1.5;
  --leading-relaxed: 1.7;
}
```

### Exemplo: spacing system (escala 4px)

```css
@theme {
  --spacing-0: 0;
  --spacing-1: 0.25rem;  /* 4px */
  --spacing-2: 0.5rem;   /* 8px */
  --spacing-3: 0.75rem;  /* 12px */
  --spacing-4: 1rem;     /* 16px */
  --spacing-6: 1.5rem;   /* 24px */
  --spacing-8: 2rem;     /* 32px */
  --spacing-12: 3rem;    /* 48px */
  --spacing-16: 4rem;    /* 64px */
  --spacing-24: 6rem;    /* 96px */
}
```
> Nota: Tailwind v4 já vem com escala default — só sobrescreva se quiser diferente.

### Exemplo: sombras (paleta Reconecta-aware)

Para fundos escuros (padrão do site), sombras tradicionais (preto) somem. Use sombras coloridas:

```css
@theme {
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.3);
  --shadow-md: 0 4px 12px -2px rgb(0 0 0 / 0.4);
  --shadow-lg: 0 10px 30px -5px rgb(0 0 0 / 0.5);

  /* Sombras de "glow" para botões em fundo escuro */
  --shadow-glow-primary: 0 0 20px rgb(107 15 15 / 0.6);
  --shadow-glow-secondary: 0 0 20px rgb(211 17 26 / 0.5);
  --shadow-glow-tertiary: 0 0 20px rgb(238 206 102 / 0.4);
}
```

### Exemplo: raios

```css
@theme {
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 1rem;
  --radius-xl: 1.5rem;
  --radius-pill: 9999px;
}
```

## Workflow após adicionar tokens

1. Edite `src/input.css` adicionando os tokens no bloco `@theme`
2. Rode `npm run build` (ou tenha `npm run dev` rodando em watch)
3. Verifique o `dist/output.css` foi atualizado
4. Use as novas classes geradas no HTML

## Anti-padrões

- ❌ Não duplicar a paleta com outros nomes (ex: criar `--color-vinho-500` para algo que já é `--color-primary-normal`)
- ❌ Não usar valores hardcoded em HTML (`style="color: #6b0f0f"`) — sempre tokens
- ❌ Não criar tokens "one-off" usados em um único lugar — mantém o sistema enxuto
- ❌ Não misturar unidades inconsistentes (sempre `rem` para tipografia/espaçamento, `px` só para borders/shadows finos)

## Quando criar um token novo vs. usar valor inline

**Crie token** se: aparece ≥3 vezes, representa decisão de design intencional, vai mudar junto se a marca mudar.
**Use valor inline** se: é um one-off raro, é específico de um componente experimental.

## Verificação

Depois de qualquer mudança em tokens:
1. Confirme que o build não quebrou (`npm run build` sai sem erros)
2. Abra `index.html` no navegador e verifique que nada visualmente quebrou
3. Se adicionou typography tokens, demonstre todos os tamanhos numa página de teste
