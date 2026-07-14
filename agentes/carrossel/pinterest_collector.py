#!/usr/bin/env python3
"""
pinterest_collector.py — Coleta semanal de imagens do Pinterest para heroes de carrosséis RECONECTA
Executa via launchd todo domingo às 08h
"""

import json
import subprocess
import shutil
import sys
from pathlib import Path
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────────────

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

# ── Configurações ────────────────────────────────────────────────────────────

BASE_DIR    = Path(_cfg["BASE"])
BANK_DIR    = BASE_DIR / "bank"
MANIFEST    = BASE_DIR / "bank_manifest.json"
LOG_DIR     = BASE_DIR / "logs"
POR_PESSOA  = 3
BUSCAR_POR_PESSOA = 10
RESOLUCAO_MIN = 800

# ── Lista de pessoas ─────────────────────────────────────────────────────────
# categoria: "atriz" → conteúdo profissional/técnico
#            "influenciadora" → conteúdo aspiracional/lifestyle

PESSOAS = [
    # Atrizes
    {"nome": "Anne Hathaway",     "categoria": "atriz",           "query": "anne hathaway fashion editorial portrait"},
    {"nome": "Anya Taylor-Joy",   "categoria": "atriz",           "query": "anya taylor joy style editorial"},
    {"nome": "Angelina Jolie",    "categoria": "atriz",           "query": "angelina jolie editorial portrait"},
    {"nome": "Sydney Sweeney",    "categoria": "atriz",           "query": "sydney sweeney fashion editorial"},
    {"nome": "Margaret Qualley",  "categoria": "atriz",           "query": "margaret qualley editorial fashion"},
    {"nome": "Zendaya",           "categoria": "atriz",           "query": "zendaya euphoria met gala look"},
    {"nome": "Margot Robbie",     "categoria": "atriz",           "query": "margot robbie editorial portrait fashion"},
    {"nome": "Ana de Armas",      "categoria": "atriz",           "query": "ana de armas editorial fashion"},
    # Influenciadoras
    {"nome": "Hailey Bieber",     "categoria": "influenciadora",  "query": "hailey bieber style aesthetic"},
    {"nome": "Kim Kardashian",    "categoria": "influenciadora",  "query": "kim kardashian skims campaign photoshoot"},
    {"nome": "Kendall Jenner",    "categoria": "influenciadora",  "query": "kendall jenner editorial fashion"},
    {"nome": "Kylie Jenner",      "categoria": "influenciadora",  "query": "kylie jenner style aesthetic"},
    {"nome": "Virginia Fonseca",  "categoria": "influenciadora",  "query": "virginia fonseca look estilo"},
    {"nome": "Gkay",              "categoria": "influenciadora",  "query": "gkay look fashion"},
]

# ── Helpers ──────────────────────────────────────────────────────────────────

def log(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"[{timestamp}] {msg}"
    print(linha, flush=True)

def semana_iso() -> str:
    ano, semana, _ = datetime.now().isocalendar()
    return f"SEM{semana:02d}"

def carregar_manifest() -> list:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    return []

def salvar_manifest(dados: list):
    MANIFEST.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")

def proximo_id(manifest: list) -> int:
    if not manifest:
        return 1
    ids = [int(e["id"].replace("img_", "")) for e in manifest if e.get("id", "").startswith("img_")]
    return max(ids, default=0) + 1

def verificar_resolucao(caminho: Path) -> tuple[bool, int, int]:
    if caminho.name.startswith("._"):
        return False, 0, 0
    try:
        from PIL import Image
        with Image.open(caminho) as img:
            w, h = img.size
            return w >= RESOLUCAO_MIN, w, h
    except Exception:
        try:
            out = subprocess.check_output(
                ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(caminho)],
                stderr=subprocess.DEVNULL, text=True
            )
            linhas = out.strip().splitlines()
            w = next((int(l.split()[-1]) for l in linhas if "pixelWidth" in l), 0)
            h = next((int(l.split()[-1]) for l in linhas if "pixelHeight" in l), 0)
            return w >= RESOLUCAO_MIN, w, h
        except Exception:
            return False, 0, 0

TEXTO_MIN_CHARS = 25

def tem_texto(caminho: Path) -> bool:
    """Retorna True se a imagem contiver texto sobreposto visível."""
    if caminho.name.startswith("._"):
        return False
    try:
        import pytesseract
        from PIL import Image
        with Image.open(caminho) as img:
            w, h = img.size
            if w > 900:
                img = img.resize((900, int(h * 900 / w)))
            texto = pytesseract.image_to_string(img, config="--psm 11 --oem 1")
        return len(texto.strip()) >= TEXTO_MIN_CHARS
    except Exception:
        return False

def ja_coletada(url_origem: str, manifest: list) -> bool:
    return any(e.get("url_origem") == url_origem for e in manifest)

# ── Coleta principal ─────────────────────────────────────────────────────────

def coletar_pessoa(pessoa: dict, semana_dir: Path, manifest: list, proximo: int) -> list:
    query = pessoa["query"]
    url   = f"https://www.pinterest.com/search/pins/?q={query.replace(' ', '%20')}"
    slug  = pessoa["nome"].lower().replace(" ", "_")

    temp_dir = semana_dir / f"_tmp_{slug}"
    temp_dir.mkdir(parents=True, exist_ok=True)

    log(f"  Buscando: {pessoa['nome']} ({query})")

    try:
        resultado = subprocess.run(
            [
                "gallery-dl",
                "--range",     f"1-{BUSCAR_POR_PESSOA}",
                "--directory", str(temp_dir),
                "--filename",  "{num:>04}.{extension}",
                "--no-part",
                "--quiet",
                url,
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if resultado.returncode not in (0, 1):
            log(f"  AVISO gallery-dl retornou {resultado.returncode}: {resultado.stderr[:200]}")
    except subprocess.TimeoutExpired:
        log(f"  TIMEOUT ao buscar {pessoa['nome']}")
        shutil.rmtree(temp_dir, ignore_errors=True)
        return []
    except FileNotFoundError:
        log("  ERRO: gallery-dl não encontrado. Instale com: brew install gallery-dl")
        sys.exit(1)

    candidatas = sorted(
        f for f in (
            list(temp_dir.glob("**/*.jpg")) +
            list(temp_dir.glob("**/*.jpeg")) +
            list(temp_dir.glob("**/*.png"))
        ) if not f.name.startswith("._")
    )

    novas = []
    for img_path in candidatas:
        if len(novas) >= POR_PESSOA:
            break

        ok, largura, altura = verificar_resolucao(img_path)
        if not ok:
            log(f"    Descartada ({largura}x{altura} < mínimo {RESOLUCAO_MIN}px): {img_path.name}")
            continue

        if tem_texto(img_path):
            log(f"    Descartada (contém texto): {img_path.name}")
            continue

        img_id    = f"img_{proximo:04d}"
        nome_arq  = f"{slug}_{proximo:04d}.jpg"
        destino   = semana_dir / nome_arq

        shutil.copy2(img_path, destino)

        entrada = {
            "id":           img_id,
            "arquivo":      str(destino),
            "semana":       semana_dir.name,
            "pessoa":       pessoa["nome"],
            "categoria":    pessoa["categoria"],
            "resolucao":    f"{largura}x{altura}",
            "data_coleta":  datetime.now().strftime("%Y-%m-%d"),
            "status":       "disponivel",
            "usado_em":     None,
        }
        novas.append(entrada)
        log(f"    {nome_arq}  ({largura}x{altura})")
        proximo += 1

    shutil.rmtree(temp_dir, ignore_errors=True)
    log(f"  -> {len(novas)} imagens salvas de {pessoa['nome']}")
    return novas

# ── Entry point ──────────────────────────────────────────────────────────────

def main():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    semana  = semana_iso()
    sem_dir = BANK_DIR / semana
    sem_dir.mkdir(parents=True, exist_ok=True)

    log(f"=== Pinterest Collector — {semana} ===")

    manifest = carregar_manifest()
    prox_id  = proximo_id(manifest)
    total    = 0

    for pessoa in PESSOAS:
        novas = coletar_pessoa(pessoa, sem_dir, manifest, prox_id)
        manifest.extend(novas)
        prox_id += len(novas)
        total   += len(novas)

    salvar_manifest(manifest)
    log(f"\n=== Concluido: {total} novas imagens adicionadas ao banco ===")
    log(f"    Manifest: {MANIFEST}")

if __name__ == "__main__":
    main()
