import datetime
import os
from random import shuffle

import numpy as np
import pandas as pd
pd.set_option('display.max_rows', None)

import beatmapparser

from curve import Bezier    # ! Mason

# Created by Awlex

if __name__ == "__main__":

    # get Songs folder
    osu_songs_directory = os.path.join(os.getenv('LOCALAPPDATA'), 'osu!', 'Songs')

    # List Songs and shuffle the list
    maps = os.listdir(osu_songs_directory)
    shuffle(maps)

    # Pick random map
    map_path = os.path.join(osu_songs_directory, maps[0])
    
    # Custom map
    map_path = os.path.join(osu_songs_directory, "595580 Roselia - LOUDER")

    # Pick first .osu file
    file = [x for x in os.listdir(map_path) if x.endswith(".osu")][2]
    osu_path = os.path.join(map_path, file)
    print(osu_path)

    # init parser
    parser = beatmapparser.BeatmapParser()

    # Parse File
    time = datetime.datetime.now()
    parser.parseFile(osu_path)
    print("Parsing done. Time: ", (datetime.datetime.now() - time).microseconds / 1000, 'ms')

    #Build Beatmap
    time = datetime.datetime.now()
    parser.build_beatmap()
    print("Building done. Time: ", (datetime.datetime.now() - time).microseconds / 1000, 'ms')
    
    # print(parser.beatmap.keys())
    print(parser.beatmap["breakTimes"]) 
    # ! NO NEED, just add a checker: if (nextObjectTime - currentBeatMapTime) < 300 then proceed
    # ! TOSU can help, see `beatmap` attribute -> `time` -> `live`
    
    df = pd.DataFrame(parser.beatmap["hitObjects"])
    print(df.columns)
    # ! ERROR: KeyError: "['repeatCount', 'pixelLength', 'curveType', 'points', 'duration', 'end_time', 'end_position'] not in index"
    # TODO: Check if beatmap contains slider first
    # end_time isn't 100% correct
    print(df.loc[:10, ["startTime", "position", "object_name", "repeatCount", "pixelLength", "curveType", "points", "duration", "end_time", "end_position"]])
    
    """ bz = Bezier([[198, 25], [167, 94], [226, 130], [190, 203]])
    for i in range(0, 101):
        print(bz.at(i/100)) """
    
    a, b = df.loc[1, "points"]
    a1, a2 = a
    b1, b2 = b
    print(a1, a2, b1, b2)

    quit()