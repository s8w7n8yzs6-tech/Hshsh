"""Renova o token de longa duração da Meta e grava de volta no Secret do GitHub.

Rodado por um workflow agendado. Tokens de longa duração da Meta expiram em ~60
dias; re-trocá-los periodicamente mantém a publicação funcionando sem intervenção.

Variáveis de ambiente necessárias (todas como Secrets do GitHub):
- FB_APP_ID, FB_APP_SECRET       -> app do Meta for Developers
- INSTAGRAM_ACCESS_TOKEN         -> token atual (será renovado)
- GH_PAT                         -> Personal Access Token com permissão de escrita
                                    em "Secrets" do repositório
- GITHUB_REPOSITORY              -> "owner/repo" (o GitHub Actions define sozinho)
"""
from __future__ import annotations

import base64
import os
import sys

import requests
from nacl import encoding, public

_GRAPH = "https://graph.facebook.com/v21.0/oauth/access_token"
_SECRET_NAME = "INSTAGRAM_ACCESS_TOKEN"


def _encrypt(public_key_b64: str, value: str) -> str:
    pk = public.PublicKey(public_key_b64.encode(), encoding.Base64Encoder())
    sealed = public.SealedBox(pk)
    return base64.b64encode(sealed.encrypt(value.encode())).decode()


def main() -> None:
    try:
        app_id = os.environ["FB_APP_ID"]
        app_secret = os.environ["FB_APP_SECRET"]
        token = os.environ["INSTAGRAM_ACCESS_TOKEN"]
        gh_pat = os.environ["GH_PAT"]
        repo = os.environ["GITHUB_REPOSITORY"]
    except KeyError as exc:
        print(f"Variável ausente: {exc}. Renovação ignorada.", file=sys.stderr)
        raise SystemExit(1)

    # 1) Re-troca o token por um novo de longa duração (renova ~60 dias).
    r = requests.get(
        _GRAPH,
        params={
            "grant_type": "fb_exchange_token",
            "client_id": app_id,
            "client_secret": app_secret,
            "fb_exchange_token": token,
        },
        timeout=30,
    )
    if r.status_code != 200 or "access_token" not in r.json():
        print(f"Falha ao renovar token: {r.status_code} {r.text[:300]}", file=sys.stderr)
        raise SystemExit(1)
    new_token = r.json()["access_token"]

    # 2) Grava o novo token no Secret do repositório (criptografado com a chave pública).
    headers = {"Authorization": f"Bearer {gh_pat}", "Accept": "application/vnd.github+json"}
    pk = requests.get(
        f"https://api.github.com/repos/{repo}/actions/secrets/public-key",
        headers=headers,
        timeout=30,
    )
    pk.raise_for_status()
    pk = pk.json()

    put = requests.put(
        f"https://api.github.com/repos/{repo}/actions/secrets/{_SECRET_NAME}",
        headers=headers,
        json={"encrypted_value": _encrypt(pk["key"], new_token), "key_id": pk["key_id"]},
        timeout=30,
    )
    if put.status_code not in (201, 204):
        print(f"Falha ao gravar o Secret: {put.status_code} {put.text[:300]}", file=sys.stderr)
        raise SystemExit(1)

    print(f"Token renovado e Secret '{_SECRET_NAME}' atualizado com sucesso.")


if __name__ == "__main__":
    main()
