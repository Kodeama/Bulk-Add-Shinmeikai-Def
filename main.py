import sys, codecs, time
import shinmeikai, japaneseParser, config, IOHandler

#Get input file
#Parse input file to get inputArray (list of all cards)
#Get definitions for each focus field in inputArray
#Save definitions to inputarray's meaning field
#Export new cards
#
'''
if len(sys.argv) <= 1:
    print("No file detected, try running:\n\"testMain.py <input> <output>\"\nor \"testMain.py -h\" for help")
    sys.exit()
else:
    definition = shinmeikai.searchForWord(sys.argv[1])

print(definition)
'''

'''
progress = 0 #0 to 100%
loadBardCharWidth = 40
for i in range(100):
    progress += 1
    sys.stdout.write ('\r[{0}{1}] {2}%'.format('#'*(int((progress/100.0) * loadBardCharWidth)),' '*(loadBardCharWidth - int(progress/100.0 * loadBardCharWidth)) , progress))
    time.sleep(0.0005)
'''

#Gets all definitions for all words, making a 2D array where the first index decides the card and the second index decides which definition for that card
def getDefinitionList(targetWordList):
    definitionList = []
    rtkKeywordList = []
    interationCounter = 0
    maxIterations = len(targetWordList)
    for x in targetWordList:
        #searches all definitions for each word
        definition = shinmeikai.searchForWord(str(x))
        #Sorts and reorder the definitions based on frequency from frequencylist
        definition = sortDefinitions(definition)
        #Remove all unwanted definitions. If user only wants 3 themove the overflow
        numOfDefs = len(definition)
        desiredNumOfDef = config.Config.numberOfDefinitions
        if numOfDefs > desiredNumOfDef:
            for x in range(0, numOfDefs - desiredNumOfDef): #definitions to remove in list
                del definition[-1] #Remove last element

        sortedDef = sortDefinitions(definition)
        #sortedDef = sortedDef.replace("\\n", "<div></div>")
        formatedDef = ""
        for x in definition:
            tempFormDef = x[0].replace("\\n", "<div></div>")
            formatedDef += str(tempFormDef.replace(r"[", r" ["))+"<div></div>"
        definitionList.append(formatedDef)

        if config.Config.enableRTKKeywords:
            rtkKeywords = ""
            if japaneseParser.stringContainsKanji(targetWordList[interationCounter]):
                rtkKeywords = japaneseParser.getRTKKeyword(targetWordList[interationCounter])
                #print("Recieved RtkKeywords: "+str(rtkKeywords))
            rtkKeywordList.append(rtkKeywords)
        interationCounter += 1
        IOHandler.updateLoadbar(interationCounter, maxIterations)
    if config.Config.debug:
        print(str(definitionList))
    if config.Config.enableRTKKeywords:
        IOHandler.saveDataListToField(config.Config.kanjiField, rtkKeywordList)
        #print("kanji amount: "+str(len(rtkKeywordList)))
        #print("All Kanji: "+ str(rtkKeywordList))
        #print("Searchterm: " + str(searchTerm))

    #print("RTK List Length: "+str(len(rtkKeywordList)))
    return definitionList

def sortDefinitions(defList):
    newList = []

    #Sorts all definitions for card
    sortedSubDefList = sorted(defList, key=lambda y : y[1])
    if config.Config.debug:
        print("(main.py:47)SUBLIST:\n"+str(defList))
        print("(main.py:48)SORTED SUBLIST:\n"+str(sortedSubDefList)+"\n")

    return sortedSubDefList



cardList = IOHandler.readFile(sys.argv)
#List of target words

targetList = IOHandler.getTargetFieldFromList(cardList)
if config.Config.debug:
    counter = 1
    for x in targetList:
        print("Target word "+str(counter)+": "+str(x))
        counter += 1

#List of definitions for target words
definitionList = getDefinitionList(targetList)
if config.Config.debug:
    counter = 1
    for x in definitionList:
        print("Definition for word "+str(counter)+": "+str(x))
        counter += 1


exportCardList = IOHandler.saveDataListToField(config.Config.cardWriteFieldIndex, definitionList)

IOHandler.exportFile(exportCardList)


print("\nScript executed secessfully\nPress enter to exit...")
input()
