import serial
import serial.tools.list_ports
import time

# Class for MINOLTA LAND CYCLOPS 300AF (infrared camera)
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
        # ERROR Codes
        # - Sound (BEEP): wrong communicating parameters
        # - E32: Data of more than 32 characters were received
        # - E33: Delimiter code error (use of only <CR> command)
        # - E34: Unaccaptable command an/or data were input
        

    # Open communication with device
    # - port: name of port ('COM3')
    # - baudrate: serial communication baudrate (4800)
    def CyclopsOpenSerial(self, port, baudrate):
        try:
            self.serialport = serial.Serial(port = port, baudrate = baudrate, bytesize = self.bytesize, parity = self.parity, stopbits = self.stopbits, xonxoff = self.xonxoff, rtscts = self.rtscts, dsrdtr = self.dsrdtr, timeout = 1)
            print(f"Opened {self.port} at {self.baudrate} baudrate.")
            return self.serialport
        except serial.SerialException as e:
            print(f"Error opening serial port {self.port}: {e}")
            return None     
        

    # Causes autofocus to be performed once
    # Response: OK! - focus achived, DF? - focus could not be achived, MAN - focus mode is switched to MANUAL
    def CyclopsAutofocus(self):
        data = 'AF' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Requests output of alarm settings (upper limit, lower limit, sound on or off)
    # Response: Alarm settings data
    def CyclopsAlarmRead(self):
        data = 'AR' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")


    #  UNFINISHED COMMAND  #    
    # Sets alarm upper value, lower limit value and sound on or odd according to the value
    # Response: OK! - values are acceptable, E34 - values are unaccaptabel
    def CyclopsAlarmSet(self, AlLow, AlHigh, AlEN):
        data = 'AS&' + str(AlLow) + str(AlHigh) + str(AlEN) + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Causes measureing display mode to be changed to AVERAGE. These data is output when camera enters display hold
    # Response: Measurement data
    def CyclopsAverageModeSet(self):
        data = 'AVRG' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")
    

    # Causes the camera to CANCLE monitor mode and returns to manual measuring mode. Most reacent measured data is 
    # held in the display and output. Can only be used when camera is in monitor mode
    # Response: Measurement data
    def CyclopsCancleModeSet(self):
        data = 'CE' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")
    

    # Causes the camera to enter MONITOR mode and output the resulting measurement data 
    # Response: Measurement data
    def CyclopsCancleModeSet(self):
        data = 'CS' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")


    #  UNFINISHED COMMAND  #
    # Sets emissivity to the value sets with argument
    # Response: Response: OK! - values are acceptable, E34 - values are unaccaptabel
    def CyclopsEmissivitySet(self, emiss):
        data = 'ES&' + str(emiss) + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")


    # Causes the camera to take measurement and output the resoult. Only works if the camera is in display mode
    # Response: Measurement data
    def CyclopsGetTemp(self):
        data = 'MS' + ' \r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Causes the camera to be changed to NORMAL measuring mode. Measurement data is output when camera enters display mode
    # Response: Measurement data
    def CyclopsNormalModeSet(self):
        data = 'NRML' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")


    # Causes the camera to be changed to PEAK measuring mode. Measurement data is output when camera enters display mode
    # Response: Measurement data
    def CyclopsPeakModeSet(self):
        data = 'PEAK' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Status request. Causes camera to output data about temperature units, emisivity value, measuring mode, focus mode and alarm status
    # Response: Status word
    def CyclopsStatusRead(self):
        data = 'SR' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Causes the camera to be changed to VALLEY measuring mode. Measurement data is output when camera enters display mode
    # Response: Measurement data
    def CyclopsValleyModeSet(self):
        data = 'VLLY' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")






