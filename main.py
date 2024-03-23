from google.cloud import videointelligence
from webcam import Webcam
import tkinter as tk # base tk library
from tkinter import ttk # newer tk widgets
import cv2
from gtts import gTTS

webcam: Webcam = None

def press_connect_webcam(event=None):
    global webcam
    webcam = Webcam(src=2)

def press_finish_button(event=None):
    print('Hello, world!')
    global webcam
    if webcam is not None:
        print(webcam.w, webcam.h)
        for frame in webcam:
            print(frame)
            cv2.imshow('webcam', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        print('Success!')

if __name__ == '__main__':
    root = tk.Tk()
    ttk.Label(root, text='KAM').pack()

    b = ttk.Button(root, text='Connect webcam', command=press_connect_webcam)
    b.bind('<Return>', press_connect_webcam)
    b.pack()

    b = ttk.Button(root, text='Finish', command=press_finish_button)
    b.bind('<Return>', press_finish_button)
    b.pack()

    root.mainloop()
