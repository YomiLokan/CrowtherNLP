from __future__ import annotations

import unicodedata


def normalize_nfc(text: str) -> str:
    """Normalize text to NFC for consistent downstream processing."""
    return unicodedata.normalize("NFC", text)


def normalize_nfd(text: str) -> str:
    """Normalize text to NFD for diacritic-level inspection."""
    return unicodedata.normalize("NFD", text)


def normalize_token_nfc(token: str) -> str:
    """Normalize a token to NFC and lowercase for canonical comparisons."""
    return unicodedata.normalize("NFC", token).lower()
