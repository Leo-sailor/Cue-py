# importing libraries
from pygame import mixer
import tkinter as tk
import tkinter.font as font
from tkinter import filedialog
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from pydub import AudioSegment


class MusicPlayer:
    def __init__(self):
        self.just_paused = False
        self.slider_update_id = None
        self.playback_position = 0
        self.counter = 0
        self.slider_update_pending = False
        self.musicPlayer = None
        self.visualization_fig = None
        self.visualization_canvas = None
        self.slider = None
        self.audio = None  # Store the loaded audio

    def create_musicPlayer_window(self, input_song):
        self.musicPlayer = tk.Toplevel()
        self.musicPlayer.title('Song Controller')
        self.musicPlayer.protocol("WM_DELETE_WINDOW", self.on_musicPlayer_close)
        self.visualize_audio(input_song)

    def on_musicPlayer_close(self):
        self.musicPlayer.destroy()
        self.__init__()

    def visualize_audio(self, file_path):
        try:
            print(file_path)
            self.audio = AudioSegment.from_mp3(file_path)
        except Exception as e:
            print(f"Error loading audio file: {e}")
            return

        samples = np.array(self.audio.get_array_of_samples())
        duration_seconds = self.audio.duration_seconds

        # Create a placeholder for the visualization
        self.visualization_canvas = None

        def update_visualization():
            nonlocal self
            if self.visualization_canvas is None:
                self.visualization_fig, ax = plt.subplots(figsize=(8, 2))
                ax.plot(np.linspace(0, duration_seconds, num=len(samples)), samples)
                ax.set_xlabel('Time (s)')
                ax.set_ylabel('Amplitude')
                ax.set_xlim(0, duration_seconds)  # Set x-axis limits to the duration of the song
                ax.set_ylim(np.min(samples), np.max(samples))  # Set y-axis limits to min and max amplitudes
                self.visualization_canvas = FigureCanvasTkAgg(self.visualization_fig, master=self.musicPlayer)
                visualization_canvas_widget = self.visualization_canvas.get_tk_widget()
                visualization_canvas_widget.pack()
                self.musicPlayer.update_idletasks()  # Force GUI update

        # Call the update_visualization function when needed (e.g., when the window is created)
        update_visualization()

        # Create a slider to control the playback position
        slider_label = tk.Label(self.musicPlayer, text="Playback Position:")

        slider_label.pack()

        self.slider = tk.Scale(self.musicPlayer, from_=0, to=self.audio.duration_seconds, orient="horizontal",
                               resolution=1, length=650)
        self.slider.set(0)
        self.slider.pack(side='bottom')
        self.musicPlayer.update_idletasks()

        self.slider.bind("<Button-1>", lambda event: setattr(self, 'slider_update_pending', True))

        # Bind the slider to a callback for ButtonRelease-1 event (slider release)
        self.slider.bind("<ButtonRelease-1>", self.slider_released)

        # Start periodic slider updates
        self.update_slider_position()

    def slider_released(self, event):
        # This function is called when the slider is released by the user
        self.update_audio_position(self.slider.get())
        self.slider_update_pending = False  # Reset the flag
        self.counter = 0
        root.after_cancel(self.slider_update_id)
        self.update_slider_position()

    def update_slider_position(self):
        # Update the slider position to reflect the current playback position
        if not self.slider_update_pending:
            self.counter += 1
            current_position = self.playback_position + self.counter
            if current_position == round(self.audio.duration_seconds):
                self.back_track_music()
            self.slider.set(current_position)
            self.slider_update_id = root.after(1000, self.update_slider_position)

    def update_audio_position(self, position):
        print(position)
        # Ensure there's an active audio playback
        if self.audio is not None:
            # Calculate the desired position in seconds based on the slider value
            self.playback_position = float(position)

            if self.playback_position == round(self.audio.duration_seconds):
                self.back_track_music()
                return

            if self.just_paused:
                mixer.music.unpause()
                self.just_paused = False
            # set mixer to the desired position
            mixer.music.set_pos(self.playback_position)

    def back_track_music(self):
        self.just_paused = True
        mixer.music.rewind()
        mixer.music.pause()
        root.after_cancel(self.slider_update_id)


song_names = []
song_paths = []
music_player = MusicPlayer()


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
    """
    Move the selection of the songs_list widget down by one index.

    Args:
        *event: Variable length argument list of events.

    Returns:
        None
    """
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
    selected_index = songs_list.curselection()
    if selected_index:
        index = selected_index[0]
    else:
        index = 0
    song_path = song_paths[index]
    mixer.music.load(song_path)
    mixer.music.play()
    songs_list.activate(index)
    if music_player.musicPlayer is None:
        music_player.create_musicPlayer_window(song_path)
    elif music_player.musicPlayer is not None:
        # refresh_musicPlayer_window(song_path)
        pass


# to stop the  song
def stop():
    mixer.music.stop()
    songs_list.selection_clear(tk.ACTIVE)
    if music_player.musicPlayer is not None:
        music_player.on_musicPlayer_close()


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
