from __future__ import annotations

from yoruba_g2p.rules.phonemes import is_vowel_token


def segment_syllables(tokens: list[str]) -> list[str]:
    syllables: list[str] = []
    pending: list[str] = []

    for token in tokens:
        if token.isspace():
            if pending:
                syllables.append("".join(pending))
                pending = []
            continue

        pending.append(token)
        if _is_syllabic_nasal(token) or _is_vowel_or_nasal_vowel(token):
            syllables.append("".join(pending))
            pending = []

    if pending:
        syllables.append("".join(pending))

    return syllables


def _is_vowel_or_nasal_vowel(token: str) -> bool:
    if is_vowel_token(token):
        return True
    if len(token) >= 2 and token[-1].lower() == "n":
        return is_vowel_token(token[:-1])
    return False


def _is_syllabic_nasal(token: str) -> bool:
    return token.lower() in {"m", "n"}
