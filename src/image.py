"""Monta o card 1080x1350: fundo fotorrealista de trader (IA) + headline forte.

Se houver um fundo gerado por IA (`background`), ele é usado em tela cheia com
véus escuros para a headline ficar legível. Sem ele, cai para a cena desenhada
(`scene.py`). Posts de mercado sobrepõem o gráfico real de 30 min num painel.
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
    """Escolhe o maior tamanho de fonte em que a headline cabe na área dada."""
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


def _cover(bg: Image.Image) -> Image.Image:
    """Redimensiona/recorta a foto para preencher exatamente 1080x1350 (cover)."""
    bw, bh = bg.size
    scale = max(_W / bw, _H / bh)
    nb = bg.resize((int(bw * scale), int(bh * scale)))
    x = (nb.width - _W) // 2
    y = (nb.height - _H) // 2
    return nb.crop((x, y, x + _W, y + _H)).convert("RGBA")


def _scrims() -> Image.Image:
    """Véu escuro no topo (headline) e no rodapé (@), transparente no meio."""
    layer = Image.new("RGBA", (_W, _H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    top_fade = int(_H * 0.5)
    for y in range(top_fade):
        a = int(210 * (1 - y / top_fade) ** 1.5)
        d.line([(0, y), (_W, y)], fill=(3, 6, 11, a))
    bot_start = int(_H * 0.8)
    for y in range(bot_start, _H):
        a = int(200 * ((y - bot_start) / (_H - bot_start)) ** 1.4)
        d.line([(0, y), (_W, y)], fill=(3, 6, 11, a))
    return layer


def _text_with_shadow(draw, xy, text, font, fill, spacing):
    x, y = xy
    draw.multiline_text((x + 2, y + 3), text, font=font, fill=(0, 0, 0, 180), spacing=spacing)
    draw.multiline_text((x, y), text, font=font, fill=fill, spacing=spacing)


def _chart_panel(img: Image.Image, chart_img: Image.Image, accent: tuple) -> None:
    """Sobrepõe o gráfico real num painel escuro translúcido (posts de mercado)."""
    ar, ag, ab = accent
    pw = _W - 2 * _MARGIN
    ph = int(_H * 0.26)
    px, py = _MARGIN, int(_H * 0.52)
    panel = Image.new("RGBA", (pw, ph), (8, 12, 18, 208))
    pd = ImageDraw.Draw(panel)
    pd.rounded_rectangle([0, 0, pw - 1, ph - 1], radius=18, outline=(ar, ag, ab, 255), width=2)
    img.alpha_composite(panel, (px, py))
    fit = chart_img.copy()
    fit.thumbnail((pw - 40, ph - 40))
    img.alpha_composite(fit, (px + (pw - fit.width) // 2, py + (ph - fit.height) // 2))


def build_card(
    headline: str,
    content_type: str,
    handle: str,
    out_path: str,
    chart_img: Image.Image | None = None,
    seed: int = 0,
    background: Image.Image | None = None,
) -> str:
    accent = scene.palette_for(seed)["glow"]
    ar, ag, ab = accent

    if background is not None:
        img = _cover(background)
        img.alpha_composite(_scrims())
    else:
        # Sem foto de IA: usa a cena desenhada (com o gráfico como tela, se mercado).
        img = scene.render_scene(_W, _H, seed=seed, screen_img=chart_img)
        img.alpha_composite(_top_scrim())
        chart_img = None  # já embutido como a tela do monitor

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

    # Gráfico real num painel (posts de mercado com fundo de IA).
    if chart_img is not None:
        _chart_panel(img, chart_img, accent)

    # Assinatura (@) no rodapé.
    hf = _font(True, 34)
    hy = _H - 92
    draw.ellipse([_MARGIN, hy + 9, _MARGIN + 18, hy + 27], fill=(ar, ag, ab, 255))
    _text_with_shadow(draw, (_MARGIN + 32, hy), handle, hf, (230, 233, 237), spacing=0)

    img.convert("RGB").save(out_path, "PNG")
    return out_path


def _top_scrim() -> Image.Image:
    """Véu escuro só no topo, para o modo de cena desenhada (fallback)."""
    scrim = Image.new("RGBA", (_W, _H), (0, 0, 0, 0))
    d = ImageDraw.Draw(scrim)
    fade = int(_H * 0.62)
    for y in range(fade):
        a = int(232 * (1 - y / fade) ** 1.6)
        d.line([(0, y), (_W, y)], fill=(3, 6, 11, a))
    return scrim
