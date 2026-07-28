#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Importa o CSV de conteúdo do Meta Business Suite para o mesmo historico.csv que o
coletor da Graph API alimenta. Assim a análise semanal lê UM formato só, venha o
número do export manual ou da API.

Por que isso existe: o export do Business Suite já traz tudo que a análise usa
(Visualizações, Alcance, Curtidas, Compartilhamentos, Seguimentos, Comentários,
Salvamentos) com "Data = Total", ou seja, acumulado de vida do post. Não precisa
de token nenhum — só de um export com a janela de datas certa.

O que o CSV NÃO traz (e a Graph API traria): visitas ao perfil e watch time de
Reels. Ficam vazios, nunca estimados.
O que NENHUM dos dois traz: retenção de 3s e % de alcance de não-seguidores por
post — só existem no app, na mão.

Uso:
  ./importar_business_suite.py caminho/do/export.csv
  ./importar_business_suite.py caminho/do/export.csv --conta oleonardorosso
"""

import argparse
import csv
import os
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE), "data", "metricas-ig")
CSV_PATH = os.path.join(DATA_DIR, "historico.csv")

COLUNAS = [
    "snapshot_em", "conta", "post_id", "publicado_em", "tipo", "permalink", "legenda_inicio",
    "views", "reach", "saved", "shares", "likes", "comments",
    "total_interactions", "follows", "profile_visits",
    "reels_avg_watch_time_ms", "reels_total_watch_time_ms",
    "s_por_r", "saves_por_r",
]

# nome no export do Business Suite -> nome canônico nosso
DE_PARA = {
    "Identificação do post": "post_id",
    "Horário de publicação": "publicado_em",
    "Tipo de post": "tipo",
    "Link permanente": "permalink",
    "Descrição": "legenda_inicio",
    "Visualizações": "views",
    "Alcance": "reach",
    "Curtidas": "likes",
    "Compartilhamentos": "shares",
    "Seguimentos": "follows",
    "Comentários": "comments",
    "Salvamentos": "saved",
}


def num(v):
    """Célula vazia vira None (ausente), não zero — zero é um dado, ausência não."""
    v = (v or "").strip().replace(".", "").replace(",", "")
    return int(v) if v.isdigit() else None


def data_iso(v):
    for fmt in ("%m/%d/%Y %H:%M", "%d/%m/%Y %H:%M", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(v.strip(), fmt).isoformat()
        except (ValueError, AttributeError):
            continue
    return None


def main():
    ap = argparse.ArgumentParser(description="Business Suite CSV -> historico.csv")
    ap.add_argument("csv_entrada", help="export de conteúdo do Business Suite")
    ap.add_argument("--conta", help="filtra por nome de usuário da conta")
    args = ap.parse_args()

    if not os.path.isfile(args.csv_entrada):
        sys.exit(f"ERRO: não achei {args.csv_entrada}")

    with open(args.csv_entrada, encoding="utf-8-sig") as f:
        entrada = list(csv.DictReader(f))
    if not entrada:
        sys.exit("ERRO: CSV vazio.")

    faltando = [c for c in DE_PARA if c not in entrada[0]]
    if faltando:
        sys.exit("ERRO: esse CSV não parece ser o export de CONTEÚDO do Business "
                 f"Suite.\n  Faltam as colunas: {', '.join(faltando)}\n"
                 f"  Colunas encontradas: {', '.join(entrada[0].keys())}")

    contas = {r.get("Nome de usuário da conta", "") for r in entrada}
    if args.conta:
        entrada = [r for r in entrada if r.get("Nome de usuário da conta") == args.conta]
        if not entrada:
            sys.exit(f"ERRO: nenhuma linha da conta '{args.conta}'. "
                     f"Contas no arquivo: {', '.join(sorted(contas))}")
    elif len(contas) > 1:
        print(f"aviso: o arquivo tem {len(contas)} contas ({', '.join(sorted(contas))}). "
              "Importando todas — use --conta pra filtrar.", file=sys.stderr)

    # já importado? chave = post_id + data de publicação (o export é acumulado)
    ja_tem = set()
    if os.path.isfile(CSV_PATH):
        with open(CSV_PATH, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                ja_tem.add((r["post_id"], r["snapshot_em"]))

    agora = datetime.now().astimezone().isoformat(timespec="seconds")
    linhas, pulados, sem_data = [], 0, 0
    for r in entrada:
        pid = r["Identificação do post"].strip()
        if not pid or (pid, agora) in ja_tem:
            pulados += 1
            continue
        pub = data_iso(r["Horário de publicação"])
        if not pub:
            sem_data += 1
            continue

        reach = num(r["Alcance"])
        shares = num(r["Compartilhamentos"])
        saved = num(r["Salvamentos"])
        likes = num(r["Curtidas"])
        comments = num(r["Comentários"])
        # total_interactions: soma das quatro (aritmética das colunas presentes,
        # não estimativa). Se faltar alguma, fica vazio.
        partes = [likes, comments, saved, shares]
        total = sum(partes) if all(p is not None for p in partes) else None

        linhas.append({
            "snapshot_em": agora,
            "conta": r.get("Nome de usuário da conta", ""),
            "post_id": pid,
            "publicado_em": pub,
            "tipo": r["Tipo de post"],
            "permalink": r["Link permanente"],
            "legenda_inicio": (r["Descrição"] or "").replace("\n", " ")[:120],
            "views": num(r["Visualizações"]),
            "reach": reach,
            "saved": saved,
            "shares": shares,
            "likes": likes,
            "comments": comments,
            "total_interactions": total,
            "follows": num(r["Seguimentos"]),
            "profile_visits": None,            # não existe no export
            "reels_avg_watch_time_ms": None,   # não existe no export
            "reels_total_watch_time_ms": None,
            "s_por_r": round(shares / reach * 100, 3) if reach and shares is not None else None,
            "saves_por_r": round(saved / reach * 100, 3) if reach and saved is not None else None,
        })

    os.makedirs(DATA_DIR, exist_ok=True)
    novo = not os.path.isfile(CSV_PATH)
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUNAS)
        if novo:
            w.writeheader()
        w.writerows(linhas)

    datas = sorted(l["publicado_em"][:10] for l in linhas)
    print(f"{len(linhas)} posts importados para {CSV_PATH}")
    if datas:
        print(f"janela: {datas[0]} → {datas[-1]}")
    if pulados:
        print(f"{pulados} pulados (sem id ou já importados neste snapshot)")
    if sem_data:
        print(f"{sem_data} pulados por data de publicação ilegível", file=sys.stderr)

    top = sorted([l for l in linhas if l["s_por_r"]],
                 key=lambda l: l["s_por_r"], reverse=True)[:5]
    if top:
        print("\nTop 5 por taxa de compartilhamento (shares/reach):")
        for l in top:
            print(f"  {l['s_por_r']:>6.2f}%  {l['publicado_em'][:10]}  "
                  f"alc={l['reach']:>6}  {l['legenda_inicio'][:52]}")


if __name__ == "__main__":
    main()
