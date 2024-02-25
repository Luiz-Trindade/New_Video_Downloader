gpl3_text='''
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

from customtkinter import *
from pytube import YouTube
from tkinter import PhotoImage, filedialog
from time import sleep
from multiprocessing import Process
import pygame as pg
pg.init()

url_list = []
alert_sound = ("_internal/sound/alert_sound.mp3")
pg.mixer.music.load(alert_sound)

def Alert(msg):
    pg.mixer.music.play()
    Alert = CTkToplevel(master=app)
    Alert.title("Notification🔔")
    Alert.geometry("450x150")
    Alert.iconphoto(False, app_icon)
    Alert_Message = CTkLabel(master=Alert, text=msg, font=("Arial", 30, "bold"))
    Alert_Message.pack(pady=20, padx=10)
    #sleep(5)

def Add_Url_To_List():
    global url_list
    url = video_url_entrt.get()
    if url:
        url_list.append(url)
        total_videos_label.configure(text=f"Total Videos: {len(url_list)}")
        video_url_entrt.delete(0, len(url))
    else: Alert("Add an URL!")

def Download_Videos(part, path):
    global url_list
    
    for i in part:
        yt = YouTube(i)
        video_stream = yt.streams.first()
        video_stream.download(output_path=path)


def Reset_List():
    global url_list
    url_list = []
    total_videos_label.configure(text="Total Videos: 0")

def Main():
    global url_list

    download_path = filedialog.askdirectory(title="Select the destination path")
    qntd = int(int(len(url_list)) / 4)

    part1 = url_list[:qntd]
    part2 = url_list[qntd:qntd*2]
    part3 = url_list[qntd*2:qntd*3]
    part4 = url_list[qntd*3:]

    p1 = Process(target=Download_Videos, args=(part1, download_path,))
    p2 = Process(target=Download_Videos, args=(part2, download_path,))
    p3 = Process(target=Download_Videos, args=(part3, download_path,))
    p4 = Process(target=Download_Videos, args=(part4, download_path,))

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join() 

    Alert("Download(s) concluído(s) com sucesso!")


set_widget_scaling(1.5)
set_appearance_mode("dark")
set_default_color_theme("green")

app = CTk()
app.title("New Video Downloader")
app.geometry("600x400")
app_icon = PhotoImage(file="_internal/icons/icon.png")
app.iconphoto(False, app_icon)

tabview = CTkTabview(master=app)
tabview.pack(pady=10, padx=10)

tab1 = tabview.add("Download")
tab2 = tabview.add("About")

frame = CTkFrame(master=tab1)
frame.pack(pady=20, padx=10)

total_videos_label = CTkLabel(master=frame, text="Total Videos: 0", font=("Arial", 20, "bold"), justify="center")
total_videos_label.grid(row=0, column=0, pady=10, padx=10)

video_url_entrt = CTkEntry(master=frame, placeholder_text="Video URL", justify="center")
video_url_entrt.grid(row=1, column=0, pady=10, padx=10)

add_url_button = CTkButton(master=frame, text="Add", command=Add_Url_To_List)
add_url_button.grid(row=1, column=1, pady=10, padx=10)

reset_list_button = CTkButton(master=frame, text="Reset", fg_color="red", hover_color="orange",command=Reset_List)
reset_list_button.grid(row=2, column=0, pady=10, padx=10)

download_button = CTkButton(master=frame, text="Download", command=Main)
download_button.grid(row=2, column=1, pady=10, padx=10)


frame2 = CTkFrame(master=tab2)
frame2.pack(pady=10, padx=10)

about_label = CTkLabel(master=frame2, text=gpl3_text, font=("Arial", 8, "bold"), justify="left")
about_label.pack(pady=10, padx=10)

app.mainloop()
