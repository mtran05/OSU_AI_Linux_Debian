import subprocess
import time
import pyautogui
import numpy as np
from PIL import ImageGrab
import cv2

"""------------------------------------------------------------------------------------------------------"""

# * Boot up run *
def bootNavigation():
    osu = subprocess.Popen(['C:\\Users\\qttra\\AppData\\Local\\osulazer\\current\\osu!.exe'])
    tosu = subprocess.Popen(['C:\\Users\\qttra\\OneDrive\\Documents\\GitHub\\OSU_AI\\Tosu\\tosu.exe'])
    time.sleep(12)

    AllWindows = pyautogui.getAllWindows()
    osuWindow = [AllWindows[i] for i in range(len(AllWindows)) if AllWindows[i].title == "osu!"][0]
    osuWindow.activate()
    
    osuWindow.resize(822 - osuWindow.width, 656 - osuWindow.height)
    osuWindow.moveTo(-13, -47)          # Move OSU! to top left & Get rid of top navigation (margin on the left too)
    max_x, max_y = osuWindow.size       # Osu sub-screen 800x600
    max_x, max_y = [max_x - 6, max_y - 40]      # ! extra -3 to also disregard margin on reminding sides
    time.sleep(0.5)

    # * Osu AI view frame code
    Screen = np.array(ImageGrab.grab(bbox=(0, 0, 800, 600)))
    gray = cv2.cvtColor(Screen, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Osu!AI_View', gray)
    time.sleep(0.5)
    
    AllWindows = pyautogui.getAllWindows()
    GrayScaledView = [AllWindows[i] for i in range(len(AllWindows)) if AllWindows[i].title == "Osu!AI_View"][0]
    GrayScaledView.moveTo(0, 700)
    time.sleep(0.5)
    # * Osu AI view frame code

    pyautogui.moveTo(max_x/2, max_y/2)
    time.sleep(0.5)
    pyautogui.click()   # Click the big OSU! icon in the middle
    time.sleep(1)
    pyautogui.click()   # Click the Play icon in the middle
    time.sleep(1)
    pyautogui.click()   # Click the Solo icon in the middle
    time.sleep(1)

    pyautogui.moveTo(270, 580)
    time.sleep(0.5)
    pyautogui.click()           # Shuffle
    time.sleep(1)

    pyautogui.click(200, 580)   # Open Mode list
    time.sleep(1)
    pyautogui.moveTo(200, 200)
    time.sleep(0.5)
    pyautogui.click()   # Pre-set Modes for Moving
    time.sleep(1)

    pyautogui.moveTo(100, 570)  # Close mode list
    time.sleep(0.5)
    pyautogui.click()
    time.sleep(1)

    pyautogui.moveTo(790, 590)
    time.sleep(0.5)
    pyautogui.click()