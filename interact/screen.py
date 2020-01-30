from PIL import ImageGrab
import os
import time
import numpy as np

def rgb2gray(self, rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

class Screen:
    def grab(self):
        im = ImageGrab.grab()
        return np.asarray(im, dtype="int32")

    def grab_area(self, x1, y1, x2, y2):
        im = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        return im

    def save(self):
        im = ImageGrab.grab()
        im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')

screen = Screen()