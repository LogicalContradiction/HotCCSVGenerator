from . import config
from bs4 import BeautifulSoup
import re
import requests


def makeSoupFromFile(filepath):
    with open(filepath, "r", encoding=config.FILE_ENCODING) as file:
        soup = BeautifulSoup(file, "html.parser")
    return soup
    
def makeSoupFromWebpage(url):
    req = requests.get(url)
    return BeautifulSoup(req.text, "html.parser")


if __name__ == "__main__":
    pass