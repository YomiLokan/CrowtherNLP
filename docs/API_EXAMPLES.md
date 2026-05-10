# API Examples

This document mirrors the currently implemented API surface in the repository.

Base URL for local development:

```text
http://127.0.0.1:8000
```

## Health check

Request:

```bash
curl http://127.0.0.1:8000/health
```

Response:

```json
{
  "status": "ok"
}
```

## POST /g2p

Request:

```bash
curl -X POST http://127.0.0.1:8000/g2p \
  -H "Content-Type: application/json" \
  -d '{
    "text": "ìgbà",
    "output_format": "json",
    "include_ipa": true,
    "include_ssml": true
  }'
```

Response:

```json
{
  "input": "ìgbà",
  "syllables": ["ì", "gbà"],
  "phonemes": ["/i/", "/͡gb/", "/a/"],
  "tones": ["L", "L"],
  "ipa": "i͡gba",
  "confidence": 0.98,
  "method": "rule_engine",
  "ssml": "<speak><phoneme alphabet=\"ipa\" ph=\"i͡gba\">ìgbà</phoneme></speak>",
  "migration_notice": {
    "deprecated": true,
    "migration_phase": "v1",
    "removal_target": "v2",
    "replacement_endpoints": ["/phonemize", "/pronounce"],
    "docs": "https://github.com/CrowtherNLP/yoruba-phonology-assistant/blob/main/docs/API_EXAMPLES.md"
  }
}
```

## POST /tokenize

Request:

```bash
curl -X POST http://127.0.0.1:8000/tokenize \
  -H "Content-Type: application/json" \
  -d '{"text":"Ẹ káàbọ̀"}'
```

Response:

```json
{
  "tokens": ["Ẹ", " ", "k", "á", "à", "b", "ọ̀"],
  "digraph_units": [],
  "special_chars": ["Ẹ", "ọ̀"],
  "migration_notice": {
    "deprecated": true,
    "migration_phase": "v1",
    "removal_target": "v2",
    "replacement_endpoints": ["/analyze"],
    "docs": "https://github.com/CrowtherNLP/yoruba-phonology-assistant/blob/main/docs/API_EXAMPLES.md"
  }
}
```

## GET /ipa

Request:

```bash
curl "http://127.0.0.1:8000/ipa?word=gbogbo"
```

Response:

```json
{
  "word": "gbogbo",
  "ipa": "͡gbo͡gbo",
  "tones": ["M", "M"],
  "migration_notice": {
    "deprecated": true,
    "migration_phase": "v1",
    "removal_target": "v2",
    "replacement_endpoints": ["/pronounce"],
    "docs": "https://github.com/CrowtherNLP/yoruba-phonology-assistant/blob/main/docs/API_EXAMPLES.md"
  }
}
```

## POST /disambiguate

Request:

```bash
curl -X POST http://127.0.0.1:8000/disambiguate \
  -H "Content-Type: application/json" \
  -d '{
    "word": "igba",
    "context": "Mo ra igba lọ sọja",
    "candidates": [
      {"form": "igba", "tones": "MM", "meaning": "200"},
      {"form": "igbá", "tones": "MH", "meaning": "calabash"},
      {"form": "ìgbà", "tones": "LL", "meaning": "time"}
    ]
  }'
```

Response (heuristic v1.1 pass):

```json
{
  "selected": {"form": "igba", "tones": "MM", "meaning": "200"},
  "confidence": 0.95,
  "method": "heuristic_context_v1",
  "status": "experimental_v1_1_heuristic",
  "stage": "heuristic"
}
```

## Notes

- Current API scope is rule-engine-backed Standard Yoruba only.
- `POST /disambiguate` is heuristic-first and falls back to scaffold behavior when context cues are insufficient.
- Canonical endpoint family is now available: `/phonemize`, `/pronounce`, `/tone`, `/analyze`.
- Legacy endpoints (`/g2p`, `/tokenize`, `/ipa`) remain available during transition.
- The committed OpenAPI specification is stored at the repository root in `openapi.yaml`.

## Legacy Migration Timeline

- Current phase: `v1` migration window
- Legacy removal target: `v2`

Legacy endpoint replacements:

- `/g2p` -> `/phonemize` and/or `/pronounce`
- `/tokenize` -> `/analyze`
- `/ipa` -> `/pronounce`

Legacy responses include deprecation headers:

- `Deprecation: true`
- `Sunset: v2`
- `X-Crowther-Replacement: <canonical-endpoint(s)>`
- `X-Crowther-Migration-Phase: v1`

Legacy responses also include `migration_notice` in the JSON body for clients that do not consume headers.

## POST /phonemize

Request:

```bash
curl -X POST http://127.0.0.1:8000/phonemize \
  -H "Content-Type: application/json" \
  -d '{"text":"ìgbà"}'
```

## POST /pronounce

Request:

```bash
curl -X POST http://127.0.0.1:8000/pronounce \
  -H "Content-Type: application/json" \
  -d '{"text":"Ẹ káàbọ̀","include_ssml":true}'
```

## POST /tone

Request:

```bash
curl -X POST http://127.0.0.1:8000/tone \
  -H "Content-Type: application/json" \
  -d '{"text":"bá bà ba"}'
```

## POST /analyze

Request:

```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"Ẹ káàbọ̀","include_ssml":true}'
```
