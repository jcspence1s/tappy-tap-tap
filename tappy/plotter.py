#!/usr/bin/python
from pymata_aio.pymata3 import PyMata3
from ik import getPoints, reflect, rotate, inverse
import curses
import asyncio
from time import sleep

SERVO_PIN1 = 9  # Back Right
SERVO_PIN2 = 10 # Front
SERVO_PIN3 = 11 # Back Left 
SERVO_POWER = 7

movement = 2


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
        # Not ideal to call non-wrapper for analog write, but used to not modify base package
        task = self.board.loop.create_task(self.board.core.analog_write(self.pin, self.angle))
        self.board.loop.run_until_complete(task)

class Robot():

    def map(self, num, in_min, in_max, out_min, out_max):
        return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    
    def move_to(self, x, y, z):
        points = getPoints(list(self.cur_loc.values()), [x, y, z], self.num_steps, 'easeInQuad')
        for point in points:
            coords = self._move_to(*point)

    def move(self, direction):
        funcs = {
            'up': self.move_up,
            'down': self.move_down,
            'left': self.move_left,
            'right': self.move_right
        }
        funcs[direction]()
        print("X: {} Y: {} Z:{}".format(*self.cur_loc.values()))

    def move_up(self):
        global movement
        if self.cur_loc['x'] < 0:
            self.cur_loc['z'] += .15
        self.cur_loc['x'] += movement
        self.cur_loc['y'] -= movement
        self.move_to(*list(self.cur_loc.values()))

    def move_down(self):
        global movement
        if self.cur_loc['x'] < 0:
            self.cur_loc['z'] -= .15
        self.cur_loc['x'] -= movement
        self.cur_loc['y'] += movement
        self.move_to(*list(self.cur_loc.values()))

    def move_left(self):
        global movement
        self.cur_loc['x'] -= movement
        self.cur_loc['y'] -= movement
        self.move_to(*list(self.cur_loc.values()))

    def move_right(self):
        global movement
        self.cur_loc['x'] += movement
        self.cur_loc['y'] += movement
        self.move_to(*list(self.cur_loc.values()))

    def move_z_up(self): 
        global movement
        self.cur_loc['z'] += movement/2
        self.move_to(*list(self.cur_loc.values()))
    
    def move_z_down(self): 
        global movement
        self.cur_loc['z'] -= movement/2
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
        
    def add_node(self, action):
        if action is 'tap':
            self.script.append([list(self.cur_loc.values()), 'tap'])
        elif action is 'swipe_up':
            self.script.append([list(self.cur_loc.values()), 'up'])
        elif action is 'swipe_down':
            self.script.append([list(self.cur_loc.values()), 'down'])
        elif action is 'swipe_left':
            self.script.append([list(self.cur_loc.values()), 'left'])
        elif action is 'swipe_right':
            self.script.append([list(self.cur_loc.values()), 'right'])
        else:
            self.script.append([list(self.cur_loc.values()), None])

    def play_script(self):
        for node in self.script:
            self.cur_loc['x'] = node[0][0]
            self.cur_loc['y'] = node[0][1]
            self.cur_loc['z'] = node[0][2]
            self.move_to(*node[0])
            self.board.sleep(.25)
            if node[1] is 'tap':
                self.tap()
            elif node[1] is None:
                pass
            else:
                self.swipe(node[1])
            self.board.sleep(.25)

    def __str__(self):
        out = "+++++NODES+++++\n"
        for node in self.script:
            out += "{} {} {} - {}\n".format(node[0][0], node[0][1], node[0][2], node[1])
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
        self.s_power = Servo("{} PW".format(self.name), self.board, SERVO_POWER)
        self.script = list()
        self.script.append([list(self.cur_loc.values()), None])

    def swipe(self, direction):
        global movement
        options = {
            'left': [self.move_left, self.move_right],
            'right': [self.move_right, self.move_left],
            'up': [self.move_up, self.move_down],
            'down': [self.move_down, self.move_up]
        }
        mvmnt = movement
        movement = movement/2
        for i in range(16):
            self.move_z_down()
        tapping = True
        for x in range(30):
            options[direction][0]()
        for i in range(16):
            self.move_z_up()
        for x in range(30):
            options[direction][1]()
        tapping = False
        movement = mvmnt

    def tap(self):
        for i in range(8):
            self.move_z_down()
        for i in range(8):
            self.move_z_up()

    def power(self, action):
        self.s_power.set_angle(110)
        if action is 'hold':
            sleep(5)
            self.swipe('right')
            sleep(1)
        else:
            sleep(.5)
        self.s_power.set_angle(0)



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
        elif c == 114:
            tappy.add_node('tap')
        elif c == 119:
            tappy.play_script()
        elif c == 82:
            tappy.script = list()
            tappy.move_to(0, 0, -140)
            tappy.script.append([[0, 0, -140], None])
        elif c == 564: # alt + up
            #swipe up
            tappy.swipe('up')
        elif c == 523: # alt + down
            tappy.swipe('down')
        elif c == 543: # alt + left
            tappy.swipe('left')
            #swipe left
        elif c == 558: # alt + right
            tappy.swipe('right')
            #swipe right
        elif c == 566: # ctrl + up
            tappy.add_node('swipe_up')
        elif c == 525: # ctrl + down
            tappy.add_node('swipe_down')
        elif c == 545: # ctrl + left
            tappy.add_node('swipe_left')
        elif c == 560: # ctrl + right
            tappy.add_node('swipe_right')
        elif c == 112: # pOWAH
            tappy.power('tap')
        elif c == 80: # POWAH
            tappy.power('hold')

        nodes = tappy.__str__()

        controls = '''Arrows: Movement
Shift+Up/Shift+Down: Z movement
s: Tap and hold(Toggle)
Mouse Click: Tap(Non-toggle)
r: Record current position to tap script
w: Replay record script
Shift+r: Clear script
Alt + Arrow: Swipe in arrow direction
ctrl + Arrow: Script swipe'''
        stdscr.clear()
        stdscr.addstr(0, 0, out)
        stdscr.addstr(1, 0, controls)
        stdscr.addstr(20, 0, nodes)

if __name__ == "__main__":
    curses.wrapper(main)
