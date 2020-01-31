import board
from time import sleep
import threading
from board import Core

class Robot:
    holder = {}
    writing = threading.Lock()
    work = threading.Semaphore(0)
    #work = threading.Condition()
    def __init__(self, name, board, servo1, servo2, servo3):
        self.name = name

        self.board = board

        self.s1 = Servo(self.board, servo1)
        #self.s2 = Servo(self.board, servo2)
        #self.s3 = Servo(self.board, servo3)
        #self.t_s1 = threading.Thread(target=self.s1.loop)
        #self.t_s2 = threading.Thread(target=self.s2.loop)
        #self.t_s3 = threading.Thread(target=self.s3.loop)

    def run(self):
        self.t_s1.start()
        self.t_s2.start()
        self.t_s3.start()
        #config each servo in their own thread with a lock have them waiting 
        #self.board.config_servo(self.s1)
        #self.board.config_servo(self.s2)
        #self.board.config_servo(self.s3)
        #self.board.analog_write(self.s1, 20)
        #self.board.analog_write(self.s2, 20)
        #self.board.analog_write(self.s3, 20)

class Servo:
    def __init__(self, board, pin):
        self.pin = pin
        self.board = board
        Robot.holder[pin] = 0
        print("Pin: {} grabbing lock setup".format(pin))
        Robot.writing.acquire()
        self.board.config_servo(self.pin)
        sleep(1)
        self.board.analog_write(self.pin, Robot.holder[pin])
        Robot.writing.release()
        print("Pin: {} releasing lock setup".format(pin))

    def loop(self):
        try:
            while True:
                print("Pin: {} waiting for work.".format(self.pin))
                Robot.work.acquire()
                Robot.writing.acquire()
                self.board.analog_write(self.pin, Robot.holder[pin])
                Robot.writing.release()
        except KeyboardInterrupt:
            return None



        

if __name__ == "__main__":
    c = Core()
    rob = Robot("tappy",c, 9, 10, 11)

