from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


@dataclass(frozen=True)
class AppConfig:
    # LLM
    llm_provider: Optional[str]
    llm_api_key: Optional[str]
    llm_base_url: Optional[str]
    llm_model: Optional[str]

    # Home Assistant
    home_assistant_url: Optional[str]
    home_assistant_token: Optional[str]

    # Speech providers (placeholders for later phases)
    stt_provider: Optional[str]
    tts_provider: Optional[str]


def load_config() -> AppConfig:
    """Load configuration from environment variables and .env file.

    .env is optional and should not be committed.
    """
    load_dotenv(override=False)

    return AppConfig(
        llm_provider=os.getenv("LLM_PROVIDER", "lm_studio"),
        llm_api_key=os.getenv("LLM_API_KEY"),
        llm_base_url=os.getenv("LLM_BASE_URL", "http://localhost:1234/v1"),
        llm_model=os.getenv("LLM_MODEL", "local-model"),
        home_assistant_url=os.getenv("HOME_ASSISTANT_URL"),
        home_assistant_token=os.getenv("HOME_ASSISTANT_TOKEN"),
        stt_provider=os.getenv("STT_PROVIDER"),
        tts_provider=os.getenv("TTS_PROVIDER"),
    )


__all__ = ["AppConfig", "load_config"]


