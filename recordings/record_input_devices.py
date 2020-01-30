from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Key, Listener as KeyboardListener
import time, datetime
import ctypes
current_milli_time = lambda: int(round(time.time() * 1000))

print('-- Record keyboard & mouse --')
ctypes.windll.kernel32.SetConsoleTitleW("Recording keyboard & mouse (ENTER to stop)")

purpose = input('What is the purpose of recording (small label): ')
purpose = purpose.replace(' ', '_')

timestamp = time.strftime("%Y%m%d%H%M%S")
keyboard_recording_filename = 'keyboard_recording_{}.{}.csv'.format(timestamp, purpose)
mouse_recording_filename = 'mouse_recording_{}.{}.csv'.format(timestamp, purpose)

print('Keyboard output: {}'.format(keyboard_recording_filename))
print('Mouse output: {}'.format(mouse_recording_filename))

keyboard_output = open(keyboard_recording_filename, "w")
mouse_output = open(mouse_recording_filename, "w")

callback_timeout = 0.05
mouse_x, mouse_y = (0, 0)
mouse_update_lag_timer = 0
mouse_update_lag = 200 
previous_time = current_milli_time()

def print_timestamp():
    print('{} | '.format(str(datetime.datetime.now())), end='')

def on_move(x, y):
    global mouse_x, mouse_y, previous_time, mouse_update_lag_timer, mouse_update_lag
    current_time = current_milli_time()
    elapsed_milliseconds = current_time - previous_time
    mouse_update_lag_timer += elapsed_milliseconds
    if x != mouse_x and y != mouse_y and mouse_update_lag_timer > mouse_update_lag:
        print_timestamp()    
        print('Pointer moved to {0}'.format((x, y)))
        mouse_x = x 
        mouse_y = y
        mouse_output.write('{}, move, {}, {}\n'.format(current_milli_time(), mouse_x, mouse_y))
        mouse_update_lag_timer = 0
    previous_time = current_time

def on_click(x, y, button, pressed):
    print_timestamp()
    print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))
    mouse_output.write('{}, click, {}, {}\n'.format(current_milli_time(), mouse_x, mouse_y))
    mouse_output.flush()

def on_scroll(x, y, dx, dy):
    print_timestamp()
    print('Scrolled {} (dx={}, dy={})'.format((x, y), dx, dy))
    mouse_output.write('{}, scroll, {}, {}, {}, {}\n'.format(current_milli_time(), mouse_x, mouse_y, dx, dy))

def on_press(key):
    print_timestamp()
    print('Key {0} pressed'.format(key))
    keyboard_output.write('{}, press, {}\n'.format(current_milli_time(), key))

def on_release(key):
    print_timestamp()
    print('Key {} release'.format(key))
    keyboard_output.write('{}, release, {}\n'.format(current_milli_time(), key))
    keyboard_output.flush()

mouse_listener = MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
print('Created mouse listener')
mouse_listener.start()
print('Mouse listener started')
keyboard_listener = KeyboardListener(on_press=on_press, on_release=on_release)
print('Created keyboard listener')
keyboard_listener.start()
print('Keyboard listener started')

print(''.rjust(40, '-'))
_ = input("Press ENTER to close the application!\n")

keyboard_output.close()
mouse_output.close()

