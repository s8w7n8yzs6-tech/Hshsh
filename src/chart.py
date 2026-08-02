"""Gráfico de candlestick (30 min) como imagem RGBA para compor no card."""
from __future__ import annotations

import io

import matplotlib

matplotlib.use("Agg")  # backend headless (necessário no GitHub Actions)

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402
from PIL import Image  # noqa: E402

_UP = "#22c55e"     # verde (alta)
_DOWN = "#ef4444"   # vermelho (baixa)
_GRID = "#94a3b8"


def render_candles(candles: list[dict], label: str, change: float, interval: str = "30min") -> Image.Image:
    """Desenha candlesticks OHLC. Fundo transparente, tema escuro."""
    fig, ax = plt.subplots(figsize=(8.6, 5.6), dpi=150)
    fig.patch.set_alpha(0.0)
    ax.set_facecolor("none")

    highs = [c["h"] for c in candles]
    lows = [c["l"] for c in candles]
    price_range = (max(highs) - min(lows)) or 1.0

    for i, cd in enumerate(candles):
        o, h, l, c = cd["o"], cd["h"], cd["l"], cd["c"]
        color = _UP if c >= o else _DOWN
        # pavio (máxima-mínima)
        ax.plot([i, i], [l, h], color=color, linewidth=1.1, zorder=2)
        # corpo (abertura-fechamento)
        body_low = min(o, c)
        body_h = abs(c - o) or price_range * 0.0008
        ax.add_patch(
            Rectangle((i - 0.32, body_low), 0.64, body_h, facecolor=color, edgecolor=color, zorder=3)
        )

    ax.set_xlim(-1, len(candles))
    pad = price_range * 0.08
    ax.set_ylim(min(lows) - pad, max(highs) + pad)

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks([])
    ax.grid(axis="y", color=_GRID, alpha=0.16, linewidth=1)
    ax.yaxis.tick_right()
    ax.tick_params(length=0, colors="white", labelsize=13)
    ax.yaxis.set_major_formatter(lambda v, _pos: f"{v:,.0f}")

    sign = "+" if change >= 0 else ""
    title_color = _UP if change >= 0 else _DOWN
    ax.set_title(
        f"{label} · {interval}    {sign}{change:.2f}%",
        color=title_color,
        fontsize=16,
        loc="left",
        pad=14,
        fontweight="bold",
    )

    buf = io.BytesIO()
    fig.savefig(buf, format="png", transparent=True, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("RGBA")
