---
name: carrossel-tweet
description: Faz o carrossel estilo "print de tweet" do @anadareconecta (um tweet por card, fundo branco, avatar e selo da Ana) a partir de um Reel campeão dela — escolhe o Reel, escreve os 8 cards e a legenda, monta capa e prova, renderiza com o engine_tweet.py e exporta com o nome final. Acionar quando alguém pedir "post estilo twitter", "carrossel de tweet", "formato tweet", "tweet das 12h", ou quiser transformar um Reel da Ana em carrossel de tweets.
---

# Carrossel estilo Twitter (@anadareconecta)

Formato que levou o alcance dos carrosséis de ~1.100 para 2,6–10,4 mil (Publer, 26/10/2026).
Os que mais foram ENVIADOS (2,8–3,4% de envios/alcance) entregam **técnica + frase pronta**.
Os de história ou opinião ficaram em 0,4–0,9%. Tudo aqui parte disso.

Exemplo canônico: **SEM44/AD004 "Textão da Consulta Antecipada"** (28/10/2026).

## Ferramentas

| O quê | Onde |
|---|---|
| Comando do formato (novo / render / exportar) | `carrosseis/_template/tweet/tweet.py` |
| Motor (HTML → PNG 1080×1350, Inter) | `carrosseis/_template/html-engine/engine_tweet.py` |
| Avatar da Ana (foto de perfil real) | `carrosseis/_template/tweet/avatar-ana.jpg` |
| Detector de punchline de comparação | `agente-carrosseis/vicio_comparacao.py` |
| Detector de legenda repetida | `agente-carrosseis/legenda_padrao.py` |
| Print de prova já usado? | `agente-carrosseis/prints_usados.py <print.png>` |
| Formas de CTA na legenda | `agente-carrosseis/banco-cta-legenda.md` |
| Regras completas | `agente-carrosseis/checklist-producao.md` (fim) e `checklist-legenda.md` (topo) |

Instalação, uma vez por máquina: `pip install playwright pillow && playwright install chromium`.
O `ffmpeg` só é necessário se algum card tiver vídeo.

**Pasta do post:** no SSD (`/Volumes/SSD kenipe/estáticos/novos/SEM{xx}/`) se ele estiver montado.
Sem o SSD, vai para `./producao/SEM{xx}/` na raiz do repo, que é gitignorada e fica só na sua máquina.
O `tweet.py` decide sozinho.

## Passo a passo

### 1. Escolher o tema: um Reel da Ana que já performou
- Ordenar os Reels do @anadareconecta por **envios** (compartilhamentos), não por curtida.
  - Fonte no Mac do Sávio: `agente-carrosseis/data/metricas-ig/historico.csv`.
  - Sem esse arquivo: Insights do Instagram ou Publer.
- Preferir Reel que ensina uma **técnica com frase pronta** (atendimento, objeção, follow up, consulta).
- Checar se o Reel já virou carrossel: procurar o código dele (`DeeoUQACRvG`) nos `copy.md` / `ORIGEM.txt` das últimas semanas.
  - Se já virou, só reusar declarando no `copy.md`.
- Transcrever o Reel e trabalhar em cima da fala dela.
  - Verbatim sempre que der: o tweet é a Ana falando.

### 2. Criar a pasta
```bash
python3 carrosseis/_template/tweet/tweet.py novo "Título do Post" --data 2026-11-04 --hora 12:00
```
- Cria `SEM{xx}/AD{nnn} - Título Do Post Twitter/` com:
  - o `tweets.json` de 8 cards, com os textos ainda marcados ESCREVER;
  - o avatar;
  - o `copy.md`, o `legenda.txt` e o `ORIGEM.txt`.
- O AD é o próximo livre da semana. **Nunca reaproveitar pasta de post já exportado**: post novo = pasta nova + AD novo.
- A linha de data/hora embaixo de cada tweet sai de `--data`/`--hora`. Use a hora real em que o post vai ao ar (na grade, o tweet sai às 12h).

### 3. Escrever os 8 cards (`tweets.json`, campo `"t"`)
Esqueleto (no máximo 8 cards, contando capa, prova e CTA):

1. **Capa (com foto).** A frase que para o dedo. **Sem ponto final** (vírgula pode). Curta, porque a foto ocupa metade do card.
2. **O caso em UM card.** O que aconteceu e a frase que o processo responde. História é só gatilho (Ana Luiza, 26/10).
3. a 5. **O processo.** O que a comercial ou a doutora faz e por quê, passo a passo. Pelo menos um card com a **frase pronta colável**.
6. **A objeção da leitora** ("Ai, Ana, mas e se…?") e a resposta.
7. **Prova:** "Olha o que uma aluna mandou no grupo:" + o print.
8. **CTA SUPERCASO** (texto já vem no esqueleto).

Regras de texto (cada uma veio de reprovação real):
- **Zero punchline de comparação**, nem verbatim: "não é X, é Y", "X, nunca Y", "tem quem X, tem quem Y", "para de X e passa a Y". Afirmar direto. O render acusa.
- Sempre "harmonização facial" (nunca HOF/orofacial).
- Nada de curtida, retweet ou visualização no card: seria número inventado.
- Nunca inventar número ou caso: dado sem fonte não entra.
- Tweet comprido estoura a faixa segura: o motor avisa "ENCURTAR O TWEET". Corte texto, nunca diminua a fonte.
- **Post de isca** (que distribui material, ex.: Framework 715): cada card fala do **conceito** da etapa, nunca do roteiro/frase. Ali a prova é print de resultado.
- **Frase pronta em tweet de técnica:** segue o dado do Publer. A Ana pediu "sem roteiro" para post de isca; ainda está em aberto se a regra vale para tweet. Na dúvida, perguntar ao Sávio.

### 4. Imagens (`img/`)
**Capa (`img/capa.png`)** = foto de **atriz, influenciadora ou meme conhecido** cuja expressão ou cena conversa com a frase. Não usar imagem de IA, a não ser que o Sávio peça.
- Recortar paisagem (ex.: 2000×870) para a foto não empurrar o texto para fora.
- A mesma imagem não repete na mesma semana.
- **Vetos:** nada sensual e nenhuma criança no quadro (nem ao fundo). A Ana nunca de blazer branco.

**Prova (`img/prova-1.png`)** = print real de aluna (Slack #mais-dos-melhores-depoimentos ou acervo `prova-resultado`).
- Recortar grande, só a conversa, **sem o avatar da aluna**.
- Borrar telefone, CPF/CNPJ, número de controle e sobrenome. O valor em R$ fica.
- `python3 agente-carrosseis/prints_usados.py img/prova-1.png` precisa dizer que é inédito.
  - Sem o SSD, ele só enxerga os seus posts em `./producao`. Pergunte a quem tem o SSD.

**Card com vídeo** (opcional): `"video": "img/x.mp4", "poster": "img/x.jpg"` no tweet. Sai `slide_N.mp4`, com os cantos redondos e sem áudio.

### 5. Legenda (`legenda.txt`)
- No jeito dos Reels da Ana: curta (1 a 3 blocos), fala de WhatsApp ("cê", "Bjo", "uai"), 1–2 emojis dela (🫪 ❤️ 🤌🏼).
- Pergunta direta ou brincadeira.
- **Um CTA de palavra só.** A promessa do SUPERCASO não muda (time analisa o cenário, 10 a 60 pacientes novos por mês). A **frase muda em toda legenda**: girar as formas do `banco-cta-legenda.md`.
- Nada de "salva e manda pra colega", parágrafo-índice ("nos slides…") ou crédito de imagem.

Exemplo (AD004):
> Amor ao próximo ❤️
>
> Quando chegar um textão perguntando quem você pensa que é pra cobrar consulta antecipada, uma frase resolve. Copia ela e deixa guardadinha aí.
>
> Agora, se o seu atendimento tá perdendo paciente e cê não sabe onde, escreve SUPERCASO aqui embaixo. Meu time descobre com você e monta o caminho pros 10 a 60 novos por mês.

### 6. Render
```bash
python3 carrosseis/_template/tweet/tweet.py render "<pasta do post>"
```
- Recusa enquanto houver card com ESCREVER.
- Gera `slides/slide_N.png` e roda os detectores:
  - faixa segura;
  - máximo de 8 cards;
  - capa com foto;
  - punchline de comparação nos cards e na legenda;
  - legenda repetida em relação às últimas 3 semanas.
- **Aviso = corrigir e renderizar de novo.**
- Render limpo não basta: **abrir cada slide, um por um**, e conferir no olho:
  - foto sem criança, sem conteúdo sensual e sem logo de terceiro;
  - print anonimizado;
  - texto sem corte.

### 7. Exportar
```bash
python3 carrosseis/_template/tweet/tweet.py exportar "<pasta do post>"
```
- Gera `[DD] [SS] [ADnnn_N] - Título.png` na raiz da pasta, mais o `_folha.png` com os 8 cards lado a lado.
- Recusa se o post já foi exportado: post exportado é imutável.
- Preencher o `copy.md` com:
  - fonte do Reel (link, alcance, envios);
  - origem da foto da capa e da prova;
  - o texto de cada card.
- Usar o AD004 da SEM44 como modelo.

### 8. Entregar
- Mandar para o Sávio aprovar: a `_folha.png` + a `legenda.txt`.
- **Não agendar nem postar** sem o ok explícito dele.
