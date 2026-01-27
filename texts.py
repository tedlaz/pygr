def grup(text: str) -> str:
    """A function who returns the characters capitalized. Specal Greek characters are handled in order to make string comparisons"""
    uptext = text.upper()
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


def is_text_same(text1: str, text2: str) -> bool:
    """A function who compares two strings in a case insensitive way, handling special Greek characters"""
    return grup(text1) == grup(text2)
