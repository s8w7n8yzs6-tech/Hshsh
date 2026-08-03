"""Cena cinematográfica de trader para o fundo do card.

Desenha, de forma 100% programática (sem depender de fotos externas), a silhueta
de um trader visto de costas diante de monitores que brilham com candlesticks —
o clima "trader na frente do PC de madrugada". Cada cena varia (paleta, número de
telas, padrão dos candles) conforme uma semente, para nunca sair repetida.
"""
from __future__ import annotations

import random

from PIL import Image, ImageDraw, ImageFilter

# Paletas de brilho (accent) — o neon que sai das telas. Rotacionam por semente.
PALETTES = [
    {"glow": (56, 189, 248), "bg_top": (10, 16, 30), "bg_bottom": (4, 6, 12)},    # ciano
    {"glow": (45, 212, 191), "bg_top": (10, 24, 26), "bg_bottom": (3, 9, 10)},    # teal
    {"glow": (129, 140, 248), "bg_top": (16, 14, 34), "bg_bottom": (6, 5, 14)},   # índigo
    {"glow": (251, 191, 36), "bg_top": (26, 18, 8), "bg_bottom": (10, 7, 3)},     # âmbar
    {"glow": (244, 114, 182), "bg_top": (28, 12, 24), "bg_bottom": (10, 4, 9)},   # magenta
    {"glow": (52, 211, 153), "bg_top": (8, 24, 20), "bg_bottom": (3, 10, 8)},     # esmeralda
]

_UP = (34, 197, 94)      # candle de alta
_DOWN = (239, 68, 68)    # candle de baixa


def palette_for(seed: int) -> dict:
    return PALETTES[seed % len(PALETTES)]


def _vgradient(w: int, h: int, top: tuple, bottom: tuple) -> Image.Image:
    img = Image.new("RGB", (w, h), top)
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / (h - 1)
        d.line([(0, y), (w, y)], fill=tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return img


def _glow(size: tuple[int, int], center: tuple[int, int], radius: int, color: tuple, alpha: int) -> Image.Image:
    """Um brilho radial suave (elipse borrada) em uma camada RGBA transparente."""
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = center
    d.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=color + (alpha,))
    return layer.filter(ImageFilter.GaussianBlur(radius * 0.55))


def _candles(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], rnd: random.Random) -> None:
    """Desenha candlesticks fictícios dentro da 'tela' de um monitor."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    n = max(6, w // 18)
    slot = w / n
    cw = slot * 0.6
    price = rnd.uniform(0.35, 0.65)
    for i in range(n):
        drift = rnd.uniform(-0.08, 0.08)
        o = price
        price = min(0.92, max(0.08, price + drift))
        c = price
        hi = max(o, c) + rnd.uniform(0.01, 0.06)
        lo = min(o, c) - rnd.uniform(0.01, 0.06)
        col = _UP if c >= o else _DOWN
        cx = x0 + slot * (i + 0.5)

        def py(v: float) -> float:
            return y1 - max(0.02, min(0.98, v)) * h

        draw.line([(cx, py(hi)), (cx, py(lo))], fill=col, width=1)
        top, bot = sorted([py(o), py(c)])
        draw.rectangle([cx - cw / 2, top, cx + cw / 2, max(bot, top + 1)], fill=col)


def _monitor(base: Image.Image, box: tuple[int, int, int, int], glow: tuple, rnd: random.Random,
             screen_img: Image.Image | None = None) -> None:
    """Um monitor: moldura fina, tela escura com candles (ou uma imagem) e brilho."""
    x0, y0, x1, y1 = box
    # Brilho por trás da tela.
    g = _glow(base.size, ((x0 + x1) // 2, (y0 + y1) // 2), int((x1 - x0) * 0.55), glow, 120)
    base.alpha_composite(g)

    panel = Image.new("RGBA", base.size, (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel)
    pd.rounded_rectangle(box, radius=10, fill=(8, 12, 18, 255), outline=glow + (255,), width=2)
    base.alpha_composite(panel)

    inset = (x0 + 10, y0 + 10, x1 - 10, y1 - 10)
    if screen_img is not None:
        iw, ih = inset[2] - inset[0], inset[3] - inset[1]
        fit = screen_img.copy()
        fit.thumbnail((iw, ih))
        ox = inset[0] + (iw - fit.width) // 2
        oy = inset[1] + (ih - fit.height) // 2
        base.alpha_composite(fit, (ox, oy))
    else:
        sd = ImageDraw.Draw(base)
        # linhas de grade tênues
        for gy in range(inset[1], inset[3], 22):
            sd.line([(inset[0], gy), (inset[2], gy)], fill=(148, 163, 184, 28), width=1)
        _candles(sd, inset, rnd)


def _silhouette(base: Image.Image, glow: tuple) -> None:
    """Silhueta de uma pessoa vista de costas, em primeiro plano, com luz de recorte."""
    w, h = base.size
    cx = w // 2
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    body_top = int(h * 0.72)
    head_r = int(w * 0.085)
    head_cy = body_top - head_r + 6
    dark = (5, 8, 12, 255)

    # Ombros/tronco: trapézio arredondado que se alarga até a base.
    d.polygon(
        [
            (cx - int(w * 0.16), h),
            (cx - int(w * 0.135), body_top),
            (cx - int(w * 0.06), body_top - int(h * 0.03)),
            (cx + int(w * 0.06), body_top - int(h * 0.03)),
            (cx + int(w * 0.135), body_top),
            (cx + int(w * 0.16), h),
        ],
        fill=dark,
    )
    d.ellipse([cx - int(w * 0.16), h - 220, cx + int(w * 0.16), h + 60], fill=dark)
    # Cabeça.
    d.ellipse([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r], fill=dark)
    # Pescoço.
    d.rectangle([cx - int(w * 0.045), head_cy, cx + int(w * 0.045), body_top], fill=dark)

    base.alpha_composite(layer)

    # Luz de recorte (rim light) das telas na borda superior de cabeça e ombros.
    rim = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rim)
    rd.arc([cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r], 200, 340, fill=glow + (230,), width=4)
    rd.line([(cx - int(w * 0.135), body_top), (cx - int(w * 0.06), body_top - int(h * 0.03))],
            fill=glow + (180,), width=4)
    rd.line([(cx + int(w * 0.06), body_top - int(h * 0.03)), (cx + int(w * 0.135), body_top)],
            fill=glow + (180,), width=4)
    base.alpha_composite(rim.filter(ImageFilter.GaussianBlur(1.5)))


def render_scene(width: int, height: int, seed: int = 0,
                 screen_img: Image.Image | None = None) -> Image.Image:
    """Cena completa: fundo, monitores brilhando e o trader de costas em 1º plano."""
    rnd = random.Random(seed)
    pal = palette_for(seed)
    glow = pal["glow"]

    base = _vgradient(width, height, pal["bg_top"], pal["bg_bottom"]).convert("RGBA")

    # Brilho ambiente amplo atrás dos monitores.
    base.alpha_composite(_glow((width, height), (width // 2, int(height * 0.5)), int(width * 0.6), glow, 60))

    # Cluster de monitores (o central maior; laterais quando couber).
    mid = width // 2
    top = int(height * 0.48)
    cw, chh = int(width * 0.44), int(height * 0.20)
    center_box = (mid - cw // 2, top, mid + cw // 2, top + chh)

    side = screen_img is None and rnd.random() > 0.35
    if side:
        sw, shh = int(width * 0.22), int(height * 0.13)
        sy = top + int(chh * 0.28)
        _monitor(base, (center_box[0] - sw - 24, sy, center_box[0] - 24, sy + shh), glow, rnd)
        _monitor(base, (center_box[2] + 24, sy, center_box[2] + sw + 24, sy + shh), glow, rnd)

    _monitor(base, center_box, glow, rnd, screen_img=screen_img)

    # Reflexo/brilho na "mesa" logo abaixo dos monitores.
    desk = _glow((width, height), (mid, int(height * 0.72)), int(width * 0.5), glow, 34)
    base.alpha_composite(desk)

    _silhouette(base, glow)
    return base
