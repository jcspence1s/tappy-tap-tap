#!/usr/bin/python
from pymata_aio.pymata3 import PyMata3
from ik import getPoints, reflect, rotate, inverse
import curses

SERVO_PIN1 = 9  # Back Right
SERVO_PIN2 = 10 # Front
SERVO_PIN3 = 11 # Back Left 
SERVO_POWER = 7


class Phone():
    def __init__(self):
        self.points = {'top_left': (0, 0, 0),
                'top_right': (0, 0, 0),
                'bot_left': (0, 0, 0),
                'bot_right': (0, 0, 0),
                'center': (0, 0, 0)}

    def __str__(self):
        out = '++++CONFIG++++\n'
        out += '{}: {}\n'.format('center', self.points['center'])
        out += '{}: {}\n'.format('top_left', self.points['top_left'])
        out += '{}: {}\n'.format('top_right', self.points['top_right'])
        out += '{}: {}\n'.format('bot_left', self.points['bot_left'])
        out += '{}: {}\n'.format('bot_right', self.points['bot_right'])
        return out

    def set_point(self, where, cur_point):
       self.points[where] = tuple(cur_point) 

class Servo():
    def __init__(self, name, board, pin):
        self.board = board
        self.board.servo_config(pin)
        self.pin = pin
        self.name = name
        self.angle = 0
        board.analog_write(self.pin, self.angle)

    def set_angle(self, angle):
        self.angle = int(angle)
        self.board.analog_write(self.pin, self.angle)

class Robot():
    def map(self, num, in_min, in_max, out_min, out_max):
        return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    
    def move_to(self, x, y, z):
        points = getPoints(list(self.cur_loc.values()), [x, y, z], self.num_steps, 'easeInQuad')
        for point in points:
            coords = self._move_to(*point)

    def move_up(self):
        self.cur_loc['x'] += 1
        self.cur_loc['y'] -= 1
        self.move_to(*list(self.cur_loc.values()))

    def move_down(self):
        self.cur_loc['x'] -= 1
        self.cur_loc['y'] += 1
        self.move_to(*list(self.cur_loc.values()))

    def move_left(self):
        self.cur_loc['x'] -= 1
        self.cur_loc['y'] -= 1
        self.move_to(*list(self.cur_loc.values()))

    def move_right(self):
        self.cur_loc['x'] += 1
        self.cur_loc['y'] += 1
        self.move_to(*list(self.cur_loc.values()))

    def move_z_up(self): 
        self.cur_loc['z'] += 1
        self.move_to(*list(self.cur_loc.values()))
    
    def move_z_down(self): 
        self.cur_loc['z'] -= 1
        self.move_to(*list(self.cur_loc.values()))

    def _move_to(self, x, y, z):
        #points = getPoints(self.cur_loc, [x, y, z], self.num_steps, 'linear')
        self.cur_loc['x'] = x
        self.cur_loc['y'] = y
        self.cur_loc['z'] = z 
        reflected = reflect(x, y)
        rotated = rotate(reflected[0], reflected[1])
        angles = inverse(rotated[0], rotated[1], z)
        
        tmp1 = self.map(angles[1], 0, 90, 19, 101)
        tmp2 = self.map(angles[2], 0, 90, 19, 101)
        tmp3 = self.map(angles[3], 0, 90, 19, 101)

        self.s1.set_angle(tmp1)
        self.s2.set_angle(tmp2)
        self.s3.set_angle(tmp3)
        
    def add_node(self):
        self.script.append(list(self.cur_loc.values()))

    def play_script(self):
        for node in self.script:
            self.cur_loc['x'] = node[0]
            self.cur_loc['y'] = node[1]
            self.cur_loc['z'] = node[2]
            self.move_to(*node)
            self.board.sleep(1)

    def __str__(self):
        out = "+++++NODES+++++\n"
        for node in self.script:
            out += "{} {} {}\n".format(node[0], node[1], node[2])
        for i in range(25):
            out += "                                    \n"
        return out

    def __init__(self, name):
        self.name = name
        self.board = PyMata3()
        self.cur_loc = {'x': 0,'y': 0, 'z': -140}
        self.num_steps = 5
        self.s1 = Servo("{} S1".format(self.name), self.board, SERVO_PIN1)
        self.s2 = Servo("{} S2".format(self.name), self.board, SERVO_PIN2)
        self.s3 = Servo("{} S3".format(self.name), self.board, SERVO_PIN3)
        self.move_to(0, 0, -140)
        self.power = Servo("{} PW".format(self.name), self.board, SERVO_POWER)
        self.script = list()
        self.script.append(list(self.cur_loc.values()))

def main(stdscr):
    curses.mousemask(1)
    stdscr.clear()
    tappy = Robot("Tappy")
    stdscr.refresh()
    tapping = False
    while True:
        c = stdscr.getch()
        out = "Key Pressed: {}\n".format(c)
        if c == curses.KEY_UP:
            tappy.move_up()
        elif c == curses.KEY_DOWN:
            tappy.move_down()
        elif c == curses.KEY_LEFT:
            tappy.move_left()
        elif c == curses.KEY_RIGHT:
            tappy.move_right()
        elif c == 336: # shift - down arrow
            tappy.move_z_down()
        elif c == 337: # shift - up arrow
            tappy.move_z_up()
        elif c == 115 and not tapping: # s
            for i in range(5):
                tappy.move_z_down()
            tapping = True
        elif c == 115:
            for i in range(5):
                tappy.move_z_up()
            tapping = False
        elif c == curses.KEY_MOUSE:
            for i in range(5):
                tappy.move_z_down()
            for i in range(5):
                tappy.move_z_up()
        elif c == 114:
            tappy.add_node()
        elif c == 119:
            tappy.play_script()
        elif c == 82:
            tappy.script = list()
            tappy.move_to(0, 0, -140)
            tappy.script.append([0, 0, -140])

        nodes = tappy.__str__()

        stdscr.addstr(0, 0, out)
        stdscr.addstr(20, 0, nodes)

if __name__ == "__main__":
    curses.wrapper(main)
