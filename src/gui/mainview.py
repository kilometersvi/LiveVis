from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror
import os
from .soundutil import SoundUtil

#figure out how to import SoundUtil

class MainWindow:

    def __init__(self):

        top = Tk()
        top.title("LiveVis")
        top.geometry('300x70')
        top.resizable(False, False)

        allConnectedAudio =



        startB = tk.Button(top,text="Start")#command=main)

        startB.pack()
        top.mainloop()

    def show(self):
        label.config( text = clicked.get() )
