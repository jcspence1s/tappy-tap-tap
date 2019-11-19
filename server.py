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
    tappy.move_up()
    return "test"

if __name__ == "__main__":
    app.run()
