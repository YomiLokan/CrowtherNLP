# CrowtherNLP — Project Plan

> **Status:** Active — Direction Reset v1  
> **Created:** 2026-05-10  
> **Last Updated:** 2026-05-10  
> **Organisation:** CrowtherNLP

---

## Identity and Mission

CrowtherNLP is an AI-native Yoruba phonology infrastructure project named in honor of Bishop Samuel Ajayi Crowther, whose work helped establish written Yoruba orthography.

The mission is to build a standardized Yoruba phonology and pronunciation infrastructure layer that modern AI systems can reliably use for pronunciation, tone analysis, speech generation, NLP, and LLM tool integration.

---

## Core Problem

Most modern AI systems pronounce Yoruba incorrectly because they:

- rely on English phonetic assumptions
- split Yoruba atomic phonemes incorrectly
- ignore tonal meaning
- do not model Yoruba-native phonological structure

CrowtherNLP does not attempt to reinvent Yoruba linguistic research or basic G2P theory. It operationalizes Yoruba phonology into reusable infrastructure.

---

## Foundational Principle

The pronunciation engine must exist before advanced AI integration.

```
Yoruba Text
  → Yoruba Phonology Engine
  → Tone + Phoneme Representation
  → AI / LLM / TTS / Speech Systems
```

The phonology layer is the foundation of the entire system.

---

## Current Project Status (Reality Check)

The following is already implemented in this repository:

- deterministic Standard Yoruba phonology engine
- atomic token handling for `gb`, `kp`, `ṣ`, `ẹ`, `ọ`
- single-token nasal vowel representation
- tone extraction (`H`, `M`, `L`)
- API endpoints currently live: `/g2p`, `/tokenize`, `/ipa`, `/disambiguate` (heuristic v1.1 scaffold)
- benchmark harness with baseline/rules/hybrid comparator
- OpenAPI parity checks in CI

Steering implication: the technical foundation is present, so the next work is interface standardization, naming alignment, and infrastructure hardening for broader AI consumption.

---

## Initial Technical Decisions (Confirmed)

| Area | Decision |
|------|----------|
| Organization | CrowtherNLP |
| Initial dialect scope | Standard Yoruba only |
| Atomic consonants | `gb`, `kp` treated as single phoneme units |
| Distinct consonants | `ṣ` is distinct from `s` |
| Distinct vowels | `ẹ` and `ọ` are distinct vowels |
| Tone | High, Mid, Low are computationally preserved |
| Nasal vowels | Represented as single phoneme tokens |

---

## Initial MVP Objectives

### 1. Yoruba Phoneme Inventory

Create and publish a standardized machine-readable Yoruba phoneme system.

### 2. Tokenization Engine

Correctly identify and preserve:

- `gb`
- `kp`
- `ṣ`
- `ẹ`
- `ọ`

before processing standard Latin characters.

### 3. Tone System

Represent and preserve tonal meaning computationally:

- High tone
- Mid tone
- Low tone

### 4. Grapheme-to-Phoneme Engine (Core Foundation)

Build pronunciation engine first.

Input: Yoruba orthography  
Output:

- phoneme tokens
- IPA representation
- tone structure

### 5. Pronunciation API Layer

Canonical MVP endpoint surface:

- `/phonemize`
- `/pronounce`
- `/tone`
- `/analyze`

### 6. AI Integration Layer

Only after phonology engine is stable:

- LLM function-calling support
- pronunciation correction tooling
- speech system integration
- TTS compatibility
- multilingual AI support

### 7. Validation Layer

Evaluate pronunciation accuracy with native Yoruba speakers.

---

## Roadmap Phases

### Phase A — Foundation Hardening (Now)

- lock phonology rules and tokenization guarantees
- keep benchmark and API contract parity checks mandatory
- maintain Standard Yoruba-only scope

### Phase B — Canonical API Alignment (Next)

- introduce canonical endpoints (`/phonemize`, `/pronounce`, `/tone`, `/analyze`)
- maintain compatibility aliases for existing endpoints during transition
- document endpoint migration path in integration docs

### Phase C — Validation and Adoption

- grow evaluation sets and native-speaker review loop
- publish reproducible scorecards for tone and pronunciation quality

### Phase D — Post-MVP (v1.1+)

- `/disambiguate` maturity beyond heuristic scaffold
- contextual tone interpretation
- semantic analysis
- dialect profiles
- speech synthesis integration
- Yoruba educational tooling
- multilingual African language expansion

---

## Non-Goals (Current Scope)

- reinventing Yoruba linguistic theory
- unbounded dialect expansion before Standard Yoruba is solid
- model-first AI integration before pronunciation infrastructure is stable

---

## Long-Term Vision

CrowtherNLP aims to become foundational phonology infrastructure for Yoruba and future African language AI systems.

Priority order:

1. Yoruba-native phonological correctness
2. Tone-aware computation
3. AI integration readiness
4. Developer usability
5. Linguistic preservation through modern infrastructure

---

## Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-05-10 | Organization fixed as CrowtherNLP | Establishes stable identity and publishing namespace |
| 2026-05-10 | Standard Yoruba only for initial scope | Reduces ambiguity and enables measurable quality |
| 2026-05-10 | Phonology engine before AI integration | Prevents English-fallback pronunciation errors upstream |
| 2026-05-10 | Atomic phoneme representation selected | Keeps Yoruba-native units stable across APIs and tooling |
| 2026-05-10 | Nasal vowels treated as single phoneme tokens | Aligns computation with chosen project phonology model |
| 2026-05-10 | `/disambiguate` treated as post-foundation capability | Keeps core release focused on pronunciation infrastructure |

---

## Open Questions

- [ ] API transition timeline from legacy endpoints to canonical MVP endpoints
- [ ] Native speaker validation protocol and reviewer panel workflow
- [ ] Public domain and hosting plan for production API
