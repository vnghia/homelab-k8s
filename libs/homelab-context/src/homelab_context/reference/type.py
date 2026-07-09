from enum import StrEnum, auto


class Type(StrEnum):
    STR = auto()
    BOOL = auto()
    INT = auto()
    FLOAT = auto()


type PythonType = str | bool | int | float
