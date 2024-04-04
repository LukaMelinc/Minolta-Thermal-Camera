import serial
import serial.tools.list_ports
import time

# Class for Fluke 4181 (precision infrared calibrator) 
class Cyclops:

    def __init__(self):
        # Defines
        self.serialport = serial.Serial()
        self.port = "COM3"
        self.baudrate = 4800
        self.bytesize = serial.SEVENBITS
        self.parity = serial.PARITY_EVEN
        self.stopbits = serial.STOPBITS_TWO
        self.xonxoff = False
        self.rtscts = True
        self.dsrdtr = False

    # Open communication with device
    def open_serial_cyclops(self):
        try:
            self.serialport = serial.Serial(port=self.port, baudrate=self.baudrate, bytesize=self.bytesize, parity=self.parity, stopbits=self.stopbits, xonxoff=self.xonxoff, rtscts=self.rtscts, dsrdtr=self.dsrdtr, timeout=1)
            print(f"Opened {self.port} at {self.baudrate} baudrate.")
            return self.serialport
        except serial.SerialException as e:
            print(f"Error opening serial port {self.port}: {e}")
            return None     

    # Measure temp.
    def CyclopsGetTemp(self):
        data = 'MS' + ' \r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")



