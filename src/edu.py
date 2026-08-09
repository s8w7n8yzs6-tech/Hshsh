"""Desenha o diagrama esquemático de um padrão gráfico (didático).

Recebe um padrão de src/patterns.py e devolve uma imagem RGBA com o diagrama —
velas (candlestick) ou linha de preço com suporte/resistência/tendência — para
compor no card educativo. São ilustrações didáticas, não dados reais.
"""
from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont

_UP = (34, 197, 94)      # alta
_DOWN = (239, 68, 68)    # baixa
_LINE = (56, 189, 248)   # linha de preço (ciano)
_GRID = (148, 163, 184)

_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def _font(size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(_SANS, size)
    except OSError:
        return ImageFont.load_default()


def _y(v: float, top: int, h: int) -> float:
    """Converte preço normalizado (0..1, 1=topo) para pixel Y."""
    return top + (1.0 - v) * h


def _dashed_h(d: ImageDraw.ImageDraw, x0: int, x1: int, y: float, color, width=3, dash=16, gap=12):
    x = x0
    while x < x1:
        d.line([(x, y), (min(x + dash, x1), y)], fill=color, width=width)
        x += dash + gap


def render_pattern(pattern: dict, width: int, height: int) -> Image.Image:
    """Diagrama do padrão numa imagem RGBA transparente (width x height)."""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pad = int(width * 0.06)
    top, left = pad, pad
    plot_w, plot_h = width - 2 * pad, height - 2 * pad

    # grade horizontal tênue
    for i in range(1, 5):
        gy = top + plot_h * i / 5
        d.line([(left, gy), (left + plot_w, gy)], fill=_GRID + (28,), width=1)

    if pattern["tipo"] == "candles":
        _draw_candles(d, pattern["candles"], left, top, plot_w, plot_h)
    else:
        _draw_line(img, d, pattern, left, top, plot_w, plot_h)
    return img


def _draw_candles(d, candles, left, top, w, h):
    n = len(candles)
    slot = w / n
    cw = slot * 0.5
    for i, (o, hi, lo, c) in enumerate(candles):
        cx = left + slot * (i + 0.5)
        color = _UP if c >= o else _DOWN
        d.line([(cx, _y(hi, top, h)), (cx, _y(lo, top, h))], fill=color, width=3)
        y1, y2 = sorted([_y(o, top, h), _y(c, top, h)])
        d.rounded_rectangle([cx - cw / 2, y1, cx + cw / 2, max(y2, y1 + 3)], radius=3, fill=color)


def _draw_line(img, d, pattern, left, top, w, h):
    pts = [(left + x * w, _y(y, top, h)) for x, y in pattern["path"]]
    # linha de preço com leve brilho
    d.line(pts, fill=_LINE + (255,), width=6, joint="curve")
    for p in pts:
        d.ellipse([p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4], fill=_LINE + (255,))

    # linhas horizontais (suporte/resistência/pescoço) com rótulo
    for label, yv, kind in pattern.get("hlines", []):
        color = _DOWN if kind == "down" else _UP if kind == "up" else _GRID
        yy = _y(yv, top, h)
        _dashed_h(d, left, left + w, yy, color + (220,))
        f = _font(26)
        tb = d.textbbox((0, 0), label, font=f)
        tw = tb[2] - tb[0]
        d.text((left + w - tw, yy - 34), label, font=f, fill=color + (255,))

    # linhas de tendência (triângulo)
    for (x1, y1), (x2, y2) in pattern.get("trendlines", []):
        d.line([(left + x1 * w, _y(y1, top, h)), (left + x2 * w, _y(y2, top, h))],
               fill=_GRID + (200,), width=3)
