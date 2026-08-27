# GRADE EDITORIAL v2 — aprovada pelo Sávio em 27/ago/26

Substitui a grade "1 CONVERSA + 1 APLICAÇÃO + 1 ISCA por dia" (SEM35).
Origem: benchmark de 27/ago (nosso perfil × @brandsdecoded__ × @vinci.society),
relatório em https://claude.ai/code/artifact/d1be374e-f17b-4d55-b4ff-882267b06c06
e corpus baixado em `/Volumes/SSD kenipe/inbox/benchmark/instagram/`.

Diagnóstico que motivou: agosto virou 100% aula interna da metodologia com CTA de
DM em todo post → mediana de alcance caiu de 12.829 (maio) pra 2.678 (agosto) com o
MESMO volume. Nossos hits (110k, 82k, 73k, ritual do abraço) falam do mundo que a
audiência vive, não do método que a casa ensina.

## As quatro franquias

| Slot | Freq. | O quê | Molde |
|---|---|---|---|
| **A — Raio-X** (série nomeada, ep. numerado) | 2x/sem | Análise de caso REAL e NOMEADO do mundo da beleza/estética (marca, clínica, influencer, celebridade) | brandsdecoded: 10 slides cheios, capa com pessoa real + curiosity gap + número, análise INTEIRA no post, fecho em TESE sem pedido |
| **B — Trend quente** | 2x/sem | Momento cultural de ≤72h (radar diário vira slot principal) com ponte declarada pro negócio da clínica | vinci: capa foto do momento + pergunta polêmica, humor no slide 2, gancho explícito entre slides, fecho em PERGUNTA DE OPINIÃO |
| **C — Comunidade** | 1x/sem | Cena emocional que toda clínica vive, contada como história (linhagem ritual do abraço) | Storytelling ST-01..20, prova casada por punch |
| **D — Conversão** | 1–2x/sem | Isca ou SUPERCASO, SEMPRE no dia seguinte a um post que provou alcance (audiência aquecida), nunca nascendo BOFU em feed frio | Padrão atual de isca/aplicação, com prova |

## Designs (atualizado 27/ago)

- Rotação vigente: **A / D / C**. O **design B está ARQUIVADO** (ordem do Sávio,
  27/ago) — `hero_b` continua no engine mas não entra em post novo.
- **Design D (dossiê)**, derivado do design system do evento (pasta
  `inbox/Reconecta Design System`): layout INVERTIDO aprovado em 27/ago — chrome no
  topo (ponto REC + HUD + barcode + slug + contador), bloco kicker + headline + sub
  ancorado embaixo com ~140px de respiro; TT Modernoir (display) + Space Mono
  (chrome) + Inter (sub); Pearl/Gold sobre Obsidian; vermelho SÓ no ponto REC.
  No Raio-X o chrome é da série (CASO Nº, PROVA Nº); em post comum, generaliza
  (HUD = marcação da semana, kicker = editoria). Foto: card de anúncio com texto
  embutido NUNCA vira fundo (nem cartão — cropar o texto fora resolve; rótulo de
  embalagem pequeno é aceitável); zona inferior precisa aceitar o bloco de texto.
  **Slides internos levam CARTÃO RETANGULAR de foto** (campo `image` em text/list,
  altura via `image_h`, default 420) quando o conteúdo pede: a foto CONVERSA com o
  que o slide diz (pedido do Sávio 27/ago: "pouca imagem pra muito texto"). Lista
  de 3 itens raramente comporta cartão (o guarda de overflow acusa). Chrome tem
  véu próprio no topo pra foto clara.
- **Fonte TT Modernoir: decisão do Sávio em 27/ago = publicar com a TRIAL por ora**
  e trocar quando licenciar. Revisitar na primeira renovação de mês.

## Regras da grade

- **10 slides** como padrão nas franquias A e B (retenção por impressão é o sinal
  que o algoritmo mais paga). C e D podem seguir 6–8.
- **Volume:** 5–7 posts/semana (1 por dia + o slot D flutuante). Menos posts,
  mais estatura por post.
- **Régua de decisão:** shares/alcance e saves/alcance em **D+14** — nunca curtida
  em D+1. Meta de retomada: s/r ≥ 1,2% sustentado (nível maio–junho).
- **Slot D ancora no dado:** o post de conversão entra quando um post da semana
  mostra tração relativa clara sobre os irmãos do dia/da véspera.
- **Franquia A e doutrina:** caso de fora analisado = debate/análise DECLARADA;
  nunca prescrever conduta que a metodologia não ensina (doutrina-fixa §5–§6).
  Todo caso nomeado passa por VERIFICAÇÃO EM FONTE antes da escrita (zero achismo).
- **O que não muda:** prova em todo post (25/ago), voz sem bafo de IA, harmonização
  facial por extenso, capas sem sombra, validação de design/estrutura com o Sávio.

## Ritual de melhoria contínua (pedido do Sávio, 27/ago: "sempre busque por melhorias constantes assim")

- **Toda segunda** (análise semanal já existente): ler s/r e saves/r maduros (D+14),
  decidir o que dobra e o que corta na semana seguinte, por franquia.
- **Primeira segunda do mês:** re-baixar o benchmark (gallery-dl, mesmos perfis +
  candidatos novos), comparar nossas franquias com as referências e propor ajustes.
  Proposta → OK do Sávio → produção. Nunca ajuste silencioso.
