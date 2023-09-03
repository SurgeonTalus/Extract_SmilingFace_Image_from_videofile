<!DOCTYPE html>
<html>
<head>
    <title>Extract Smiling Face Image from Video</title>
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

<p>Download and extract this file to the same directory/folder:</p>
<p><a href="http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2">shape_predictor_68_face_landmarks.dat</a></p>

<p>Add a videofile called <code>input_video.MOV</code> to the path.</p>
<p>Navigate to the folder in the terminal using the CD command and drag the file path to it.</p>
<p>Write <code>python3 smile_detection.py</code> and hit enter.</p>

<p>If there is a smiling face in the video, you will get output: <code>smiling_face.jpg</code></p>

</body>
</html>
