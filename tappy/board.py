import serial
import sys

class Core:

    ANALOG_MESSAGE = 0xE0
    START_SYSEX = 0xF0
    END_SYSEX = 0xF7
    SERVO_CONFIG = 0x70

    def __init__(self):
        self.port = self.get_port()

    def get_port(self):
        ports = ['/dev/ttyACM0', 'com3']
        con_port = None

        for port in ports:
            try:
                tmp = serial.Serial(port, 57600, timeout=0)
                print("Port found: " + str(tmp))
                con_port = tmp
            except serial.SerialException:
                if port == 'com3':
                    print("Unable to find Arduino")
                    sys.exit(1)

        return con_port

    def analog_write(self, pin, data):
        command =  [Core.ANALOG_MESSAGE + pin, data & 0x7f, (data >> 7) & 0x7f]
        self.build_command(command)

    def build_command(self, command):
        message = ""

        for i in command:
            message += chr(i)

        self.write(message)

    def config_servo(self, pin, min_pulse=544, max_pulse=2400):
        print("Configure pin {}".format(pin))
        command = [pin, min_pulse & 0x7f, (min_pulse >> 7) & 0x7f, max_pulse & 0x7f, 
                (max_pulse >> 7) & 0x7f]

        self.send_sysex(Core.SERVO_CONFIG, command)


    def send_sysex(self, sysex_command, sysex_data=None):
        if not sysex_data:
            sysex_data = []

        sysex_message = chr(Core.START_SYSEX)
        sysex_message += chr(sysex_command)
        if len(sysex_data):
            for d in sysex_data:
                sysex_message += chr(d)
        sysex_message += chr(Core.END_SYSEX)
        print("Sending: {}".format(sysex_message))
        
        for data in sysex_message:
            self.write(data)

    def write(self, message):
        for data in message:
            try:
                self.port.write(bytes([ord(data)]))
            except BaseException as e:
                print("Unable to write: " + str(e))
                sys.exit()
