import logging
import threading
from tkinter import *  
from PIL import ImageTk,Image
import os
import queue

class ImageLoader:
    def __init__(self, files, batch_size=50):
        self.files = [f for f in files]
        self.files_index = 0
        self.batch_size = batch_size
        self.loadedImages = queue.Queue()
        self.load_image()

    def load_image(self):
        
        if self.loadedImages.qsize() >= self.batch_size:
            return 
        print("loading images")
        while self.loadedImages.qsize() < 2 * self.batch_size and self.files_index < len(self.files):
            filePath, destPath = self.files[self.files_index]
            img = Image.open(filePath)
            w, h = img.size
            resize = False
            if w > 1856:
                factor = 1624/w
                w = 1624
                h = int(h * factor)
                resize = True
            if h > 1024:
                factor = 896/h
                w = int(w * factor)
                h = 896
                resize = True
            if resize:
                print("resize {0} {1}".format(w,h))
                img = img.resize((w,h))

            self.files_index += 1
            self.loadedImages.put((img, filePath, destPath))

    def has_next(self):
        return not self.loadedImages.empty()

    def get(self):
        if self.loadedImages.empty():
            return None
        else:
            result = self.loadedImages.get()
            threading.Thread(target=self.load_image).start()
            return result

class CustomCanvas(Canvas):
    def __init__(self, im_l, parent, **kwargs):
        self.im = im_l[0]
        self.filePath = im_l[1]
        self.destPath = im_l[2]
        w, h = self.im.size
        self.width = w
        self.height = h
        Canvas.__init__(self,parent,width=w,height=h,**kwargs)
        self.rect_size = min(576,min(w,h)) - 64
        self.img = ImageTk.PhotoImage(self.im)
        self.create_image(0, 0, anchor=NW, image=self.img)
        self.rect = None
        self.createRectangle(0,0,512,512)
        self.bind("<Motion>", self.motion)
        self.bind("<MouseWheel>", self.mouse_wheel)
        self.pack()
    
    def mouse_wheel(self, event):
        if event.num == 5 or event.delta == -120:
            if self.rect_size > 32:
                self.rect_size = max(32, self.rect_size - 16)
        if event.num == 4 or event.delta == 120:
            if self.rect_size < min(self.width, self.height):
                self.rect_size = min(self.rect_size + 16, min(self.width, self.height))
        half = int(self.rect_size / 2)
        self.createRectangle(event.x - half, event.y - half, event.x + half, event.y + half)

    def createRectangle(self, x0,y0,x1,y1):
        if self.rect:
            self.delete(self.rect)
        self.rect = self.create_rectangle(x0,y0,x1,y1,outline='red')

    def motion(self, event):
        half = int(self.rect_size / 2)
        self.createRectangle(event.x - half, event.y - half, event.x + half, event.y + half)

    def process_click(self):
        im2 = self.im.crop(self.coords(self.rect))
        im2.save(self.destPath)

class MainApp:
    def __init__(self, image_loader):
        self.root = Tk()
        self.image_loader = image_loader
        self.load_canvas()

    def click(self, event):
        if self.canvas.find_withtag(CURRENT):
            print("click detected: {0} {1}".format(event.x, event.y))
            self.canvas.process_click()
            self.canvas.destroy()
            self.load_canvas()

    def click_right(self, event):
        if self.canvas.find_withtag(CURRENT):
            print("right click detected: skipped")
            self.canvas.destroy()
            self.load_canvas()

    def load_canvas(self):
        if self.image_loader.has_next():
            self.canvas = CustomCanvas(self.image_loader.get(), self.root)
            self.canvas.bind("<Button-1>", self.click)
            self.canvas.bind("<Button-3>", self.click_right)
        else:
            self.root.destroy()

    def start(self):
        self.root.mainloop()

import json
with open("config.json", "r") as configFile:
    configJson = json.load(configFile)

folders = [(config["src"], config["dest"]) for config in configJson]

files = []
for fromDir, toDir in folders:
    for f in os.listdir(fromDir):
        filepath = os.path.join(fromDir, f)
        destPath = os.path.join(toDir, f)
        if not os.path.exists(destPath):
            files.append((filepath, destPath))

MainApp(ImageLoader(files)).start()