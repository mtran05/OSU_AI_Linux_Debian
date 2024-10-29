import os
import sys
sys.path.append("C:\\Users\\qttra\\OneDrive\\Documents\\GitHub\\OSU_AI\\Parser")

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
    return df