from __future__ import annotations
import requests
from urllib.parse import urlparse, parse_qs

def _extract_file_id(url: str) -> str | None:
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    return qs.get("id", [None])[0]

def download_text_from_gdrive(url: str, timeout: int = 30) -> str:
    """
    Faz o fluxo de confirmação do Google Drive e retorna o conteúdo como texto.
    Levanta requests.exceptions em caso de falha.
    """
    session = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0"}
    file_id = _extract_file_id(url)
    if not file_id:
        raise ValueError("URL do Google Drive inválida: id ausente.")

    resp = session.get(url, stream=True, headers=headers, timeout=timeout)
    token = None
    for k, v in resp.cookies.items():
        if k.startswith("download_warning"):
            token = v
            break
    if token:
        params = {"id": file_id, "export": "download", "confirm": token}
        resp = session.get("https://drive.google.com/uc", params=params, stream=True, headers=headers, timeout=timeout)

    resp.raise_for_status()
    return resp.text
