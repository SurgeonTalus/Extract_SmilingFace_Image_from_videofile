<!DOCTYPE html>
<html>
<head>
    <title>Extract_SmilingFace_Image_from_videofile</title>
</head>
<body>
    <h1>Extract_SmilingFace_Image_from_videofile</h1>

    <h2>Description</h2>
    <p>This Python script can be used to extract a frame containing a smiling face from a video file and save it as an image. It utilizes OpenCV, dlib, numpy, and ffmpeg-python libraries for video processing and face detection.</p>

    <h2>Installation</h2>
    <p>Make sure to download all the required files to the same directory.</p>
    <pre><code>pip install opencv-python-headless
pip install dlib
pip install numpy
pip install ffmpeg-python
    </code></pre>
    <p>You also need to download the <a href="http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2">shape_predictor_68_face_landmarks.dat</a> file from the following link and extract it to the same directory/folder.</p>

    <h2>Usage</h2>
    <ol>
        <li>Add a video file called <code>input_video.MOV</code> to the same directory where you have the script and the <code>shape_predictor_68_face_landmarks.dat</code> file.</li>
        <li>Open your terminal and navigate to the folder using the <code>cd</code> command.</li>
        <li>Drag the video file's path into the terminal to set the working directory.</li>
        <li>Run the script using Python 3:</li>
    </ol>
    <pre><code>python3 smile_detection.py</code></pre>
    <p>If the video contains a smiling face, the script will extract it and save it as <code>smiling_face.jpg</code>.</p>

    <p>Enjoy your smiling face image!</p>
</body>
</html>
