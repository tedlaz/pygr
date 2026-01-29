def compare_values(operator: str, a, b) -> bool:
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
