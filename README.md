# Yoruba Phonology Assistant

Yoruba Phonology Assistant is a Yoruba-native grapheme-to-phoneme (G2P) system built to prevent English phonetic fallback when processing Yoruba text.

The current repository ships a deterministic Standard Yoruba core with:

- atomic handling of `gb` and `kp`
- single-token nasal vowels: `an`, `en`, `in`, `ọn`, `un`
- Yoruba tone extraction with `H`, `M`, and `L`
- canonical FastAPI endpoints for `/phonemize`, `/pronounce`, `/tone`, and `/analyze`
- legacy compatibility endpoints for `/g2p`, `/tokenize`, and `/ipa` with migration metadata
- heuristic-first `/disambiguate` with scaffold fallback
- a benchmark harness with baseline, rules, and hybrid comparison rows

## What problem this solves

Many general-purpose systems treat Yoruba as if it were phonetically close to English. That causes predictable failures:

- splitting `gb` into `g` + `b`
- flattening tone distinctions such as `bá`, `ba`, and `bà`
- collapsing `ẹ` into `e`, `ọ` into `o`, and `ṣ` into `s` or `sh`
- treating nasal vowels as separate vowel-plus-consonant sequences instead of atomic phonological units in this project model

This repository is designed to stop those failures upstream.

## Before and after

Examples of distinctions the project preserves:

| Input | Correct Yoruba-native interpretation | Common fallback error |
|-------|--------------------------------------|------------------------|
| `gbogbo` | `gb` remains one phoneme | `g` + `b` split |
| `bá` / `ba` / `bà` | High / Mid / Low tone remain distinct | tones flattened |
| `ẹ̀kọ́` | `ẹ` and `ọ` stay Yoruba vowels | mapped to plain `e` and `o` |
| `tan` | nasal vowel token handled as one unit in this project | vowel + trailing `n` treated separately |

## Current status

- Scope: Standard Yoruba only
- Core priority: Yoruba-native phonology before LLM integration
- Rule engine: implemented
- Canonical API (`/phonemize`, `/pronounce`, `/tone`, `/analyze`): implemented
- Legacy compatibility layer (`/g2p`, `/tokenize`, `/ipa`): implemented with deprecation headers and payload migration notice
- Disambiguation endpoint (`/disambiguate`): implemented (heuristic-first v1.1 scaffold)
- Benchmark comparator: implemented
- Neural fallback: planned

## Quick start

Install the project in editable mode:

```bash
/usr/bin/python3 -m pip install -e .
/usr/bin/python3 -m pip install fastapi uvicorn httpx pytest
```

Basic Python usage:

```python
from yoruba_g2p import G2P

g2p = G2P(backend="rules")
result = g2p.convert("ìgbà", include_ssml=True)

print(result.phonemes)
print(result.tones)
print(result.ipa)
print(result.ssml)
```

Example output:

```text
['/i/', '/͡gb/', '/a/']
['L', 'L']
i͡gba
<speak><phoneme alphabet="ipa" ph="i͡gba">ìgbà</phoneme></speak>
```

## Local API

Start the API locally:

```bash
/usr/bin/python3 -m api.server
```

Interactive docs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Contract and examples in the repository:

- OpenAPI spec: `openapi.yaml`
- Example requests and responses: `docs/API_EXAMPLES.md`
- Local run instructions: `Localrun.md`

## API examples

Canonical pronunciation analysis:

```bash
curl -X POST http://127.0.0.1:8000/pronounce \
	-H "Content-Type: application/json" \
	-d '{"text":"ìgbà","include_ssml":true}'
```

Canonical integrated analysis:

```bash
curl -X POST http://127.0.0.1:8000/analyze \
	-H "Content-Type: application/json" \
	-d '{"text":"Ẹ káàbọ̀","include_ssml":true}'
```

Legacy compatibility (during v1 migration window):

```bash
curl -X POST http://127.0.0.1:8000/g2p \
	-H "Content-Type: application/json" \
	-d '{"text":"ìgbà","include_ipa":true,"include_ssml":true}'
```

## Benchmarks

The repository includes a comparator harness that reports baseline, rules, and hybrid rows in publishing-plan format.

Run it with:

```bash
/usr/bin/python3 benchmarks/evaluate.py \
	--gold benchmarks/data/gold_words.jsonl \
	--models baseline,rules,hybrid \
	--json-out benchmarks/results/latest.json
```

Current benchmark summary on the committed 31-sample Standard Yoruba gold set:

| Model | Phoneme Error Rate (PER) | Tone Accuracy | Word Exact Match |
|-------|--------------------------|---------------|------------------|
| baseline | 0.6667 | 0.4167 | 0.0323 |
| rules | 0.0000 | 1.0000 | 1.0000 |
| hybrid | 0.0000 | 1.0000 | 1.0000 |

Current implementation note:

- `hybrid` is presently an alias of `rules` until neural fallback is added.

## Repository layout

```text
yoruba-phonology-assistant/
├── api/
├── benchmarks/
├── docs/
├── tests/
├── yoruba_g2p/
├── CONTRIBUTING.md
├── LICENSE
├── Localrun.md
├── README.md
└── openapi.yaml
```

## Planned public endpoints and registries

These namespaces are reserved in the project plan and can be used once publishing goes live:

- GitHub: `https://github.com/CrowtherNLP/yoruba-phonology-assistant`
- Hugging Face model: `https://huggingface.co/CrowtherNLP/yoruba-g2p`
- Hugging Face dataset: `https://huggingface.co/datasets/CrowtherNLP/yoruba-phoneme-dataset`

Current free API state:

- Local development API is available now through the FastAPI server in this repository.
- Public hosted API URL is planned but not yet published.

## Contributing

Contribution guidelines are documented in `CONTRIBUTING.md`.

Please preserve the project decisions already made:

- Standard Yoruba only for v1.x
- atomic phoneme representation
- nasal vowels as single phoneme tokens
- phonology-first development before LLM integration work

## Citation

If you use this repository in research or downstream tooling, cite it as:

```bibtex
@software{crowthernlp_yoruba_phonology_assistant_2026,
	author = {CrowtherNLP},
	title = {Yoruba Phonology Assistant},
	year = {2026},
	url = {https://github.com/CrowtherNLP/yoruba-phonology-assistant}
}
```
