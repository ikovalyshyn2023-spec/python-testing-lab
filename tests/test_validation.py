import pytest
from src.validation import require_int, require_text


def test_require_int_returns_valid_value():
    assert require_int(5, "n") == 5
    assert require_int(0, "n") == 0


def test_require_int_accepts_value_at_minimum():
    assert require_int(1, "n", minimum=1) == 1


def test_require_int_rejects_below_minimum():
    with pytest.raises(ValueError):
        require_int(-1, "n")
    with pytest.raises(ValueError):
        require_int(0, "n", minimum=1)


def test_require_int_rejects_bool():
    with pytest.raises(TypeError):
        require_int(True, "n")
    with pytest.raises(TypeError):
        require_int(False, "n")


def test_require_int_rejects_float_and_str():
    with pytest.raises(TypeError):
        require_int(1.5, "n")
    with pytest.raises(TypeError):
        require_int("10", "n")


def test_require_text_returns_stripped():
    assert require_text("  hello  ", "t") == "hello"


def test_require_text_rejects_empty_and_whitespace():
    with pytest.raises(ValueError):
        require_text("", "t")
    with pytest.raises(ValueError):
        require_text("   ", "t")


def test_require_text_rejects_non_string():
    with pytest.raises(TypeError):
        require_text(123, "t")
    with pytest.raises(TypeError):
        require_text(None, "t")
