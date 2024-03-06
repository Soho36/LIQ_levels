import subprocess


def open_file(filename):
    # Use the 'start' command to open the file with the default application
    subprocess.run(['start', filename], shell=True)

# Define the filename of the JPEG image
filename = '2020-09-01_18-16-03.png'  # Replace 'example.jpg' with the actual filename

# Open the file
open_file(filename)
