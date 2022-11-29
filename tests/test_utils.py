from decimal import Decimal

import pytest

from pyparsy import extract_float, extract_integer
from pyparsy.utils import extract_decimal


@pytest.mark.parametrize("input_string,expected",
                         [("13,44 €", 13.44),
                          ("56.65EUR", 56.65),
                          ("test 12,99", 12.99),
                          (None, None)])
def test_extract_float(input_string, expected):
    assert extract_float(input_string) == expected


@pytest.mark.parametrize("input_string,expected",
                         [("test123", 123),
                          ("543,231 reviews", 543231),
                          (None, None)])
def test_extract_integer(input_string, expected):
    assert extract_integer(input_string) == expected


@pytest.mark.parametrize("input_string,expected",
                         [("13,44 €", Decimal("13.44")),
                          ("56.65EUR", Decimal("56.65")),
                          ("test 12,99", Decimal("12.99")),
                          (None, None)])
def test_extract_decimal(input_string, expected):
    assert extract_decimal(input_string) == expected
