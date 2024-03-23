from google.cloud import videointelligence
from webcam import Webcam
import tkinter as tk # base tk library
from tkinter import ttk # newer tk widgets
import cv2
from gtts import gTTS
from itertools import islice
from PIL import Image, ImageTk # for converting webcam images to show in tk

webcam: Webcam = None
lastframe = None

preview: tk.Label = None

def press_connect_webcam(event=None):
    global webcam
    webcam = Webcam(src=2)
    if webcam is None:
        print("Failed to connect.")
    else:
        print("Connected!")
        print(f'{webcam.w}x{webcam.h}')

def update_webcam_preview():
    global webcam
    if webcam is None:
        return
    
    frame = next(webcam)
    # print(frame.shape)

    global lastframe
    lastframe = frame

    # convert image data to a form suitable for tk
    pillowimg = Image.fromarray(frame)
    tkimg = ImageTk.PhotoImage(image=pillowimg)
    # print(tkimg.width(), tkimg.height())

    # show the image
    global preview
    preview.config(image=tkimg)
    preview.image = tkimg # see https://stackoverflow.com/questions/3482081/how-to-update-the-image-of-a-tkinter-label-widget
    preview.pack()

def is_clean(frame) -> bool:
    # TODO: send data to api, determine if environment is clean or dirty
    return False

def press_finish_button(event=None):
    global webcam
    if webcam is None:
        print('No webcam connected!')
        return
    
    # fetch image data
    global lastframe
    if lastframe is None:
        print('No webcam data! Is the webcam connected?')
        return

    if is_clean(lastframe):
        print("Nice! Everything's clean!")
    else:
        print("There's still more to clean!")

    # print('Success!')

if __name__ == '__main__':
    root = tk.Tk()
    ttk.Label(root, text='KAM').pack()

    # preview = tk.PhotoImage()
    # preview.
    preview = ttk.Label(root, image=[])
    preview.pack()

    b = ttk.Button(root, text='Connect webcam', command=press_connect_webcam)
    b.bind('<Return>', press_connect_webcam)
    b.pack()

    b = ttk.Button(root, text='Finish', command=press_finish_button)
    b.bind('<Return>', press_finish_button)
    b.pack()

    # root.mainloop()

    while True:
        update_webcam_preview()
        root.update_idletasks()
        root.update()
