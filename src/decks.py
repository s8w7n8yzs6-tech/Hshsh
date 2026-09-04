"""Carrosséis de notícia IMAGE-DRIVEN: a FOTO do assunto é a protagonista.

3 layouts fortes que se alternam por post (para parar o scroll):
- poster : foto em tela cheia com véu e tipografia enorme
- band   : foto no topo + faixa escura com manchete serifada (editorial)
- frame  : foto emoldurada num fundo escuro, cara de revista

Sem foto disponível, cai para um layout sólido (ainda forte). A cor de acento
rotaciona por post. Recebe a foto já baixada (ver src/topicphoto.py).
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

_ACCENTS = [(233, 181, 86), (56, 189, 248), (163, 230, 53), (255, 107, 74), (167, 139, 250), (52, 211, 153)]
_DARK = (10, 12, 16)
_W_ = (255, 255, 255)


def _f(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(_SANS_B, size)


def _fit(d, text, path, max_w, max_h, hi, lo, ratio=0.12, upper=False):
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


def _bottom(d, xy, w, f, sp):
    return d.multiline_textbbox(xy, w, font=f, spacing=sp)[3]


def _tracked(d, xy, text, font, fill, tr=6):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + tr
    return x


def _cover_crop(img, w, h, fy=0.32):
    from PIL import Image as I

    iw, ih = img.size
    s = max(w / iw, h / ih)
    r = img.resize((max(1, int(iw * s)), max(1, int(ih * s))), I.LANCZOS)
    x = (r.width - w) // 2
    y = max(0, min(r.height - h, int((r.height - h) * fy)))
    return r.crop((x, y, x + w, y + h)).convert("RGBA")


def _scrim(top_a, bot_a, color=(6, 8, 12)):
    layer = Image.new("RGBA", (_W, _H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for y in range(_H):
        t = y / (_H - 1)
        a = int(top_a + (bot_a - top_a) * t)
        d.line([(0, y), (_W, y)], fill=color + (max(0, min(255, a)),))
    return layer


def _progress(d, accent, frac):
    d.rectangle([0, 0, _W, 8], fill=(255, 255, 255, 60))
    d.rectangle([0, 0, int(_W * max(0.06, min(1.0, frac))), 8], fill=accent)


def _kicker(d, accent, text, y=_M + 6, fg=_W_):
    d.rectangle([_M, y + 4, _M + 22, y + 26], fill=accent)
    _tracked(d, (_M + 40, y), text.upper(), _f(_SANS_B, 26), fg, 6)


def _shadow_text(d, xy, wrapped, font, sp, fill=_W_):
    x, y = xy
    d.multiline_text((x + 2, y + 3), wrapped, font=font, fill=(0, 0, 0, 150), spacing=sp)
    d.multiline_text((x, y), wrapped, font=font, fill=fill, spacing=sp)


def _footer(d, accent, handle, page, total, fg=_W_, muted=(210, 214, 222)):
    y = _H - 90
    d.line([(_M, y), (_W - _M, y)], fill=(255, 255, 255, 40), width=2)
    d.ellipse([_M, y + 24, _M + 16, y + 40], fill=accent)
    d.text((_M + 30, y + 18), handle, font=_f(_SANS_B, 30), fill=muted)
    txt = f"{page:02d} / {total:02d}"
    tb = d.textbbox((0, 0), txt, font=_f(_MONO_B, 30))
    d.text((_W - _M - (tb[2] - tb[0]), y + 18), txt, font=_f(_MONO_B, 30), fill=fg)


def _credit(d, credit):
    if credit:
        cf = _f(_SANS_R, 19)
        cb = d.textbbox((0, 0), credit, font=cf)
        d.text((_W - _M - (cb[2] - cb[0]), _H - 62), credit, font=cf, fill=(210, 214, 222))


def _arraste(d, accent, y=_H - 172):
    af = _f(_SANS_B, 28)
    tb = d.textbbox((0, 0), "ARRASTE  →", font=af)
    d.rounded_rectangle([_M, y, _M + (tb[2] - tb[0]) + 54, y + (tb[3] - tb[1]) + 30],
                        radius=30, fill=accent)
    d.text((_M + 27, y + 15 - tb[1]), "ARRASTE  →", font=af, fill=_DARK)


def _photo_bg(photo, heavy=False):
    if photo is None:
        img = Image.new("RGBA", (_W, _H), _DARK + (255,))
        d = ImageDraw.Draw(img)
        for y in range(_H):
            c = int(10 + 10 * y / _H)
            d.line([(0, y), (_W, y)], fill=(c, c + 2, c + 6, 255))
        return img
    img = _cover_crop(photo, _W, _H)
    img.alpha_composite(_scrim(120 if heavy else 70, 255 if heavy else 235))
    return img


# ---------------------------------------------------------------- POSTER
def _poster(cover, slides, source, handle, credit, accent, photo, save, kicker):
    total = 2 + len(slides)
    img = _photo_bg(photo, heavy=False)
    d = ImageDraw.Draw(img)
    _progress(d, accent, 1 / total)
    _kicker(d, accent, kicker)
    hw, hf, hsp = _fit(d, cover, _SANS_B, _W - 2 * _M, 520, 108, 56)
    hb = d.multiline_textbbox((0, 0), hw, font=hf, spacing=hsp)
    hy = _H - 308 - (hb[3] - hb[1])
    d.rectangle([_M, hy - 26, _M + 90, hy - 14], fill=accent)
    _shadow_text(d, (_M, hy), hw, hf, hsp)
    d.text((_M, _H - 264), f"O que movimentou o mercado · {source or 'esta semana'}",
           font=_f(_SANS_R, 30), fill=(224, 228, 234))
    _arraste(d, accent)
    _credit(d, credit)
    save(img, 0)

    for i, s in enumerate(slides):
        img = _photo_bg(photo, heavy=True)
        d = ImageDraw.Draw(img)
        _progress(d, accent, (i + 2) / total)
        d.text((_M, _M + 4), f"{i + 1:02d}", font=_f(_SERIF_B, 150), fill=accent)
        ty = _M + 210
        tw, tf, tsp = _fit(d, s.get("titulo", ""), _SANS_B, _W - 2 * _M, 200, 74, 44)
        _shadow_text(d, (_M, ty), tw, tf, tsp)
        b = _bottom(d, (_M, ty), tw, tf, tsp)
        d.rectangle([_M, b + 30, _M + 96, b + 38], fill=accent)
        bw, bf, bsp = _fit(d, s.get("texto", ""), _SANS_R, _W - 2 * _M, _H - 220 - b, 46, 30, 0.24)
        _shadow_text(d, (_M, b + 74), bw, bf, bsp, fill=(238, 240, 245))
        _footer(d, accent, handle, i + 2, total)
        save(img, i + 1)

    _cta(cover, handle, accent, photo, total, save)


# ---------------------------------------------------------------- BAND
def _band(cover, slides, source, handle, credit, accent, photo, save, kicker):
    total = 2 + len(slides)

    def band_top(frac_h):
        img = Image.new("RGBA", (_W, _H), _DARK + (255,))
        h = int(_H * frac_h)
        if photo is not None:
            ph = _cover_crop(photo, _W, h)
            fade = Image.new("RGBA", (_W, _H), (0, 0, 0, 0))
            fd = ImageDraw.Draw(fade)
            for y in range(h - 160, h):
                a = int(255 * (y - (h - 160)) / 160)
                fd.line([(0, y), (_W, y)], fill=_DARK + (a,))
            img.alpha_composite(ph, (0, 0))
            img.alpha_composite(fade)
        return img, h

    img, h = band_top(0.60)
    d = ImageDraw.Draw(img)
    _progress(d, accent, 1 / total)
    _kicker(d, accent, kicker, y=h - 60)
    hy = h + 10
    hw, hf, hsp = _fit(d, cover, _SERIF_B, _W - 2 * _M, _H - 330 - hy, 92, 52, 0.14)
    d.multiline_text((_M, hy), hw, font=hf, fill=_W_, spacing=hsp)
    b = _bottom(d, (_M, hy), hw, hf, hsp)
    d.text((_M, b + 30), f"Fonte · {source or 'manchetes da semana'}", font=_f(_SANS_R, 28), fill=(170, 178, 190))
    _arraste(d, accent, y=min(b + 92, _H - 130))
    _credit(d, credit)
    save(img, 0)

    for i, s in enumerate(slides):
        img, h = band_top(0.42)
        d = ImageDraw.Draw(img)
        _progress(d, accent, (i + 2) / total)
        _kicker(d, accent, f"Ponto {i + 1:02d} de {len(slides):02d}", y=h + 24)
        ty = h + 90
        tw, tf, tsp = _fit(d, s.get("titulo", ""), _SERIF_B, _W - 2 * _M, 200, 66, 42, 0.14)
        d.multiline_text((_M, ty), tw, font=tf, fill=_W_, spacing=tsp)
        b = _bottom(d, (_M, ty), tw, tf, tsp)
        bw, bf, bsp = _fit(d, s.get("texto", ""), _SANS_R, _W - 2 * _M, _H - 210 - b, 44, 28, 0.24)
        d.multiline_text((_M, b + 40), bw, font=bf, fill=(196, 202, 212), spacing=bsp)
        _footer(d, accent, handle, i + 2, total)
        save(img, i + 1)

    _cta(cover, handle, accent, photo, total, save)


# ---------------------------------------------------------------- FRAME
def _frame(cover, slides, source, handle, credit, accent, photo, save, kicker):
    total = 2 + len(slides)

    img = Image.new("RGBA", (_W, _H), _DARK + (255,))
    d = ImageDraw.Draw(img)
    _progress(d, accent, 1 / total)
    _kicker(d, accent, kicker)
    # foto emoldurada
    fx0, fy0, fx1, fy1 = _M, _M + 90, _W - _M, int(_H * 0.56)
    if photo is not None:
        ph = _cover_crop(photo, fx1 - fx0, fy1 - fy0)
        img.alpha_composite(ph, (fx0, fy0))
    d.rectangle([fx0 - 4, fy0 - 4, fx1 + 4, fy1 + 4], outline=accent, width=5)
    hy = fy1 + 44
    hw, hf, hsp = _fit(d, cover, _SANS_B, _W - 2 * _M, _H - 200 - hy, 84, 48)
    d.multiline_text((_M, hy), hw, font=hf, fill=_W_, spacing=hsp)
    b = _bottom(d, (_M, hy), hw, hf, hsp)
    d.text((_M, b + 24), f"Fonte · {source or 'manchetes da semana'}", font=_f(_SANS_R, 27), fill=(160, 168, 180))
    _credit(d, credit)
    save(img, 0)

    for i, s in enumerate(slides):
        img = Image.new("RGBA", (_W, _H), _DARK + (255,))
        d = ImageDraw.Draw(img)
        _progress(d, accent, (i + 2) / total)
        # faixa de foto no topo com moldura
        if photo is not None:
            ph = _cover_crop(photo, _W - 2 * _M, 300)
            img.alpha_composite(ph, (_M, _M + 60))
            d.rectangle([_M - 4, _M + 56, _W - _M + 4, _M + 364], outline=accent, width=4)
        d.text((_M, _M + 60 + 300 + 20), f"{i + 1:02d}", font=_f(_SERIF_B, 96), fill=accent)
        ty = _M + 60 + 300 + 130
        tw, tf, tsp = _fit(d, s.get("titulo", ""), _SANS_B, _W - 2 * _M, 160, 64, 40)
        d.multiline_text((_M, ty), tw, font=tf, fill=_W_, spacing=tsp)
        b = _bottom(d, (_M, ty), tw, tf, tsp)
        bw, bf, bsp = _fit(d, s.get("texto", ""), _SANS_R, _W - 2 * _M, _H - 200 - b, 44, 28, 0.24)
        d.multiline_text((_M, b + 34), bw, font=bf, fill=(200, 206, 216), spacing=bsp)
        _footer(d, accent, handle, i + 2, total)
        save(img, i + 1)

    _cta(cover, handle, accent, photo, total, save)


def _cta(cover, handle, accent, photo, total, save):
    img = _photo_bg(photo, heavy=True) if photo is not None else Image.new("RGBA", (_W, _H), _DARK + (255,))
    d = ImageDraw.Draw(img)
    _progress(d, accent, 1.0)
    _kicker(d, accent, "Toda semana por aqui")
    cw, cf, csp = _fit(d, "Salve. Compartilhe.", _SANS_B, _W - 2 * _M, 380, 104, 60, 0.14)
    d.multiline_text((_M, int(_H * 0.34)), cw, font=cf, fill=_W_, spacing=csp)
    b = _bottom(d, (_M, int(_H * 0.34)), cw, cf, csp)
    d.rectangle([_M, b + 54, _M + 110, b + 64], fill=accent)
    d.text((_M, b + 96), handle, font=_f(_SANS_B, 58), fill=accent)
    save(img, total - 1)


# ---------------------------------------------------------------- SPLIT
def _split(cover, slides, source, handle, credit, accent, photo, save, kicker):
    """Bloco de cor + foto em paisagem — forte e ideal para fotos landscape."""
    total = 2 + len(slides)
    top_h = int(_H * 0.46)

    img = Image.new("RGBA", (_W, _H), _DARK + (255,))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, _W, top_h], fill=accent)
    if photo is not None:
        img.alpha_composite(_cover_crop(photo, _W, _H - top_h, 0.4), (0, top_h))
    d = ImageDraw.Draw(img)
    _progress(d, _DARK, 1 / total)
    d.rectangle([_M, _M + 10, _M + 22, _M + 32], fill=_DARK)
    _tracked(d, (_M + 40, _M + 6), kicker.upper(), _f(_SANS_B, 26), _DARK, 6)
    hy = _M + 86
    hw, hf, hsp = _fit(d, cover, _SANS_B, _W - 2 * _M, top_h - hy - 90, 92, 48)
    d.multiline_text((_M, hy), hw, font=hf, fill=_DARK, spacing=hsp)
    b = _bottom(d, (_M, hy), hw, hf, hsp)
    d.text((_M, min(b + 22, top_h - 54)), f"Fonte · {source or 'manchetes da semana'}",
           font=_f(_SANS_B, 26), fill=(40, 40, 44))
    af = _f(_SANS_B, 28)
    tb = d.textbbox((0, 0), "ARRASTE  →", font=af)
    d.rounded_rectangle([_M, _H - 130, _M + (tb[2] - tb[0]) + 54, _H - 130 + (tb[3] - tb[1]) + 30],
                        radius=30, fill=accent)
    d.text((_M + 27, _H - 130 + 15 - tb[1]), "ARRASTE  →", font=af, fill=_DARK)
    _credit(d, credit)
    save(img, 0)

    strip_h = 300
    for i, s in enumerate(slides):
        img = Image.new("RGBA", (_W, _H), _DARK + (255,))
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, _W, 250], fill=accent)
        if photo is not None:
            img.alpha_composite(_cover_crop(photo, _W, strip_h, 0.45), (0, _H - strip_h))
            d = ImageDraw.Draw(img)
            fade = Image.new("RGBA", (_W, _H), (0, 0, 0, 0))
            fd = ImageDraw.Draw(fade)
            for y in range(_H - strip_h, _H - strip_h + 120):
                a = int(255 * (1 - (y - (_H - strip_h)) / 120))
                fd.line([(0, y), (_W, y)], fill=_DARK + (a,))
            img.alpha_composite(fade)
            d = ImageDraw.Draw(img)
        _progress(d, _DARK, (i + 2) / total)
        d.text((_M, 58), f"{i + 1:02d}", font=_f(_SERIF_B, 110), fill=_DARK)
        ty = 300
        tw, tf, tsp = _fit(d, s.get("titulo", ""), _SANS_B, _W - 2 * _M, 190, 70, 42)
        d.multiline_text((_M, ty), tw, font=tf, fill=_W_, spacing=tsp)
        b = _bottom(d, (_M, ty), tw, tf, tsp)
        d.rectangle([_M, b + 26, _M + 96, b + 34], fill=accent)
        bw, bf, bsp = _fit(d, s.get("texto", ""), _SANS_R, _W - 2 * _M,
                           _H - strip_h - 60 - b, 44, 28, 0.24)
        d.multiline_text((_M, b + 70), bw, font=bf, fill=(206, 212, 222), spacing=bsp)
        d.text((_M, _H - 56), handle, font=_f(_SANS_B, 28), fill=_W_)
        pg = f"{i + 2:02d} / {total:02d}"
        tb2 = d.textbbox((0, 0), pg, font=_f(_MONO_B, 28))
        d.text((_W - _M - (tb2[2] - tb2[0]), _H - 56), pg, font=_f(_MONO_B, 28), fill=_W_)
        save(img, i + 1)

    img = Image.new("RGBA", (_W, _H), accent + (255,))
    d = ImageDraw.Draw(img)
    _progress(d, _DARK, 1.0)
    d.rectangle([_M, _M + 10, _M + 22, _M + 32], fill=_DARK)
    _tracked(d, (_M + 40, _M + 6), "TODA SEMANA POR AQUI", _f(_SANS_B, 26), _DARK, 6)
    cw, cf, csp = _fit(d, "Salve. Compartilhe.", _SANS_B, _W - 2 * _M, 400, 104, 60, 0.12)
    d.multiline_text((_M, int(_H * 0.32)), cw, font=cf, fill=_DARK, spacing=csp)
    b = _bottom(d, (_M, int(_H * 0.32)), cw, cf, csp)
    d.rectangle([_M, b + 54, _M + 120, b + 66], fill=_DARK)
    d.text((_M, b + 100), handle, font=_f(_SANS_B, 58), fill=_DARK)
    save(img, total - 1)


_LAYOUTS = [_poster, _band, _frame, _split]
LAYOUT_NAMES = ["poster", "band", "frame", "split"]
# Layouts cuja área de foto é PAISAGEM (funcionam bem com fotos landscape).
_LANDSCAPE_OK = [_band, _frame, _split]


def build(cover: str, slides: list, source: str, handle: str, out_dir: str,
          seed: int = 0, photo=None, credit: str = "", kicker: str = "") -> list:
    """Renderiza o carrossel image-driven, escolhendo o layout que melhor cabe na foto.

    Foto retrato → qualquer layout (inclui o poster em tela cheia). Foto paisagem
    → só layouts com área de foto em paisagem, para não borrar/cortar demais.
    """
    slides = [s for s in (slides or []) if s.get("titulo") or s.get("texto")][:5]
    os.makedirs(out_dir, exist_ok=True)
    paths: list[str] = []

    def save(img, i):
        p = os.path.join(out_dir, f"slide_{i:02d}.png")
        img.convert("RGB").save(p, "PNG")
        paths.append(p)

    kicker = (kicker or "Mercado · Esta semana").strip()
    accent = _ACCENTS[seed % len(_ACCENTS)]
    tall = photo is not None and (photo.height / max(1, photo.width)) >= 1.15
    options = _LAYOUTS if tall else _LANDSCAPE_OK
    layout = options[seed % len(options)]
    layout(cover, slides, source, handle, credit, accent, photo, save, kicker)
    return paths
