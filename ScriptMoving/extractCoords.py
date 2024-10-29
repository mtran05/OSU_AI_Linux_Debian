import sys
sys.path.append("C:\\Users\\qttra\\OneDrive\\Documents\\GitHub\\OSU_AI\\Parser")

import numpy as np
from curve import Bezier
from slidercalc import rotate, get_circum_circle
from extractBeatmap import extractBeatmap

# * --------------- *

def extractCoords(response, df):
    timeObject = response["beatmap"]["time"]
    hits = response["play"]["hits"]
    
    hitObject = 0
    for x, y in hits.items():
        if x == "geki":     # we don't care about `geki` onwards
            break
        hitObject += y

    liveTime = timeObject["live"]
    x, y = [None, None]
    
    if df.loc[hitObject, "startTime"] - liveTime > 300:     # * only care if within 300ms *
        return x, y
    
    # * ----------------- *
    
    if df.loc[hitObject, "object_name"] == "circle":
        x, y = df.loc[hitObject, "position"]
        return x, y
    
    elif df.loc[hitObject, "object_name"] == "slider":
        repeatCount = int(df.loc[hitObject, "repeatCount"])
        sliderPercent = (liveTime - df.loc[hitObject, "startTime"])/df.loc[hitObject, "duration"]
        
        if sliderPercent < 0:
            x, y = df.loc[hitObject, "position"]
            return x, y
        
        if df.loc[hitObject, "curveType"] == "bezier":
            
            for i in range(1, repeatCount + 1):
                if ((liveTime - df.loc[hitObject, "startTime"]) <= (df.loc[hitObject, "duration"] / repeatCount) * i):
                    progress = (sliderPercent - (i-1) / repeatCount) * repeatCount
                    if (i % 2 != 0):
                        bz = Bezier(df.loc[hitObject, "points"])
                        x, y = bz.at(progress)
                        return x, y
                    else:
                        bz = Bezier(df.loc[hitObject, "points"][::-1])  # ! Backwards
                        x, y = bz.at(progress) 
                        return x, y
        
        elif df.loc[hitObject, "curveType"] == "pass-through":
            # ?? p1, p2, p3 = [*df.loc[hitObject, "points"][:2], df.loc[hitObject, "end_position"]]
            p1, p2, p3 = df.loc[hitObject, "points"]
            
            try:
                cx, cy, radius = get_circum_circle(p1, p2, p3)
                radians = df.loc[hitObject, "pixelLength"] / radius

                matrix = np.array([p1, p2, p3])
                matrix = np.concatenate((matrix, [[1],[1],[1]]), axis=1)
                det = np.linalg.det(matrix)

                if det < 0:
                    sign = -1   # ! - radians if counter-clockwise
                elif det > 0:
                    sign = 1    # ! + radians if clockwise

                for i in range(1, repeatCount + 1):
                    if ((liveTime - df.loc[hitObject, "startTime"]) <= (df.loc[hitObject, "duration"] / repeatCount) * i):
                        progress = (sliderPercent - (i-1) / repeatCount) * repeatCount
                        if (i % 2 != 0):
                            x, y = rotate(cx, cy, p1[0], p1[1], sign * radians * progress)
                            return x, y
                        else:
                            x, y = rotate(cx, cy, p3[0], p3[1], -1 * sign * radians * progress)
                            return x, y

            except ValueError:
                for i in range(1, repeatCount + 1):
                    if ((liveTime - df.loc[hitObject, "startTime"]) <= (df.loc[hitObject, "duration"] / repeatCount) * i):
                        progress = (sliderPercent - (i-1) / repeatCount) * repeatCount
                        if (i % 2 != 0):
                            x, y = interpolate_point(p1, p3, progress)
                            return x, y
                        else:
                            x, y = interpolate_point(p3, p1, progress)   # ! Backwards: swap p1 & p2
                            return x, y

        elif df.loc[hitObject, "curveType"] == "linear":
            # ?? p1, p2 = [df.loc[hitObject, "position"], df.loc[hitObject, "end_position"]]
            p1, p2 = df.loc[hitObject, "points"]
            
            for i in range(1, repeatCount + 1):
                if ((liveTime - df.loc[hitObject, "startTime"]) <= (df.loc[hitObject, "duration"] / repeatCount) * i):
                    progress = (sliderPercent - (i-1) / repeatCount) * repeatCount
                    if (i % 2 != 0):
                        x, y = interpolate_point(p1, p2, progress)
                        return x, y
                    else:
                        x, y = interpolate_point(p2, p1, progress)   # ! Backwards: swap p1 & p2
                        return x, y
    
    elif df.loc[hitObject, "object_name"] == "spinner":
        x, y = 256, 192
        return x, y
    
    return x, y

# * Helper Function *
def interpolate_point(p1, p2, percentage):
    x1, y1 = p1
    x2, y2 = p2

    # Calculate the interpolated coordinates
    x = x1 + percentage * (x2 - x1)
    y = y1 + percentage * (y2 - y1)

    return x, y

# * --------------------------Test-------------------------- *
# ! Key Error: Likely because of duplicate map's name folder?
# import requests
# import json
# import time
# import pyautogui
# pyautogui.PAUSE = 0.01
# pyautogui.FAILSAFE = False

# res = requests.get('http://127.0.0.1:24050/json/v2')
# response = json.loads(res.text)
# df = extractBeatmap(response)

# while True:
#     res = requests.get('http://127.0.0.1:24050/json/v2')
#     response = json.loads(res.text)

#     liveTime = response["beatmap"]["time"]["live"]
#     timeObject = response["beatmap"]["time"]
    
#     if liveTime > timeObject["lastObject"]:
#         break
    
#     # * ------------- *
    
#     x, y = extractCoords(response, df)
#     if (x == None or y == None):
#         continue
    
#     scale = 5.0/4.0
#     x = x * scale + 80
#     y = y * scale + 70
#     pyautogui.moveTo(x, y)