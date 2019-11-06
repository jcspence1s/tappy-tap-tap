#!/usr/bin/python
from pymata_aio.pymata3 import PyMata3
from ik import moveTo, test_move, getPoints
from tkinter import *

board = PyMata3()
SERVO_PIN1 = 9  # Back Right
SERVO_PIN2 = 10 # Front
SERVO_PIN3 = 11 # Back Left 
SERVO_POWER = 7

cur_loc = [0, 0, -100]
numberOfSteps = 10

corners = [moveTo(40, 40, -175), moveTo(-13, 50, -175), moveTo(0, 0, -175), moveTo(13, -50, -175), moveTo(-40, -35, -175), moveTo(0, 0, -175), moveTo(0, 0, -135)]


def setup():
    board.servo_config(SERVO_PIN1)
    board.servo_config(SERVO_PIN2)
    board.servo_config(SERVO_PIN3)
    board.servo_config(SERVO_POWER)
    board.analog_write(SERVO_PIN1, 0)
    board.analog_write(SERVO_PIN2, 0)
    board.analog_write(SERVO_PIN3, 0)
    board.analog_write(SERVO_POWER, 0)

def loop(cur_loc):
    choice = input("X, Y, Z or cross or POWER: ")
    if "cross" == choice:
        for point in corners:
            board.analog_write(SERVO_PIN1, int(point[2]))
            board.analog_write(SERVO_PIN2, int(point[3]))
            board.analog_write(SERVO_PIN3, int(point[1]))
            board.sleep(.25)
        return
    elif "POWER" == choice:
        board.analog_write(SERVO_POWER, 100)  #Fine tune
        board.sleep(2)
        board.analog_write(SERVO_POWER, 0)
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
    #coords = moveTo(x, y, z)
    #coords = test_move(cur_loc, [x, y, z], numberOfSteps, 'linear')
    points = getPoints(cur_loc, [x, y, z], numberOfSteps, 'easeInQuad')
    for point in points:
        print("{}->{}".format(cur_loc, point))
        cur_loc = point
        coords = moveTo(*point)
        board.analog_write(SERVO_PIN1, int(coords[2]))
        board.analog_write(SERVO_PIN2, int(coords[1]))
        board.analog_write(SERVO_PIN3, int(coords[3]))

    #board.analog_write(SERVO_PIN1, int(coords[2]))
    #board.analog_write(SERVO_PIN2, int(coords[1]))
    #board.analog_write(SERVO_PIN3, int(coords[3]))
    
def main(cur_loc, numberOfSteps):
    root = Tk()
    x = IntVar()
    y = IntVar() 
    z = IntVar()

    x_scale = Scale(root, orient=HORIZONTAL, from_=-50, to=50, variable = x)
    y_scale = Scale(root, orient=HORIZONTAL, from_=-70, to=60, variable = y)
    z_scale = Scale(root, orient=HORIZONTAL, from_=-150, to=-190, variable = z)

    x_scale.pack(anchor=CENTER)
    y_scale.pack(anchor=CENTER)
    z_scale.pack(anchor=CENTER)

    def get_and_move():
        global cur_loc, numberOfSteps,SERVO_PIN1, SERVO_PIN2, SERVO_PIN3, board
        new_x = x.get()
        new_y = y.get()
        new_z = z.get()
        points = getPoints(cur_loc, [new_x, new_y, new_z], numberOfSteps, 'linear')
        for point in points:
            coords = moveTo(*point)
            
            print(point.__str__() + ":" + coords.__str__())
            if coords[0] is 1:
                print("Error in move")
                return
            cur_loc = point
            print(coords)
            board.analog_write(SERVO_PIN1, int(coords[2]))
            board.analog_write(SERVO_PIN2, int(coords[1]))
            board.analog_write(SERVO_PIN3, int(coords[3]))

    def tap():
        global cur_loc, numberOfSteps
        new_x = x.get()
        new_y = y.get()
        new_z = z.get()
        points = getPoints(cur_loc, [new_x, new_y, new_z - 10], 2, 'linear')
        origin = points[::-1]
        for point in points:
            coords = moveTo(*point)
            
            if coords[0] is 1:
                print("Error in move")
                return
            cur_loc = point
            board.analog_write(SERVO_PIN1, int(coords[2]))
            board.analog_write(SERVO_PIN2, int(coords[1]))
            board.analog_write(SERVO_PIN3, int(coords[3]))
        board.sleep(.1)
        for point in origin:
            coords = moveTo(*point)
            
            if coords[0] is 1:
                print("Error in move")
                return
            cur_loc = point
            board.analog_write(SERVO_PIN1, int(coords[2]))
            board.analog_write(SERVO_PIN2, int(coords[1]))
            board.analog_write(SERVO_PIN3, int(coords[3]))

    move_button = Button(root, text="Move to pos", command=get_and_move)
    tap_button = Button(root, text="TAP!!!!", command=tap)
    move_button.pack(anchor=CENTER)
    tap_button.pack(anchor=CENTER)

    label = Label(root)
    label.pack()

    root.mainloop()
    

if __name__ == "__main__":
    setup()
    main(cur_loc, numberOfSteps)
#    while True:
#        loop(cur_loc)
