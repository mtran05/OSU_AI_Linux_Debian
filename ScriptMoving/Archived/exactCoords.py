import os
import sys
sys.path.append("C:\\Users\\qttra\\OneDrive\\Documents\\GitHub\\OSU_AI\\Parser")

import pyautogui
pyautogui.PAUSE = 0.01     # ! IMPORTANT

import time
import datetime
import requests
import json
import numpy as np
import pandas as pd
pd.set_option('display.max_rows', None)

import beatmapparser
from curve import Bezier
from slidercalc import rotate, get_circum_circle
from CoordsHelper import interpolate_point

# * --------------- *
# get Songs folder
osu_songs_directory = os.path.join(os.getenv('LOCALAPPDATA'), 'osu!', 'Songs')

# fetch
res1st = requests.get('http://127.0.0.1:24050/json/v2')
response1st = json.loads(res1st.text)
beatmap = response1st["beatmap"]

# song dir
maps = os.listdir(osu_songs_directory)
selectedMapFolder = [x for x in maps if beatmap["title"] in x]

# get osu path
osuMap = f"{beatmap["artist"]} - {beatmap["title"]} ({beatmap["mapper"]}) [{beatmap["version"]}].osu"
osu_path = os.path.join(osu_songs_directory, selectedMapFolder[0], osuMap)
print(osu_path)

# init parser
parser = beatmapparser.BeatmapParser()

# Parse File
currentTime = datetime.datetime.now()
parser.parseFile(osu_path)
print("Parsing done. Time: ", (datetime.datetime.now() - currentTime).microseconds / 1000, 'ms')

# Build Beatmap
currentTime = datetime.datetime.now()
parser.build_beatmap()
print("Building done. Time: ", (datetime.datetime.now() - currentTime).microseconds / 1000, 'ms')

# Load into DataFrame
df = pd.DataFrame(parser.beatmap["hitObjects"])

# ! DEBUG
time.sleep(2)
# ! END OF DEBUG

x = 800
y = 600

while True:
    res = requests.get('http://127.0.0.1:24050/json/v2')
    response = json.loads(res.text)
    timeObject = response["beatmap"]["time"]
    hits = response["play"]["hits"]
    
    hitObject = 0
    for x, y in hits.items():
        if x == "geki":     # we don't care about `geki` onwards
            break
        hitObject += y

    liveTime = timeObject["live"]
    
    # * !
    if liveTime > timeObject["lastObject"]:
        break
    if df.loc[hitObject, "startTime"] - liveTime > 300:     # only care if within 300ms
        continue
    # * !
            
    if df.loc[hitObject, "object_name"] == "circle":
        x, y = df.loc[hitObject, "position"]
    
    elif df.loc[hitObject, "object_name"] == "slider":
        repeatCount = int(df.loc[hitObject, "repeatCount"])
        sliderPercent = (liveTime - df.loc[hitObject, "startTime"])/df.loc[hitObject, "duration"]
        if sliderPercent < 0:
            continue
        
        if df.loc[hitObject, "curveType"] == "bezier":
            
            for i in range(1, repeatCount + 1):
                if ((liveTime - df.loc[hitObject, "startTime"]) <= (df.loc[hitObject, "duration"] / repeatCount) * i):
                    progress = (sliderPercent - (i-1) / repeatCount) * repeatCount
                    if (i % 2 != 0):
                        bz = Bezier(df.loc[hitObject, "points"])
                        x, y = bz.at(progress)
                        break
                    else:
                        bz = Bezier(df.loc[hitObject, "points"][::-1])  # ! Backwards
                        x, y = bz.at(progress) 
                        break
        
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
                            break
                        else:
                            x, y = rotate(cx, cy, p3[0], p3[1], -1 * sign * radians * progress)      # ! plz test   (may need to multiply -1?)
                            break

            except ValueError:
                for i in range(1, repeatCount + 1):
                    if ((liveTime - df.loc[hitObject, "startTime"]) <= (df.loc[hitObject, "duration"] / repeatCount) * i):
                        progress = (sliderPercent - (i-1) / repeatCount) * repeatCount
                        if (i % 2 != 0):
                            x, y = interpolate_point(p1, p3, progress)
                            break
                        else:
                            x, y = interpolate_point(p3, p1, progress)   # ! Backwards: swap p1 & p2
                            break

        elif df.loc[hitObject, "curveType"] == "linear":
            # ?? p1, p2 = [df.loc[hitObject, "position"], df.loc[hitObject, "end_position"]]
            p1, p2 = df.loc[hitObject, "points"]
            
            for i in range(1, repeatCount + 1):
                if ((liveTime - df.loc[hitObject, "startTime"]) <= (df.loc[hitObject, "duration"] / repeatCount) * i):
                    progress = (sliderPercent - (i-1) / repeatCount) * repeatCount
                    if (i % 2 != 0):
                        x, y = interpolate_point(p1, p2, progress)
                        break
                    else:
                        x, y = interpolate_point(p2, p1, progress)   # ! Backwards: swap p1 & p2
                        break
    
    # ?? elif df.loc[hitObject, "object_name"] == "spinner":
        # ??
    
    scale = 5.0/4.0
    x = x * scale + 80
    y = y * scale + 70
    pyautogui.moveTo(x, y)