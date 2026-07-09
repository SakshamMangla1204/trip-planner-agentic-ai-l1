import os

from langchain_mistralai import ChatMistralAI

from config.settings import (
    MISTRAL_MODEL,
    LLM_TEMPERATURE,
    LLM_MAX_OUTPUT_TOKENS,
    LLM_TIMEOUT,
)
from clients.base import BaseLLMProvider


class MistralProvider(BaseLLMProvider):
    def get_client(self) -> ChatMistralAI:
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY environment variable is not set")

        return ChatMistralAI(
            model=MISTRAL_MODEL,
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_OUTPUT_TOKENS,
            timeout=LLM_TIMEOUT,
            api_key=api_key,
        )