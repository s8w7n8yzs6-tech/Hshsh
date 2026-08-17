"""Geração do conteúdo com Claude — um formato diferente por tipo de post.

Cada formato (foto, mercado, citacao, lista, mito_verdade, numero) tem seu
próprio prompt e esquema de saída. Retorna sempre `caption`, `fmt` e um campo
`main` (texto representativo, usado para não repetir e para log).
"""
from __future__ import annotations

import json

import anthropic

from . import config

_BASE_RULES = (
    "Você cria conteúdo para o Instagram de um trader, sobre a MENTE e a rotina de "
    f"quem opera. Escreva SEMPRE em {config.POST_LANGUAGE}, incluindo hashtags. "
    "Nunca em inglês.\n"
    "Regras invioláveis: NUNCA dê recomendação de compra/venda, alvo de preço, "
    "promessa de lucro ou aconselhamento financeiro. Nada de 'compre', 'venda', "
    "'vai subir'. Não invente estatísticas de pesquisa nem números de desempenho. "
    "Não inclua @ de usuário nem assinatura (é adicionada depois). Sem aspas "
    "desnecessárias. Tom humano, direto e que gera identificação."
)

_FMT = {
    "foto": {
        "schema": {"headline": {"type": "string"}, "caption": {"type": "string"}},
        "required": ["headline", "caption"],
        "main": "headline",
        "prompt": (
            "Formato FOTO-REFLEXÃO (a imagem é uma foto de um trader). Crie:\n"
            "- headline: um GANCHO curto (pergunta provocativa ou verdade incômoda "
            "sobre a mente do trader), máx ~70 caracteres, sem hashtags.\n"
            "- caption: desenvolve a reflexão (máx ~400 caracteres), 1-2 emojis no "
            "máximo, terminando com 3-5 hashtags."
        ),
    },
    "citacao": {
        "schema": {"statement": {"type": "string"}, "caption": {"type": "string"}},
        "required": ["statement", "caption"],
        "main": "statement",
        "prompt": (
            "Formato CITAÇÃO (frase de destaque em fundo limpo). Crie:\n"
            "- statement: uma frase FORTE e original sobre disciplina/psicologia do "
            "trader, de impacto, máx ~120 caracteres, sem aspas e sem hashtags.\n"
            "- caption: comenta/expande a frase (máx ~400 caracteres), 1-2 emojis, "
            "terminando com 3-5 hashtags."
        ),
    },
    "lista": {
        "schema": {
            "title": {"type": "string"},
            "items": {"type": "array", "items": {"type": "string"}},
            "caption": {"type": "string"},
        },
        "required": ["title", "items", "caption"],
        "main": "title",
        "prompt": (
            "Formato LISTA (conteúdo pra salvar). Crie:\n"
            "- title: um título chamativo (ex.: '3 sinais de que você está em revenge "
            "trade', '4 hábitos do trader consistente'), máx ~60 caracteres.\n"
            "- items: de 3 a 5 itens CURTOS e diretos (cada um máx ~70 caracteres), "
            "sem numeração (o número é desenhado automaticamente).\n"
            "- caption: fecha a ideia (máx ~400 caracteres), 1-2 emojis, com 3-5 hashtags."
        ),
    },
    "mito_verdade": {
        "schema": {"mito": {"type": "string"}, "verdade": {"type": "string"}, "caption": {"type": "string"}},
        "required": ["mito", "verdade", "caption"],
        "main": "verdade",
        "prompt": (
            "Formato MITO x VERDADE (card dividido). Crie:\n"
            "- mito: uma crença COMUM e equivocada do trader iniciante, curta (máx ~90 caracteres).\n"
            "- verdade: a visão madura que corrige o mito, curta (máx ~90 caracteres).\n"
            "- caption: explica o contraste (máx ~400 caracteres), 1-2 emojis, com 3-5 hashtags."
        ),
    },
    "numero": {
        "schema": {"stat": {"type": "string"}, "label": {"type": "string"}, "caption": {"type": "string"}},
        "required": ["stat", "label", "caption"],
        "main": "label",
        "prompt": (
            "Formato NÚMERO DE IMPACTO (um número gigante + um texto). Crie:\n"
            "- stat: um número/símbolo CURTO e retórico sobre mentalidade (ex.: '1', "
            "'2x', 'R$0', '10min', '-1%'). NÃO é estatística de pesquisa nem promessa "
            "de lucro — é um recurso de reflexão.\n"
            "- label: a frase que dá sentido ao número (máx ~90 caracteres).\n"
            "- caption: desenvolve (máx ~400 caracteres), 1-2 emojis, com 3-5 hashtags."
        ),
    },
    "padrao": {
        "schema": {"explicacao": {"type": "string"}, "caption": {"type": "string"}},
        "required": ["explicacao", "caption"],
        "main": "explicacao",
        "prompt": (
            "Formato APRENDA UM PADRÃO (o card mostra um DIAGRAMA do padrão). Ensine, "
            "de forma EDUCATIVA e para iniciantes, o padrão indicado abaixo. É ENSINO, "
            "não recomendação: não mande comprar/vender/entrar; deixe implícito que "
            "serve para estudo e deve ser confirmado com o método e a gestão de risco.\n"
            "- explicacao: 1 a 2 frases (máx ~180 caracteres) dizendo o que é o padrão "
            "e o que ele costuma sinalizar, de forma neutra.\n"
            "- caption: aprofunda de forma didática (máx ~400 caracteres), 1-2 emojis, "
            "terminando com 3-5 hashtags."
        ),
    },
    "conceito": {
        "schema": {"titulo": {"type": "string"}, "explicacao": {"type": "string"}, "caption": {"type": "string"}},
        "required": ["titulo", "explicacao", "caption"],
        "main": "titulo",
        "prompt": (
            "Formato APRENDA (educativo). Ensine, para iniciantes, o tema indicado "
            "abaixo — pode ser um CONCEITO, um INDICADOR técnico ou uma ESTRATÉGIA de "
            "trade. Explique o que é e como costuma ser usado/observado, de forma clara "
            "e prática. É ENSINO, não recomendação: não mande comprar/vender, não dê "
            "alvo de preço nem prometa resultado; deixe implícito que precisa ser "
            "confirmado com o método e a gestão de risco de cada um.\n"
            "- titulo: título curto e claro do tema (máx ~48 caracteres).\n"
            "- explicacao: explicação didática (máx ~240 caracteres).\n"
            "- caption: complementa (máx ~400 caracteres), 1-2 emojis, com 3-5 hashtags."
        ),
    },
    "dica": {
        "schema": {
            "title": {"type": "string"},
            "items": {"type": "array", "items": {"type": "string"}},
            "caption": {"type": "string"},
        },
        "required": ["title", "items", "caption"],
        "main": "title",
        "prompt": (
            "Formato DICAS (lista educativa pra salvar) sobre o tema indicado abaixo, "
            "para o trader evoluir. Educativo, sem recomendar operação específica.\n"
            "- title: título chamativo (máx ~58 caracteres).\n"
            "- items: de 3 a 5 dicas CURTAS e acionáveis (cada uma máx ~70 caracteres), "
            "sem numeração (o número é desenhado).\n"
            "- caption: fecha (máx ~400 caracteres), 1-2 emojis, com 3-5 hashtags."
        ),
    },
    "mercado": {
        "schema": {"headline": {"type": "string"}, "caption": {"type": "string"}},
        "required": ["headline", "caption"],
        "main": "headline",
        "prompt": (
            "Formato MERCADO (o post traz um gráfico de candlestick de 30 min do ativo "
            "abaixo). Baseie-se NOS DADOS reais e descreva o movimento do dia de forma "
            "neutra, sem prever direção nem recomendar operação.\n"
            "- headline: cita o ativo e o movimento do dia (máx ~70 caracteres).\n"
            "- caption: comenta os dados (máx ~400 caracteres), 1-2 emojis, com 3-5 hashtags.\n\n"
            "{market}"
        ),
    },
}


def _schema(fmt: str) -> dict:
    spec = _FMT[fmt]
    return {
        "type": "object",
        "properties": spec["schema"],
        "required": spec["required"],
        "additionalProperties": False,
    }


def generate_post(
    fmt: str,
    market_snapshot: str | None = None,
    angle: str | None = None,
    avoid: list[str] | None = None,
) -> dict:
    """Gera o conteúdo do formato `fmt`. Retorna dict com os campos do formato + caption/fmt/main."""
    if fmt not in _FMT:
        raise ValueError(f"Formato desconhecido: {fmt}")
    if fmt == "mercado" and not market_snapshot:
        fmt = "foto"  # sem dados de mercado, cai para foto-reflexão

    spec = _FMT[fmt]
    if fmt == "mercado":
        prompt = spec["prompt"].format(market=market_snapshot)
        if angle:
            prompt += f"\n\nEnfoque desta vez: {angle}."
    else:
        prompt = spec["prompt"]
        if angle:
            prompt += (
                f"\n\nTEMA OBRIGATÓRIO deste post (escreva sobre isto, de forma "
                f"original e sem clichês): {angle}."
            )

    if avoid:
        recentes = "\n".join(f"- {h}" for h in avoid if h)
        if recentes:
            prompt += (
                "\n\nEstes posts recentes JÁ saíram. NÃO repita as ideias, frases nem "
                "as aberturas — escreva algo claramente diferente:\n" + recentes
            )

    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=config.ANTHROPIC_MODEL,
        max_tokens=800,
        thinking={"type": "disabled"},
        system=_BASE_RULES,
        messages=[{"role": "user", "content": prompt}],
        output_config={"format": {"type": "json_schema", "schema": _schema(fmt)}},
    )
    raw = "".join(b.text for b in resp.content if b.type == "text").strip()
    parsed = json.loads(raw)

    # Normaliza espaços e limpa campos de texto.
    out: dict = {"fmt": fmt}
    for key in spec["schema"]:
        val = parsed.get(key)
        if isinstance(val, str):
            out[key] = val.strip()
        elif isinstance(val, list):
            out[key] = [str(x).strip() for x in val if str(x).strip()]
        else:
            out[key] = val

    handle = config.POST_HANDLE
    caption = out.get("caption", "")
    if handle and handle.lower() not in caption.lower():
        out["caption"] = f"{caption}\n\n{handle}".strip()
    out["main"] = out.get(spec["main"]) if isinstance(out.get(spec["main"]), str) else out.get("caption", "")
    return out
