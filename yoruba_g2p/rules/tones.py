from __future__ import annotations

from yoruba_g2p.rules.phonemes import is_vowel_token, tone_of_token


def extract_tones(tokens: list[str]) -> list[str]:
    tones: list[str] = []
    for token in tokens:
        if is_vowel_token(token):
            tones.append(tone_of_token(token))
            continue

        # Nasal vowels are represented as <vowel+n>; tone is carried on the vowel.
        if len(token) >= 2 and token[-1].lower() == "n":
            vowel_part = token[:-1]
            if is_vowel_token(vowel_part):
                tones.append(tone_of_token(vowel_part))

    return tones
