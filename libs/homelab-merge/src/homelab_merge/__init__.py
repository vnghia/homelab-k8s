from typing import Any


def merge(lhs: Any, rhs: Any) -> Any:
    if isinstance(lhs, dict) and isinstance(rhs, dict):
        result: dict[Any, Any] = lhs
        for rkey, rvalue in rhs.items():
            if isinstance(rkey, str):
                if rkey.startswith("-"):
                    key = rkey[1:]
                    result.pop(key, None)
                    continue
                if rkey.startswith("!"):
                    key = rkey[1:]
                    result[key] = merge({}, rvalue)
                    continue
                if rkey.startswith("~"):
                    key = rkey[1:]
                    result[key] = (
                        merge(rvalue, result.get(key, {}))
                        if (key in result) or isinstance(rvalue, dict)
                        else rvalue
                    )
                    continue
            if rkey in result:
                result[rkey] = merge(result[rkey], rvalue)
            else:
                result[rkey] = rvalue
        return result
    if isinstance(lhs, list) and isinstance(rhs, list):
        return lhs + rhs
    return rhs
