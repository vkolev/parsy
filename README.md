![Logo](https://raw.githubusercontent.com/vkolev/parsy/master/images/parsy-logo.png)

![CI](https://github.com/vkolev/parsy/actions/workflows/main.yml/badge.svg?branch=master) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyparsy) ![PyPI](https://img.shields.io/pypi/v/pyparsy)

# PyParsy

Parsy is a HTML parsing library using YAML definition files. The idea is to use the YAML file as
sort of intent - what you want to have as a result and let Parsy do the heavy lifting for you.

The YAML files contain:
- The desired structure of the output
- XPath variants of the parsed items

## Features

- YAML File definitions
- Intent instead of coding
- support for XPath and Regex
- Different output formats e.g. JSON, YAML, XML

## Installation

Using pip:
```shell
pip install pyparsy
```

## Running Tests

To run tests, run the following command

```bash
  poetry run pytest
```

## Examples

We can consider as an example the amazon bestseller page. First we define the .yaml definition file:

```yaml
title:
  selector: //div[contains(@class, "_card-title_")]/h1/text()
  selector_type: XPATH
  return_type: STRING
page:
  selector: //ul[contains(@class, "a-pagination")]/li[@class="a-selected"]/a/text()
  selector_type: XPATH
  return_type: INTEGER
products:
  selector: //div[@id="gridItemRoot"]
  selector_type: XPATH
  multiple: true
  return_type: MAP
  children:
    image:
      selector: //img[contains(@class, "a-dynamic-image")]/@src
      selector_type: XPATH
      return_type: STRING
    title:
      selector: //a[@class="a-link-normal"]/span/div/text()
      selector_type: XPATH
      return_type: STRING
    price:
      selector: //span[contains(@class, "a-color-price")]/span/text()
      selector_type: XPATH
      return_type: FLOAT
    asin:
      selector: //div[contains(@class, "sc-uncoverable-faceout")]/@id
      selector_type: XPATH
      return_type: STRING
    reviews_count:
      selector: //div[contains(@class, "sc-uncoverable-faceout")]/div/div/a/span/text()
      selector_type: XPATH
      return_type: INTEGER
```

For the example sake let's store the file as `amazon_bestseller.yaml`.

Then we can use the PyParsy library in out code:

```python
import httpx
from pyparsy import Parsy

def main():
    html = httpx.get("https://www.amazon.com/gp/bestsellers/hi/?ie=UTF8&ref_=sv_hg_1")
    parser = Parsy("amazon_bestseller.yaml")
    result = parser.parse(html.text)
    print(result)
    
if __name__ == "__main__":
    main()
```

For more examples please see the tests for the library.

## Documentation

[Documentation](https://parsy.readthedocs.com) (hopefuly some day)

## Acknowledgements

 - [selectorlib](https://selectorlib.com/) - It is the main inspiration for this project
 - [Scrapy](https://scrapy.org/) - One of the best crawling libraries for Python
 - [Tiangolo](https://tiangolo.com/projects) - His projects are real inspiration to produce great software


## Contributing

