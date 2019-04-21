import re, sys, getopt, config, IOHandler
import japaneseParser
#Function used to find definition for searchTerm in shinmeikai
amountOfDictionaryFiles = 9
def searchForWord(searchTerm):
    dictionaryCounter = 1
    defArray = []
    definitionFound = False
    if config.Config.debug:
        print("Searching for "+searchTerm)

    if japaneseParser.stringContainsKanji(searchTerm):
        regex = u"(\[\""+searchTerm+"\"(,.*?){7}\])" #With kanji
    else:
        regex = u"(\[\".{0,8}\",\""+searchTerm+"\"(,.*?){6}\])" #Without kanji
    rtkKeywordList = []


    #Looks for matches in all shinmeikai dictionary files.
    while True:
        dict = open("Data\\Shinmeikai\\shinmeikai_"+str(dictionaryCounter)+".txt", "rb")
        contents = dict.read().decode("UTF-8")
        dict.close()

        pattern = re.compile(regex, re.UNICODE)
        export = pattern.findall(contents)
        if len(export) >= 1:
            definitionFound = True
            for x in export:
                #print("X:\n"+str(x))
                innerDef = extractDefFromDef(str(x))
                #print("InnerDef: "+ innerDef)
                #print("Hira: "+extractHiraFromDef(innerDef)+".")
                #print("Kanji: "+str(extractKanjiFromDef(innerDef))+".")
                hira = extractHiraFromDef(innerDef)
                kanji = extractKanjiFromDef(innerDef)

                if kanji == -1:#If word doesnt have kanji, search with hira for both fields
                    kanji = hira

                freq = japaneseParser.getWordFreq(hira, kanji)
                #print("Freq: "+str(freq))
                #print("Hira: "+hira+"\nKanji: "+str(kanji))
                defArray.append((innerDef, int(freq)))
            #print("EXPORT:" + str(export))
            #print("Definition found:\n"+defArray+"\n")
        if dictionaryCounter >= amountOfDictionaryFiles:
            if definitionFound == False:
                if config.Config.debug:
                    print(searchTerm+" was not found in dictionary")
                defArray = ""
            break
        dictionaryCounter += 1
    return (defArray)

#Returns the necessary definition in textm excluding other fields of the whole definition like order in dictionary.
def extractDefFromDef(org):
    #print("Org:\n"+org)
    regex = u"(.*)\[.*\[\"(.*?)\"\]"

    matchObj = re.match(regex, org)
    if matchObj == None:
        if config.Config.debug:
            print("Definition not found in definition\nError in Shinmeikai.py at line 47")
        returnValue = -1
    else:
        returnValue = matchObj.group(2)
        returnValue = re.sub(r'\\\\', r'\\', str(returnValue))
    return returnValue

def extractHiraFromDef(org):
    #regex = u"\[\".*?\[\"(.*?)  【"
    #print("ORG:\n"+org)
    regex = u"(.*?) "
    matchObj = re.match(regex, org)
    if matchObj == None:
        if config.Config.debug:
            print("ORG:\n"+str(org)+"\n\n")
            print("Hiragana not found in definition\nError in Shinmeikai.py at line 58")
        returnValue = -1
    else:
        returnValue = matchObj.group(1)
    return returnValue

def extractKanjiFromDef(org):
    #regex = u"\[\".*?\[\"(.*?)  【"
    regex = u".*?【(.*?)】"
    matchObj = re.match(regex, org)
    if matchObj == None:
        if config.Config.debug:
            print("ORG:\n"+str(org))
            print("Kanji not found in definition\nError in Shinmeikai.py at line 72")
        returnValue = -1
    else:
        returnValue = matchObj.group(1)

    #If more than one kanji, ex(内・家) for うち
    #return an array of kanji, It seems like the "・" character doesnt work with regex?
    #Currently only handles two different words, like うち -> 家 and 内 works
    matchObj = re.search(u"・", str(returnValue))
    if matchObj != None: #Multiple kanji found
        if config.Config.debug:
            print("MULTIPLE KANJI FOUND:\nKanji amount: "+str(1+len(matchObj.group())))
            print("SEARCHING IN STRING:\n"+returnValue)
        matchObj = re.match(u"(.*?)・(.*?) ", returnValue+" ")
        if config.Config.debug:
            print("After match object:\n"+str(matchObj))
        if matchObj != None:
            if config.Config.debug:
                print("Group1:\n"+matchObj.group(1))
                print("Group2:\n"+matchObj.group(2))
            returnValue = []
            returnValue.append(str(matchObj.group(1)))
            returnValue.append(str(matchObj.group(2)))
    return returnValue
