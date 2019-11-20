from flask import Flask, render_template, send_from_directory
from plotter import *

app = Flask(__name__)
tappy = Robot("Tappy")

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/plotter')
def plotter():
    print("Hello")
    return "nothing"

@app.route('/up')
def up():
    tappy.move('up')
    return "test"

@app.route('/down')
def down():
    tappy.move('down')
    return "test"

@app.route('/left')
def left():
    tappy.move('left')
    return "test"

@app.route('/right')
def right():
    tappy.move('right')
    return "test"

@app.route('/z_up')
def z_up():
    tappy.move_z_up()
    return "test"

@app.route('/z_down')
def z_down():
    tappy.move_z_down()
    return "test"

@app.route('/swipe_up')
def swipe_up():
    tappy.swipe('up')
    return "test"

@app.route('/swipe_down')
def swipe_down():
    tappy.swipe('down')
    return "test"

@app.route('/swipe_left')
def swipe_left():
    tappy.swipe('left')
    return "test"

@app.route('/swipe_right')
def swipe_right():
    tappy.swipe('right')
    return "test"

@app.route('/power_tap')
def power_tap():
    tappy.power('tap')
    return "test"

@app.route('/power_hold')
def power_hold():
    tappy.power('hold')
    return "test"

@app.route('/tap')
def tap():
    for i in range(10):
        tappy.move_z_down()
    for i in range(10):
        tappy.move_z_up()
    return "test"

@app.route('/tap_up')
def tap_up():
    return "test"

if __name__ == "__main__":
    app.run()
