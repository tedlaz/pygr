import pytest

from utils.texts import are_texts_equal, grup


@pytest.mark.parametrize(
    "input_text,expected_output",
    [
        ("Καλημέρα", "ΚΑΛΗΜΕΡΑ"),
        ("Καλησπέρα", "ΚΑΛΗΣΠΕΡΑ"),
        ("Καληνύχτα", "ΚΑΛΗΝΥΧΤΑ"),
        ("Άνθρωπος", "ΑΝΘΡΩΠΟΣ"),
        ("Ελλάδα", "ΕΛΛΑΔΑ"),
        ("Ήλιος", "ΗΛΙΟΣ"),
        ("Ίριδα", "ΙΡΙΔΑ"),
        ("Ϊκαρος", "ΙΚΑΡΟΣ"),
        ("Όμορφος", "ΟΜΟΡΦΟΣ"),
        ("Ύμνος", "ΥΜΝΟΣ"),
        ("Ϋδρογόνο", "ΥΔΡΟΓΟΝΟ"),
        ("Ώρα", "ΩΡΑ"),
        ("Δοϊράνη special", "ΔΟΙΡΑΝΗ SPECIAL"),
        ("ΰ", "Υ"),
    ],
)
def test_grup(input_text, expected_output):
    assert grup(input_text) == expected_output


def test_grup_special_characters():
    input_text = "Ϋ́ Ϊ́"
    expected_output = "Υ Ι"
    assert input_text == "Ϋ́ Ϊ́"
    assert grup(input_text) == expected_output


@pytest.mark.parametrize(
    "text1,text2,expected",
    [
        ("Καλημέρα", "καλημέρα", True),
        ("Καλημέρα", "καλημερα", True),
        ("Καλησπέρα", "ΚΑΛΗΣΠΕΡΑ", True),
        ("Καληνύχτα", "καληνυχτα", True),
        ("Άνθρωπος", "ΑΝΘΡΩΠΟΣ", True),
        ("Ελλάδα", "ΕΛΛΑΔΑ", True),
        ("Ήλιος", "ΗΛΙΟΣ", True),
        ("Ίριδα", "ΙΡΙΔΑ", True),
        ("Ϊκαρος", "ΙΚΑΡΟΣ", True),
        ("Όμορφος", "ΟΜΟΡΦΟΣ", True),
        ("Ύμνος", "ΥΜΝΟΣ", True),
        ("Ϋδρογόνο", "ΥΔΡΟΓΟΝΟ", True),
        ("Ώρα", "ΩΡά", True),
        ("Δοϊράνη special", "ΔΟΙΡΑΝΗ SPECIAL", True),
        ("Καλημέρα", "Καλησπέρα", False),
        ("Hello", "World", False),
    ],
)
def test_is_text_same(text1, text2, expected):
    assert are_texts_equal(text1, text2) == expected
