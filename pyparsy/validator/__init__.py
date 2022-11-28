import re
from typing import Dict, Union

import lxml.etree
from schema import Schema, And, Use, Optional, Or

from pyparsy.enum_types import SelectorType
from pyparsy.exceptions import XPathValidationException, RegexValidationException

DEFINITION_SCHEMA = Schema({
    And("selector"): Or(str, list[str]),
    And("selector_type"): And(str, Use(str.upper),
                              lambda s: s in ("XPATH", "REGEX")),
    Optional("multiple"): And(bool),
    And("return_type"): And(str, Use(str.upper),
                            lambda s: s in ("INTEGER", "STRING", "FLOAT", "DOUBLE", "MAP")),
    Optional("children"): Or(dict, list)
})


class Validator:

    def __init__(self, yaml_def: Dict):
        self.yaml_def = yaml_def
        self.__validate_all()
        self.is_valid = True

    def __validate_all(self):
        for field, definitions in self.yaml_def.items():
            self.validate_schema(definitions)
            if SelectorType[definitions.get("selector_type")] == SelectorType.XPATH:
                self.validate_xpath(definitions.get("selector"), field)
            if SelectorType[definitions.get("selector_type")] == SelectorType.REGEX:
                self.validate_regex(definitions.get("selector"), field)

    def validate_schema(self, definitions: Dict):
        try:
            DEFINITION_SCHEMA.validate(definitions)
        except Exception as e:
            raise e

    def validate_xpath(self, xpath: Union[str, list[str]], field: str):
        try:
            if isinstance(xpath, str):
                lxml.etree.XPath(xpath)
            else:
                for path in xpath:
                    lxml.etree.XPath(path)
        except lxml.etree.XPathSyntaxError:
            raise XPathValidationException(field)

    def validate_regex(self, regex: str, field: str):
        try:
            re.compile(regex)
        except Exception:
            raise RegexValidationException(field)
