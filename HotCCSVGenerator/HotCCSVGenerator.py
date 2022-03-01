from . import config
from bs4 import BeautifulSoup
import re
import requests
from typing import TypedDict


class Card(TypedDict):
    name: str
    translatedName: str
    cardNum: str
    rarity: str
    color: str
    side: str
    type: str
    level: int
    cost: int
    power: int
    soul: int
    traits: str
    triggers: str
    flavor: str
    text: str
    
    def __eq__(self, other:object) -> bool:
        if isinstance(other, Card):
            return self.name == other.name \
            and self.translatedName == other.translatedName \
            and self.cardNum == other.cardNum \
            and self.rarity == other.rarity \
            and self.color == other.color \
            and self.side == other.side \
            and self.character == other.character \
            and self.level == other.level \
            and self.cost == other.cost \
            and self.power == other.power \
            and self.soul == other.soul \
            and self.traits == other.traits \
            and self.triggers == other.triggers \
            and self.flavor == other.flavor \
            and self.text == other.text
        return False
        

      
def makeSoupFromFile(filepath):
    with open(filepath, "r", encoding=config.FILE_ENCODING) as file:
        soup = BeautifulSoup(file, "html.parser")
    return soup
    
def makeSoupFromWebpage(url):
    req = requests.get(url)
    return BeautifulSoup(req.text, "html.parser")


if __name__ == "__main__":
    pass 