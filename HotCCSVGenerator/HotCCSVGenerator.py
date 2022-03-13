from . import config
from . import textData
from bs4 import BeautifulSoup
import re
import requests
from typing import TypedDict, Dict
from pathlib import Path
import csv
import argparse
import sys
import logging
from datetime import datetime

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
        
class WebScrapeException(Exception):

    def __init__(self, url):
        self.url = url
        
    def __str__(self):
        return textData.WEB_SCRAPE_EXCEPTION_MSG.format(url=self.url)
        

      
def makeSoupFromFile(filepath: str):
    logger = logging.getLogger(config.LOGGER_NAME)
    logger.info(textData.RUN_INFO_READING_HTML_FILE)
    #doLogging(None, textData.RUN_INFO_READING_HTML_FILE)
    with open(filepath, "r", encoding=config.FILE_ENCODING) as file:
        soup = BeautifulSoup(file, "html.parser")
    logger.info(textData.RUN_INFO_COMPLETE)
    #doLogging(None, textData.RUN_INFO_COMPLETE)
    return soup
    
def makeSoupFromWebpage(url: str):
    logger = logging.getLogger(config.LOGGER_NAME)
    logger.info(textData.RUN_INFO_WEBPAGE.format(url=url))
    #doLogging(None, textData.RUN_INFO_WEBPAGE.format(url=url))
    req = requests.get(url)
    req.raise_for_status()
    soup = BeautifulSoup(req.text, "html.parser")
    #check to see if the page wasn't found
    if config.HOTC_NOT_FOUND_TITLE_FRAGMENT in soup.head.title.text:
        raise WebScrapeException(url)
    logger.info(textData.RUN_INFO_COMPLETE)
    #doLogging(None, textData.RUN_INFO_COMPLETE)
    return soup
    
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
    startIndexes.append(len(textLine))
    index = -1
    text = []
    for item in startIndexes:
        index += 1
        if index < len(startIndexes)-1:
            #grab startIndex at locations index and index+1 and slice the string at those indexes
            t = textLine[item:startIndexes[index+1]]
            text.append(t)
    text = [(item.replace(config.NEWLINE_CHAR, " ")).strip() for item in text]
    return config.NEWLINE_CHAR.join(text)
    
def extractDataFromLine(line: str, indexes: Dict[str, int] | None)->Dict[str, str]:
    """
    Pass in a dict in the form {fieldName : indexWhenSplitByWhitespace}
    Extracts those indexes and returns dict in form {fieldName : textData}
    If there is only one item (the entire line is the field), pass {fieldName : lineStarterToRemove}
    """
    if len(indexes) == 1:
        fieldName = next(iter(indexes))
        value = indexes[fieldName]
        return {fieldName : line[value:].strip()}
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
    logger = logging.getLogger(config.LOGGER_NAME)
    logger.info(textData.RUN_INFO_BEGIN_SCRAPING)
    #doLogging(None, textData.RUN_INFO_BEGIN_SCRAPING)
    text = soup.pre.text
    lines = re.split(config.PATTERN, text)
    result = []
    for dataLine in lines:
        result.append(dataLine.strip())
    del result[len(result)-1]
    logger.info(textData.RUN_INFO_COMPLETE)
    #doLogging(None, textData.RUN_INFO_COMPLETE)
    return result     
    
def writeCardsToCSVFile(filepath: Path, cardData: list[Card])->None:
    """
    Open a file and write a list of Cards to items
    """
    logger = logging.getLogger(config.LOGGER_NAME)
    logger.info(textData.RUN_INFO_BEGIN_WRITING_TO_FILE.format(filename=str(filepath)))
    #doLogging(None, textData.RUN_INFO_BEGIN_WRITING_TO_FILE.format(filename=str(filepath)))
    #open the file
    with open(filepath, "w", encoding=config.FILE_ENCODING, newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=config.CSV_WRITER_FIELDNAMES, delimiter=config.CSV_DELIMITER)
        writer.writeheader()
        for card in cardData:
            writer.writerow(card)
    logger.info(textData.RUN_INFO_COMPLETE)
    #doLogging(None, textData.RUN_INFO_COMPLETE)
    return
    
def makeCardFromData(data: str)->Card:
    """
    Take the string that's been stripped, extract the data, and return a Card
    """
    #first split the string on newline
    splitData = data.split(config.NEWLINE_CHAR)
    index = -1
    resultData = {}
    for line in config.CARD_LINES:
        index += 1
        lineInfo = extractDataFromLine(splitData[index], line)
        resultData.update(lineInfo)
    #check for the fields to convert to int
    for key in config.FIELDS_TO_CONVERT_TO_INT:
        if key in resultData.keys():
            resultData[key] = int(resultData[key])
    #now get the textline
    textInfo = extractAndFormatTextField(data)
    resultData["text"] = textInfo
    return Card(resultData)
    
def formatUrl(setName: str, packType:str)->str:
    """
    Takes the name of a set (typically a series) and the pack type (booster pack, trial deck, or one of the many
    misc. sets) and returns a formatted url (replace spaces with underscores and cast entire string to lowercase)
    """
    #colon, comma, apostrophe, ampersand, forward slash, parenthesis become dash
    #question mark is removed
    #space replaced with underscore
    #first, strip excess whitespace from the ends and cast to lowercase
    setName = setName.strip().lower()
    packType = packType.strip().lower()
    #replace all the special characters we don't want
    for tup in config.URL_REGEX_REPLACE_CHARS:
        (pattern, replaceChar) = tup
        setName = re.sub(pattern, replaceChar, setName)
        packType = re.sub(pattern, replaceChar, packType)
    #now join the two on an underscore
    setNameAndPackType = setName + "_" + packType
    #now return the formatted url
    return config.URL_FORMAT_PATTERN.format(setNameAndType=setNameAndPackType)
    
def convertAPageToCards(filepathOrUrl: str)->list[Card]:
    """
    Convert a single page to Cards and return a list of cards
    """
    #Decide if it's a url or filepath. Make soup based on that
    if re.match(config.URL_VALIDATION_PATTERN, str(filepathOrUrl)):
        soup = makeSoupFromWebpage(filepathOrUrl)
    else:
        soup = makeSoupFromFile(filepathOrUrl)
    #now extract the data to be turned into cards
    cardData = getLinesFromSoup(soup)
    #now turn all the cardDatas into cards
    cards = []
    for dataGroup in cardData[1:]:
        cards.append(makeCardFromData(dataGroup))
    #now get the possible filename
    filename = extractPossibleFilename(cardData[0])
    return cards, filename
    
def extractPossibleFilename(dataLine: str)->str:
    """
    Extract the possible filename from the data
    """
    #first, split the lines
    lines = dataLine.split("\n")
    nameLine = lines[0].strip()
    #now remove illegal characters
    for item in config.FILENAME_REPLACE_CHARS:
        pattern, replaceChar = item
        nameLine = re.sub(pattern, replaceChar, nameLine)
    return nameLine
    
def proccessCommandLineArgs(arguments: list[str])->Dict[str,str]:
    """
    Process the command line flags and return a data structure dictating how the program should run.
    Call formatCommandLineArgs first to stitch together quoted variables
    Make sure the script name is not present. 
    """
    #make the main parser
    parser = argparse.ArgumentParser(description=textData.PROG_DESCRIPTION_FOR_PARSER_TEXT)
    #crate subparsers to handle the subtype of what mode to run in
    subparsers = parser.add_subparsers(help=textData.SUBPARSER_HELP_TEXT)
    #url mode parser
    parserUrl = subparsers.add_parser("url", help=textData.SUBPARSER_URL_HELP_TEXT)
    parserUrl.add_argument("url", help=textData.SUBPARSER_URL_ARGUMENT_HELP_TEXT, metavar="URL")
    #filepath mode parser
    parserFileName = subparsers.add_parser("filepath", help=textData.SUBPARSER_FILEPATH_HELP_TEXT)
    parserFileName.add_argument("filepath", help=textData.SUBPARSER_FILEPATH_ARGUMENT_HELP_TEXT, metavar="FILEPATH")
    #set name and pack type parser
    parserSetPack = subparsers.add_parser("name", help=textData.SUBPARSER_PACK_HELP_TEXT)
    parserSetPack.add_argument("setName", help=textData.SUBPARSER_PACK_ARGUMENT_ONE_HELP_TEXT, metavar="SET_NAME")
    parserSetPack.add_argument("packType", help=textData.SUBPARSER_PACK_ARGUMENT_TWO_HELP_TEXT, metavar="PACK_TYPE")

    #main parser arguments - apply to before the subtype
    parser.add_argument("--version", help=textData.PARSER_VERSION_HELP_TEXT, action="store_true")
    
    #parse the args. can also pass a list as an argument to parse that
    args = parser.parse_args(arguments)
    #check if the arg passed was for version
    if args.version:
        print(config.VERSION_NUM)
        exit(0)
    #create the structure to dictate how the program runs
    runInfo = {"mode": None, "outputFilepath": None}
    #figure out which subprocessor was found:
    if "filepath" in args:
        runInfo["mode"] = config.RUN_MODE_FILEPATH
        runInfo["filepath"] = args.filepath
    if "url" in args:
        runInfo["mode"] = config.RUN_MODE_URL
        runInfo["url"] = args.url
    if "setName" and "packType" in args:
        runInfo["mode"] = config.RUN_MODE_SET_AND_PACK
        runInfo["setName"] = args.setName
        runInfo["packType"] = args.packType
    return runInfo
    
def formatCommandLineArgs(args: list[str])->list[str]:
    """
    Used to connect strings that are within quotes that parsing the command line broke up.
    Make sure to call with sys.args[1:]
    """
    index = 0
    result = []
    while index < len(args):
        #chech if first character is "
        if args[index][0] == "\"":
            #we need to try to these arguments together
            quoteStartIndex = index
            quoteEndIndex = index
            #now try to find an argument that ends with "
            foundEndQuote = False
            while quoteEndIndex < len(args):
                #check the last character for "
                item = args[quoteEndIndex]
                if item[len(item)-1] == "\"":
                    #first join the arguments to get the full string
                    joinedStr = " ".join(args[quoteStartIndex:quoteEndIndex+1])
                    #now remove the quotation marks since they aren't needed
                    joinedStr = joinedStr.replace("\"", "")
                    result.append(joinedStr)
                    index = quoteEndIndex+1
                    foundEndQuote = True
                    break
                else:
                    quoteEndIndex += 1
            if not foundEndQuote:
                #case of reaching end of arguments list and not finding a closing quote
                #add the rest of the items to result
                for argument in args[quoteStartIndex:]:
                    result.append(argument)
                index = quoteEndIndex
        else:
            result.append(args[index])
            index += 1
    return result
    
def doLogging(level: str, msg: str):
    """
    Do the logging.
    """
    logger = logging.getLogger(config.LOGGER_NAME)
    if level == config.LOGGER_INFO:
        logger.info(msg)
    elif level == config.LOGGER_WARN:
        logger.warning(msg)
    else:
        print(msg)
    return
    
def setupLogger(runInfo: Dict[str,str]):
    """
    Use to set up the logger.
    """
    logger = logging.getLogger(config.LOGGER_NAME)
    if not len(logger.handlers):
        #add support here for level depending on runInfo
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
    return
    

def run(arguments: list[str])->Dict[str,str]:
    """
    The main method that drives the entire program.
    """
    #first, get the command line args (don't need arg0 since it's script name
    if arguments == None:
        args = sys.argv[1:]
    else:
        args = arguments
    #format the arguments
    args = formatCommandLineArgs(args)
    #now get the dict to determine how the program should run
    runInfo = proccessCommandLineArgs(args)
    #now set up the logger
    setupLogger(runInfo)
    logger = logging.getLogger(config.LOGGER_NAME)
    logger.info(textData.RUN_INFO_PROGRAM_START_MSG)
    logger.info(textData.RUN_INFO_INFO_PROVIDED)
    #doLogging(None, textData.RUN_INFO_PROGRAM_START_MSG)
    #doLogging(None, textData.RUN_INFO_INFO_PROVIDED)
    #check if it's in setname mode
    if runInfo["mode"] == config.RUN_MODE_SET_AND_PACK:
        logger.info(textData.RUN_INFO_SETNAME_PACKTYPE_PROVIDED.format(setname=runInfo["setName"], packtype=runInfo["packType"]))
        #doLogging(None, textData.RUN_INFO_SETNAME_PACKTYPE_PROVIDED.format(setname=runInfo["setName"], packtype=runInfo["packType"]))
        #set name and pack type, so format the url
        urlOrFilename = formatUrl(runInfo["setName"], runInfo["packType"])
        #set the output filepath
        if runInfo["outputFilepath"] == None:
            possibleFilename = extractPossibleFilename(runInfo["setName"] + " " + runInfo["packType"])
            defaultOutputDirectory = Path(__file__).parent.parent / config.DEFAULT_FILEPATH
            defaultOutputDirectory.mkdir(exist_ok=True)
            runInfo["outputFilepath"] = defaultOutputDirectory / config.DEFAULT_FILENAME.format(filename=possibleFilename)
    elif runInfo["mode"] == config.RUN_MODE_URL:
        logger.info(textData.RUN_INFO_URL_PROVIDED.format(url=runInfo["url"]))
        #doLogging(None, textData.RUN_INFO_URL_PROVIDED.format(url=runInfo["url"]))
        #url case, so just extract it
        urlOrFilename = runInfo["url"]
        #validate it's a HotC url
        if not re.match(config.URL_VALIDATION_PATTERN, urlOrFilename):
            #not a HotC url, so exit
            logger.warning(textData.NOT_A_HOTC_URL_ERROR_MSG)
            #doLogging(config.LOGGER_INFO, textData.NOT_A_HOTC_URL_ERROR_MSG)
            runInfo["status"] = config.RUN_STATUS_FAIL
            runInfo["info"] = textData.NOT_A_HOTC_URL_ERROR_MSG
            return runInfo
    else:
        #filepath given, so validate it and then extract items
        if Path(runInfo["filepath"]).exists():
            urlOrFilename = runInfo["filepath"]
            logger.info(textData.RUN_INFO_FILENAME_PROVIDED.format(filename=urlOrFilename))
            #doLogging(None, textData.RUN_INFO_FILENAME_PROVIDED.format(filename=urlOrFilename))
        else:
            #file doesn't exist, so output error
            logger.warning(textData.FILEPATH_NOT_FOUND_ERROR_MSG.format(filename=runInfo["filepath"]))
            #doLogging(config.LOGGER_INFO, textData.FILEPATH_NOT_FOUND_ERROR_MSG.format(filename=runInfo["filepath"]))
            runInfo["status"] = config.RUN_STATUS_FAIL
            runInfo["info"] = textData.FILEPATH_NOT_FOUND_ERROR_MSG.format(filename=runInfo["filepath"])
            return runInfo
    #now we have a url or filepath that is valid. Extract the data
    try:
        cards, resultFilename = convertAPageToCards(urlOrFilename)
    except WebScrapeException as exc:
        #pack and data info wasn't found
        if runInfo["mode"] == config.RUN_MODE_SET_AND_PACK:
            logger.warning(textData.SET_NAME_PACK_TYPE_NOT_FOUND.format(setname=runInfo["setName"],packtype=runInfo["packType"],url=exc.url))
            #doLogging(config.LOGGER_INFO, textData.SET_NAME_PACK_TYPE_NOT_FOUND.format(setname=runInfo["setName"],packtype=runInfo["packType"],url=exc.url))
            runInfo["info"] = textData.SET_NAME_PACK_TYPE_NOT_FOUND.format(setname=runInfo["setName"],packtype=runInfo["packType"],url=exc.url)
        elif runInfo["mode"] == config.RUN_MODE_URL:
            logger.warning(textData.URL_NOT_VALID.format(url=exc.url))
            #doLogging(config.LOGGER_INFO, textData.URL_NOT_VALID.format(url=exc.url))
            runInfo["info"] = textData.URL_NOT_VALID.format(url=exc.url)
        else:
            logger.warning(str(exc))
            #doLogging(None, str(exc))
            runInfo["info"] = str(exc)
        runInfo["status"] = config.RUN_STATUS_FAIL
        return runInfo
    except requests.ConnectionError as exc:
        #invalid url
        logger.warning(textData.CONNECTIONERROR_ERROR_MSG.format(url=urlOrFilename))
        #doLogging(config.LOGGER_INFO, textData.CONNECTIONERROR_ERROR_MSG.format(url=urlOrFilename))
        runInfo["status"] = config.RUN_STATUS_FAIL
        runInfo["info"] = textData.CONNECTIONERROR_ERROR_MSG.format(url=urlOrFilename)
        return runInfo
    except requests.HTTPError as exc:
        #some kind of http error
        logger.warning(textData.HTTPERROR_ERROR_MSG.format(statusCode=exc.response.status_code, reason=exc.response.reason))
        #doLogging(config.LOGGER_INFO, textData.HTTPERROR_ERROR_MSG.format(statusCode=exc.response.status_code, reason=exc.response.reason))
        runInfo["status"] = config.RUN_STATUS_FAIL
        runInfo["info"] = textData.HTTPERROR_ERROR_MSG.format(statusCode=exc.response.status_code, reason=exc.response.reason)
        return runInfo
    #check if we don't already have an output filepath
    if runInfo["outputFilepath"] == None:
        #don't have one. So compute it
        defaultOutputDirectory = Path(__file__).parent.parent / config.DEFAULT_FILEPATH
        defaultOutputDirectory.mkdir(exist_ok=True)
        runInfo["outputFilepath"] = defaultOutputDirectory / config.DEFAULT_FILENAME.format(filename=resultFilename)
    #we have the data and an output file, so write it.
    try:
        writeCardsToCSVFile(runInfo["outputFilepath"], cards)
    except OSError as exc:
        logger.warning(textData.WRITE_OSERROR_ERROR_MSG.format(filename=exc.filename, errormsg=exc.strerror))
        #doLogging(config.LOGGER_INFO, textData.WRITE_OSERROR_ERROR_MSG.format(filename=exc.filename, errormsg=exc.strerror))
        runInfo["status"] = config.RUN_STATUS_FAIL
        runInfo["info"] = textData.WRITE_OSERROR_ERROR_MSG.format(filename=exc.filename, errormsg=exc.strerror)
        return runInfo
    runInfo["status"] = config.RUN_STATUS_SUCCESS
    return runInfo
        
def generateFinalReport(startTime: datetime, runSummary:list[Dict[str,str]])->str:
    """
    Generate a final report for use in displaying to the user.
    """
    success = [textData.FINAL_REPORT_SUCCESS_FILES_WRITTEN]
    fails = [textData.FINAL_REPORT_FILES_FAILED]
    numSuccess = 0
    numFail = 0
    for summary in runSummary:
        if summary["status"] == config.RUN_STATUS_SUCCESS:
            success.append(textData.FINAL_REPORT_SUCCESS_SUMMARY.format(filename=summary["outputFilepath"]))
            numSuccess += 1
        else:
            if summary["mode"] == config.RUN_MODE_URL:
                fails.append(textData.FINAL_REPORT_FAIL_SUMMARY_URL.format(url=summary["url"]))
            elif summary["mode"] == config.RUN_MODE_FILEPATH:
                fails.append(textData.FINAL_REPORT_FAIL_SUMMARY_FILEPATH.format(filename=summary["filename"]))
            else:
                fails.append(textData.FINAL_REPORT_FAIL_SUMMARY_SETNAME_PACKTYPE.format(setname=summary["setname"],packtype=summary["packtype"]))
            fails.append(textData.FINAL_REPORT_FAIL_SUMMARY_REASON.format(reason=summary["info"]))
            numFail +=1
    if len(success) == 1:
        success.append(textData.FINAL_REPORT_NONE_LINE)
    if len(fails) == 1:
        fails.append(textData.FINAL_REPORT_NONE_LINE)
    report = [textData.FINAL_REPORT_PROGRAM_COMPLETE,
              textData.FINAL_REPORT_NUM_SUCCESS.format(numSuccess=numSuccess,totalNum=numSuccess+numFail),
              textData.FINAL_REPORT_NUM_FAIL.format(numFail=numFail,totalNum=numSuccess+numFail),
              textData.FINAL_REPORT_TIME_COMPLETE.format(time=datetime.now()-startTime)
             ]
    return "\n".join(report) + "\n" + "\n".join(success) + "\n" + "\n".join(fails)
        
    
    
if __name__ == "__main__":
    startTime = datetime.now()
    runInfo = run(None)
    print(generateFinalReport(startTime, [runInfo]))
    #doLogging(None, generateFinalReport(startTime, [runInfo]))