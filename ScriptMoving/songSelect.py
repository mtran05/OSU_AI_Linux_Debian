import time
import os
import json
import pyautogui
pyautogui.FAILSAFE = False

with open(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "config.json")) as config:
    configDict = json.load(config)
    xOffSet = configDict["osuConfig"]["XOffSet"]
    yOffSet = configDict["osuConfig"]["YOffSet"]
    yOffSetMargin = configDict["osuConfig"]["YOffSetMargin"]
    yOffTotal = yOffSet + yOffSetMargin

def chooseSong():
    time.sleep(8)
    
    pyautogui.click(20 + xOffSet, 580 + yOffTotal)   # click the back button at bottom left
    time.sleep(1)

    pyautogui.moveTo(430 + xOffSet, 580 + yOffTotal)  # The position changed
    time.sleep(0.5)
    pyautogui.click()           # Shuffle
    time.sleep(3)

    pyautogui.moveTo(780 + xOffSet, 580 + yOffTotal)
    time.sleep(0.5)
    pyautogui.click()