"""
Gera imagens de background para slides do carrossel usando Gemini 2.5 Flash Image
(nano banana). Cache-aware: só regenera se o prompt mudar (hash md5).

Uso:
  python3 generate_bg.py <slide_slug> "<prompt>"

Exemplo:
  python3 generate_bg.py slide1 "editorial photo of..."

Outputs:
  img/bg_<slide_slug>.png
"""
import hashlib
import os
import sys
from pathlib import Path

from google import genai
from google.genai import types

BASE = Path(__file__).parent
IMG_DIR = BASE / "img"
CACHE_DIR = BASE / ".bg_cache"
IMG_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)

MODEL = "gemini-2.5-flash-image"


def load_api_key() -> str:
    """Lê GEMINI_API_KEY de ~/.reconecta.env."""
    env_path = Path.home() / ".reconecta.env"
    if not env_path.exists():
        raise RuntimeError(f"Arquivo de credenciais não existe: {env_path}")
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line.startswith("GEMINI_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise RuntimeError("GEMINI_API_KEY não encontrada em ~/.reconecta.env")


def prompt_hash(prompt: str) -> str:
    return hashlib.md5(prompt.encode("utf-8")).hexdigest()[:12]


def generate(slug: str, prompt: str, force: bool = False) -> Path:
    """Gera (ou retorna cache de) imagem para o slug + prompt."""
    out_path = IMG_DIR / f"bg_{slug}.png"
    cache_marker = CACHE_DIR / f"{slug}.hash"
    current_hash = prompt_hash(prompt)

    # Checa cache: mesmo prompt + arquivo existente = skip
    if not force and out_path.exists() and cache_marker.exists():
        if cache_marker.read_text().strip() == current_hash:
            print(f"  [cache] {slug}: prompt inalterado, reusando {out_path.name}")
            return out_path

    print(f"  [gen] {slug}: chamando {MODEL}...")
    api_key = load_api_key()
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=MODEL,
        contents=[prompt],
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
        ),
    )

    # Extrai bytes da imagem da resposta
    image_bytes = None
    for part in response.candidates[0].content.parts:
        if getattr(part, "inline_data", None) and part.inline_data.data:
            image_bytes = part.inline_data.data
            break

    if image_bytes is None:
        raise RuntimeError(
            f"Resposta do modelo não contém imagem. Resposta: {response}"
        )

    out_path.write_bytes(image_bytes)
    cache_marker.write_text(current_hash)
    size_kb = out_path.stat().st_size / 1024
    print(f"  [ok] {slug}: {out_path.name} ({size_kb:.1f} KB)")
    return out_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 generate_bg.py <slug> '<prompt>'")
        sys.exit(1)
    slug = sys.argv[1]
    prompt = sys.argv[2]
    force = "--force" in sys.argv
    generate(slug, prompt, force=force)
