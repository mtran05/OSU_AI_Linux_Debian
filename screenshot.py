import cv2
import numpy
import time
import mss
import keras
import matplotlib.pyplot as plt

# Possible values: 20, 25, 30, 35, 40, 50, 60
fps = 40

def getState(frames = 4, top = 80, left = 70, width = 800, height = 600):
    # ls = numpy.array([])
    ls = []

    with mss.mss() as sct:
        # Part of the screen to capture
        monitor = {"top": top, "left": left, "width": width, "height": height}

        # if "Screen capturing":
        for i in range(frames):
            last_time = time.time()
            time.sleep(1.0 / fps)

            # Get raw pixels from the screen, save it to a Numpy array
            img = numpy.array(sct.grab(monitor))    # shape (600, 800, 4)
            grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   # shape (600, 800)
            resized = cv2.resize(grey_img, (80, 60), interpolation= cv2.INTER_LANCZOS4)   # shape (60, 80)
            
            # ls = numpy.append(ls, resized)
            ls.append(resized)

            # Display the picture in grayscale
            """ cv2.imshow('OpenCV/Numpy grayscale', grey_img) """

            # Display FPS rate for each frame captured
            """ print(f"fps: {1 / (time.time() - last_time)}") """

            # Press "q" to quit
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break
            
            cv2.imshow('Osu!AI_View', cv2.resize(grey_img, (80*5, 60*5)))
            # cv2.imshow('Osu!AI_View', cv2.resize(resized, (800, 600)))
    
    # ls = ls.reshape((4, 60, 80))
    transposed = keras.ops.transpose(ls, [1, 2, 0]) # (60, 80, 4) <- (4, 60, 80)
    
    # ! START OF DEBUGGING AREA !
    # plt.figure(1, figsize=(10,10))
    # for i in range(4):
    #     plt.subplot(2,2,i+1)
    #     plt.xticks([])
    #     plt.yticks([])
    #     plt.grid(False)
    #     plt.imshow(ls[i])
    
    # plt.figure(2, figsize=(10,10))
    # plt.subplot(1,1,1)
    # plt.xticks([])
    # plt.yticks([])
    # plt.grid(False)
    # plt.imshow(transposed)

    # plt.show()
    # ! START OF DEBUGGING AREA !
    
    return transposed