# Design System RECONECTA

Um lugar só pra identidade da marca. Se você precisa montar uma apresentação e
quer que ela pareça nossa, é aqui que começa.

![Os 8 layouts](pptx/preview.png)

---

## Começando (3 passos, uma vez só)

**1. Instale as fontes.** No Terminal, dentro da pasta do repo:

```bash
bash design-system/instalar-fontes.sh
```

**2. Feche e reabra o PowerPoint** (ou o Keynote). Programa aberto não enxerga
fonte nova.

**3. Abra o modelo e salve com outro nome:**

```
design-system/pptx/RECONECTA-modelo.pptx
```

Pronto. Agora é só escrever.

---

## A regra que faz tudo funcionar

> **Você não escolhe cor nem fonte. Você escolhe o tipo de slide e digita o texto.**

O design já está dentro de cada layout. Se você trocar a cor de uma palavra na
mão, quebrou o sistema — e o próximo que abrir o arquivo não vai saber por quê.

Pra trocar de layout num slide: **Início → Layout** e escolhe da lista.

---

## Qual layout eu uso?

| Se você quer... | Use |
|---|---|
| abrir a apresentação | **Capa** |
| avisar que começou uma parte nova | **Abertura de seção** |
| que uma frase fique sozinha na tela e pese | **Afirmação** |
| mostrar um número e explicar o que ele significa | **Dado** |
| listar 3 ou 4 coisas curtas | **Lista** |
| mostrar antes e depois lado a lado | **Comparação** |
| uma imagem grande com título por cima | **Foto** |
| fechar com a única coisa que precisa ficar | **Encerramento** |
| montar algo que não se encaixa em nada acima | **Livre** |

O arquivo já vem com um slide de exemplo de cada um, preenchido. Olhe, entenda,
apague os que não for usar.

---

## Coisas que quebram (e como evitar)

**A fonte aparece errada / vira Arial.**
As fontes não estão instaladas nessa máquina. Volte no passo 1.

**Vou usar no Google Slides.**
Funciona. Suba o `.pptx` no Drive e abra com o Slides — Archivo Black e Figtree
são do catálogo do Google, então aparecem normalmente. Foi por isso que a
apresentação usa essas duas, e não as fontes do carrossel.

**O texto não cabe no slide.**
Não diminua a fonte. **Corte a copy.** Um slide com texto miúdo não é um slide
cheio, é um slide ilegível. Se não couber, vira dois slides.

**Quero destacar uma palavra.**
Use cor, nunca itálico e nunca um peso mais fino. E só um vermelho por slide —
dois destaques na mesma tela se cancelam.

---

## As duas pistas de tipografia

A marca tem duas famílias porque tem dois destinos diferentes:

| | Display | Corpo | Rótulo |
|---|---|---|---|
| **licenciada** — o que a gente renderiza (carrossel, PDF) | Dx Monstral | Grift | Inter |
| **google** — o que o time edita (PPTX, Slides) | Archivo Black | Figtree | Inter |

Mesmas cores, mesma escala, mesmos layouts nas duas. Só muda a família conforme
onde o arquivo vai viver.

As Google são OFL e estão neste repo. As licenciadas são comerciais e
**não podem ser redistribuídas** — confira os seats antes de instalar em máquina
nova.

---

## Pra quem mexe no sistema

```
design-system/
├── core/tokens.json        ← a fonte de verdade. Mudou aqui, muda em tudo.
├── pptx/build_potx.py      ← gera o modelo lendo os tokens (zero cor hardcoded)
├── pptx/preview.png        ← a imagem lá de cima; regerar quando mudar layout
├── fontes/google/          ← as OFL + as licenças (manter sempre juntas)
└── instalar-fontes.sh
```

Regerar o modelo:

```bash
./.venv-ds/bin/python design-system/pptx/build_potx.py
```

**Antes de commitar mudança de layout:** exporte em PDF e olhe os 8 slides. Um
layout quebrado aqui se espalha por todo deck que o time fizer depois.

Cor nova, tamanho novo ou regra nova entram no `tokens.json` — nunca direto no
`build_potx.py`, nunca direto num slide.
