import subprocess
import time
import pyautogui
import numpy as np
import os
import json
from PIL import ImageGrab
import cv2
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from screenshot import getState

"""------------------------------------------------------------------------------------------------------"""
with open(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "config.json")) as config:
    configDict = json.load(config)
    pathToOsuExe = configDict["system"]["pathToOsuExe"]
    Width = configDict["osuConfig"]["Width"]
    Height = configDict["osuConfig"]["Height"]
    xOffSet = configDict["osuConfig"]["XOffSet"]
    yOffSet = configDict["osuConfig"]["YOffSet"]
    yOffSetMargin = configDict["osuConfig"]["YOffSetMargin"]
    yOffTotal = yOffSet + yOffSetMargin

# * Boot up run *
def bootNavigation():
    # subprocess.Popen("sudo " + os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Tosu/tosu"), shell=True)
    # subprocess.Popen(f"sudo {pathToOsuExe}", shell=True)
    # time.sleep(15)

    osuID = subprocess.check_output("xdotool search --onlyvisible --name osu!", shell=True, text=True).strip()
    subprocess.run(f"xdotool windowactivate {osuID}", shell=True)
    subprocess.run(f"xdotool windowsize {osuID} {Width} {Height}", shell=True)
    subprocess.run(f"xdotool windowmove {osuID} {xOffSet} {yOffSet}", shell=True)

    # * Osu AI view frame code
    Screen = np.array(ImageGrab.grab(bbox=(xOffSet, yOffTotal, Width + xOffSet, Height + yOffTotal), xdisplay=":0"))
    gray = cv2.cvtColor(Screen, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Osu!AI_View', gray)
    time.sleep(0.5)
    
    # Linux Compatible Piece of Code
    getState()
    time.sleep(0.5)
    
    # * Osu AI view frame code
    osuAI_ID = subprocess.check_output("xdotool search --onlyvisible --name Osu!AI_View", shell=True, text=True).strip()
    subprocess.run(f"xdotool windowmove {osuAI_ID} {xOffSet} {Height + 600}", shell=True)
    time.sleep(0.5)

    # Other Operations
    subprocess.run(f"xdotool windowactivate {osuID}", shell=True)
    pyautogui.moveTo(Width/2 + xOffSet, Height/2 + yOffTotal)
    time.sleep(0.5)
    pyautogui.click()   # Click the big OSU! icon in the middle
    time.sleep(1)
    pyautogui.click()   # Click the Play icon in the middle
    time.sleep(1)
    pyautogui.click()   # Click the Solo icon in the middle
    time.sleep(1)

    pyautogui.moveTo(270 + xOffSet, 580 + yOffTotal)
    time.sleep(0.5)
    pyautogui.click()           # Shuffle
    time.sleep(1)

    pyautogui.moveTo(200 + xOffSet, 580 + yOffTotal)
    time.sleep(0.5)
    pyautogui.click()   # Open Mode list
    time.sleep(1)
    pyautogui.moveTo(200 + xOffSet, 200 + yOffTotal)
    time.sleep(0.5)
    pyautogui.click()   # Pre-set Modes for Moving
    time.sleep(1)

    pyautogui.moveTo(100 + xOffSet, 570 + yOffTotal)  # Close mode list
    time.sleep(0.5)
    pyautogui.click()
    time.sleep(1)

    pyautogui.moveTo(780 + xOffSet, 580 + yOffTotal)
    time.sleep(0.5)
    pyautogui.click()