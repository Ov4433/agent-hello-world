"""Shared helpers for GitHub Actions automation scripts."""

from __future__ import annotations

import json
import os
import time
import urllib.request
from pathlib import Path
from typing import Any
from urllib.error import URLError


DEFAULT_HEADERS = {
    "Accept": "application/json",
    "User-Agent": "agent-hello-world/1.0",
}


def write_github_output(name: str, value: str) -> None:
    output_path = os.getenv("GITHUB_OUTPUT")
    if output_path:
        with open(output_path, "a", encoding="utf-8") as output:
            output.write(f"{name}={value}\n")


def load_json_file(path_value: str, *, label: str) -> dict[str, Any]:
    path = Path(path_value)
    if not path.is_file():
        raise ValueError(f"{label} file does not exist: {path_value}")

    try:
        with path.open("r", encoding="utf-8") as file_handle:
            payload = json.load(file_handle)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label} file is not valid JSON: {path_value}") from exc

    if not isinstance(payload, dict):
        raise ValueError(f"{label} file must contain a JSON object: {path_value}")
    return payload


def request_json(url: str, *, headers: dict[str, str] | None = None, timeout: int = 20, attempts: int = 3) -> Any:
    request_headers = dict(DEFAULT_HEADERS)
    if headers:
        request_headers.update(headers)

    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            request = urllib.request.Request(url, headers=request_headers)
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.load(response)
        except (OSError, URLError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt == attempts:
                break
            time.sleep(attempt)

    raise RuntimeError(f"Failed to fetch JSON from {url}: {last_error}") from last_error


def require_string(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a non-empty string")
    return value.strip()


def require_float(data: dict[str, Any], key: str) -> float:
    value = data.get(key)
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{key} must be a number") from exc


def require_int(data: dict[str, Any], key: str) -> int:
    value = data.get(key)
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{key} must be an integer") from exc


def require_mapping(data: dict[str, Any], key: str, *, default: dict[str, Any] | None = None) -> dict[str, Any]:
    value = data.get(key, default if default is not None else {})
    if not isinstance(value, dict):
        raise ValueError(f"{key} must be a JSON object")
    return value
