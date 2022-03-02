from . import config
from bs4 import BeautifulSoup
import re
import requests
from typing import TypedDict, Dict
from pathlib import Path
import csv

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
            and self.type == other.type \
            and self.level == other.level \
            and self.cost == other.cost \
            and self.power == other.power \
            and self.soul == other.soul \
            and self.traits == other.traits \
            and self.triggers == other.triggers \
            and self.flavor == other.flavor \
            and self.text == other.text
        return False
        

      
def makeSoupFromFile(filepath: str):
    with open(filepath, "r", encoding=config.FILE_ENCODING) as file:
        soup = BeautifulSoup(file, "html.parser")
    return soup
    
def makeSoupFromWebpage(url: str):
    req = requests.get(url)
    return BeautifulSoup(req.text, "html.parser")
    
def extractAndFormatTextField(data: str)->str:
    """
    Use to extract the "TEXT" field from the card
    """    
    #first extract textline
    try:
        textLine = data[data.index(config.TEXTLINE_STARTER)+len(config.TEXTLINE_STARTER):]
    except ValueError as exc:
        return None
    #create list to hold all the indexes of pattern that start a newline
    startIndexes = []
    for match in re.finditer(config.TEXTLINE_PATTERN, textLine):
        startIndexes.append(match.start())
        
    index = 0
    text = []
    while index < len(startIndexes) and len(startIndexes) > 1:
        #grab startIndex at locations index and index+1 and slice the string at those indexes
        t = textLine[startIndexes[index]:startIndexes[index+1]]
        text.append(t)
        index +=2
    if len(startIndexes) > 0:
        #slice the last line of text that wouldn't be added above
        text.append(textLine[startIndexes[len(startIndexes)-1]:])
    else:
        #no matches, so this line is different, just append it
        text.append(textLine)
    text = [item.replace(config.NEWLINE_CHAR, "") for item in text]
    return config.NEWLINE_CHAR.join(text)
    
def extractDataFromLine(line: str, indexes: Dict[str, int])->Dict[str, str]:
    """
    Pass in a dict in the form {fieldName : indexWhenSplitByWhitespace}
    Extracts those indexes and returns dict in form {fieldName : textData}
    """
    #first split the line on whitespace
    splitLine = re.split(config.WHITESPACE_PATTERN, line)
    #now go through the dict and extract the indexes that you need
    result = {}
    for key in indexes:
        result[key] = splitLine[indexes[key]]
        
    return result

def getLinesFromSoup(soup: BeautifulSoup)->list[str]:
    """
    Extract the lines of data from Soup to turn into cards
    """
    text = soup.pre.text
    lines = re.split(config.PATTERN, text)
    skip = True
    result = []
    for dataLine in lines:
        if skip:
            #the first line is a dataline, ignore it
            skip = not skip
            continue
        result.append(dataLine.strip())
    del result[len(result)-1]
    return result
    
    
    
def writeCardsToCSVFile(filepath: Path, cardData: list[Card])->None:
    """
    Open a file and write a list of Cards to items
    """
    #open the file
    with open(filepath, "w", encoding=config.FILE_ENCODING, newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=config.CSV_WRITER_FIELDNAMES, delimiter=config.CSV_DELIMITER)
        writer.writeheader()
        for card in cardData:
            writer.writerow(card)
    return
    
    


if __name__ == "__main__":
    pass 