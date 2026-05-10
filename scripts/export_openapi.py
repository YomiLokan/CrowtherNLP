from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.server import app


def main() -> int:
    output_path = ROOT / "openapi.yaml"
    schema = app.openapi()
    output_path.write_text(
        yaml.safe_dump(schema, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    print(f"Wrote OpenAPI spec to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
