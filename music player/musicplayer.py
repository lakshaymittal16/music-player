from distutils.command.config import config
from tkinter import *
import tkinter.ttk as ttk
import shutil
import webbrowser
from PIL import ImageTk,Image 
from tkinter import filedialog
from pygame import mixer
from pydub import AudioSegment
from pydub.playback import play 
import os
import sys
import time


player = Tk()
player.geometry('500x350')
player.resizable(False,False)
sys.setrecursionlimit(1000)
mixer.init()
mixer.music.set_volume(0.5)

#variables
selection = StringVar()
selection.set('Options') 
state = False
lst = os.listdir('music player/songs/')
lst.pop(0)
playlist = []

#playlist
for i in lst:
    Path = 'music player/songs/'+i
    playlist.append(Path)
currentsong = playlist[0]

#list of names
for i in range(2):
    for i in lst:
        lst.remove(i)
        lst.append(i.rstrip('(online-audio-converter.com).mp3'))     


#commands
def options(n):
    if selection.get() == 'Add Music':
        #open file window
        song = filedialog.askopenfilename(initialdir='music player/songs/', title='Select A Song',filetypes=(('mp3','*.mp3'),))
        playlist.append(song)
        queue.insert(END, os.path.basename(song.rstrip('.mp3'))) 
        shutil.copy(song, 'music player/songs/')
    elif selection.get() == 'Convert File Type':
        #open browser
        webbrowser.open('https://audio.online-convert.com/convert-to-mp3', new=1)
        filedialog.askopenfilename(initialdir='Desktop/', title='Select A File',filetypes=(('Audio Files','*.*'),))

def pause():
    global state
    state = not state
    if state == True:
        mixer.music.load(currentsong)
        mixer.music.play()
        queue.select_set(playlist.index(currentsong))
        #timeUpdate()
        slider()  
    else:
        mixer.music.pause()

def change(n):
    global state
    global currentsong
    state = not state
    #checking if the user isn't on last song
    if n == 1 and playlist.index(currentsong) != len(playlist)-1:
        currentsong = playlist[playlist.index(currentsong)+ 1]
        mixer.music.load(currentsong)
        mixer.music.play()
        queue.select_set(playlist.index(currentsong))
        #timeUpdate()
        slider()
    elif n == 1 and playlist.index(currentsong) == len(playlist)-1:
        currentsong = playlist[0]
        mixer.music.load(currentsong)
        mixer.music.play()
        queue.select_set(playlist.index(currentsong))
        #timeUpdate()
        slider()
    #checking if the user isn't on the first song
    elif n == 0 and playlist.index(currentsong) != 0:    
        currentsong = playlist[playlist.index(currentsong) - 1]
        mixer.music.load(currentsong)
        mixer.music.play()
        queue.select_set(playlist.index(currentsong))
        #timeUpdate()
        slider()
    elif n == 0 and playlist.index(currentsong) == 0:
        currentsong = playlist[len(playlist)-1]
        mixer.music.load(currentsong)
        mixer.music.play()
        queue.select_set(playlist.index(currentsong))
        #timeUpdate()
        slider()

def volume(n):
    mixer.music.set_volume(volumeSlider.get()/100)

def timeUpdate():
    global songLength
    #loop till song is playing
    while mixer.music.get_busy():
        currentLength = mixer.music.get_pos() / 1000
        timeFormat = time.strftime('%M:%S', time.gmtime(currentLength))
        timeFormat1 = time.strftime('%M:%S', time.gmtime(songLength))
        timer.config(text=timeFormat + '/' + timeFormat1)

def slider():
    global songLength
    while mixer.music.get_busy():
        currentLength = int(mixer.music.get_pos() / 1000)
        songLength = int(AudioSegment.from_file(currentsong).duration_seconds)
        sliderPosition = int((currentLength/songLength)*100)
        print(sliderPosition)
        musicSlider.config(to=sliderPosition)

#images
pauseImage = ImageTk.PhotoImage(Image.open('music player/pause-button.png'))
forwardImage = ImageTk.PhotoImage(Image.open('music player/forward-button.jpeg'))
backwardImage = ImageTk.PhotoImage(Image.open('music player/backward-button.jpeg'))

#dropbox
optionsMenu = OptionMenu(player, selection, 'Add Music', 'Convert File Type',command=options).grid(row=0,column=0)
lbl = Label(player,text='__PLAYLIST__',fg = 'red').grid(row=1,column=0)


#listbox
queue = Listbox(player,width=40,height=12,bg='black',fg='green')
queue.grid(row=2,column=0,columnspan=4,padx=20)

#adding to queue
while len(lst) != 0:
    queue.insert(END, lst[0])
    lst.remove(lst[0])       

#buttons
backwardButton = Button(player,image=backwardImage, command=lambda:change(0)).grid(row=6,column=0)
pauseButton = Button(player,image=pauseImage,command=pause).grid(row=6,column=1)
forwardButton = Button(player,image=forwardImage,command=lambda:change(1)).grid(row=6,column=2)

#sliders
volumeSlider = Scale(player, from_=100, to=0,length=200,command=volume )
volumeSlider.set(50)
volumeSlider.grid(row=2,column=4)

musicSlider = ttk.Scale(player,from_=0,to=100,length=370,orient=HORIZONTAL)
musicSlider.grid(row=4,column=0,columnspan=4)

#timer
songLength = int(AudioSegment.from_file(currentsong).duration_seconds)
timer = Label(player,text='00:00/00:00')
timer.grid(row=4,column=4)

player.mainloop()