import time
import pyautogui
pyautogui.FAILSAFE = False

def chooseSong():
    time.sleep(8)
    
    pyautogui.click(20, 580)   # click the back button at bottom left
    time.sleep(1)

    pyautogui.moveTo(430, 580)  # The position changed
    time.sleep(0.5)
    pyautogui.click()           # Shuffle
    time.sleep(3)

    pyautogui.moveTo(790, 590)
    time.sleep(0.5)
    pyautogui.click()