import requests
import json
import time

def getUnixTime():
    res = requests.get('http://127.0.0.1:24050/json/v2')
    response = json.loads(res.text)
    
    liveTime = response["beatmap"]["time"]["live"]
    firstObject = response["beatmap"]["time"]["firstObject"]
    
    if response["client"] == "standard" and firstObject > liveTime and firstObject - liveTime < 300:
        return time.time() * 1000 - liveTime
    
    elif response["client"] == "lazer":
        res2 = requests.get('http://127.0.0.1:24050/json/v2')
        response2 = json.loads(res2.text)

        liveTime2 = response2["beatmap"]["time"]["live"]
    
        if liveTime != liveTime2 and (firstObject - liveTime2 < 300 or liveTime2 > firstObject):
            return time.time() * 1000 - liveTime2
    
    return None


def getUnixTimeTest():
    res = requests.get('http://127.0.0.1:24050/json/v2')
    response = json.loads(res.text)
    
    liveTime = response["beatmap"]["time"]["live"]
    firstObject = response["beatmap"]["time"]["firstObject"]
    
    if response["client"] == "standard" and firstObject > liveTime and firstObject - liveTime < 300:
        return time.time() * 1000 - liveTime
    
    elif response["client"] == "lazer":
        res2 = requests.get('http://127.0.0.1:24050/json/v2')
        response2 = json.loads(res2.text)

        liveTime2 = response2["beatmap"]["time"]["live"]
    
        if liveTime != liveTime2 and abs(firstObject - liveTime2) < 300:
            return time.time() * 1000 - liveTime2
    
    return None