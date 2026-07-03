import functools
from enum import StrEnum, auto


class Mode(StrEnum):
    ENFORCE = auto()
    AUDIT = auto()
    WARN = auto()

    @functools.cached_property
    def label(self) -> str:
        return f"pod-security.kubernetes.io/{self}"


class Level(StrEnum):
    PRIVILEGED = auto()
    BASELINE = auto()
    RESTRICTED = auto()
