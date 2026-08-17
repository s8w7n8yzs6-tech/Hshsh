"""Vários formatos de card para dar VARIEDADE ao feed (não só foto + frase).

Formatos desenhados (sem foto), com paletas claras e escuras que se revezam:
- citacao      : uma frase forte, tipografia grande, com aspas gigantes
- lista        : título + 3 a 5 itens numerados (ótimo para salvar)
- mito_verdade : card dividido, MITO (vermelho) x VERDADE (verde)
- numero       : um número/estatística gigante + um rótulo curto

Os formatos foto (IA) e mercado (gráfico real) ficam em image.py.
"""
from __future__ import annotations

import textwrap

from PIL import Image, ImageDraw, ImageFont

_W, _H = 1080, 1350
_MARGIN = 84

_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
_SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
_DEJAVU_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Paletas: mistura de fundos CLAROS e ESCUROS para o grid não ficar monótono.
# bg2 (opcional) cria gradiente vertical. dark=True → texto claro.
THEMES = [
    {"bg": (244, 242, 236), "bg2": (232, 229, 220), "fg": (18, 22, 30), "muted": (90, 96, 110), "accent": (37, 99, 235), "dark": False},
    {"bg": (250, 250, 252), "bg2": (238, 240, 245), "fg": (17, 17, 20), "muted": (95, 100, 112), "accent": (5, 150, 105), "dark": False},
    {"bg": (13, 27, 62), "bg2": (8, 15, 38), "fg": (245, 249, 255), "muted": (150, 170, 200), "accent": (56, 189, 248), "dark": True},
    {"bg": (12, 14, 20), "bg2": (6, 8, 12), "fg": (245, 246, 248), "muted": (150, 156, 168), "accent": (45, 212, 191), "dark": True},
    {"bg": (49, 46, 129), "bg2": (30, 27, 75), "fg": (248, 248, 255), "muted": (185, 180, 225), "accent": (196, 181, 253), "dark": True},
    {"bg": (6, 30, 24), "bg2": (3, 16, 13), "fg": (240, 253, 246), "muted": (150, 190, 172), "accent": (52, 211, 153), "dark": True},
    {"bg": (24, 12, 10), "bg2": (12, 6, 5), "fg": (255, 247, 242), "muted": (200, 165, 150), "accent": (251, 146, 60), "dark": True},
]


def theme(seed: int) -> dict:
    return THEMES[seed % len(THEMES)]


_DARK = [t for t in THEMES if t["dark"]]


def dark_theme(seed: int) -> dict:
    """Tema escuro (melhor para diagramas de gráfico)."""
    return _DARK[seed % len(_DARK)]


def _font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(_DEJAVU_B, size)


def _bg(th: dict) -> Image.Image:
    top, bot = th["bg"], th.get("bg2", th["bg"])
    img = Image.new("RGB", (_W, _H), top)
    d = ImageDraw.Draw(img)
    for y in range(_H):
        t = y / (_H - 1)
        d.line([(0, y), (_W, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    return img.convert("RGBA")


def _wrap_fit(draw, text, font_path, max_w, max_h, hi, lo, spacing_ratio=0.22):
    """Maior fonte em que `text` (com quebra) cabe em max_w x max_h."""
    wrapped, font = text, _font(font_path, lo)
    for size in range(hi, lo - 2, -3):
        font = _font(font_path, size)
        avg = draw.textlength("média", font=font) / 5 or 1
        wrapped = "\n".join(textwrap.wrap(text, width=max(6, int(max_w / avg)))) or text
        sp = int(size * spacing_ratio)
        bb = draw.multiline_textbbox((0, 0), wrapped, font=font, spacing=sp)
        if (bb[2] - bb[0]) <= max_w and (bb[3] - bb[1]) <= max_h:
            return wrapped, font, sp
    return wrapped, font, int(font.size * spacing_ratio)


def _badge(draw, th, label):
    bf = _font(_SANS_B, 27)
    tb = draw.textbbox((0, 0), label, font=bf)
    bw, bh = tb[2] - tb[0], tb[3] - tb[1]
    px, py = 24, 14
    draw.rounded_rectangle(
        [_MARGIN, _MARGIN, _MARGIN + bw + 2 * px, _MARGIN + bh + 2 * py],
        radius=(bh + 2 * py) // 2, fill=th["accent"],
    )
    fg = (255, 255, 255) if th["dark"] else (255, 255, 255)
    draw.text((_MARGIN + px - tb[0], _MARGIN + py - tb[1]), label, font=bf, fill=fg)


def _footer(draw, th, handle):
    hf = _font(_SANS_B, 32)
    hy = _H - 86
    draw.ellipse([_MARGIN, hy + 8, _MARGIN + 17, hy + 25], fill=th["accent"])
    draw.text((_MARGIN + 30, hy), handle, font=hf, fill=th["muted"])


def build_quote(statement: str, handle: str, out_path: str, seed: int = 0, badge: str = "MENTALIDADE") -> str:
    th = theme(seed)
    img = _bg(th)
    d = ImageDraw.Draw(img)
    _badge(d, th, badge)

    # Aspas gigante como elemento gráfico.
    qf = _font(_SERIF_B, 260)
    d.text((_MARGIN - 12, _MARGIN + 70), "“", font=qf, fill=th["accent"] + (70,) if th["dark"] else th["accent"])

    area_top, area_bot = int(_H * 0.30), int(_H * 0.80)
    wrapped, font, sp = _wrap_fit(d, statement, _SERIF_B, _W - 2 * _MARGIN, area_bot - area_top, 96, 52)
    bb = d.multiline_textbbox((0, 0), wrapped, font=font, spacing=sp)
    ty = area_top + ((area_bot - area_top) - (bb[3] - bb[1])) // 2
    d.multiline_text((_MARGIN, ty), wrapped, font=font, fill=th["fg"], spacing=sp)

    _footer(d, th, handle)
    img.convert("RGB").save(out_path, "PNG")
    return out_path


def build_list(title: str, items: list[str], handle: str, out_path: str, seed: int = 0, badge: str = "PRA SALVAR") -> str:
    th = theme(seed)
    img = _bg(th)
    d = ImageDraw.Draw(img)
    _badge(d, th, badge)

    ty = _MARGIN + 96
    tw, tfont, tsp = _wrap_fit(d, title, _SANS_B, _W - 2 * _MARGIN, 260, 68, 40)
    d.multiline_text((_MARGIN, ty), tw, font=tfont, fill=th["fg"], spacing=tsp)
    tb = d.multiline_textbbox((_MARGIN, ty), tw, font=tfont, spacing=tsp)
    d.rounded_rectangle([_MARGIN, tb[3] + 26, _MARGIN + 96, tb[3] + 36], radius=5, fill=th["accent"])

    items = [i for i in items if i][:5]
    top = tb[3] + 80
    gap = (_H - 150 - top) // max(1, len(items))
    nf = _font(_SANS_B, 40)
    itf_size = 37 if len(items) >= 4 else 41
    for idx, item in enumerate(items):
        cy = top + idx * gap
        r = 33
        d.ellipse([_MARGIN, cy, _MARGIN + 2 * r, cy + 2 * r], fill=th["accent"])
        num = str(idx + 1)
        nb = d.textbbox((0, 0), num, font=nf)
        d.text((_MARGIN + r - (nb[2] - nb[0]) / 2 - nb[0], cy + r - (nb[3] - nb[1]) / 2 - nb[1]),
               num, font=nf, fill=(255, 255, 255))
        iw, ifont, isp = _wrap_fit(d, item, _SANS_R, _W - 2 * _MARGIN - 2 * r - 34, 2 * r + 20,
                                    itf_size, 26, spacing_ratio=0.18)
        ib = d.multiline_textbbox((0, 0), iw, font=ifont, spacing=isp)
        d.multiline_text((_MARGIN + 2 * r + 34, cy + r - (ib[3] - ib[1]) / 2 - ib[1]),
                         iw, font=ifont, fill=th["fg"], spacing=isp)

    _footer(d, th, handle)
    img.convert("RGB").save(out_path, "PNG")
    return out_path


def build_myth_truth(mito: str, verdade: str, handle: str, out_path: str, seed: int = 0) -> str:
    th = theme(seed if theme(seed)["dark"] else seed + 3)  # myth/truth fica melhor no escuro
    img = _bg(th)
    d = ImageDraw.Draw(img)

    red = (239, 68, 68)
    green = (34, 197, 94)
    mid = _H // 2

    def half(y0, y1, color, label, text):
        pill = _font(_SANS_B, 30)
        lb = d.textbbox((0, 0), label, font=pill)
        pw, ph = lb[2] - lb[0], lb[3] - lb[1]
        px, py = 26, 14
        d.rounded_rectangle([_MARGIN, y0 + 44, _MARGIN + pw + 2 * px, y0 + 44 + ph + 2 * py],
                            radius=(ph + 2 * py) // 2, fill=color)
        d.text((_MARGIN + px - lb[0], y0 + 44 + py - lb[1]), label, font=pill, fill=(255, 255, 255))
        tw, tf, ts = _wrap_fit(d, text, _SANS_B, _W - 2 * _MARGIN, (y1 - y0) - 150, 58, 34)
        tb = d.multiline_textbbox((0, 0), tw, font=tf, spacing=ts)
        d.multiline_text((_MARGIN, y0 + 130 + ((y1 - y0 - 150) - (tb[3] - tb[1])) // 2),
                         tw, font=tf, fill=th["fg"], spacing=ts)

    half(0, mid, red, "MITO", mito)
    # linha divisória
    d.line([(_MARGIN, mid), (_W - _MARGIN, mid)], fill=th["muted"] + (120,), width=2)
    half(mid, _H - 40, green, "VERDADE", verdade)

    _footer(d, th, handle)
    img.convert("RGB").save(out_path, "PNG")
    return out_path


def build_pattern(nome: str, explicacao: str, diagram: "object", handle: str,
                  out_path: str, seed: int = 0) -> str:
    """Card educativo 'Aprenda um padrão': título + diagrama de gráfico + explicação."""
    from PIL import Image

    th = dark_theme(seed)
    img = _bg(th)
    d = ImageDraw.Draw(img)
    _badge(d, th, "APRENDA UM PADRÃO")

    # Título (nome do padrão).
    ty = _MARGIN + 92
    tw, tfont, tsp = _wrap_fit(d, nome, _SANS_B, _W - 2 * _MARGIN, 170, 72, 44)
    d.multiline_text((_MARGIN, ty), tw, font=tfont, fill=th["fg"], spacing=tsp)
    tb = d.multiline_textbbox((_MARGIN, ty), tw, font=tfont, spacing=tsp)

    # Diagrama do padrão (imagem RGBA já renderizada), centralizado.
    diag_top = tb[3] + 40
    diag_w = _W - 2 * _MARGIN
    diag_h = 560
    if diagram is not None:
        fit = diagram if isinstance(diagram, Image.Image) else None
        if fit is not None:
            f = fit.copy()
            f.thumbnail((diag_w, diag_h))
            img.alpha_composite(f, ((_W - f.width) // 2, diag_top))

    # Explicação abaixo do diagrama.
    exp_top = diag_top + diag_h + 24
    ew, efont, esp = _wrap_fit(d, explicacao, _SANS_R, _W - 2 * _MARGIN,
                               _H - 120 - exp_top, 42, 28, spacing_ratio=0.2)
    d.multiline_text((_MARGIN, exp_top), ew, font=efont, fill=th["muted"], spacing=esp)

    _footer(d, th, handle)
    img.convert("RGB").save(out_path, "PNG")
    return out_path


def build_concept(titulo: str, explicacao: str, handle: str, out_path: str, seed: int = 0,
                  badge: str = "APRENDA") -> str:
    """Card educativo (conceito/indicador/estratégia): título forte + explicação clara."""
    th = theme(seed)
    img = _bg(th)
    d = ImageDraw.Draw(img)
    _badge(d, th, badge)

    ty = _MARGIN + 96
    tw, tfont, tsp = _wrap_fit(d, titulo, _SANS_B, _W - 2 * _MARGIN, 300, 78, 44)
    d.multiline_text((_MARGIN, ty), tw, font=tfont, fill=th["fg"], spacing=tsp)
    tb = d.multiline_textbbox((_MARGIN, ty), tw, font=tfont, spacing=tsp)
    d.rounded_rectangle([_MARGIN, tb[3] + 30, _MARGIN + 96, tb[3] + 40], radius=5, fill=th["accent"])

    exp_top = tb[3] + 76
    ew, efont, esp = _wrap_fit(d, explicacao, _SANS_R, _W - 2 * _MARGIN,
                               _H - 130 - exp_top, 50, 30, spacing_ratio=0.22)
    d.multiline_text((_MARGIN, exp_top), ew, font=efont, fill=th["fg"], spacing=esp)

    _footer(d, th, handle)
    img.convert("RGB").save(out_path, "PNG")
    return out_path


def build_number(stat: str, label: str, handle: str, out_path: str, seed: int = 0, badge: str = "REALIDADE") -> str:
    th = theme(seed)
    img = _bg(th)
    d = ImageDraw.Draw(img)
    _badge(d, th, badge)

    # Número gigante.
    nf = _font(_DEJAVU_B, 340)
    for size in range(340, 140, -20):
        nf = _font(_DEJAVU_B, size)
        if d.textlength(stat, font=nf) <= _W - 2 * _MARGIN:
            break
    nb = d.textbbox((0, 0), stat, font=nf)
    nx = (_W - (nb[2] - nb[0])) // 2 - nb[0]
    ny = int(_H * 0.26)
    d.text((nx, ny), stat, font=nf, fill=th["accent"])

    # Rótulo/contexto abaixo.
    lw, lf, ls = _wrap_fit(d, label, _SANS_B, _W - 2 * _MARGIN, 300, 58, 34)
    lb = d.multiline_textbbox((0, 0), lw, font=lf, spacing=ls)
    lx = (_W - (lb[2] - lb[0])) // 2
    d.multiline_text((lx, ny + (nb[3] - nb[1]) + 70), lw, font=lf, fill=th["fg"], spacing=ls, align="center")

    _footer(d, th, handle)
    img.convert("RGB").save(out_path, "PNG")
    return out_path
