import tempfile, os, time


def save_data_to_tempfile(song_path, data):
    # Create a temporary directory if it doesn't exist
    temp_dir = tempfile.mkdtemp()

    # Create a unique file name based on the song_path
    _, file_extension = os.path.splitext(song_path)
    print(file_extension)
    song_path = song_path.replace(file_extension, '')
    print(song_path)
    temp_file_name = os.path.join(temp_dir, f"tempfile_{os.path.basename(song_path)}{file_extension}")

    # Save data to the temporary file
    with open(temp_file_name, 'wb') as temp_file:
        temp_file.write(data)

    return temp_file_name


# Example usage:
song_path = "C:/Users/stirl/iCloudDrive/Downloads/songs/Calm.mp3"
data_to_save = b"This is your data to save in the temporary file."

# Save data to a temporary file with a name based on the song_path
temp_file_path = save_data_to_tempfile(song_path, data_to_save)

# You can now use temp_file_path as needed
print(f"Temporary file path: {temp_file_path}")

time.sleep(10)


