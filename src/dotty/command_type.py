from enum import Enum, auto


class CommandType(Enum):
    CONTAINS = auto()
    EXACT = auto()
    SUBSTITUTION = auto()
    STARTS_WITH = auto()
    UNSET = auto()
