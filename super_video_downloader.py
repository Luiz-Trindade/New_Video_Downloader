# Importing necessary libraries
from customtkinter import *
from yt_dlp import YoutubeDL
from tkinter import PhotoImage, filedialog
from time import sleep
from multiprocessing import Process
import pygame as pg
from os import listdir, remove
import ffmpeg

# Initializing pygame for sound playback
pg.init()

# Copyright and license information for the program
gpl3_text = '''
    Simple YouTube Video Downloader Written In Python!

    Copyright (C) 2024  Luiz Gabriel Magalhães Trindade.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

# Initializing global variables
url_list = []
alert_sound = ("_internal/sound/alert_sound.mp3")
pg.mixer.music.load(alert_sound)
highest_resolution = True
videoToAudio = False

# Function to display an alert notification
def Alert(msg):
    pg.mixer.music.play()
    Alert = CTkToplevel(master=app)
    Alert.title("Notification🔔")
    Alert.geometry("450x150")
    Alert.iconphoto(False, app_icon)
    Alert_Message = CTkLabel(master=Alert, text=msg, font=("Arial", 15, "bold"))
    Alert_Message.pack(pady=20, padx=10)

# Function to add URL to the download list
def Add_Url_To_List():
    global url_list
    url = video_url_entrt.get()
    if url:
        if "playlist" in url:
            ydl_opts = {
                'extract_flat': True,
                'quiet': True,
            }
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                url_list = [video['url'] for video in info['entries']]
                total_videos_label.configure(text=f"Total Videos: {len(url_list)}")
                video_url_entrt.delete(0, len(url))

        else:
            url_list.append(url)
            total_videos_label.configure(text=f"Total Videos: {len(url_list)}")
            video_url_entrt.delete(0, len(url))
    else:
        Alert("Add an URL!")

# Function to download videos using threading
def Download_Videos(part, path):
    global url_list, highest_resolution

    if part == []:
        #print("Null")
        pass

    else:
        if path:
            for i in part:
                try:
                    options = {
                        "format": "bestvideo[ext=mp4]+bestaudio[ext=mp4a]/best[ext=mp4]/best",
                        "outtmpl": f"{path}/%(title)s.%(ext)s",
                        "limit-rate": -1
                    }
                    with YoutubeDL(options) as ydl:
                        info = ydl.extract_info(i, download=True)
                except Exception as error:
                    Alert("Vídeo não baixado!")
                    pass

        
# Function to reset the download list
def Reset_List():
    global url_list
    url_list = []
    total_videos_label.configure(text="Total Videos: 0")

#Function to convert the video to audio
def ConvertVideoToAudio(downloadDir):
    global videoToAudio
    video_path  = listdir(downloadDir)
    video_list  = []
    
    for video in video_path:
        if ".mp4" in video:
            video_list.append(f"{downloadDir}/{video}")

    for video in video_list:
        # Criar um objeto FFmpeg
        ff = ffmpeg.input(video)
        # Definir a saída como MP3
        ff = ff.output(video.replace(".mp4", ".mp3"))
        # Executar a conversão
        ff.run()

        #Remove video
        remove(video)

# Main function to initiate video downloads
def Main():
    global url_list, videoToAudio

    # Asking user for the destination path
    download_path = filedialog.askdirectory(title="Select the destination path")
    
    # Dividing the URL list into four parts
    qntd = int(int(len(url_list)) / 4)
    part1 = url_list[:qntd]
    part2 = url_list[qntd:qntd*2]
    part3 = url_list[qntd*2:qntd*3]
    part4 = url_list[qntd*3:]

    # Creating threadings for each part and starting them
    p1 = Process(target=Download_Videos, args=(part1, download_path,))
    p2 = Process(target=Download_Videos, args=(part2, download_path,))
    p3 = Process(target=Download_Videos, args=(part3, download_path,))
    p4 = Process(target=Download_Videos, args=(part4, download_path,))

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    # Waiting for all threadings to finish
    p1.join()
    p2.join()
    p3.join()
    p4.join()

    #Convert to audio when finish to download all videos
    if videoToAudio == True:
        ConvertVideoToAudio(download_path)

    # Displaying a success notification
    Alert("Download(s) completed successfully!")

# Setting up the GUI using CustomTkinter
set_widget_scaling(1.5)
set_appearance_mode("dark")
set_default_color_theme("green")

app = CTk()
app.title("Super Video Downloader")
app.geometry("600x400")
app_icon = PhotoImage(file="_internal/icons/icon.png")
app.iconphoto(False, app_icon)

# Creating tabs for download and about sections
tabview = CTkTabview(master=app)
tabview.pack(pady=10, padx=10)

tab1 = tabview.add("Download")
tab2 = tabview.add("About")

# Creating frames for each tab
frame = CTkFrame(master=tab1)
frame.pack(pady=20, padx=10)

frame2 = CTkFrame(master=tab2)
frame2.pack(pady=10, padx=10)

# GUI elements for the download tab
total_videos_label = CTkLabel(master=frame, text="Total Videos: 0", font=("Arial", 20, "bold"), justify="center")
total_videos_label.grid(row=0, column=0, pady=10, padx=10)

def checkboxEvent():
    global videoToAudio
    if videoToAudio == False:
        videoToAudio = True
    else:
        videoToAudio = False

#checkbox
checkboxVar = StringVar(value="audio")
checkbox = CTkCheckBox(master=frame, text="Download audio?", command=checkboxEvent, variable=checkboxVar, 
                        onvalue="video", offvalue="audio")
checkbox.grid(row=0, column=1, pady=10, padx=10)

video_url_entrt = CTkEntry(master=frame, placeholder_text="Video URL", justify="center")
video_url_entrt.grid(row=1, column=0, pady=10, padx=10)

add_url_button = CTkButton(master=frame, text="Add", command=Add_Url_To_List)
add_url_button.grid(row=1, column=1, pady=10, padx=10)

reset_list_button = CTkButton(master=frame, text="Reset", fg_color="red", hover_color="orange", command=Reset_List)
reset_list_button.grid(row=2, column=0, pady=10, padx=10)

download_button = CTkButton(master=frame, text="Download", command=Main)
download_button.grid(row=2, column=1, pady=10, padx=10)

# GUI element for the about tab
about_label = CTkLabel(master=frame2, text=gpl3_text, font=("Arial", 8, "bold"), justify="left")
about_label.pack(pady=10, padx=10)

# Running the application
app.mainloop()
