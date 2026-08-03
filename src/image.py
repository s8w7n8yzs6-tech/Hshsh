"""Monta um card 1080x1350 chamativo: cena cinematográfica de trader + headline.

O fundo é uma cena programática (silhueta do trader diante de monitores que
brilham — ver `scene.py`). Por cima vai um véu escuro no topo e a headline curta
e impactante. Posts de mercado usam o gráfico real de 30 min como a "tela" do
monitor central.
"""
from __future__ import annotations

import textwrap

from PIL import Image, ImageDraw, ImageFont

from . import scene

_W, _H = 1080, 1350  # retrato (feed do Instagram)
_MARGIN = 76
_TEXT = (248, 249, 250)

_FONTS_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
]
_FONTS_REG = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/Library/Fonts/Arial.ttf",
]


def _font(bold: bool, size: int) -> ImageFont.FreeTypeFont:
    for path in (_FONTS_BOLD if bold else _FONTS_REG):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _fit_headline(draw: ImageDraw.ImageDraw, text: str, max_w: int, max_h: int):
    """Escolhe o maior tamanho de fonte em que a headline cabe na área do topo."""
    wrapped, font = text, _font(True, 44)
    for size in range(92, 42, -4):
        font = _font(True, size)
        avg = draw.textlength("média", font=font) / 5 or 1
        wrap_at = max(8, int(max_w / avg))
        wrapped = "\n".join(textwrap.wrap(text, width=wrap_at)) or text
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, spacing=14)
        if (bbox[2] - bbox[0]) <= max_w and (bbox[3] - bbox[1]) <= max_h:
            return wrapped, font
    return wrapped, font


def _top_scrim(accent: tuple) -> Image.Image:
    """Véu escuro no topo (transparente embaixo) para a headline ficar legível."""
    scrim = Image.new("RGBA", (_W, _H), (0, 0, 0, 0))
    d = ImageDraw.Draw(scrim)
    fade = int(_H * 0.62)
    for y in range(fade):
        t = y / fade
        a = int(232 * (1 - t) ** 1.6)
        d.line([(0, y), (_W, y)], fill=(3, 6, 11, a))
    return scrim


def _text_with_shadow(draw, xy, text, font, fill, spacing):
    x, y = xy
    draw.multiline_text((x + 2, y + 3), text, font=font, fill=(0, 0, 0, 170), spacing=spacing)
    draw.multiline_text((x, y), text, font=font, fill=fill, spacing=spacing)


def build_card(
    headline: str,
    content_type: str,
    handle: str,
    out_path: str,
    chart_img: Image.Image | None = None,
    seed: int = 0,
) -> str:
    img = scene.render_scene(_W, _H, seed=seed, screen_img=chart_img)
    accent = scene.palette_for(seed)["glow"]
    ar, ag, ab = accent

    img.alpha_composite(_top_scrim(accent))
    draw = ImageDraw.Draw(img)

    # Badge (pílula) no topo.
    badge = "MERCADO" if content_type == "mercado" else "TRADER"
    bf = _font(True, 28)
    tb = draw.textbbox((0, 0), badge, font=bf)
    bw, bh = tb[2] - tb[0], tb[3] - tb[1]
    pad_x, pad_y = 26, 15
    pill_h = bh + 2 * pad_y
    draw.rounded_rectangle(
        [_MARGIN, _MARGIN, _MARGIN + bw + 2 * pad_x, _MARGIN + pill_h],
        radius=pill_h // 2,
        fill=(ar, ag, ab, 255),
    )
    draw.text((_MARGIN + pad_x - tb[0], _MARGIN + pad_y - tb[1]), badge, font=bf, fill=(9, 12, 18))

    # Barrinha de destaque + headline grande no topo.
    ht_top = _MARGIN + pill_h + 54
    ht_bottom = int(_H * 0.45)
    wrapped, font = _fit_headline(draw, headline, _W - 2 * _MARGIN, ht_bottom - ht_top - 30)
    draw.rounded_rectangle([_MARGIN, ht_top, _MARGIN + 64, ht_top + 8], radius=4, fill=(ar, ag, ab, 255))
    _text_with_shadow(draw, (_MARGIN, ht_top + 30), wrapped, font, _TEXT, spacing=14)

    # Assinatura (@) no rodapé.
    hf = _font(True, 34)
    hy = _H - 92
    draw.ellipse([_MARGIN, hy + 9, _MARGIN + 18, hy + 27], fill=(ar, ag, ab, 255))
    draw.text((_MARGIN + 32, hy), handle, font=hf, fill=(226, 229, 233))

    img.convert("RGB").save(out_path, "PNG")
    return out_path
