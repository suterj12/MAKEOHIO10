# This will import all the widgets
# and modules which are available in
# tkinter and ttk module
from tkinter import *
from tkinter.ttk import *
from gtts import *
from playsound import playsound
 
# creates a Tk() object
master = Tk()
 
# sets the geometry of main 
# root window
master.geometry("500x500")
 
 
# function to open a new window 
# on a button click
def openNewWindow():
        
    # Toplevel object which will 
    # be treated as a new window
    newWindow = Toplevel(master)
 
    # sets the title of the
    # Toplevel widget
    newWindow.title("New Window")
 
    # sets the geometry of toplevel
    newWindow.geometry("1000x1000")
 
    # A Label widget to show in toplevel
    Label(newWindow, 
          text ="This is a new window").pack()
     
 
label = Label(master, text ="This is the main window", font=("Arial", 25))
 
label.pack(pady = 10)
 
# a button widget which will open a 
# new window on button click
btn = Button(master, 
             text ="Click to open a new window", 
             command = openNewWindow)
btn.pack(pady = 10)


#section to implement text to speech
language = 'en'

# Passing the text and language to the engine,  
# here we have marked slow=False. Which tells  
# the module that the converted audio should  
# have a high speed 
audioObj = gTTS(text="howdy partner", lang=language, slow=False) 
  
soundFile = "runSound.mp3"

# Saving the converted audio in a mp3 file named welcome
audioObj.save(soundFile) 

soundFile = soundFile.replace(" ", "%20");
  
# Playing the converted file 
playsound(soundFile)  
 
# mainloop, runs infinitely
mainloop()