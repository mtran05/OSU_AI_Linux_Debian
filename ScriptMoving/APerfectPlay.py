import requests
import json
import time
import os
from getUnixTime import getUnixTimeTest
from extractCoords import extractCoords
from extractBeatmap import extractBeatmap
import pyautogui
pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = False

# * --------------------------Test-------------------------- *
# ! Key Error: Likely because of duplicate map's name folder?

with open(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "config.json")) as config:
    configDict = json.load(config)
    xOffSet = configDict["osuConfig"]["XOffSet"]
    yOffSet = configDict["osuConfig"]["YOffSet"]
    yOffSetMargin = configDict["osuConfig"]["YOffSetMargin"]
    yOffTotal = yOffSet + yOffSetMargin

def perfectPlay():
    res = requests.get('http://127.0.0.1:24050/json/v2')
    response = json.loads(res.text)
    df = extractBeatmap(response)

    startTime = None
    while startTime == None:
        startTime = getUnixTimeTest()
        print(startTime)
    
    stopTime = startTime + response["beatmap"]["time"]["lastObject"]

    while True:
        if time.time() * 1000 > stopTime:
            break

        x, y = extractCoords(startTime, df)
        if (x == None or y == None):
            continue
        
        scale = 5.0/4.0
        x = (x * scale + 80) + xOffSet
        y = (y * scale + 70) + yOffTotal
        
        currentX, currentY = pyautogui.position()
        
        pyautogui.moveRel(x - currentX, y - currentY)

# def randomMove():
#     res = requests.get('http://127.0.0.1:24050/json/v2')
#     response = json.loads(res.text)
#     stopTime = response["beatmap"]["time"]["lastObject"]
    
#     lastTime = time.time()
#     while (time.time() - lastTime) < stopTime/1000:
#         pyautogui.moveRel(random.randint(-10, 10), random.randint(-10, 10))
#         time.sleep(0.01)

# if __name__ =="__main__":
    
#     t1 = threading.Thread(target=randomMove, args=([]))
#     t2 = threading.Thread(target=perfectPlay, args=())

#     t1.start()
#     t2.start()
    
#     t1.join()
#     t2.join()

#     print("Done!")

# !
time.sleep(1)
perfectPlay()