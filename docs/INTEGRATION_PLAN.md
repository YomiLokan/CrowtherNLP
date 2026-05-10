# CrowtherNLP — Integration Plan

> **Status:** Active — Direction Reset v1  
> **Created:** 2026-05-10  
> **Last Updated:** 2026-05-10  
> **Organisation:** CrowtherNLP

---

## Integration Objective

Define a stable phonology infrastructure layer that other AI systems can call instead of guessing Yoruba pronunciation from English spelling patterns.

Integration order is strict:

1. phonology engine correctness
2. phoneme/tone representation contracts
3. API and package interfaces
4. advanced AI integration

---

## Canonical Architecture

```
Yoruba Text
  → CrowtherNLP Phonology Engine
  → Tone + Phoneme Representation
  → AI / LLM / TTS / Speech / NLP Systems
```

---

## Current Implementation Snapshot

Already live in repository:

- deterministic phonology engine (Standard Yoruba)
- API endpoints: `/g2p`, `/tokenize`, `/ipa`, `/disambiguate`
- OpenAPI contract with parity checks
- benchmark harness with baseline/rules/hybrid comparisons

Steering decision: retain compatibility for existing endpoints while introducing canonical CrowtherNLP endpoint names for external adopters.

---

## Canonical MVP API Surface

### `POST /phonemize`

Purpose: convert Yoruba orthography into phoneme token sequence.

Primary output:

- normalized input
- phoneme tokens
- syllable segmentation
- method + confidence metadata

### `POST /pronounce`

Purpose: return pronunciation-focused output.

Primary output:

- IPA representation
- SSML-ready pronunciation payload
- phoneme + tone alignment

### `POST /tone`

Purpose: extract and structure tone information.

Primary output:

- tone sequence (`H`, `M`, `L`)
- tone-bearing units
- structural metadata

### `POST /analyze`

Purpose: unified phonology analysis endpoint.

Primary output:

- phonemes
- IPA
- tones
- tokenization artifacts
- diagnostics flags

---

## Endpoint Transition Plan (Compatibility)

Until canonical endpoints are fully rolled out:

- `/g2p` maps to `/phonemize` + `/pronounce` behavior
- `/tokenize` contributes to `/analyze`
- `/ipa` contributes to `/pronounce`
- `/disambiguate` remains v1.1+ capability (currently heuristic scaffold)

Deprecation policy:

- keep legacy endpoints for at least one minor cycle after canonical endpoints are stable
- provide explicit migration notes in API docs and changelog

Versioned timeline:

- `v1`: canonical endpoints are primary; legacy endpoints still available with deprecation metadata
- `v1.x`: migration support window; SDK/docs default to canonical endpoints
- `v2`: planned removal of legacy endpoint surface (`/g2p`, `/tokenize`, `/ipa`)

### Legacy Payload Migration Contract

During `v1` and `v1.x`, legacy endpoints must return a JSON body field named `migration_notice`.

Reference contract:

```json
{
  "deprecated": true,
  "migration_phase": "v1",
  "removal_target": "v2",
  "replacement_endpoints": ["/phonemize", "/pronounce"],
  "docs": "https://github.com/CrowtherNLP/yoruba-phonology-assistant/blob/main/docs/API_EXAMPLES.md"
}
```

Schema constraints:

- `deprecated`: required boolean, must be `true`
- `migration_phase`: required string, currently `v1`
- `removal_target`: required string, currently `v2`
- `replacement_endpoints`: required non-empty array of canonical endpoint strings
- `docs`: required HTTPS URL to migration documentation

Validation requirement:

- Integration tests must assert `migration_notice` for `/g2p`, `/tokenize`, and `/ipa` until legacy removal.
- OpenAPI export must include the `migration_notice` response field for legacy response models.

---

## Package Integration Surfaces

### Python (`crowthernlp-yoruba-g2p`)

Primary use cases:

- backend services
- NLP pipelines
- evaluation tooling

Current interfaces in use:

- `G2P`
- `Tokenizer`
- `ToneExtractor`

### JavaScript (planned)

Goal: browser/Node integration for frontend tools and LLM tool adapters.

---

## AI Integration Layer (After Foundation Stability)

Once canonical API and phonology benchmarks are stable:

- LLM function-calling tool definitions
- pronunciation correction helpers
- TTS and speech-system adapters
- multilingual orchestration with Yoruba as phonology-first module

---

## Validation Layer

Technical validation:

- API contract parity checks
- regression tests
- benchmark score tracking
- migration payload contract assertions for legacy endpoints

Linguistic validation:

- native Yoruba speaker review
- minimal pair review workflow
- pronunciation acceptability sampling

---

## Preventing English-Fallback Errors

The integration stack enforces Yoruba-native behavior by design:

| Layer | Safeguard |
|------|-----------|
| Tokenization | Detect `gb`, `kp`, `ṣ`, `ẹ`, `ọ` before generic character processing |
| Phonology engine | Preserve atomic units and nasal-vowel token policy |
| Tone layer | Preserve `H/M/L` meaning as first-class data |
| API layer | Return explicit phonology outputs, not inferred English approximations |
| Integration sequencing | Block advanced AI integration until phonology contracts are stable |

---

## Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-05-10 | Phonology engine is mandatory foundation layer | AI consumers must not infer Yoruba pronunciation heuristically |
| 2026-05-10 | Canonical endpoint set defined as `/phonemize`, `/pronounce`, `/tone`, `/analyze` | Clarifies infrastructure intent and API contract boundaries |
| 2026-05-10 | Backward compatibility maintained for existing endpoints during transition | Protects current adopters while steering architecture |
| 2026-05-10 | `/disambiguate` kept in post-foundation track | Reduces risk of scope drift before core pronunciation stability |

---

## Open Questions

- [ ] exact versioning strategy for endpoint migration (v1 aliases vs v2 canonical-only)
- [ ] batching semantics for `/phonemize` and `/analyze`
- [ ] validation dataset publication schedule for native-speaker review cycles
