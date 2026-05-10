# Local Run Guide

## Prerequisites

- Python 3.9+
- Project root as current working directory

## Install dependencies

```bash
/usr/bin/python3 -m pip install -e .
/usr/bin/python3 -m pip install fastapi uvicorn httpx pytest PyYAML
```

## Run tests

```bash
/usr/bin/python3 -m pytest -q
```

## Start the API server

```bash
/usr/bin/python3 -m api.server
```

## Verify routes quickly

```bash
/usr/bin/python3 -c "from api.server import app; print(sorted({route.path for route in app.routes}))"
```

## Export and verify OpenAPI

```bash
/usr/bin/python3 scripts/export_openapi.py
/usr/bin/python3 scripts/check_openapi.py
```

## Verify legacy migration contract

```bash
/usr/bin/python3 scripts/check_migration_contract.py
```

## Verify docs migration contract

```bash
/usr/bin/python3 scripts/check_docs_migration_contract.py
```

## Open API docs

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Quick endpoint checks

```bash
curl -X POST http://127.0.0.1:8000/g2p \
  -H "Content-Type: application/json" \
  -d '{"text":"ìgbà","include_ipa":true,"include_ssml":true}'

curl -X POST http://127.0.0.1:8000/tokenize \
  -H "Content-Type: application/json" \
  -d '{"text":"Ẹ káàbọ̀"}'

curl "http://127.0.0.1:8000/ipa?word=gbogbo"
```
