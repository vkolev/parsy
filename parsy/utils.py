import re
from decimal import Decimal

from typing import Optional


def __clean_string_number(given_string: str) -> str:
    number = re.sub(r"[^(\d,.)]", "", given_string)
    dot_position = number.find(".")
    comma_position = number.find(',')
    if comma_position > dot_position:
        number = number.replace('.', "")
        number = number.replace(",", ".")
    else:
        number = number.replace(",", "")
    return number


def extract_float(float_string: str) -> Optional[float]:
    if not float_string:
        return None
    return float(__clean_string_number(float_string))


def extract_decimal(decimal_string: str) -> Optional[Decimal]:
    if not decimal_string:
        return None
    return Decimal(__clean_string_number(decimal_string))


def extract_integer(integer_string: str) -> Optional[int]:
    if not integer_string:
        return None
    return int(re.sub(r"\D", "", integer_string))

