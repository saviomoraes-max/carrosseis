#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coletor de métricas orgânicas do Instagram RECONECTA (Meta Graph API v25.0 —
a mais nova em produção, verificada por sonda em 28/jul/2026; v26 ainda não existe).

Grava historico.csv com UMA LINHA POR POST POR SNAPSHOT: rodar de novo noutro dia
não sobrescreve nada, adiciona um snapshot novo. Assim dá pra ver a CURVA de cada
peça (o carrossel que continua sendo salvo na segunda semana aparece aqui).

Zero dependência externa (só stdlib) — o Python desta máquina é o do Homebrew e é
externally-managed (PEP 668), então instalar pacote global é bloqueado.

Token (nesta ordem de preferência):
  1. Keychain: security find-generic-password -s reconecta-meta -a insights-token
  2. Arquivo:  ~/.config/meta-api/token   (chmod 600)
Nunca no repo, nunca no argv, nunca no log.

Uso:
  ./coletar_metricas_ig.py --check-token     # valida token, escopos e qual conta enxerga
  ./coletar_metricas_ig.py --dias 30         # coleta os posts dos últimos 30 dias

LIMITAÇÃO DURA DA API (confirmada na doc oficial e pelo time, jul/2026):
retenção de 3 segundos e % de alcance de NÃO-SEGUIDORES **por post** NÃO existem
na Graph API. O breakdown seguidor/não-seguidor só existe no nível da CONTA por
dia. Esses dois números só saem do app na mão — este script nunca os estima.
"""

import argparse
import csv
import json
import os
import ssl
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

API = "https://graph.facebook.com/v25.0"
BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE), "data", "metricas-ig")
CSV_PATH = os.path.join(DATA_DIR, "historico.csv")

# métricas por tipo de mídia — a API recusa a chamada inteira se pedir uma que o
# tipo não suporta, então cada família tem sua lista.
METRICAS_FEED = ["views", "reach", "saved", "shares", "likes", "comments",
                 "total_interactions", "follows", "profile_visits"]
METRICAS_REELS = ["views", "reach", "saved", "shares", "likes", "comments",
                  "total_interactions", "follows", "profile_visits",
                  "ig_reels_avg_watch_time", "ig_reels_video_view_total_time"]

COLUNAS = [
    "snapshot_em", "post_id", "publicado_em", "tipo", "permalink", "legenda_inicio",
    "views", "reach", "saved", "shares", "likes", "comments",
    "total_interactions", "follows", "profile_visits",
    "reels_avg_watch_time_ms", "reels_total_watch_time_ms",
    "s_por_r", "saves_por_r",
]


def ler_token():
    """Keychain vence o arquivo. Devolve (token, origem) ou sai com erro claro."""
    try:
        r = subprocess.run(
            ["security", "find-generic-password", "-s", "reconecta-meta",
             "-a", "insights-token", "-w"],
            capture_output=True, text=True, timeout=10)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip(), "Keychain (reconecta-meta/insights-token)"
    except Exception:
        pass

    caminho = os.path.expanduser("~/.config/meta-api/token")
    if os.path.isfile(caminho):
        # se a permissão vier frouxa, apertar em vez de só avisar
        if (os.stat(caminho).st_mode & 0o777) != 0o600:
            os.chmod(caminho, 0o600)
            print(f"aviso: permissão de {caminho} corrigida para 600", file=sys.stderr)
        with open(caminho) as f:
            token = f.read().strip()
        if token:
            return token, caminho

    sys.exit(
        "ERRO: nenhum token encontrado.\n"
        "  Keychain: security add-generic-password -s reconecta-meta "
        "-a insights-token -w 'TOKEN' -U\n"
        "  ou arquivo: ~/.config/meta-api/token (chmod 600)")


def get(path, token, **params):
    """GET na Graph API. Token vai por header (não vaza em log de URL)."""
    params = {k: v for k, v in params.items() if v is not None}
    url = f"{API}/{path.lstrip('/')}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=45, context=ctx) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        corpo = e.read().decode(errors="replace")
        try:
            erro = json.loads(corpo).get("error", {})
            raise RuntimeError(
                f"Graph API {e.code}: {erro.get('message', corpo)} "
                f"(type={erro.get('type')}, code={erro.get('code')})") from None
        except json.JSONDecodeError:
            raise RuntimeError(f"Graph API {e.code}: {corpo[:300]}") from None


def descobrir_conta(token):
    """Acha o IG Business Account. Keychain > páginas do usuário."""
    try:
        r = subprocess.run(
            ["security", "find-generic-password", "-s", "reconecta-meta",
             "-a", "ig-user-id", "-w"],
            capture_output=True, text=True, timeout=10)
        if r.returncode == 0 and r.stdout.strip():
            ig_id = r.stdout.strip()
            info = get(ig_id, token, fields="username,followers_count,media_count")
            return ig_id, info
    except Exception:
        pass

    paginas = get("me/accounts", token,
                  fields="name,instagram_business_account{id,username,"
                         "followers_count,media_count}", limit=100)
    achadas = [p for p in paginas.get("data", []) if p.get("instagram_business_account")]
    if not achadas:
        sys.exit("ERRO: o token não enxerga nenhuma conta IG Business.\n"
                 "  Confira: a conta é Business/Criador, está ligada a uma Página, e o\n"
                 "  token tem instagram_basic + instagram_manage_insights + pages_show_list.")
    if len(achadas) > 1:
        print("Mais de uma conta IG visível — usando a primeira:", file=sys.stderr)
        for p in achadas:
            iba = p["instagram_business_account"]
            print(f"  · @{iba.get('username')} (página: {p.get('name')})", file=sys.stderr)
    iba = achadas[0]["instagram_business_account"]
    return iba["id"], iba


def check_token(token, origem):
    print(f"Token lido de: {origem}")
    dbg = get("debug_token", token, input_token=token).get("data", {})
    validade = dbg.get("expires_at", 0)
    if validade == 0:
        quando = "nunca expira"
    else:
        dt = datetime.fromtimestamp(validade, tz=timezone.utc).astimezone()
        dias = (dt - datetime.now(tz=dt.tzinfo)).days
        quando = f"expira em {dt:%d/%m/%Y %H:%M} ({dias} dias)"
    print(f"Válido: {dbg.get('is_valid')} · {quando} · tipo: {dbg.get('type')}")

    escopos = set(dbg.get("scopes", []))
    print(f"Escopos: {', '.join(sorted(escopos)) or '(nenhum)'}")
    faltando = {"instagram_basic", "instagram_manage_insights"} - escopos
    if faltando:
        print(f"⚠ FALTA escopo obrigatório: {', '.join(sorted(faltando))}", file=sys.stderr)

    ig_id, info = descobrir_conta(token)
    print(f"Conta IG: @{info.get('username')} (id {ig_id}) · "
          f"{info.get('followers_count', '?')} seguidores · "
          f"{info.get('media_count', '?')} posts")
    print("OK — pronto pra coletar.")


def insights_do_post(token, post):
    """Insights de um post. Se a API recusar alguma métrica, tenta sem as opcionais."""
    tipo = post.get("media_product_type") or post.get("media_type") or ""
    metricas = METRICAS_REELS if tipo.upper() == "REELS" else METRICAS_FEED
    for tentativa in (metricas, [m for m in metricas if m not in
                                 ("follows", "profile_visits", "views")]):
        try:
            r = get(f"{post['id']}/insights", token, metric=",".join(tentativa))
            valores = {}
            for m in r.get("data", []):
                v = m.get("values", [{}])[0].get("value")
                valores[m["name"]] = v
            return valores
        except RuntimeError as e:
            ultimo = str(e)
            continue
    print(f"  ⚠ sem insights para {post['id']}: {ultimo[:140]}", file=sys.stderr)
    return {}


def coletar(token, dias):
    os.makedirs(DATA_DIR, exist_ok=True)
    ig_id, info = descobrir_conta(token)
    corte = datetime.now(timezone.utc) - timedelta(days=dias)
    agora = datetime.now().astimezone().isoformat(timespec="seconds")
    print(f"Conta @{info.get('username')} · coletando posts desde {corte:%d/%m/%Y}")

    posts, url_proxima = [], None
    campos = ("id,caption,media_type,media_product_type,permalink,timestamp,"
              "like_count,comments_count")
    pagina = get(f"{ig_id}/media", token, fields=campos, limit=50)
    while True:
        parou = False
        for p in pagina.get("data", []):
            quando = datetime.fromisoformat(p["timestamp"].replace("+0000", "+00:00"))
            if quando < corte:
                parou = True
                break
            posts.append(p)
        url_proxima = pagina.get("paging", {}).get("next")
        if parou or not url_proxima:
            break
        req = urllib.request.Request(url_proxima)
        with urllib.request.urlopen(req, timeout=45) as r:
            pagina = json.loads(r.read().decode())

    print(f"{len(posts)} posts na janela. Puxando insights...")
    linhas = []
    for i, p in enumerate(posts, 1):
        val = insights_do_post(token, p)
        reach = val.get("reach") or 0
        shares = val.get("shares") or 0
        saved = val.get("saved") or 0
        legenda = (p.get("caption") or "").replace("\n", " ")[:120]
        linhas.append({
            "snapshot_em": agora,
            "post_id": p["id"],
            "publicado_em": p["timestamp"],
            "tipo": p.get("media_product_type") or p.get("media_type"),
            "permalink": p.get("permalink"),
            "legenda_inicio": legenda,
            "views": val.get("views"),
            "reach": val.get("reach"),
            "saved": val.get("saved"),
            "shares": val.get("shares"),
            "likes": val.get("likes", p.get("like_count")),
            "comments": val.get("comments", p.get("comments_count")),
            "total_interactions": val.get("total_interactions"),
            "follows": val.get("follows"),
            "profile_visits": val.get("profile_visits"),
            "reels_avg_watch_time_ms": val.get("ig_reels_avg_watch_time"),
            "reels_total_watch_time_ms": val.get("ig_reels_video_view_total_time"),
            "s_por_r": round(shares / reach * 100, 3) if reach else None,
            "saves_por_r": round(saved / reach * 100, 3) if reach else None,
        })
        print(f"  [{i}/{len(posts)}] {p.get('media_product_type', '?'):9} "
              f"reach={reach or '-'} shares={shares or '-'} saves={saved or '-'}")

    novo = not os.path.isfile(CSV_PATH)
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUNAS)
        if novo:
            w.writeheader()
        w.writerows(linhas)

    print(f"\n{len(linhas)} linhas gravadas em {CSV_PATH}")
    top = sorted([l for l in linhas if l["s_por_r"]],
                 key=lambda l: l["s_por_r"], reverse=True)[:5]
    if top:
        print("\nTop 5 por taxa de compartilhamento (shares/reach):")
        for l in top:
            print(f"  {l['s_por_r']:>6.2f}%  {l['publicado_em'][:10]}  "
                  f"{l['legenda_inicio'][:60]}")


def main():
    ap = argparse.ArgumentParser(description="Métricas orgânicas do IG RECONECTA")
    ap.add_argument("--check-token", action="store_true",
                    help="valida token, escopos e qual conta ele enxerga")
    ap.add_argument("--dias", type=int, default=30,
                    help="janela de coleta em dias (padrão: 30)")
    args = ap.parse_args()

    token, origem = ler_token()
    try:
        if args.check_token:
            check_token(token, origem)
        else:
            coletar(token, args.dias)
    except RuntimeError as e:
        sys.exit(f"ERRO: {e}")


if __name__ == "__main__":
    main()
