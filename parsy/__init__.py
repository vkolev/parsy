import os

import yaml
from yaml import SafeLoader

from parsy.exceptions import YamlFileNotFound
from parsy.enum_types import ReturnType
from parsy.internal import Definition
from parsy.validator import Validator


class Parsy:

    def __init__(self, yaml_path: str = None, validate: bool = True):
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
        self.html_string = html_string
        print("Parsing...")

    def get_xpath(self, xpath: str, return_type: ReturnType):
        pass


