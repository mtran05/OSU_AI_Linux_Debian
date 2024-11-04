import requests
import json
import time
import random
import threading
from extractCoords import extractCoords
from extractBeatmap import extractBeatmap
from humancursor import SystemCursor
import pyautogui
pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = False

# * --------------------------Test-------------------------- *
# ! Key Error: Likely because of duplicate map's name folder?

def perfectPlay():
    res = requests.get('http://127.0.0.1:24050/json/v2')
    response = json.loads(res.text)
    df = extractBeatmap(response)

    cursor = SystemCursor()     # ! TEST

    while True:
        res = requests.get('http://127.0.0.1:24050/json/v2')
        response = json.loads(res.text)

        liveTime = response["beatmap"]["time"]["live"]
        timeObject = response["beatmap"]["time"]

        if liveTime > timeObject["lastObject"]:
            break
        
        # * ------------- *

        x, y = extractCoords(response, df)
        if (x == None or y == None):
            continue
        
        scale = 5.0/4.0
        x = int(x * scale) + 80
        y = int(y * scale) + 70
        pyautogui.moveTo(x, y)

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
perfectPlay()