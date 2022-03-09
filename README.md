## Table of Contents
* [Description](#description)
* [Modes](#modes)
  * [url](#url)
  * [fielpath](#filepath)
  * [set name and pack type](#set-name-and-pack-type)
* [Options](#options)
* [Disclaimer](#disclaimer)

# DESCRIPTION
HotCCSVGenerator is a command-line program to convert the translated Weiß Schwarz card data from HeartoftheCards.com (HotC) into a .csv file. It requires the Python interpreter, the `requests` library, and `beautifulsoup4`\.  
**Note:** Although it was developed on Python v3.10.1, it will likely work with version 3.8 or greater, due to the use of TypedDict.

```
hotCCSVGenerator [OPTIONS] {RUN_MODE} [MODE_ARGUMENTS]
```

## Modes
There are three different ways this tool can get the card data, depending on what mode it is run in:

### 1. url
```
hotCCSVGenerator [OPTIONS] url URL
```
By providing the full url to the translated card data, this tool will fetch the provided page before extracting the data. The provided url must be a link to the full set translation data, i.e. the url should look something like this:
```
www.heartofthecards.com/translations/{set_name_and_pack_type_go_here}.html
```

### 2. filepath
```
hotCCSVGenerator [OPTIONS] filepath FILEPATH
```
If you have previously downloaded the card data page from HotC, you can run the tool in filepath mode to specify that file.
### 3. set name and pack type
```
hotCCSVGenerator [OPTIONS] name SETNAME PACKTYPE
```
You can simply specify the name of the set and what type of pack you want, and the tool will generate the url automatically and fetch the data for you. If either arugment contains spaces, remember to surround it with quotation marks.

# OPTIONS
```
-h, --help                           Print the help text and exit.
--version                            Print the version number and exit.
```

## DISCLAIMER: 
No data from HotC is being hosted in this repository. This is just a tool to convert the data to a more useful format, intended for personal use only.  
If you do use this tool, please follow the terms and conditions regarding HotC data and "\[d]o not distribute, reprint, or repost \[the data] in whole or in part."