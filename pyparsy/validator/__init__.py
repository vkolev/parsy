import re
from typing import Dict, Union

import lxml.etree
from schema import Schema, And, Use, Optional, Or

from pyparsy.enum_types import SelectorType
from pyparsy.exceptions import XPathValidationException, RegexValidationException

DEFINITION_SCHEMA = Schema(
    {
        And("selector"): Or(str, list[str]),
        And("selector_type"): And(
            str, Use(str.upper), lambda s: s in ("XPATH", "REGEX", "CSS")
        ),
        Optional("multiple"): And(bool),
        And("return_type"): And(
            str,
            Use(str.upper),
            lambda s: s in ("INTEGER", "STRING", "FLOAT", "DOUBLE", "MAP"),
        ),
        Optional("children"): Or(dict, list),
    }
)


class Validator:
    def __init__(self, yaml_def: Dict):
        self.yaml_def = yaml_def
        self.__validate_all()

    def __validate_all(self):
        """
        Internal method to validate the schema and Xpath/CSS/Regex selector expression

        :raises: SchemaError / XPathValidationException / RegexValidationException / CSSValidationException
        """
        for field, definitions in self.yaml_def.items():
            self.validate_schema(definitions)
            if SelectorType[definitions.get("selector_type")] == SelectorType.XPATH:
                self.validate_xpath(definitions.get("selector"), field)
            if SelectorType[definitions.get("selector_type")] == SelectorType.REGEX:
                self.validate_regex(definitions.get("selector"), field)

    def validate_schema(self, definitions: Dict):
        """
        Validates the schema of the field definitions

        :param definitions:
        :return:
        :raises: SchemaError
        """
        try:
            DEFINITION_SCHEMA.validate(definitions)
        except Exception as e:
            raise e

    def validate_xpath(self, xpath: Union[str, list[str]], field: str):
        """
        Validates xpath expression in definition

        :param xpath: XPath expression
        :param field: field
        :raises: XPathValidationException
        """
        try:
            if isinstance(xpath, str):
                lxml.etree.XPath(xpath)
            else:
                for path in xpath:
                    lxml.etree.XPath(path)
        except lxml.etree.XPathSyntaxError:
            raise XPathValidationException(field)

    def validate_regex(self, regex: str, field: str):
        """
        Validates the regex expression in definition

        :param regex: Regex expression
        :param field: field
        :raises: RegexValidationException
        """
        try:
            if isinstance(regex, str):
                re.compile(regex)
            else:
                for reg in regex:
                    re.compile(reg)
        except Exception:
            raise RegexValidationException(field)
