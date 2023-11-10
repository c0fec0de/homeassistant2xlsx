#
# MIT License
#
# Copyright (c) 2023 c0fec0de
#

"""Convertion Testing."""


from homeassistant2xlsx import INVALID_NAME, INVALID_TYPE, UNAVAILABLE, _convert


def test_ignore_reserved():
    """Conversion of reserved keywords."""
    for type_ in (None, "int", "float", "other"):
        for value in (UNAVAILABLE, INVALID_NAME):
            assert _convert(type_, value) == value


def test_notype():
    """Convertion without type."""
    values = [None, "", "True", "false", "abc", 12, 12.3, "12", "12.3"]
    for value in values:
        assert _convert(None, value) == value


def test_int():
    """Integer."""
    assert _convert("int", None) is None
    assert _convert("int", "") is None
    assert _convert("int", "True") == "invalid literal for int() with base 10: 'True'"
    assert _convert("int", "False") == "invalid literal for int() with base 10: 'False'"
    assert _convert("int", "abc") == "invalid literal for int() with base 10: 'abc'"
    assert _convert("int", 12) == 12
    assert _convert("int", 12.7) == 12
    assert _convert("int", "12") == 12
    assert _convert("int", "12.7") == "invalid literal for int() with base 10: '12.7'"


def test_float():
    """Float."""
    assert _convert("float", None) is None
    assert _convert("float", "") is None
    assert _convert("float", "True") == "could not convert string to float: 'True'"
    assert _convert("float", "False") == "could not convert string to float: 'False'"
    assert _convert("float", "abc") == "could not convert string to float: 'abc'"
    assert _convert("float", 12) == 12
    assert _convert("float", 12.7) == 12.7
    assert _convert("float", "12") == 12
    assert _convert("float", "12.7") == 12.7


def test_invalidtype():
    """Invalid Type."""

    assert _convert("foo", 5) == INVALID_TYPE
