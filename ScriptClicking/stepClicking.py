import sys
sys.path.append("C:\\Users\\qttra\\OneDrive\\Documents\\GitHub\\OSU_AI")

from screenshot import getState
import pyautogui
import requests
import json

mapping = {
    # Possible rewards for clicking
    '0': -1,   # miss
    '50': 1,
    '100': 3,
    '300': 10,
    
    # Reward for not clicking
    'noClick': 0,
}

""" test1 = {
    "0": 5,
    "50": 1,
    "100": 0,
    "300": 0,
}

test2 = {
    "0": 6,
    "50": 1,
    "100": 0,
    "300": 0,
} """

def getStep(action):    
    if action == 0:
        next_state = getState()
        
        res = requests.get('http://127.0.0.1:24050/json/v2')
        response = json.loads(res.text)
        hits = response["play"]["hits"]
        
        mapAccuracy = response["play"]["accuracy"]
        
        objects = 0
        for x, y in hits.items():
            if x == "geki":     # we don't care about `geki` onwards
                break
            objects += y
        
        isDone = doneCheck(objects, response)
        
        return (next_state, mapping['noClick'], isDone, mapAccuracy)
    
    elif action == 1:
        # Game's data before doing anything
        res_before = requests.get('http://127.0.0.1:24050/json/v2')
        response_before = json.loads(res_before.text)
        hits_before = response_before["play"]["hits"]
        
        # Click & Get Next State (What happens after clicking)
        pyautogui.click()
        next_state = getState()
        
        # Game's data after clicking
        res_after = requests.get('http://127.0.0.1:24050/json/v2')
        response_after = json.loads(res_after.text)
        hits_after = response_after["play"]["hits"]
        
        # Current Accuracy after clicking
        mapAccuracy = response_after["play"]["accuracy"]

        # Compute rewards
        reward = 0
        objects = 0
        for (x, y), (a, b) in zip(hits_before.items(), hits_after.items()):
            if x == "geki":     # we don't care about `geki` onwards
                break
            reward += mapping[x] * abs(b - y)
            objects += b
        
        # Is episode done yet?
        isDone = doneCheck(objects, response_after)
        
        return (next_state, reward, isDone, mapAccuracy)

def doneCheck(objects, response):
    if (objects == response["beatmap"]["stats"]["objects"]["total"]):
        return True
    else:
        return False