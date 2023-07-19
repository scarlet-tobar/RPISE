import cv2
import base64
import threading
from flask import Flask, render_template, Response

app = Flask(__name__)

# Create a VideoCapture object to access the camera
video_stream = cv2.VideoCapture(0)

def generate_frame():
    while True:
        success, frame = video_stream.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = base64.b64encode(buffer).decode('utf-8')
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame.encode() + b'\r\n')

@app.route('/')
def index():
    return render_template('app/index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=True, threaded=True)