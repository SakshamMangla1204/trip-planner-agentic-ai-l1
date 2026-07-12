import json
import re
from typing import Any

from logger import setup_logger

parser_logger = setup_logger('parser')


def _clean_response(response: str) -> str:
    """Strip whitespace and remove Markdown code fences from the response."""
    parser_logger.info("Cleaning response")

    cleaned = response.strip()

    # Remove Markdown code fences: ```json, ```JSON, or plain ```
    cleaned = re.sub(r'^```(?:json|JSON)\s*', '', cleaned)
    cleaned = re.sub(r'\s*```\s*$', '', cleaned)
    cleaned = cleaned.strip()

    parser_logger.info("Markdown removed")
    return cleaned


def _extract_json(text: str) -> str:
    """Extract the first JSON object or JSON array from text that may contain
    surrounding explanatory text."""
    # Try to find a JSON object { ... }
    obj_match = re.search(r'\{.*\}', text, re.DOTALL)
    if obj_match:
        return obj_match.group(0)

    # Try to find a JSON array [ ... ]
    arr_match = re.search(r'\[.*\]', text, re.DOTALL)
    if arr_match:
        return arr_match.group(0)

    # No JSON structure found – return the cleaned text as-is so json.loads
    # can produce a meaningful error
    return text


def parse_json_response(response: str) -> list[dict[str, Any]]:
    parser_logger.info("Parsing LLM response")

    try:
        # Step 1: clean whitespace and markdown fences
        cleaned = _clean_response(response)

        # Step 2: extract the JSON portion from surrounding text
        json_str = _extract_json(cleaned)
        parser_logger.info("JSON extracted successfully")

        # Step 3: parse
        parsed = json.loads(json_str)
        parser_logger.info("Parsing successful")

        if isinstance(parsed, dict):
            # If the dict has a single key whose value is a list,
            # unwrap it — the LLM wraps the list inside a named key
            # (e.g. {"travel_options": [...]}).
            keys = list(parsed.keys())
            if len(keys) == 1 and isinstance(parsed[keys[0]], list):
                return parsed[keys[0]]
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