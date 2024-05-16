import serial
import serial.tools.list_ports
import time

# Class for MINOLTA LAND CYCLOPS 300AF (infrared camera)
class Cyclops:

    def __init__(self):
        # Defines
        self.serialport = serial.Serial()
        self.port = ""
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
            #print(f"Opened {self.port} at {baudrate} baudrate.")
            #print(self.serialport.is_open)
            return self.serialport.is_open
        except serial.SerialException as e:
            #print(f"Error opening serial port {self.port}: {e}")
            return self.serialport.is_open   
        

    # Close communication with device
    def CyclopsCloseSerial(self):
        response = self.serialport.close()
        return response
    

    # Read communication output
    def CyclopsReadSerial(self):
        response = self.serialport.readline().decode().strip()
        return response
        

    # Causes autofocus to be performed once
    # Response: OK! - focus achived, DF? - focus could not be achived, MAN - focus mode is switched to MANUAL
    def CyclopsAutofocus(self):
        data = 'AF' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        #print(f"Response: {response}")
        return response

    
    # Requests output of alarm settings (upper limit, lower limit, sound on or off)
    # Response: Alarm settings data
    def CyclopsAlarmRead(self):
        data = 'AR' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        #print(f"Response: {response}")
        return response


    #  UNFINISHED COMMAND  #    
    # Sets alarm upper value, lower limit value and sound on or odd according to the value
    # To enable specific alarm set ON_OFF_ALx with "S" or disable it with "C" (if desabled use alarm value as "")
    # Response: OK! - values are acceptable, E34 - values are unaccaptabel
    def CyclopsAlarmSet(self, ON_OFF_AlHigh, Val_AlHigh, ON_OFF_AlLow, Val_AlLow, AlEN):

        # Space matching depanding on value send (expected lenght of message)
        if ON_OFF_AlHigh == "C":
            AlHighSpaces = "    "       # 4x space
        else:
            if Val_AlHigh > -1000 and Val_AlHigh < 10000: 
                AlHighSpaces = ""       # 0x space
            if Val_AlHigh > -100 and Val_AlHigh < 1000: 
                AlHighSpaces = " "      # 1x space
            if Val_AlHigh > -10 and Val_AlHigh < 100: 
                AlHighSpaces = "  "     # 2x space
            if Val_AlHigh >= 0 and Val_AlHigh < 10: 
                AlHighSpaces = "   "    # 3x space

        if ON_OFF_AlLow == "C":
            AlLowSpaces = "    "        # 4x space
        else:
            if Val_AlLow > -1000 and Val_AlLow < 10000: 
                AlLowSpaces = ""        # 0x space
            if Val_AlLow > -100 and Val_AlLow < 1000: 
                AlLowSpaces = " "       # 1x space
            if Val_AlLow > -10 and Val_AlLow < 100: 
                AlLowSpaces = "  "      # 2x space
            if Val_AlLow >= 0 and Val_AlLow < 10: 
                AlLowSpaces = "   "     # 3x space            

        data = 'AS&' + str(ON_OFF_AlHigh) + AlHighSpaces + str(Val_AlHigh) + str(ON_OFF_AlLow) + AlLowSpaces + str(Val_AlLow) + str(AlEN) + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        #print(f"Response: {response}")
        return response

    
    # Causes measureing display mode to be changed to AVERAGE. These data is output when camera enters display hold
    # Response: Measurement data
    def CyclopsAverageModeSet(self):
        data = 'AVRG' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        #print(f"Response: {response}")
        return response
    

    # Causes the camera to CANCLE monitor mode and returns to manual measuring mode. Most reacent measured data is 
    # held in the display and output. Can only be used when camera is in monitor mode
    # Response: Measurement data
    def CyclopsCancleModeSet(self):
        data = 'CE' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        #print(f"Response: {response}")
        return response
    

    # Causes the camera to enter MONITOR mode and output the resulting measurement data 
    # Response: Measurement data
    def CyclopsMonitorModeSet(self):
        data = 'CS' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        #print(f"Response: {response}")
        return response


    # Sets emissivity to the value sets with argument
    # Response: Response: OK! - values are acceptable, E34 - values are unaccaptabel
    def CyclopsEmissivitySet(self, emiss):
        data = 'ES&' + str(round(emiss,2)) + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        #print(f"Response: {response}")
        return response


    # Causes the camera to take measurement and output the resoult. Only works if the camera is in display mode
    # Response: Measurement data
    def CyclopsGetTemp(self):
        data = 'MS' + ' \r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        #print(f"Response: {response}")
        return response

    
    # Causes the camera to be changed to NORMAL measuring mode. Measurement data is output when camera enters display mode
    # Response: Measurement data
    def CyclopsNormalModeSet(self):
        data = 'NRML' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        #print(f"Response: {response}")
        return response


    # Causes the camera to be changed to PEAK measuring mode. Measurement data is output when camera enters display mode
    # Response: Measurement data
    def CyclopsPeakModeSet(self):
        data = 'PEAK' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        #print(f"Response: {response}")
        return response

    
    # Status request. Causes camera to output data about temperature units, emisivity value, measuring mode, focus mode and alarm status
    # Response: Status word
    def CyclopsStatusRead(self):
        data = 'SR' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        #print(f"Response: {response}")
        return response

    
    # Causes the camera to be changed to VALLEY measuring mode. Measurement data is output when camera enters display mode
    # Response: Measurement data
    def CyclopsValleyModeSet(self):
        data = 'VLLY' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        #print(f"Response: {response}")
        return response






