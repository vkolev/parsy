from typing import Dict

import pytest
from schema import SchemaError

from pyparsy import YamlFileNotFound, Parsy, Definition
from pyparsy.enum_types import ReturnType, SelectorType
from pyparsy.exceptions import XPathValidationException, RegexValidationException


def test_initialization_raises_not_found():
    with pytest.raises(YamlFileNotFound):
        parser = Parsy("some_file_that_doesn_exists.yaml")


def test_initialization_passes():
    parser = Parsy("tests/assets/amazon_com.yaml", validate=False)
    assert "tests/assets/amazon_com.yaml" == parser.yaml_path


def test_initialization_loaded():
    parser = Parsy("tests/assets/base_test.yaml")
    assert isinstance(parser._definitions.get("title"), Dict)
    assert isinstance(parser._definitions.get("title").get("selector"), str)
    assert SelectorType.XPATH == SelectorType[parser._definitions.get("title").get("selector_type")]
    assert ReturnType.STRING == ReturnType[parser._definitions.get("title").get("return_type")]
    assert not parser._definitions.get("title").get("multiple")


def test_validate_yaml_file():
    parser = Parsy("tests/assets/base_test.yaml")
    assert isinstance(parser.field_selectors, Dict)
    assert isinstance(parser.field_selectors.get("title"), Definition)
    assert parser.field_selectors.get("title").selector_type == SelectorType.XPATH
    assert parser.field_selectors.get("title").return_type == ReturnType.STRING
    assert not parser.field_selectors.get("title").multiple
    assert isinstance(parser.field_selectors.get("subtitle_versions").xpath, list)
    assert isinstance(parser.field_selectors.get("components").children, dict)
    assert isinstance(parser.field_selectors.get("components").children.get("link"), Definition)


def test_css_selector_field():
    parser = Parsy("tests/assets/base_test.yaml")
    assert isinstance(parser.field_selectors, Dict)
    assert parser.field_selectors.get("css_test").selector_type == SelectorType.CSS


def test_invalid_xpath():
    with pytest.raises(XPathValidationException):
        parser = Parsy("tests/assets/invalid/invalid_xpath.yaml")


def test_invalid_regex():
    with pytest.raises(RegexValidationException):
        parser = Parsy("tests/assets/invalid/invalid_regex.yaml")


def test_invalid_schema():
    with pytest.raises(SchemaError):
        parser = Parsy("tests/assets/invalid/invalid_schema.yaml")

#
# def test_invalid_css():
#     with pytest.raises(CSSValidationException):
#         parser = Parsy("tests/assets/invalid/invalid_css.yaml")


def test_base_html_parse():
    parser = Parsy("tests/assets/base_test.yaml", validate=False)
    with open("tests/assets/base_test.html") as file:
        result = parser.parse(file.read())
        assert result.get("title") == "Test 1 2 3"
        assert result.get("subtitle_versions") == "Subtitle"
        assert result.get("list_items") == ["Hello", "World"]
        assert result.get("css_test") == "CSS Test"
        assert result.get("image") == "https://raw.githubusercontent.com/vkolev/parsy/master/images/parsy-logo.png"
        assert result.get("re_test") == "re_test"
        assert isinstance(result.get("multiple_re"), list)
        assert result.get("components").get("link") == "https://github.com"
        assert result.get("components").get("count") == 1
        assert result.get("re_not_existing") is None
        assert result.get("re_multi_selector") == "re_test"





