from pyparsy import Definition, ReturnType, SelectorType


def test_definition_initialization():
    definition = Definition("test", {
          "selector": "//input[@name=\"q\"]/@value",
          "selector_type": "XPATH",
          "return_type": "STRING"
    })
    assert definition.field == "test"
    assert definition.return_type == ReturnType.STRING
    assert definition.selector_type == SelectorType.XPATH


def test_definition_with_children():
    definition = Definition("test", {
        "selector": "//input[@name=\"q\"]/@value",
        "selector_type": "XPATH",
        "return_type": "MAP",
        "children": {
            "test_child": {
                "selector": "//title[1]",
                "selector_type": "REGEX",
                "return_type": "INTEGER",
                "multiple": True
            }
        }
    })
    assert definition.field == "test"
    assert definition.return_type == ReturnType.MAP
    assert definition.selector_type == SelectorType.XPATH
    assert len(definition.children) == 1
    assert isinstance(definition.children.get("test_child"), Definition)
    child_def = definition.children.get("test_child")
    assert child_def.selector_type == SelectorType.REGEX
    assert child_def.return_type == ReturnType.INTEGER
    assert child_def.multiple
