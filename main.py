import imagej
import numpy as np
import scyjava
import os
from tkinter import Tk, filedialog

scyjava.config.add_options('-Xmx6g')
ij = imagej.init('sc.fiji:fiji', mode='interactive')


class ImageSet:
    def __init__(self, image_path, image_id):
        self.channel0 = image_path + '/' + image_id + '_ch00_SV.tif'
        self.channel1 = image_path + '/' + image_id + '_ch01_SV.tif'
        self.channel2 = image_path + '/' + image_id + '_ch02_SV.tif'
        self.channel3 = image_path + '/' + image_id + '_ch03_SV.tif'
        self.channel4 = image_path + '/' + image_id + '_ch04_SV.tif'
        self.overlay = image_path + '/' + image_id + '_overlay.tif'

    def check_files(self):
        files = [self.channel0, self.channel1, self.channel2, self.channel3, self.channel4, self.overlay]
        for file in files:
            if not os.path.isfile(file):
                return False
        return True


# Function to open a directory selection dialog
def select_directory(initial_dir=os.getcwd()):
    root = Tk()
    root.withdraw()  # Hide the root window
    root.attributes("-topmost", True)  # Bring the dialog to the front
    directory = filedialog.askdirectory(initialdir=initial_dir)
    root.destroy()  # Destroy the root window after selection
    return directory


def get_file_list(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


def get_files(path_input):
    image_files = get_file_list(path_input)
    files = []

    for file in image_files:
        base_name = os.path.basename(file)
        parts = base_name.split('_')
        image_id = parts[0]
        if 'overlay' in base_name:
            image_set = ImageSet(path_input, image_id)
            files.append(image_set)

    return files


def open_image(image_path):
    try:
        image = ij.io().open(image_path)
        return image
    except Exception as e:
        print(f"Error opening image: {e}")
        return None


def process_islet_image(image_set: ImageSet):
    lower_thresholds = [10, 10, 10, 10]
    upper_thresholds = [255, 255, 255, 255]
    sd_multipliers = [3, 3, 3, 3]

    # Open each channel image
    try:
        overlay = open_image(image_set.overlay)
        ij.py.show(overlay)
        print('here')


    except Exception as e:
        print(f"Error in opening image files: {e}")
        return {}


def main():
    path_input = select_directory()
    files = get_files(path_input)
    process_islet_image(files[0])







if __name__ == "__main__":
    main()
