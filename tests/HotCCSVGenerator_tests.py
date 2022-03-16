import unittest
from unittest.mock import mock_open, patch, call
from pathlib import Path
from bs4 import BeautifulSoup
import builtins
import requests
from datetime import datetime, timedelta

from hotCCSVGenerator import hotCCSVGenerator

dataOne = {"name": "ボブ",
        "translatedName": "Bob",
        "cardNum": "AA/Z00-069ZZ",
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
        "cardNum": "QQ/Z21-777MM",
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
TEST_DATA_ONE_NEWLINES_REMOVED = {"name": "ボブ",
                                  "translatedName": "Bob",
                                  "cardNum": "AA/Z00-069ZZ",
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
                                  "text": "[Z] When that thing happens, do the other thing.\n[A] According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. Ya like jazz?\n[Q] [(7) Discard everything] Do the other thing."
                                 } 
TEST_DATA_TWO_NEWLINES_REMOVED = {"name": "成歩堂 龍",
                                  "translatedName": "Phoenix Wright",
                                  "cardNum": "QQ/Z21-777MM",
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
                                  "text": "[D] COMBO [TOD] j.H., (s.S, j.M, j.H, vH)x2, DP.H, cr.H, ->H, QCB.M,QCF.L+M\n[X] 632146S, 5P, 5K, 5S, 5H, 5D, 5K, 5S, 632146H"
                                 }
                                 
TEST_CSV_HEADERS = ["name", 
                         "translatedName", 
                         "cardNum",
                         "rarity",
                         "color",
                         "side",
                         "type",
                         "level",
                         "cost",
                         "power",
                         "soul",
                         "traits",
                         "triggers",
                         "flavor",
                         "text"]                                 

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
        
        expectedResult = "[D] COMBO [TOD] j.H., (s.S, j.M, j.H, vH)x2, DP.H, cr.H, ->H, QCB.M, QCF.L+M\n[X] 632146S, 5P, 5K, 5S, 5H, 5D, 5K, 5S, 632146H"
        result = hotCCSVGenerator.extractAndFormatTextField(strippedDataStr)

        self.assertEqual(result, expectedResult, "Make sure you didn't change strippedDataStr.")
        
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
        global WEBPAGE_DATA_TWO
        line = WEBPAGE_DATA_TWO.split("\n")[2]
        dictionary = {"cardNum": 2,
                      "rarity": 4}
        result = hotCCSVGenerator.extractDataFromLine(line, dictionary)
        
        self.assertEqual(result["cardNum"], "QQ/Z21-777MM")
        self.assertEqual(result["rarity"], "MMM")
        
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
        
    def test_extractDataFromLine_OneElement(self):
        global WEBPAGE_DATA_TWO
        line = WEBPAGE_DATA_TWO.split("\n")[0]
        dictionary = {"name": None}
        
        result = hotCCSVGenerator.extractDataFromLine(line, dictionary)
        self.assertEqual(result["name"], "Phoenix Wright")

    def test_getLinesFromSoup(self):
        TEST_FILE = Path(__file__).parent / "testData/testWebpage.html"
        global FILE_ENCODING
        global WEBPAGE_DATA_ONE
        global WEBPAGE_DATA_TWO
        with open(TEST_FILE, "r", encoding=FILE_ENCODING) as file:
            soup = BeautifulSoup(file, "html.parser")
        data = hotCCSVGenerator.getLinesFromSoup(soup)
        self.assertEqual(len(data), 3)
        self.assertEqual(data[1], WEBPAGE_DATA_ONE)
        self.assertEqual(data[2], WEBPAGE_DATA_TWO)
        
    def test_writeCardsToCSVFile(self):
        TEST_FILE = Path(__file__).parent /"testData/testCSVFile.csv"
        global dataOne
        c = hotCCSVGenerator.Card(dataOne)
        cardData = [c]
        with patch('builtins.print') as mock_print:
            with patch('builtins.input', return_value='y') as mock_input:
                hotCCSVGenerator.writeCardsToCSVFile(TEST_FILE, cardData, True)
        self.assertEqual(0,0)
        
    def test_writeCardsToCSVFile_withMock(self):
        m = mock_open()
        global TEST_DATA_ONE_NEWLINES_REMOVED
        global TEST_CSV_HEADERS
        c = hotCCSVGenerator.Card(TEST_DATA_ONE_NEWLINES_REMOVED)
        cardData = [c]
        fakeFilepath = "testdir/testfile.csv"
        resultCSVHeaders = "\t".join(TEST_CSV_HEADERS) + "\r\n"
        calls = [call(resultCSVHeaders)]
        for card in cardData:
            r = []
            for key in card:
                if key == "text":
                    r.append("\"" + card[key] + "\"")
                else:
                    r.append(card[key])
            res = "\t".join(str(a) for a in r) + "\r\n"
            calls.append(call(res))
        
        with patch("builtins.open", m) as mockedFile:
            with patch('builtins.print') as mock_print:
                with patch('builtins.input', return_value='y') as mock_input:
                    hotCCSVGenerator.writeCardsToCSVFile(fakeFilepath, cardData, True)
            #assert if opened file on write mode "w"
            mockedFile.assert_called_once_with(fakeFilepath, "w", encoding="utf8", newline="")
            #assert if write cas called from the file opened with in the order and with the params of calls 
            mockedFile().write.assert_has_calls(calls)
            
    def test_makeCardFromData(self):
        self.maxDiff = None
        global TEST_DATA_ONE_NEWLINES_REMOVED
        global WEBPAGE_DATA_ONE
        
        resultStrFormat = "\nExpected {key}:\n{eValue}\nActual {key}:\n{aValue}\n"
        
        expectedCard = hotCCSVGenerator.Card(TEST_DATA_ONE_NEWLINES_REMOVED)
        resultCard = hotCCSVGenerator.makeCardFromData(WEBPAGE_DATA_ONE)
        resultStr = ""
        for key in resultCard:
            resultStr = resultStr + resultStrFormat.format(key=key, eValue=expectedCard[key], aValue=resultCard[key])
        
        self.assertEqual(expectedCard, resultCard, resultStr)
        
    def test_formatUrl_standardCase(self):
        setName = "Da Capo 10th Anniversary Mix"
        packType = "Trial Deck"
        expectedUrl = "https://www.heartofthecards.com/translations/da_capo_10th_anniversary_mix_trial_deck.html"
        
        resultUrl = hotCCSVGenerator.formatUrl(setName, packType)
        self.assertEqual(expectedUrl, resultUrl)
        
    def test_formatUrl_ColonAndApostPunctuation(self):
        setName = "Bofuri: I Don't Want to Get Hurt, so I'll Max Out My Defense"
        packType = "Booster Pack"
        expectedUrl = "https://www.heartofthecards.com/translations/bofuri-_i_don-t_want_to_get_hurt-_so_i-ll_max_out_my_defense_booster_pack.html"
        
        resultUrl = hotCCSVGenerator.formatUrl(setName, packType)
        self.assertEqual(expectedUrl, resultUrl)
        
    def test_formatUrl_AmpersandPunctuation(self):
        setName = "Angel Beats! & Kud Wafter"
        packType = "Trial Deck"
        expectedUrl = "https://www.heartofthecards.com/translations/angel_beats!_-_kud_wafter_trial_deck.html"
        
        resultUrl = hotCCSVGenerator.formatUrl(setName, packType)
        self.assertEqual(expectedUrl, resultUrl)
        
    def test_formatUrl_ForwardSlashPunctuation(self):
        setName = "Da Capo / Da Capo II"
        packType = "Booster Pack"
        expectedUrl = "https://www.heartofthecards.com/translations/da_capo_-_da_capo_ii_booster_pack.html"
        
        resultUrl = hotCCSVGenerator.formatUrl(setName, packType)
        self.assertEqual(expectedUrl, resultUrl)
        
    def test_formatUrl_QuestionMarkPunctuation(self):
        setName = "Is It Wrong to Try to Pick Up Girls in a Dungeon?"
        packType = "Booster Pack"
        expectedUrl = "https://www.heartofthecards.com/translations/is_it_wrong_to_try_to_pick_up_girls_in_a_dungeon_booster_pack.html"
        
        resultUrl = hotCCSVGenerator.formatUrl(setName, packType)
        self.assertEqual(expectedUrl, resultUrl)
        
    def test_formatUrl_ParenthesisPunctuation(self):
        setName = "Hatsune Miku Project Diva F (Vocaloid) 2nd"
        packType = "Booster Pack"
        expectedUrl = "https://www.heartofthecards.com/translations/hatsune_miku_project_diva_f_-vocaloid-_2nd_booster_pack.html"
        
        resultUrl = hotCCSVGenerator.formatUrl(setName, packType)
        self.assertEqual(expectedUrl, resultUrl)
        
    def test_formatUrl_DoubleQuestionmarkPunctuation(self):
        setName = "Is the Order a Rabbit?? Dear My Sister"
        packType = "Booster Pack"
        expectedUrl = "https://www.heartofthecards.com/translations/is_the_order_a_rabbit_dear_my_sister_booster_pack.html"
        
        resultUrl = hotCCSVGenerator.formatUrl(setName, packType)
        self.assertEqual(expectedUrl, resultUrl)

            
    def test_convertAPageToCards(self):
        self.masDiff = None
        testDataOne = {"name": "ボブ",
                                  "translatedName": "Bob",
                                  "cardNum": "AA/Z00-069ZZ",
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
                                  "text": "[Z] When that thing happens, do the other thing.\n[A] According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. Ya like jazz?\n[Q] [(7) Discard everything] Do the other thing."
                                 } 
        testDataTwo = {"name": "成歩堂 龍",
                                  "translatedName": "Phoenix Wright",
                                  "cardNum": "QQ/Z21-777MM",
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
                                  "text": "[D] COMBO [TOD] j.H., (s.S, j.M, j.H, vH)x2, DP.H, cr.H, ->H, QCB.M, QCF.L+M\n[X] 632146S, 5P, 5K, 5S, 5H, 5D, 5K, 5S, 632146H"
                                 }
        filepath = Path(__file__).parent /"testData/testWebpage.html"
        
        card1 = hotCCSVGenerator.Card(testDataOne)
        card2 = hotCCSVGenerator.Card(testDataTwo)
        expectedResult = [card1,card2]
        expectedFilename = "Fake_Deck_Translation"
        
        #for key in card1:
        #    print("\nkey:",key,"\neValue:",card1[key])
        actualResult, actualFilename = hotCCSVGenerator.convertAPageToCards(filepath)  
        self.assertEqual(expectedResult, actualResult)
        self.assertEqual(expectedFilename,actualFilename)
        
    def test_proccessCommandLineArgs_version(self):
        args = ["--version"]
        with self.assertRaises(SystemExit):
            hotCCSVGenerator.proccessCommandLineArgs(args)
    
    def test_processCommandLineArgs_url(self):
        args = ["url", "www.example.com"]
        expectedResult = {"mode": "url",
                          "url": "www.example.com",
                          "outputFilepath": None,
                          "verbose": False,
                          "quiet": False,
                          "abortOnError": False
                         }
        actualResult = hotCCSVGenerator.proccessCommandLineArgs(args)
        self.assertEqual(expectedResult, actualResult)
        
    def test_processCommandLineArgs_verbose(self):
        args = ["--verbose", "url", "www.thisDoesntMatter.com"]
        expectedResult = {"mode": "url",
                          "url": "www.thisDoesntMatter.com",
                          "outputFilepath": None,
                          "verbose": True,
                          "quiet": False,
                          "abortOnError": False
                         }
        actualResult = hotCCSVGenerator.proccessCommandLineArgs(args)
        self.assertEqual(expectedResult, actualResult)
        
    def test_processCommandLineArgs_verbose_character(self):
        args = ["-v", "url", "www.thisDoesntMatter.com"]
        expectedResult = {"mode": "url",
                          "url": "www.thisDoesntMatter.com",
                          "outputFilepath": None,
                          "verbose": True,
                          "quiet": False,
                          "abortOnError": False
                         }
        actualResult = hotCCSVGenerator.proccessCommandLineArgs(args)
        self.assertEqual(expectedResult, actualResult)
        
    def test_processCommandLineArgs_quiet_character(self):
        args = ["-q", "url", "www.thisDoesntMatter.com"]
        expectedResult = {"mode": "url",
                          "url": "www.thisDoesntMatter.com",
                          "outputFilepath": None,
                          "verbose": False,
                          "quiet": True,
                          "abortOnError": False
                         }
        actualResult = hotCCSVGenerator.proccessCommandLineArgs(args)
        self.assertEqual(expectedResult, actualResult)
        
    def test_processCommandLineArgs_quiet(self):
        args = ["--quiet", "url", "www.thisDoesntMatter.com"]
        expectedResult = {"mode": "url",
                          "url": "www.thisDoesntMatter.com",
                          "outputFilepath": None,
                          "verbose": False,
                          "quiet": True,
                          "abortOnError": False
                         }
        actualResult = hotCCSVGenerator.proccessCommandLineArgs(args)
        self.assertEqual(expectedResult, actualResult)
                          
        
    def test_processCommandLineArgs_filepath(self):
        args = ["filepath", "this/is/a/filepath.txt"]
        expectedResult = {"mode": "filepath",
                          "filepath": "this/is/a/filepath.txt",
                          "outputFilepath": None,
                          "verbose": False,
                          "quiet": False,
                          "abortOnError": False
                         }
        actualResult = hotCCSVGenerator.proccessCommandLineArgs(args)
        self.assertEqual(expectedResult, actualResult)
        
    def test_processCommandLineArgs_setNamePackType(self):
        args = ["name", "Symphogear XV", "booster pack"]
        expectedResult = {"mode": "name",
                          "setName": "Symphogear XV",
                          "packType": "booster pack",
                          "outputFilepath": None,
                          "verbose": False,
                          "quiet": False,
                          "abortOnError": False
                         }
        actualResult = hotCCSVGenerator.proccessCommandLineArgs(args)
        self.assertEqual(expectedResult, actualResult)
        
    def test_formatCommandLineArgs_NoQuotes(self):
        args = ["a", "cute", "owl", "eating", "berries", "with", "a", "clock"]
        expectedResult = args
        
        actualResult = hotCCSVGenerator.formatCommandLineArgs(args)
        self.assertEqual(expectedResult, actualResult)
        
    def test_formatCommandLineArgs_OneQuotedGroup(self):
        args = ["a", "\"cute", "owl", "eating", "berries\"", "with", "a", "clock"]
        expectedResult = ["a", "cute owl eating berries", "with", "a", "clock"]
        
        actualResult = hotCCSVGenerator.formatCommandLineArgs(args)
        self.assertEqual(expectedResult, actualResult)
        
    def test_formatCommandLineArgs_TwoQuotedGroup(self):
        args = ["a", "\"cute", "owl\"", "\"eating", "berries\"", "with", "a", "clock"]
        expectedResult = ["a", "cute owl", "eating berries", "with", "a", "clock"]
        
        actualResult = hotCCSVGenerator.formatCommandLineArgs(args)
        self.assertEqual(expectedResult, actualResult)
        
    def test_formatCommandLineArgs_SingleQuote(self):
        args = ["a", "\"cute", "owl", "eating", "berries", "with", "a", "clock"]
        expectedResult = args
        
        actualResult = hotCCSVGenerator.formatCommandLineArgs(args)
        self.assertEqual(expectedResult, actualResult)
        
    def test_extractPossibleFilename(self):
        dataline = "Packname goes here Trial Deck Translation\nThis is an extra line\nso is this"
        expectedResult = "Packname_goes_here_Trial_Deck_Translation"
        
        actualResult = hotCCSVGenerator.extractPossibleFilename(dataline)
        self.assertEqual(expectedResult, actualResult)
        
    def test_extractPossibleFilename_illegalChars(self):
        dataline = "P@ckna<me g\"oes here/ Trial D>eck\ Tr|ans:lati?on\nThis is an extra line\nso is this"
        expectedResult = "Packna_me_g_oes_here__Trial_D_eck__Tr_ans_lati_on"
        
        actualResult = hotCCSVGenerator.extractPossibleFilename(dataline)
        self.assertEqual(expectedResult, actualResult)
        
    def test_run_Filepath(self):
        args = ["filepath", "tests/testData/testWebpage.html"]
        correctCSVDataFilepath= "tests/testData/Expected_Fake_Deck_Translation.csv"
        expectedCSVFilepath = "output/Fake_Deck_Translation.csv"
        
        with open(correctCSVDataFilepath, "r", encoding=FILE_ENCODING) as file:
            expectedResult = file.readlines()
        with patch('builtins.print') as mock_print:
            with patch('builtins.input', return_value='y') as mock_input:
                hotCCSVGenerator.run(args)
        
        self.assertTrue(Path(expectedCSVFilepath).exists())
        
        with open(expectedCSVFilepath, "r", encoding=FILE_ENCODING) as file:
            actualResult = file.readlines() 
        self.assertEqual(expectedResult, actualResult)
        
    def test_run_Filepath_gibberish(self):
        args = ["filepath", "adfas;ldkfa;jsdlkfajs;dflkas"]
        with patch('builtins.print') as mock_print:
            with patch('builtins.input', return_value='y') as mock_input:
                runInfo = hotCCSVGenerator.run(args)
        self.assertEqual(runInfo["status"], hotCCSVGenerator.config.RUN_STATUS_FAIL)
        self.assertEqual(runInfo["mode"], hotCCSVGenerator.config.RUN_MODE_FILEPATH)
        self.assertEqual(runInfo["filepath"],args[1])
            
    def test_run_Filepath_nonexistant_file(self):
        args = ["filepath", "this/is/not/valid"]
        with patch('builtins.print') as mock_print:
            with patch('builtins.input', return_value='y') as mock_input:
                runInfo = hotCCSVGenerator.run(args)
        self.assertEquals(runInfo["status"], hotCCSVGenerator.config.RUN_STATUS_FAIL)
        self.assertEquals(runInfo["mode"], hotCCSVGenerator.config.RUN_MODE_FILEPATH)
        self.assertEquals(runInfo["filepath"],args[1])
            
    def test_run_Url_gibberish(self):
        args = ["url", "ksadfasdfasdflkjl"]
        with patch('builtins.print') as mock_print:
            with patch('builtins.input', return_value='y') as mock_input:
                runInfo = hotCCSVGenerator.run(args)
        self.assertEquals(runInfo["status"], hotCCSVGenerator.config.RUN_STATUS_FAIL)
        self.assertEquals(runInfo["mode"], hotCCSVGenerator.config.RUN_MODE_URL)
        self.assertEquals(runInfo["url"],args[1])
                
    def test_run_Url_Non_HotC_url(self):
        args = ["url", "www.youtube.com"]
        with patch('builtins.print') as mock_print:
            with patch('builtins.input', return_value='y') as mock_input:
                runInfo = hotCCSVGenerator.run(args)
        self.assertEquals(runInfo["status"], hotCCSVGenerator.config.RUN_STATUS_FAIL)
        self.assertEquals(runInfo["mode"], hotCCSVGenerator.config.RUN_MODE_URL)
        self.assertEquals(runInfo["url"],args[1])
            
    def test_run_Name_not_valid(self):
        args = ["name", "mother nature", "the embodiment of chaos"]
        with patch('builtins.print') as mock_print:
            with patch('builtins.input', return_value='y') as mock_input:
                runInfo = hotCCSVGenerator.run(args)
        self.assertEquals(runInfo["status"], hotCCSVGenerator.config.RUN_STATUS_FAIL)
        self.assertEquals(runInfo["mode"], hotCCSVGenerator.config.RUN_MODE_SET_AND_PACK)
        self.assertEquals(runInfo["setName"],args[1])
        self.assertEquals(runInfo["packType"],args[2])
            
    def test_run_url_HotC_not_valid(self):
        args = ["url", "https://www.heartofthecards.com/translations/bob"]
        with patch('builtins.print') as mock_print:
            with patch('builtins.input', return_value='y') as mock_input:
                runInfo = hotCCSVGenerator.run(args)
        self.assertEquals(runInfo["status"], hotCCSVGenerator.config.RUN_STATUS_FAIL)
        self.assertEquals(runInfo["mode"], hotCCSVGenerator.config.RUN_MODE_URL)
        self.assertEquals(runInfo["url"],args[1])
            
    def test_run_url_not_translation(self):
        args = ["url", "https://www.heartofthecards.com/rfy/translations/"]
        with patch('builtins.print') as mock_print:
            with patch('builtins.input', return_value='y') as mock_input:
                runInfo = hotCCSVGenerator.run(args)
        self.assertEquals(runInfo["status"], hotCCSVGenerator.config.RUN_STATUS_FAIL)
        self.assertEquals(runInfo["mode"], hotCCSVGenerator.config.RUN_MODE_URL)
        self.assertEquals(runInfo["url"],args[1])
            
    #def test_doLogging(self):
    #    runInfo = {"verbosity": None}
    #    hotCCSVGenerator.setupLogger(runInfo)
        
    #    hotCCSVGenerator.doLogging(None, "This should print logging.info.")
    #    hotCCSVGenerator.doLogging(hotCCSVGenerator.config.LOGGER_WARN, "This should also print logging.warning.")  

    def test_generateFinalReport(self):
        tenSecAgo = datetime.now() - timedelta(seconds=10)
        runSummarySuccess1 = {"status": "success",
                              "outputFilepath": "success/filepath/here"
                             }
        runSummarySuccess2 = {"status": "success",
                              "outputFilepath": "another/path/here"
                             }
        runSummaryFail1 = {"status": "fail",
                           "mode": "url",
                           "url": "https://istheinternetonfire.com",
                           "info" : "HTTP Error 418: Server is a teapot."
                           }
        runSummaryFail2 = {"status": "fail",
                           "mode": "filepath",
                           "filename": "totallyHomeworkNothingSuspicious.pdf",
                           "info": "File was eaten by goats."
                           }
        runSummaryFail3 = {"status": "fail",
                           "mode": "setname and packtype",
                           "setname": "totally not a set name",
                           "packtype": "totally not a pack type",
                           "info": "A time-traveling detective changed the timeline. This set does not exist in this timeline."
                           }
        print(hotCCSVGenerator.generateFinalReport(tenSecAgo, [runSummarySuccess1]))
        print(hotCCSVGenerator.generateFinalReport(tenSecAgo, [runSummaryFail1]))
        print(hotCCSVGenerator.generateFinalReport(tenSecAgo, [runSummarySuccess1, runSummarySuccess2, runSummaryFail1, runSummaryFail2,runSummaryFail3]))
        print(hotCCSVGenerator.generateFinalReport(tenSecAgo, [runSummaryFail1, runSummarySuccess1, runSummaryFail2, runSummarySuccess2, runSummaryFail3]))
       
    def test_writeCardsToCSVFile_no_overwrite(self):
        TEST_FILE = Path(__file__).parent /"testData/testCSVFile.csv"
        global dataOne
        c = hotCCSVGenerator.Card(dataOne)
        cardData = [c]
        with patch('builtins.print') as mock_print:
            with patch('builtins.input', return_value='n') as mock_input:
                with self.assertRaises(FileExistsError):
                    hotCCSVGenerator.writeCardsToCSVFile(TEST_FILE, cardData, False)
                    
    def test_proccessCommandLineArgs_outputFile_char(self):
        args = ["-o", "outputFile.csv", "filepath", "this/is/a/filepath.txt"]
        expectedResult = {"mode": "filepath",
                          "filepath": "this/is/a/filepath.txt",
                          "outputFilepath": Path(__file__).parent.parent / "output" /"outputFile.csv",
                          "verbose": False,
                          "quiet": False,
                          "abortOnError": False
                         }
        actualResult = hotCCSVGenerator.proccessCommandLineArgs(args)
        self.assertEqual(expectedResult, actualResult)
    
    def test_proccessCommandLineArgs_outputFile(self):
        args = ["--output-file", "outputFile.csv", "filepath", "this/is/a/filepath.txt"]
        expectedResult = {"mode": "filepath",
                          "filepath": "this/is/a/filepath.txt",
                          "outputFilepath": Path(__file__).parent.parent / "output" / "outputFile.csv",
                          "verbose": False,
                          "quiet": False,
                          "abortOnError": False
                         }
        actualResult = hotCCSVGenerator.proccessCommandLineArgs(args)
        self.assertEqual(expectedResult, actualResult)
        
    def test_proccessCommandLineArgs_abortOnError(self):
        args = ["--output-file", "outputFile.csv", "--abort-on-error", "filepath", "this/is/a/filepath.txt"]
        expectedResult = {"mode": "filepath",
                          "filepath": "this/is/a/filepath.txt",
                          "outputFilepath": Path(__file__).parent.parent / "output" / "outputFile.csv",
                          "verbose": False,
                          "quiet": False,
                          "abortOnError": True
                         }
        actualResult = hotCCSVGenerator.proccessCommandLineArgs(args)
        self.assertEqual(expectedResult, actualResult)
   
        
        
if __name__ == "__main__":
    unittest.main()