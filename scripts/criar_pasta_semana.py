#!/usr/bin/env python3
"""
Cria as pastas SEMxx em /Volumes/SSD kenipe/estáticos/novos/ referentes às
PRÓXIMAS semanas ISO (buffer de 2 semanas, pra um domingo perdido ou SSD
desmontado não travar o fluxo).

Disparado pelo launchd todo domingo. Idempotente — rodar várias vezes não
causa problema. Se o SSD não estiver montado, loga e sai sem erro.

OBS: rodando em background pelo launchd, o macOS exige "Acesso Total ao Disco"
(TCC) pro interpretador (/usr/bin/python3) escrever em volumes externos
(/Volumes/...). Sem isso dá PermissionError [Errno 1]. Ver README do script.
"""
import sys
from datetime import date, timedelta
from pathlib import Path

BASE = Path("/Volumes/SSD kenipe/estáticos/novos")
SEMANAS_BUFFER = 2  # cria a próxima semana + a seguinte


def proximas_segundas(qtd):
    """Lista das próximas `qtd` segundas-feiras (a partir da próxima)."""
    hoje = date.today()
    dias_ate_segunda = (7 - hoje.weekday()) % 7 or 7  # 1..7 (nunca 0)
    primeira = hoje + timedelta(days=dias_ate_segunda)
    return [primeira + timedelta(weeks=i) for i in range(qtd)]


def main():
    if not BASE.exists():
        print(f"[{date.today()}] SSD não montado ({BASE}). Pulando.", flush=True)
        return 0

    criadas, existentes = [], []
    for segunda in proximas_segundas(SEMANAS_BUFFER):
        semana = segunda.isocalendar()[1]
        alvo = BASE / f"SEM{semana:02d}"
        try:
            if alvo.exists():
                existentes.append(alvo.name)
                continue
            alvo.mkdir(parents=True, exist_ok=True)
            criadas.append(f"{alvo.name} (inicia {segunda})")
        except PermissionError as e:
            print(f"[{date.today()}] SEM PERMISSÃO (TCC) p/ {alvo}: {e}. "
                  f"Conceda Acesso Total ao Disco ao /usr/bin/python3.", flush=True)
            return 1

    if criadas:
        print(f"[{date.today()}] Criadas: {', '.join(criadas)}", flush=True)
    if existentes:
        print(f"[{date.today()}] Já existiam: {', '.join(existentes)}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
