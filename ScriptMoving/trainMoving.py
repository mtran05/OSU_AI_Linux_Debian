import os
os.environ["KERAS_BACKEND"] = "tensorflow"

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import keras
from keras import layers
import numpy as np
import tensorflow as tf
import datetime
import time
import matplotlib.pyplot as plt
import requests
import json
import pyautogui
pyautogui.PAUSE = 0.001

from songSelect import chooseSong
from screenshot import getState
from getUnixTime import getUnixTime
from extractCoords import extractCoords
from extractBeatmap import extractBeatmap
from bootNavigation import bootNavigation

"""----------------------"""

# Main model (continue training if exists)
main = "../Models/Moving/osu_ai-main.keras"

def create_model():
    inputA = keras.Input(shape=(60, 80, 4))
    inputB = keras.Input(shape=(2,))

    x = layers.Conv2D(64, 5, strides=3, activation="relu")(inputA)
    x = layers.Conv2D(128, 5, strides=2, activation="relu")(x)
    x = layers.Conv2D(128, 3, strides=1, activation="relu")(x)
    x = layers.Flatten()(x)
    x = layers.Dense(2048, activation="relu")(x)
    x = layers.Dense(512, activation="relu")(x)
    x = keras.Model(inputs=inputA, outputs=x)

    combined = layers.concatenate([x.output, inputB])

    z = layers.Dense(128, activation="relu")(combined)
    z = layers.Dense(2, activation="linear")(z)

    model = keras.Model(inputs=[x.input, inputB], outputs=z)
    model.compile(
        optimizer=keras.optimizers.SGD(learning_rate=0.00025, clipnorm=1.0),
        loss=keras.losses.Huber(),
        metrics=[keras.metrics.MeanAbsoluteError()]
    )
    return model

if (os.path.isfile(main)):
    model = keras.models.load_model(main)
    print("\n\n\n\nREUSING MODEL\n\n\n\n")
else: 
    model = create_model()

# Open Tosu and OSU! after loading model, so we can start training right away without waiting model to load
bootNavigation()

# Load config
with open(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "config.json")) as config:
    configDict = json.load(config)
    numberOfGames = configDict["osuConfig"]["numberOfGames"]
    
    xOffSet = configDict["osuConfig"]["XOffSet"]
    yOffSet = configDict["osuConfig"]["YOffSet"]
    yOffSetMargin = configDict["osuConfig"]["YOffSetMargin"]
    yOffTotal = yOffSet + yOffSetMargin

"""------------------------"""

for i in range(1, numberOfGames + 1):
    res = requests.get('http://127.0.0.1:24050/json/v2')
    response = json.loads(res.text)
    df = extractBeatmap(response)
    
    time.sleep(3)
    pyautogui.moveTo(400 + xOffSet, 420 + yOffTotal)  # skip cut-scene
    time.sleep(0.5)
    pyautogui.click()

    startTime = None
    while startTime == None:
        startTime = getUnixTime()
        print(startTime)
    
    stopTime = startTime + response["beatmap"]["time"]["lastObject"]

    while True:
        if time.time() * 1000 > stopTime:
            break

        state = getState()
        state = keras.ops.expand_dims(state, 0)
        
        # Test for every n-10th beatmap
        if (i % 10 != 0):
            # ! TRAIN ONLY !
            x, y = extractCoords(startTime, df)
            if (x == None or y == None):
                continue
            
            # Convert from Osu! Pixels to actual Screen Pixels
            scale = 5.0/4.0
            x = x * scale + 80
            y = y * scale + 70

            currentMousePos = np.array(pyautogui.position()) - np.array([xOffSet, yOffTotal])
            currentMousePos = keras.ops.expand_dims(currentMousePos, 0)
            hitObjectPosition = keras.ops.expand_dims([x, y], 0)

            history = model.fit(
                x=[state, currentMousePos],
                y=hitObjectPosition,
                epochs=1,
            )
            
            # Accounting for offsets
            x += xOffSet
            y += yOffTotal
            pyautogui.moveTo(x, y)  
            
        else:
            # ! TEST ONLY !
            currentMousePos = np.array(pyautogui.position()) - np.array([xOffSet, yOffTotal])
            currentMousePos = keras.ops.expand_dims(currentMousePos, 0)

            newX, newY = model.predict([state, currentMousePos])[0]
            
            # Accounting for offsets
            newX += xOffSet
            newY += yOffTotal
            print(newX, newY)
            pyautogui.moveTo(newX, newY)
    
    # Choose a new song upon finishing one
    if i == numberOfGames:
        break
    else:
        chooseSong()

# Save model after training
if (os.path.isfile(main)):
    model.save(main)
else:
    model.save(f"../Models/Moving/osu_ai-{datetime.date.today()}.keras")