from __future__ import annotations


def ipa_to_ssml(text: str, ipa: str) -> str:
    """Wrap IPA in an SSML phoneme tag for TTS providers."""
    return f'<speak><phoneme alphabet="ipa" ph="{ipa}">{text}</phoneme></speak>'
