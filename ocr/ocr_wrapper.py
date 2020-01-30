from PIL import Image
import pytesseract
import argparse
import cv2
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class OCR:
    def __init__(self):
        pass

    def image_to_string(self, image):
        return pytesseract.image_to_string(image)

    def file_to_string(self, path):
        img = Image.open(path)
        return self.image_to_string(img)

ocr = OCR()