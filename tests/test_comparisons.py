import pytest

from utils.comparisons import compare_values


@pytest.mark.parametrize(
    "operator,a,b,expected",
    [
        ("=", 5, 5, True),
        ("!=", 5, 3, True),
        ("<", 3, 5, True),
        ("<=", 3, 5, True),
        (">", 5, 3, True),
        (">=", 5, 3, True),
        ("in", "a", "abc", True),
        ("anyInList", ["a", "x"], "abc", True),
        ("allInList", ["a", "b"], "abc", True),
        ("not_in", "x", "abc", True),
        ("contains", "abc", "a", True),
        ("not_contains", "abc", "x", True),
        ("startsWith", "abc", "a", True),
    ],
)
def test_compare_values(operator, a, b, expected):
    assert compare_values(operator, a, b) == expected
