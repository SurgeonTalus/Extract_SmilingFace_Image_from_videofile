<!DOCTYPE html>
<html>
<head>
</head>
<body>

<h1>Extract_SmilingFace_Image_from_videofile</h1>

<p>If there is a smiling face in a video, it will extract the image and save it as a video file.</p>

<p>Download all the files to the same directory.</p>

<h2>RUN:</h2>

<pre><code>pip install opencv-python-headless
pip install dlib
pip install numpy
pip install ffmpeg-python
</code></pre>

<p>Download and extract this file to the same directory/folder as the other files in this repo:</p>
<p><a href="http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2">shape_predictor_68_face_landmarks.dat</a></p>

These two files are added in the repo but can also be found at their original place here:
https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_smile.xml
https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml


</body>
</html>

# Smile Detector GUI Program

This is a Python GUI program for processing video files to detect smiles and save frames with smiles or regular faces as images. The program utilizes OpenCV for face and smile detection, as well as `exiftool` for embedding metadata from the source video to the generated images. Below, you will find information on how to use the program, its dependencies, functionality, and what sets it apart from other programs.

## Dependencies

To use this program on your Mac, you will need to have the following dependencies installed:

1. **Python**: You can download Python from [python.org](https://www.python.org/downloads/).

2. **OpenCV**: Install OpenCV for Python using `pip` with the following command:


3. **exiftool**: You need to install the ExifTool command-line utility. You can download and install it from [ExifTool website](https://exiftool.org/).

4. **tkinter**: The `tkinter` library is included with Python, so no additional installation is required.

## Functionality

This program processes video files to detect smiles and save frames as images with the following steps:

1. Select a folder containing video files.

2. The program checks the video dimensions and skips videos with dimensions 1440x1920 or 1920x1440 as they are considered invalid.

3. For each valid video file in the selected folder:
- It opens the video file.
- Detects smiles in the video frames using a pre-trained face and smile cascade classifier from OpenCV.
- Saves frames with detected smiles as images in a subfolder named "exported_images."
- Embeds metadata (location data, creation date and modified date) from the source video to the generated images using `exiftool`.
- If no smile is detected it detects faces, and will mark the file with an f in the end.

4. If no smiles are detected in the entire video, frames with regular faces are saved as separate images.

## Program Description

This program simplifies the process of extracting frames with smiles from videos while preserving their metadata. Here are some key points that set it apart:

- **Automatic Smile Detection**: The program automatically detects smiles in video frames using OpenCV, making it convenient for users to extract joyful moments.

- **Metadata Preservation**: It preserves the metadata (location, creation date and modified date) from the source video, which is often lost when manually extracting frames.

- **Efficient Naming**: The program generates unique filenames for the extracted frames to prevent overwriting existing files in the "exported_images" folder.

- **User-Friendly GUI**: The program provides a graphical user interface (GUI) for selecting the input folder, making it accessible to users with minimal command-line experience.

- **Skip Invalid Videos**: It skips iPhone Live photo video dimensions to avoid processing videos where a live photo exists.

In summary, this GUI program simplifies the process of extracting frames with smiles from videos while preserving metadata, providing an efficient and user-friendly solution for this task.
