from __future__ import annotations

import unicodedata

from yoruba_g2p.rules.phonemes import canonical_token, is_vowel_token

WORD_BOUNDARY_CHARS = set(" \t\n\r.,!?;:()[]{}\"'/-")
DIGRAPHS = {("g", "b"): "gb", ("k", "p"): "kp"}
NASAL_VOWELS = {"an", "en", "in", "ọn", "un"}


def split_graphemes(text: str) -> list[str]:
    graphemes: list[str] = []
    current = ""
    for ch in unicodedata.normalize("NFD", text):
        if unicodedata.combining(ch) and current:
            current += ch
            continue
        if current:
            graphemes.append(unicodedata.normalize("NFC", current))
        current = ch
    if current:
        graphemes.append(unicodedata.normalize("NFC", current))
    return graphemes


def _is_boundary(token: str) -> bool:
    return token in WORD_BOUNDARY_CHARS


def _base_letter(token: str) -> str:
    canonical = canonical_token(token)
    return canonical[0] if canonical else ""


def detect_atomic_tokens(text: str) -> list[str]:
    graphemes = split_graphemes(text)
    out: list[str] = []
    i = 0

    while i < len(graphemes):
        cur = graphemes[i]

        if _is_boundary(cur):
            out.append(cur)
            i += 1
            continue

        if i + 1 < len(graphemes):
            nxt = graphemes[i + 1]
            if not _is_boundary(nxt):
                pair = (_base_letter(cur), _base_letter(nxt))
                digraph = DIGRAPHS.get(pair)
                if digraph:
                    out.append(digraph)
                    i += 2
                    continue

        if i + 1 < len(graphemes):
            nxt = graphemes[i + 1]
            if not _is_boundary(nxt) and is_vowel_token(cur):
                candidate = canonical_token(cur) + canonical_token(nxt)
                if candidate in NASAL_VOWELS and _base_letter(nxt) == "n":
                    out.append(cur + nxt)
                    i += 2
                    continue

        out.append(cur)
        i += 1

    return out
