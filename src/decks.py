"""Vários SISTEMAS DE DESIGN de carrossel que se alternam por post.

Cada estilo é uma linguagem visual distinta e forte (para parar o scroll):
- editorial : revista sofisticada, serifada, com numeral gigante
- terminal  : dark trader/tech, mono, grid, neon, marcas de canto
- brutal    : pôster suíço/brutalista, tipografia enorme em caixa-alta, blocos
- gradient  : moderno vibrante, fundo em gradiente, cartão translúcido

build() escolhe o estilo por semente, então posts vizinhos ficam diferentes.
"""
from __future__ import annotations

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont, ImageFilter

_W, _H = 1080, 1350
_M = 96

_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
_SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
_MONO_B = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"
_MONO_R = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"


def _f(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(_SANS_B, size)


def _fit(d, text, path, max_w, max_h, hi, lo, ratio=0.14, upper=False):
    t = text.upper() if upper else text
    wrapped, font, sp = t, _f(path, lo), int(lo * ratio)
    for size in range(hi, lo - 2, -3):
        font = _f(path, size)
        avg = d.textlength("MÉDIO", font=font) / 5 or 1
        wrapped = "\n".join(textwrap.wrap(t, width=max(5, int(max_w / avg)))) or t
        sp = int(size * ratio)
        bb = d.multiline_textbbox((0, 0), wrapped, font=font, spacing=sp)
        if (bb[2] - bb[0]) <= max_w and (bb[3] - bb[1]) <= max_h:
            return wrapped, font, sp
    return wrapped, font, sp


def _tracked(d, xy, text, font, fill, tr=6):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + tr
    return x


def _mtext_bottom(d, xy, wrapped, font, sp):
    bb = d.multiline_textbbox(xy, wrapped, font=font, spacing=sp)
    return bb[3]


def _clean_slides(slides):
    return [s for s in (slides or []) if s.get("titulo") or s.get("texto")][:5]


# ======================================================================
# ESTILO 1 — EDITORIAL (revista serifada)
# ======================================================================
_EDITORIAL_PALS = [
    {"bg": (13, 20, 38), "fg": (244, 247, 252), "muted": (150, 165, 195), "accent": (233, 181, 86)},
    {"bg": (243, 240, 232), "fg": (22, 22, 26), "muted": (110, 108, 102), "accent": (204, 64, 52), "light": True},
    {"bg": (16, 17, 21), "fg": (245, 244, 242), "muted": (150, 150, 158), "accent": (255, 107, 74)},
]


def _bg_flat(color):
    return Image.new("RGBA", (_W, _H), color + (255,))


def _editorial(cover, slides, source, handle, out_dir, seed, save):
    pal = _EDITORIAL_PALS[seed % len(_EDITORIAL_PALS)]
    total = 2 + len(slides)

    def base(frac):
        img = _bg_flat(pal["bg"])
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, _W, 8], fill=tuple(min(255, c + 24) for c in pal["bg"]))
        d.rectangle([0, 0, int(_W * frac), 8], fill=pal["accent"])
        return img, d

    def eyebrow(d, text, y=_M + 8):
        d.rectangle([_M, y + 4, _M + 22, y + 26], fill=pal["accent"])
        _tracked(d, (_M + 40, y), text.upper(), _f(_SANS_B, 26), pal["muted"], 6)

    # capa
    img, d = base(1 / total)
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.ellipse([_W - 250, 150, _W + 210, 610], outline=pal["accent"] + (150,), width=6)
    img.alpha_composite(ov)
    eyebrow(d, "Mercado no Brasil · Esta semana")
    hy = int(_H * 0.30)
    hw, hf, hsp = _fit(d, cover, _SERIF_B, _W - 2 * _M, 600, 104, 58)
    d.multiline_text((_M, hy), hw, font=hf, fill=pal["fg"], spacing=hsp)
    b = _mtext_bottom(d, (_M, hy), hw, hf, hsp)
    d.text((_M, b + 34), f"O que movimentou o mercado · {source or 'esta semana'}",
           font=_f(_SANS_R, 30), fill=pal["muted"])
    af = _f(_SANS_B, 28)
    tb = d.textbbox((0, 0), "ARRASTE  →", font=af)
    d.rounded_rectangle([_M, _H - 168, _M + (tb[2] - tb[0]) + 54, _H - 168 + (tb[3] - tb[1]) + 30],
                        radius=30, fill=pal["accent"])
    d.text((_M + 27, _H - 168 + 15 - tb[1]), "ARRASTE  →", font=af, fill=pal["bg"])
    save(img, 0)

    for i, s in enumerate(slides):
        img, d = base((i + 2) / total)
        ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(ov).text((_W - 430, -70), f"{i + 1}", font=_f(_SERIF_B, 460), fill=pal["accent"] + (34,))
        img.alpha_composite(ov)
        eyebrow(d, f"Ponto {i + 1:02d} de {len(slides):02d}")
        ty = _M + 150
        tw, tf, tsp = _fit(d, s.get("titulo", ""), _SERIF_B, _W - 2 * _M, 250, 76, 44)
        d.multiline_text((_M, ty), tw, font=tf, fill=pal["fg"], spacing=tsp)
        b = _mtext_bottom(d, (_M, ty), tw, tf, tsp)
        d.rectangle([_M, b + 34, _M + 96, b + 42], fill=pal["accent"])
        bw, bf, bsp = _fit(d, s.get("texto", ""), _SANS_R, _W - 2 * _M, _H - 220 - b, 46, 30, 0.24)
        d.multiline_text((_M, b + 82), bw, font=bf, fill=pal["muted"], spacing=bsp)
        _editorial_footer(d, pal, handle, i + 2, total)
        save(img, i + 1)

    img, d = base(1.0)
    eyebrow(d, "Toda semana por aqui")
    cw, cf, csp = _fit(d, "Salve. Compartilhe.", _SERIF_B, _W - 2 * _M, 360, 104, 60, 0.16)
    d.multiline_text((_M, int(_H * 0.34)), cw, font=cf, fill=pal["fg"], spacing=csp)
    b = _mtext_bottom(d, (_M, int(_H * 0.34)), cw, cf, csp)
    d.rectangle([_M, b + 54, _M + 110, b + 64], fill=pal["accent"])
    d.text((_M, b + 96), handle, font=_f(_SANS_B, 58), fill=pal["accent"])
    save(img, total - 1)


def _editorial_footer(d, pal, handle, page, total):
    y = _H - 92
    d.line([(_M, y), (_W - _M, y)], fill=tuple(min(255, c + 24) for c in pal["bg"]), width=2)
    d.ellipse([_M, y + 26, _M + 16, y + 42], fill=pal["accent"])
    d.text((_M + 30, y + 20), handle, font=_f(_SANS_B, 30), fill=pal["muted"])
    txt = f"{page:02d} / {total:02d}"
    tb = d.textbbox((0, 0), txt, font=_f(_MONO_B, 30))
    d.text((_W - _M - (tb[2] - tb[0]), y + 20), txt, font=_f(_MONO_B, 30), fill=pal["fg"])


# ======================================================================
# ESTILO 2 — TERMINAL (dark trader/tech)
# ======================================================================
_TERMINAL_PALS = [
    {"bg": (7, 10, 12), "fg": (226, 240, 236), "muted": (110, 130, 128), "accent": (0, 230, 140)},
    {"bg": (7, 10, 16), "fg": (228, 238, 248), "muted": (110, 126, 150), "accent": (56, 220, 255)},
    {"bg": (12, 9, 14), "fg": (240, 233, 244), "muted": (140, 120, 148), "accent": (191, 130, 255)},
]


def _terminal(cover, slides, source, handle, out_dir, seed, save):
    pal = _TERMINAL_PALS[seed % len(_TERMINAL_PALS)]
    total = 2 + len(slides)
    ac = pal["accent"]

    def base():
        img = _bg_flat(pal["bg"])
        d = ImageDraw.Draw(img)
        for x in range(0, _W, 90):
            d.line([(x, 0), (x, _H)], fill=ac + (14,))
        for y in range(0, _H, 90):
            d.line([(0, y), (_W, y)], fill=ac + (14,))
        for cx, cy, sx, sy in [(46, 46, 1, 1), (_W - 46, 46, -1, 1), (46, _H - 46, 1, -1), (_W - 46, _H - 46, -1, -1)]:
            d.line([(cx, cy), (cx + 34 * sx, cy)], fill=ac, width=3)
            d.line([(cx, cy), (cx, cy + 34 * sy)], fill=ac, width=3)
        return img, d

    def tag(d, text):
        mf = _f(_MONO_B, 28)
        x = _tracked(d, (_M, _M), text, mf, ac, 2)
        d.rectangle([x + 12, _M - 2, x + 34, _M + 30], fill=ac)  # cursor

    img, d = base()
    tag(d, "// MERCADO_BR")
    hy = int(_H * 0.32)
    hw, hf, hsp = _fit(d, cover, _SANS_B, _W - 2 * _M, 560, 100, 54, upper=False)
    d.multiline_text((_M, hy), hw, font=hf, fill=pal["fg"], spacing=hsp)
    b = _mtext_bottom(d, (_M, hy), hw, hf, hsp)
    d.rectangle([_M, b + 34, _M + 130, b + 40], fill=ac)
    d.text((_M, b + 70), f"> fonte: {source or 'manchetes da semana'}", font=_f(_MONO_R, 28), fill=pal["muted"])
    d.text((_M, _H - 150), "swipe →", font=_f(_MONO_B, 34), fill=ac)
    save(img, 0)

    for i, s in enumerate(slides):
        img, d = base()
        tag(d, f"// PONTO_{i + 1:02d}")
        ty = _M + 120
        tw, tf, tsp = _fit(d, s.get("titulo", ""), _SANS_B, _W - 2 * _M, 220, 72, 42)
        d.multiline_text((_M, ty), tw, font=tf, fill=ac, spacing=tsp)
        b = _mtext_bottom(d, (_M, ty), tw, tf, tsp)
        bw, bf, bsp = _fit(d, s.get("texto", ""), _MONO_R, _W - 2 * _M, _H - 240 - b, 40, 26, 0.34)
        d.multiline_text((_M, b + 48), bw, font=bf, fill=pal["fg"], spacing=bsp)
        d.text((_M, _H - 132), handle, font=_f(_MONO_B, 28), fill=pal["muted"])
        pg = f"{i + 2:02d}/{total:02d}"
        tb = d.textbbox((0, 0), pg, font=_f(_MONO_B, 28))
        d.text((_W - _M - (tb[2] - tb[0]), _H - 132), pg, font=_f(_MONO_B, 28), fill=ac)
        save(img, i + 1)

    img, d = base()
    tag(d, "// SEGUE")
    cw, cf, csp = _fit(d, "SALVE E SIGA", _SANS_B, _W - 2 * _M, 300, 110, 60, upper=True)
    d.multiline_text((_M, int(_H * 0.36)), cw, font=cf, fill=pal["fg"], spacing=csp)
    d.text((_M, int(_H * 0.60)), handle, font=_f(_MONO_B, 52), fill=ac)
    d.text((_M, int(_H * 0.60) + 78), "> o mercado_br, sem ruido", font=_f(_MONO_R, 28), fill=pal["muted"])
    save(img, total - 1)


# ======================================================================
# ESTILO 3 — BRUTAL (pôster suíço, caixa-alta enorme)
# ======================================================================
_BRUTAL_PALS = [
    {"bg": (13, 13, 15), "fg": (245, 245, 245), "block": (255, 61, 61), "on": (255, 255, 255)},
    {"bg": (240, 237, 229), "fg": (16, 16, 18), "block": (28, 74, 255), "on": (255, 255, 255), "light": True},
    {"bg": (17, 17, 19), "fg": (245, 245, 245), "block": (190, 255, 60), "on": (17, 17, 19)},
    {"bg": (245, 243, 238), "fg": (16, 16, 18), "block": (16, 16, 18), "on": (245, 243, 238), "light": True},
]


def _brutal(cover, slides, source, handle, out_dir, seed, save):
    pal = _BRUTAL_PALS[seed % len(_BRUTAL_PALS)]
    total = 2 + len(slides)
    blk, on = pal["block"], pal["on"]

    # capa: bloco de cor no topo + manchete gigante caixa-alta
    img = _bg_flat(pal["bg"])
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, _W, 280], fill=blk)
    kf = _f(_SANS_B, 30)
    _tracked(d, (_M, 90), "MERCADO BR", kf, on, 8)
    _tracked(d, (_M, 150), "ESTA SEMANA", kf, on, 8)
    hw, hf, hsp = _fit(d, cover, _SANS_B, _W - 2 * _M, 700, 132, 66, 0.06, upper=True)
    d.multiline_text((_M, 360), hw, font=hf, fill=pal["fg"], spacing=hsp)
    d.text((_M, _H - 150), (source or "MANCHETES DA SEMANA").upper(), font=_f(_SANS_B, 26), fill=blk)
    save(img, 0)

    for i, s in enumerate(slides):
        img = _bg_flat(pal["bg"])
        d = ImageDraw.Draw(img)
        # numeral gigante em bloco na lateral
        d.rectangle([0, _M, 150, _M + 170], fill=blk)
        nf = _f(_SANS_B, 150)
        nb = d.textbbox((0, 0), str(i + 1), font=nf)
        d.text((75 - (nb[2] - nb[0]) / 2 - nb[0], _M + 85 - (nb[3] - nb[1]) / 2 - nb[1]), str(i + 1), font=nf, fill=on)
        tw, tf, tsp = _fit(d, s.get("titulo", ""), _SANS_B, _W - 2 * _M, 240, 92, 46, 0.06, upper=True)
        ty = _M + 210
        d.multiline_text((_M, ty), tw, font=tf, fill=pal["fg"], spacing=tsp)
        b = _mtext_bottom(d, (_M, ty), tw, tf, tsp)
        d.rectangle([_M, b + 30, _W - _M, b + 36], fill=blk)
        bw, bf, bsp = _fit(d, s.get("texto", ""), _SANS_R, _W - 2 * _M, _H - 210 - b, 48, 30, 0.24)
        d.multiline_text((_M, b + 70), bw, font=bf, fill=pal["fg"], spacing=bsp)
        d.text((_M, _H - 128), handle, font=_f(_SANS_B, 30), fill=pal["fg"])
        pg = f"{i + 2:02d}/{total:02d}"
        tb = d.textbbox((0, 0), pg, font=_f(_SANS_B, 30))
        d.text((_W - _M - (tb[2] - tb[0]), _H - 128), pg, font=_f(_SANS_B, 30), fill=blk)
        save(img, i + 1)

    img = _bg_flat(blk)
    d = ImageDraw.Draw(img)
    cw, cf, csp = _fit(d, "SALVE. COMPARTILHE.", _SANS_B, _W - 2 * _M, 500, 120, 60, 0.08, upper=True)
    d.multiline_text((_M, int(_H * 0.30)), cw, font=cf, fill=on, spacing=csp)
    d.rectangle([_M, int(_H * 0.66), _M + 140, int(_H * 0.66) + 12], fill=on)
    d.text((_M, int(_H * 0.66) + 44), handle, font=_f(_SANS_B, 60), fill=on)
    save(img, total - 1)


# ======================================================================
# ESTILO 4 — GRADIENT (moderno vibrante)
# ======================================================================
_GRADIENTS = [
    ((124, 58, 237), (236, 72, 153)),   # violeta → rosa
    ((37, 99, 235), (56, 189, 248)),    # azul → ciano
    ((244, 63, 94), (251, 146, 60)),    # vermelho → laranja
    ((5, 150, 105), (163, 230, 53)),    # verde → lima
    ((30, 27, 75), (124, 58, 237)),     # índigo → violeta
]


def _diag_gradient(c1, c2):
    img = Image.new("RGB", (_W, _H))
    px = img.load()
    for y in range(_H):
        for x in range(0, _W, 4):
            t = (x / _W + y / _H) / 2
            c = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
            for dx in range(4):
                if x + dx < _W:
                    px[x + dx, y] = c
    return img.convert("RGBA")


def _blob(img, center, r, color, alpha):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse([center[0] - r, center[1] - r, center[0] + r, center[1] + r], fill=color + (alpha,))
    img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(r * 0.5)))


def _gradient(cover, slides, source, handle, out_dir, seed, save):
    c1, c2 = _GRADIENTS[seed % len(_GRADIENTS)]
    total = 2 + len(slides)
    W = (255, 255, 255)

    def base():
        img = _diag_gradient(c1, c2)
        _blob(img, (_W - 120, 180), 300, (255, 255, 255), 60)
        _blob(img, (120, _H - 160), 320, (0, 0, 0), 50)
        return img, ImageDraw.Draw(img)

    def pill(d, text, y=_M):
        pf = _f(_SANS_B, 26)
        text = text.upper()
        w = sum(d.textlength(ch, font=pf) + 4 for ch in text) - 4
        tb = d.textbbox((0, 0), text, font=pf)
        h = tb[3] - tb[1]
        d.rounded_rectangle([_M, y, _M + int(w) + 46, y + h + 26], radius=(h + 26) // 2, fill=(8, 10, 18, 180))
        _tracked(d, (_M + 23, y + 13 - tb[1]), text, pf, W, 4)

    img, d = base()
    pill(d, "Mercado no Brasil · Esta semana")
    hy = int(_H * 0.30)
    hw, hf, hsp = _fit(d, cover, _SANS_B, _W - 2 * _M, 620, 118, 60, 0.1)
    # sombra p/ legibilidade
    d.multiline_text((_M + 3, hy + 4), hw, font=hf, fill=(0, 0, 0, 90), spacing=hsp)
    d.multiline_text((_M, hy), hw, font=hf, fill=W, spacing=hsp)
    b = _mtext_bottom(d, (_M, hy), hw, hf, hsp)
    d.text((_M, b + 30), f"{source or 'manchetes da semana'}", font=_f(_SANS_B, 30), fill=(255, 255, 255, 220))
    d.text((_M, _H - 150), "arraste  →", font=_f(_SANS_B, 40), fill=W)
    save(img, 0)

    for i, s in enumerate(slides):
        img, d = base()
        pill(d, f"Ponto {i + 1:02d}")
        # cartão translúcido
        cx0, cy0, cx1, cy1 = _M - 20, _M + 110, _W - _M + 20, _H - 150
        card = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(card).rounded_rectangle([cx0, cy0, cx1, cy1], radius=36, fill=(10, 12, 20, 150))
        img.alpha_composite(card)
        d = ImageDraw.Draw(img)
        d.text((cx0 + 40, cy0 + 30), f"{i + 1:02d}", font=_f(_SANS_B, 96), fill=(255, 255, 255, 90))
        ty = cy0 + 150
        tw, tf, tsp = _fit(d, s.get("titulo", ""), _SANS_B, cx1 - cx0 - 80, 200, 70, 42)
        d.multiline_text((cx0 + 40, ty), tw, font=tf, fill=W, spacing=tsp)
        b = _mtext_bottom(d, (cx0 + 40, ty), tw, tf, tsp)
        bw, bf, bsp = _fit(d, s.get("texto", ""), _SANS_R, cx1 - cx0 - 80, cy1 - b - 60, 44, 30, 0.26)
        d.multiline_text((cx0 + 40, b + 40), bw, font=bf, fill=(235, 238, 245), spacing=bsp)
        d.text((_M, _H - 128), handle, font=_f(_SANS_B, 30), fill=W)
        pg = f"{i + 2:02d} / {total:02d}"
        tb = d.textbbox((0, 0), pg, font=_f(_SANS_B, 30))
        d.text((_W - _M - (tb[2] - tb[0]), _H - 128), pg, font=_f(_SANS_B, 30), fill=W)
        save(img, i + 1)

    img, d = base()
    pill(d, "Toda semana por aqui")
    cw, cf, csp = _fit(d, "Salve e compartilhe.", _SANS_B, _W - 2 * _M, 420, 108, 60, 0.12)
    d.multiline_text((_M, int(_H * 0.34)), cw, font=cf, fill=W, spacing=csp)
    b = _mtext_bottom(d, (_M, int(_H * 0.34)), cw, cf, csp)
    d.text((_M, b + 50), handle, font=_f(_SANS_B, 62), fill=W)
    save(img, total - 1)


_STYLES = [_editorial, _terminal, _brutal, _gradient]
STYLE_NAMES = ["editorial", "terminal", "brutal", "gradient"]


def build(cover: str, slides: list, source: str, handle: str, out_dir: str, seed: int = 0) -> list:
    """Renderiza o carrossel em UM dos estilos (alterna por semente)."""
    slides = _clean_slides(slides)
    os.makedirs(out_dir, exist_ok=True)
    paths: list[str] = []

    def save(img, i):
        p = os.path.join(out_dir, f"slide_{i:02d}.png")
        img.convert("RGB").save(p, "PNG")
        paths.append(p)

    style = _STYLES[seed % len(_STYLES)]
    style(cover, slides, source, handle, out_dir, seed, save)
    return paths
