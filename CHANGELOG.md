# Changelog

All notable changes to CrowtherNLP Yoruba Phonology Assistant are documented here.

## [Unreleased]

- No unreleased changes yet.

## [1.0.0] - 2026-05-10

### Milestones

- Canonical endpoint family introduced and active:
  - `POST /phonemize`
  - `POST /pronounce`
  - `POST /tone`
  - `POST /analyze`
- Legacy compatibility preserved with deprecation signaling:
  - headers (`Deprecation`, `Sunset`, `X-Crowther-*`)
  - payload field `migration_notice`
- Heuristic-first `POST /disambiguate` shipped with scaffold fallback and `stage` metadata.
- Benchmark harness includes baseline/rules/hybrid comparator output.
- OpenAPI parity checks, migration contract checks, and docs drift checks enforced in CI.

### Migration (v1 to v2)

Legacy endpoints remain available in `v1` migration window:

- `POST /g2p`
- `POST /tokenize`
- `GET /ipa`

Planned replacement mapping:

- `/g2p` -> `/phonemize` and/or `/pronounce`
- `/tokenize` -> `/analyze`
- `/ipa` -> `/pronounce`

Planned legacy removal target: `v2`.
