class YamlFileNotFound(Exception):

    def __init__(self, yaml_path: str = ""):
        self.message = f"Path {yaml_path} not found."
        super().__init__(self.message)


class XPathValidationException(Exception):

    def __init__(self, field: str = ""):
        self.message = f"Invalid xpath expression for field: {field}"
        super().__init__(self.message)


class RegexValidationException(Exception):

    def __init__(self, field: str = ""):
        self.message = f"Invalid regex expression for field: {field}"
        super().__init__(self.message)
