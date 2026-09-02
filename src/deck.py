"""Carrossel editorial de nível agência sobre um assunto em alta do mercado BR.

Sistema de design robusto: barra de progresso, kicker com tracking, tipografia
serifada de display, numerais gigantes como elemento gráfico, paleta sofisticada
e rodapé com paginação. Sem foto — o peso é do design e da tipografia.
"""
from __future__ import annotations

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

_W, _H = 1080, 1350
_M = 96

_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
_SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
_MONO_B = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"

# Paletas sofisticadas (bg, painel, fg, muted, accent, accent2).
PALETTES = [
    {"bg": (13, 20, 38), "panel": (22, 31, 56), "fg": (244, 247, 252), "muted": (146, 162, 194), "accent": (233, 181, 86), "accent2": (120, 150, 255)},
    {"bg": (16, 17, 21), "panel": (26, 27, 33), "fg": (245, 244, 242), "muted": (150, 150, 158), "accent": (255, 107, 74), "accent2": (255, 205, 120)},
    {"bg": (9, 26, 22), "panel": (15, 38, 32), "fg": (238, 247, 242), "muted": (146, 182, 168), "accent": (163, 230, 53), "accent2": (94, 234, 212)},
    {"bg": (24, 13, 30), "panel": (37, 22, 45), "fg": (247, 240, 250), "muted": (188, 168, 200), "accent": (244, 114, 182), "accent2": (167, 139, 250)},
    {"bg": (243, 240, 232), "panel": (233, 229, 218), "fg": (22, 22, 26), "muted": (108, 106, 100), "accent": (204, 64, 52), "accent2": (37, 99, 235), "light": True},
    {"bg": (15, 18, 24), "panel": (24, 29, 38), "fg": (240, 244, 250), "muted": (148, 158, 172), "accent": (56, 189, 248), "accent2": (52, 211, 153)},
]


def palette(seed: int) -> dict:
    return PALETTES[seed % len(PALETTES)]


def _font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(_SANS_B, size)


def _bg(pal: dict) -> Image.Image:
    top = pal["bg"]
    bot = tuple(max(0, c - 8) for c in top) if not pal.get("light") else tuple(min(255, c + 4) for c in top)
    img = Image.new("RGB", (_W, _H), top)
    d = ImageDraw.Draw(img)
    for y in range(_H):
        t = y / (_H - 1)
        d.line([(0, y), (_W, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    return img.convert("RGBA")


def _wrap_fit(d, text, font_path, max_w, max_h, hi, lo, ratio=0.16):
    wrapped, font, sp = text, _font(font_path, lo), int(lo * ratio)
    for size in range(hi, lo - 2, -3):
        font = _font(font_path, size)
        avg = d.textlength("médio", font=font) / 5 or 1
        wrapped = "\n".join(textwrap.wrap(text, width=max(6, int(max_w / avg)))) or text
        sp = int(size * ratio)
        bb = d.multiline_textbbox((0, 0), wrapped, font=font, spacing=sp)
        if (bb[2] - bb[0]) <= max_w and (bb[3] - bb[1]) <= max_h:
            return wrapped, font, sp
    return wrapped, font, sp


def _tracked(d, xy, text, font, fill, tracking=6):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + tracking
    return x


def _progress(d, pal, frac):
    d.rectangle([0, 0, _W, 8], fill=pal["panel"])
    d.rectangle([0, 0, int(_W * max(0.06, min(1.0, frac))), 8], fill=pal["accent"])


def _eyebrow(d, pal, text, y=_M + 8):
    d.rectangle([_M, y + 4, _M + 22, y + 26], fill=pal["accent"])
    ef = _font(_SANS_B, 26)
    _tracked(d, (_M + 40, y), text.upper(), ef, pal["muted"], tracking=6)


def _dotgrid(img, pal, x0, y0, cols, rows, gap=26, r=3):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for i in range(cols):
        for j in range(rows):
            cx, cy = x0 + i * gap, y0 + j * gap
            ld.ellipse([cx - r, cy - r, cx + r, cy + r], fill=pal["muted"] + (60,))
    img.alpha_composite(layer)


def _footer(d, pal, handle, page, total):
    y = _H - 92
    d.line([(_M, y), (_W - _M, y)], fill=pal["panel"], width=2)
    hf = _font(_SANS_B, 30)
    d.ellipse([_M, y + 26, _M + 16, y + 42], fill=pal["accent"])
    d.text((_M + 30, y + 20), handle, font=hf, fill=pal["muted"])
    pf = _font(_MONO_B, 30)
    txt = f"{page:02d} / {total:02d}"
    tb = d.textbbox((0, 0), txt, font=pf)
    d.text((_W - _M - (tb[2] - tb[0]), y + 20), txt, font=pf, fill=pal["fg"])


def build_topic_deck(kicker: str, cover: str, slides: list, source: str, handle: str,
                     out_dir: str, seed: int = 0) -> list:
    pal = palette(seed)
    slides = [s for s in (slides or []) if s.get("titulo") or s.get("texto")][:6]
    total = 1 + len(slides) + 1
    os.makedirs(out_dir, exist_ok=True)
    paths: list[str] = []

    def save(img, i):
        p = os.path.join(out_dir, f"slide_{i:02d}.png")
        img.convert("RGB").save(p, "PNG")
        paths.append(p)

    # ---------- CAPA ----------
    img = _bg(pal)
    d = ImageDraw.Draw(img)
    _progress(d, pal, 1 / total)
    # anel decorativo sangrando pela borda + bloco de acento
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.ellipse([_W - 250, 150, _W + 210, 610], outline=pal["accent"] + (150,), width=6)
    od.ellipse([_W - 150, 300, _W - 40, 410], fill=pal["accent2"] + (60,))
    img.alpha_composite(ov)
    _dotgrid(img, pal, _M, _H - 360, 7, 5)

    _eyebrow(d, pal, kicker)
    d.line([(_M, _M + 70), (_M + 120, _M + 70)], fill=pal["accent"], width=4)
    # headline (serif display), ancorada no topo e medida para posicionar o resto
    hy = int(_H * 0.30)
    hw, hf, hsp = _wrap_fit(d, cover, _SERIF_B, _W - 2 * _M, 600, 104, 58, ratio=0.14)
    d.multiline_text((_M, hy), hw, font=hf, fill=pal["fg"], spacing=hsp)
    hb = d.multiline_textbbox((_M, hy), hw, font=hf, spacing=hsp)
    sf = _font(_SANS_R, 30)
    d.text((_M, hb[3] + 34), f"O que movimentou o mercado brasileiro · {source or 'esta semana'}",
           font=sf, fill=pal["muted"])
    # arraste
    af = _font(_SANS_B, 28)
    txt = "ARRASTE  →"
    tb = d.textbbox((0, 0), txt, font=af)
    d.rounded_rectangle([_M, _H - 168, _M + (tb[2] - tb[0]) + 54, _H - 168 + (tb[3] - tb[1]) + 30],
                        radius=30, fill=pal["accent"])
    d.text((_M + 27, _H - 168 + 15 - tb[1]), txt, font=af, fill=pal["bg"])
    save(img, 0)

    # ---------- CAPÍTULOS ----------
    for i, s in enumerate(slides):
        img = _bg(pal)
        d = ImageDraw.Draw(img)
        _progress(d, pal, (i + 2) / total)
        # numeral gigante (marca d'água)
        ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
        od = ImageDraw.Draw(ov)
        nf = _font(_SERIF_B, 460)
        od.text((_W - 430, -70), f"{i + 1}", font=nf, fill=pal["accent"] + (36,))
        img.alpha_composite(ov)

        _eyebrow(d, pal, f"Ponto {i + 1:02d} de {len(slides):02d}")
        ty = _M + 150
        tw, tf, tsp = _wrap_fit(d, s.get("titulo", ""), _SERIF_B, _W - 2 * _M, 260, 78, 46, ratio=0.14)
        d.multiline_text((_M, ty), tw, font=tf, fill=pal["fg"], spacing=tsp)
        tb2 = d.multiline_textbbox((_M, ty), tw, font=tf, spacing=tsp)
        d.rectangle([_M, tb2[3] + 34, _M + 96, tb2[3] + 42], fill=pal["accent"])
        bw, bf, bsp = _wrap_fit(d, s.get("texto", ""), _SANS_R, _W - 2 * _M,
                                _H - 210 - (tb2[3] + 80), 46, 30, ratio=0.24)
        d.multiline_text((_M, tb2[3] + 82), bw, font=bf, fill=pal["muted"], spacing=bsp)
        _footer(d, pal, handle, i + 2, total)
        save(img, i + 1)

    # ---------- CTA ----------
    img = _bg(pal)
    d = ImageDraw.Draw(img)
    _progress(d, pal, 1.0)
    _dotgrid(img, pal, _W - _M - 160, _M + 40, 6, 4)
    _eyebrow(d, pal, "Toda semana por aqui")
    cy = int(_H * 0.32)
    cw, cf, csp = _wrap_fit(d, "Salve. Compartilhe.", _SERIF_B, _W - 2 * _M, 380, 104, 60, ratio=0.16)
    d.multiline_text((_M, cy), cw, font=cf, fill=pal["fg"], spacing=csp)
    cb = d.multiline_textbbox((_M, cy), cw, font=cf, spacing=csp)
    d.rectangle([_M, cb[3] + 54, _M + 110, cb[3] + 64], fill=pal["accent"])
    hf = _font(_SANS_B, 60)
    d.text((_M, cb[3] + 96), handle, font=hf, fill=pal["accent"])
    sf = _font(_SANS_R, 32)
    d.text((_M, cb[3] + 186), "O resumo do mercado brasileiro, sem enrolação.",
           font=sf, fill=pal["muted"])
    save(img, total - 1)

    return paths
