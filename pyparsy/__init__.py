from collections import defaultdict
from pathlib import Path
from typing import Any, Union, List

import yaml
from parsel import Selector, SelectorList
from yaml import SafeLoader

from pyparsy.exceptions import YamlFileNotFound
from pyparsy.enum_types import ReturnType, SelectorType
from pyparsy.internal import Definition
from pyparsy.utils import extract_float, extract_integer
from pyparsy.validator import Validator


class Parsy:
    def __init__(self, yaml_def: dict = None, validate: bool = True, strip_strings=False):
        """
        Parsing class initializer

        :param yaml_def: Yaml definition.
        :param validate: bool - turn on/off yaml schema validation
        """
        self._definitions = yaml_def
        if validate:
            self.__validate()
        self.field_selectors = self.__create_field_selectors()
        self.html_string = None
        self.strip_strings = strip_strings

    @classmethod
    def from_file(cls, yaml_file: Path, validate: bool = True, strip_strings=False):
        if yaml_file.is_file():
            stream = yaml_file.open()
            data = yaml.load(stream, Loader=SafeLoader)
            return cls(data, validate, strip_strings)
        raise YamlFileNotFound(yaml_file.name)

    @classmethod
    def from_string(cls, yaml_string: str, validate: bool = True, strip_strings=False):
        data = yaml.safe_load(yaml_string)
        return cls(data, validate, strip_strings)

    def __create_field_selectors(self):
        if self._definitions:
            result = {}
            for field, definitions in self._definitions.items():
                result[field] = Definition(field, definitions)
            return result

    def __validate(self):
        try:
            return Validator(self._definitions)
        except Exception as e:
            raise e

    def parse(self, html_string: str):
        """
        Parse the whole html_string to a default-dict

        :param html_string: HTML formatted string.
        :return: dictionary of the parsed data
        """
        result = defaultdict()
        html_data = Selector(html_string)
        for field, definition in self.field_selectors.items():
            if not definition.multiple:
                result[field] = self.parse_field(html_data, definition)
            else:
                result[field] = list(self.parse_filed_multiple(html_data, definition))
        return result

    def parse_field(
        self, html_data: Union[Selector, SelectorList], definition: Definition
    ) -> Any:
        """
        Extract field from html_data with given definition
        :param html_data: parsel.Selector with HTML data
        :param definition: pyparsy.internal.Definition
        :return: Any
        """
        if definition.return_type != ReturnType.MAP:
            data = self._get_selector_data(html_data, definition)
            return self._convert_to_type(data, return_type=definition.return_type)
        result = defaultdict()
        data = self._get_selector_data(html_data, definition)
        for child, child_definition in definition.children.items():
            result[child] = self.parse_field(data, child_definition)
        return result

    def parse_filed_multiple(
        self, html_data: Union[Selector, SelectorList], definition
    ) -> Any:
        if definition.selector_type == SelectorType.REGEX:
            items = self._get_selector_data(html_data, definition)
        else:
            items = self._get_selector_data(html_data, definition).getall()
        if definition.return_type == ReturnType.MAP:
            for item in items:
                html_data = Selector(item)
                result = defaultdict()
                for field, field_definition in definition.children.items():
                    result[field] = self.parse_field(html_data, field_definition)
                yield result
        else:
            for item in items:
                yield self._convert_to_type(item, definition.return_type)

    def _get_selector_data(self, html_data: Selector, definition: Definition):
        """
        Factory method to get the Selector from HTML based on the SelectorType

        :param html_data: Selector - `lxml.etree` HTML content
        :param definition: Definition - of the field
        :return: SelectorList - result of the selector query
        """
        if definition.selector_type == SelectorType.XPATH:
            return self.__get_xpath(html_data, definition.xpath)
        if definition.selector_type == SelectorType.REGEX:
            if definition.multiple:
                return self.__get_regex(html_data, definition.regex)
            else:
                try:
                    return self.__get_regex(html_data, definition.regex)[0]
                except IndexError:
                    return None
        if definition.selector_type == SelectorType.CSS:
            return self.__get_css(html_data, definition.css)

    @staticmethod
    def __get_xpath(html_data: Selector, selector: Union[str, List[str]]):
        result = None
        if isinstance(selector, list):
            for sel in selector:
                result = html_data.xpath(sel)
                if result:
                    break
        else:
            result = html_data.xpath(selector)
        return result

    @staticmethod
    def __get_regex(html_data: Selector, selector: Union[str, List[str]]):
        result = None
        if isinstance(selector, list):
            for sel in selector:
                result = html_data.re(sel)
                if result:
                    break
        else:
            result = html_data.re(selector)
        return result

    @staticmethod
    def __get_css(html_data: Selector, selector: Union[str, List[str]]):
        result = None
        if isinstance(selector, list):
            for sel in selector:
                result = html_data.css(sel)
                if result:
                    break
        else:
            result = html_data.css(selector)
        return result

    def _convert_to_type(self,
        html_data: Union[Selector, SelectorList, str], return_type: ReturnType
    ):
        """
        Convert the SelectorList/Selector data to a ReturnType format
        :param html_data: Selector/SelectorList HTML data
        :param return_type: ReturnType desired return type
        :return: data in desired type or None
        """
        try:
            data = html_data.get()
        except AttributeError:
            data = html_data
        if return_type == ReturnType.STRING:
            return data.strip() if self.strip_strings and data else data
        if return_type == ReturnType.INTEGER:
            return extract_integer(data.strip() if self.strip_strings and data else data)
        if return_type == ReturnType.FLOAT:
            return extract_float(data.strip() if self.strip_strings and data else data)
        if return_type == ReturnType.BOOLEAN:
            return data is not None
