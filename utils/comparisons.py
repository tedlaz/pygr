def compare_values(operator: str, a, b) -> bool:
    """Compare two values based on the given operator."""
    if operator == "=":
        return a == b

    elif operator == "!=":
        return a != b

    elif operator == "<":
        return a < b

    elif operator == "<=":
        return a <= b

    elif operator == ">":
        return a > b

    elif operator == ">=":
        return a >= b

    elif operator == "in":
        return a in b

    elif operator == "any_in":
        return any(item in b for item in a)

    elif operator == "all_in":
        return all(item in b for item in a)

    elif operator == "not in":
        return a not in b

    elif operator == "contains":
        return b in a

    elif operator == "not contains":
        return b not in a

    elif operator == "starts with":
        return a.startswith(b)

    else:
        raise ValueError(f"Unsupported operator: {operator}")


def has_attributes(attributes: list, cls: type) -> bool:
    """Check if the given class has all the specified attributes."""
    state = True
    valid_attrs = {f.name for f in cls.__dataclass_fields__.values()}
    for attr in attributes:
        if attr not in valid_attrs:
            print(f"Attribute '{attr}' does not exist in {cls.__name__} class.")
            state = False
    return state
