#!/usr/bin/env python3
"""Lê a saída de um Workflow de revisão, salva revisao/NN/rodada-K.json e imprime os achados confirmados de forma compacta.
Uso: python3 ler_rodada.py <task-output.json> <pasta revisao/NN> [--full]"""
import json, sys, pathlib
o = json.load(open(sys.argv[1])); res = o["result"]; d = pathlib.Path(sys.argv[2]); d.mkdir(parents=True, exist_ok=True)
(d / f"rodada-{res['rodada']}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
full = "--full" in sys.argv
c = res.get("cego") or {}
print(f"{pathlib.Path(res['capitulo']).name} · rodada {res['rodada']} · brutos {res['brutos']} · confirmados {res['confirmados_n']} · altas {res['altas_confirmadas']} · cego {c.get('veredito')} {c.get('confianca')}")
for i, a in enumerate(res["confirmados"], 1):
    print(f"\n[{i}] {a['revisor']}/{a['gravidade']}")
    print("  TRECHO:", a["trecho"][:260 if not full else 2000].replace("\n", " ⏎ "))
    print("  DETALHE:", a["detalhe"][:220 if not full else 2000].replace("\n", " "))
    print("  CORRECAO:", a["correcao"][:700 if not full else 3000].replace("\n", " ⏎ "))
    m = a["motivos"][-1] if a.get("motivos") else ""
    if full: print("  CETICO:", m[:600].replace("\n", " "))
