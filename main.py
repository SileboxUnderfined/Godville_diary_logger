import time, json, urllib
from time import sleep as s
from urllib import request as r
from urllib import parse as p
from os.path import isfile

aboutProg = "Godville Diary Logger. Created by Silent Underfined Box(SileboxUnderfined), 2020"
version = 0.1

def enterMainValues():
    apiKey = input("Введите API ключ: ")    
    godName = input("Введите имя бога: ")    
    countOfCycles = input("Введите кол-во циклов, после которых начинается запись действий в дневник: ")
    mainValuesDict = {"nameOfGod":godName,"apiKey":apiKey,"countOfCycles":countOfCycles}
    mainValues = list((godName,apiKey,countOfCycles))
    settingsFileOpenWrite = open("settings.json","w")
    json.dump(mainValuesDict,settingsFileOpenWrite)
    settingsFileOpenWrite.close()
    return mainValues

def init():
    global initCount
    if isfile("settings.json") == False:
        print("Файл settings.json не найден! Начинаю создание нового")
        enterMainValues()

    settingsFileOpenRead = open("settings.json",'r')
    settingsFile = json.load(settingsFileOpenRead)
    settingsFileOpenRead.close()
    mainValues = None
    if settingsFile["nameOfGod"] == "" or settingsFile["apiKey"] == "":
        mainValues = enterMainValues()

    else:
        godName = settingsFile["nameOfGod"]
        apiKey = settingsFile["apiKey"]
        maxCountOfCycles = settingsFile["countOfCycles"]
        maxCountOfCycles = int(maxCountOfCycles)
        mainValues = list((godName,apiKey,maxCountOfCycles))
        print("имя бога: {}".format(mainValues[0]))
        print("API ключ: {}".format(mainValues[1]))
        print("Кол-во циклов, после которых начинается запись: {}".format(mainValues[2]))
        print('Вы хотите изменить персонажа? 1 - да, enter - нет')
        ch = input(">> ")
        if ch == "1":
            mainValues = enterMainValues()    

    global fileName
    fileName = input("Введите название файла, в который надо логгировать(без расширения): ")
    fileName = fileName + ".txt"
    if isfile(fileName) == False:
        f = open(fileName, 'w')
        print('файл {} создан'.format(fileName))
        f.close()
    else:
        print('Продолжим запись уже в существующий файл {}'.format(fileName))    

    jsonFileUrl = "http://www.godville.net/gods/api/{gn}/{apik}".format(gn=p.quote(mainValues[0]),apik=p.quote(mainValues[1]))
    initCount = 1
    return tuple((jsonFileUrl,fileName,maxCountOfCycles))

def receive_json_obj(jsonFileUrl):
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


def main(inited, mainF):
    countOfCycles = mainF[0]
    diaryMSGList = mainF[1]
    if initCount == 0:
        bInited = init()
        inited[0] = bInited[0]
        inited[1] = bInited[1]
        inited[2] = bInited[2]

    diaryLastMSG = receive_json_obj(inited[0])
    if diaryLastMSG not in diaryMSGList: 
        timestr = time.strftime("%X",time.localtime())   
        diaryLastMSG = timestr + ": " + diaryLastMSG
        print(diaryLastMSG)
        diaryMSGList.append(diaryLastMSG)

    print(countOfCycles)
    print(inited[2])
    s(60)
    countOfCycles += 1    
    if countOfCycles == inited[2]:
        writeInFile(diaryMSGList)
        countOfCycles = 0
        diaryMSGList.clear()

    mainF[0] = countOfCycles
    mainF[1] = diaryMSGList
    main(inited,mainF)

if __name__ == "__main__":
    print(aboutProg)
    print("Версия: {}".format(version))
    global initCount
    inited = list(("","",""))
    countOfCycles = 0
    initCount = 0
    diaryMSGList = list()
    mainF = [countOfCycles,diaryMSGList]    
    main(inited,mainF)