# CrowtherNLP — Publishing Plan

> **Status:** Active — Direction Reset v1  
> **Created:** 2026-05-10  
> **Last Updated:** 2026-05-10  
> **Organisation:** CrowtherNLP

---

## Publishing Objective

Publish CrowtherNLP as foundational Yoruba phonology infrastructure for AI systems.

Publishing sequence follows architecture priority:

1. phonology infrastructure credibility
2. developer adoption
3. AI integration ecosystem
4. enterprise reliability

---

## Current Status Checkpoint

Already publish-ready in repository:

- Apache 2.0 license, contribution guide, and expanded README
- deterministic phonology engine and API service
- benchmark harness with reproducible metrics
- OpenAPI contract with parity checks in CI

Not yet live publicly:

- hosted production API domain
- package registry releases
- official Hugging Face model/dataset cards

Steering implication: next publishing effort should prioritize infrastructure positioning and API onboarding, not model-marketing first.

---

## Publishing Philosophy

1. **Phonology-first trust**: prove Yoruba-native correctness before broad AI claims.
2. **Open infrastructure core**: rules, contracts, and tooling stay transparent.
3. **Developer-first ergonomics**: clear API, stable schemas, benchmark reproducibility.
4. **Free-first adoption**: reduce friction for research and ecosystem uptake.
5. **Enterprise readiness later**: SLA and paid tiers after proven utility.

---

## Channel Strategy

```
GitHub (source of truth: engine + API + benchmarks + docs)
    ↓
PyPI (Python infrastructure package)
    ↓
Hosted API (canonical endpoint surface)
    ↓
Developer ecosystem integrations (LLM tools, TTS adapters, SDKs)
    ↓
Hugging Face + community channels (for discoverability and collaboration)
    ↓
Enterprise tier (SLA, support, high-volume usage)
```

---

## Channel 1 — GitHub (Primary Source of Truth)

**Repository:** `github.com/CrowtherNLP/yoruba-phonology-assistant`  
**License:** Apache 2.0  
**Visibility:** Public

GitHub must communicate infrastructure identity clearly:

- CrowtherNLP as Yoruba phonology layer for AI systems
- phonology-first architecture and rationale
- canonical endpoint roadmap (`/phonemize`, `/pronounce`, `/tone`, `/analyze`)
- reproducible benchmark and validation process

CI requirements:

- tests
- benchmark execution
- OpenAPI parity check
- package smoke checks

---

## Channel 2 — PyPI (Developer Distribution)

**Package:** `crowthernlp-yoruba-g2p`

Positioning:

- deterministic phonology infrastructure SDK
- server-side and pipeline integration
- stable programmatic API for phonemization, tone, and analysis workflows

Release gating:

- all CI checks green
- benchmark report regenerated
- API spec parity confirmed

---

## Channel 3 — Hosted API (Infrastructure Access Layer)

Canonical public endpoint strategy:

- `/phonemize`
- `/pronounce`
- `/tone`
- `/analyze`

Transition policy:

- temporary compatibility aliases for existing endpoint names
- documented migration path and deprecation schedule

Documentation assets:

- committed `openapi.yaml`
- API examples
- changelog notes for contract evolution

Migration payload requirement during transition:

- legacy endpoints (`/g2p`, `/tokenize`, `/ipa`) must include a `migration_notice` field in JSON responses
- `migration_notice.replacement_endpoints` must only reference canonical endpoints
- response headers and JSON body guidance must remain semantically aligned

Partner validation snippet (release docs):

```json
{
    "migration_notice": {
        "deprecated": true,
        "migration_phase": "v1",
        "removal_target": "v2",
        "replacement_endpoints": ["/analyze"],
        "docs": "https://github.com/CrowtherNLP/yoruba-phonology-assistant/blob/main/docs/API_EXAMPLES.md"
    }
}
```

Pre-release gate:

- reject release if any legacy endpoint omits `migration_notice`
- reject release if OpenAPI and runtime schema differ on migration fields
- reject release if migration mapping in changelog, docs, and API examples diverges

---

## Channel 4 — Ecosystem Integrations

After core API stabilizes:

- LLM function-calling tool schemas
- pronunciation correction tool wrappers
- TTS and speech adapter templates
- multilingual orchestration compatibility notes

---

## Channel 5 — Community and Research Outreach

Primary communities:

- Masakhane
- AfricaNLP
- Yoruba linguistics collaborators

What to publish in outreach:

- benchmark methodology and results
- phonology contract and API docs
- validation framework with native-speaker feedback loops

---

## Adoption Metrics (Infrastructure-Focused)

| Milestone | Metric | Target |
|-----------|--------|--------|
| Developer onboarding | API quickstart completion rate | Track and improve |
| Reliability | CI pass rate on main | >95% |
| Credibility | Reproducible benchmark artifacts | Required on release |
| Adoption | PyPI downloads | Upward trend |
| Integration pull | API usage from external tools | Upward trend |
| Linguistic quality | Native-speaker validation rounds | Regular cadence |

---

## Monetization Roadmap (Later)

Keep free-first model until infrastructure adoption signals are clear.

Potential later tiers:

- free developer tier
- production tier with API keys and quotas
- enterprise tier with SLA and priority support

---

## Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-05-10 | Brand and organization set to CrowtherNLP | Creates coherent identity for long-term ecosystem adoption |
| 2026-05-10 | Publishing narrative shifted to infrastructure-first | Aligns messaging with phonology-foundation principle |
| 2026-05-10 | Canonical endpoint roadmap prioritized in publishing assets | Ensures external developers integrate against intended interface |
| 2026-05-10 | Free-first adoption retained | Lowers entry barrier for researchers and builders |

---

## Open Questions

- [ ] production API domain and hosting provider choice
- [ ] exact timeline for canonical endpoint public launch
- [ ] first public version tags for PyPI and API
- [ ] native-speaker validation publication format
