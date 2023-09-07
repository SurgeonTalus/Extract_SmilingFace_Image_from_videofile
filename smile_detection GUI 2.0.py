import cv2
import os
import tkinter as tk
from tkinter import filedialog
import numpy as np
import subprocess  # Added import for subprocess

# Function to check video dimensions
def is_invalid_video_dimensions(video_path):
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    return (width == 1440 and height == 1920) or (width == 1920 and height == 1440)

# Load the pre-trained face and smile detectors
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

# Function to detect smiles
def detect_smile(gray):
    smiles = smile_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=6,
        minSize=(100, 100),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    for (sx, sy, sw, sh) in smiles:
        return True

    return False

# Function to check if two images are equal
def are_images_equal(image1, image2):
    return np.array_equal(image1, image2)

# Function to embed metadata from video to photo
def embed_metadata(video_path, photo_path):
    try:
        # Use exiftool to copy metadata from video to photo
        subprocess.run(["exiftool", "-overwrite_original", "-TagsFromFile", video_path, photo_path])
        print("Metadata embedded successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

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
skipped_videos = 0
created_images = 0

# Count the total number of files
total_files = len(video_files)

for input_video_file in video_files:
    # Get the filename without the file extension
    base_filename = os.path.splitext(input_video_file)[0]

    # Check if the length of the base filename is less than 9 characters, use that as the limit
    first_9_characters = base_filename[:min(9, len(base_filename))]

    # Check if the first 9 characters match the start of a file in the export folder
    matching_existing_file = next((filename for filename in existing_filenames if filename.startswith(first_9_characters)), None)

    if matching_existing_file:
        print(f"Skipping {input_video_file} as it matches {matching_existing_file}.")
        skipped_videos += 1
        continue

    input_video_path = os.path.join(folder_selected, input_video_file)

    # Check video dimensions and skip if invalid
    if is_invalid_video_dimensions(input_video_path):
        print(f"Skipping {input_video_file} due to invalid dimensions.")
        skipped_videos += 1
        continue

    # Print the results
    print(f"Processing: {input_video_file} {processed_videos} of {total_files}")
    print(f"Skipped files: {skipped_videos}")
    print(f"Created images: {created_images}")

    # Open the video file
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
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

            for (x, y, w, h) in faces:
                # Detect smiles in the face region
                is_smiling = detect_smile(gray[y:y+h, x:x+w])

                if is_smiling:
                    smile_detected = True
                    # Calculate the timestamp in seconds
                    timestamp_seconds = int(frame_number / cap.get(cv2.CAP_PROP_FPS))

                    # Generate a unique filename
                    filename = generate_unique_filename(f'{base_filename}_{timestamp_seconds}s', existing_filenames)

                    output_path = os.path.join(exported_images_folder, filename + '.jpg')

                    # Check if the current frame is the same as the previous frame
                    if previous_frame is None or not are_images_equal(frame, previous_frame):
                        cv2.imwrite(output_path, frame)

                        # Embed metadata if a smile is detected
                        metadata_embedded = False
                        if smile_detected:
                            try:
                                embed_metadata(input_video_path, output_path)
                                metadata_embedded = True
                            except Exception as e:
                                print(f"An error occurred while embedding metadata: {str(e)}")

                        # Modify the creation date and modified date of the image file
                        os.utime(output_path, (creation_date, modified_date))
                        existing_filenames.add(filename)
                        created_images += 1

                    previous_frame = frame.copy()  # Store the current frame
                    break  # Break out of the loop if a smile is detected

    # Release the video capture
    cap.release()

    if not smile_detected:
        # If no smiles were detected in the entire video, save frames with regular faces
        frame_interval_regular = max(total_frames // 5, 60)  # Ensure regular face frames are saved every 40 frames or at frame_interval
        cap = cv2.VideoCapture(input_video_path)
        frame_number = 0

        while True:
            ret, frame = cap.read()
            frame_number += 1

            if not ret:
                break

            if frame_number % frame_interval_regular == 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

                for (x, y, w, h) in faces:
                    # Calculate the timestamp in seconds
                    timestamp_seconds = int(frame_number / cap.get(cv2.CAP_PROP_FPS))

                    # Generate a unique filename
                    filename = generate_unique_filename(f'{base_filename}_{timestamp_seconds}s', existing_filenames)

                    output_path = os.path.join(exported_images_folder, filename + '_f.jpg')

                    # Check if the current frame is the same as the previous frame
                    if previous_frame is None or not are_images_equal(frame, previous_frame):
                        cv2.imwrite(output_path, frame)

                        # Embed metadata if a smile is detected
                        metadata_embedded = False
                        try:
                            embed_metadata(input_video_path, output_path)
                            metadata_embedded = True
                        except Exception as e:
                            print(f"An error occurred while embedding metadata: {str(e)}")

                        # Modify the creation date and modified date of the image file
                        os.utime(output_path, (creation_date, modified_date))
                        existing_filenames.add(filename)
                        created_images += 1

                    previous_frame = frame.copy()  # Store the current frame

        # Release the video capture
        cap.release()

    processed_videos += 1
