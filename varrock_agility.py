import interact.device as device
import window_size.window_size_wrapper as ws
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib.patches as patches
import numpy as np
import time
from pynput.keyboard import Key
import math
import ocr.ocr_wrapper
import random
from PIL import Image

"""
The idea is to watch the course from the south, and lock onto a position.
"""

refresh_interval = 256

width, height, left, top, right, bottom = ws.get_window_size() # window size

# my retarded monitor scaling
windows_dpi_scaling = 1.5 
left *= windows_dpi_scaling; right *= windows_dpi_scaling
top *= windows_dpi_scaling ; bottom *= windows_dpi_scaling
pad_left, pad_top, pad_right, pad_bottom = (10, 32 * windows_dpi_scaling, 10, 8)

print('-- Window detected at position --')
print('Dimension: {} x {}'.format(width, height))
print('BBox: {}, {}, {}, {}'.format(left, top, right, bottom))
print('DPI Scaling: {} (set to 1.0 if the window is not right)'.format(windows_dpi_scaling))

"""
Grabs the game area from the screen.
"""
def grab_screen():   
    img = device.screen.grab_area(left + pad_left, top + pad_top, right - pad_right, bottom - pad_bottom)
    return np.asarray(img, dtype="int32")

"""
A target is where it should click.
"""
class Target:
    def __init__(self, x, y, w, h, name='', color='red'):
        self.position = (x, y)
        self.dimension = (w, h)
        self.name = name
        self.color = color
    def center(self, random_spread=4):
        x, y = self.position
        w, h = self.dimension
        return (x + w/2 + random.randint(1, random_spread), y + h/2 + random.randint(1, random_spread)) 
    def draw(self, ax):
        x, y = self.position
        w, h = self.dimension
        self.rect = patches.Rectangle(self.position, w, h, linewidth=1, edgecolor=self.color, facecolor='none')
        ax.add_patch(self.rect)
        self.text = plt.text(x, y - 10, self.name, fontsize=8, color=self.color)
    def click(self):
        x, y = self.center()
        x /= windows_dpi_scaling
        y /= windows_dpi_scaling
        device.mouse.move(x + pad_left / 2, y + pad_top / 2)
        time.sleep(random.randint(50, 125) / 1000)
        device.mouse.left_click()
        time.sleep(random.randint(50, 125) / 1000)
        device.mouse.left_release()
    def hide(self):
        self.rect.set_visible(False)

"""
Add all the different targets here.
"""
class Targets:
    climb_rocks = Target(2860, 780, 60, 60, 'Climb rocks')
    clothes_line = Target(2250, 1015, 75, 75, 'Clothes line')
    gap1 = Target(2445, 1142, 100, 100, 'Gap 1')
    wall = Target(2208, 900, 100, 190, 'Wall')
    gap2 = Target(1643, 685, 300, 70, 'Gap 2')
    gap3 = Target(775, 1100, 100, 90, 'Gap 3')
    gap4 = Target(813, 1163, 100, 100, 'Gap 4')
    ledge = Target(1871, 1420, 100, 100, 'Ledge / Edge')
    anchor = Target(1664, 1192, 200, 200, '<anchor>', 'blue')


# Setup plot and animation.
screenshot = grab_screen()
fig = plt.figure()
ax = fig.add_subplot()
im = ax.imshow(screenshot, animated=True)

# Draw all the targets
Targets.climb_rocks.draw(ax)
Targets.clothes_line.draw(ax)
Targets.gap1.draw(ax)
Targets.wall.draw(ax)
Targets.gap2.draw(ax)
Targets.gap3.draw(ax)
Targets.gap4.draw(ax)
Targets.ledge.draw(ax)
Targets.anchor.draw(ax)

# Draw custom text and patches 
text = plt.text(10, 64, '<Iteration>', fontsize=8, color='red')

# State machine definitions for the bot.
state_climb_rocks = 0
state_clothes_line = 1
state_gap1 = 2
state_wall = 3
state_gap2 = 4
state_gap3 = 5
state_gap4 = 6
state_ledge = 7
state_edge = 8
state_string = ['Climb rock (start)', 'Clothes line', 'Gap 1', 'Wall', 'Gap 2', 'Gap 3', 'Gap 4', 'Ledge', 'Edge (end)']

state = state_climb_rocks  # state of the actions
timer = 0  # timer for idling
max_timer = 0
stopped = True
previous_time = time.time()

"""
Animation loop.
"""
def update_image(i):
    global timer, state, previous_time, stopped, max_timer

    if not stopped and timer > max_timer:
        timer = 0
        max_timer = 10
        if state == state_climb_rocks:
            Targets.climb_rocks.click()
            state = state_clothes_line
            max_timer = 11
        elif state == state_clothes_line:
            Targets.clothes_line.click()
            state = state_gap1
        elif state == state_gap1:
            Targets.gap1.click()
            state = state_wall
            max_timer = 8
        elif state == state_wall:
            Targets.wall.click()
            state = state_gap2
            max_timer = 13
        elif state == state_gap2:
            Targets.gap2.click()
            state = state_gap3
            max_timer = 5
        elif state == state_gap3:
            Targets.gap3.click()
            state = state_gap4
            max_timer = 11
        elif state == state_gap4:
            Targets.gap4.click()
            state = state_ledge
            max_timer = 10
        elif state == state_ledge:
            Targets.ledge.click()
            state = state_edge
            max_timer = 5.5
        elif state == state_edge:
            Targets.ledge.click()
            state = state_climb_rocks
            max_timer = 5.5
        
    # Time management
    current_time = time.time()
    elapsed_time = current_time - previous_time
    previous_time = current_time
    timer += elapsed_time

    if device.keyboard.key_pressed(Key.f2):
        stopped = not stopped
    
    screenshot = grab_screen()

    info = 'Current frame: {}, Stopped: {} (F2), State: {} ({}), Timer: {}, Max Time: {}'.format(i, stopped, state_string[state], state, round(timer, 2), max_timer)
    text._text = info
    im.set_array(screenshot)
    print('\r{}'.format(info), end='')

ani = animation.FuncAnimation(fig, update_image, interval=refresh_interval)
plt.axis('off')
plt.show()