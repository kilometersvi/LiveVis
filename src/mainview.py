from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
import os
from soundutil import SoundUtil
import numpy as np
from PIL import Image, ImageTk
import cv2
from layer_controller import LayerController
import time


#figure out how to import SoundUtil

class MainWindow:

    def __init__(self):

        top = Tk()
        top.title("LiveVis")
        top.geometry('600x150')
        top.resizable(True, True)

        self.allConnectedAudio = SoundUtil.GetInputDevices()

        #self.imgdim = (600,800)
        #array = np.ones((self.imgdim[1], self.imgdim[0]))
        #self.img =  ImageTk.PhotoImage(image=Image.fromarray(array))

        #self.canvas = tk.Canvas(top,width=self.imgdim[1],height=self.imgdim[0])
        #self.canvas.pack()
        #self.image_container = self.canvas.create_image(24,18, anchor="n", image=self.img)

        # Dropdown menu options
        options = [k for k, v in self.allConnectedAudio.items()]

        #initial config
        self.inputID = -1
        # datatype of menu text
        self.inputSelectClicked = StringVar()

        # initial menu text
        self.inputSelectClicked.set( "None" )

        # Create Input Dropdown menu
        self.inputSelectDrop = OptionMenu( top , self.inputSelectClicked , *options )
        self.inputSelectDrop.pack()

        # Input Select Button
        self.inputSelectButton = Button( top , text = "Select input" , command = self.updateLabel ).pack()

        # Input Select Label
        self.inputSelectLabel = Label( top , text = " " )
        self.inputSelectLabel.pack()



        self.startButton = tk.Button(top,text="Start",command=self.start)

        self.startButton.pack()

        top.mainloop()

    def start(self):
        self.layercontroller = LayerController(self.inputID, resolution=8)
        self.layercontroller.start()

        #while True:
        #    if self.layercontroller.frames.qsize() >= 1:
        #        self.img = self.image_from_array(self, self.layercontroller.frames.get())
        #    else:
        #        time.sleep(0.1)

    def resize_pil_image(self, root, image):
        max_height, max_width = self.imgdim
        if (max_width is not None and max_height is not None): # change the image size to fit in a thumbnail
            #max_width = int(root.winfo_fpixels(max_width)) # convert the max_width to device pixels from physical units
            #max_height = int(root.winfo_fpixels(max_height)) # convert the max_height to device pixels from physical units
            image.thumbnail((max_width, max_height), Image.ANTIALIAS)

    def image_from_array(self, top, cv_image):
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB) # convert colorspace from BGR to RGB
        pil_image = Image.fromarray(cv_image)
        self.resize_pil_image(top, pil_image)
        tk_image = ImageTk.PhotoImage(pil_image)
        return tk_image

    def updateLabel(self):
        self.inputSelectLabel.config( text = self.inputSelectClicked.get() )
        self.inputID = self.allConnectedAudio[self.inputSelectClicked.get()]
