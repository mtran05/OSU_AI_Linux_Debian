import time
import pyautogui
pyautogui.FAILSAFE = False

max_x, max_y = pyautogui.size()     # Osu sub-screen 1280x1024

def chooseSong():
    time.sleep(8)
    
    pyautogui.click(0, max_y)   # click the back button at bottom left
    time.sleep(1)

    x, y = pyautogui.locateCenterOnScreen('../Images/Shuffle.png', grayscale=True, confidence=0.8)
    pyautogui.click(x, y)
    time.sleep(3)

    pyautogui.click(max_x, max_y)
    time.sleep(2)
    pyautogui.click()   # skip cut-scene