import unittest

from hotCCSVGenerator import hotCCSVGenerator

data = {"name": "ボブ",
        "translatedName": "Bob",
        "cardNum": "AA/Z00-069 ZZ",
        "rarity": "ZZ",
        "color": "purple",
        "side": "W",
        "type": "character",
        "level": 42,
        "cost": 500,
        "power": 0,
        "soul": 22,
        "traits": "magic (mag), wisdom (wis)",
        "triggers": "soul",
        "flavor": "flavor text goes here",
        "text": "When that happens, do the other thing."
        }

class HotCCSVGeneratorTest(unittest.TestCase):
    
    def test_Card_Object_Creation(self):
        global data
        card = hotCCSVGenerator.Card(data)
        
        self.assertEqual(card["name"],data["name"])
        self.assertEqual(card["translatedName"],data["translatedName"])
        self.assertEqual(card["cardNum"],data["cardNum"])
        self.assertEqual(card["rarity"],data["rarity"])
        self.assertEqual(card["color"],data["color"])
        self.assertEqual(card["side"],data["side"])
        self.assertEqual(card["type"],data["type"])
        self.assertEqual(card["level"],data["level"])
        self.assertEqual(card["cost"],data["cost"])
        self.assertEqual(card["power"],data["power"])
        self.assertEqual(card["soul"],data["soul"])
        self.assertEqual(card["traits"],data["traits"])
        self.assertEqual(card["triggers"],data["triggers"])
        self.assertEqual(card["flavor"],data["flavor"])
        self.assertEqual(card["text"],data["text"])
        
    def test_Card_Object_eq(self):
        global data
        card1 = hotCCSVGenerator.Card(data)
        card2 = hotCCSVGenerator.Card(data)
        self.assertEqual(card1, card2, "Made with the same data, should be the same.")
        
    

if __name__ == "__main__":
    unittest.main()