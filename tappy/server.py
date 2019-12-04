from flask import Flask, render_template, send_from_directory, Response
from plotter import *
from imutils.video import VideoStream
import imutils
import cv2
import threading

app = Flask(__name__)
tappy = Robot("Tappy")
padlock = threading.Lock()

# src is the video device number from /dev/video#
stream = VideoStream(src=2).start()

def jpg_encode():
    global stream
    while True:
        frame = stream.read()
        #frame = imutils.resize(frame, width=400)
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        if not flag:
            continue
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n'+ bytearray(encodedImage) + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(jpg_encode(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/plotter')
def plotter():
    print("Hello")
    return "nothing"

@app.route('/up')
def up():
    padlock.acquire(True)
    tappy.move('up')
    padlock.release()
    return "test"

@app.route('/down')
def down():
    padlock.acquire(True)
    tappy.move('down')
    padlock.release()
    return "test"

@app.route('/left')
def left():
    padlock.acquire(True)
    tappy.move('left')
    padlock.release()
    return "test"

@app.route('/right')
def right():
    padlock.acquire(True)
    tappy.move('right')
    padlock.release()
    return "test"

@app.route('/z_up')
def z_up():
    padlock.acquire(True)
    tappy.move_z_up()
    padlock.release()
    return "test"

@app.route('/z_down')
def z_down():
    padlock.acquire(True)
    tappy.move_z_down()
    padlock.release()
    return "test"

@app.route('/swipe_up')
def swipe_up():
    padlock.acquire(True)
    tappy.swipe('up')
    padlock.release()
    return "test"

@app.route('/swipe_down')
def swipe_down():
    padlock.acquire(True)
    tappy.swipe('down')
    padlock.release()
    return "test"

@app.route('/swipe_left')
def swipe_left():
    padlock.acquire(True)
    tappy.swipe('left')
    padlock.release()
    return "test"

@app.route('/swipe_right')
def swipe_right():
    padlock.acquire(True)
    tappy.swipe('right')
    padlock.release()
    return "test"

@app.route('/power_tap')
def power_tap():
    padlock.acquire(True)
    tappy.power('tap')
    padlock.release()
    return "test"

@app.route('/power_hold')
def power_hold():
    padlock.acquire(True)
    tappy.power('hold')
    padlock.release()
    return "test"

@app.route('/tap')
def tap():
    padlock.acquire(True)
    tappy.tap()
    padlock.release()
    return "test"

@app.route('/tap_up')
def tap_up():
    return "test"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
