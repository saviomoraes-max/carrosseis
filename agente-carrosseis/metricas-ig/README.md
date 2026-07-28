# Métricas do Instagram — dois caminhos, um formato

Tudo desemboca em `../data/metricas-ig/historico.csv`: **uma linha por post por
snapshot**. Rodar de novo noutro dia não sobrescreve, adiciona — é assim que se
enxerga a curva de cada peça (o carrossel que continua sendo salvo na segunda
semana aparece aqui).

## Caminho A — export do Business Suite (SEM TOKEN, é o padrão)

O export de **Conteúdo** do Meta Business Suite já traz tudo que a análise usa:
Visualizações, Alcance, Curtidas, Compartilhamentos, Seguimentos, Comentários,
Salvamentos, com `Data = Total` (acumulado de vida do post).

```
./importar_business_suite.py ~/Downloads/export.csv
./importar_business_suite.py ~/Downloads/export.csv --conta oleonardorosso
```

O export costuma vir com mais de uma conta dentro (o de jun/2025→jun/2026 tinha
`oleonardorosso` com 264 posts + `draalinedamazio` e `mentoriareconecta` com 1
post e alcance 0 cada). A coluna `conta` no histórico resolve; `--conta` filtra.

**Custo real desse caminho: exportar de novo quando a janela vencer.** O export
que estava no repo parava em 29/06/2026 — não era incompleto, era velho.

## Caminho B — Graph API (precisa de token, automatiza)

```
./coletar_metricas_ig.py --check-token
./coletar_metricas_ig.py --dias 30
```

Zero dependência (stdlib pura — o Python daqui é Homebrew/PEP 668). Token vem do
Keychain `reconecta-meta/insights-token`, com fallback em `~/.config/meta-api/token`
(600); vai por header, nunca em URL, argv ou log. Descobre a conta IG sozinho.

**O que o token compra:** não precisar exportar na mão toda semana, mais
`profile_visits` e o watch time dos Reels. **Não compra métrica nova nenhuma**
que decida pauta — alcance, compartilhamento e salvamento já vêm no export.

Gerar o token (Explorer, ~1h de validade, bom pra testar):
developers.facebook.com/tools/explorer → app da RECONECTA → *Get User Access
Token* → `instagram_basic`, `instagram_manage_insights`, `pages_show_list`,
`pages_read_engagement` → *Generate*. Guardar sem passar pelo histórico do shell:

```
security add-generic-password -s reconecta-meta -a insights-token -U -w
```

Permanente: business.facebook.com → Configurações do negócio → Usuários do
sistema → Gerar token → expiração "Nunca", mesmos escopos.

## O script do time

`coletar.sh` é o wrapper do `coletar_metricas_instagram.py` (script oficial do
Jardel, que usa `requests` — daí o `.venv/` aqui). Quando ele chegar, os dois
convivem: mesmo destino, mesmo formato.

## Limitação que nenhum caminho resolve

**Retenção de 3 segundos** e **% de alcance de não-seguidores por post** não
existem na Graph API nem no export. O breakdown seguidor/não-seguidor só existe
no nível da CONTA por dia. Confirmado na doc oficial (jul/2026) e pelo time.

Esses dois só saem do app do Instagram, na mão, e toda análise que os citar tem
que marcá-los como **"manual no app"**. Estimar é proibido.
