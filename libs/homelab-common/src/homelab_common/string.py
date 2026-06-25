def add_prefix(prefix: str | None, value: str, *, separator: str = "-") -> str:
    if prefix:
        return prefix + separator + value
    return value


def add_suffix(value: str, suffix: str | None, *, separator: str = "-") -> str:
    if suffix:
        return value + separator + suffix
    return value
