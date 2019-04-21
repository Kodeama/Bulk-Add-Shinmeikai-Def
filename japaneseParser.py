#    hira = "あいうえおかきくけこがぎぐげごさしすせそざじずぜぞたちつてとだぢづでどなにぬねのはひふへほばびぶべぼぱぴぷぺぽまみむめもやゆよらりるれろわゐゑをんっゃゅょ"
import config, re

dict = open(config.Config.wordFreqList, "rb")
contents = dict.read().decode("UTF-8")
dict.close()

dict = open(config.Config.kanjiList, "rb")
kanjiList = dict.read().decode("UTF-8")
dict.close()

#Returns boolean depending on if string contains kanji or not
def stringContainsKanji(inputString):
    debugOutput = "Checks if string contains kanji...\nSting: "+ inputString
    for c in inputString:
        debugOutput += "\n"+c+": "+str(hex(ord(c)))
        #Checks if codepoint of character is anything but hiragana/katakana
        if ord(c) < 12353 or ord(c) > 12543:
            if config.Config.debug:
                print(debugOutput+"\nTrue, string does contain kanji\n")
            return True
    if config.Config.debug:
        print(debugOutput+"\nFalse, string does not contain kanji\n")
    return False

def getWordFreq(hira, kanji):
    hira = str(hira)
    kanji = str(kanji)

    regex = u""+kanji+"	"+hira+"	(.*?)	"
    if config.Config.debug:
        print("getWordFreq regex:\n"+regex)
    matchObj = re.search(regex, contents)

    if matchObj == None:
        if config.Config.debug:
            print("Frequency of word: "+kanji+"["+hira+"] not found in "+config.Config.wordFreqList+"\nError in japaneseParser.py at line 28")
        return 999999 #Just something high so the sort gets this word to the back of the list

    if config.Config.debug:
        print("Frequency of word: "+kanji+"["+hira+"] is: "+str(matchObj.group(1)))

    return matchObj.group(1)

def getRTKKeyword(kanji):
    kanjiFound = False
    kanjiField = ""
    keywordList = []
    #print("recieved kanji len: "+ str(len(kanji)))
    for x in range(0, len(kanji)):
        #print(str(x))
        if stringContainsKanji(kanji[x]):
            #print("Contained kanji")
            regex = kanji[x]+u"\t(.*)"
            keyword = re.search(regex, kanjiList)
            #print("Keywords: "+str(keyword))
            if keyword != None:
                if kanjiFound:
                    kanjiField += "<div></div>"
                kanjiField += u""+kanji[x]
                kanjiField += " "+str(keyword.group(1)).replace("\r","")
                kanjiFound = True
                #print("Found kanji: "+kanji[x]+" = "+keyword.group(1))
    #print(kanjiField)
    return str(kanjiField)
