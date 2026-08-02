"""Monta um card visual 1080x1080 chamativo para cada post.

Cada tipo de conteúdo tem seu tema (cores/badge). Posts de mercado recebem um
gráfico. A headline curta vai na imagem; a legenda completa vai no texto do post.
"""
from __future__ import annotations

import textwrap

from PIL import Image, ImageDraw, ImageFont

from . import theme

_W = _H = 1080
_MARGIN = 72
_TEXT = (245, 245, 245)

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


def _gradient(top: tuple, bottom: tuple) -> Image.Image:
    img = Image.new("RGB", (_W, _H), top)
    draw = ImageDraw.Draw(img)
    for y in range(_H):
        t = y / (_H - 1)
        color = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(0, y), (_W, y)], fill=color)
    return img


def _fit_headline(draw: ImageDraw.ImageDraw, text: str, max_w: int, max_h: int):
    wrapped, font = text, _font(True, 40)
    for size in range(84, 38, -4):
        font = _font(True, size)
        avg = draw.textlength("média", font=font) / 5 or 1
        wrap_at = max(8, int(max_w / avg))
        wrapped = "\n".join(textwrap.wrap(text, width=wrap_at)) or text
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, spacing=12)
        if (bbox[2] - bbox[0]) <= max_w and (bbox[3] - bbox[1]) <= max_h:
            return wrapped, font
    return wrapped, font


def build_card(
    headline: str,
    content_type: str,
    handle: str,
    out_path: str,
    chart_img: Image.Image | None = None,
) -> str:
    th = theme.theme_for(content_type)
    ar, ag, ab = th["accent"]

    img = _gradient(th["bg_top"], th["bg_bottom"]).convert("RGBA")

    # Formas decorativas translúcidas nos cantos.
    overlay = Image.new("RGBA", (_W, _H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse([_W - 260, -160, _W + 180, 280], fill=(ar, ag, ab, 40))
    od.ellipse([-200, _H - 260, 180, _H + 180], fill=(ar, ag, ab, 26))
    img = Image.alpha_composite(img, overlay)

    draw = ImageDraw.Draw(img)

    # Badge (pílula) com o tipo de conteúdo.
    badge = th["badge"]
    bf = _font(True, 30)
    tb = draw.textbbox((0, 0), badge, font=bf)
    bw, bh = tb[2] - tb[0], tb[3] - tb[1]
    pad_x, pad_y = 28, 16
    pill_h = bh + 2 * pad_y
    draw.rounded_rectangle(
        [_MARGIN, _MARGIN, _MARGIN + bw + 2 * pad_x, _MARGIN + pill_h],
        radius=pill_h // 2,
        fill=(ar, ag, ab, 255),
    )
    draw.text((_MARGIN + pad_x - tb[0], _MARGIN + pad_y - tb[1]), badge, font=bf, fill=(17, 17, 17))

    # Headline.
    ht_top = _MARGIN + pill_h + 50
    ht_bottom = 470 if chart_img is not None else _H - 150
    wrapped, font = _fit_headline(draw, headline, _W - 2 * _MARGIN, ht_bottom - ht_top)
    hb = draw.multiline_textbbox((0, 0), wrapped, font=font, spacing=12)
    if chart_img is None:
        # Sem gráfico: centraliza a headline verticalmente para não ficar vazio.
        ty = ht_top + ((ht_bottom - ht_top) - (hb[3] - hb[1])) // 2 - hb[1]
    else:
        ty = ht_top
    draw.multiline_text((_MARGIN, ty), wrapped, font=font, fill=_TEXT, spacing=12)

    # Gráfico (posts de mercado).
    if chart_img is not None:
        max_w = _W - 2 * _MARGIN
        region_top = ht_bottom + 10
        region_bottom = _H - 150
        max_h = max(120, region_bottom - region_top)
        cw, ch = chart_img.size
        scale = min(max_w / cw, max_h / ch, 1.0)
        nw, nh = int(cw * scale), int(ch * scale)
        resized = chart_img.resize((nw, nh))
        cx = (_W - nw) // 2
        cy = region_top + (max_h - nh) // 2
        img.alpha_composite(resized, (cx, cy))

    # Assinatura (@) no rodapé.
    hf = _font(True, 34)
    hy = _H - 96
    draw.ellipse([_MARGIN, hy + 8, _MARGIN + 18, hy + 26], fill=(ar, ag, ab, 255))
    draw.text((_MARGIN + 32, hy), handle, font=hf, fill=(215, 215, 215))

    img.convert("RGB").save(out_path, "PNG")
    return out_path
