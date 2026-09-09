#!/usr/bin/env python3
"""Coleta as mensagens ESCRITAS de uma pessoa no Slack, pra alimentar o fingerprint de voz.

Uso:
    export SLACK_BOT_TOKEN=xoxb-...
    python3 coleta_slack_autor.py "Ana Luiza" ebooks/715/fontes/voz/escritas-analuiza.txt

Por que existe: o fingerprint do ebook 715 foi montado só com FALA transcrita. Prosa
composta em cima de fala transcrita deixa uma costura que três leitores cegos
independentes identificaram (ver `experimento-desalinho.md`). Texto que a autora
digitou é o material que fecha esse buraco.

Escopo e privacidade, de propósito:
- coleta SÓ as mensagens da própria pessoa (filtro por user id), nunca de terceiros;
- só canais em que o bot já é membro (não entra em canal novo, não lê DM);
- descarta mensagem curta, só-emoji, só-link e mensagem de bot/integração;
- grava um .txt de amostras, sem ids, sem timestamps, sem nome de canal.

Escopos necessários no bot: users:read, channels:read, channels:history
(e groups:read + groups:history se quiser canal privado onde o bot esteja).
"""
import json, os, re, sys, time, urllib.parse, urllib.request

API = "https://slack.com/api/"
MIN_PALAVRAS = 12          # abaixo disso não é amostra de escrita, é recado
PAUSA = 1.1                # rate limit do Slack

def api(metodo, token, **params):
    url = API + metodo + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + token})
    with urllib.request.urlopen(req) as r:
        return json.load(r)

def paginar(metodo, token, chave, **params):
    cursor = None
    while True:
        p = dict(params)
        if cursor: p["cursor"] = cursor
        d = api(metodo, token, **p)
        if not d.get("ok"):
            raise SystemExit(f"{metodo} falhou: {d.get('error')}")
        for item in d.get(chave, []):
            yield item
        cursor = (d.get("response_metadata") or {}).get("next_cursor")
        if not cursor: return
        time.sleep(PAUSA)

def achar_pessoa(token, nome):
    alvo = nome.lower().split()
    achados = []
    for u in paginar("users.list", token, "members", limit=200):
        if u.get("deleted") or u.get("is_bot"): continue
        pf = u.get("profile", {})
        campos = " ".join(filter(None, [pf.get("real_name",""), pf.get("display_name",""), u.get("name","")])).lower()
        if all(t in campos for t in alvo):
            achados.append((u["id"], pf.get("real_name") or u.get("name")))
    return achados

def limpar(texto):
    """Tira o que não é prosa dela: menção, canal, emoji custom, link, citação."""
    t = re.sub(r"<@[UW][A-Z0-9]+(\|[^>]*)?>", "", texto)      # menções
    t = re.sub(r"<#C[A-Z0-9]+(\|[^>]*)?>", "", t)              # canais
    t = re.sub(r"<(https?://[^|>]+)(\|[^>]*)?>", "", t)        # links
    t = re.sub(r":[a-z0-9_+\-]+:", "", t)                      # emoji
    t = re.sub(r"^>.*$", "", t, flags=re.M)                    # citação
    t = re.sub(r"```.*?```", "", t, flags=re.S)                # código
    t = re.sub(r"[ \t]+", " ", t)
    return t.strip()

def main():
    token = os.environ.get("SLACK_BOT_TOKEN")
    if not token: raise SystemExit("Falta SLACK_BOT_TOKEN no ambiente.")
    if len(sys.argv) < 3: raise SystemExit(__doc__)
    nome, saida = sys.argv[1], sys.argv[2]

    teste = api("auth.test", token)
    if not teste.get("ok"):
        raise SystemExit(f"Token inválido: {teste.get('error')}. "
                         "'account_inactive' = app desinstalado ou token revogado; gerar outro em api.slack.com/apps.")
    print(f"conectado no workspace {teste.get('team')} como {teste.get('user')}")

    pessoas = achar_pessoa(token, nome)
    if not pessoas: raise SystemExit(f"Ninguém com nome parecido com {nome!r}.")
    if len(pessoas) > 1:
        print("mais de uma pessoa casou; usando a primeira:")
        for p in pessoas: print("  ", p)
    uid, real = pessoas[0]
    print(f"coletando de {real} ({uid})")

    canais = [c for c in paginar("conversations.list", token, "channels",
                                 types="public_channel,private_channel", limit=200, exclude_archived="true")
              if c.get("is_member")]
    print(f"{len(canais)} canais em que o bot é membro")

    amostras, vistos = [], set()
    for i, c in enumerate(canais, 1):
        print(f"  [{i}/{len(canais)}] #{c['name']}", flush=True)
        try:
            for m in paginar("conversations.history", token, "messages", channel=c["id"], limit=200):
                if m.get("user") != uid or m.get("subtype") or m.get("bot_id"): continue
                t = limpar(m.get("text") or "")
                if len(t.split()) < MIN_PALAVRAS: continue
                chave = t[:80]
                if chave in vistos: continue
                vistos.add(chave); amostras.append(t)
        except SystemExit as e:
            print(f"     pulei: {e}")
        time.sleep(PAUSA)

    amostras.sort(key=lambda x: -len(x.split()))
    total = sum(len(a.split()) for a in amostras)
    with open(saida, "w", encoding="utf-8") as f:
        f.write(f"# Mensagens escritas por {real} no Slack\n")
        f.write(f"# {len(amostras)} mensagens, {total} palavras. Só as mensagens dela, sem ids nem canais.\n\n")
        for a in amostras:
            f.write(a + "\n\n")
    print(f"\n{len(amostras)} mensagens, {total} palavras → {saida}")
    if total < 800:
        print("AVISO: menos de 800 palavras. Dá pra cruzar com a fala, mas é pouco pra refazer o fingerprint sozinho.")

if __name__ == "__main__":
    main()
