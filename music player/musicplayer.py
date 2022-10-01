from operator import truediv
from tkinter import *
from PIL import ImageTk,Image 
from tkinter import filedialog
from pydub import AudioSegment
from pydub.playback import play 
import os

root = Tk()
state = False
lst = os.listdir('music player/songs/')
lst.pop(0)
playlist = []
for i in lst:
    s = 'music player/songs/'+i
    print(s)
    playlist.append(s)
currentsong = AudioSegment.from_mp3(playlist[0])
#commands
def add():
    song = filedialog.askopenfilename(initialdir='music player/songs/', title='Select A Song',filetypes=(('mp3','*.mp3'),('m4a','*.m4a')))
    playlist.append(song)
def pause():
    global state 
    state = not state
    if state == True:
        play(currentsong)
        
    else:
        return
        








#widgets
pauseImage = ImageTk.PhotoImage(Image.open('music player/pause-button.png'))
forwardImage = ImageTk.PhotoImage(Image.open('music player/forward-button.jpeg'))
backwardImage = ImageTk.PhotoImage(Image.open('music player/backward-button.jpeg'))


addButton = Button(root,text='Add Song',command=add).grid(row=0,column=0)
queue = Entry(root,width=50).grid(row=2,column=2)
pauseButton = Button(root,image=pauseImage,command=pause).grid(row=6,column=3)
forwardButton = Button(root,image=forwardImage).grid(row=6,column=4)
backwardButton = Button(root,image=backwardImage).grid(row=6,column=2)
root.mainloop()