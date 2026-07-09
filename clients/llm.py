import logging
from typing import Any, Optional

from clients.base import BaseLLMProvider
from clients.groq_client import GroqProvider
from clients.mistral_client import MistralProvider
from config.settings import PRIMARY_PROVIDER, FALLBACK_PROVIDER

logger = logging.getLogger("llm_client")

PROVIDER_MAP: dict[str, type[BaseLLMProvider]] = {
    "groq": GroqProvider,
    "mistral": MistralProvider,
}

_RETRYABLE_MESSAGES = (
    "rate limit",
    "rate_limit",
    "quota exceeded",
    "quota_exceeded",
    "429",
    "too many requests",
    "service unavailable",
    "503",
    "api unavailable",
    "timeout",
    "timed out",
    "connection error",
    "connection refused",
    "internal server error",
    "500",
    "502",
    "504",
)


def _is_retryable_error(exception: Exception) -> bool:
    message = str(exception).lower()
    for pattern in _RETRYABLE_MESSAGES:
        if pattern in message:
            return True
    return False


def _build_provider(name: str) -> BaseLLMProvider:
    provider_cls = PROVIDER_MAP.get(name)
    if provider_cls is None:
        raise ValueError(
            f"Unknown provider '{name}'. "
            f"Registered providers: {list(PROVIDER_MAP.keys())}"
        )
    return provider_cls()


def _get_client(provider_name: str) -> Any:
    logger.info("Selected provider: %s", provider_name)
    provider = _build_provider(provider_name)
    return provider.get_client()


def get_llm() -> Any:
    primary = PRIMARY_PROVIDER
    fallback = FALLBACK_PROVIDER

    try:
        return _get_client(primary)
    except Exception as exc:
        logger.warning(
            "Primary provider '%s' failed: %s. Attempting fallback to '%s'.",
            primary,
            exc,
            fallback,
        )
        primary_error = exc

        if not _is_retryable_error(exc):
            logger.error(
                "Primary provider '%s' failed with a non-retryable error. "
                "Raising original exception.",
                primary,
            )
            raise

    if fallback is None:
        logger.error(
            "Primary provider '%s' failed and no fallback is configured.",
            primary,
        )
        raise primary_error

    try:
        logger.info(
            "Activating fallback provider: '%s'",
            fallback,
        )
        return _get_client(fallback)
    except Exception as fallback_exc:
        logger.error(
            "Fallback provider '%s' also failed: %s",
            fallback,
            fallback_exc,
        )
        raise RuntimeError(
            f"All LLM providers failed.\n"
            f"  Primary ({primary}): {primary_error}\n"
            f"  Fallback ({fallback}): {fallback_exc}"
        ) from fallback_exc