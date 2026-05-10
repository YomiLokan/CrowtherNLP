from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from yoruba_g2p import G2P
from yoruba_g2p.rules.digraphs import split_graphemes
from yoruba_g2p.rules.phonemes import canonical_token, is_vowel_token


@dataclass
class GoldRecord:
    word: str
    phonemes: list[str]
    tones: list[str]


@dataclass
class EvalRow:
    word: str
    ref_phonemes: list[str]
    hyp_phonemes: list[str]
    ref_tones: list[str]
    hyp_tones: list[str]
    phoneme_edits: int
    tone_matches: int
    tone_total: int
    exact_word_match: bool


PredictFn = Callable[[str], tuple[list[str], list[str]]]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate deterministic Yoruba G2P")
    parser.add_argument(
        "--gold",
        type=Path,
        default=Path("benchmarks/data/gold_words.jsonl"),
        help="Path to JSONL gold benchmark records",
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        default=None,
        help="Optional path to write JSON metrics output",
    )
    parser.add_argument(
        "--show-rows",
        action="store_true",
        help="Print per-word comparison rows",
    )
    parser.add_argument(
        "--models",
        type=str,
        default="baseline,rules,hybrid",
        help="Comma-separated models to evaluate (supported: baseline, rules, hybrid)",
    )
    return parser.parse_args()


def load_gold(path: Path) -> list[GoldRecord]:
    records: list[GoldRecord] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            raw = json.loads(line)
            records.append(
                GoldRecord(
                    word=raw["word"],
                    phonemes=list(raw["phonemes"]),
                    tones=list(raw["tones"]),
                )
            )
    return records


def levenshtein_distance(seq1: list[str], seq2: list[str]) -> int:
    if not seq1:
        return len(seq2)
    if not seq2:
        return len(seq1)

    prev = list(range(len(seq2) + 1))
    for i, a in enumerate(seq1, start=1):
        cur = [i]
        for j, b in enumerate(seq2, start=1):
            insert_cost = cur[j - 1] + 1
            delete_cost = prev[j] + 1
            replace_cost = prev[j - 1] + (0 if a == b else 1)
            cur.append(min(insert_cost, delete_cost, replace_cost))
        prev = cur
    return prev[-1]


def tone_match_counts(ref: list[str], hyp: list[str]) -> tuple[int, int]:
    total = max(len(ref), len(hyp))
    if total == 0:
        return 0, 0

    matches = 0
    for i in range(min(len(ref), len(hyp))):
        if ref[i] == hyp[i]:
            matches += 1
    return matches, total


def _rules_predictor() -> PredictFn:
    g2p = G2P(backend="rules")

    def _predict(text: str) -> tuple[list[str], list[str]]:
        result = g2p.convert(text)
        return result.phonemes, result.tones

    return _predict


def _baseline_predict(text: str) -> tuple[list[str], list[str]]:
    # Intentionally simplistic baseline to emulate English-adjacent fallback behavior.
    char_to_ipa = {
        "a": "/a/",
        "e": "/e/",
        "ẹ": "/e/",
        "i": "/i/",
        "o": "/o/",
        "ọ": "/o/",
        "u": "/u/",
        "b": "/b/",
        "d": "/d/",
        "f": "/f/",
        "g": "/g/",
        "h": "/h/",
        "j": "/dʒ/",
        "k": "/k/",
        "l": "/l/",
        "m": "/m/",
        "n": "/n/",
        "p": "/p/",
        "r": "/r/",
        "s": "/s/",
        "ṣ": "/s/",
        "t": "/t/",
        "w": "/w/",
        "y": "/j/",
    }

    phonemes: list[str] = []
    tones: list[str] = []
    for g in split_graphemes(text):
        c = canonical_token(g)
        if not c or c.isspace():
            continue
        mapped = char_to_ipa.get(c)
        if mapped:
            phonemes.append(mapped)
        if is_vowel_token(g):
            tones.append("M")

    return phonemes, tones


def _get_predictor(model_name: str) -> PredictFn:
    if model_name in {"rules", "hybrid"}:
        return _rules_predictor()
    if model_name == "baseline":
        return _baseline_predict
    raise ValueError(f"Unsupported model: {model_name}")


def evaluate(records: Iterable[GoldRecord], predictor: PredictFn) -> tuple[list[EvalRow], dict[str, float | int]]:
    rows: list[EvalRow] = []

    total_phoneme_edits = 0
    total_ref_phonemes = 0
    total_tone_matches = 0
    total_tones = 0
    exact_words = 0

    for rec in records:
        hyp_phonemes, hyp_tones = predictor(rec.word)
        edits = levenshtein_distance(rec.phonemes, hyp_phonemes)
        tone_matches, tone_total = tone_match_counts(rec.tones, hyp_tones)

        exact = (rec.phonemes == hyp_phonemes) and (rec.tones == hyp_tones)
        if exact:
            exact_words += 1

        rows.append(
            EvalRow(
                word=rec.word,
                ref_phonemes=rec.phonemes,
                hyp_phonemes=hyp_phonemes,
                ref_tones=rec.tones,
                hyp_tones=hyp_tones,
                phoneme_edits=edits,
                tone_matches=tone_matches,
                tone_total=tone_total,
                exact_word_match=exact,
            )
        )

        total_phoneme_edits += edits
        total_ref_phonemes += len(rec.phonemes)
        total_tone_matches += tone_matches
        total_tones += tone_total

    n = len(rows)
    metrics: dict[str, float | int] = {
        "samples": n,
        "phoneme_error_rate": (total_phoneme_edits / total_ref_phonemes) if total_ref_phonemes else 0.0,
        "tone_accuracy": (total_tone_matches / total_tones) if total_tones else 0.0,
        "word_exact_match": (exact_words / n) if n else 0.0,
        "total_phoneme_edits": total_phoneme_edits,
    }
    return rows, metrics


def print_report(rows: list[EvalRow], metrics: dict[str, float | int], show_rows: bool) -> None:
    print("Yoruba G2P Evaluation")
    print("-" * 60)
    print(f"Samples: {metrics['samples']}")
    print(f"PER: {metrics['phoneme_error_rate']:.4f}")
    print(f"Tone Accuracy: {metrics['tone_accuracy']:.4f}")
    print(f"Word Exact Match: {metrics['word_exact_match']:.4f}")
    print(f"Total Phoneme Edits: {metrics['total_phoneme_edits']}")

    if show_rows:
        print("\nPer-word rows")
        print("-" * 60)
        for row in rows:
            print(
                json.dumps(
                    {
                        "word": row.word,
                        "ref_phonemes": row.ref_phonemes,
                        "hyp_phonemes": row.hyp_phonemes,
                        "ref_tones": row.ref_tones,
                        "hyp_tones": row.hyp_tones,
                        "phoneme_edits": row.phoneme_edits,
                        "exact_word_match": row.exact_word_match,
                    },
                    ensure_ascii=False,
                )
            )


def print_side_by_side_report(results: dict[str, dict[str, float | int]]) -> None:
    print("\nSide-by-side results")
    print("-" * 60)
    print("| Model | Phoneme Error Rate (PER) | Tone Accuracy | Word Exact Match |")
    print("|-------|--------------------------|---------------|------------------|")

    for model_name, metrics in results.items():
        print(
            "| "
            f"{model_name} | "
            f"{metrics['phoneme_error_rate']:.4f} | "
            f"{metrics['tone_accuracy']:.4f} | "
            f"{metrics['word_exact_match']:.4f} |"
        )


def parse_models(raw_models: str) -> list[str]:
    models = [m.strip() for m in raw_models.split(",") if m.strip()]
    supported = {"rules", "baseline", "hybrid"}
    invalid = [m for m in models if m not in supported]
    if invalid:
        raise ValueError(f"Unsupported model(s): {', '.join(invalid)}")
    if not models:
        raise ValueError("No models provided")
    return models


def main() -> int:
    args = parse_args()
    records = load_gold(args.gold)
    model_names = parse_models(args.models)

    output: dict[str, dict[str, float | int]] = {}
    for i, model_name in enumerate(model_names):
        predictor = _get_predictor(model_name)
        rows, metrics = evaluate(records, predictor)
        output[model_name] = metrics

        print(f"\n=== Model: {model_name} ===")
        print_report(rows, metrics, show_rows=args.show_rows)

        # Avoid duplicate row dumps in multi-model mode unless explicitly desired.
        if args.show_rows and i < len(model_names) - 1:
            args.show_rows = False

    if len(output) > 1:
        print_side_by_side_report(output)

    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(
            json.dumps(output if len(output) > 1 else next(iter(output.values())), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
