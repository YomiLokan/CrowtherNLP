from fastapi.testclient import TestClient

from api.server import app


client = TestClient(app)


def test_g2p_endpoint() -> None:
    response = client.post(
        "/g2p",
        json={"text": "ìgbà", "include_ipa": True, "include_ssml": True},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["method"] == "rule_engine"
    assert payload["tones"] == ["L", "L"]
    assert payload["ssml"] is not None
    assert payload["migration_notice"]["deprecated"] is True
    assert payload["migration_notice"]["replacement_endpoints"] == ["/phonemize", "/pronounce"]
    assert response.headers["Deprecation"] == "true"
    assert response.headers["X-Crowther-Replacement"] == "/phonemize,/pronounce"


def test_tokenize_endpoint() -> None:
    response = client.post("/tokenize", json={"text": "Ẹ káàbọ̀"})
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload["tokens"], list)
    assert isinstance(payload["special_chars"], list)
    assert payload["migration_notice"]["deprecated"] is True
    assert payload["migration_notice"]["replacement_endpoints"] == ["/analyze"]
    assert response.headers["Deprecation"] == "true"
    assert response.headers["X-Crowther-Replacement"] == "/analyze"


def test_ipa_endpoint() -> None:
    response = client.get("/ipa", params={"word": "gbogbo"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["word"] == "gbogbo"
    assert isinstance(payload["ipa"], str)
    assert isinstance(payload["tones"], list)
    assert payload["migration_notice"]["deprecated"] is True
    assert payload["migration_notice"]["replacement_endpoints"] == ["/pronounce"]
    assert response.headers["Deprecation"] == "true"
    assert response.headers["X-Crowther-Replacement"] == "/pronounce"


def test_phonemize_endpoint() -> None:
    response = client.post("/phonemize", json={"text": "ìgbà"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["input"] == "ìgbà"
    assert "/͡gb/" in payload["phonemes"]
    assert payload["method"] == "rule_engine"


def test_pronounce_endpoint() -> None:
    response = client.post(
        "/pronounce",
        json={"text": "Ẹ káàbọ̀", "include_ssml": True},
    )
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload["ipa"], str)
    assert isinstance(payload["tones"], list)
    assert payload["ssml"] is not None


def test_tone_endpoint() -> None:
    response = client.post("/tone", json={"text": "bá bà ba"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["tones"] == ["H", "L", "M"]
    assert isinstance(payload["tone_units"], list)


def test_analyze_endpoint() -> None:
    response = client.post(
        "/analyze",
        json={"text": "Ẹ káàbọ̀", "include_ssml": True},
    )
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload["tokens"], list)
    assert isinstance(payload["phonemes"], list)
    assert isinstance(payload["tones"], list)
    assert isinstance(payload["ipa"], str)
    assert payload["ssml"] is not None


def test_disambiguate_endpoint_heuristic() -> None:
    response = client.post(
        "/disambiguate",
        json={
            "word": "igba",
            "context": "Mo ra igba lọ sọja",
            "candidates": [
                {"form": "igba", "tones": "MM", "meaning": "200"},
                {"form": "igbá", "tones": "MH", "meaning": "calabash"},
                {"form": "ìgbà", "tones": "LL", "meaning": "time"},
            ],
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["selected"]["form"] == "igba"
    assert payload["method"] == "heuristic_context_v1"
    assert payload["status"] == "experimental_v1_1_heuristic"
    assert payload["stage"] == "heuristic"
    assert payload["confidence"] > 0.0


def test_disambiguate_endpoint_scaffold_fallback() -> None:
    response = client.post(
        "/disambiguate",
        json={
            "word": "igba",
            "context": "Ìtàn yi dáa.",
            "candidates": [
                {"form": "igbá", "tones": "MH", "meaning": "calabash"},
                {"form": "igba", "tones": "MM", "meaning": "200"},
                {"form": "ìgbà", "tones": "LL", "meaning": "time"},
            ],
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["selected"]["form"] == "igba"
    assert payload["method"] == "placeholder_disambiguation"
    assert payload["status"] == "not_final_v1_1_scaffold"
    assert payload["stage"] == "scaffold"
    assert payload["confidence"] == 0.0


def test_disambiguate_endpoint_requires_candidates() -> None:
    response = client.post(
        "/disambiguate",
        json={
            "word": "igba",
            "context": "Mo ra igba lọ sọja",
            "candidates": [],
        },
    )
    assert response.status_code == 422
