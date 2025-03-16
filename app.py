from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import cv2
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
CORS(app, resources={r"/*": {"origins": "*"}})  # CORS for all routes
socketio = SocketIO(app, cors_allowed_origins="*")

# Pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

camera = cv2.VideoCapture(0)

def detect_faces():
    while True:
        success, frame = camera.read()
        if not success:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        face_list = [{"x": int(x), "y": int(y), "width": int(w), "height": int(h)} for (x, y, w, h) in faces]
        socketio.emit('faces_detected', {'faces': face_list})

@app.route('/')
def home():
    return "Hello Flask from ubuntu!"

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    threading.Thread(target=detect_faces, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000)