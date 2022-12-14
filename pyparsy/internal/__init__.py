from typing import Dict

from pyparsy.enum_types import SelectorType, ReturnType


class Definition:

    __slots__ = (
        "field",
        "selector_type",
        "return_type",
        "multiple",
        "xpath",
        "regex",
        "css",
        "children",
    )

    def __init__(self, field: str, definition: dict):
        self.field: str = field
        self.selector_type: SelectorType = SelectorType[definition.get("selector_type")]
        self.return_type: ReturnType = ReturnType[definition.get("return_type")]
        self.multiple: bool = definition.get("multiple", False)
        self.xpath = None
        self.css = None
        self.regex = None
        if self.selector_type.XPATH:
            self.xpath = definition.get("selector")
        if self.selector_type.REGEX:
            self.regex = definition.get("selector")
        if self.selector_type.CSS:
            self.css = definition.get("selector")
        self.children: Dict[str, Definition] = {
            _field: self.__class__(_field, _definitions)
            for _field, _definitions in definition.get("children", {}).items()
        }
