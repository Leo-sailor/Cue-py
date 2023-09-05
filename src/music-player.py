# importing libraries
from pygame import mixer
import tkinter as tk
import tkinter.font as font
from tkinter import filedialog
import os
# TODO: turn the funge to get the first one to play into a proper selction, ie enter key doesnt work after that
song_names = []
song_paths = []

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
    file_path = filedialog.askopenfilenames(initialdir="Music/", title="Choose a song", filetypes=(("mp3 Files", "*.mp3"),))
    if file_path == '':
        return None
    song_paths.append(file_path[0])
    song_names.append(os.path.splitext(os.path.basename(file_path[0]))[0])
    songs_list.insert(tk.END, *song_names[-len(song_paths):])

def delete_song():
    curr_song = songs_list.curselection()
    songs_list.delete(curr_song[0])

def play():
    selected_index = songs_list.curselection()
    if selected_index:
        index = selected_index[0]
    else:
        index = 0
    song_path = song_paths[index]
    mixer.music.load(song_path)
    mixer.music.play()
    songs_list.activate(index)

# to stop the  song
def stop():
    mixer.music.stop()
    songs_list.selection_clear(tk.ACTIVE)


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


# function to navigate from the current song
def previous_song():
    selected_index = songs_list.curselection()
    if selected_index:
        index = selected_index[0]
        if index > 0:
            songs_list.selection_clear(0, tk.END)
            songs_list.selection_set(index - 1)

def next_song():
    selected_index = songs_list.curselection()
    if selected_index:
        index = selected_index[0]
        if index < len(song_names) - 1:
            songs_list.selection_clear(0, tk.END)
            songs_list.selection_set(index + 1)
    else:
        songs_list.selection_clear(0, tk.END)
        songs_list.selection_set(0)

# TODO: repopulate this
def space_key(*args):
    pass

def back_key(*args):
    pass

def enter_key(*args):
    pass

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
previous_button = tk.Button(root, text="prev", width=7, command=previous_song)
previous_button['font'] = defined_font
previous_button.grid(row=1, column=4)

# next_song button
next_button = tk.Button(root, text="next", width=7, command=next_song)
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

tk.mainloop()
