# importing libraries
from pygame import mixer
from tkinter import *
import tkinter.font as font
from tkinter import filedialog
import os


def add_folder():
    folder_path = filedialog.askdirectory(initialdir="Music/", title="Choose a folder")
    for song_file in os.listdir(folder_path):
        if song_file.endswith(".mp3"):
            song_name = os.path.splitext(os.path.basename(song_file))[0]
            songs_list.insert(END, song_name)


# add a song to the playlist
def add_songs():
    # a song is returned
    s = filedialog.askopenfilenames(initialdir="Music/", title="Choose a song", filetypes=(("mp3 Files", "*.mp3"),))
    s = os.path.splitext(os.path.basename(s))[0]
    songs_list.insert(END, s)


def delete_song():
    curr_song = songs_list.curselection()
    songs_list.delete(curr_song[0])


def play():
    song = songs_list.get(ACTIVE)
    mixer.music.load(song)
    mixer.music.play()


# to stop the  song
def stop():
    mixer.music.stop()
    songs_list.selection_clear(ACTIVE)


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
    # to get the selected song index
    previous_one = songs_list.curselection()
    # to get the previous_song song index
    previous_one = previous_one[0] - 1
    # to get the previous_song song
    temp2 = songs_list.get(previous_one)
    temp2 = f'C:/Users/lenovo/Desktop/DataFlair/Notepad/Music/{temp2}'
    mixer.music.load(temp2)
    mixer.music.play()
    songs_list.selection_clear(0, END)
    # activate new song
    songs_list.activate(previous_one)
    # set the next_song song
    songs_list.selection_set(previous_one)


def next_song():
    # to get the selected song index
    next_one = songs_list.curselection()
    # to get the next_song song index
    next_one = next_one[0] + 1
    # to get the next_song song
    temp = songs_list.get(next_one)
    temp = f'C:/Users/lenovo/Desktop/DataFlair/Notepad/Music/{temp}'
    mixer.music.load(temp)
    mixer.music.play()
    songs_list.selection_clear(0, END)
    # activate new song
    songs_list.activate(next_one)
    # set the next_song song
    songs_list.selection_set(next_one)


# creating the root window
root = Tk()
root.title('DataFlair Music player App ')
# initialize mixer
mixer.init()

# create the listbox to contain songs
songs_list = Listbox(root, selectmode=SINGLE, bg="black", fg="white", font=('arial', 15), height=12, width=47,
                     selectbackground="gray", selectforeground="black")
songs_list.grid(columnspan=9)

# font is defined which is to be used for the button font
defined_font = font.Font(family='Helvetica')

# play button
play_button = Button(root, text="play", width=7, command=play)
play_button['font'] = defined_font
play_button.grid(row=1, column=0)

# stop button
stop_button = Button(root, text="stop", width=7, command=stop)
stop_button['font'] = defined_font
stop_button.grid(row=1, column=1)

# pause button
pause_button = Button(root, text="pause", width=7, command=pause)
pause_button['font'] = defined_font
pause_button.grid(row=1, column=3)

# resume button
Resume_button = Button(root, text="resume", width=7, command=resume)
Resume_button['font'] = defined_font
Resume_button.grid(row=1, column=2)

# previous_song button
previous_button = Button(root, text="Prev", width=7, command=previous_song)
previous_button['font'] = defined_font
previous_button.grid(row=1, column=4)

# next_song button
next_button = Button(root, text="next_song", width=7, command=next_song)
next_button['font'] = defined_font
next_button.grid(row=1, column=5)

# menu
my_menu = Menu(root)
root.config(menu=my_menu)
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Menu", menu=add_song_menu)
add_song_menu.add_command(label="Add folder", command=add_folder)
add_song_menu.add_command(label="Add songs", command=add_songs)
add_song_menu.add_command(label="Delete song", command=delete_song)

root.bind("<space>", lambda event: toggle_play())
root.bind("<Return>", lambda event: next_song())
root.bind("<BackSpace>", lambda event: previous_song())

mainloop()
