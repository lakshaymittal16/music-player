from ast import Delete
from distutils.command.config import config
from tkinter import *
import tkinter.ttk as ttk
import shutil
import webbrowser
from PIL import ImageTk,Image 
from tkinter import filedialog
from pygame import mixer
from pydub.playback import play
from threading import Thread 
import os
import sys
import time


player = Tk()
player.geometry('500x350')
player.title('mp3 Player')
player.resizable(False,False)
sys.setrecursionlimit(1000)
mixer.init()
mixer.music.set_volume(0.5)

#variables
selection = StringVar()
selection.set('Options')
slidertime = DoubleVar() 
state = False
skip = True
initialPlay = False
removedSong = 0
#fetching file names
lst = os.listdir('music player/songs/')
lst2 = []
lst3 = []
lst.pop(0)
playlist = []

#playlist
for i in lst:
    Path = 'music player/songs/'+i
    playlist.append(Path)
currentsong = playlist[0]
currentsound = mixer.Sound(currentsong)

#list of names
for i in range(2):
    for i in lst:
        lst.remove(i)
        lst.append(i.rstrip('(online-audio-converter.com).mp3'))     


#commands
def options(n):
    if selection.get() == 'Add Song':
        #open file window
        song = filedialog.askopenfilename(initialdir='music player/songs/', title='Select A Song',filetypes=(('mp3','*.mp3'),))
        playlist.append(song)
        queue.insert(END, os.path.basename(song.rstrip('.mp3'))) 
        queue1.insert(END, os.path.basename(song.rstrip('.mp3'))) 
        shutil.copy(song, 'music player/songs/')
        selection.set('Options')
    
    elif selection.get() == 'Remove Song':
        #remove music window
        RemoveSong = Tk()

        def removeSelection():
            global removedSong
            lst3.append(int(str(queue1.curselection()).lstrip('(').rstrip(',)')))
            queue1.delete(int(str(queue1.curselection()).lstrip('(').rstrip(',)')))
            lst2.pop(lst3[removedSong])
            if len(lst3) > 1:
                lst3.pop(0)
            removedSong += 1
            remove()

        #remove music window listbox
        queue1 = Listbox(RemoveSong,width=42,height=12,bg='black',fg='green')
        queue1.grid(row=0,column=0,columnspan=3)
        

        for i in lst2:
            queue1.insert(END, i)
        
        while len(lst) != 0:
            queue1.insert(END, lst[0])
            lst2.append(lst[0])
            lst.remove(lst[0])

        #remove music window button
        removeButton = Button(RemoveSong,text='Remove Song',command=removeSelection)
        removeButton.grid(row=1,column=1)

        selection.set('Options')
        RemoveSong.mainloop()
    
    elif selection.get() == 'Convert File Type':
        #open browser
        webbrowser.open('https://audio.online-convert.com/convert-to-mp3', new=1)
        filedialog.askopenfilename(initialdir='Desktop/', title='Select A File',filetypes=(('Audio Files','*.*'),))
        selection.set('Options')

def pause():
    global state
    global initialPlay
    
    #to replay the song if it ends
    if not mixer.music.get_busy() and state == True:
        mixer.music.load(currentsong)
        mixer.music.play()
        queue.select_set(playlist.index(currentsong))
        queue.select_clear(playlist.index(currentsong) - 1)
        currentsound = mixer.Sound(currentsong)
        songLength = int(currentsound.get_length())
        Thread(target= slider).start()
        Thread(target= lambda:timeUpdate()).start()
        return
    
    state = not state
    if state == True:
        if initialPlay == False:
            mixer.music.load(currentsong)
            mixer.music.play(loops=0)
            queue.select_set(playlist.index(currentsong))
            queue.select_clear(playlist.index(currentsong) - 1)
            currentsound = mixer.Sound(currentsong)
            songLength = int(currentsound.get_length())
            Thread(target= slider).start()
            Thread(target= lambda:timeUpdate()).start()
            initialPlay = True
        elif not mixer.music.get_busy:
            mixer.music.load(currentsong)
            mixer.music.play(loops=0)
        
        #to not play the song from begining 
        else:
            mixer.music.unpause()
            queue.select_set(playlist.index(currentsong))
            currentsound = mixer.Sound(currentsong)
            songLength = int(currentsound.get_length())
            Thread(target= slider).start()
            Thread(target= lambda:timeUpdate()).start()
  
    else:
        mixer.music.pause()

def change(n):
    global state
    global currentsong
    global currentsong
    global songLength
    global skip
    state = True
    #checking if the user isn't on last song
    if n == 1 and playlist.index(currentsong) != len(playlist)-1:
        skip = False
        currentsong = playlist[playlist.index(currentsong)+ 1]
        currentsound = mixer.Sound(currentsong)
        songLength = int(currentsound.get_length())
        mixer.music.load(currentsong)
        mixer.music.play()
        queue.select_set(playlist.index(currentsong))
        queue.select_clear(playlist.index(currentsong) - 1)
        Thread(target= slider).start()
    
    elif n == 1 and playlist.index(currentsong) == len(playlist)-1:
        skip = False
        currentsong = playlist[0]
        currentsound = mixer.Sound(currentsong)
        songLength = int(currentsound.get_length())
        mixer.music.load(currentsong)
        mixer.music.play()
        queue.select_set(playlist.index(currentsong))
        queue.select_clear(len(playlist)-1)
        Thread(target= slider).start()

    #checking if the user isn't on the first song
    elif n == 0 and playlist.index(currentsong) != 0:    
        skip = False
        currentsong = playlist[playlist.index(currentsong) - 1]
        currentsound = mixer.Sound(currentsong)
        songLength = int(currentsound.get_length())
        mixer.music.load(currentsong)
        mixer.music.play()
        queue.select_set(playlist.index(currentsong))
        queue.select_clear(playlist.index(currentsong) + 1)
        Thread(target= slider).start()
    
    elif n == 0 and playlist.index(currentsong) == 0:
        skip = False
        currentsong = playlist[len(playlist)-1]
        currentsound = mixer.Sound(currentsong)
        songLength = int(currentsound.get_length())
        mixer.music.load(currentsong)
        mixer.music.play()
        queue.select_set(playlist.index(currentsong))
        queue.select_clear(0)
        Thread(target= slider).start()
    
    #starting timer and slider if the music is skipped 
    if n == 0 or 1 and mixer.music.get_busy():
        Thread(target= slider).start()
        Thread(target= lambda:timeUpdate()).start()

def volume(n):
    mixer.music.set_volume(volumeSlider.get()/100)

def timeUpdate():
    global songLength
    global skip
    #loop till song is playing or skipped
    while mixer.music.get_busy() and skip != False:
        currentLength = mixer.music.get_pos() / 1000
        timeFormat = time.strftime('%M:%S', time.gmtime(int(currentLength)))
        timeFormat1 = time.strftime('%M:%S', time.gmtime(songLength))
        timer.config(text=timeFormat + '/' + timeFormat1)
    skip = True


def slider():
    global songLength
    global sliderPosition
    while  mixer.music.get_busy():
        currentPosition = mixer.music.get_pos()/1000
        sliderPosition = (currentPosition/songLength)*100
        musicSlider.set(sliderPosition)

def remove():
    global currentsong
    for i in lst3:
        #checking if the song removed is the one currently playing
        if currentsong == playlist[i]:
            if i == len(playlist) - 1 :
                queue.delete(i)
                playlist.pop(i)
                playlist.pop(i)
                currentsong = playlist[0]
            else:
                queue.delete(i)
                playlist.pop(i)
                currentsong = playlist[i+1]
        else:
            queue.delete(i)
            playlist.pop(i)
         
        

#images
pauseImage = ImageTk.PhotoImage(Image.open('music player/pause-button.png'))
forwardImage = ImageTk.PhotoImage(Image.open('music player/forward-button.jpeg'))
backwardImage = ImageTk.PhotoImage(Image.open('music player/backward-button.jpeg'))
bgImage = ImageTk.PhotoImage(Image.open('music player/pastel-blue-vignette-concrete-textured-background.jpg'))

#app background
background = Label(player,image=bgImage).place(x=0,y=0)

#dropbox
optionsMenu = OptionMenu(player, selection, 'Add Song','Remove Song', 'Convert File Type',command=options).grid(row=0,column=0)

#listbox
queue = Listbox(player,width=42,height=12,bg='black',fg='green')
queue.place(x=30,y=35)


#adding to queue
for i in lst:
    queue.insert(END, i)       

#buttons
backwardButton = Button(player,image=backwardImage, command=lambda:change(0)).place(x=100,y=280)
pauseButton = Button(player,image=pauseImage,command=pause).place(x=210,y=280)
forwardButton = Button(player,image=forwardImage,command=lambda:change(1)).place(x=320,y=280)

#sliders
volumeSlider = Scale(player, from_=100, to=0,length=204,orient=VERTICAL,command=volume)
volumeSlider.set(50)
volumeSlider.place(x=410,y=35)

musicSlider = ttk.Scale(player,variable=slidertime,from_=0,to=100,length=343,orient=HORIZONTAL)
musicSlider.place(x=30,y=242)

#timer
songLength = int(currentsound.get_length())
timer = Label(player,text='00:00/00:00',borderwidth=3)
timer.place(x=373,y=242)

player.mainloop()
