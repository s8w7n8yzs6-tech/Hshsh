"""Renova o token de longa duração do Instagram e grava no Secret do GitHub.

Fluxo "login do Instagram" (graph.instagram.com): o token de longa duração (60
dias) é renovado com `ig_refresh_token` — não precisa de app id/secret. Rodado
por um workflow agendado semanalmente, mantém a publicação sem intervenção.

Variáveis de ambiente necessárias (Secrets do GitHub):
- INSTAGRAM_ACCESS_TOKEN  -> token atual (será renovado)
- GH_PAT                  -> Personal Access Token com escrita em "Secrets" do repo
- GITHUB_REPOSITORY       -> "owner/repo" (o GitHub Actions define sozinho)
"""
from __future__ import annotations

import base64
import os
import sys

import requests
from nacl import encoding, public

_REFRESH = "https://graph.instagram.com/refresh_access_token"
_SECRET_NAME = "INSTAGRAM_ACCESS_TOKEN"


def _encrypt(public_key_b64: str, value: str) -> str:
    pk = public.PublicKey(public_key_b64.encode(), encoding.Base64Encoder())
    sealed = public.SealedBox(pk)
    return base64.b64encode(sealed.encrypt(value.encode())).decode()


def main() -> None:
    try:
        token = os.environ["INSTAGRAM_ACCESS_TOKEN"]
        gh_pat = os.environ["GH_PAT"]
        repo = os.environ["GITHUB_REPOSITORY"]
    except KeyError as exc:
        print(f"Variável ausente: {exc}. Renovação ignorada.", file=sys.stderr)
        raise SystemExit(1)

    # 1) Renova o token de longa duração (ig_refresh_token — sem app secret).
    r = requests.get(
        _REFRESH,
        params={"grant_type": "ig_refresh_token", "access_token": token},
        timeout=30,
    )
    if r.status_code != 200 or "access_token" not in r.json():
        print(f"Falha ao renovar token: {r.status_code} {r.text[:300]}", file=sys.stderr)
        raise SystemExit(1)
    new_token = r.json()["access_token"]

    # 2) Grava o novo token no Secret do repositório (criptografado).
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
