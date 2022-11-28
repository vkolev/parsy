from enum import Enum


class ReturnType(Enum):
    STRING = str
    INTEGER = int
    FLOAT = float
    BOOLEAN = bool
    MAP = dict


class SelectorType(Enum):
    XPATH = "xpath"
    REGEX = "regex"
