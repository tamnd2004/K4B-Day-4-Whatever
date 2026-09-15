from __future__ import annotations

import os

from providers.openai_provider import OpenAIProvider


class LocalProvider(OpenAIProvider):
    """LocalProvider uses an OpenAI-compatible Chat Completions surface."""

    def __init__(self) -> None:
        super().__init__(
            api_key_env="9ROUTER_API_KEY",
            base_url=os.getenv("9ROUTER_BASE_URL", "http://localhost:20128/v1"),
            default_model=os.getenv("9ROUTER_MODEL", "openai/gpt-4o-mini"),
        )
