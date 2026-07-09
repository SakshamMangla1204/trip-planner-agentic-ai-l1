import json
from typing import Any

from logger import setup_logger

parser_logger = setup_logger('parser')


def parse_json_response(response: str) -> list[dict[str, Any]]:
    parser_logger.info("Parsing LLM response")
    try:
        parsed = json.loads(response)

        if isinstance(parsed, dict):
            return [parsed]
        elif isinstance(parsed, list):
            return parsed
        else:
            raise ValueError(f"Unexpected JSON format: {type(parsed)}")

    except json.JSONDecodeError as exc:
        parser_logger.error(f"Invalid JSON received: {exc}")
        raise ValueError(f"Invalid JSON response: {exc}") from exc
    except Exception as exc:
        parser_logger.error(f"Unexpected error parsing response: {exc}")
        raise ValueError(f"Failed to parse response: {exc}") from exc