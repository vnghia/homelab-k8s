from typing import Any

import pytest

from homelab_merge import merge


@pytest.mark.parametrize(
    "lhs, rhs, result",
    [
        ("a", 0, 0),
        (["a", "b"], [0, 1], ["a", "b", 0, 1]),
        ({"user": ["a", "b"]}, {"user": [0, 1]}, {"user": ["a", "b", 0, 1]}),
        ({"user": "a"}, {"age": 0}, {"user": "a", "age": 0}),
        ({"user": "a"}, {"user": 0}, {"user": 0}),
        (
            {"user": {"age": 10, "address": "home", "phone": 1}, "origin": "A"},
            {"user": {"address": "work", "phone": 2, "company": "example"}},
            {
                "user": {
                    "age": 10,
                    "address": "work",
                    "phone": 2,
                    "company": "example",
                },
                "origin": "A",
            },
        ),
        (
            {None: {"age": 10, "address": "home"}},
            {"user": {"company": "example"}},
            {
                None: {"age": 10, "address": "home"},
                "user": {"company": "example"},
            },
        ),
        (
            {"user": {"age": 10, "address": "home"}},
            {"user": {"-age": None, "company": "example"}},
            {
                "user": {"address": "home", "company": "example"},
            },
        ),
        ({"user": ["a", "b"]}, {"!user": [0, 1]}, {"user": [0, 1]}),
        (
            {"user": {"name": "a", "phone": 1}},
            {"!user": {"age": 1, "address": "home"}},
            {"user": {"age": 1, "address": "home"}},
        ),
        (
            {"user": {"age": 10, "address": "home"}},
            {"!user": {"-age": None, "company": "example"}},
            {
                "user": {"company": "example"},
            },
        ),
        ({"user": ["a", "b"]}, {"~user": [0, 1]}, {"user": [0, 1, "a", "b"]}),
        ({"company": {}}, {"~user": [0, 1]}, {"user": [0, 1], "company": {}}),
    ],
)
def test_merge(lhs: Any, rhs: Any, result: Any) -> None:
    assert merge(lhs, rhs) == result
