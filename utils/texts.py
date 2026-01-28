import unicodedata


def grup(text: str) -> str:
    """A function who returns the characters capitalized. Specal Greek characters are handled in order to make string comparisons"""
    # Normalize to NFD (decomposed form) to separate base characters from combining diacritics
    normalized_text = unicodedata.normalize("NFD", text)
    # Remove combining diacritical marks
    text_without_marks = "".join(
        char
        for char in normalized_text
        if unicodedata.category(char) != "Mn"  # Mn = Mark, nonspacing (combining marks)
    )
    uptext = text_without_marks.upper()
    replaces = {
        "Ά": "Α",
        "Έ": "Ε",
        "Ή": "Η",
        "Ί": "Ι",
        "Ϊ": "Ι",
        "Ό": "Ο",
        "Ϋ": "Υ",
        "Ύ": "Υ",
        "Ώ": "Ω",
    }
    return "".join(replaces.get(letter, letter) for letter in uptext)


def are_texts_equal(text1: str, text2: str) -> bool:
    """A function who compares two strings in a case insensitive way, handling special Greek characters"""
    return grup(text1) == grup(text2)
