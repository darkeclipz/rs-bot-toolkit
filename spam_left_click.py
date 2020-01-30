import interact.device as device
from pynput.keyboard import Key, Listener
import time 
import random
import numpy as np

enabled = False

def on_release(key):
    global enabled
    if key == Key.f2:
        enabled = not enabled
    if key == Key.esc:
        return False

listener = Listener(on_release=on_release) 
listener.start()

while True:
    print('\rEnabled: {} (F2)   '.format(enabled), end='')
    if enabled:
        device.mouse.left_press()
        time_before_release = max(np.random.normal(75, 33) / 10000, 20 / 1000)
        time.sleep(time_before_release)
        device.mouse.left_release()
    time_between_clicks = max(np.random.normal(800, 600) / 1000, 200 / 1000)
    time.sleep(time_between_clicks)
