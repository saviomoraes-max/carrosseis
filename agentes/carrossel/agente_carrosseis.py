#!/usr/bin/env python3
"""
agente_carrosseis.py — Utilitário CLI do agente de carrosséis RECONECTA.

Gerencia banco de imagens, cria estrutura de pastas, executa build/export e renomeia slides.
Chamado via Bash por Claude Code durante a orquestração de cada carrossel.

Comandos:
  selecionar  --categoria atriz|influenciadora
  marcar-usada --id img_042 --carrossel AD005-slug
  criar       --semana SEM18 --slug tema-slug
  build       --dir /caminho/carrossel
  renomear    --dir /caminho --ano 26 --sem 18 --num AD005 --titulo "Título"
  baixar      --url https://... --destino ./img/hero.jpg
  listar      [--status disponivel|usado]
  provas      (lista prints disponíveis em provas_sociais/)
"""

import argparse
import json
import shutil
import subprocess
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

# ── Config ───────────────────────────────────────────────────────────────────

def _load_config() -> dict:
    cfg_path = Path(__file__).parent / "agente.config.json"
    if not cfg_path.exists():
        print(json.dumps({
            "erro": (
                f"Arquivo de configuração não encontrado: {cfg_path}\n"
                "Copie agente.config.json.template como agente.config.json "
                "e preencha os caminhos do seu ambiente. Veja SETUP.md."
            )
        }, ensure_ascii=False))
        sys.exit(1)
    return json.loads(cfg_path.read_text(encoding="utf-8"))

_cfg = _load_config()

# ── Paths ────────────────────────────────────────────────────────────────────

BASE          = Path(_cfg["BASE"])
MANIFEST      = BASE / "bank_manifest.json"
PROVAS_DIR    = BASE / "provas_sociais"
TEMPLATE_DIR  = Path(_cfg["TEMPLATE_DIR"])
NOISE_SRC     = Path(_cfg["NOISE_SRC"])
PYTHON        = _cfg["PYTHON"]

# ── Helpers ──────────────────────────────────────────────────────────────────

def load_manifest() -> list:
    if not MANIFEST.exists():
        return []
    return json.loads(MANIFEST.read_text(encoding="utf-8"))

def save_manifest(data: list):
    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def out(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))

# ── Comandos ─────────────────────────────────────────────────────────────────

def cmd_selecionar(args):
    """
    Retorna a imagem disponível mais adequada ao tema.
    Prioridade: categoria solicitada → data de coleta mais recente → nunca repetir.
    """
    manifest = load_manifest()
    disponiveis = [e for e in manifest if e.get("status") == "disponivel"]

    if not disponiveis:
        out({"erro": "Banco vazio — rode pinterest_collector.py primeiro."})
        return

    if args.categoria:
        filtradas = [e for e in disponiveis if e.get("categoria") == args.categoria]
        if filtradas:
            disponiveis = filtradas

    # Mais recentes primeiro
    disponiveis.sort(key=lambda e: e.get("data_coleta", ""), reverse=True)
    out(disponiveis[0])


def cmd_marcar_usada(args):
    """Marca uma imagem como usada e registra em qual carrossel."""
    manifest = load_manifest()
    for entrada in manifest:
        if entrada["id"] == args.id:
            entrada["status"] = "usado"
            entrada["usado_em"] = args.carrossel
            save_manifest(manifest)
            out({"ok": True, "id": args.id, "usado_em": args.carrossel})
            return
    out({"erro": f"ID {args.id} não encontrado no manifest."})


def cmd_criar(args):
    """
    Cria a estrutura de pastas do carrossel no SSD:
      SEM{xx}/{slug}/
        img/         ← hero.jpg vai aqui (após Adobe)
        slides/      ← PNGs exportados ficam aqui
      Copia export.py do template e noise.png automaticamente.
    """
    carrossel_dir = BASE / args.semana / args.slug
    img_dir       = carrossel_dir / "img"
    slides_dir    = carrossel_dir / "slides"

    img_dir.mkdir(parents=True, exist_ok=True)
    slides_dir.mkdir(parents=True, exist_ok=True)

    # export.py do template
    export_src = TEMPLATE_DIR / "export.py"
    export_dst = carrossel_dir / "export.py"
    if export_src.exists() and not export_dst.exists():
        shutil.copy2(export_src, export_dst)

    # noise.png (overlay de textura da hero)
    noise_dst = img_dir / "noise.png"
    if NOISE_SRC.exists() and not noise_dst.exists():
        shutil.copy2(NOISE_SRC, noise_dst)

    out({
        "ok": True,
        "dir":        str(carrossel_dir),
        "img_dir":    str(img_dir),
        "slides_dir": str(slides_dir),
        "export_py":  str(export_dst),
    })


def cmd_build(args):
    """Executa build.py → carousel.html e depois export.py → slides PNG."""
    d = Path(args.dir)

    if not (d / "build.py").exists():
        out({"erro": f"build.py não encontrado em {d}"})
        return

    r1 = subprocess.run(
        [PYTHON, "build.py"], cwd=d, capture_output=True, text=True, timeout=60
    )
    if r1.returncode != 0:
        out({"erro": "build.py falhou", "stderr": r1.stderr[:800]})
        return

    r2 = subprocess.run(
        [PYTHON, "export.py"], cwd=d, capture_output=True, text=True, timeout=180
    )
    if r2.returncode != 0:
        out({"erro": "export.py falhou", "stderr": r2.stderr[:800]})
        return

    slides = sorted((d / "slides").glob("slide_*.png"))
    out({
        "ok":     True,
        "slides": len(slides),
        "dir":    str(d),
        "html":   str(d / "carousel.html"),
    })


def cmd_renomear(args):
    """
    Renomeia slides de slide_N.png para a nomenclatura oficial:
    [AA] [SS] [AD00N_M] - Título.png
    """
    slides_dir = Path(args.dir) / "slides"
    slides = sorted(slides_dir.glob("slide_*.png"))

    if not slides:
        out({"erro": f"Nenhum slide encontrado em {slides_dir}"})
        return

    renomeados = []
    for idx, slide in enumerate(slides, start=1):
        novo_nome = f"[{args.ano}] [{args.sem}] [{args.num}_{idx}] - {args.titulo}.png"
        destino   = slide.parent / novo_nome
        slide.rename(destino)
        renomeados.append(novo_nome)

    out({"ok": True, "total": len(renomeados), "slides": renomeados})


def cmd_baixar(args):
    """
    Baixa uma imagem de URL (tipicamente output do Adobe for Creativity)
    para um caminho local. Cria a pasta de destino se necessário.
    """
    destino = Path(args.destino)
    destino.parent.mkdir(parents=True, exist_ok=True)

    try:
        req = urllib.request.Request(args.url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            destino.write_bytes(resp.read())
        out({"ok": True, "destino": str(destino), "bytes": destino.stat().st_size})
    except Exception as e:
        out({"erro": str(e), "url": args.url})


def cmd_listar(args):
    """Lista imagens do banco, opcionalmente filtrando por status."""
    manifest = load_manifest()
    if args.status:
        manifest = [e for e in manifest if e.get("status") == args.status]

    resumo = {
        "total":         len(manifest),
        "disponiveis":   sum(1 for e in manifest if e.get("status") == "disponivel"),
        "usados":        sum(1 for e in manifest if e.get("status") == "usado"),
        "imagens":       manifest,
    }
    out(resumo)


def cmd_provas(args):
    """Lista prints de provas sociais disponíveis em provas_sociais/."""
    PROVAS_DIR.mkdir(parents=True, exist_ok=True)
    extensoes = {".jpg", ".jpeg", ".png", ".webp"}
    provas = [
        {
            "arquivo": str(f),
            "nome":    f.name,
            "bytes":   f.stat().st_size,
        }
        for f in sorted(PROVAS_DIR.iterdir())
        if f.suffix.lower() in extensoes and not f.name.startswith("._")
    ]
    out({"total": len(provas), "provas": provas})


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Agente de carrosséis RECONECTA — utilitário de suporte"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("selecionar", help="Escolhe imagem disponível do banco")
    p.add_argument("--categoria", choices=["atriz", "influenciadora"])

    p = sub.add_parser("marcar-usada", help="Marca imagem como usada no manifest")
    p.add_argument("--id",        required=True, help="ex: img_042")
    p.add_argument("--carrossel", required=True, help="ex: AD005-erro-financeiro")

    p = sub.add_parser("criar", help="Cria estrutura de pastas do carrossel")
    p.add_argument("--semana", required=True, help="ex: SEM18")
    p.add_argument("--slug",   required=True, help="ex: erro-financeiro-dentista")

    p = sub.add_parser("build", help="Executa build.py + export.py")
    p.add_argument("--dir", required=True, help="Caminho absoluto do carrossel")

    p = sub.add_parser("renomear", help="Renomeia slides para nomenclatura oficial")
    p.add_argument("--dir",    required=True)
    p.add_argument("--ano",    required=True, help="ex: 26")
    p.add_argument("--sem",    required=True, help="ex: 18")
    p.add_argument("--num",    required=True, help="ex: AD005")
    p.add_argument("--titulo", required=True, help="ex: Erro Financeiro Dentista")

    p = sub.add_parser("baixar", help="Baixa imagem de URL Adobe para local")
    p.add_argument("--url",     required=True)
    p.add_argument("--destino", required=True, help="Caminho local de destino")

    p = sub.add_parser("listar", help="Lista imagens do banco")
    p.add_argument("--status", choices=["disponivel", "usado"])

    sub.add_parser("provas", help="Lista prints de provas sociais disponíveis")

    args = parser.parse_args()
    {
        "selecionar":   cmd_selecionar,
        "marcar-usada": cmd_marcar_usada,
        "criar":        cmd_criar,
        "build":        cmd_build,
        "renomear":     cmd_renomear,
        "baixar":       cmd_baixar,
        "listar":       cmd_listar,
        "provas":       cmd_provas,
    }[args.cmd](args)


if __name__ == "__main__":
    main()
