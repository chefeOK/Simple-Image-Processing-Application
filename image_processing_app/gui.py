import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import os
from image_processor import ImageProcessor

class ImageProcessingApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Processing Application")
        self.image_processor = None

        self.create_widgets()

    def create_widgets(self):
        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack()

        self.canvas = tk.Canvas(self.image_frame, width=500, height=500)
        self.canvas.pack()

        self.control_panel = tk.Frame(self.root)
        self.control_panel.pack()

        self.upload_button = tk.Button(self.control_panel, text="Upload Image", command=self.upload_image)
        self.upload_button.grid(row=0, column=0)

        self.grayscale_button = tk.Button(self.control_panel, text="Grayscale", command=self.apply_grayscale)
        self.grayscale_button.grid(row=0, column=1)

        self.blur_button = tk.Button(self.control_panel, text="Blur", command=self.apply_blur)
        self.blur_button.grid(row=0, column=2)

        self.edge_button = tk.Button(self.control_panel, text="Edge Detection", command=self.apply_edge_detection)
        self.edge_button.grid(row=0, column=3)

        self.brightness_scale = tk.Scale(self.control_panel, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, label="Brightness")
        self.brightness_scale.set(1.0)
        self.brightness_scale.grid(row=1, column=0, columnspan=2)

        self.contrast_scale = tk.Scale(self.control_panel, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, label="Contrast")
        self.contrast_scale.set(1.0)
        self.contrast_scale.grid(row=1, column=2, columnspan=2)

        self.apply_adjustments_button = tk.Button(self.control_panel, text="Apply Adjustments", command=self.apply_adjustments)
        self.apply_adjustments_button.grid(row=2, column=0, columnspan=4)

        self.save_button = tk.Button(self.control_panel, text="Save Image", command=self.save_image)
        self.save_button.grid(row=3, column=0, columnspan=4)

        self.reset_button = tk.Button(self.control_panel, text="Reset Image", command=self.reset_image)
        self.reset_button.grid(row=4, column=0, columnspan=4)

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            print(f"Selected file path: {file_path}")
            if os.path.exists(file_path):
                try:
                    self.image_processor = ImageProcessor(file_path)
                    self.display_image(self.image_processor.image)
                except ValueError as e:
                    messagebox.showerror("Image Processing Error", str(e))
            else:
                messagebox.showerror("File Error", f"File does not exist: {file_path}")

    def display_image(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_tk = ImageTk.PhotoImage(image_pil)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
        self.canvas.image_tk = image_tk

    def apply_grayscale(self):
        if self.image_processor:
            self.image_processor.apply_grayscale()
            self.display_image(self.image_processor.image)

    def apply_blur(self):
        if self.image_processor:
            self.image_processor.apply_blur()
            self.display_image(self.image_processor.image)

    def apply_edge_detection(self):
        if self.image_processor:
            self.image_processor.apply_canny_edge_detection()
            self.display_image(self.image_processor.image)

    def apply_adjustments(self):
        if self.image_processor:
            brightness = self.brightness_scale.get()
            contrast = self.contrast_scale.get()
            self.image_processor.adjust_brightness(brightness)
            self.image_processor.adjust_contrast(contrast)
            self.display_image(self.image_processor.image)

    def save_image(self):
        if self.image_processor:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                self.image_processor.save_image(file_path)
                messagebox.showinfo("Image Processing", "Image saved successfully!")

    def reset_image(self):
        if self.image_processor:
            self.image_processor.reset_image()
            self.display_image(self.image_processor.image)

    def run(self):
        self.root.mainloop()

