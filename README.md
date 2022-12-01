![Logo](https://raw.githubusercontent.com/vkolev/parsy/master/images/parsy-logo.png)

![CI](https://github.com/vkolev/parsy/actions/workflows/main.yml/badge.svg?branch=master) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyparsy) ![PyPI](https://img.shields.io/pypi/v/pyparsy)

# PyParsy

PyParsy is an HTML parsing library using YAML definition files. The idea is to use the YAML file as
sort of intent - what you want to have as a result and let Parsy do the heavy lifting for you. The
differences to other similar libraries (e.g. [selectorlib](https://selectorlib.com/)) is that it 
supports multiple version of selectors for a single field. This way you will not need to create a new 
yaml definition file for every change on a website.


The YAML files contain:
- The desired structure of the output
- XPath/CSS/Regex selectors for the element extraction
- Return type definition
- Optional children of the field

## Features

- [x] YAML File definitions
- [x] YAML File validation
- [x] Intent instead of coding
- [x] support for XPath, CSS and Regex selectors
- [ ] Different output formats e.g. JSON, YAML, XML
- [x] Somewhat opinionated
- [x] 99% coverage

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

## YAML Structure

- `<field_name>:` Field name is the top level of the yaml
  - `selector:` `<selector_definition>` - The Selector expression
  - `selector_type:` `<selector_type[XPATH, CSS, REGEX]>` - The type of the selector expression only in of `XPATH, CSS, REGEX`
  - `multiple:` `<true/flase>` *[Optional]* true - get all matching results as list, false - get first matching result
  - `return_type:` `<return_type[STRING, INTEGER, FLOAT, MAP]` - Desired return type on of `STRING, INTEGER, FLOAT or MAP`
  - `children:` `<list of definitions` *[Optional]* - used for `return_type: MAP`

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
Then we can use this definition in code:

```python
from pyparsy import Parsy
import httpx
import json


def main():
    parser = Parsy('tests/assets/amazon_bestseller_de.yaml')
    response = httpx.get("https://www.amazon.de/-/en/gp/bestsellers/ce-de/ref=zg_bs_nav_0")
    result = parser.parse(response.text)
    print(json.dumps(dict(result), indent=4))


if __name__ == "__main__":
    main()
```

Will result in:
```json
{
    "title": "Best Sellers in Electronics & Photo",
    "page": 1,
    "products": [
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/81ZnAYiX5sL._AC_UL300_SR300,200_.jpg",
            "title": "Amazon Basics High Power 1.5V AA Alkaline Batteries, Pack of 48 (Appearance May Vary)",
            "price": 19.12,
            "asin": "B00MNV8E0C",
            "reviews_count": 526202
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/71C3lbbeLsL._AC_UL300_SR300,200_.jpg",
            "title": "All-new Echo Dot (5th generation, 2022 release) smart speaker with Alexa | Charcoal",
            "price": 59.99,
            "asin": "B09B8X9RGM",
            "reviews_count": 760
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/811OG1FsNFL._AC_UL300_SR300,200_.jpg",
            "title": "Fire TV Stick with Alexa Voice Remote (includes TV controls) | HD streaming device",
            "price": 39.99,
            "asin": "B08C1KN5J2",
            "reviews_count": 92504
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/81FGpGF5kaL._AC_UL300_SR300,200_.jpg",
            "title": "Amazon Basics AA Industrial Alkaline Batteries, Pack of 40",
            "price": 11.78,
            "asin": "B07MLFBJG3",
            "reviews_count": 72375
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/61ymYQD3gaL._AC_UL300_SR300,200_.jpg",
            "title": "Fire TV Stick 4K with Alexa Voice Remote (includes TV controls)",
            "price": 59.99,
            "asin": "B08XW4FDJV",
            "reviews_count": 46503
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/61UV1sshWKL._AC_UL300_SR300,200_.jpg",
            "title": "Varta Lithium Button Cell Battery",
            "price": 3.29,
            "asin": "B00TYEL11K",
            "reviews_count": 62993
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/61bLsZejhPL._AC_UL300_SR300,200_.jpg",
            "title": "Instax Fujifilm Mini Instant Film, White, 2 x 10 Sheets (20 Sheets)",
            "price": 15.95,
            "asin": "B0000C73CQ",
            "reviews_count": 197326
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/71PTROtCLRL._AC_UL300_SR300,200_.jpg",
            "title": "2032 20 40 Cell Battery Silver",
            "price": 8.99,
            "asin": "B07CSZ575S",
            "reviews_count": 16096
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/51CDcTTd3-S._AC_UL300_SR300,200_.jpg",
            "title": "Apple AirTag, pack of 4",
            "price": 119.0,
            "asin": "B0935JRJ59",
            "reviews_count": 47525
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/71yf6yTNWSL._AC_UL300_SR300,200_.jpg",
            "title": "All-new Echo Dot (5th generation, 2022 release) smart speaker with clock and Alexa | Cloud Blue",
            "price": 69.99,
            "asin": "B09B8RVKGW",
            "reviews_count": 665
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/71EFiZtPjML._AC_UL300_SR300,200_.jpg",
            "title": "Duracell Plus C Baby Alkaline Batteries 1.5 V LR14 MN1400 Pack of 4",
            "price": 7.13,
            "asin": "B093C9FN7W",
            "reviews_count": 42466
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/51Z0FcUPmgL._AC_UL300_SR300,200_.jpg",
            "title": "ooono traffic alarm: Warns about speed cameras and hazards in road traffic in real time, automatically active after connection to smartphone via Bluetooth, data from Blitzer.de",
            "price": 49.95,
            "asin": "B07Q619ZKS",
            "reviews_count": 26587
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/71g8a2BcgRL._AC_UL300_SR300,200_.jpg",
            "title": "Fire TV Stick 4K Max streaming device, Wi-Fi 6, Alexa Voice Remote (includes TV controls)",
            "price": 64.99,
            "asin": "B08MT4MY9J",
            "reviews_count": 30523
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/81Tt3+NBcSL._AC_UL300_SR300,200_.jpg",
            "title": "KabelDirekt - 2m - 4K HDMI Cable (4K @120Hz & 4K @60Hz - Spectacular Ultra HD Experience - High Speed with Ethernet - HDMI 2.0/1.4, Blu-ray/PS4/PS5/Xbox Series X/Switch - Black",
            "price": 7.99,
            "asin": "B004BEMD5Q",
            "reviews_count": 125724
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/61a3VAbtpQL._AC_UL300_SR300,200_.jpg",
            "title": "Soundcore Life P2 Bluetooth Headphones, Wireless Earbuds with CVC 8.0 Noise Isolation for a Crystal Clear Sound Profile, 40-hour Battery Life, IPX7 Water Protection Class, for Work and Travel",
            "price": 23.99,
            "asin": "B07SJR6HL3",
            "reviews_count": 115557
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/41qfJN7dLhL._AC_UL300_SR300,200_.jpg",
            "title": "Fire TV Stick Lite mit Alexa-Sprachfernbedienung Lite (ohne TV-Steuerungstasten) | HD-Streamingger\u00e4t",
            "price": 29.99,
            "asin": "B091G3WT74",
            "reviews_count": 5601
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/41hX+2Es+vL._AC_UL300_SR300,200_.jpg",
            "title": "Echo Dot (3rd Gen) - Smart speaker with Alexa - Charcoal Fabric",
            "price": 49.99,
            "asin": "B07PHPXHQS",
            "reviews_count": 312374
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/71nnAxdMtkL._AC_UL300_SR300,200_.jpg",
            "title": "Pack of 40 AG13 LR44 1.5 V Alkaline Button Cell Batteries, Mercury-Free (357 / 357A / L1154 / A76 / GPA76)",
            "price": 6.99,
            "asin": "B079HZ6RQR",
            "reviews_count": 10692
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/418AP8pw3KL._AC_UL300_SR300,200_.jpg",
            "title": "EarPods with Lightning Connector",
            "price": 16.9,
            "asin": "B01M1EEPOB",
            "reviews_count": 22486
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/715i0StnSlS._AC_UL300_SR300,200_.jpg",
            "title": "Amazon Basics High Capacity AA Rechargeable 2400mAh Batteries Pre-Charged Pack of 12",
            "price": 21.94,
            "asin": "B07NWT6YLD",
            "reviews_count": 146981
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/61iYFNhtwHL._AC_UL300_SR300,200_.jpg",
            "title": "NEW'C tempered glass foil, protective foil for iPhone 11, iPhone XR, 2pcs., free from scratches, fingerprints and oil, 9H hardness, 0.33 mm ultra clear, screen protective foil for iPhone 11, iPhone XR",
            "price": 5.99,
            "asin": "B07NC8PWDM",
            "reviews_count": 76098
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/81Pd4ogDITL._AC_UL300_SR300,200_.jpg",
            "title": "LiCB CR2032 3V Lithium Button Cell Batteries CR 2032 Pack of 10",
            "price": 6.99,
            "asin": "B07P7V9SP7",
            "reviews_count": 10781
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/61MRw0Bun4L._AC_UL300_SR300,200_.jpg",
            "title": "Varta Ready2Use Rechargeable Battery, Pre-Charged AAA Micro Ni-Mh Battery, Pack of 4, 1000 mAh, Rechargeable without Memory Effect, Ready to Use",
            "price": 10.22,
            "asin": "B000IGW3JC",
            "reviews_count": 47147
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/61pBvlYVPxL._AC_UL300_SR300,200_.jpg",
            "title": "Amazon Basics - high-speed cable, Ultra HD HDMI 2.0, supports 3D formats, with audio return channel, 1.8 m",
            "price": 6.99,
            "asin": "B014I8SSD0",
            "reviews_count": 469788
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/71AwNMpA29L._AC_UL300_SR300,200_.jpg",
            "title": "Instax Mini 11 Camera",
            "price": 79.0,
            "asin": "B084S3Y6L1",
            "reviews_count": 14441
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/51hsq3bombL._AC_UL300_SR300,200_.jpg",
            "title": "Soundcore by Anker Life P2 Mini Bluetooth Headphones, In-Ear Headphones with 10 mm Audio Driver, Intense Bass, EQ, Bluetooth 5.2, 32 Hours Battery, Charging with USB-C, Minimalist Design (Night Black)",
            "price": 39.99,
            "asin": "B099DP3617",
            "reviews_count": 14245
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/61pUgAx+pPL._AC_UL300_SR300,200_.jpg",
            "title": "NEW'C Pack of 3 Tempered Protective Glass for iPhone 14, 13, 13 Pro (6.1 inches), Free from Scratches, 9H Hardness, HD Screen Protector, 0.33 mm Ultra Clear, Ultra Resistant",
            "price": 5.99,
            "asin": "B09F3P3DQD",
            "reviews_count": 10136
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/71fzcZQlbqS._AC_UL300_SR300,200_.jpg",
            "title": "Echo Show 5 | 2nd generation (2021 release), smart display with Alexa and 2 MP camera | Charcoal",
            "price": 84.99,
            "asin": "B08KH2MTSS",
            "reviews_count": 22944
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/81Jz6OogtbL._AC_UL300_SR300,200_.jpg",
            "title": "Misxi hard case with glass screen protector compatible with Apple Watch Series 6 / SE / Series 5 / Series 4 44 mm, pack of 2",
            "price": 10.99,
            "asin": "B07ZRMCRG7",
            "reviews_count": 28111
        },
        {
            "image": "https://images-eu.ssl-images-amazon.com/images/I/71gG2vN8FFS._AC_UL300_SR300,200_.jpg",
            "title": "Duracell Plus AAA Micro Alkaline Batteries 1.5 V LR03 MN2400 Pack of 12",
            "price": 6.99,
            "asin": "B093LT2N4Q",
            "reviews_count": 20307
        }
    ]
}

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

[Documentation](https://pyparsy.readthedocs.com) (hopefuly some day)

## Acknowledgements

 - [selectorlib](https://selectorlib.com/) - It is the main inspiration for this project
 - [Scrapy](https://scrapy.org/) - One of the best crawling libraries for Python
 - [parsel](https://github.com/scrapy/parsel) - Scrapy parsing library is heavily used in this project and can be considered main dependency.
 - [schema](https://github.com/keleshev/schema) - Used for validating the YAML file schema

## Contributing

Contributions are very much welcome. Just create your Pull request with enough tests.
