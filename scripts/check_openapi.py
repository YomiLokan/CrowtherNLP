from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.server import app


def main() -> int:
    spec_path = ROOT / "openapi.yaml"
    if not spec_path.exists():
        print("openapi.yaml does not exist")
        return 1

    committed = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    generated = app.openapi()

    if committed != generated:
        print("OpenAPI parity check failed.")
        print("Run: /usr/bin/python3 scripts/export_openapi.py")
        return 1

    print("OpenAPI parity check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
