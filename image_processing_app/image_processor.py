import cv2
import numpy as np
from PIL import Image, ImageEnhance
import os

class ImageProcessor:
    def __init__(self, image_path):
        print(f"Attempting to read image from path: {image_path}")
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError(f"Error: Unable to read image from path '{image_path}'")
        self.original_image = self.image.copy()

    def apply_grayscale(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def apply_blur(self, ksize=5):
        self.image = cv2.GaussianBlur(self.image, (ksize, ksize), 0)

    def apply_canny_edge_detection(self, threshold1=100, threshold2=200):
        self.image = cv2.Canny(self.image, threshold1, threshold2)

    def adjust_brightness(self, factor):
        pil_img = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        enhancer = ImageEnhance.Brightness(pil_img)
        pil_img = enhancer.enhance(factor)
        self.image = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    def adjust_contrast(self, factor):
        pil_img = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        enhancer = ImageEnhance.Contrast(pil_img)
        pil_img = enhancer.enhance(factor)
        self.image = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    def save_image(self, path):
        cv2.imwrite(path, self.image)

    def reset_image(self):
        self.image = self.original_image.copy()
