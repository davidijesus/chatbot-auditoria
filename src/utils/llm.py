import os
import requests
from src.config import settings

OPENAI_BASE_URL = "https://api.openai.com/v1"

def _headers() -> dict:
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY não está configurada. Crie um .env baseado no .env.example.")
    return {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }

def embed_texts(texts: list[str], model: str = "text-embedding-3-small") -> list[list[float]]:
    payload = {"model": model, "input": texts}
    r = requests.post(f"{OPENAI_BASE_URL}/embeddings", headers=_headers(), json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()["data"]
    return [item["embedding"] for item in data]

def chat(system: str, user: str, model: str | None = None) -> str:
    m = model or settings.openai_model
    payload = {
        "model": m,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.0,
    }
    r = requests.post(f"{OPENAI_BASE_URL}/chat/completions", headers=_headers(), json=payload, timeout=60)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]
