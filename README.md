# AndroidXMLTranslator
This is a Python script to translate your string.xml files for your Android projects with the Google Translate API.

## How to use
```
pip3 install -r requirements.txt
```

```
$ python3 translator.py -h
usage: translator.py [-h] [-l LANG] [-a [ALL]] [--list [LIST]] [-v] inFile inLang

positional arguments:
    inFile		Imput file XML
    inLang		Original file language

optional arguments:
    -h, --help		show this help message and exit
    -l, --lang		Output file language/s (example: -l es -l en)
    -a, --all		Select all output languages
    --list			Return all Google Translate languages
    -v, --version	Show program's version number and exit
```

## Features

 - Translate your strings to your selected language
 - Translate to multiple languages with various "-l" arguments (e.g. -l es -l en)

## TODO

 - Append new translations you your already existing files
 
## Credits
Credits to [Swisyn](https://github.com/Swisyn) whose [code](https://github.com/Swisyn/android-strings.xml-translator) inspired us to make this script
