import cv2
import dlib
import os
import tkinter as tk
from tkinter import filedialog
import numpy as np

# Load the pre-trained face and smile detectors
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

# Function to detect smiles
def detect_smile(gray):
    smiles = smile_cascade.detectMultiScale(
        gray,
        scaleFactor=1.5,
        minNeighbors=20,
        minSize=(25, 25),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    for (sx, sy, sw, sh) in smiles:
        return True

    return False

# Function to check if two images are equal
def are_images_equal(image1, image2):
    return np.array_equal(image1, image2)

# Create a GUI window to select the folder
root = tk.Tk()
root.withdraw()  # Hide the main window
folder_selected = filedialog.askdirectory(initialdir=os.path.expanduser("~"), title="Select Input Folder")

# Check if a folder was selected
if not folder_selected:
    print("No folder selected. Exiting.")
    exit()

# Create the "exported_images" subfolder with a prefix
folder_name = os.path.basename(folder_selected)
exported_images_folder = os.path.join(folder_selected, f"{folder_name}_exported_images")
os.makedirs(exported_images_folder, exist_ok=True)

# Function to generate a unique filename
def generate_unique_filename(base_filename, existing_filenames):
    if base_filename not in existing_filenames:
        return base_filename
    else:
        count = 1
        while f"{base_filename}_{count}" in existing_filenames:
            count += 1
        return f"{base_filename}_{count}"

# Create a list of existing filenames in the exported_images folder
existing_filenames = set(os.listdir(exported_images_folder))

# Iterate through video files in the selected folder
video_files = [f for f in os.listdir(folder_selected) if f.lower().endswith(('.mp4', '.mov', '.avi'))]

# Variable to keep track of the number of processed videos
processed_videos = 0

for input_video_file in video_files:
    # Open the video file
    input_video_path = os.path.join(folder_selected, input_video_file)
    cap = cv2.VideoCapture(input_video_path)

    # Calculate frame interval based on the total length of the video divided by 5
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = max(total_frames // 5, 30)  # Set frame_interval to the current calculation or at least 30 frames

    frame_number = 0  # Track the frame number
    smile_detected = False

    # Get the creation date and modified date of the input video
    creation_date = os.path.getctime(input_video_path)
    modified_date = os.path.getmtime(input_video_path)

    previous_frame = None  # Store the previous frame

    while True:
        ret, frame = cap.read()
        frame_number += 1

        if not ret:
            break

        if frame_number % frame_interval == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                # Detect smiles in the face region
                is_smiling = detect_smile(gray[y:y+h, x:x+w])

                if is_smiling:
                    smile_detected = True
                    # Calculate the timestamp in seconds
                    timestamp_seconds = int(frame_number / cap.get(cv2.CAP_PROP_FPS))
                    
                    # Generate the base filename based on timestamp
                    base_filename = f'{os.path.splitext(input_video_file)[0]}_{timestamp_seconds}s'
                    
                    # Generate a unique filename
                    filename = generate_unique_filename(base_filename, existing_filenames)
                    
                    output_path = os.path.join(exported_images_folder, filename + '.jpg')
                    
                    # Check if the current frame is the same as the previous frame
                    if previous_frame is None or not are_images_equal(frame, previous_frame):
                        cv2.imwrite(output_path, frame)
                        # Modify the creation date and modified date of the image file
                        os.utime(output_path, (creation_date, modified_date))
                        existing_filenames.add(filename)
                    
                    previous_frame = frame.copy()  # Store the current frame
                    break  # Break out of the loop if a smile is detected

    # Release the video capture
    cap.release()

    if not smile_detected:
        # If no smiles were detected in the entire video, save frames with regular faces
        frame_interval_regular = max(total_frames // 5, 30)  # Ensure regular face frames are saved every 40 frames or at frame_interval
        cap = cv2.VideoCapture(input_video_path)
        frame_number = 0

        while True:
            ret, frame = cap.read()
            frame_number += 1

            if not ret:
                break

            if frame_number % frame_interval_regular == 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

                for (x, y, w, h) in faces:
                    # Calculate the timestamp in seconds
                    timestamp_seconds = int(frame_number / cap.get(cv2.CAP_PROP_FPS))
                    
                    # Generate the base filename based on timestamp
                    base_filename = f'{os.path.splitext(input_video_file)[0]}_{timestamp_seconds}s'
                    
                    # Generate a unique filename
                    filename = generate_unique_filename(base_filename, existing_filenames)
                    
                    output_path = os.path.join(exported_images_folder, filename + '_f.jpg')
                    
                    # Check if the current frame is the same as the previous frame
                    if previous_frame is None or not are_images_equal(frame, previous_frame):
                        cv2.imwrite(output_path, frame)
                        # Modify the creation date and modified date of the image file
                        os.utime(output_path, (creation_date, modified_date))
                        existing_filenames.add(filename)
                    
                    previous_frame = frame.copy()  # Store the current frame

        # Release the video capture
        cap.release()

    print(f"Exported {smile_detected} smiling face images from {input_video_file}")
    processed_videos += 1

# Close all windows
cv2.destroyAllWindows()

print(f"Processing complete for {processed_videos} videos.")
