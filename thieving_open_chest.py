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
        print('Started' if enabled else 'Stopped')

print('Thiefing helper - Ardougne Nature Rune Chest')
print('Instruction: Stand next to the chest in Ardougne, and zoom in completely.')
print('Also remember to select to world change tab and have three worlds on top!')
print('Press F2 to start or stop...')
print(''.ljust(60, '-'))

listener = Listener(on_release=on_release) 
listener.start()

chest_x, chest_y = (950, 719)
world_switch_x, world_switch_y = (2459, 1143)
current_world = 0
max_worlds = 3
total_runes = 0

original_mouse_x, original_mouse_y = device.mouse.position()

wait_between_click = lambda: time.sleep(max(np.random.normal(75, 33) / 10000, 20 / 1000))
wait_short = lambda: time.sleep(max(np.random.normal(25, 100) / 1000, 20 / 1000))
wait_medium = lambda: time.sleep(max(np.random.normal(200, 100) / 1000, 20 / 1000))
wait_long = lambda: time.sleep((6500 + np.random.normal(0, 250))/1000)
wait_break = lambda: time.sleep(np.random.normal(60, 10))

while True:
    if enabled:

        if(random.uniform(0, 1) < 0.02):
            print('[action] taking a small break . . . ')
            wait_break()

        # Move to the chest
        print('[action] move to chest')
        device.mouse.move(chest_x, chest_y)
        wait_medium()

        # Right click
        print('[action] right click')
        device.mouse.right_press()
        wait_between_click()
        device.mouse.right_release()

        wait_medium()

        # Move the mouse to the search for traps menu item
        print('[action] move to search for traps')
        x, y = device.mouse.position()
        move_x, move_y = random.randint(10, 60), random.randint(38, 46)
        device.mouse.move(x + move_x, y + move_y)
        wait_short()

        # Search for traps click
        print('[action] left click')
        device.mouse.left_press()
        wait_between_click()
        device.mouse.left_release()
        wait_short()

        # Random mouse movement
        if random.uniform(0, 1) < 0.25:
            print('[action] goto random position')
            rx, ry = random.randint(300, 2000), random.randint(300, 900)
            device.mouse.move(rx, ry)

        wait_long()
        total_runes += 1
        print('[status] farmed total of {} runes'.format(total_runes))

        if random.uniform(0, 1) < 0.06:
            print('[action] waiting for a small time . . .')
            time.sleep(np.random.normal(30, 5))

        # Select the next world
        print('[action] move to world {} out of {}'.format(current_world+1, max_worlds))
        device.mouse.move(world_switch_x + 16 * current_world, world_switch_y + 12 * current_world)
        current_world = (current_world + 1) % max_worlds
        wait_medium()
        print('[action] left click')
        device.mouse.left_press()
        wait_between_click()
        device.mouse.left_release()
        wait_medium()

        if(random.uniform(0, 1) < 0.25):
            print('[action] goto random position')
            rx, ry = random.randint(300, 2000), random.randint(300, 900)
            device.mouse.move(rx, ry)

        print('[wait] waiting . . . ')
        time.sleep(6 + abs(np.random.normal(0, 0.5)))
