import pytest

from utils.comparisons import compare_values, find


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


def test_find():
    from dataclasses import dataclass

    @dataclass
    class TestClass:
        id: int
        name: str
        tags: list

    instances = [
        TestClass(1, "Alice", ["tag1", "tag2"]),
        TestClass(2, "Bob", ["tag2", "tag3"]),
        TestClass(3, "Charlie", ["tag1", "tag3"]),
    ]
    search_attrs = {
        "tags": ("anyInList", ["tag1"]),
        "name": ("startsWith", "A"),
    }
    results = find(
        search_attributes=search_attrs, class_=TestClass, class_instances=instances
    )
    assert len(results) == 1
    assert results[0].name == "Alice"
