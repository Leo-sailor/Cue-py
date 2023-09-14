# importing libraries
from pygame import mixer
import tkinter as tk
import tkinter.font as font
from tkinter import filedialog
import os
import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment
import tempfile
import io
from PIL import Image, ImageTk
import time
from matplotlib.colors import LinearSegmentedColormap


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
        self.musicPlayer.geometry("804x259")
        self.musicPlayer.resizable(width=False, height=False)

    def on_musicPlayer_close(self):
        self.musicPlayer.destroy()
        self.__init__()

    def load_saved_plot(self, file_path):
        # Open the saved PNG file in binary read mode
        print(f'loading saved image: {file_path}')
        with open(file_path, 'rb') as saved_file:
            # Read the file content into a buffer
            buffer = io.BytesIO(saved_file.read())

        # Use PIL to open the image from the buffer
        saved_image = Image.open(buffer)

        # Convert the PIL image to a Tkinter PhotoImage
        saved_photo = ImageTk.PhotoImage(saved_image)
        # Create a Label widget to display the image
        if self.visualization_canvas is not None:
            self.visualization_canvas.get_tk_widget().destroy()
        self.visualization_canvas = tk.Label(self.musicPlayer, image=saved_photo)
        self.visualization_canvas.image = saved_photo
        self.visualization_canvas.place(x=0, y=0)

    def visualize_audio(self, file_path):
        self.audio = song_dict[file_path][1]

        def update_visualization():
            self.load_saved_plot(song_dict[file_path][0])

        update_visualization()

        # Create a slider to control the playback position
        slider_label = tk.Label(self.musicPlayer, text="Playback Position:", anchor="center")

        slider_label.place(y=202, x=350)

        self.slider = tk.Scale(self.musicPlayer, from_=0, to=self.audio.duration_seconds, orient="horizontal",
                               resolution=1, length=655)
        self.slider.set(0)
        self.slider.place(x=75, y=220)

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
song_dict = {}
music_player = MusicPlayer()


def plotData(file_path):
    try:
        audio = AudioSegment.from_mp3(file_path)
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return

    samples = np.array(audio.get_array_of_samples())
    duration_seconds = audio.duration_seconds
    num_segments = round(duration_seconds)

    # Create a custom colormap with your list of colors
    colors = ["red", "green"]  # Add more colors as needed
    cmap = LinearSegmentedColormap.from_list("custom", colors, N=num_segments)

    def update_visualization():
        fig, ax = plt.subplots(figsize=(8, 2))
        x_values = np.linspace(0, duration_seconds, num=round(len(samples) / 20))
        segment_length = round(len(samples) / 20) // num_segments

        for i in range(num_segments):
            start_idx = i * segment_length
            end_idx = (i + 1) * segment_length
            segment_samples = samples[start_idx:end_idx]
            segment_x = x_values[start_idx:end_idx]

            color = cmap(i / (num_segments - 1))  # Interpolate color based on the segment index
            ax.plot(segment_x, segment_samples, color=color)

        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude')
        ax.set_xlim(0, duration_seconds)
        ax.set_ylim(np.min(samples), np.max(samples))

        # Add light vertical lines every 5 seconds
        interval_seconds = 5
        for i in range(0, int(duration_seconds) + 1, interval_seconds):
            ax.vlines(i, np.min(samples), (np.min(samples) * .9), color='darkgray', linestyle='--')

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')  # You can choose a different format if needed

        # Seek to the beginning of the buffer
        buffer.seek(0)
        return buffer

    return update_visualization()


def save_data_to_tempfile(song_path, buffer):
    # Create a temporary directory if it doesn't exist
    temp_dir = tempfile.mkdtemp()

    # Create a unique file name based on the song_path
    audio = AudioSegment.from_mp3(song_path)
    _, file_extension = os.path.splitext(song_path)
    song_path = song_path.replace(".mp3", "")
    temp_file_name = os.path.join(temp_dir, f"tempfile_{os.path.basename(song_path)}.png")

    # Save data to the temporary file
    with open(temp_file_name, 'wb') as temp_file:
        temp_file.write(buffer.getvalue())
    buffer.close()
    return temp_file_name, audio


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


def toggle_loading(started, ammElems):
    if started:
        songs_list.delete(0, tk.END)
        songs_list.insert(tk.END, "Loading...")
        songs_list.insert(tk.END, '')
        songs_list.insert(tk.END, f'(Should be done in roughly {round(ammElems * 1.7, 2)} seconds.)')
        mixer.music.pause()
        songs_list.master.update()
    else:
        songs_list.delete(0, tk.END)
        for name in song_names:
            songs_list.insert(tk.END, name)
        mixer.music.unpause()


def add_folder():
    folder_path = filedialog.askdirectory(initialdir="Music/", title="Choose a folder")
    if folder_path == '':
        return None
    toggle_loading(True, len(os.listdir(folder_path)))
    how_long = 0
    num_cycles = 0
    for song_file in os.listdir(folder_path):
        print(f'song_file {song_file}')
        if song_file.endswith(".mp3"):
            t0 = time.time()
            song_name = os.path.splitext(os.path.basename(song_file))[0]
            song_names.append(song_name)  # Add the song name to the list
            song_path = os.path.join(folder_path, song_file)
            song_paths.append(song_path)  # Add the full file path to the list
            buffer = plotData(song_path)
            location, saved_audio = save_data_to_tempfile(song_path, buffer)
            song_dict[song_path] = [location, saved_audio]
            t1 = time.time()
            how_long += (t1 - t0)
            num_cycles += 1
            songs_list.delete(2)
            songs_list.delete(2)
            average_length = (how_long / num_cycles) * len(os.listdir(folder_path))
            songs_list.insert(2, f'Done in {round(average_length - how_long, 1)} seconds.')
            songs_list.insert(3, f'Average time per song of {round(how_long / num_cycles, 2)} seconds.')
            root.update()
    print(f'Took {round(how_long, 2)} seconds to complete, with an average of '
          f'{round((how_long / len(os.listdir(folder_path))), 2)} seconds per song.')
    toggle_loading(False, 1)


# add a song to the playlist
def add_songs():
    file_path = filedialog.askopenfilename(initialdir="Music/", title="Choose a song",
                                           filetypes=(("mp3 Files", "*.mp3"),))
    if file_path == '':
        return None
    toggle_loading(True, 1)
    how_long = 0
    t0 = time.time()
    song_paths.append(file_path)
    song_names.append(os.path.splitext(os.path.basename(file_path))[0])
    songs_list.insert(tk.END, song_names[-1])
    print('plotting')
    buffer = plotData(file_path)
    print('saving')
    location, saved_audio = save_data_to_tempfile(file_path, buffer)
    song_dict[file_path] = [location, saved_audio]
    t1 = time.time()
    how_long += (t1 - t0)
    print(f'Took {round(how_long, 2)} seconds to complete.')
    toggle_loading(False, 1)


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
    t0 = time.time()
    if music_player.musicPlayer is None:
        music_player.create_musicPlayer_window(song_path)
    elif music_player.musicPlayer is not None:
        root.after_cancel(music_player.slider_update_id)
        music_player.on_musicPlayer_close()
        music_player.create_musicPlayer_window(song_path)
    t1 = time.time()
    print("Time elapsed: ", t1 - t0)


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
    music_player.slider_update_pending = True


# to resume the song
def resume():
    mixer.music.unpause()
    music_player.slider_update_pending = False
    root.after_cancel(music_player.slider_update_id)
    music_player.update_slider_position()


def space_key(*args):
    toggle_play()


def back_key(*args):
    move_selection_up()


def enter_key(*args):
    move_selection_down()

def add_to_queue():
    pass

def remove_from_queue():
    pass

# creating the root window
root = tk.Tk()
root.title('DataFlair Music player App ')
# initialize mixer
mixer.init()

# create the listbox to contain songs
songs_list = tk.Listbox(root, selectmode=tk.SINGLE, bg="black", fg="white", font=('arial', 15), height=12, width=47,
                        selectbackground="gray", selectforeground="black")
songs_list.grid(columnspan=9, sticky="w")

queue_list = tk.Listbox(root, selectmode=tk.DISABLED, bg="black", fg="white", font=('arial', 15), height=12, width=28,
                        selectbackground="gray", selectforeground="black")
queue_list.insert(0, 'Currently playing:')
queue_list.insert(1, '')
queue_list.insert(2, '')
queue_list.insert(3, 'Next:')
queue_list.grid(columnspan=2, column=6, row=0)

# font is defined which is to be used for the button font
defined_font = font.Font(family='Helvetica')

# play button
play_button = tk.Button(root, text="play", width=7, command=play)
play_button['font'] = defined_font
play_button.grid(row=10, column=0)

# stop button
stop_button = tk.Button(root, text="stop", width=7, command=stop)
stop_button['font'] = defined_font
stop_button.grid(row=10, column=1)

# pause button
pause_button = tk.Button(root, text="pause", width=7, command=pause)
pause_button['font'] = defined_font
pause_button.grid(row=10, column=3)

# resume button
Resume_button = tk.Button(root, text="resume", width=7, command=resume)
Resume_button['font'] = defined_font
Resume_button.grid(row=10, column=2)

# previous_song button
previous_button = tk.Button(root, text="prev", width=7, command=move_selection_up)
previous_button['font'] = defined_font
previous_button.grid(row=10, column=4)

# next_song button
next_button = tk.Button(root, text="next", width=7, command=move_selection_down)
next_button['font'] = defined_font
next_button.grid(row=10, column=5)

# add_to_queue button
add_to_queue_button = tk.Button(root, text="add to queue", width=11, command=add_to_queue)
add_to_queue_button['font'] = defined_font
add_to_queue_button.grid(row=10, column=6, sticky='w')

# remove_from_queue button
add_to_queue_button = tk.Button(root, text="remove from queue", width=16, command=remove_from_queue)
add_to_queue_button['font'] = defined_font
add_to_queue_button.grid(row=10, column=7)


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
