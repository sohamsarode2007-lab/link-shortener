"""In-memory URL shortener: turns long URLs into short base62 codes and back."""
import string
from urllib.parse import urlparse

ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase


class ShortenerError(ValueError):
    """Raised when a URL can't be shortened."""


def encode(number: int) -> str:
    """Encode a non-negative integer in base62 (0-9, a-z, A-Z)."""
    if number < 0:
        raise ShortenerError("number must be non-negative")
    if number == 0:
        return ALPHABET[0]
    digits = []
    while number:
        number, remainder = divmod(number, len(ALPHABET))
        digits.append(ALPHABET[remainder])
    return "".join(reversed(digits))


def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


class Shortener:
    def __init__(self, start: int = 1000) -> None:
        self._next_id = start
        self._url_by_code: dict[str, str] = {}
        self._code_by_url: dict[str, str] = {}

    def shorten(self, url: str) -> str:
        if not is_valid_url(url):
            raise ShortenerError(f"not a valid http(s) URL: {url}")
        if url in self._code_by_url:
            return self._code_by_url[url]
        code = encode(self._next_id)
        self._next_id += 1
        self._url_by_code[code] = url
        self._code_by_url[url] = code
        return code

    def resolve(self, code: str) -> str:
        if code not in self._url_by_code:
            raise KeyError(code)
        return self._url_by_code[code]
