import os

from tavily import TavilyClient

from config.settings import TAVILY_MAX_RESULTS


def get_tavily_client() -> TavilyClient:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY environment variable is not set")

    return TavilyClient(api_key=api_key)