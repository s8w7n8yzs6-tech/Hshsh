"""Gera um gráfico de variação 24h (cripto) como imagem RGBA para compor no card."""
from __future__ import annotations

import io

import matplotlib

matplotlib.use("Agg")  # backend headless (necessário no GitHub Actions)

import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402

_UP = "#22c55e"    # verde
_DOWN = "#ef4444"  # vermelho


def render_change_chart(data: list[dict]) -> Image.Image:
    """Barras horizontais da variação 24h (%) por ativo. Fundo transparente."""
    labels = [d["short"] for d in data]
    changes = [d["change"] for d in data]
    colors = [_UP if c >= 0 else _DOWN for c in changes]

    fig, ax = plt.subplots(figsize=(8.2, 3.4), dpi=150)
    fig.patch.set_alpha(0.0)
    ax.set_facecolor("none")

    y = range(len(labels))
    ax.barh(list(y), changes, color=colors, height=0.6, zorder=3)
    ax.axvline(0, color="#94a3b8", linewidth=1, zorder=2)

    ax.set_yticks(list(y))
    ax.set_yticklabels(labels, color="white", fontsize=15, fontweight="bold")
    ax.set_xticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0)
    ax.set_title("Variação 24h (%)", color="white", fontsize=14, pad=10, loc="left")

    span = max((abs(c) for c in changes), default=1) or 1
    ax.set_xlim(-span * 1.35, span * 1.35)
    for yi, c in zip(y, changes):
        offset = span * 0.05
        ax.text(
            c + (offset if c >= 0 else -offset),
            yi,
            f"{c:+.2f}%",
            va="center",
            ha="left" if c >= 0 else "right",
            color="white",
            fontsize=14,
            fontweight="bold",
        )

    buf = io.BytesIO()
    fig.savefig(buf, format="png", transparent=True, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("RGBA")
