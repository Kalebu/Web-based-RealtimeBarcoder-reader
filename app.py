from cv2 import cv2
from PIL import Image
from pyzbar import pyzbar
from flask import Flask , render_template, Response , url_for, redirect

app = Flask(__name__)

barcode_text = None

def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y , w, h = barcode.rect
        barcode_text = barcode.data.decode('utf-8')
        print(barcode_text)
        cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
    return frame

def capture_frames():
    camera = cv2.VideoCapture(0)
    if camera.isOpened():
        ret, frame = camera.read()
    while ret:
        ret, frame = camera.read()
        frame = read_barcodes(frame)
        ret , frame = cv2.imencode('.jpg', frame)
        if ret:
            frame = frame.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield False

@app.route('/video_frames')
def video_frames():
    return Response(capture_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html', _value = barcode_text)

if __name__ == '__main__':
    app.run(debug=True)