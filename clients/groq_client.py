import os

from langchain_groq import ChatGroq

from config.settings import (
    GROQ_MODEL,
    LLM_TEMPERATURE,
    LLM_MAX_OUTPUT_TOKENS,
    LLM_TIMEOUT,
)
from clients.base import BaseLLMProvider


class GroqProvider(BaseLLMProvider):
    def get_client(self) -> ChatGroq:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")

        return ChatGroq(
            model=GROQ_MODEL,
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_OUTPUT_TOKENS,
            timeout=LLM_TIMEOUT,
            api_key=api_key,
        )