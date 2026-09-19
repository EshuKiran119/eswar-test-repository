from dataclasses import dataclass
from urllib.parse import urlsplit
import os


@dataclass(frozen=True)
class Settings:
    base_url: str
    timeout: float = 5.0

    @classmethod
    def load(cls, url):
        p = urlsplit(url)
        if (
            p.scheme not in ("http", "https")
            or not p.hostname
            or p.username
            or p.password
            or p.query
            or p.fragment
        ):
            raise ValueError("Use a base URL without credentials, query or fragment")
        if (
            p.hostname not in ("127.0.0.1", "localhost", "::1")
            and os.getenv("ALLOW_REMOTE_TARGET", "false").lower() != "true"
        ):
            raise ValueError("Remote target requires ALLOW_REMOTE_TARGET=true")
        timeout = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "5"))
        if timeout <= 0:
            raise ValueError("Timeout must be positive")
        return cls(url.rstrip("/"), timeout)
