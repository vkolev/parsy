from parsy import Parsy


def test_amazon_bestseller_de():
    parser = Parsy("tests/assets/amazon_bestseller_de.yaml")
    with open("tests/assets/amazon_bestseller_de.html") as file:
        result = parser.parse(html_string=file.read())
        assert "Bestseller in Elektronik & Foto" == result.get("title")
        assert 1 == result.get("page")
        assert isinstance(result.get("products"), list)
        assert 30 == len(result.get("products"))


def test_amazon_com():
    parser = Parsy("tests/assets/amazon_com.yaml")
    with open("tests/assets/amazon_com.html") as file:
        result = parser.parse(html_string=file.read())
        assert "Best Sellers in Tools & Home Improvement" == result.get("title")
        assert 1 == result.get("page")
        assert isinstance(result.get("products"), list)
        assert 30 == len(result.get("products"))
