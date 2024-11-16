import sys
sys.path.append("C:\\Users\\qttra\\OneDrive\\Documents\\GitHub\\OSU_AI\\Parser")

import time
import numpy as np
from curve import Bezier
from slidercalc import rotate, get_circum_circle

# * --------------- *

# TODO: Catch random error??
def extractCoords(unixStartTime, df):
    TimeDelta = time.time() * 1000 - unixStartTime
    DelayEpsilon = 40   # ! At least 30ms, no more than 100ms
    nextHitObject = df[(df["startTime"] > TimeDelta - DelayEpsilon) | ((df["object_name"] == "slider") & (TimeDelta < df["end_time"]))]
    
    x, y = [None, None]
    
    if nextHitObject.empty:
        return x, y
    hitObject = nextHitObject.iloc[0]

    if (unixStartTime + hitObject["startTime"]) - time.time() * 1000 > 300:     # * only care if within 300ms *
        return x, y
    
    # * ----------------- *
    
    if hitObject["object_name"] == "circle":
        x, y = hitObject["position"]
        return x, y
    
    elif hitObject["object_name"] == "slider":
        repeatCount = int(hitObject["repeatCount"])
        sliderTimeDelta = time.time()*1000 - (hitObject["startTime"] + unixStartTime)
        sliderPercent = (sliderTimeDelta)/hitObject["duration"]
        
        if sliderPercent < 0:
            x, y = hitObject["position"]
            return x, y
        
        if hitObject["curveType"] == "bezier":
            
            for i in range(1, repeatCount + 1):
                if sliderTimeDelta <= (hitObject["duration"] / repeatCount) * i:
                    progress = (sliderPercent - (i-1) / repeatCount) * repeatCount
                    if (i % 2 != 0):
                        bz = Bezier(hitObject["points"])
                        x, y = bz.at(progress)
                        return x, y
                    else:
                        bz = Bezier(hitObject["points"][::-1])  # ! Backwards
                        x, y = bz.at(progress) 
                        return x, y
        
        elif hitObject["curveType"] == "pass-through":
            # ?? p1, p2, p3 = [*df.loc[hitObject, "points"][:2], df.loc[hitObject, "end_position"]]
            p1, p2, p3 = hitObject["points"]
            
            try:
                cx, cy, radius = get_circum_circle(p1, p2, p3)
                radians = hitObject["pixelLength"] / radius

                matrix = np.array([p1, p2, p3])
                matrix = np.concatenate((matrix, [[1],[1],[1]]), axis=1)
                det = np.linalg.det(matrix)

                if det < 0:
                    sign = -1   # ! - radians if counter-clockwise
                elif det > 0:
                    sign = 1    # ! + radians if clockwise

                for i in range(1, repeatCount + 1):
                    if sliderTimeDelta <= (hitObject["duration"] / repeatCount) * i:
                        progress = (sliderPercent - (i-1) / repeatCount) * repeatCount
                        if (i % 2 != 0):
                            x, y = rotate(cx, cy, p1[0], p1[1], sign * radians * progress)
                            return x, y
                        else:
                            x, y = rotate(cx, cy, p3[0], p3[1], -1 * sign * radians * progress)
                            return x, y

            except ValueError:
                for i in range(1, repeatCount + 1):
                    if sliderTimeDelta <= (hitObject["duration"] / repeatCount) * i:
                        progress = (sliderPercent - (i-1) / repeatCount) * repeatCount
                        if (i % 2 != 0):
                            x, y = interpolate_point(p1, p3, progress)
                            return x, y
                        else:
                            x, y = interpolate_point(p3, p1, progress)   # ! Backwards: swap p1 & p2
                            return x, y

        elif hitObject["curveType"] == "linear":
            # ?? p1, p2 = [df.loc[hitObject, "position"], df.loc[hitObject, "end_position"]]
            p1, p2 = hitObject["points"]
            
            for i in range(1, repeatCount + 1):
                if sliderTimeDelta <= (hitObject["duration"] / repeatCount) * i:
                    progress = (sliderPercent - (i-1) / repeatCount) * repeatCount
                    if (i % 2 != 0):
                        x, y = interpolate_point(p1, p2, progress)
                        return x, y
                    else:
                        x, y = interpolate_point(p2, p1, progress)   # ! Backwards: swap p1 & p2
                        return x, y
    
    elif hitObject["object_name"] == "spinner":
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