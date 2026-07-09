from typing import Optional

from langchain_ollama import ChatOllama

from config.settings import (
    LLM_MODEL,
    LLM_TEMPERATURE,
    LLM_TOP_P,
    LLM_MAX_OUTPUT_TOKENS,
)


def get_llm() -> ChatOllama:
    return ChatOllama(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        top_p=LLM_TOP_P,
        max_tokens=LLM_MAX_OUTPUT_TOKENS,
    )