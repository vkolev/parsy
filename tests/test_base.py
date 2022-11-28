from typing import Dict

import pytest
from schema import SchemaError

from parsy import YamlFileNotFound, Parsy, Definition
from parsy.enum_types import ReturnType, SelectorType
from parsy.exceptions import XPathValidationException, RegexValidationException


def test_initialization_raises_not_found():
    with pytest.raises(YamlFileNotFound):
        parser = Parsy("some_file_that_doesn_exists.yaml")


def test_initialization_passes():
    parser = Parsy("assets/amazon_com.yaml", validate=False)
    assert "assets/amazon_com.yaml" == parser.yaml_path


def test_initialization_loaded():
    parser = Parsy("assets/base_test.yaml")
    assert isinstance(parser._definitions.get("title"), Dict)
    assert isinstance(parser._definitions.get("title").get("selector"), str)
    assert SelectorType.XPATH == SelectorType[parser._definitions.get("title").get("selector_type")]
    assert ReturnType.STRING == ReturnType[parser._definitions.get("title").get("return_type")]
    assert not parser._definitions.get("title").get("multiple")


def test_validate_yaml_file():
    parser = Parsy("assets/base_test.yaml")
    assert isinstance(parser.field_selectors, Dict)
    assert isinstance(parser.field_selectors.get("title"), Definition)
    assert parser.field_selectors.get("title").selector_type == SelectorType.XPATH
    assert parser.field_selectors.get("title").return_type == ReturnType.STRING
    assert not parser.field_selectors.get("title").multiple
    assert isinstance(parser.field_selectors.get("subtitle_versions").xpath, list)
    assert isinstance(parser.field_selectors.get("components").children, dict)
    assert isinstance(parser.field_selectors.get("components").children.get("link"), Definition)


def test_invalid_xpath():
    with pytest.raises(XPathValidationException):
        parser = Parsy("assets/invalid/invalid_xpath.yaml")


def test_invalid_regex():
    with pytest.raises(RegexValidationException):
        parser = Parsy("assets/invalid/invalid_regex.yaml")


def test_invalid_schema():
    with pytest.raises(SchemaError):
        parser = Parsy("assets/invalid/invalid_schema.yaml")


