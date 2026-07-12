import time
from dataclasses import dataclass, field

import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

NSE_BASE_URL = 'https://www.nseindia.com'
REPORTS_ENDPOINT = '/api/reports'
REPORTS_REFERER_PATH = '/all-reports'

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
    "image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

@dataclass
class NSEClientConfig:
    base_url: str = NSE_BASE_URL
    timeout: float = 10.0 # in seconds
    max_retries: int = 3
    retry_wait_time: float = 1.0 # in seconds
    warm_up_path: str = REPORTS_REFERER_PATH # loads this page first to collect cookies
    cookie_refresh_seconds: float = 300.0 # in seconds. re-warm session after this duration
    extra_headers: dict = field(default_factory=dict)

class NSEConnectionError(Exception):
    """Raised when an error occurs when connecting to the NSE server."""
    pass

class NSEClient:
    def __init__(self, config: NSEClientConfig):
        self.config = config

        # Build session
        self._session = requests.Session()
        self._session.headers.update(DEFAULT_HEADERS)
        self._session.headers.update(self.config.extra_headers)

        retry_strategy = Retry(
            total=self.config.max_retries,
            backoff_factor=self.config.retry_wait_time,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
            raise_on_status=False
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self._session.mount("https://", adapter)

        self._last_warm_up: float | None = None

    def connect(self, force: bool = False) -> None:
        """Connect to the NSE homepage and establish a session.
        To be called at start-up and re-run when the session looks stale.
        The param 'force' is used to force re-establishing the session."""
        if not force and self._session_is_fresh():
            logger.debug("Session is fresh")
            return

        url = NSE_BASE_URL + self.config.warm_up_path
        logger.info(f"Connecting to {url}")
        try:
            response = self._session.get(url, timeout=self.config.timeout)
        except requests.exceptions.RequestException as e:
            raise NSEConnectionError(f"Error connecting to {url}") from e

        if response.status_code != 200:
            raise NSEConnectionError(f"Error connecting to {url}\n Status code: {response.status_code}")

        if not self._session.cookies:
            logger.warning("Cookies were not set")

        logger.info("Connection established")
        logger.info(f"Status code: {response.status_code}")

    def _session_is_fresh(self) -> bool:
        if self._last_warm_up is None:
            return False

        age = time.monotonic() - self._last_warm_up
        if age > self.config.cookie_refresh_seconds:
            return False

        return True

    def close(self) -> None:
        self._session.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    config = NSEClientConfig()
    client = NSEClient(config)
    try:
        client.connect()
    except NSEConnectionError as e:
        print(f"failed to connect to NSE server: {e}")
    finally:
        client.close()