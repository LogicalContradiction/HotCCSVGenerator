VERSION_NUM = "notCCSVGenerator version 1.0"
PATTERN = r"==+"
FILE_ENCODING= "utf8"
TEXTLINE_STARTER = "TEXT: "
TEXTLINE_PATTERN = "\[.]"
NEWLINE_CHAR = "\n"
WHITESPACE_PATTERN = "\s+"
CSV_WRITER_FIELDNAMES = ["name", 
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
                         "text"
                        ]
CSV_DELIMITER = "\t"

TRANSLATED_NAME = {"translatedName" : None}
NAME = {"name" : None}
CARD_NUM_RARITY = {"cardNum" : 2,
                   "rarity" : 4
                  }
COLOR_SIDE_TYPE = {"color" : 1,
                   "side" : 3,
                   "type" : 4
                  }
LEVEL_COST_POWER_SOUL = {"level" : 1,
                         "cost" : 3,
                         "power" : 5,
                         "soul" : 7
                        }
TRAITS = {"traits" : 8}
TRIGGERS = {"triggers" : 10}
FLAVOR = {"flavor" : 8}
CARD_LINES = [TRANSLATED_NAME,
              NAME,
              CARD_NUM_RARITY,
              COLOR_SIDE_TYPE,
              LEVEL_COST_POWER_SOUL,
              TRAITS,
              TRIGGERS,
              FLAVOR
             ]
FIELDS_TO_CONVERT_TO_INT = ["level",
                            "cost",
                            "power",
                            "soul"
                           ]

URL_VALIDATION_PATTERN = "^((http|https):\/\/)?(www.)?heartofthecards(.com)\/translations\/"                       
URL_FORMAT_PATTERN = "https://www.heartofthecards.com/translations/{setNameAndType}.html"

URL_REGEX_PATTERN_REPLACE_WITH_DASH = ":|,|'|&|\/|\(|\)"
URL_REGEX_PATTERN_REPLACE_WITH_UNDERSCORE = " "
URL_REGEX_PATTERN_REMOVE = "\?"

URL_REGEX_REPLACE_CHARS = [(URL_REGEX_PATTERN_REPLACE_WITH_DASH, "-"),
                           (URL_REGEX_PATTERN_REPLACE_WITH_UNDERSCORE, "_"),
                           (URL_REGEX_PATTERN_REMOVE, "")
                          ]
                          
RUN_MODE_FILEPATH = "filepath"
RUN_MODE_URL = "url"
RUN_MODE_SET_AND_PACK = "name"

DEFAULT_FILEPATH = "output"
DEFAULT_FILENAME = "{filename}.csv"

OUTPUT_FILENAME_REPLACE_WITH_A = "@"
OUTPUT_FILENAME_REPLACE_WITH_UNDERSCORE = r"[/<>:\"\\|?* ]"
OUTPUT_FILENAME_REPLACE_SPACE = " "

FILENAME_REPLACE_CHARS = [(OUTPUT_FILENAME_REPLACE_WITH_A, "a"),
                          (OUTPUT_FILENAME_REPLACE_WITH_UNDERSCORE, "_")
                         ]
                         
HOTC_NOT_FOUND_TITLE_FRAGMENT = "404"
