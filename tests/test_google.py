from pathlib import Path

from pyparsy import Parsy


def test_google_search_results():
    parser = Parsy.from_file(Path("tests/assets/google_com.yaml"))
    with open("tests/assets/google_com.html") as file:
        result = parser.parse(file.read())
        assert "test" == result.get("search_term")
        assert 9 == len(result.get("results"))
