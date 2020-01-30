import math
import random
import time
import os
import numpy as np
from pynput.mouse import Button, Controller as MouseController, Listener as MouseListener
from pynput.keyboard import Controller as KeyboardController, Listener as KeyboardListener, Key
from PIL import ImageGrab

class Mouse:
    """
    https://pythonhosted.org/pynput/mouse.html
    """
    def __init__(self):
        self.mouse = MouseController()
    
    def move(self, x, y):
        def set_mouse_position(x, y):
            self.mouse.position = (int(x), int(y))
        def smooth_move_mouse(from_x, from_y, to_x, to_y, speed=0.2):
            steps = 40
            sleep_per_step = speed / steps
            x_delta = (to_x - from_x) / steps
            y_delta = (to_y - from_y) / steps
            for step in range(steps):
                new_x = x_delta * (step + 1) + from_x
                new_y = y_delta * (step + 1) + from_y
                set_mouse_position(new_x, new_y)
                time.sleep(sleep_per_step)
        return smooth_move_mouse(
            self.mouse.position[0],
            self.mouse.position[1],
            x,
            y
        )

    def left_click(self):
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)

    def left_press(self):
        self.mouse.press(Button.left)

    def left_release(self):
        self.mouse.release(Button.left)

    def right_click(self):
        self.mouse.press(Button.right)
        self.mouse.release(Button.right)

    def right_press(self):
        self.mouse.press(Button.right)

    def right_release(self):
        self.mouse.release(Button.right)

    def scroll(self, y):
        def scroll(scroll_y):
            self.mouse.scroll(0, scroll_y)
        def smooth_scroll(scroll_y, speed=0.1):
            steps = 20
            sleep_per_step = speed / steps
            y_delta = y / steps
            for _ in range(steps):
                scroll(y_delta)
                time.sleep(sleep_per_step)
        return smooth_scroll(y)
        

    def position(self):
        return self.mouse.position


class Keyboard:
    """
    https://pythonhosted.org/pynput/keyboard.html#controlling-the-keyboard
    """
    def __init__(self):
        self.keys_pressed = {}
        self.exit = False
        self.keyboard_listener = KeyboardListener(on_press=self.on_press, on_release=self.on_release).start()
        self.keyboard = KeyboardController()

    def on_press(self, key):
        #print('{0} pressed'.format(key))
        self.keys_pressed[key] = True

    def on_release(self, key):
        #print('{} release'.format(key))
        self.keys_pressed[key] = False
        if self.exit:
            return False 

    def press(self, key):
        self.keyboard.press(key)

    def release(self, key):
        self.keyboard.release(key)

    def click(self, key):
        self.keyboard.press(key)
        self.keyboard.release(key)

    def key_pressed(self, key):
        if key in self.keys_pressed.keys():
            return self.keys_pressed[key]
        return False

    def type(self, str):
        self.keyboard.type(str)


class Screen:
    def grab(self):
        return ImageGrab.grab()

    def grab_area(self, x1, y1, x2, y2):
        return ImageGrab.grab(bbox=(x1, y1, x2, y2))
    
    def grab_as_array(self):
        return np.asarray(self.grab(), dtype="int32")

    def save(self):
        im = ImageGrab.grab()
        im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')

    def rgb2gray(self, rgb):
        return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])


mouse = Mouse()
keyboard = Keyboard()
screen = Screen()
