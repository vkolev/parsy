import os
from collections import defaultdict
from typing import Any, Union

import yaml
from parsel import Selector, SelectorList
from yaml import SafeLoader

from pyparsy.exceptions import YamlFileNotFound
from pyparsy.enum_types import ReturnType, SelectorType
from pyparsy.internal import Definition
from pyparsy.utils import extract_float, extract_integer
from pyparsy.validator import Validator


class Parsy:

    def __init__(self, yaml_path: str = None, validate: bool = True):
        """
        Parsing class initializer

        :param yaml_path: path to YAML file containing definitions
        :param validate: bool - turn on/off yaml schema validation
        """
        self.yaml_path = yaml_path
        self._definitions = self.__load_definitions()
        if validate:
            self.__validate()
        self.field_selectors = self.__create_field_selectors()
        self.html_string = None

    def __load_definitions(self):
        if not os.path.exists(self.yaml_path):
            raise YamlFileNotFound(self.yaml_path)
        with open(self.yaml_path) as yaml_file:
            data = yaml.load(yaml_file, Loader=SafeLoader)
            return data

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
        Parse the whole html_string to a defaultdict

        :param html_string: HTML formated string
        :return: defaultdict()
        """
        result = defaultdict()
        html_data = Selector(html_string)
        for field, definition in self.field_selectors.items():
            if not definition.multiple:
                result[field] = self.parse_field(html_data, definition)
            else:
                result[field] = list(self.parse_filed_multiple(html_data, definition))
        return result

    def parse_field(self, html_data: Union[Selector, SelectorList], definition: Definition) -> Any:
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

    def parse_filed_multiple(self, html_data: Union[Selector, SelectorList], definition) -> Any:
        items = self._get_selector_data(html_data, definition).getall()
        for item in items:
            html_data = Selector(item)
            result = defaultdict()
            for field, field_definition in definition.children.items():
                result[field] = self.parse_field(html_data, field_definition)
            yield result

    def _get_selector_data(self, html_data: Selector, definition: Definition):
        if definition.selector_type == SelectorType.XPATH:
            return html_data.xpath(query=definition.xpath)
        return html_data.re(definition.regex)

    def _convert_to_type(self, html_data: Union[Selector, SelectorList], return_type: ReturnType):
        if return_type == ReturnType.STRING:
            return html_data.get()
        if return_type == ReturnType.INTEGER:
            return extract_integer(html_data.get())
        if return_type == ReturnType.FLOAT:
            return extract_float(html_data.get())
        if return_type == ReturnType.BOOLEAN:
            return html_data.get() is not None
        return None



