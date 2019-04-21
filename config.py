import json
class Config(object):
    '''
    debug = False #Enable debug output in console

    #If input & output is not specified when calling the script these filenames will be searched for instead.
    inputFileName = "input.txt"
    outputFileName = "output.txt"

    #Other data filenames
    wordFreqList = r"Data\10kData.txt"
    kanjiList = r"Data\HeisigKeywords.txt"

    #NOTE index starts at 1! So index 1 would be the first field in anki, 2 would be the second and so on.
    cardReadFieldIndex = 6 #The index of which field to read from, most likely the "Focus" field.
    cardWriteFieldIndex = 7 #The Index of which field to write to, most likely the "Meaning" field.

    #Maximum number of definitions for each word
    numberOfDefinitions = 3

    enableRTKKeywords = True
    kanjiField = 8
    '''
    with open(r"config.json") as f:
        data = json.load(f)

    debug = data["debug"]
    inputFileName = data["inputFileName"]
    outputFileName = data["outputFileName"]
    wordFreqList = data["wordFreqList"]
    kanjiList = data["kanjiList"]
    cardReadFieldIndex = data["cardReadFieldIndex"]
    cardWriteFieldIndex = data["cardWriteFieldIndex"]
    numberOfDefinitions = data["numberOfDefinitions"]
    enableRTKKeywords = data["enableRTKKeywords"]
    kanjiField = data["kanjiField"]

'''
def configInit():
    with open(r"config.json") as f:
        data = json.load(f)

    debug = data["debug"]
    inputFileName = data["inputFileName"]
    outputFileName = data["outputFileName"]
    wordFreqList = data["wordFreqList"]
    kanjiList = data["kanjiList"]
    cardReadFieldIndex = data["cardReadFieldIndex"]
    cardWriteFieldIndex = data["cardWriteFieldIndex"]
    numberOfDefinitions = data["numberOfDefinitions"]
    enableRTKKeywords = data["enableRTKKeywords"]
    kanjiField = data["kanjiField"]

    return

configInit()
'''
