from pathlib import Path

from pyparsy import Parsy


def test_amazon_bestseller_de():
    parser = Parsy.from_file(Path("tests/assets/amazon_bestseller_de.yaml"))
    with open("tests/assets/amazon_bestseller_de.html") as file:
        result = parser.parse(html_string=file.read())
        assert "Bestseller in Elektronik & Foto" == result.get("title")
        assert 1 == result.get("page")
        assert isinstance(result.get("products"), list)
        assert 30 == len(result.get("products"))


def test_amazon_com():
    parser = Parsy.from_file(Path("tests/assets/amazon_com.yaml"))
    with open("tests/assets/amazon_com.html") as file:
        result = parser.parse(html_string=file.read())
        assert "Best Sellers in Tools & Home Improvement" == result.get("title")
        assert 1 == result.get("page")
        assert isinstance(result.get("products"), list)
        assert 30 == len(result.get("products"))


def test_amazon_de_search():
    parser = Parsy.from_file(Path("tests/assets/amazon_de_search.yaml"), strip_strings=True)
    with open("tests/assets/amazon_de_search.html") as file:
        result = parser.parse(html_string=file.read())
        assert "katzenfutter" == result.get('search_query')
        assert 1 == result.get('current_page')
        assert "katzenfutter" in result.get('next_page_url')
        assert len(result.get('products')) == 60
        assert len(result.get('related_searches')) == 6
