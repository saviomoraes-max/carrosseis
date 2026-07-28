# Métricas do Instagram (Meta Graph API)

Fonte de verdade dos números orgânicos do perfil: views, alcance, likes,
salvamentos, compartilhamentos e tempo de visualização, uma linha por post,
com snapshots ao longo do tempo (dá pra ver a curva de cada peça).

Substitui o CSV incompleto do Business Suite e alimenta a **análise semanal**
(`run-analise-semanal.sh`, LaunchAgent de segunda 07:50).

## Estado do setup (28/jul/2026)

| Passo | Status |
|---|---|
| `~/.config/meta-api/` criado (700) | ✅ |
| Dependência `requests` instalada | ✅ (venv, ver nota abaixo) |
| Pasta de dados `data/metricas-ig/` | ✅ |
| `.gitignore` (venv + token + dados) | ✅ |
| Wrapper `coletar.sh` | ✅ |
| **Token em `~/.config/meta-api/token`** | ⛔ **falta — vem do time** |
| **`coletar_metricas_instagram.py` nesta pasta** | ⛔ **falta — vem do time** |
| `DATA_DIR` do script apontado pra cá | ⛔ depende do script chegar |
| Primeira coleta (`--dias 30`) | ⛔ depende dos dois acima |

## Desvio do passo a passo original (necessário)

O guia manda `pip3 install requests`. **Nesta máquina isso falha**: o Python é o
do Homebrew (3.14.6) e é *externally-managed* (PEP 668) — o pip global recusa
instalar e sugere venv/pipx. Instalar com `--break-system-packages` arriscaria a
instalação do Homebrew.

Solução adotada: venv isolado em `.venv/` aqui dentro, e o wrapper `coletar.sh`
chama o Python dele. Nada muda na forma de usar:

```
./coletar.sh --check-token
./coletar.sh --dias 30
```

## Quando o script e o token chegarem

1. Salvar `coletar_metricas_instagram.py` **nesta pasta**.
2. Colar o token em `~/.config/meta-api/token` (sem quebra de linha extra).
   O wrapper já corrige a permissão pra 600 sozinho se vier frouxa.
3. Ajustar o `DATA_DIR` do script para:
   `/Users/saviomoraes/reconecta/agente-carrosseis/data/metricas-ig`
4. `./coletar.sh --check-token` e depois `./coletar.sh --dias 30`.

O token também será espelhado no **Keychain** (`reconecta-meta`), porque a
integração MCP já commitada (`run-meta-mcp.sh` / `.mcp.json`) lê de lá — mesmo
token, dois consumidores. O arquivo continua existindo porque o script do time
espera ele.

## Limitação da API — regra dura

**Retenção de 3 segundos** e **% de alcance de não-seguidores por post NÃO
existem na Graph API.** Confirmado de forma independente (pesquisa na doc oficial
em jul/2026) e pelo time. O que existe é o breakdown seguidor/não-seguidor **da
conta por dia**, nunca por post.

Esses dois números só saem do app do Instagram, na mão. Toda análise que os
citar deve marcá-los como **"manual no app"** — estimar é proibido.
