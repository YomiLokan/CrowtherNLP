# Contributing

Thanks for contributing to Yoruba Phonology Assistant.

## Scope

This repository currently prioritizes:

- Standard Yoruba only
- Yoruba-native phonology before LLM integration
- Deterministic correctness for digraphs, tone, dotted vowels, and nasal-vowel tokens

Please keep new work aligned with those constraints unless there is an explicit roadmap decision to expand them.

## Development setup

```bash
/usr/bin/python3 -m pip install -e .
/usr/bin/python3 -m pip install fastapi uvicorn httpx pytest build PyYAML
```

## Before opening a pull request

Run these checks locally:

```bash
/usr/bin/python3 -m pytest -q
/usr/bin/python3 benchmarks/evaluate.py --gold benchmarks/data/gold_words.jsonl --models baseline,rules,hybrid --json-out benchmarks/results/latest.json
/usr/bin/python3 scripts/check_openapi.py
/usr/bin/python3 -m build
```

## Contribution guidelines

- Preserve atomic handling for `gb` and `kp`
- Preserve single-token handling for nasal vowels: `an`, `en`, `in`, `ọn`, `un`
- Do not introduce English phonetic approximations for Yoruba-specific characters
- Keep benchmark additions within Standard Yoruba unless the roadmap changes
- Add or update tests when behavior changes
- Keep OpenAPI and example docs aligned with implemented endpoints
- Regenerate `openapi.yaml` with `scripts/export_openapi.py` when the API contract changes

## Pull request checklist

- Tests pass
- Benchmarks still run
- Documentation is updated if behavior changed
- API contract is updated if endpoint behavior changed

## Reporting issues

When filing a bug, include:

- input word or phrase
- expected phonemes or tones
- actual output
- whether the issue involves digraphs, tone marks, dotted vowels, or nasal vowels

## Roadmap note

`POST /disambiguate` is planned for v1.1. If you want to work on that area, coordinate around the agreed project scope first.
