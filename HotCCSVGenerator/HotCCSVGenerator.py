import config
from bs4 import BeautifulSoup
import re


def makeSoupFromFile(filepath):
    with open(filepath, "r", encoding=config.FILE_ENCODING) as file:
        soup = BeautifulSoup(file, "html.parser")
    return soup
    


if __name__ == "__main__":
    pass