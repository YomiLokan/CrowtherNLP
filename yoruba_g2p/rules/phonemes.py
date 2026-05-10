from __future__ import annotations

import unicodedata

TONE_MARKS = {"\u0300", "\u0301"}  # grave, acute

VOWEL_IPA = {
    "a": "/a/",
    "e": "/e/",
    "ẹ": "/ɛ/",
    "i": "/i/",
    "o": "/o/",
    "ọ": "/ɔ/",
    "u": "/u/",
}

NASAL_VOWEL_IPA = {
    "an": "/ã/",
    "en": "/ɛ̃/",
    "in": "/ĩ/",
    "ọn": "/ɔ̃/",
    "un": "/ũ/",
}

CONSONANT_IPA = {
    "b": "/b/",
    "d": "/d/",
    "f": "/f/",
    "g": "/g/",
    "gb": "/͡gb/",
    "h": "/h/",
    "j": "/dʒ/",
    "k": "/k/",
    "kp": "/͡kp/",
    "l": "/l/",
    "m": "/m/",
    "n": "/n/",
    "p": "/kp/",
    "r": "/r/",
    "s": "/s/",
    "ṣ": "/ʃ/",
    "t": "/t/",
    "w": "/w/",
    "y": "/j/",
}


def _strip_tones_keep_dot_below(text: str) -> str:
    nfd = unicodedata.normalize("NFD", text)
    kept = "".join(ch for ch in nfd if ch not in TONE_MARKS)
    return unicodedata.normalize("NFC", kept)


def canonical_token(token: str) -> str:
    return _strip_tones_keep_dot_below(token).lower()


def is_vowel_token(token: str) -> bool:
    return canonical_token(token) in VOWEL_IPA


def tone_of_token(token: str) -> str:
    nfd = unicodedata.normalize("NFD", token)
    if "\u0301" in nfd:
        return "H"
    if "\u0300" in nfd:
        return "L"
    return "M"


def token_to_phoneme(token: str) -> str | None:
    canonical = canonical_token(token)
    if canonical in NASAL_VOWEL_IPA:
        return NASAL_VOWEL_IPA[canonical]
    if canonical in VOWEL_IPA:
        return VOWEL_IPA[canonical]
    if canonical in CONSONANT_IPA:
        return CONSONANT_IPA[canonical]
    return None
