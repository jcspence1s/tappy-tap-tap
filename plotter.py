#!/usr/bin/python
from pymata_aio.pymata3 import PyMata3
from ik import moveTo

board = PyMata3()
SERVO_PIN1 = 9  # Back Right
SERVO_PIN2 = 10 # Front
SERVO_PIN3 = 11 # Back Left

corners = [moveTo(40, 40, -175), moveTo(-13, 50, -175), moveTo(0, 0, -175), moveTo(13, -50, -175), moveTo(-40, -35, -175), moveTo(0, 0, -175), moveTo(0, 0, -135)]

def setup():
    board.servo_config(SERVO_PIN1)
    board.servo_config(SERVO_PIN2)
    board.servo_config(SERVO_PIN3)
    board.analog_write(SERVO_PIN1, 0)
    board.analog_write(SERVO_PIN2, 0)
    board.analog_write(SERVO_PIN3, 0)

def loop():
    choice = input("X, Y, Z or cross: ")
    if "cross" == choice:
        for point in corners:
            board.analog_write(SERVO_PIN1, int(point[2]))
            board.analog_write(SERVO_PIN2, int(point[1]))
            board.analog_write(SERVO_PIN3, int(point[3]))
            board.sleep(.25)
        return
    try:
        x, y, z = choice.split()
    except:
        print("error")
        return
    x = int(x)
    y = int(y)
    z = int(z)
    if not -40 <= x <= 40:
        print("X out of range")
        return
    if not -50 <= y <= 50:
        print("Y out of range")
        return
    print("You entered X:{} Y:{} Z:{}".format(x, y, z))
    coords = moveTo(x, y, z)
    print(coords)
    board.analog_write(SERVO_PIN1, int(coords[2]))
    board.analog_write(SERVO_PIN2, int(coords[1]))
    board.analog_write(SERVO_PIN3, int(coords[3]))
    

if __name__ == "__main__":
    setup()
    while True:
        loop()
