from yoruba_g2p import Tokenizer


def test_gb_is_atomic_unit() -> None:
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize("ìgbà")
    assert "gb" in tokens


def test_kp_is_atomic_unit() -> None:
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize("kpa")
    assert tokens[0] == "kp"


def test_nasal_vowel_is_single_token() -> None:
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize("ọn")
    assert tokens == ["ọn"]
