from yoruba_g2p import G2P, ToneExtractor


def test_tone_extraction_hml() -> None:
    extractor = ToneExtractor()
    assert extractor.extract("bá bà ba") == ["H", "L", "M"]


def test_g2p_core_output() -> None:
    g2p = G2P(backend="rules")
    result = g2p.convert("ìgbà", include_ssml=True)

    assert result.method == "rule_engine"
    assert result.tones == ["L", "L"]
    assert "/͡gb/" in result.phonemes
    assert result.ssml is not None


def test_standard_yoruba_scope_sample_word() -> None:
    g2p = G2P(backend="hybrid")
    result = g2p.convert("Ẹ káàbọ̀")

    assert result.method == "rule_engine"
    assert len(result.tones) >= 1
