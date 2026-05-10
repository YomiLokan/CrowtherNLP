# Benchmark Harness

This folder contains a starter evaluation harness for Yoruba G2P.

## Current gold set coverage

- Standard Yoruba-only benchmark entries
- Minimal tone pairs and triplets (`ba`, `bá`, `bà`; `gba`, `gbá`, `gbà`; `kpa`, `kpá`, `kpà`)
- Digraph-heavy words (`gb`, `kp`)
- Dotted-vowel words (`ẹ`, `ọ`, `ṣ`)
- Nasal-vowel single-token cases (`tan`, `dun`, `rin`, `ọ̀nà`, `àwọn`)
- Short phrase coverage (`Ẹ káàbọ̀`)

Current sample count: 31

## Current metrics

- Phoneme Error Rate (PER): token-level Levenshtein distance over phoneme sequences
- Tone accuracy: exact token-level match rate over tone labels
- Word exact match: percentage where both phonemes and tones match exactly

## Run

```bash
/usr/bin/python3 benchmarks/evaluate.py --gold benchmarks/data/gold_words.jsonl
```

## Compare models side-by-side

```bash
/usr/bin/python3 benchmarks/evaluate.py \
	--gold benchmarks/data/gold_words.jsonl \
	--models baseline,rules,hybrid
```

This prints a markdown table in publishing-plan format:

- Model
- Phoneme Error Rate (PER)
- Tone Accuracy
- Word Exact Match

Current implementation note:

- `hybrid` is currently an alias of `rules` until neural fallback is implemented.

## Write metrics to JSON

```bash
/usr/bin/python3 benchmarks/evaluate.py \
	--gold benchmarks/data/gold_words.jsonl \
	--models baseline,rules,hybrid \
	--json-out benchmarks/results/latest.json
```
