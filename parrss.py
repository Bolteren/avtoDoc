import requests
from bs4 import BeautifulSoup
import codecs
import pandas as pd


def clear_file():
    inputFile = codecs.open('Report.htm', 'r')
    outputFile = open('temp.htm', 'w')
    for i in range(1, 119):
        next(inputFile)
    while True:
        try:
            words = inputFile.readline()
        except Exception:
            next(inputFile)
            words = inputFile.readline()
        outputFile.write(words)
        if not words:
            break
    inputFile.close()
    outputFile.close()


def parse_ssr():
    f = open('temp.htm', 'r')
    html = f.read()
    lst = html.split('\n')
    print(lst)


if __name__ == '__main__':
    clear_file()
    parse_ssr()
