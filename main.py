from google.cloud import videointelligence
from google.oauth2 import service_account
from webcam import Webcam
import tkinter as tk # base tk library
from tkinter.messagebox import showinfo
from tkinter import ttk # newer tk widgets
import cv2
from gtts import gTTS
from itertools import islice
from PIL import Image, ImageTk # for converting webcam images to show in tk
from io import BytesIO

CREDENTIALS = service_account.Credentials.from_service_account_file(
    '.env')
FEATURES = [videointelligence.Feature.OBJECT_TRACKING]
video_client = videointelligence.VideoIntelligenceServiceClient(credentials=CREDENTIALS)

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

class BoundingBox:
    """
    all values range from 0 to 1 (they are proportional to the image)
    """
    def __init__(self, x: float, y: float, w: float, h: float):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def get_center(self) -> tuple[float, float]:
        return (
            self.x + (self.w / 2),
            self.y + (self.h / 2)
        )
    
    def __str__(self) -> str:
        return f'{self.x:.1f}, {self.h:.1f}, {self.w:.1f}x{self.h:.1f}'

class Object:
    def __init__(self, name: str, confidence: float, bounds: BoundingBox):
        self.name = name
        self.confidence = confidence
        self.bounds = bounds
    
    def __str__(self) -> str:
        return f'{self.confidence*100:.1f}% {self.name} @ {{{self.bounds}}}'

def detect_objects(data) -> list[Object]:
    """
    `data` is a binary video or image file
    """
    results: list[Object] = []

    global video_client
    global FEATURES
    operation = video_client.annotate_video(
        request={"features": FEATURES, "input_content": data}
    )

    print("Detecting objects...")
    result = operation.result(timeout=500)

    # The first result is retrieved because a single file was processed.
    object_annotations = result.annotation_results[0].object_annotations
    print(f'{len(object_annotations)} objects detected.')

    # process results
    for annotation in object_annotations:
        print("Entity description: {}".format(annotation.entity.description))
        if annotation.entity.entity_id:
            print("Entity id: {}".format(annotation.entity.entity_id))

        print(
            "Segment: {}s to {}s".format(
                annotation.segment.start_time_offset.seconds
                + annotation.segment.start_time_offset.microseconds / 1e6,
                annotation.segment.end_time_offset.seconds
                + annotation.segment.end_time_offset.microseconds / 1e6,
            )
        )

        print("Confidence: {}".format(annotation.confidence))

        bounds = annotation.frames[0].normalized_bounding_box
        bb = BoundingBox(
            bounds.left,
            bounds.top,
            bounds.right - bounds.left,
            bounds.bottom - bounds.top
        )
        o = Object(
            annotation.entity.description,
            annotation.confidence,
            bb
        )
        results.append(o)

    return results

def get_object_message(o: Object) -> str:
    position = 'ahead'
    if o.bounds.get_center()[0] < 0.33:
        position = 'to your left'
    elif o.bounds.get_center()[0] > 0.66:
        position = 'to your right'
    return f"There's a {o.name} {position}."

def say_message(msg: str):
    # TODO: use gTTS to say the message
    showinfo('info', msg)

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

    # convert image data to format useable by videointelligence api
    img = Image.fromarray(lastframe)
    buffer = BytesIO()
    img.save(buffer, format='png')
    buffer.seek(0)
    imgfile = buffer.read()
    print(len(imgfile))

    objects = detect_objects(imgfile)

    for o in objects:
        print(o)
        print(o.bounds.get_center())
    
    for o in objects:
        say_message(get_object_message(o))

    # if detect_objects(imgfile):
    #     print("Nice! Everything's clean!")
    #     showinfo(":)", "Nice! Everything's clean!")
    # else:
    #     print("There's still more to clean!")
    #     showinfo(":()", "There's still more to clean!")

    # print('Success!')

if __name__ == '__main__':
    root = tk.Tk()
    ttk.Label(root, text='KAM').pack()

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
