import tkinter as tk
from tkinter import filedialog
import pygame
from pygame import mixer

def open_file():
    file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    if file:
        current_track.set(file.split("/")[-1])
        mixer.music.load(file)

def play_music():
    if not mixer.music.get_busy():
        mixer.music.play()

def pause_music():
    if mixer.music.get_busy():
        mixer.music.pause()

def stop_music():
    mixer.music.stop()
    current_track.set("")

# Инициализация окна
root = tk.Tk()
root.title("Simple Music Player")
root.geometry("400x150")

mixer.init()

# Элементы интерфейса
current_track = tk.StringVar()
track_label = tk.Label(root, textvariable=current_track, width=50)
track_label.pack(pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

btn_open = tk.Button(button_frame, text="Open", command=open_file)
btn_play = tk.Button(button_frame, text="Play", command=play_music)
btn_pause = tk.Button(button_frame, text="Pause", command=pause_music)
btn_stop = tk.Button(button_frame, text="Stop", command=stop_music)

btn_open.grid(row=0, column=0, padx=5)
btn_play.grid(row=0, column=1, padx=5)
btn_pause.grid(row=0, column=2, padx=5)
btn_stop.grid(row=0, column=3, padx=5)

root.mainloop()
