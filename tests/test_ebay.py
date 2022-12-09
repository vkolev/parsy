from pathlib import Path

from pyparsy import Parsy


def test_ebay_de():
    parser = Parsy.from_file(Path("tests/assets/ebay_de.yaml"))
    with open("tests/assets/ebay_de.html") as file:
        result = parser.parse(file.read())
        assert "apple" == result.get("search_term")
        assert 1 == result.get("page")
        assert 64 == len(result.get("products"))
