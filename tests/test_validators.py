import pytest

from utils.validators import is_valid_afm, is_valid_amka


@pytest.mark.parametrize(
    "afm,expected",
    [
        ("1", False),
        (1, False),
        ("1a", False),
        ("123456789", False),
        ("123456789b", False),
        ("012312312", True),
    ],
)
def test_is_valid_afm(afm, expected):
    assert is_valid_afm(afm) == expected


@pytest.mark.parametrize(
    "amka,expected",
    [
        ("1", False),
        (1, False),
        ("1a", False),
        ("12345678901", False),
        ("1234567890a", False),
        ("12345678912cb", False),
        ("13080002382", True),
    ],
)
def test_is_valid_amka(amka, expected):
    assert is_valid_amka(amka) == expected
