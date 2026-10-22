import pytest

from app.shortener import Shortener, ShortenerError, encode, is_valid_url


def test_encode_is_base62():
    assert encode(0) == "0"
    assert encode(61) == "Z"
    assert encode(62) == "10"


def test_shorten_and_resolve_round_trip():
    shortener = Shortener()
    code = shortener.shorten("https://example.com/page")
    assert shortener.resolve(code) == "https://example.com/page"


def test_same_url_gets_same_code():
    shortener = Shortener()
    assert shortener.shorten("https://a.com") == shortener.shorten("https://a.com")


def test_invalid_url_is_rejected():
    assert not is_valid_url("ftp://example.com")
    with pytest.raises(ShortenerError):
        Shortener().shorten("not a url")


def test_unknown_code_raises():
    with pytest.raises(KeyError):
        Shortener().resolve("nope")
