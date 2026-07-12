"""NSE HTTP client with retries."""

from __future__ import annotations

import time
from dataclasses import dataclass

import requests


@dataclass
class NSEClient:
    timeout_seconds: int = 30
    retries: int = 3

    def __post_init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/octet-stream,*/*",
            }
        )

    def get(self, url: str) -> bytes:
        last_error: Exception | None = None
        for attempt in range(1, self.retries + 1):
            try:
                response = self.session.get(url, timeout=self.timeout_seconds)
                response.raise_for_status()
                return response.content
            except requests.RequestException as exc:
                last_error = exc
                if attempt == self.retries:
                    break
                time.sleep(min(attempt, 3))
        raise RuntimeError(f"Failed to download {url}") from last_error
