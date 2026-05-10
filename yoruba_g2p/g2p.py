from __future__ import annotations

from dataclasses import dataclass

from yoruba_g2p.rules.digraphs import detect_atomic_tokens
from yoruba_g2p.rules.phonemes import token_to_phoneme
from yoruba_g2p.rules.syllables import segment_syllables
from yoruba_g2p.rules.tones import extract_tones
from yoruba_g2p.utils.normalize import normalize_nfc
from yoruba_g2p.utils.ssml import ipa_to_ssml


@dataclass
class G2PResult:
    input: str
    syllables: list[str]
    phonemes: list[str]
    tones: list[str]
    ipa: str
    confidence: float
    method: str
    ssml: str | None = None


class G2P:
    def __init__(self, backend: str = "rules") -> None:
        if backend not in {"rules", "hybrid", "neural"}:
            raise ValueError("backend must be one of: rules, hybrid, neural")
        self.backend = backend

    def convert(
        self,
        text: str,
        *,
        include_ssml: bool = False,
    ) -> G2PResult:
        normalized = normalize_nfc(text)
        tokens = detect_atomic_tokens(normalized)

        phonemes = [
            token_to_phoneme(token)
            for token in tokens
            if token_to_phoneme(token) is not None
        ]
        tones = extract_tones(tokens)
        syllables = segment_syllables(tokens)
        ipa = _join_ipa_tokens(phonemes)

        ssml = ipa_to_ssml(normalized, ipa) if include_ssml else None
        method = "rule_engine" if self.backend in {"rules", "hybrid"} else "neural_stub"

        return G2PResult(
            input=normalized,
            syllables=syllables,
            phonemes=phonemes,
            tones=tones,
            ipa=ipa,
            confidence=0.98 if method == "rule_engine" else 0.0,
            method=method,
            ssml=ssml,
        )


class Tokenizer:
    def tokenize(self, text: str) -> list[str]:
        return detect_atomic_tokens(normalize_nfc(text))


class ToneExtractor:
    def extract(self, text: str) -> list[str]:
        tokens = detect_atomic_tokens(normalize_nfc(text))
        return extract_tones(tokens)


def _join_ipa_tokens(phoneme_tokens: list[str]) -> str:
    out = []
    for token in phoneme_tokens:
        out.append(token.strip("/"))
    return "".join(out)
