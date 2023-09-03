import cv2
import dlib

# Load the pre-trained face and smile detectors
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

# Function to detect smiles
def detect_smile(gray, face):
    smiles = smile_cascade.detectMultiScale(
        gray,
        scaleFactor=1.7,
        minNeighbors=22,
        minSize=(25, 25),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    for (sx, sy, sw, sh) in smiles:
        return True

    return False

# Open the video file
video_path = 'input_video.MOV'
cap = cv2.VideoCapture(video_path)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Detect smiles in the face region
        is_smiling = detect_smile(gray[y:y+h, x:x+w], (x, y, w, h))

        if is_smiling:
            # Save the frame when a smiling face is detected
            cv2.imwrite('smiling_face.jpg', frame)
            break  # Exit the loop after saving the image

cap.release()
cv2.destroyAllWindows()
