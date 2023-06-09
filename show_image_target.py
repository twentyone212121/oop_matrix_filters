import tkinter as tk
from PIL import ImageTk, Image

class ShowImageTarget(tk.Frame):
    '''
    Canvas with Image that encapsulates all image updating behaviour and stores current image with id
    '''
    def __init__(self, parent):
        super().__init__(parent)

        self.canvas_width = 640
        self.canvas_height = 480

        self.__canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height)
        self.__canvas.pack()
        self.__canvas['bg'] = '#dfe4ea'
        self.__canvas['highlightcolor'] = '#dfe4ea'
        self.__canvas['highlightbackground'] = '#dfe4ea'
        self.__canvas['bd'] = 0
        self.__tk_image = None
        self.__tk_image_id = None
    
    def update_image(self, image: Image.Image):
        self.clear()
        self.__tk_image = self.resize_image(image)
        self.__tk_image_id = self.__canvas.create_image(0, 0, anchor='nw', image=self.__tk_image)
    
    def resize_image(self, image: Image.Image):
        original_width, original_height = image.size
        aspect_ratio = original_width / original_height

        if original_width > original_height:
            new_width = self.canvas_width
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = self.canvas_height
            new_width = int(new_height * aspect_ratio)

        resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(resized_image)
    
    def clear(self):
        if self.__tk_image_id != None:
            self.__canvas.delete(self.__tk_image_id)

