#!/usr/bin/env python3
"""
slack_collector.py — Busca prints de provas sociais no Slack e salva em provas_sociais/.

Lê mensagens com imagens do canal #mais-dos-melhores-depoimentos.
Indexa cada print com descrição do resultado para o agente de carrosséis cruzar com temas.

Uso:
  python3 slack_collector.py              # sincroniza novos prints
  python3 slack_collector.py --listar     # exibe índice atual em JSON
"""

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path
from datetime import datetime

try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
except ImportError:
    print("ERRO: slack_sdk não instalado. Rode: pip install slack_sdk")
    raise

# ── Config ─────────────────────────────────────────────────────────────────────

def _load_config() -> dict:
    cfg_path = Path(__file__).parent / "agente.config.json"
    if not cfg_path.exists():
        print(
            f"ERRO: agente.config.json não encontrado em {cfg_path}\n"
            "Copie agente.config.json.template como agente.config.json e preencha os caminhos. Veja SETUP.md."
        )
        sys.exit(1)
    return json.loads(cfg_path.read_text(encoding="utf-8"))

_cfg = _load_config()

# ── Configurações ─────────────────────────────────────────────────────────────

BASE_DIR    = Path(_cfg["BASE"])
PROVAS_DIR  = BASE_DIR / "provas_sociais"
INDICE      = BASE_DIR / "provas_indice.json"
TOKEN_FILE  = BASE_DIR / ".slack_token"
CANAL_NOME  = "mais-dos-melhores-depoimentos"
EXTENSOES   = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

# ── Token ─────────────────────────────────────────────────────────────────────

def carregar_token() -> str:
    token = os.environ.get("SLACK_BOT_TOKEN", "").strip()
    if not token and TOKEN_FILE.exists():
        token = TOKEN_FILE.read_text(encoding="utf-8").strip()
    if not token:
        raise RuntimeError(
            f"Token do Slack não encontrado.\n"
            f"Salve seu Bot Token em: {TOKEN_FILE}\n"
            f"Ou exporte: export SLACK_BOT_TOKEN=xoxb-..."
        )
    return token

# ── Helpers ───────────────────────────────────────────────────────────────────

def carregar_indice() -> list:
    if INDICE.exists():
        return json.loads(INDICE.read_text(encoding="utf-8"))
    return []

def salvar_indice(dados: list):
    INDICE.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")

def ja_baixado(file_id: str, indice: list) -> bool:
    return any(e.get("slack_file_id") == file_id for e in indice)

def baixar_arquivo(url: str, destino: Path, token: str) -> bool:
    try:
        req = urllib.request.Request(
            url,
            headers={"Authorization": f"Bearer {token}", "User-Agent": "reconecta-bot/1.0"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            destino.write_bytes(resp.read())
        return True
    except Exception as e:
        print(f"    ERRO ao baixar {destino.name}: {e}")
        return False

def slug_arquivo(nome_original: str, idx: int) -> str:
    ext = Path(nome_original).suffix.lower() or ".jpg"
    if ext not in EXTENSOES:
        ext = ".jpg"
    return f"prova_{idx:04d}{ext}"

# ── Coleta principal ──────────────────────────────────────────────────────────

def barra(atual, total, largura=20):
    if total == 0:
        return "[" + "░" * largura + "] ?%"
    pct     = atual / total
    cheios  = int(pct * largura)
    vazios  = largura - cheios
    return f"[{'█' * cheios}{'░' * vazios}] {int(pct*100)}% · {atual}/{total}"

def coletar_arquivos_canal(client, canal_id) -> list:
    """Varre o histórico e retorna lista de todos os arquivos de imagem."""
    arquivos = []
    cursor   = None
    while True:
        resp = client.conversations_history(channel=canal_id, limit=200, cursor=cursor)
        for msg in resp.get("messages", []):
            for f in msg.get("files", []):
                ext = Path(f.get("name", "")).suffix.lower()
                url = f.get("url_private_download") or f.get("url_private", "")
                if ext in EXTENSOES and url:
                    arquivos.append({
                        "id":       f.get("id", ""),
                        "nome":     f.get("name", "arquivo.jpg"),
                        "url":      url,
                        "contexto": msg.get("text", "").strip()[:300],
                        "ts":       msg.get("ts", ""),
                    })
        cursor = resp.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break
    return arquivos

def sincronizar():
    PROVAS_DIR.mkdir(parents=True, exist_ok=True)

    token  = carregar_token()
    client = WebClient(token=token)
    indice = carregar_indice()

    print(f"Conectando ao canal #{CANAL_NOME}...", flush=True)
    canal_id = None
    cursor   = None
    while True:
        resp = client.conversations_list(
            types="public_channel,private_channel", limit=200, cursor=cursor
        )
        for ch in resp["channels"]:
            if ch["name"] == CANAL_NOME:
                canal_id = ch["id"]
                break
        if canal_id:
            break
        cursor = resp.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break

    if not canal_id:
        print(f"ERRO: canal #{CANAL_NOME} não encontrado.", flush=True)
        return

    try:
        client.conversations_join(channel=canal_id)
    except SlackApiError:
        pass

    try:
        client.conversations_info(channel=canal_id)
    except SlackApiError as e:
        if "not_in_channel" in str(e) or "channel_not_found" in str(e):
            print(
                f"ERRO: bot sem acesso ao canal. Envie no Slack: /invite @Reconecta Bot",
                flush=True,
            )
            return
        raise

    print(f"Varrendo historico do canal...", flush=True)
    todos = coletar_arquivos_canal(client, canal_id)
    novos_arqs = [f for f in todos if not ja_baixado(f["id"], indice)]

    total  = len(novos_arqs)
    ja_tem = len(indice)
    print(f"{total} prints novos para baixar  ({ja_tem} ja no banco)", flush=True)

    if total == 0:
        print("Nada novo. Banco ja esta atualizado.", flush=True)
        return

    prox_idx = max(
        [int(e["arquivo"].split("_")[1].split(".")[0])
         for e in indice if e.get("arquivo", "").startswith("prova_")],
        default=0,
    ) + 1

    novos = 0
    for i, f in enumerate(novos_arqs, start=1):
        nome_local = slug_arquivo(f["nome"], prox_idx)
        destino    = PROVAS_DIR / nome_local

        progresso = barra(i, total)
        print(f"{progresso} · {nome_local}", flush=True)

        ok = baixar_arquivo(f["url"], destino, token)
        if not ok:
            print(f"  falha ao baixar {f['nome']}", flush=True)
            continue

        data = datetime.fromtimestamp(float(f["ts"])).strftime("%Y-%m-%d") if f["ts"] else ""
        indice.append({
            "slack_file_id": f["id"],
            "arquivo":       nome_local,
            "caminho":       str(destino),
            "data":          data,
            "contexto":      f["contexto"],
            "tema_sugerido": "",
        })
        salvar_indice(indice)
        prox_idx += 1
        novos    += 1

    print(f"Concluido — {novos} prints baixados. Total no banco: {len(indice)}", flush=True)

def listar():
    indice = carregar_indice()
    print(json.dumps(indice, ensure_ascii=False, indent=2))

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Coleta provas sociais do Slack")
    parser.add_argument("--listar", action="store_true", help="Exibe indice em JSON")
    args = parser.parse_args()

    if args.listar:
        listar()
    else:
        sincronizar()

if __name__ == "__main__":
    main()
