import subprocess
import time
import pyautogui

osu = subprocess.Popen(['C:\\Users\\qttra\\AppData\\Local\\osu!\\osu!.exe'])
tosu = subprocess.Popen(['C:\\Users\\qttra\\OneDrive\\Documents\\GitHub\\OSU_AI\\Tosu\\tosu.exe'])
time.sleep(12)

"""------------------------------------------------------------------------------------------------------"""

# * Boot up run *

np = pyautogui.getActiveWindow()
np.moveTo(-3, -37)           # Move OSU! to top left & Get rid of top navigation (margin on the left too)
max_x, max_y = np.size       # Osu sub-screen 800x600
max_x, max_y = [max_x - 6, max_y - 40]      # ! extra -3 to also disregard margin on reminding sides
time.sleep(0.5)

# ! START OF DEBUGGING !

# pyautogui.moveTo(700, 500)
# print("Moved to 700, 500")
# time.sleep(10)

# pyautogui.moveTo(1500, 1500)
# print("Moved to 1500, 1500")
# time.sleep(10)

# ! END OF DEBUGGING !

pyautogui.click(max_x/2, max_y/2)   # Click the big OSU! icon in the middle
time.sleep(0.5)

x, y = pyautogui.locateCenterOnScreen('../Images/PlayHorizontal.png', grayscale=True, confidence=0.8)
pyautogui.click(x, y)
time.sleep(0.5)

x, y = pyautogui.locateCenterOnScreen('../Images/Solo.png', grayscale=True, confidence=0.8)
pyautogui.click(x, y)
time.sleep(1)

pyautogui.click(x, y)     # Click the OsuAI collection
time.sleep(0.5)

x, y = pyautogui.locateCenterOnScreen('../Images/Shuffle.png', grayscale=True, confidence=0.8)
pyautogui.click(x, y)
time.sleep(0.5)

pyautogui.click(x-50, y)        # Mode list
time.sleep(0.5)
pyautogui.click(x+70, y-220)   # Choose mode
time.sleep(0.5)

x, y = pyautogui.locateCenterOnScreen('../Images/Close.png', grayscale=True, confidence=0.8)
pyautogui.click(x, y)   # Close mode list
time.sleep(1)

pyautogui.click(max_x, max_y)
time.sleep(2)
pyautogui.click()   # skip cut-scene

"""------------------------------------------------------------------------------------------------------"""

# Run training for Clicking task
subprocess.run('python trainClicking.py', shell=True, check=False)

# osu.wait()
# tosu.wait()