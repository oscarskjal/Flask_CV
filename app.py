from flask import Flask, jsonify
import cv2
import numpy as np

app = Flask(__name__)

# pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

@app.route('/')
def home():
    return "Hello Flask from ubuntu!"


@app.route('/detect_faces_camera', methods=['GET'])
def detect_faces_camera():
    # Open the default camera
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        return jsonify({"error": "Could not open camera"}), 500

    ret, frame = cap.read()
    cap.release()

    if not ret:
        return jsonify({"error": "Failed to capture image from camera"}), 500

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    face_list = []
    for (x, y, w, h) in faces:
        face_list.append({"x": int(x), "y": int(y), "width": int(w), "height": int(h)})

    return jsonify({"faces": face_list})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


