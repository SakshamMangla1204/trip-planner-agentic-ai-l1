from typing import Final

LLM_TEMPERATURE: Final[float] = 0.0
LLM_MAX_OUTPUT_TOKENS: Final[int] = 500

PRIMARY_PROVIDER: Final[str] = "groq"
FALLBACK_PROVIDER: Final[str] = "mistral"

GROQ_MODEL: Final[str] = "llama-3.3-70b-versatile"

MISTRAL_MODEL: Final[str] = "mistral-large-latest"

TAVILY_MAX_RESULTS: Final[int] = 10
TAVILY_SEARCH_DEPTH: Final[str] = "advanced"

MAX_TRAVEL_OPTIONS: Final[int] = 5
MAX_HOTEL_OPTIONS: Final[int] = 5
MAX_FOOD_OPTIONS: Final[int] = 5
MAX_ACTIVITY_OPTIONS: Final[int] = 5

MAX_BUDGET_PERCENT: Final[float] = 1.0

LLM_TIMEOUT: Final[int] = 60
SEARCH_TIMEOUT: Final[int] = 30

PHOENIX_PROJECT_NAME: Final[str] = "trip-planner"
PHOENIX_COLLECTOR_ENDPOINT: Final[str] = "http://localhost:6006"

LOG_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL: Final[str] = "INFO"

APP_NAME: Final[str] = "AI Trip Planner"
APP_VERSION: Final[str] = "1.0.0"