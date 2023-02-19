import socket 
from threading import Thread 
from tkinter import *
from tkinter import ttk
from playsound import playsound
import pygame
from pygame import mixer
import os
import time
import ftplib
from ftplib import  FTP
import ntpath 
from pathlib import Path

PORT =8050
IP_ADDRESS = "127.0.0.1"
SERVER = None
BufferSize = 4096
song_Counter = 0

def browseFiles():
    global Listbox
    global song_Counter
    global filePathLabel

    try:
        filename = filedialog.askopenfilename()
        HOSTNAME = "127.0.0.1"
        USERNAME = "lftpd"
        PASSWORD = "lftpd"
        ftp_server = FTP(HOSTNAME,USERNAME,PASSWORD)
        ftp_server.encoding = "utf-8"
        ftp_server.cwd("shared_files")
        fname = ntpath.basename(filename)
        with open(filename, "rb") as file:
            ftp_server.storbinary(f"STOR {filename} " ,file)
        ftp_server.dir()
        ftp_server.quit()
    except FileNotFoundError:
        print("Cancel Button Pressed")

def download():
    song_to_download = listbox.get(ANCHOR)
    infolabel.configure(text="Downloading" + song_to_download)
    HOSTNAME = "127.0.0.1"
    USERNAME = "lftpd"
    PASSWORD = "lftpd"
    home = str(Path.home())
    download_path = home + "/Downloads"
    ftp_server = ftplib.FTP(HOSTNAME,USERNAME,PASSWORD)
    ftp_server.encoding = "utf-8"
    ftp_server.cwd("shared_files")
    local_filename = os.path.join(download_path,song_to_download)
    file = open(local_filename,"wb")
    ftp_server.retrbinary("RETR" + song_to_download,file.write)
    ftp_server.dir()
    file.close()
    ftp_server.quit()
    infolabel.configure(text = "Download Complete")
    time.sleep(1)
    if(songSelected !== ""):
        infolabel.configure(text="Now Playing" + songSelected)
    else : 
        infolabel.configure(text = "")     

def resume():
    global songSelected
    mixer.init()
    mixer.music.load('shared_files/'+songSelected)
    mixer.music.play()

def pause():
    global songSelected
    mixer.init()
    mixer.music.load('shared_files/'+songSelected)
    mixer.music.pause()

for file in os.listdir("shared_files"):
        filename = os.fsdecode(file)
        listBox.insert(song_Counter,filename)
        song_Counter = song_Counter + 1

def play():
    global songSelected 
    songSelected = listBox.get(ANCHOR)
    pygame
    mixer.init()
    mixer.music.load("shared_files/"+ songSelected)
    mixer.music.play()
    if(songSelected != ""):
        infoLabel.configure(text="Now Playing" + songSelected)
    else : 
        infoLabel.configure(text="") 

def stop():
    global songSelected
    pygame
    mixer.init()
    mixer.music.load("shared_files/"+ songSelected)
    mixer.music.pause()
    infoLabel.configure(text="")

def musicWindow():
    window = Tk()
    window.title("Music Window")
    window.geometry("600x600")
    window.configure(bg="LightSkyBlue")

    selectLabel = Label(window,text="Select Song",bg="LightSkyBlue",font=("Calibri",20))
    selectLabel.place(x=4,y=2)
    listBox = Listbox(window,height=10,width=40,activestyle="dotbox",bg="LightSkyBlue",borderwidth=4,font=("Calibri",20))
    listBox.place(x=20,y=45)
    scrollBar=Scrollbar(listBox)
    scrollBar.place(relheight=1,relx=1)
    scrollBar.config(command=listBox.yview)
    playButton=Button(window,text="Play",width=10,bd=1,bg="SkyBlue",font=("Calibri",10), command=play)
    playButton.place(x=30,y=450)
    stop=Button(window,text="Stop",bd=1,width=10,bg="SkyBlue",font=("Calibri",10),command=stop)
    stop.place(x=200,y=450)
    upload=Button(window,text="Upload",width=10,bd=1,bg="SkyBlue",font=("Calibri",10))
    upload.place(x=30,y=500)
    download=Button(window,text="Download",width=10,bd=1,bg="skyBlue",font=("Calibri",10))
    download.place(x=200,y=500)
    infoLabel=Label(window,text="",fg="blue",font=("Calibri",10))
    infoLabel.place(x=4,y=530)
    resumeButton = Button(window,text="Resume",width= 10 ,bd= 1,bg="skyBlue",font=("Calibri",10),command=resume)
    resumeButton.place(x=30,y=250)
    pauseButton = Button(window,text="Pause",width= 10 ,bd= 1,bg="skyBlue",font=("Calibri",10),command=pause)
    pauseButton.place(x=200,y=250)

    window.mainloop()

          
def setup():
    global SERVER
    global PORT
    global IP_ADDRESS 

    SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS,PORT))
    musicWindow()
setup()