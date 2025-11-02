"""Integration with an open-source Ollama language model for property search."""

from __future__ import annotations

import json
from typing import Any
import httpx

from ..config import get_settings


settings = get_settings()


async def query_smart_agent(prompt: str) -> dict[str, Any]:
    """Send a natural language request to the Ollama model and return the response.

    Parameters
    ----------
    prompt:
        User-provided natural language query regarding real estate needs.
    """

    payload = {
        "model": settings.ollama_model,
        "prompt": prompt,
        "stream": False,
    }

    async with httpx.AsyncClient(base_url=settings.ollama_host, timeout=60) as client:
        response = await client.post("/api/generate", content=json.dumps(payload))
        response.raise_for_status()
        data = response.json()

    return {
        "model": payload["model"],
        "prompt": prompt,
        "response": data.get("response", ""),
    }
