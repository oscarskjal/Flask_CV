from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import pyttsx3
import cv2
import threading

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
camera = cv2.VideoCapture(0)

speech_done = False  

def detect_faces():
    global speech_done
    
    while True:
        success, frame = camera.read()
        if not success:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        face_list = [{"x": int(x), "y": int(y), "width": int(w), "height": int(h)} for (x, y, w, h) in faces]
        socketio.emit('faces_detected', {'faces': face_list})
        
        if face_list and not speech_done:  
            speech_done = True  
            engine = pyttsx3.init()
            engine.say("Hello! I am your computer vision Arcada assistant here to introduce you to Arcada!")
            engine.runAndWait()

@app.route('/')
def home():
    return "Hello Flask from Ubuntu!"

@app.route('/text_to_speech', methods=['POST'])
def text_to_speech():
    data = request.json
    text = data.get('text', '')
    if text:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return jsonify({"status": "success", "message": "Text spoken successfully"}), 200
    return jsonify({"status": "error", "message": "No text provided"}), 400

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    threading.Thread(target=detect_faces, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000)
