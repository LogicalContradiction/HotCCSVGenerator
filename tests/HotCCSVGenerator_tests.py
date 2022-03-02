import unittest
from pathlib import Path
from bs4 import BeautifulSoup

from hotCCSVGenerator import hotCCSVGenerator

dataOne = {"name": "ボブ",
        "translatedName": "Bob",
        "cardNum": "AA/Z00-069 ZZ",
        "rarity": "ZZ",
        "color": "purple",
        "side": "Weiss",
        "type": "Character",
        "level": 42,
        "cost": 500,
        "power": 0,
        "soul": 22,
        "traits": "magic (mag), wisdom (wis)",
        "triggers": "soul",
        "flavor": "flavor text goes here",
        "text": "[Z] When that thing happens, do the other thing.\n[A] According to all known laws of aviation, there is no way a bee should be\nable to fly. Its wings are too small to get its fat little body off the ground.\nYa like jazz?\n[Q] [(7) Discard everything] Do the other thing."
        }
        
dataTwo = {"name": "成歩堂 龍",
        "translatedName": "Phoenix Wright",
        "cardNum": "QQ/Z21-777 MM",
        "rarity": "MMM",
        "color": "Green",
        "side": "Weiss",
        "type": "Climax",
        "level": 69,
        "cost": 70,
        "power": 9001,
        "soul": 1,
        "traits": "intelligence (int), luck (lck)",
        "triggers": "Draw",
        "flavor": "",
        "text": "[D] COMBO [TOD] j.H., (s.S, j.M, j.H, vH)x2, DP.H, cr.H, ->H, QCB.M,\nQCF.L+M\n[X] 632146S, 5P, 5K, 5S, 5H, 5D, 5K, 5S, 632146H"
        }
strippedDataStr = """Phoenix Wright
成歩堂 龍
Card No.: QQ/Z21-777MM  Rarity: MM
Color: Green   Side: Weiss  Climax
Level: 69   Cost: 70   Power: 9001   Soul: 1
Traits: intelligence (int), luck (lck)
Triggers: Draw
Flavor: 
TEXT: [D] COMBO [TOD] j.H., (s.S, j.M, j.H, vH)x2, DP.H, cr.H, ->H, QCB.M, 
QCF.L+M
[X] 632146S, 5P, 5K, 5S, 5H, 5D, 5K, 5S, 632146H"""

strippedDataStrEmptyText = """Phoenix Wright
成歩堂 龍
Card No.: QQ/Z21-777MM  Rarity: MM
Color: Green   Side: Weiss  Climax
Level: 69   Cost: 70   Power: 9001   Soul: 1
Traits: intelligence (int), luck (lck)
Triggers: Draw
Flavor: 
TEXT: """

strippedDataStrOneText = """Phoenix Wright
成歩堂 龍
Card No.: QQ/Z21-777MM  Rarity: MM
Color: Green   Side: Weiss  Climax
Level: 69   Cost: 70   Power: 9001   Soul: 1
Traits: intelligence (int), luck (lck)
Triggers: Draw
Flavor: 
TEXT: [D] COMBO [TOD] j.H., (s.S, j.M, j.H, vH)x2, DP.H, cr.H, ->H, QCB.M, 
QCF.L+M"""

strippedDataStrNoText = """Phoenix Wright
成歩堂 龍
Card No.: QQ/Z21-777MM  Rarity: MM
Color: Green   Side: Weiss  Climax
Level: 69   Cost: 70   Power: 9001   Soul: 1
Traits: intelligence (int), luck (lck)
Triggers: Draw
Flavor: 
TEXT:"""

#TEST_FILE = pathlib.Path(__file__).parent.joinpath("/testData/testWebpage.html")
FILE_ENCODING = "utf8"

WEBPAGE_DATA_ONE = """Bob
ボブ
Card No.: AA/Z00-069ZZ  Rarity: ZZ
Color: purple   Side: Weiss  Character
Level: 42   Cost: 500   Power: 0   Soul: 22
Traits: magic (mag), wisdom (wis)
Triggers: soul
Flavor: flavor text goes here
TEXT: [Z] When that thing happens, do the other thing.
[A] According to all known laws of aviation, there is no way a bee should be
able to fly. Its wings are too small to get its fat little body off the ground.
Ya like jazz?
[Q] [(7) Discard everything] Do the other thing."""

WEBPAGE_DATA_TWO = """Phoenix Wright
成歩堂 龍
Card No.: QQ/Z21-777MM  Rarity: MMM
Color: Green   Side: Weiss  Climax
Level: 69   Cost: 70   Power: 9001   Soul: 1
Traits: intelligence (int), luck (lck)
Triggers: Draw
Flavor: 
TEXT: [D] COMBO [TOD] j.H., (s.S, j.M, j.H, vH)x2, DP.H, cr.H, ->H, QCB.M, 
QCF.L+M
[X] 632146S, 5P, 5K, 5S, 5H, 5D, 5K, 5S, 632146H"""


class HotCCSVGeneratorTest(unittest.TestCase):
    
    def test_Card_Object_Creation(self):
        global dataOne
        card = hotCCSVGenerator.Card(dataOne)
        
        self.assertEqual(card["name"],dataOne["name"])
        self.assertEqual(card["translatedName"],dataOne["translatedName"])
        self.assertEqual(card["cardNum"],dataOne["cardNum"])
        self.assertEqual(card["rarity"],dataOne["rarity"])
        self.assertEqual(card["color"],dataOne["color"])
        self.assertEqual(card["side"],dataOne["side"])
        self.assertEqual(card["type"],dataOne["type"])
        self.assertEqual(card["level"],dataOne["level"])
        self.assertEqual(card["cost"],dataOne["cost"])
        self.assertEqual(card["power"],dataOne["power"])
        self.assertEqual(card["soul"],dataOne["soul"])
        self.assertEqual(card["traits"],dataOne["traits"])
        self.assertEqual(card["triggers"],dataOne["triggers"])
        self.assertEqual(card["flavor"],dataOne["flavor"])
        self.assertEqual(card["text"],dataOne["text"])
        
    def test_Card_Object_eq(self):
        global dataOne
        card1 = hotCCSVGenerator.Card(dataOne)
        card2 = hotCCSVGenerator.Card(dataOne)
        self.assertEqual(card1, card2, "Made with the same data, should be the same.")
    
    def test_extractAndFormatTextField_MultipleTextLines(self):
        global strippedDataStr

        result = hotCCSVGenerator.extractAndFormatTextField(strippedDataStr)
        self.assertEqual(result, "[D] COMBO [TOD] j.H., (s.S, j.M, j.H, vH)x2, DP.H, cr.H, ->H, QCB.M, QCF.L+M\n[X] 632146S, 5P, 5K, 5S, 5H, 5D, 5K, 5S, 632146H",\
        "Make sure you didn't change strippedDataStr.")
        
    def test_extractAndFormatTextField_OneTextLine(self):
        global strippedDataStrOneText
        
        result = hotCCSVGenerator.extractAndFormatTextField(strippedDataStrOneText)
        self.assertEqual(result, "[D] COMBO [TOD] j.H., (s.S, j.M, j.H, vH)x2, DP.H, cr.H, ->H, QCB.M, QCF.L+M",\
        "Make sure you didn't change strippedDataStrOneText.")
    
    def test_extractAndFormatTextField_NoTextLine(self):
        global strippedDataStrNoText
        
        result = hotCCSVGenerator.extractAndFormatTextField(strippedDataStrNoText)
        self.assertEqual(result, None, "Result: %s\nMake sure you didn't change strippedDataStrNoText." % result)
    
    def test_extractAndFormatTextField_EmptyTextLines(self):
        global strippedDataStrEmptyText
        
        result = hotCCSVGenerator.extractAndFormatTextField(strippedDataStrEmptyText)
        self.assertEqual(result, "", "Make sure you didn't change strippedDataStrEmptyText.")
        
    def test_extractDataFromLine_TwoValues(self):
        line = "Card No.: QQ/Z21-777MM  Rarity: MM"
        dictionary = {"cardNum": 2,
                      "rarity": 4}
        result = hotCCSVGenerator.extractDataFromLine(line, dictionary)
        
        self.assertEqual(result["cardNum"], "QQ/Z21-777MM")
        self.assertEqual(result["rarity"], "MM")
        
    def test_extractDataFromLine_FourIntValues(self):
        line = "Level: 69   Cost: 70   Power: 9001   Soul: 1"
        dictionary = {"level": 1,
                      "cost": 3,
                      "power": 5,
                      "soul": 7}
        result = hotCCSVGenerator.extractDataFromLine(line, dictionary)          
        
        self.assertEqual(result["level"], "69")
        self.assertEqual(result["cost"], "70")
        self.assertEqual(result["power"], "9001")
        self.assertEqual(result["soul"], "1") 

    def test_getLinesFromSoup(self):
        TEST_FILE = Path(__file__).parent / "testData/testWebpage.html"
        global FILE_ENCODING
        global WEBPAGE_DATA_ONE
        global WEBPAGE_DATA_TWO
        with open(TEST_FILE, "r", encoding=FILE_ENCODING) as file:
            soup = BeautifulSoup(file, "html.parser")
        data = hotCCSVGenerator.getLinesFromSoup(soup)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0], WEBPAGE_DATA_ONE)
        self.assertEqual(data[1], WEBPAGE_DATA_TWO)
        
            
    

if __name__ == "__main__":
    unittest.main()