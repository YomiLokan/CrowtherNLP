from __future__ import annotations

import re
import unicodedata
from typing import Literal, Optional

from fastapi import FastAPI, Query, Response
from pydantic import BaseModel, Field

from yoruba_g2p import G2P, Tokenizer
from yoruba_g2p.rules.phonemes import canonical_token


app = FastAPI(
    title="Yoruba Phonology Assistant API",
    version="0.1.0",
    summary="Deterministic Yoruba-native G2P API",
)

_g2p = G2P(backend="rules")
_tokenizer = Tokenizer()

LEGACY_DEPRECATION_PHASE = "v1"
LEGACY_REMOVAL_TARGET = "v2"
LEGACY_DOC_URL = "https://github.com/CrowtherNLP/yoruba-phonology-assistant/blob/main/docs/API_EXAMPLES.md"


def _set_legacy_headers(response: Response, replacement: str) -> None:
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = LEGACY_REMOVAL_TARGET
    response.headers["Link"] = f'<{LEGACY_DOC_URL}>; rel="deprecation"'
    response.headers["X-Crowther-Replacement"] = replacement
    response.headers["X-Crowther-Migration-Phase"] = LEGACY_DEPRECATION_PHASE
    response.headers["X-Crowther-Removal-Target"] = LEGACY_REMOVAL_TARGET


def _legacy_notice(replacement: str) -> dict[str, object]:
    replacement_endpoints = [r.strip() for r in replacement.split(",") if r.strip()]
    return {
        "deprecated": True,
        "migration_phase": LEGACY_DEPRECATION_PHASE,
        "removal_target": LEGACY_REMOVAL_TARGET,
        "replacement_endpoints": replacement_endpoints,
        "docs": LEGACY_DOC_URL,
    }


class G2PRequest(BaseModel):
    text: str = Field(min_length=1)
    output_format: Literal["json"] = "json"
    include_ipa: bool = True
    include_ssml: bool = False


class G2PResponse(BaseModel):
    input: str
    syllables: list[str]
    phonemes: list[str]
    tones: list[str]
    ipa: Optional[str]
    confidence: float
    method: str
    ssml: Optional[str] = None
    migration_notice: Optional[dict[str, object]] = None


class TokenizeRequest(BaseModel):
    text: str = Field(min_length=1)


class TokenizeResponse(BaseModel):
    tokens: list[str]
    digraph_units: list[str]
    special_chars: list[str]
    migration_notice: Optional[dict[str, object]] = None


class IPAResponse(BaseModel):
    word: str
    ipa: str
    tones: list[str]
    migration_notice: Optional[dict[str, object]] = None


class DisambiguationCandidate(BaseModel):
    form: str = Field(min_length=1)
    tones: str = Field(min_length=1)
    meaning: str = Field(min_length=1)


class DisambiguateRequest(BaseModel):
    word: str = Field(min_length=1)
    context: str = Field(min_length=1)
    candidates: list[DisambiguationCandidate] = Field(min_length=1)


class DisambiguateResponse(BaseModel):
    selected: DisambiguationCandidate
    confidence: float
    method: str
    status: str
    stage: Literal["scaffold", "heuristic"]


class PhonemizeRequest(BaseModel):
    text: str = Field(min_length=1)


class PhonemizeResponse(BaseModel):
    input: str
    phonemes: list[str]
    syllables: list[str]
    confidence: float
    method: str


class PronounceRequest(BaseModel):
    text: str = Field(min_length=1)
    include_ssml: bool = False


class PronounceResponse(BaseModel):
    input: str
    phonemes: list[str]
    tones: list[str]
    ipa: str
    ssml: Optional[str] = None
    confidence: float
    method: str


class ToneRequest(BaseModel):
    text: str = Field(min_length=1)


class ToneResponse(BaseModel):
    input: str
    tones: list[str]
    tone_units: list[str]
    confidence: float
    method: str


class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=1)
    include_ssml: bool = False


class AnalyzeResponse(BaseModel):
    input: str
    tokens: list[str]
    digraph_units: list[str]
    special_chars: list[str]
    syllables: list[str]
    phonemes: list[str]
    tones: list[str]
    ipa: str
    ssml: Optional[str] = None
    confidence: float
    method: str


FORM_CUE_HINTS: dict[str, set[str]] = {
    # Numeric sense cues for igba (200) in commerce/count contexts.
    "igba": {"ra", "soja", "sọja", "owo", "naira", "egberun", "nomba", "number"},
    # Object sense cues for igbá (calabash).
    "igbá": {"omi", "mu", "agbọn", "gourd", "koko"},
    # Temporal sense cues for ìgbà (time/era).
    "ìgbà": {"akoko", "àkókò", "nigba", "nigbà", "asiko", "asikò", "igba"},
}


def _tokenize_context(text: str) -> set[str]:
    parts = re.findall(r"[0-9A-Za-zÀ-ÖØ-öø-ÿẸỌṢẹọṣ]+", text)
    return {canonical_token(part) for part in parts if part}


def _meaning_tokens(meaning: str) -> set[str]:
    parts = re.findall(r"[0-9A-Za-zÀ-ÖØ-öø-ÿẸỌṢẹọṣ]+", meaning)
    return {canonical_token(part) for part in parts if part}


def _candidate_score(candidate: DisambiguationCandidate, context_tokens: set[str], context_raw: str) -> int:
    score = 0
    cand_form_norm = canonical_token(candidate.form)

    if candidate.form.lower() in context_raw.lower() or cand_form_norm in context_tokens:
        score += 2

    for token in _meaning_tokens(candidate.meaning):
        if token in context_tokens:
            score += 2

    cue_tokens = FORM_CUE_HINTS.get(cand_form_norm, set())
    for cue in cue_tokens:
        if canonical_token(cue) in context_tokens:
            score += 3

    return score


def _normalized_form(text: str) -> str:
    return unicodedata.normalize("NFC", text).casefold()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/phonemize", response_model=PhonemizeResponse)
def phonemize(request: PhonemizeRequest) -> PhonemizeResponse:
    result = _g2p.convert(request.text)
    return PhonemizeResponse(
        input=result.input,
        phonemes=result.phonemes,
        syllables=result.syllables,
        confidence=result.confidence,
        method=result.method,
    )


@app.post("/pronounce", response_model=PronounceResponse)
def pronounce(request: PronounceRequest) -> PronounceResponse:
    result = _g2p.convert(request.text, include_ssml=request.include_ssml)
    return PronounceResponse(
        input=result.input,
        phonemes=result.phonemes,
        tones=result.tones,
        ipa=result.ipa,
        ssml=result.ssml,
        confidence=result.confidence,
        method=result.method,
    )


@app.post("/tone", response_model=ToneResponse)
def tone(request: ToneRequest) -> ToneResponse:
    result = _g2p.convert(request.text)
    return ToneResponse(
        input=result.input,
        tones=result.tones,
        tone_units=result.syllables,
        confidence=result.confidence,
        method=result.method,
    )


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    result = _g2p.convert(request.text, include_ssml=request.include_ssml)
    tokens = _tokenizer.tokenize(request.text)
    digraph_units = [token for token in tokens if token in {"gb", "kp"}]
    special_chars = [
        token
        for token in tokens
        if canonical_token(token) in {"ẹ", "ọ", "ṣ"}
    ]
    return AnalyzeResponse(
        input=result.input,
        tokens=tokens,
        digraph_units=digraph_units,
        special_chars=special_chars,
        syllables=result.syllables,
        phonemes=result.phonemes,
        tones=result.tones,
        ipa=result.ipa,
        ssml=result.ssml,
        confidence=result.confidence,
        method=result.method,
    )


@app.post(
    "/g2p",
    response_model=G2PResponse,
    deprecated=True,
    summary="Legacy: use /phonemize or /pronounce",
)
def g2p(request: G2PRequest, response: Response) -> G2PResponse:
    replacement = "/phonemize,/pronounce"
    _set_legacy_headers(response, replacement=replacement)
    result = _g2p.convert(request.text, include_ssml=request.include_ssml)
    return G2PResponse(
        input=result.input,
        syllables=result.syllables,
        phonemes=result.phonemes,
        tones=result.tones,
        ipa=result.ipa if request.include_ipa else None,
        confidence=result.confidence,
        method=result.method,
        ssml=result.ssml,
        migration_notice=_legacy_notice(replacement),
    )


@app.post(
    "/tokenize",
    response_model=TokenizeResponse,
    deprecated=True,
    summary="Legacy: use /analyze",
)
def tokenize(request: TokenizeRequest, response: Response) -> TokenizeResponse:
    replacement = "/analyze"
    _set_legacy_headers(response, replacement=replacement)
    tokens = _tokenizer.tokenize(request.text)
    digraph_units = [token for token in tokens if token in {"gb", "kp"}]
    special_chars = [
        token
        for token in tokens
        if canonical_token(token) in {"ẹ", "ọ", "ṣ"}
    ]
    return TokenizeResponse(
        tokens=tokens,
        digraph_units=digraph_units,
        special_chars=special_chars,
        migration_notice=_legacy_notice(replacement),
    )


@app.get(
    "/ipa",
    response_model=IPAResponse,
    deprecated=True,
    summary="Legacy: use /pronounce",
)
def ipa(response: Response, word: str = Query(min_length=1)) -> IPAResponse:
    replacement = "/pronounce"
    _set_legacy_headers(response, replacement=replacement)
    result = _g2p.convert(word)
    return IPAResponse(
        word=word,
        ipa=result.ipa,
        tones=result.tones,
        migration_notice=_legacy_notice(replacement),
    )


@app.post("/disambiguate", response_model=DisambiguateResponse)
def disambiguate(request: DisambiguateRequest) -> DisambiguateResponse:
    # v1.1: heuristic-first disambiguation with deterministic scaffold fallback.
    context_tokens = _tokenize_context(request.context)
    target_form_exact = _normalized_form(request.word)

    selected = request.candidates[0]
    best_score = -1
    selected_is_exact = _normalized_form(selected.form) == target_form_exact

    for candidate in request.candidates:
        candidate_score = _candidate_score(candidate, context_tokens, request.context)
        candidate_is_exact = _normalized_form(candidate.form) == target_form_exact

        if candidate_score > best_score:
            best_score = candidate_score
            selected = candidate
            selected_is_exact = candidate_is_exact
            continue

        if candidate_score == best_score and candidate_is_exact and not selected_is_exact:
            selected = candidate
            selected_is_exact = True

    if best_score <= 0:
        for candidate in request.candidates:
            if _normalized_form(candidate.form) == target_form_exact:
                selected = candidate
                selected_is_exact = True
                break

        return DisambiguateResponse(
            selected=selected,
            confidence=0.0,
            method="placeholder_disambiguation",
            status="not_final_v1_1_scaffold",
            stage="scaffold",
        )

    confidence = min(0.95, 0.45 + (0.1 * float(best_score)))

    return DisambiguateResponse(
        selected=selected,
        confidence=confidence,
        method="heuristic_context_v1",
        status="experimental_v1_1_heuristic",
        stage="heuristic",
    )


def run() -> None:
    import uvicorn

    uvicorn.run("api.server:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    run()
