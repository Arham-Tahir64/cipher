from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from typing import Any, Dict

import requests

from packages.shared import AppConfig


class LLMClient(ABC):
    @abstractmethod
    def generate_structured_intent(self, prompt_messages: list[dict[str, str]]) -> Dict[str, Any]:
        """Return a JSON object parsed as dict, representing the intent payload."""
        raise NotImplementedError


class LMStudioLLMClient(LLMClient):
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate_structured_intent(self, prompt_messages: list[dict[str, str]]) -> Dict[str, Any]:
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model,
            "messages": prompt_messages,
            "temperature": 0,
        }
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"].strip()

        # Best effort to extract JSON object
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            match = re.search(r"\{[\s\S]*\}", content)
            if match:
                return json.loads(match.group(0))
            raise


def get_llm_client(config: AppConfig) -> LLMClient:
    # Default to LM Studio local server
    provider = (config.llm_provider or "lm_studio").lower()
    if provider == "lm_studio":
        return LMStudioLLMClient(
            base_url=config.llm_base_url or "http://localhost:1234/v1",
            model=config.llm_model or "local-model",
        )
    # Fallback to LM Studio if unknown, to keep local-first
    return LMStudioLLMClient(
        base_url=config.llm_base_url or "http://localhost:1234/v1",
        model=config.llm_model or "local-model",
    )


__all__ = ["LLMClient", "LMStudioLLMClient", "get_llm_client"]


