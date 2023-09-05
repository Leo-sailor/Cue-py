# importing libraries
from pygame import mixer
import tkinter as tk
import tkinter.font as font
from tkinter import filedialog
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import wave

# Global variables
musicPlayer = None
visualization_fig = None
visualization_canvas = None
slider = None

# Function to create the musicPlayer window
def create_musicPlayer_window():
    global musicPlayer
    musicPlayer = tk.Toplevel()
    musicPlayer.title('Song Controller')
    musicPlayer.protocol("WM_DELETE_WINDOW", on_musicPlayer_close)

# Function to handle musicPlayer window closure
def on_musicPlayer_close():
    global musicPlayer
    musicPlayer.destroy()
    musicPlayer = None

# Function to visualize audio using matplotlib
def visualize_audio(file_path):
    global visualization_fig, visualization_canvas
    audio = wave.open(file_path, 'rb')
    framerate = audio.getframerate()
    samples = audio.readframes(-1)
    samples = np.frombuffer(samples, dtype=np.int16)
    time = np.linspace(0, len(samples) / framerate, num=len(samples))

    visualization_fig, ax = plt.subplots(figsize=(8, 2))
    ax.plot(time, samples)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    visualization_canvas = FigureCanvasTkAgg(visualization_fig, master=musicPlayer)
    visualization_canvas_widget = visualization_canvas.get_tk_widget()
    visualization_canvas_widget.pack()

    slider_label = tk.Label(musicPlayer, text="Playback Position:")
    slider_label.pack()
    global slider
    slider = tk.Scale(musicPlayer, from_=0, to=1, orient="horizontal")
    slider.set(0)
    slider.pack()


# Function to update the slider position
def update_slider_position():
    if visualization_fig:
        current_position = mixer.music.get_pos() / 1000  # Current position in seconds
        slider.set(current_position)
    root.after(100, update_slider_position)

# Function to set audio position based on slider
def set_position(event):
    position = slider.get()
    mixer.music.set_pos(position)

# TODO: turn the funge to get the first one to play into a proper selction, ie enter key doesnt work after that
song_names = []
song_paths = []


def move_selection_up(*event):
    current_index = songs_list.curselection()
    if event == 'key':
        songs_list.selection_set(current_index)
    if current_index:
        new_index = max(int(current_index[0]) - 1, 0)
        if new_index == current_index[0]:
            new_index = songs_list.size() - 1
        songs_list.selection_clear(0, tk.END)
        songs_list.selection_set(new_index)
    else:
        songs_list.selection_clear(0, tk.END)
        songs_list.selection_set(0)


def move_selection_down(*event):
    current_index = songs_list.curselection()
    if event == 'key':
        songs_list.selection_set(current_index)
    if current_index:
        new_index = min(int(current_index[0]) + 1, songs_list.size() - 1)
        if new_index == current_index[0]:
            new_index = 0
        songs_list.selection_clear(0, tk.END)
        songs_list.selection_set(new_index)
    else:
        songs_list.selection_clear(0, tk.END)
        songs_list.selection_set(0)


def add_folder():
    folder_path = filedialog.askdirectory(initialdir="Music/", title="Choose a folder")
    if folder_path == '':
        return None
    for song_file in os.listdir(folder_path):
        if song_file.endswith(".mp3"):
            song_name = os.path.splitext(os.path.basename(song_file))[0]
            song_names.append(song_name)  # Add the song name to the list
            song_paths.append(os.path.join(folder_path, song_file))  # Add the full file path to the list
            songs_list.insert(tk.END, song_name)  # Display the song name in the listbox


# add a song to the playlist
def add_songs():
    file_path = filedialog.askopenfilename(initialdir="Music/", title="Choose a song",
                                           filetypes=(("mp3 Files", "*.mp3"),))
    if file_path == '':
        return None
    song_paths.append(file_path)
    song_names.append(os.path.splitext(os.path.basename(file_path))[0])
    songs_list.insert(tk.END, song_names[-1])


def delete_song():
    curr_song = songs_list.curselection()
    songs_list.delete(curr_song[0])


def play():
    global musicPlayer
    selected_index = songs_list.curselection()
    if selected_index:
        index = selected_index[0]
    else:
        index = 0
    song_path = song_paths[index]
    mixer.music.load(song_path)
    mixer.music.play()
    songs_list.activate(index)
    if not musicPlayer:
        create_musicPlayer_window()
    elif musicPlayer:
        # refresh_musicPlayer_window(song_path)
        pass


# to stop the  song
def stop():
    global musicPlayer
    mixer.music.stop()
    songs_list.selection_clear(tk.ACTIVE)
    if musicPlayer:
        on_musicPlayer_close()


# to toggle the song for pause and resume
def toggle_play():
    if mixer.music.get_busy():
        print('Pausing')
        mixer.music.pause()
    else:
        print('Playing')
        mixer.music.unpause()


# to pause the song
def pause():
    mixer.music.pause()


# to resume the song
def resume():
    mixer.music.unpause()


# TODO: repopulate this
def space_key(*args):
    toggle_play()


def back_key(*args):
    move_selection_up()


def enter_key(*args):
    move_selection_down()


# creating the root window
root = tk.Tk()
root.title('DataFlair Music player App ')
# initialize mixer
mixer.init()

# create the listbox to contain songs
songs_list = tk.Listbox(root, selectmode=tk.SINGLE, bg="black", fg="white", font=('arial', 15), height=12, width=47,
                        selectbackground="gray", selectforeground="black")
songs_list.grid(columnspan=9)

# font is defined which is to be used for the button font
defined_font = font.Font(family='Helvetica')

# play button
play_button = tk.Button(root, text="play", width=7, command=play)
play_button['font'] = defined_font
play_button.grid(row=1, column=0)

# stop button
stop_button = tk.Button(root, text="stop", width=7, command=stop)
stop_button['font'] = defined_font
stop_button.grid(row=1, column=1)

# pause button
pause_button = tk.Button(root, text="pause", width=7, command=pause)
pause_button['font'] = defined_font
pause_button.grid(row=1, column=3)

# resume button
Resume_button = tk.Button(root, text="resume", width=7, command=resume)
Resume_button['font'] = defined_font
Resume_button.grid(row=1, column=2)

# previous_song button
previous_button = tk.Button(root, text="prev", width=7, command=move_selection_up)
previous_button['font'] = defined_font
previous_button.grid(row=1, column=4)

# next_song button
next_button = tk.Button(root, text="next", width=7, command=move_selection_down)
next_button['font'] = defined_font
next_button.grid(row=1, column=5)

# menu
my_menu = tk.Menu(root)
root.config(menu=my_menu)
add_song_menu = tk.Menu(my_menu)
my_menu.add_cascade(label="Menu", menu=add_song_menu)
add_song_menu.add_command(label="Add folder", command=add_folder)
add_song_menu.add_command(label="Add songs", command=add_songs)
add_song_menu.add_command(label="Delete song", command=delete_song)

root.bind("<space>", space_key)
root.bind("<Return>", enter_key)
root.bind("<BackSpace>", back_key)
root.bind("<Up>", move_selection_up("key"))
root.bind("<Down>", move_selection_down("key"))

tk.mainloop()
