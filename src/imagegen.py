"""Fundo fotorrealista do card gerado por IA (OpenAI Images / gpt-image-1).

Cada post recebe uma cena única de trader — o "homem na frente dos monitores" —
com iluminação cinematográfica, para parar o scroll. Se a chave não existir ou a
API falhar, retorna None e o card cai para a cena desenhada (scene.py).
"""
from __future__ import annotations

import base64
import io
import random
import sys

import requests
from PIL import Image

from . import config

# Variações de câmera/luz/ambiente — combinadas pela semente para nunca repetir.
_SHOTS = [
    "seen from behind over his shoulder, facing a wall of glowing monitors",
    "low three-quarter angle, his face lit only by the screen glow",
    "wide cinematic shot, small against a large dark trading room",
    "close over-the-shoulder, monitors filling the background in soft focus",
    "silhouetted against bright candlestick charts in a dark room",
    "side profile, leaning toward the screens with intense focus",
]
_LIGHT = [
    "cool teal and blue screen glow, moody and cinematic",
    "warm amber desk lamp mixed with cold monitor light",
    "deep indigo and violet ambient light, night mood",
    "high-contrast chiaroscuro lighting, single light source from the screens",
    "soft dawn light through a window mixing with the screen glow",
    "neon magenta and cyan reflections, modern and striking",
]
_SCENE = [
    "a modern home trading desk with several monitors showing green and red candlestick charts",
    "a minimalist dark office at night, city skyline bokeh through the window behind him",
    "a multi-monitor setup with financial charts, coffee mug steam rising",
    "an immersive curved-monitor battlestation glowing with market charts",
    "a clean desk with two large screens full of candlestick charts and market data",
]
# Enfoques emocionais para os posts de 'trader' (o lado mental).
_MOOD_TRADER = [
    "contemplative and a little tense, the weight of the decision on him",
    "focused and disciplined, calm under pressure",
    "head resting on his hand, tired after a long session",
    "leaning back, exhaling, processing a tough day",
]


def _prompt(content_type: str, seed: int) -> str:
    rnd = random.Random(seed)
    shot = rnd.choice(_SHOTS)
    light = rnd.choice(_LIGHT)
    scene = rnd.choice(_SCENE)
    mood = rnd.choice(_MOOD_TRADER) if content_type == "trader" else "professional and focused"
    return (
        f"Cinematic photorealistic photograph of a lone male day trader, {shot}, in {scene}. "
        f"He is {mood}. {light}. Shallow depth of field, volumetric haze, film grain, "
        "ultra-realistic, editorial photography, 8k, dramatic composition. "
        "Leave clean darker negative space in the TOP THIRD of the frame for a headline. "
        "Vertical portrait composition. No text, no words, no letters, no watermark, no logo, no UI overlays."
    )


def _payload(content_type: str, seed: int) -> dict:
    """Monta o corpo da requisição conforme o modelo (gpt-image-1 ou dall-e-3)."""
    model = config.IMAGE_MODEL
    body = {"model": model, "prompt": _prompt(content_type, seed), "n": 1}
    if model.startswith("dall-e-3"):
        # dall-e-3: retrato 1024x1792, qualidade standard|hd, b64 explícito.
        body["size"] = "1024x1792"
        body["quality"] = "hd" if config.IMAGE_QUALITY in ("high", "hd") else "standard"
        body["response_format"] = "b64_json"
    else:
        # gpt-image-1: retrato 1024x1536, qualidade low|medium|high (b64 por padrão).
        body["size"] = "1024x1536"
        body["quality"] = config.IMAGE_QUALITY
    return body


def generate_background(content_type: str, seed: int = 0) -> Image.Image | None:
    """Gera um fundo fotorrealista de trader. Retorna None se não for possível."""
    if not config.OPENAI_API_KEY:
        return None
    try:
        r = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers={
                "Authorization": f"Bearer {config.OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json=_payload(content_type, seed),
            timeout=180,
        )
        if r.status_code != 200:
            print(f"Aviso: geração de imagem falhou ({r.status_code}): {r.text[:300]}", file=sys.stderr)
            return None
        data = r.json()["data"][0]
        raw = base64.b64decode(data["b64_json"]) if "b64_json" in data else _download(data.get("url"))
        if not raw:
            return None
        return Image.open(io.BytesIO(raw)).convert("RGBA")
    except Exception as exc:  # noqa: BLE001 — nunca derruba o post; cai para a cena desenhada
        print(f"Aviso: geração de imagem indisponível: {exc}", file=sys.stderr)
        return None


def _download(url: str | None) -> bytes | None:
    if not url:
        return None
    resp = requests.get(url, timeout=60)
    return resp.content if resp.status_code == 200 else None
