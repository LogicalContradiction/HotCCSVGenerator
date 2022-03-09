SUBPARSER_HELP_TEXT = "Specifies where the data is coming from. Supports a HotC url, a .html file downloaded from HotC, or the set name and pack type."
PROG_DESCRIPTION_FOR_PARSER_TEXT = "Description of program goes here."

SUBPARSER_URL_HELP_TEXT = "Use this command to specify a url to download the data from."
SUBPARSER_URL_ARGUMENT_HELP_TEXT = "The HotC url to convert data from."

SUBPARSER_FILEPATH_HELP_TEXT = "Use this command to specify the filepath of a .html file downloaded from HotC to convert."
SUBPARSER_FILEPATH_ARGUMENT_HELP_TEXT = "Filepath to the .html file downloaded from HotC to be converted."

SUBPARSER_PACK_HELP_TEXT = "Use this command to specify a set name and pack type to get the data about."
SUBPARSER_PACK_ARGUMENT_ONE_HELP_TEXT = "The name of the set to get data about. This is normally the name of the series."
SUBPARSER_PACK_ARGUMENT_TWO_HELP_TEXT = "The type of pack for a particular set to get the data about. This is normally \"trial deck\", \"booster pack\", or \"extra deck\", but there are also a few other miscellaneous types."

PARSER_VERSION_HELP_TEXT = "Prints the version number and exit."
PARSER_VERBOSE_HELP_TEXT = "Print various debugging information while running."
PARSER_OUTPUT_FILE_HELP_TEXT = "Specify a filepath to output to"
PARSER_ABORT_ON_ERROR_HELP_TEXT = "Abort converting any more pages if an error occurs."
PARSER_BATCH_FILE_HELP_TEXT = "File containing HotC urls, .html files, or set name and pack type separated by a tab character, with only one of these per line. Following each of these arguments should be another tab character, which is then followed by the output filename. If no filename is specified, the default is used. Lines starting with '#' are treated as comments and ignored."
PARSER_DRY_RUN_HELP_TEXT = "Simulate running and print what will happen given the set of inputs."

FILEPATH_NOT_FOUND_ERROR_MSG = "The specified file could not be found, please double check the spelling and try again.\nFile specified: {filename}"
CONNECTIONERROR_ERROR_MSG = "A connection error occured. Please double check that the url is correct and try again.\nurl provided: {url}"
HTTPERROR_ERROR_MSG = "HTTP error occured. Please take the reccomended action and try again.\nHTTP status code: {statusCode}\nReason: {reason}"
WRITE_OSERROR_ERROR_MSG = "An error occured while writing. Please try again.\nFilename: {filename}\nError msg: {errormsg}"
NOT_A_HOTC_URL_ERROR_MSG = "The provided url was not a valid HotC url. Please double check it and try again."
SET_NAME_PACK_TYPE_NOT_FOUND = "There was an issue getting the data from the webpage. This was likely caused by an issue with either the set name or pack type. Please double check these and try again.\nSet name: {setname}\nPack type: {packtype}\nGenerated url: {url}"
URL_NOT_VALID = "The url provided was not a valid link to a HotC translation page. Please double check it and try again.\nurl: {url}"

WEB_SCRAPE_EXCEPTION_MSG = "Error when scraping url.\nurl: {url}"