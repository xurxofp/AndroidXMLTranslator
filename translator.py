# -*- coding: utf-8 -*-

import os
import re
import argparse
import xml.etree.ElementTree as ElementTree
from googletrans import Translator

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser()
parser.add_argument("inFile", help="Imput file XML")
parser.add_argument("inLang", help="Original file language")
parser.add_argument("-l","--lang", action="append", help="Output file language/s (example: -l es -l en)")

parser.add_argument("-a", "--all", type=str2bool, nargs="?", const=True, default=False, help="Select all output languages")
#parser.add_argument("-s", "--safe", type=float, default=0, help="Safe mode (add delay of x seconds between requests)")

parser.add_argument("--list", type=str2bool, nargs="?", const=True, default=False ,help="Return all Google Translate languages")
parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.8.1")

args = parser.parse_args()

LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
    'fil': 'Filipino',
    'he': 'Hebrew'
}

if args.list:
    #print(list(LANGUAGES.keys()))
    print(LANGUAGES)

def create_directory_if_not_exists(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

def create_directories(dir_language):
    create_directory_if_not_exists("translated")

    file_directory = "translated/" + "values-" + dir_language

    create_directory_if_not_exists(file_directory)
    return file_directory

languages_to_translate = []
if args.all:
    languages_to_translate = list(LANGUAGES.keys())
elif args.lang is not None:
    for value in args.lang:
        if value is not None:
            languages_to_translate.append(value)
else:
    raise argparse.ArgumentTypeError('Output language required.')

translator = Translator()
for language_name in languages_to_translate:
    language_to_translate = language_name.strip()

    translated_file_directory = create_directories(language_to_translate)
    print(" -> " + language_to_translate + " =========================")

    tree = ElementTree.parse(args.inFile)
    root = tree.getroot()

    textToSplit = []
    for i in range(len(root)):
        if 'translatable' not in root[i].attrib:
            value = root[i].text
            if value is not None:
                output = re.compile("(\\\.)").split(value)
                textToSplit.append(output)

    textToTranslate = ""
    translatedText = ""
    x = 0
    for line in textToSplit:
        if (len(textToTranslate) > 2500):
            print("Translating group of " + str(len(textToTranslate)) + " characters")
            translatedText += translator.translate(textToTranslate, language_to_translate).text
            translatedText += "\n"           
            textToTranslate = ""
            
        even = True
        for i in range(len(line)):
            if even:
                textToTranslate += line[i] + "\t\n"
                even = False
            else:
                textToTranslate += "¶\n"
                even = True

    print("Translating last group of " + str(len(textToTranslate)) + " characters")
    translatedText += translator.translate(textToTranslate, language_to_translate).text 
    
    linesTranslated = translatedText.splitlines()

    i = 0
    k = 0
    outputText = ""
    while i < len(textToSplit):
        j = 0
        while j < len(textToSplit[i]):
            if j == 0:
                outputText = ""
            if linesTranslated[k] == "¶":
                outputText += textToSplit[i][j]
            else:
                outputText += linesTranslated[k]
            j += 1
            k += 1
        root[i].text = outputText
        i += 1

    translated_file = translated_file_directory + "/strings.xml"
    tree.write(translated_file, encoding='utf-8')

