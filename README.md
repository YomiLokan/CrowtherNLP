# CrowtherNLP Yoruba Phonology Infrastructure

CrowtherNLP is an AI-native Yoruba phonology infrastructure project.

This repository provides a deterministic, tone-aware Standard Yoruba pronunciation foundation that AI systems can call directly instead of inferring Yoruba pronunciation from English spelling patterns.

## Mission

Build a standardized Yoruba phonology and pronunciation infrastructure layer for:

- NLP systems
- LLM tools and agents
- TTS and speech systems
- pronunciation-sensitive developer applications

The project is named in honor of Bishop Samuel Ajayi Crowther.

## Foundational Principle

Pronunciation infrastructure comes before advanced AI integration.

```text
Yoruba Text
  -> CrowtherNLP Phonology Engine
  -> Tone + Phoneme Representation
  -> AI / LLM / TTS / Speech Systems
```

## Current Scope

- Dialect scope: Standard Yoruba only
- Core engine: deterministic rule engine
- Priority: Yoruba-native phonology correctness before model-first integration

## What Is Implemented

- Atomic handling of Yoruba units including `gb`, `kp`, `ṣ`, `ẹ`, `ọ`
- Single-token nasal vowel representation (`an`, `en`, `in`, `ọn`, `un`)
- Tone extraction with `H`, `M`, `L`
- Canonical API endpoints:
  - `POST /phonemize`
  - `POST /pronounce`
  - `POST /tone`
  - `POST /analyze`
- Legacy compatibility endpoints with migration metadata:
  - `POST /g2p`
  - `POST /tokenize`
  - `GET /ipa`
- `POST /disambiguate` (heuristic-first v1.1 scaffold)
- OpenAPI parity checks, runtime migration contract checks, and docs contract checks in CI
- Benchmark harness with baseline/rules/hybrid comparison

## Why This Exists

Many systems mis-handle Yoruba by:

- splitting atomic phonemes (for example `gb` into `g` + `b`)
- flattening tonal distinctions (`bá`, `ba`, `bà`)
- collapsing distinct vowels and consonants (`ẹ`, `ọ`, `ṣ`) into non-Yoruba approximations

CrowtherNLP prevents these errors at the infrastructure layer.

## Canonical API

### POST /phonemize
Converts Yoruba orthography into phoneme tokens and syllable structure.

### POST /pronounce
Returns pronunciation-focused output, including IPA and optional SSML.

### POST /tone
Returns tone sequence and tone-bearing units.

### POST /analyze
Returns unified phonology analysis (tokens, phonemes, tones, IPA, diagnostics).

## Migration Window

Legacy endpoints remain available during the v1 migration window and include:

- deprecation headers
- `migration_notice` payload guidance with replacement endpoints

Replacement mapping:

- `/g2p` -> `/phonemize` and/or `/pronounce`
- `/tokenize` -> `/analyze`
- `/ipa` -> `/pronounce`

Planned legacy removal target: v2.

## Quick Start

Install dependencies:

```bash
/usr/bin/python3 -m pip install -e .
/usr/bin/python3 -m pip install fastapi uvicorn httpx pytest PyYAML
```

Run tests:

```bash
/usr/bin/python3 -m pytest -q
```

Run API locally:

```bash
/usr/bin/python3 -m api.server
```

Note: if copying manually, remove the space after `/` in the command above.

## Minimal Python Usage

```python
from yoruba_g2p import G2P

engine = G2P(backend="rules")
result = engine.convert("ìgbà", include_ssml=True)

print(result.phonemes)
print(result.tones)
print(result.ipa)
print(result.ssml)
```

## Local API Docs

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Benchmarks

Run evaluator:

```bash
/usr/bin/python3 benchmarks/evaluate.py \
  --gold benchmarks/data/gold_words.jsonl \
  --models baseline,rules,hybrid \
  --json-out benchmarks/results/latest.json
```

Current benchmark summary (31-sample Standard Yoruba gold set):

| Model | PER | Tone Accuracy | Word Exact Match |
|------|-----|---------------|------------------|
| baseline | 0.6667 | 0.4167 | 0.0323 |
| rules | 0.0000 | 1.0000 | 1.0000 |
| hybrid | 0.0000 | 1.0000 | 1.0000 |

`hybrid` is currently an alias of `rules` until neural fallback is introduced.

## Repository References

- API examples: docs/API_EXAMPLES.md
- Integration direction: docs/INTEGRATION_PLAN.md
- Project direction: docs/PROJECT_PLAN.md
- Publishing path: docs/PUBLISHING_PLAN.md
- OpenAPI contract: openapi.yaml
- Local run guide: Localrun.md

## Contributing

See CONTRIBUTING.md.

Please preserve these project constraints:

- Standard Yoruba only for v1.x
- atomic phoneme representation
- tone as first-class computational data
- phonology infrastructure first, advanced AI integration second

## License

Apache 2.0 (see LICENSE).

## Citation

```bibtex
@software{crowthernlp_yoruba_phonology_infrastructure_2026,
  author = {CrowtherNLP},
  title = {CrowtherNLP Yoruba Phonology Infrastructure},
  year = {2026},
  url = {https://github.com/YomiLokan/CrowtherNLP}
}
```
