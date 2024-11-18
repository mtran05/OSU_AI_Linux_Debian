import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Parser"))

import re
import datetime
import pandas as pd
import beatmapparser

# * ------------- *

def extractBeatmap(response):
    # get Songs folder
    osu_songs_directory = os.path.join(os.getenv('LOCALAPPDATA'), 'osu!', 'Songs')
    beatmap = response["beatmap"]

    # song dir
    maps = os.listdir(osu_songs_directory)
    tokensTitle = response["beatmap"]["title"].split()
    
    # mass select map folders
    selectedMapFolder = []
    for map in maps:
        for token in tokensTitle:
            if token in map:
                selectedMapFolder.append(map)
                break
    # print(selectedMapFolder)

    # get osu path
    # osuMap = f"{beatmap["artist"]} - {beatmap["title"]} ({beatmap["mapper"]}) [{beatmap["version"]}].osu"
    osu_path = None
    for folder in selectedMapFolder:
        # print(folder)
        songsFound = os.listdir(os.path.join(osu_songs_directory, folder))
        songs = [songFile for songFile in songsFound if re.match(r'.*\.osu$', songFile)
                and (re.sub(r'\?', '', f"[{beatmap["version"]}].osu").lower() in songFile.lower())
                and beatmap["artist"].split(":")[0].lower() in songFile.lower() 
                and beatmap["mapper"].lower() in songFile.lower()]
        
        if not songs:
            songs = [songFile for songFile in songsFound if re.match(r'.*\.osu$', songFile)
                and re.sub(r'[^a-zA-Z0-9\s\'\"()!]', '', beatmap["version"]).lower() in songFile.lower() 
                and beatmap["artist"].split(":")[0].lower() in songFile.lower() 
                and beatmap["mapper"].lower() in songFile.lower()]
            if not songs:
                continue
        
        song = songs[0]
        
        if os.path.isfile(os.path.join(osu_songs_directory, folder, song)):
            osu_path = os.path.join(osu_songs_directory, folder, song)
            break
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
    return df

# * --------------------------Test-------------------------- *
# import requests
# import json
# import time

# res = requests.get('http://127.0.0.1:24050/json/v2')
# response = json.loads(res.text)
# df = extractBeatmap(response)
# print(df.loc[:10, ["startTime", "position", "object_name", "repeatCount", "pixelLength", "curveType", "points", "duration", "end_time", "end_position"]])


# while(True):
#     res = requests.get('http://127.0.0.1:24050/json/v2')
#     response = json.loads(res.text)
#     df = extractBeatmap(response)
#     time.sleep(5)