-- =====================================================================
-- Agente Social Media RECONECTA — schema do Postgres (Railway)
-- Rodar UMA vez: psql "$DATABASE_URL" -f sql/schema.sql
-- Tudo idempotente (IF NOT EXISTS) — rodar de novo não quebra nada.
-- =====================================================================

-- Token da Meta (Graph API). O workflow meta_token_refresh mantém esta
-- tabela viva; os outros workflows sempre leem o registro mais recente.
CREATE TABLE IF NOT EXISTS meta_token (
  id          SERIAL PRIMARY KEY,
  token       TEXT NOT NULL,
  expires_at  TIMESTAMPTZ,                        -- NULL = token sem validade (System User não-expirável)
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Insights agregados da CONTA. A Meta só guarda 90 dias — por isso
-- persistimos aqui. Métricas semanais entram com sufixo _7d
-- (ex.: reach_7d); série diária de seguidores entra como follower_count.
CREATE TABLE IF NOT EXISTS ig_account_insights_daily (
  metric_date  DATE NOT NULL,
  metric       TEXT NOT NULL,
  value        BIGINT,
  captured_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (metric_date, metric)
);

-- Snapshot semanal por post/reel/carrossel. A Meta guarda insights de
-- mídia por até 2 anos; 1 linha por (mídia, data de captura) permite
-- ver a evolução de um post ao longo das semanas.
CREATE TABLE IF NOT EXISTS ig_media_snapshot (
  ig_media_id             TEXT NOT NULL,
  captured_at             DATE NOT NULL DEFAULT CURRENT_DATE,
  media_type              TEXT,
  media_product_type      TEXT,                   -- FEED | REELS | CAROUSEL_CONTAINER...
  caption                 TEXT,
  permalink               TEXT,
  posted_at               TIMESTAMPTZ,
  views                   BIGINT,
  reach                   BIGINT,
  likes                   BIGINT,
  comments                BIGINT,
  saved                   BIGINT,
  shares                  BIGINT,                 -- "sends" — sinal nº 1 do algoritmo em 2026
  total_interactions      BIGINT,
  reels_avg_watch_time_ms BIGINT,
  raw                     JSONB,                  -- resposta bruta da API, pra não perder nada
  PRIMARY KEY (ig_media_id, captured_at)
);

-- Candidatos de tendência coletados toda sexta pelas fontes RSS
-- gratuitas. A skill tendencias-research consome daqui (status novo)
-- e aplica o filtro de relevância do nicho.
CREATE TABLE IF NOT EXISTS trends_candidates (
  id           SERIAL PRIMARY KEY,
  source       TEXT NOT NULL,                     -- google_trends_br | google_news | g1 | uol | reddit_brasil | x_getdaytrends
  title        TEXT NOT NULL,
  url          TEXT,
  extra        JSONB,
  captured_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  status       TEXT NOT NULL DEFAULT 'novo',      -- novo | aprovado | descartado | usado
  UNIQUE (source, title)
);

-- Inspirações virais garimpadas pela skill social-media-semanal
-- (links de posts/reels/anúncios de referência). O UNIQUE em url
-- evita repetir a mesma inspiração em semanas seguintes.
CREATE TABLE IF NOT EXISTS viral_inspirations (
  id        SERIAL PRIMARY KEY,
  url       TEXT NOT NULL UNIQUE,
  title     TEXT,
  why       TEXT,                                 -- por que inspira (gancho/formato/ângulo)
  niche     TEXT,                                 -- nicho | adjacente | fora_do_nicho | ad_library
  found_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  used      BOOLEAN NOT NULL DEFAULT false
);
