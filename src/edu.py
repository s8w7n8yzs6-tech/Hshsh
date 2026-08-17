"""Desenha o diagrama esquemático de um padrão gráfico (didático).

Recebe um padrão de src/patterns.py e devolve uma imagem RGBA com o diagrama —
velas (candlestick) ou linha de preço com suporte/resistência/tendência.

Cada render aplica uma pequena variação (jitter) determinística pela semente,
para que o MESMO padrão nunca saia com a imagem idêntica, mantendo-se
reconhecível. São ilustrações didáticas, não dados reais.
"""
from __future__ import annotations

import random

from PIL import Image, ImageDraw, ImageFont

_UP = (34, 197, 94)      # alta
_DOWN = (239, 68, 68)    # baixa
_GRID = (148, 163, 184)
# Cores possíveis da linha de preço (variam por post).
_LINE_COLORS = [(56, 189, 248), (45, 212, 191), (129, 140, 248), (251, 146, 60), (52, 211, 153)]

_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def _font(size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(_SANS, size)
    except OSError:
        return ImageFont.load_default()


def _clip(v: float, lo: float = 0.06, hi: float = 0.94) -> float:
    return max(lo, min(hi, v))


def _y(v: float, top: int, h: int) -> float:
    return top + (1.0 - v) * h


def _dashed_h(d, x0, x1, y, color, width=3, dash=16, gap=12):
    x = x0
    while x < x1:
        d.line([(x, y), (min(x + dash, x1), y)], fill=color, width=width)
        x += dash + gap


def render_pattern(pattern: dict, width: int, height: int, seed: int = 0) -> Image.Image:
    """Diagrama do padrão numa imagem RGBA transparente, com pequena variação por `seed`."""
    rnd = random.Random((seed * 2654435761) ^ (hash(pattern.get("key", "")) & 0xFFFFFFFF))
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pad = int(width * (0.055 + rnd.uniform(0, 0.02)))
    top, left = pad, pad
    plot_w, plot_h = width - 2 * pad, height - 2 * pad

    for i in range(1, 5):
        gy = top + plot_h * i / 5
        d.line([(left, gy), (left + plot_w, gy)], fill=_GRID + (26,), width=1)

    if pattern["tipo"] == "candles":
        _draw_candles(d, pattern["candles"], left, top, plot_w, plot_h, rnd)
    else:
        _draw_line(img, d, pattern, left, top, plot_w, plot_h, rnd)
    return img


def _draw_candles(d, candles, left, top, w, h, rnd):
    shift = rnd.uniform(-0.05, 0.05)          # desloca o conjunto todo
    n = len(candles)
    slot = w / n
    cw = slot * rnd.uniform(0.42, 0.58)
    for i, (o, hi, lo, c) in enumerate(candles):
        j = rnd.uniform(-0.02, 0.02)          # ruído por vela (preserva o formato)
        o2, c2 = _clip(o + shift + j), _clip(c + shift + j)
        hi2 = _clip(max(o2, c2) + (hi - max(o, c)) + rnd.uniform(-0.01, 0.015))
        lo2 = _clip(min(o2, c2) - (min(o, c) - lo) - rnd.uniform(-0.01, 0.015))
        cx = left + slot * (i + 0.5) + rnd.uniform(-slot * 0.06, slot * 0.06)
        color = _UP if c2 >= o2 else _DOWN
        d.line([(cx, _y(hi2, top, h)), (cx, _y(lo2, top, h))], fill=color, width=3)
        y1, y2 = sorted([_y(o2, top, h), _y(c2, top, h)])
        d.rounded_rectangle([cx - cw / 2, y1, cx + cw / 2, max(y2, y1 + 3)], radius=3, fill=color)


def _draw_line(img, d, pattern, left, top, w, h, rnd):
    line_color = rnd.choice(_LINE_COLORS)
    shift = rnd.uniform(-0.05, 0.05)
    pts = [(left + (x + rnd.uniform(-0.008, 0.008)) * w,
            _y(_clip(y + shift + rnd.uniform(-0.02, 0.02)), top, h)) for x, y in pattern["path"]]
    d.line(pts, fill=line_color + (255,), width=6, joint="curve")
    for p in pts:
        d.ellipse([p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4], fill=line_color + (255,))

    for label, yv, kind in pattern.get("hlines", []):
        color = _DOWN if kind == "down" else _UP if kind == "up" else _GRID
        yy = _y(_clip(yv + shift), top, h)
        _dashed_h(d, left, left + w, yy, color + (220,))
        f = _font(26)
        tb = d.textbbox((0, 0), label, font=f)
        d.text((left + w - (tb[2] - tb[0]), yy - 34), label, font=f, fill=color + (255,))

    for (x1, y1), (x2, y2) in pattern.get("trendlines", []):
        d.line([(left + x1 * w, _y(_clip(y1 + shift), top, h)),
                (left + x2 * w, _y(_clip(y2 + shift), top, h))], fill=_GRID + (200,), width=3)
