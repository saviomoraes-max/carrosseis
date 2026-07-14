# Agente Social Media RECONECTA

Agente semanal que analisa a performance orgânica do Instagram, garimpa tendências BR e traz inspiração de posts virais com links — **100% gratuito, só rotas oficiais/de risco ~nulo**.

Decisão de arquitetura fundamentada na pesquisa de 13/07/2026 (verificação adversarial, tudo com fonte):
- Vault: `30 Resources/Agente Social Media — pesquisa de rotas de métricas IG (2026-07-13).md`
- Artifact: https://claude.ai/code/artifact/b1c043c6-7e4e-4664-999e-c710941c673f

**Fora de escopo (decisão de 13/07/2026):** monitoramento de concorrentes (adiado), qualquer ferramenta paga, scraping logado (risco de ban na conta).

## Arquitetura

```
Meta Graph API (oficial, grátis)          Fontes RSS BR (grátis)
        │                                        │
        ▼                                        ▼
n8n (workflows.reconectaoficial.com) ──► Postgres (Railway)
   3 workflows semanais                          │
                                                 ▼
                            Claude Code: skill social-media-semanal
                            (relatório + inspiração viral com links)
```

O Claude Code **nunca fala com a Meta** no fluxo semanal — só lê o Postgres. O token não vive no Mac.

A skill `social-media-semanal` funciona em **dois modos**:
- **Completo**: com o Postgres populado pelos workflows (métricas + tendências + inspiração).
- **Degradado (já funciona hoje)**: sem token/DB, busca tendências ao vivo nas mesmas fontes RSS e faz o garimpo de inspiração viral — dá pra usar antes de qualquer setup.

## Estrutura

| Arquivo | O que é |
|---|---|
| `sql/schema.sql` | Tabelas do Postgres (idempotente, rodar 1x) |
| `n8n/meta_token_refresh.json` | Checa diariamente a validade do token e renova quando faltam ≤15 dias |
| `n8n/ig_metricas_semanais.json` | Segunda 07h: insights da conta + snapshot por post → Postgres |
| `n8n/tendencias_semanais.json` | Sexta 08h: 6 fontes de tendência BR → `trends_candidates` |
| `.env.example` | Modelo do `.env` local usado pela skill (o real nunca entra no git) |
| Skill | `~/.claude/skills/social-media-semanal/SKILL.md` |

## Setup (ordem exata)

### Parte humana — só você/Jardel podem fazer (~2-3h)

1. **Criar app na Meta**: [developers.facebook.com](https://developers.facebook.com) → Create App → tipo **Business** → adicionar o produto **Instagram** pela rota *Facebook Login for Business*. Usar a conta Meta que já roda os anúncios. Pra puxar dados **só da própria conta**, Standard Access basta — **não** precisa de App Review ([fonte](https://developers.facebook.com/docs/instagram-platform/overview/)).
2. **Pré-requisito**: a conta IG profissional precisa estar vinculada à Página do Facebook (já deve estar, por causa dos ads).
3. **Descobrir o IG_USER_ID**: no [Graph API Explorer](https://developers.facebook.com/tools/explorer/), com o app selecionado: `GET /me/accounts` → pegar o id da Página → `GET /{page-id}?fields=instagram_business_account` → o id retornado é o `IG_USER_ID`.
4. **Gerar o token** (Business Manager → Configurações do negócio → Usuários → Usuários do sistema):
   - Criar um System User (admin não é necessário; employee basta).
   - Atribuir a ele a Página + a conta do Instagram.
   - Instalar o app criado no passo 1 e gerar token com os escopos: `instagram_basic`, `instagram_manage_insights`, `pages_read_engagement`, `pages_show_list`, `business_management`.
   - Se a opção "nunca expira" aparecer, ótimo. Se só vier com 60 dias, tudo bem — o workflow de refresh cuida disso.
5. **Guardar credenciais**:
   - No n8n (env vars do container/instância): `META_APP_ID`, `META_APP_SECRET`, `IG_USER_ID`.
   - No Mac: copiar `.env.example` → `.env` e preencher `DATABASE_URL` (Railway → serviço Postgres → Connect) + os mesmos 3 valores.

### Parte técnica — qualquer sessão do Claude Code executa depois disso (~2-3h)

6. **Criar as tabelas**: `psql "$DATABASE_URL" -f sql/schema.sql`
7. **Inserir o token inicial**: `INSERT INTO meta_token (token, expires_at) VALUES ('<TOKEN>', now() + interval '60 days');` — usar `NULL` no `expires_at` se o token for não-expirável.
8. **Importar os 3 JSONs** no n8n (menu do workflow → *Import from file*). Depois de importar, em cada node do Postgres, **re-selecionar a credencial** "Postgres Railway" (o JSON traz um placeholder).
9. **Conferir os nodes de HTTP** após o import (os JSONs foram escritos à mão; parâmetro fora do lugar se ajusta na UI em 1 min).
10. **Configurar o Error Workflow padrão** da casa em cada workflow (Settings → Error Workflow) — regra do projeto: todo workflow tem tratamento de erro com notificação.
11. **Testar manualmente** (`Execute workflow`) nesta ordem: tendências → métricas → refresh de token. Validar no Postgres: `SELECT source, count(*) FROM trends_candidates GROUP BY 1;` e `SELECT count(*) FROM ig_media_snapshot;`
    - **Teste real do ramo de renovação** (importante — a troca de token de System User via `fb_exchange_token` não é documentada pela Meta; melhor descobrir agora do que no dia 45): `UPDATE meta_token SET expires_at = now() + interval '10 days';` → Execute workflow → conferir que apareceu linha nova em `meta_token` com validade estendida. O próprio insert corrige o estado.
12. **Backfill histórico (1x)**: o node "Buscar Mídias Recentes" não pagina sozinho — reexecutar com `limit=100` traz sempre as mesmas 100 mídias. Pedir pro Claude Code rodar um script pontual que siga `paging.cursors.after` até 2 anos atrás e grave direto no Postgres (ou, na mão: adicionar temporariamente o query param `after` com o cursor de cada página). A Meta guarda insights de mídia por até 2 anos — o que não for capturado agora não se recupera depois.
13. **Ativar os 3 workflows.**

## Regras que os workflows já respeitam (CLAUDE.md)

- Nenhum ID hardcoded — `IG_USER_ID`/`META_APP_ID`/`META_APP_SECRET` vêm de env vars.
- Delay de 1s no loop de mídias (rate limit).
- Fontes de tendência com `onError: continue` — se uma fonte RSS sumir, as outras seguem (degradação graciosa).
- Segredos nunca aparecem em URL — token vai por header `Authorization: Bearer`; o refresh OAuth vai por body de POST.

## Notas de dados

- **`views` é a métrica atual** — `impressions` foi deprecada em abr/2025. Em carrossel, `views` conta cada card.
- **`shares` = "sends"**, o sinal nº 1 do algoritmo em 2026. O ranking do relatório usa shares/reach como métrica-mestra.
- A Meta retém insights de conta por **90 dias** e de mídia por **até 2 anos** — o Postgres é a memória permanente.
- Nomes de métricas ficam em Code nodes (fáceis de editar) porque a Meta muda nomes unilateralmente.
- **Stories ficam fora da coleta** (decisão de escopo): `GET /{ig-user-id}/media` não retorna STORY — precisaria do edge `/stories` com coleta diária (janela de 24h) e métricas próprias. Se um dia stories virarem prioridade, é um 4º workflow.
