import logging
import threading
from tkinter import *  
from PIL import ImageTk,Image
import os
import queue

class ImageLoader:
    def __init__(self, files, batch_size=3):
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
        Canvas.__init__(self,parent,width=w,height=h,**kwargs)
        self.rect_size = min(576,min(w,h)) - 64
        self.img = ImageTk.PhotoImage(self.im)
        self.create_image(0, 0, anchor=NW, image=self.img)
        self.rect = self.create_rectangle(0,0,512,512)
        self.bind("<Motion>", self.motion)
        self.bind("<MouseWheel>", self.mouse_wheel)
        self.pack()
    
    def mouse_wheel(self, event):
        if event.num == 5 or event.delta == -120:
            if self.rect_size > 32:
                self.rect_size -=32
        if event.num == 4 or event.delta == 120:
            if self.rect_size < 1024:
                self.rect_size += 32
        if self.rect:
            self.delete(self.rect)
        half = int(self.rect_size / 2)
        self.rect = self.create_rectangle(event.x - half, event.y - half, event.x + half, event.y + half)


    def motion(self, event):
        if self.rect:
            self.delete(self.rect)
        half = int(self.rect_size / 2)
        self.rect = self.create_rectangle(event.x - half, event.y - half, event.x + half, event.y + half)

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

    def load_canvas(self):
        if self.image_loader.has_next():
            self.canvas = CustomCanvas(self.image_loader.get(), self.root)
            self.canvas.bind("<Button-1>", self.click)
        else:
            self.root.destroy()

    def start(self):
        self.root.mainloop()


folders = [
    ("original\\train\\cendol", "data\\train\\cendol"), 
    ("original\\train\\tauhuay", "data\\train\\tauhuay"), 
    ("original\\train\\tausuan", "data\\train\\tausuan")]

files = []
for fromDir, toDir in folders:
    for f in os.listdir(fromDir):
        filepath = os.path.join(fromDir, f)
        destPath = os.path.join(toDir, f)
        if not os.path.exists(destPath):
            files.append((filepath, destPath))

MainApp(ImageLoader(files)).start()