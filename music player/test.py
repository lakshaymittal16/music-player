from operator import truediv
from subprocess import list2cmdline
from tkinter import *
from PIL import ImageTk,Image 
from tkinter import filedialog
from pygame import mixer
import pydub
from pydub.playback import play 
import os
lst = ['apple.com','google.com']
for i in lst:
    lst.remove(i)
    lst.append(i.rstrip('.com'))
print(lst)