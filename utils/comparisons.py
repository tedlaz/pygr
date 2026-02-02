# Dictionary mapping operators to their comparison functions
OPERATORS = {
    "=": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,
    "in": lambda a, b: a in b,
    "anyInList": lambda a, b: any(item in b for item in a),
    "allInList": lambda a, b: all(item in b for item in a),
    "not_anyInList": lambda a, b: all(item not in b for item in a),
    "not_allInList": lambda a, b: any(item not in b for item in a),
    "not_in": lambda a, b: a not in b,
    "contains": lambda a, b: b in a,
    "not_contains": lambda a, b: b not in a,
    "startsWith": lambda a, b: a.startswith(b),
    "endsWith": lambda a, b: a.endswith(b),
}


def compare_values(operator: str, value, criterion) -> bool:
    """Compare two values based on the given operator."""
    if operator not in OPERATORS:
        raise ValueError(f"Unsupported operator: {operator}")
    return OPERATORS[operator](value, criterion)


def has_attributes(attributes: list, cls: type) -> bool:
    """Check if the given class has all the specified attributes."""
    state = True
    valid_attrs = {f.name for f in cls.__dataclass_fields__.values()}
    for attr in attributes:
        if attr not in valid_attrs:
            print(f"Attribute '{attr}' does not exist in {cls.__name__} class.")
            state = False
    return state


def is_match(attributes: dict, class_instance: object) -> bool:
    """Check if the class instance matches all the given attribute conditions."""
    for key, op_val in attributes.items():
        operator, value = op_val
        attribute = getattr(class_instance, key)
        if compare_values(operator, attribute, value) is False:
            return False
    return True


def find(search_attributes: dict, cls: type, class_instances: list) -> list:
    """Find all class instances that match the given attribute conditions."""
    if not has_attributes(list(search_attributes.keys()), cls):
        return []
    return [obj for obj in class_instances if is_match(search_attributes, obj)]
