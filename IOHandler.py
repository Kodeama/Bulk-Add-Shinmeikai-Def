import sys, codecs, re
import config

#tempString = u"ＮＡＳＡのみんなには 会っとくべきだもんね。		[sound:Uchuu_kyoudai_28_0.10.40.900-0.10.43.890.mp3]	\"<img src=\"\"paste-450473349873667.jpg\"\" />\"		僕			"
#(.*?)	(.*?)	(.*?)	(.*?)	(.*?)	(.*?)	(.*?)	(.*?)	(.*?)
#Read input

readFile = ""
writeFile = ""

class Cards:
    cardArray = []


#Reads input file and returns a list of all rows(cards)
def readFile(systemArgs):
    #Use config location
    if(len(systemArgs) == 1):
        readFile = config.Config.inputFileName
        print("Reading from: " + readFile)
        writeFile = config.Config.outputFileName

    #Use assigned file as read and write file
    elif(len(systemArgs) == 2):
        readFile = systemArgs[1]
        writeFile = systemArgs[1]

    #Use assigned input and output
    elif(len(systemArgs) == 3):
        readFile = systemArgs[1]
        writeFile = systemArgs[2]
    else:
        print("No file detected, try running:\n\"testMain.py <input> <output>\"\nor \"testMain.py -h\" for help")
        sys.exit()

    input = open(readFile, "rb")
    contents = input.read().decode("UTF-8")
    input.close()
    cardArray = contents.splitlines()
    Cards.cardArray = cardArray

    return cardArray

def getTargetFieldFromList(list):
    fieldAmount = getFieldAmountOfList(list)
    regex = generateRegex(fieldAmount)
    targetList = []

    #print(list)
    if config.Config.debug:
        print("Regex: \n"+regex+".\n")

    for x in list:
        targetWord = re.search(regex, str(x))
        #print("TargetWord: " + str(targetWord))
        #print(targetWord.group(config.Config.cardReadFieldIndex))
        targetList.append(targetWord.group(config.Config.cardReadFieldIndex))
    return targetList

def saveDataListToField(fieldIndex, data):
    fieldAmount = getFieldAmountOfList(Cards.cardArray)
    regex = generateRegex(fieldAmount)
    preReg = "" #Pre regex replace expression
    posReg = "" #Post regex repalce expression
    if len(data) != len(Cards.cardArray):
        print("(IOHandler.py:65)\nERROR. Data and CardArray are not the same size!!")
    for y in range(1,fieldAmount+1):
        if y < fieldIndex:
            preReg += "\\"+str(y)+"	"
        elif y > fieldIndex:
            posReg += "\\"+str(y)+"	"

    if config.Config.debug:
        print("ReplaceRegex:\n"+preReg+"MIDDLE	"+posReg)


    for x in range(0, len(data)):
        replaceRegex = preReg+str(data[x])+"	"+posReg
        Cards.cardArray[x] = re.sub(regex, replaceRegex, str(Cards.cardArray[x]))

    #Cards.cardArray[0] = re.sub(regex, replaceRegex, str(Cards.cardArray[0]))
    if config.Config.debug:
        print(Cards.cardArray[0])
    #for x in data:

    return Cards.cardArray

def exportFile(data):

    #export = open(config.Config.outputFileName, "wb")
    #export.write(data)

    with open(config.Config.outputFileName, 'w', encoding="utf-8") as f:
        for item in data:
            f.write("%s\n" % item)
            if config.Config.debug:
                print("Item:\n"+item)

    #export.close()
    return

def generateRegex(fieldAmount):
    regex = "	(.*?)"
    return "(.*?)"+regex*(fieldAmount)

def getFieldAmountOfList(input):
    fieldAmount = len(re.findall(u"	", input[0]))
    if config.Config.debug:
        print("Number of fields found: "+str(fieldAmount))
    return fieldAmount

def updateLoadbar(cur, max):
    loadBardCharWidth = 40
    sys.stdout.write ('\r[{0}{1}] {2} cards'.format('#'*(int((cur/max) * loadBardCharWidth)),' '*(loadBardCharWidth - int(cur/max * loadBardCharWidth)) , str(cur)+"/"+str(max)))
