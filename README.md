![Logo](images/parsy-logo.png)

![CI](https://github.com/github/docs/actions/workflows/main.yml/badge.svg)

# Parsy

Parsy is a HTML parsing library using YAML definition files. The idea is to use the YAML file as
sort of intent - what you want to have as a result and let Parsy do the heavy lifting for you.

The YAML files contain:
- The desired structure of the output
- XPath variants of the parsed items

## Features

- YAML File definitions
- Intent instead of coding
- support for XPath and Regex
- Different output formats e.g. JSON, YAML, XML, Avro

## Installation

Using pip:
```shell
pip install parsy
```


## Running Tests

To run tests, run the following command

```bash
  poetry run pytest
```

## Examples

## Documentation

[Documentation](https://parsy.readthedocs.com) (hopefuly some day)

## Acknowledgements

 - [selectorlib](https://selectorlib.com/) - It is the main inspiration for this project
 - [Scrapy](https://scrapy.org/) - One of the best crawling libraries for Python
 - [Tiangolo](https://tiangolo.com/projects) - His projects are real inspiration to produce great software


## Contributing

