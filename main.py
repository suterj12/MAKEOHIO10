from google.cloud import videointelligence
from webcam import Webcam
import tkinter as tk # base tk library
from tkinter import ttk # newer tk widgets

def press_finish_button(event=None):
    print('Hello, world!')

if __name__ == '__main__':
    root = tk.Tk()
    ttk.Label(root, text='KAM').pack()
    b = ttk.Button(root, text='Finish', command=press_finish_button)
    b.bind('<Return>', press_finish_button)
    b.pack()
    root.mainloop()
