"""Geração do texto do post usando a API da Anthropic (Claude)."""
from __future__ import annotations

import anthropic

from . import config

_BASE_RULES = (
    "Você escreve posts curtos para redes sociais sobre trade e mercados financeiros. "
    f"Escreva SEMPRE em {config.POST_LANGUAGE} — incluindo o corpo e as hashtags. "
    "Nunca escreva em inglês ou em outro idioma. Regras:\n"
    "- No máximo ~400 caracteres.\n"
    "- Tom claro, direto e envolvente; use no máximo 1 ou 2 emojis.\n"
    "- Termine com 3 a 5 hashtags relevantes (em português).\n"
    "- NUNCA dê recomendação de compra/venda, alvo de preço, promessa de lucro "
    "ou aconselhamento financeiro. Nada de 'compre', 'venda', 'vai subir'.\n"
    "- Não inclua @ de usuários nem assinatura; isso é adicionado automaticamente depois.\n"
    "- Responda APENAS com o texto final do post, sem comentários seus."
)

_PROMPTS = {
    "motivacional": (
        "Crie um post motivacional/de engajamento sobre a jornada e a mentalidade "
        "de quem opera no mercado (disciplina, paciência, gestão de risco, aprender "
        "com erros). Sem números específicos de mercado."
    ),
    "educacional": (
        "Crie um post educacional que explique, de forma simples e acessível, um "
        "conceito de trade ou análise (ex.: suporte/resistência, stop-loss, "
        "diversificação, volatilidade, risco x retorno). Escolha um conceito e "
        "explique-o brevemente."
    ),
    "mercado": (
        "Crie um post de comentário de mercado baseado NOS DADOS reais fornecidos "
        "abaixo. Descreva o movimento de forma neutra e informativa, sem prever "
        "direção futura nem recomendar operações.\n\n{market}"
    ),
}


def generate_post(content_type: str, market_snapshot: str | None = None) -> str:
    """Gera o texto de um post do tipo indicado. Levanta ValueError se o tipo for inválido."""
    if content_type not in _PROMPTS:
        raise ValueError(f"Tipo de conteúdo desconhecido: {content_type}")

    if content_type == "mercado":
        if not market_snapshot:
            # Sem dados reais não fazemos comentário de mercado — cai para educacional.
            content_type = "educacional"
        else:
            prompt = _PROMPTS["mercado"].format(market=market_snapshot)

    if content_type != "mercado":
        prompt = _PROMPTS[content_type]

    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=config.ANTHROPIC_MODEL,
        max_tokens=500,
        thinking={"type": "disabled"},  # posts curtos não precisam de raciocínio estendido
        system=_BASE_RULES,
        messages=[{"role": "user", "content": prompt}],
    )
    text = "".join(b.text for b in resp.content if b.type == "text").strip()

    # Acrescenta o @ (assinatura) ao final, se ainda não estiver presente.
    handle = config.POST_HANDLE
    if handle and handle.lower() not in text.lower():
        text = f"{text}\n\n{handle}"
    return text
