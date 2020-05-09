import time, json, urllib
from time import sleep as s
from urllib import request as r
from urllib import parse as p

aboutProg = "Godville Diary Logger. Created by Silent Underfined Box(SileboxUnderfined), 2020"
version = 0.2
phrases = {
    "quest":{    
        "nameOfGod":"Введите имя бога: ",
        "apiKey":"Введите API ключ: ",
        "countOfCycles":"Введите кол-во циклов, после которых начинается запись действий в дневник: ",
        "sleepCount":"Введите кол-во секунд, которые надо ожидать до следующей фразы(не меньше 60!): "
    },
    "default":{
        "inited":"инициализирован ли settings.json: ",
        "nameOfGod":"Имя бога: ",
        "apiKey":"API ключ: ",
        "countOfCycles":"Кол-во циклов, после которых начинается запись действий в дневник: ",
        "sleepCount":"Кол-во секунд, после которых заканчивается цикл: "
    }    
}

def enterMainValues():
    mainValuesDict = {"inited":1}
    mainValues = list()
    phrasesForQuest = phrases["quest"]
    for i in phrasesForQuest:
        try:
            tmp = input(phrasesForQuest[i])
            int(tmp)
        except ValueError:
            None    

        mainValuesDict.update({i:tmp})
        mainValues.append(tmp)

    settingsFileOpenWrite = open("settings.json","w")
    json.dump(mainValuesDict,settingsFileOpenWrite)
    settingsFileOpenWrite.close()

def init():
    global fileName, jsonFileUrl, inited
    try:
        settingsFileOpenRead = open("settings.json",'r')
    except FileNotFoundError:
        print("файл с настройками не найден!")
        enterMainValues()
        init()

    settingsFile = json.load(settingsFileOpenRead)
    settingsFileOpenRead.close()
    if settingsFile["inited"] == 0:
        enterMainValues()
        init()

    mainValues = dict()
    phrasesD = phrases["default"]
    for i in settingsFile:
        mainValues.update({i:settingsFile[i]})
        print(phrasesD[i] + str(settingsFile[i]))

    print('Вы хотите изменить персонажа? 1 - да, enter - нет')
    ch = input(">> ")
    if ch == "1":
        enterMainValues()
        init()    

    fileName = input("Введите название файла, в который надо логгировать(без расширения): ")
    fileName = fileName + ".txt"
    try:
        f = open(fileName, 'r')
        print('Продолжим запись уже в существующий файл {}'.format(fileName))   
 
    except FileNotFoundError:
        f = open(fileName,"w")
        print('файл {} создан'.format(fileName))
        f.close()    

    jsonFileUrl = "http://www.godville.net/gods/api/{gn}/{apik}".format(gn=p.quote(mainValues["nameOfGod"]),apik=p.quote(mainValues["apiKey"]))
    countOfCycles = int(mainValues["countOfCycles"])
    sleepCount = int(mainValues["sleepCount"])
    inited = tuple((countOfCycles,sleepCount))

def receive_json_obj():
    gotFile = r.urlopen(jsonFileUrl).read()
    objOfJSON = json.loads(gotFile)
    strOfJSON = objOfJSON["diary_last"]
    return strOfJSON

def writeInFile(diaryMSGList):
    print('считываем файл, получаем строку')
    CustomFileRead = open(fileName, "r")
    stringFromReadFile = CustomFileRead.read()
    print("Получили строку")
    CustomFileRead.close()
    print("файл на чтение закрыт")
    print('Начинается запись дневника в файл')
    CustomfileWrite = open(fileName,"w")
    strToWrite = stringFromReadFile
    for i in diaryMSGList:
        strToWrite = strToWrite + i + '\n'

    CustomfileWrite.write(strToWrite)
    print("В файл успешно записано {} фраз!".format(len(diaryMSGList)))
    CustomfileWrite.close()
    print("Файл закрыт")    

def main(mainF):
    diaryLastMSG = receive_json_obj()
    timestr = time.strftime("%X",time.localtime())   
    diaryLastMSG = timestr + ": " + diaryLastMSG    
    if diaryLastMSG not in mainF[1]: 
        print(diaryLastMSG)
        mainF[1].append(diaryLastMSG)

    if inited[1] < 60:
        print("Перепишите так, чтобы было больше 60 секунд!")
        init()

    s(inited[1])
    mainF[0] += 1    
    if mainF[0] == inited[0]:
        writeInFile(mainF[1])
        mainF[0] = 0
        mainF[1].clear()

    main(mainF)

def closeProg():
    input("Нажмите Enter, чтобы завершить работу: ")
    quit()

if __name__ == "__main__":
    print(aboutProg)
    print("Версия: {}".format(version))
    countOfCycles = 0
    diaryMSGList = list()
    mainF = [countOfCycles,diaryMSGList]
    init()        
    main(mainF)