from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DOC_FILES = {
    "api_examples": ROOT / "docs" / "API_EXAMPLES.md",
    "integration_plan": ROOT / "docs" / "INTEGRATION_PLAN.md",
    "publishing_plan": ROOT / "docs" / "PUBLISHING_PLAN.md",
    "changelog": ROOT / "CHANGELOG.md",
}

EXPECTED_MAPPING = {
    "/g2p": ["/phonemize", "/pronounce"],
    "/tokenize": ["/analyze"],
    "/ipa": ["/pronounce"],
}

EXPECTED_PHASE = "v1"
EXPECTED_REMOVAL = "v2"

SOURCE_PATTERN = re.compile(r"-\s*`(/g2p|/tokenize|/ipa)`")
TARGET_PATTERN = re.compile(r"`(/[^`]+)`")


def _extract_mapping(text: str) -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = {}

    for line in text.splitlines():
        source_match = SOURCE_PATTERN.search(line)
        if not source_match:
            continue

        source = source_match.group(1)
        all_backtick_paths = TARGET_PATTERN.findall(line)
        targets = sorted({path for path in all_backtick_paths if path != source})
        if targets:
            mapping[source] = targets

    return mapping


def _contains_phase(text: str) -> bool:
    return (
        "Current phase: `v1`" in text
        or "migration_phase\": \"v1\"" in text
        or "migration_phase`: `v1`" in text
        or "migration_phase: \"v1\"" in text
        or "`v1` migration window" in text
        or ("migration_phase" in text and "v1" in text)
    )


def _contains_removal(text: str) -> bool:
    return (
        "Legacy removal target: `v2`" in text
        or "Planned legacy removal target: `v2`" in text
        or "removal_target\": \"v2\"" in text
        or ("removal_target" in text and "v2" in text)
    )


def _expect_subset_mapping(found: dict[str, list[str]], failures: list[str], file_label: str) -> None:
    for source, expected_targets in EXPECTED_MAPPING.items():
        if source not in found:
            continue
        actual = sorted(found[source])
        expected = sorted(expected_targets)
        if actual != expected:
            failures.append(
                f"{file_label}: mapping for {source} expected {expected}, found {actual}"
            )


def main() -> int:
    failures: list[str] = []

    for label, path in DOC_FILES.items():
        if not path.exists():
            failures.append(f"{label}: file missing at {path}")
            continue

        text = path.read_text(encoding="utf-8")

        found = _extract_mapping(text)
        _expect_subset_mapping(found, failures, label)

        if label in {"api_examples", "changelog"}:
            if not all(key in found for key in EXPECTED_MAPPING):
                failures.append(
                    f"{label}: missing one or more required legacy mappings ({', '.join(EXPECTED_MAPPING)})"
                )

        if label in {"api_examples", "changelog", "integration_plan", "publishing_plan"}:
            if not _contains_phase(text):
                failures.append(f"{label}: expected migration phase '{EXPECTED_PHASE}' mention")
            if not _contains_removal(text):
                failures.append(f"{label}: expected removal target '{EXPECTED_REMOVAL}' mention")

    if failures:
        print("Docs migration contract check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Docs migration contract check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
