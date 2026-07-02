from enum import StrEnum, auto


class Mode(StrEnum):
    ENFORCE = auto()
    AUDIT = auto()
    WARN = auto()


class Level(StrEnum):
    PRIVILEGED = auto()
    BASELINE = auto()
    RESTRICTED = auto()
