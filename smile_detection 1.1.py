import cv2
import dlib
import os

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

# Input video file and variable for the output image filenames
input_video_file = 'input_video.MOV'
output_image_prefix = os.path.splitext(os.path.basename(input_video_file))[0]

# Open the video file
cap = cv2.VideoCapture(input_video_file)

# Calculate frame interval based on the total length of the video divided by 5
frame_interval = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / 5)

frame_number = 0  # Track the frame number
smile_count = 0  # Count of exported smile face images

# Get the creation date and modified date of the input video
creation_date = os.path.getctime(input_video_file)
modified_date = os.path.getmtime(input_video_file)

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
                # Save the frame when a smiling face is detected with the input file variable name as a prefix
                filename = f'{output_image_prefix}_smiling_face_{frame_number // frame_interval}.jpg'
                cv2.imwrite(filename, frame)
                smile_count += 1

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()

# Get a list of image files in the current directory
image_files = [f for f in os.listdir() if f.endswith('.jpg')]

# Check if smile_count is less than or equal to 1
if smile_count <= 1:
    cap = cv2.VideoCapture(input_video_file)  # Reopen the video file

    frame_number = 0  # Reset frame number for regular face export

    while True:
        ret, frame = cap.read()
        frame_number += 1

        if not ret:
            break

        if frame_number % frame_interval == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                # Save the frame when a regular face is detected with the same naming system as smiling face
                filename = f'{output_image_prefix}_face_{frame_number // frame_interval}.jpg'
                cv2.imwrite(filename, frame)

    # Release the video capture
    cap.release()

# Modify the metadata (creation_date, modified_date) of the images to match the input video
for image_file in image_files:
    os.utime(image_file, (creation_date, modified_date))

print(f"Exported {smile_count} smile face images and {frame_number // frame_interval} regular face images.")
