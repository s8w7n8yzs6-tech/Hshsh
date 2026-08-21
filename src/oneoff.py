"""Post ÚNICO (one-off) — estilo tweet sobre a alta do Bitcoin e os ~US$ 3 bi em
shorts liquidados. Carrossel de 3 slides. Não faz parte do rodízio automático:
roda só quando disparado manualmente (workflow oneoff-btc.yml).

Uso:
    python -m src.oneoff [--dry-run]
"""
from __future__ import annotations

import argparse
import math
import os
import shutil
import sys
import tempfile

import requests
from PIL import Image, ImageDraw

from . import cards, config

_TH = {"bg": (22, 16, 8), "bg2": (9, 6, 3), "fg": (247, 242, 234),
       "muted": (201, 180, 150), "accent": (247, 147, 26), "dark": True}
_W, _H, _M = cards._W, cards._H, cards._MARGIN

_CAPTION = (
    "🚨 O Bitcoin disparou para a máxima desde junho e liquidou mais de "
    "US$ 3 BILHÕES em posições vendidas (shorts). Foram cerca de 188 mil traders "
    "zerados — o maior short squeeze desde 2021.\n\n"
    "Quem apostou na queda virou combustível da alta. ⚡\n\n"
    "Não é recomendação de compra ou venda — é o mercado lembrando por que gestão "
    "de risco e stop existem.\n\n"
    "#bitcoin #btc #cripto #mercadofinanceiro #trade\n\n@thiago.cunhaff"
)
_TWEET = (
    "O Bitcoin explodiu e levou junto US$ 3 BI em shorts. "
    "188 mil traders liquidados — o maior short squeeze desde 2021. "
    "Quem apostou na queda virou o combustível da alta."
)


def _btc_candles():
    r = requests.get(
        "https://api.coingecko.com/api/v3/coins/bitcoin/ohlc",
        params={"vs_currency": "usd", "days": 14},
        headers={"User-Agent": "Mozilla/5.0 (HshshBot)"}, timeout=30,
    )
    rows = r.json()
    candles = [{"o": o, "h": h, "l": l, "c": c} for _ts, o, h, l, c in rows][-48:]
    return candles


def _brl_num(v: float) -> str:
    return f"{v:,.0f}".replace(",", ".")


def _tweet_slide(out_path: str) -> str:
    th = _TH
    img = cards._bg(th)
    d = ImageDraw.Draw(img)
    ac = th["accent"]

    # Avatar (círculo com inicial) + nome + selo + @handle.
    ax, ay, ar = _M, _M + 6, 54
    d.ellipse([ax, ay, ax + 2 * ar, ay + 2 * ar], fill=ac)
    af = cards._font(cards._SANS_B, 58)
    tb = d.textbbox((0, 0), "T", font=af)
    d.text((ax + ar - (tb[2] - tb[0]) / 2 - tb[0], ay + ar - (tb[3] - tb[1]) / 2 - tb[1]), "T",
           font=af, fill=(20, 14, 6))
    nx = ax + 2 * ar + 26
    nf = cards._font(cards._SANS_B, 44)
    d.text((nx, ay + 2), "Thiago", font=nf, fill=th["fg"])
    nb = d.textbbox((nx, ay + 2), "Thiago", font=nf)
    # selo de verificado (círculo accent + check)
    cx, cy, cr = nb[2] + 24, ay + 26, 18
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=ac)
    d.line([(cx - 8, cy), (cx - 2, cy + 7), (cx + 9, cy - 8)], fill=(20, 14, 6), width=4)
    hf = cards._font(cards._SANS_R, 32)
    d.text((nx, ay + 58), "@thiago.cunhaff · agora", font=hf, fill=th["muted"])

    # Texto do tweet (grande).
    ty = ay + 2 * ar + 40
    tw, tf, tsp = cards._wrap_fit(d, _TWEET, cards._SANS_B, _W - 2 * _M, 620, 62, 40, spacing_ratio=0.3)
    d.multiline_text((_M, ty), tw, font=tf, fill=th["fg"], spacing=tsp)
    tbb = d.multiline_textbbox((_M, ty), tw, font=tf, spacing=tsp)

    # Hora + separador.
    sy = tbb[3] + 46
    d.text((_M, sy), "14:20 · 20 de ago de 2026", font=hf, fill=th["muted"])
    d.line([(_M, sy + 58), (_W - _M, sy + 58)], fill=(70, 58, 40), width=2)

    # Ícones de ação (sem números — não fabricar métricas).
    iy = sy + 96
    ix = _M
    gap = int((_W - 2 * _M) / 3)
    # responder (balão)
    d.rounded_rectangle([ix, iy, ix + 40, iy + 30], radius=10, outline=th["muted"], width=3)
    d.polygon([(ix + 10, iy + 30), (ix + 10, iy + 44), (ix + 24, iy + 30)], fill=th["muted"])
    # repostar (setas)
    rx = ix + gap
    d.line([(rx + 4, iy + 8), (rx + 34, iy + 8)], fill=th["muted"], width=3)
    d.line([(rx + 34, iy + 8), (rx + 27, iy + 1)], fill=th["muted"], width=3)
    d.line([(rx + 34, iy + 8), (rx + 27, iy + 15)], fill=th["muted"], width=3)
    d.line([(rx + 34, iy + 30), (rx + 4, iy + 30)], fill=th["muted"], width=3)
    d.line([(rx + 4, iy + 30), (rx + 11, iy + 23)], fill=th["muted"], width=3)
    d.line([(rx + 4, iy + 30), (rx + 11, iy + 37)], fill=th["muted"], width=3)
    # curtir (coração accent)
    lx = ix + 2 * gap
    d.ellipse([lx, iy + 4, lx + 20, iy + 24], fill=ac)
    d.ellipse([lx + 16, iy + 4, lx + 36, iy + 24], fill=ac)
    d.polygon([(lx + 2, iy + 16), (lx + 34, iy + 16), (lx + 18, iy + 40)], fill=ac)

    img.convert("RGB").save(out_path, "PNG")
    return out_path


def _chart_slide(candles, out_path: str) -> str:
    from . import chart

    th = _TH
    price = candles[-1]["c"]
    change = (candles[-1]["c"] / candles[0]["o"] - 1) * 100
    img = cards._bg(th)
    d = ImageDraw.Draw(img)
    cards._badge(d, th, "AGORA NO MERCADO")

    ty = _M + 96
    tw, tf, tsp = cards._wrap_fit(d, "Bitcoin disparou", cards._SANS_B, _W - 2 * _M, 150, 88, 54)
    d.multiline_text((_M, ty), tw, font=tf, fill=th["fg"], spacing=tsp)

    pf = cards._font(cards._SANS_B, 52)
    d.text((_M, ty + 150), f"US$ {_brl_num(price)}", font=pf, fill=th["fg"])

    try:
        ci = chart.render_candles(candles, "Bitcoin (BTC)", change, interval="diário")
        maxw, maxh = _W - 2 * _M, 620
        cw, chh = ci.size
        sc = min(maxw / cw, maxh / chh)
        ci = ci.resize((int(cw * sc), int(chh * sc)))
        img.alpha_composite(ci, ((_W - ci.width) // 2, ty + 250))
    except Exception as exc:  # noqa: BLE001
        print(f"Aviso: gráfico falhou: {exc}", file=sys.stderr)

    cards._footer(d, th, config.POST_HANDLE)
    img.convert("RGB").save(out_path, "PNG")
    return out_path


def _number_slide(out_path: str) -> str:
    th = _TH
    img = cards._bg(th)
    d = ImageDraw.Draw(img)
    cards._badge(d, th, "O ESTRAGO")

    nf = cards._font(cards._SANS_B, 300)
    stat = "US$ 3 BI"
    for size in (300, 260, 220, 190):
        nf = cards._font(cards._SANS_B, size)
        if d.textlength(stat, font=nf) <= _W - 2 * _M:
            break
    nb = d.textbbox((0, 0), stat, font=nf)
    d.text(((_W - (nb[2] - nb[0])) // 2 - nb[0], int(_H * 0.28)), stat, font=nf, fill=th["accent"])

    lw, lf, lsp = cards._wrap_fit(d, "em shorts liquidados na alta do Bitcoin",
                                  cards._SANS_B, _W - 2 * _M, 240, 58, 34)
    lb = d.multiline_textbbox((0, 0), lw, font=lf, spacing=lsp)
    d.multiline_text(((_W - (lb[2] - lb[0])) // 2, int(_H * 0.55)), lw, font=lf, fill=th["fg"],
                     spacing=lsp, align="center")
    sub = "188 mil traders zerados · maior short squeeze desde 2021"
    sw, sf, ssp = cards._wrap_fit(d, sub, cards._SANS_R, _W - 2 * _M, 160, 38, 26)
    sbb = d.multiline_textbbox((0, 0), sw, font=sf, spacing=ssp)
    d.multiline_text(((_W - (sbb[2] - sbb[0])) // 2, int(_H * 0.72)), sw, font=sf, fill=th["muted"],
                     spacing=ssp, align="center")

    cards._footer(d, th, config.POST_HANDLE)
    img.convert("RGB").save(out_path, "PNG")
    return out_path


def build(out_dir: str) -> list:
    os.makedirs(out_dir, exist_ok=True)
    candles = _btc_candles()
    return [
        _tweet_slide(os.path.join(out_dir, "slide_00.png")),
        _chart_slide(candles, os.path.join(out_dir, "slide_01.png")),
        _number_slide(os.path.join(out_dir, "slide_02.png")),
    ]


def run(dry_run: bool = False) -> None:
    out_dir = "preview_oneoff" if dry_run else os.path.join(tempfile.gettempdir(), "oneoff")
    shutil.rmtree(out_dir, ignore_errors=True)
    paths = build(out_dir)
    print(f"{len(paths)} slides gerados em {out_dir}.")
    if dry_run:
        print("DRY_RUN — nada publicado.")
        return

    from .post import _host_images
    from .publishers import instagram

    urls = _host_images(paths)
    if len(urls) < 2:
        raise SystemExit("Falha ao hospedar as imagens do post único.")
    post_id = instagram.publish_carousel(urls, _CAPTION)
    print(f"Publicado no Instagram: {post_id}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Post único: alta do Bitcoin / shorts liquidados.")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
