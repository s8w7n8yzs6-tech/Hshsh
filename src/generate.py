"""Geração do conteúdo (chamada da imagem + legenda) usando Claude."""
from __future__ import annotations

import json

import anthropic

from . import config

_BASE_RULES = (
    "Você cria conteúdo para redes sociais sobre trade e mercados financeiros. "
    f"Escreva SEMPRE em {config.POST_LANGUAGE}, incluindo as hashtags. Nunca em inglês.\n"
    "Você deve produzir dois campos:\n"
    "- headline: um GANCHO curto que faça o trader PARAR e PENSAR — de preferência "
    "uma pergunta provocativa ou uma verdade incômoda sobre a mente de quem opera "
    "(máx ~70 caracteres, sem hashtags, sem @, sem aspas). Nada de frase motivacional "
    "genérica ('disciplina é tudo'); prefira algo que gere identificação e reflexão.\n"
    "- caption: o texto completo do post (máx ~400 caracteres) que DESENVOLVE a "
    "reflexão da headline, tom humano e provocador, no máximo 1 ou 2 emojis, "
    "terminando com 3 a 5 hashtags em português.\n"
    "NUNCA dê recomendação de compra/venda, alvo de preço, promessa de lucro ou "
    "aconselhamento financeiro. Nada de 'compre', 'venda', 'vai subir'. "
    "Não inclua @ de usuários nem assinatura (é adicionada depois)."
)

_PROMPTS = {
    "trader": (
        "Tema: um post que faça o trader PENSAR e se ENXERGAR — a mente e a realidade "
        "psicológica de quem opera (ex.: operar pra ter razão em vez de lucrar, o ego "
        "que não aceita o stop, a ilusão de controle, revenge trade, medo e ganância, "
        "a montanha-russa emocional, autossabotagem, paciência, a solidão do day "
        "trade, disciplina que ninguém vê). A headline deve ser um GANCHO reflexivo "
        "(pergunta provocativa ou verdade incômoda) e a legenda desenvolve a ideia de "
        "forma honesta e próxima, falando 'você'. Não é aula técnica nem comentário "
        "de preço — é para tocar o lado mental do trader."
    ),
    "mercado": (
        "Tema: comentário de mercado sobre O ATIVO abaixo (o post traz um gráfico "
        "de candlestick de 30 min). Baseie-se NOS DADOS reais abaixo e descreva o "
        "movimento do dia de forma neutra e informativa, sem prever direção nem "
        "recomendar operações. A headline deve citar o ativo e o movimento do dia."
        "\n\n{market}"
    ),
}

_SCHEMA = {
    "type": "object",
    "properties": {
        "headline": {"type": "string"},
        "caption": {"type": "string"},
    },
    "required": ["headline", "caption"],
    "additionalProperties": False,
}


def generate_post(
    content_type: str,
    market_snapshot: str | None = None,
    angle: str | None = None,
    style: str | None = None,
    avoid: list[str] | None = None,
) -> dict:
    """Gera {headline, caption, type}. `angle`/`style` variam; `avoid` evita repetir posts recentes."""
    if content_type not in _PROMPTS:
        raise ValueError(f"Tipo de conteúdo desconhecido: {content_type}")

    if content_type == "mercado" and not market_snapshot:
        content_type = "trader"

    if content_type == "mercado":
        prompt = _PROMPTS["mercado"].format(market=market_snapshot)
        if angle:
            prompt += f"\n\nEnfoque desta vez: {angle}."
    else:
        prompt = _PROMPTS[content_type]
        if angle:
            prompt += (
                f"\n\nÂngulo específico e OBRIGATÓRIO deste post (escreva exatamente "
                f"sobre isto, de forma original e sem clichês repetidos): {angle}."
            )
        if style:
            prompt += f"\nFormato/estilo deste post: {style}."

    if avoid:
        recentes = "\n".join(f"- {h}" for h in avoid if h)
        if recentes:
            prompt += (
                "\n\nEstes posts recentes JÁ foram publicados. NÃO repita as ideias, "
                "as frases nem as aberturas deles — escreva algo claramente diferente:\n"
                + recentes
            )

    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=config.ANTHROPIC_MODEL,
        max_tokens=700,
        thinking={"type": "disabled"},
        system=_BASE_RULES,
        messages=[{"role": "user", "content": prompt}],
        output_config={"format": {"type": "json_schema", "schema": _SCHEMA}},
    )
    raw = "".join(b.text for b in resp.content if b.type == "text").strip()
    parsed = json.loads(raw)

    headline = parsed["headline"].strip()
    caption = parsed["caption"].strip()

    handle = config.POST_HANDLE
    if handle and handle.lower() not in caption.lower():
        caption = f"{caption}\n\n{handle}"

    return {"headline": headline, "caption": caption, "type": content_type}
