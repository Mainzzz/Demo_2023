import os

def batch_replace_word_in_filenames(folder_path, old_word, new_word):
    for filename in os.listdir(folder_path):
        if old_word in filename:
            new_filename = filename.replace(old_word, new_word)
            old_file_path = os.path.join(folder_path, filename)
            new_file_path = os.path.join(folder_path, new_filename)
            os.rename(old_file_path, new_file_path)
            print(f'Renamed: {filename} -> {new_filename}')

if __name__ == "__main__":
    folder_path = "C:\AIRBUS_F1\TASK\A350\CTP_A3850_PERF_PROCESS_DECEL_TIMESEG"  # Current folder
    old_word = "A3580"
    new_word = "A3850"
    
    batch_replace_word_in_filenames(folder_path, old_word, new_word)
