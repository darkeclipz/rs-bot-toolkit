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
from PIL import Image

refresh_interval = 256

width, height, left, top, right, bottom = ws.get_window_size()
windows_dpi_scaling = 1.5
left *= windows_dpi_scaling; right *= windows_dpi_scaling
top *= windows_dpi_scaling ; bottom *= windows_dpi_scaling
pad_left, pad_top, pad_right, pad_bottom = (10, 32 * windows_dpi_scaling, 10, 8)

print('-- Window detected at position --')
print('Dimension: {} x {}'.format(width, height))
print('BBox: {}, {}, {}, {}'.format(left, top, right, bottom))
print('DPI Scaling: {} (set to 1.0 if the window is not right)'.format(windows_dpi_scaling))

def grab_screen():   
    img = device.screen.grab_area(left + pad_left, top + pad_top, right - pad_right, bottom - pad_bottom)
    return np.asarray(img, dtype="int32")

screenshot = grab_screen()

fig = plt.figure()
ax = fig.add_subplot()
im = ax.imshow(screenshot, animated=True)

text_width, text_height = 600, 28
rect = patches.Rectangle((0, 0), text_width, text_height, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)

#label_current_iteration = text(0.5, 0.5, 'matplotlib', horizontalalignment='center', verticalalignment='center', transform.ax.transAes)
#text = plt.text(0, 0, '', bbox={'facecolor':'none', 'alpha':0.5, 'pad':10})

text = plt.text(10, right - 100, '', fontsize=8, color='red')

def update_image(i):
    ocr_data = '<no data>'
    screenshot = grab_screen()
    text._text = 'Current frame: {}'.format(i)

    # get sub rect for text
    S = np.array(screenshot)

    print('Image shape: {}'.format(S.shape))
    #print(S.shape)
    sub_image = S[:text_height, :text_width, :]
    print('Subimage shape: {}'.format(sub_image.shape))
    sub_image_I = Image.fromarray(sub_image, 'RGBA')

    plt.imshow(sub_image_I)
    
    # read text
    ocr_read = ocr.ocr_wrapper.ocr.image_to_string(sub_image_I)
    if len(ocr_read) > 0:
        print('\n OCR read: {}\n'.format(ocr_read))
        ocr_data = ocr_read

    im.set_array(screenshot)
    print('\rIteration: {}, OCR: {}'.format(i, ocr_data), end='')

ani = animation.FuncAnimation(fig, update_image, interval=refresh_interval)
plt.axis('off')
plt.show()