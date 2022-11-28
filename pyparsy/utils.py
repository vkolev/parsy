import re
from decimal import Decimal

from typing import Optional


def __clean_string_number(given_string: str) -> str:
    """
    Format the given string to a numbered floating point string without using locales.

    :param given_string: string containing floating point number
    :return: str
    """
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
    """
    Extract floating point number from string

    :param float_string: string containing floating point number
    :return: float or None
    """
    if not float_string:
        return None
    return float(__clean_string_number(float_string))


def extract_decimal(decimal_string: str) -> Optional[Decimal]:
    """
    Extract Decimal from string

    :param decimal_string: string containing decimal
    :return: Decimal or None
    """
    if not decimal_string:
        return None
    return Decimal(__clean_string_number(decimal_string))


def extract_integer(integer_string: str) -> Optional[int]:
    """
    Extract single integer from string

    :param integer_string: string containing integer
    :return: int or None
    """
    if not integer_string:
        return None
    return int(re.sub(r"\D", "", integer_string))

