from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.server import app

EXPECTED_PHASE = "v1"
EXPECTED_REMOVAL = "v2"
EXPECTED_DOCS_URL = (
    "https://github.com/CrowtherNLP/yoruba-phonology-assistant/blob/main/docs/API_EXAMPLES.md"
)

LEGACY_CASES = [
    {
        "path": "/g2p",
        "method": "post",
        "payload": {"text": "igba", "include_ipa": True, "include_ssml": False},
        "expected_replacements": ["/phonemize", "/pronounce"],
    },
    {
        "path": "/tokenize",
        "method": "post",
        "payload": {"text": "E kaabo"},
        "expected_replacements": ["/analyze"],
    },
    {
        "path": "/ipa",
        "method": "get",
        "payload": {"word": "gbogbo"},
        "expected_replacements": ["/pronounce"],
    },
]

EXPECTED_SCHEMAS = ["G2PResponse", "TokenizeResponse", "IPAResponse"]


def _request(client: TestClient, method: str, path: str, payload: dict[str, object]):
    if method == "post":
        return client.post(path, json=payload)
    return client.get(path, params=payload)


def _check_runtime_payloads() -> list[str]:
    client = TestClient(app)
    failures: list[str] = []

    for case in LEGACY_CASES:
        response = _request(client, case["method"], case["path"], case["payload"])
        if response.status_code != 200:
            failures.append(
                f"{case['path']} expected HTTP 200, got {response.status_code}"
            )
            continue

        payload = response.json()
        notice = payload.get("migration_notice")
        if not isinstance(notice, dict):
            failures.append(f"{case['path']} missing migration_notice object")
            continue

        if notice.get("deprecated") is not True:
            failures.append(f"{case['path']} migration_notice.deprecated must be true")

        if notice.get("migration_phase") != EXPECTED_PHASE:
            failures.append(
                f"{case['path']} migration_notice.migration_phase must be '{EXPECTED_PHASE}'"
            )

        if notice.get("removal_target") != EXPECTED_REMOVAL:
            failures.append(
                f"{case['path']} migration_notice.removal_target must be '{EXPECTED_REMOVAL}'"
            )

        if notice.get("docs") != EXPECTED_DOCS_URL:
            failures.append(
                f"{case['path']} migration_notice.docs must match canonical docs URL"
            )

        replacements = notice.get("replacement_endpoints")
        if replacements != case["expected_replacements"]:
            failures.append(
                f"{case['path']} replacement_endpoints expected {case['expected_replacements']}, got {replacements}"
            )

    return failures


def _check_openapi_schema() -> list[str]:
    failures: list[str] = []
    schema = app.openapi()
    components = schema.get("components", {})
    schemas = components.get("schemas", {})

    for schema_name in EXPECTED_SCHEMAS:
        model_schema = schemas.get(schema_name)
        if not isinstance(model_schema, dict):
            failures.append(f"OpenAPI missing schema for {schema_name}")
            continue

        properties = model_schema.get("properties", {})
        if "migration_notice" not in properties:
            failures.append(f"OpenAPI {schema_name} missing migration_notice property")

    return failures


def main() -> int:
    failures = []
    failures.extend(_check_runtime_payloads())
    failures.extend(_check_openapi_schema())

    if failures:
        print("Migration contract check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Migration contract check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
