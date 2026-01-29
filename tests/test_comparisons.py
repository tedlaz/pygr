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
        ("any_in", ["a", "x"], "abc", True),
        ("all_in", ["a", "b"], "abc", True),
        ("not in", "x", "abc", True),
        ("contains", "abc", "a", True),
        ("not contains", "abc", "x", True),
        ("starts with", "abc", "a", True),
    ],
)
def test_compare_values(operator, a, b, expected):
    assert compare_values(operator, a, b) == expected
