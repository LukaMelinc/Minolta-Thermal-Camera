import serial
import serial.tools.list_ports
import time

# Class for Fluke 4181 (precision infrared calibrator) 
class Fluke:

    def __init__(self):
        # Defines
        self.serialport = serial.Serial()
        self.port = "COM5"
        self.baudrate = 9600
        self.bytesize = serial.EIGHTBITS
        self.parity = serial.PARITY_NONE
        self.stopbits = serial.STOPBITS_ONE
        self.xonxoff = False
        self.rtscts = False
        self.dsrdtr = False

    # Open communication with device
    def open_serial_fluke(self):
        try:
            self.serialport = serial.Serial(port=self.port, baudrate=self.baudrate, bytesize=self.bytesize, parity=self.parity, stopbits=self.stopbits, xonxoff=self.xonxoff, rtscts=self.rtscts, dsrdtr=self.dsrdtr, timeout=1)
            print(f"Opened {self.port} at {self.baudrate} baudrate.")
            return self.serialport
        except serial.SerialException as e:
            print(f"Error opening serial port {self.port}: {e}")
            return None     

    # Reset device registers
    def FlukeRegisterReset(self):
        data = '*CLS' + ' \r'
        self.serialport.write(data.encode('ascii'))

    # Read device info
    def FlukeID(self):
        data = '*IDN?' + ' \r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    # Read device info
    def FlukeID(self):
        data = '*IDN?' + ' \r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

