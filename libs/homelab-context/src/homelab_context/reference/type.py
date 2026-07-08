from enum import StrEnum, auto


class Type(StrEnum):
    STR = auto()
    BOOL = auto()
    INT = auto()
    FLOAT = auto()


PythonType = str | bool | int | float
