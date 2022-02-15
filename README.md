# JobScrapper
### A program that looks for specific Job Offerings on Stackoverflow, and writes them to a csv.
##### (Important: This script is still under development and may raise errors when executed.)
This tool is for personal use. Don't use it to spam Stackoverflow!

## Setting up

### Dependencies

To use this script, install Selenium with the following command:
```shell
pip3 install selenium
```
This script works with the **Firefox Web Browser**. Make sure you have the latest version installed.
You also have to download the **Webdriver** specifically for it.
Read Selenium's documentation for further instructions here: https://selenium-python.readthedocs.io/installation.html

## Usage

Type the following command to learn how to use this script:
```shell
python3 scrapper.py --help
```

Usage example:
```shell
python3 scrapper.py -k python -p 1
```

### Known Issues

The -p option currently only works if it is set to ```-p 1```. Multiple pages do not work yet.
