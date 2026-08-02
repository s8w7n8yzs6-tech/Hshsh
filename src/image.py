"""Renderiza o texto de um post em uma imagem 1080x1080 (necessário no Instagram)."""
from __future__ import annotations

import textwrap

from PIL import Image, ImageDraw, ImageFont

_SIZE = 1080
_BG = (14, 17, 23)          # fundo escuro
_FG = (240, 240, 240)       # texto claro
_ACCENT = (56, 189, 248)    # detalhe (barra superior)
_MARGIN = 90

_FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/Library/Fonts/Arial.ttf",
]


def _load_font(size: int) -> ImageFont.FreeTypeFont:
    for path in _FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _strip_hashtags(text: str) -> str:
    """Remove a linha de hashtags do corpo da imagem (elas ficam só na legenda)."""
    lines = [ln for ln in text.splitlines() if not ln.strip().startswith("#")]
    return "\n".join(lines).strip() or text


def render_caption_image(text: str, out_path: str) -> str:
    """Escreve `text` centralizado numa imagem quadrada e salva em `out_path`."""
    body = _strip_hashtags(text)
    img = Image.new("RGB", (_SIZE, _SIZE), _BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, _SIZE, 16], fill=_ACCENT)

    font_size = 60
    max_width = _SIZE - 2 * _MARGIN
    while font_size >= 28:
        font = _load_font(font_size)
        # largura média de caractere para estimar a quebra de linha
        avg = draw.textlength("média", font=font) / 5 or 1
        wrap_at = max(10, int(max_width / avg))
        wrapped = "\n".join(
            "\n".join(textwrap.wrap(par, width=wrap_at)) if par.strip() else ""
            for par in body.splitlines()
        )
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, spacing=14)
        if (bbox[3] - bbox[1]) <= (_SIZE - 2 * _MARGIN):
            break
        font_size -= 4

    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, spacing=14)
    x = (_SIZE - (bbox[2] - bbox[0])) / 2 - bbox[0]
    y = (_SIZE - (bbox[3] - bbox[1])) / 2 - bbox[1]
    draw.multiline_text((x, y), wrapped, font=font, fill=_FG, spacing=14, align="center")

    img.save(out_path, "PNG")
    return out_path
