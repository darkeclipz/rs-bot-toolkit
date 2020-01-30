import ocr_wrapper
from PIL import Image
import os

print('-- OCR --')
print()
print('All .png files will be read.')
print()

for file in os.listdir(os.getcwd()):
    file = file.lower()
    if os.path.isfile(file) and 'png' in file:
        print('[{}]'.format(file))
        im = Image.open(file)
        text = ocr_wrapper.ocr.image_to_string(im)
        print(text)
        print()