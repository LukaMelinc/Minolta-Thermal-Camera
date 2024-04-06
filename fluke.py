import serial
import serial.tools.list_ports
import time

# Class for Fluke 4180-4181 (precision infrared calibrator) 
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
    # - port: name of port ('COM5')
    # - baudrate: serial communication baudrate (9600)
    def FlukeOpenSerial(self, port, baudrate):
        try:
            self.serialport = serial.Serial(port = port, baudrate = baudrate, bytesize = self.bytesize, parity = self.parity, stopbits=self.stopbits, xonxoff = self.xonxoff, rtscts = self.rtscts, dsrdtr = self.dsrdtr, timeout = 1)
            print(f"Opened {self.port} at {self.baudrate} baudrate.")
            return self.serialport
        except serial.SerialException as e:
            print(f"Error opening serial port {self.port}: {e}")
            return None     


    # Clear the status registers
    def FlukeRegisterReset(self):
        data = '*CLS' + ' \r'
        self.serialport.write(data.encode('ascii'))


    # Read the product information
    def FlukeID(self):
        data = '*IDN?' + ' \r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")


    # Read the main heat output percent
    def FlukeID(self):
        data = '*IDN?' + ' \r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")


    # Read the main heat output percent
    def FlukeOutpData(self):
        data = '*OUTP:DATA?' + ' \r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")


    # Read the Main Heat output
    def FlukeOutpStatRead(self):
        data = '*OUTP:STAT?' + ' \r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")
        

    # Set the Main Heat output enable
    # - state: off [0] or on [1]
    def FlukeOutpStatSet(self, state):
        data = '*OUTP:STAT ' + str(state) + ' \r'
        self.serialport.write(data.encode('ascii'))


    # Read the program name by identifier
    # - n: 1 to 8
    def FlukeProgNameRead(self, n):
        data = 'PROG:[' + str(n) + ']NAME?' + ' \r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")


    # Set the program name by identifier
    # - n: 1 to 8
    # - name: characters 0 to 9, A to Z and -
    def FlukeProgNameSet(self, n, name):
        data = 'PROG:[' + str(n) + ']NAME ' + name + ' \r'
        self.serialport.write(data.encode('ascii'))


    # Read the program advance option
    def FlukeProgOptAdvRead(self):
        data = 'PROG:OPT:ADV?' + ' \r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")
        

    # Set the program advance option
    # - n; 0 (prompt) or 1 (continue automatically)
    def FlukeProgOptAdvSet(self, n):
        data = 'PROG:OPT:ADV ' + str(n)+ ' \r'
        self.serialport.write(data.encode('ascii'))


    # Read the program cyclesS
    def FlukeProgOptCyclRead(self):
        data = 'PROG:OPT:CYCL?' + ' \r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")
        

    # Set the program cycles
    # - n: 1 to 999, default 1.
    def FlukeProgOptCyclSet(self, n):
        data = 'PROG:OPT:CYCL ' + str(n)+ ' \r'
        self.serialport.write(data.encode('ascii'))


    # Read the program settle option
    def FlukeProgOptSettRead(self):
        data = 'PROG:OPT:SETT?' + ' \r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")
        

    # Read or set the program settle option
    # -n: 0 (apply default limit) or 1 (apply STABLE LIMIT setting).
    def FlukeProgOptSettSet(self, n):
        data = 'PROG:OPT:SETT ' + str(n)+ ' \r'
        self.serialport.write(data.encode('ascii'))


    # Read the program soak time, 0 to 500 minutes. Default 1
    def FlukeProgOptSoakRead(self):
        data = 'PROG:OPT:SOAK?' + ' \r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")
        

    # Read or set the program soak time
    # - n: 0 to 500 minutes. Default 1
    def FlukeProgOptSoakSet(self, n):
        data = 'PROG:OPT:SOAK ' + str(n)+ ' \r'
        self.serialport.write(data.encode('ascii'))


    # Read a program parameter, for a given program identified
    # - n: 1 to 8
    # - par:
    # SPOi = setpoints (1-8), where i = the value of one setpoint
    # POIN = the number of setpoints for the indicated program
    # IRTE= the emmissivity ε value 0.9 to 1.0, default 0.95
    # DIST= the distance from the target to the UUT in cm, 0.1 to 999.9
    # APER= yes or no to promt user for the aperature. 0 = none, 1 = prompt user
    def FlukeProgParParRead(self, n, par):
        data = 'PROG[' + str(n) + ']PAR? ' + par + '?' + ' \r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")
        

    # Set a program parameter, for a given program identified
    # - n: 1 to 8
    # - par:
    # SPOi = setpoints (1-8), where i = the value of one setpoint
    # POIN = the number of setpoints for the indicated program
    # IRTE= the emmissivity ε value 0.9 to 1.0, default 0.95
    # DIST= the distance from the target to the UUT in cm, 0.1 to 999.9
    # APER= yes or no to promt user for the aperature. 0 = none, 1 = prompt user
    def FlukeProgParParSet(self, n, par, val):
        data = 'PROG[' + str(n) + ']PAR ' + par + ',' + str(val) + ' \r'
        self.serialport.write(data.encode('ascii'))


    # Read a list of program parameters *
    def FlukeProgParCatRead(self):
        data = 'PROG:OPT:SOAC?' + ' \r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")


    # Advance to the next program step if waiting for user input
    def FlukeProgPromAdvSet(self):
        data = 'PROG:PROM:ADV' + '\r'
        self.serialport.write(data.encode('ascii'))

    
    # Read the manual program advance prompt state
    # 0 (operating or program off) or 1 (waiting for user input)
    def FlukeProgPromStatRead(self):
        data = 'PROG:STAT?' + ' \r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Read the program selection
    def FlukeProgSelRead(self):
        data = 'PROG:SEL?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Set the program selection
    # - n: 1 to 8
    def FlukeProgSelSet(self, n):
        data = 'PROG:SEL ' + str(n) + ' \r'
        self.serialport.write(data.encode('ascii'))

    
    # Read the program execution state for the selected program
    def FlukeProgStatRead(self):
        data = 'PROG:STAT?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Read or set the program execution state for the selected program
    # - state: 0(off) or 1(run)
    def FlukeProgStatSet(self, state):
        data = 'PROG:STAT ' + str(state) + ' \r'
        self.serialport.write(data.encode('ascii'))


    # Read the instrument calibration date in yyyy,mm,dd format.
    def FlukeSourCalDateRead(self):
        data = 'SOUR:CAL:DATE?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")


    # Set the instrument calibration date in yyyy,mm,dd format
    # - year: range 2000 to 2999
    # - month: range 1 to 12
    # - day: range 0 to 31 *
    # !!! Protected with password !!!
    def FlukeSourCalDateSet(self, year, month, day):
        data = 'SOUR:CAL:DATE ' + str(year) + ',' + str(month) + ',' + str(day) + ',' + '\r'
        self.serialport.write(data.encode('ascii'))

    
    # Read the nominal IR calibration emissivity (0.95)
    def FlukeSourCalEmisRead(self):
        data = 'SOUR:CAL:EMIS?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")
    

    # Read a control temperature parameter
    # - x: a numeric value indicating the parameter, valid values are 1,2, or 3 representing IR CAL 1, IR CAL 2, and IR CAL 3.
    def FlukeSourCalParxRead(self, x):
        data = 'SOUR:CAL:PAR' + str(x) + '?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Read a control temperature parameter
    # - x: a numeric value indicating the parameter, valid values are 1,2, or 3 representing IR CAL 1, IR CAL 2, and IR CAL 3.
    # - val: Range = +/-99.0; default: 0.0
    # !!! Protected with password !!!
    def FlukeSourCalParxSet(self, x, val):
        data = data = 'SOUR:CAL:PAR' + str(x) + ' ' + str(val) + '?' + '\r'
        self.serialport.write(data.encode('ascii'))


    # Read the calibration temperature associated with a calibration parameter
    # - x: a numeric value indicating the parameter, valid values are 1,2, or 3.
    def FlukeSourCalParxTempRead(self, x):
        data = 'SOUR:CAL:PAR' + str(x) + ':TEMP?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")


    # Read the calibration IR wavelength option
    def FlukeSourCalWavRead(self):
        data = 'SOUR:CAL:WAV?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")


    # Set the calibration IR wavelength option
    # - val: 0(8-14um) or 1(undefined); default 0
    def FlukeSourCalWavSet(self, val):
        data = 'SOUR:CAL:WAV ' + str(val) + '\r'
        self.serialport.write(data.encode('ascii'))

    
    # Read the IR emissivity setting
    def FlukeSourEmisRead(self):
        data = 'SOUR:EMIS?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")


    # Set the IR emissivity setting
    # - val: range 0.90 to 1.0, default 0.95.
    def FlukeSourEmisSet(self, val):
        data = 'SOUR:EMIS ' + str(val) + '\r'
        self.serialport.write(data.encode('ascii'))

    
    # Read the main control loop derivative time in seconds
    def FlukeSourLconDerRead(self):
        data = 'SOUR:LCON:DER?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")


    # Read or set the main control loop derivative time in seconds
    # - val: Min: 0.0, Max: 99.9
    # !!! Protected with password !!!
    def FlukeSourLconDerSet(self, val):
        data = 'SOUR:LCON:DER ' + str(val) + '\r'
        self.serialport.write(data.encode('ascii'))

    
    # Read the main control loop integral time in seconds
    def FlukeSourLconIntRead(self):
        data = 'SOUR:LCON:INT?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")


    # Read or set the main control loop derivative time in seconds
    # - val: Range = {10.0-999.9}
    # !!! Protected with password !!!
    def FlukeSourLconIntSet(self, val):
        data = 'SOUR:LCON:INT ' + str(val) + '\r'
        self.serialport.write(data.encode('ascii'))

    
    # Read the main control loop proportional band in °C
    def FlukeSourLconPbanRead(self):
        data = 'SOUR:LCON:PBAN?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")


    # Set the main control loop proportional band in °C
    # - val: Range = {1.0-99.9}
    # !!! Protected with password !!!
    def FlukeSourLconPbanSet(self, val):
        data = 'SOUR:LCON:PBAN ' + str(val) + '\r'
        self.serialport.write(data.encode('ascii'))

    
    # Read a main temperature preset set-point
    def FlukeSourListSpoRead(self, n):
        data = 'SOUR:LIST:SPO:' + str(n) + '?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")


    # Set a main temperature preset set-point
    def FlukeSourListSpoSet(self, n, val):
        data = 'SOUR:LCON:PBAN ' + str(n) + str(val) + '\r'
        self.serialport.write(data.encode('ascii'))


    # Reset the cutout to enable the system
    def FlukeSourProtCleaReset(self):
        data = 'SOUR:PROT:CLEAR' + '\r'
        self.serialport.write(data.encode('ascii'))

    
    # Read the hard cutout temperature set-point in °C or °F
    def FlukeSourProtHcutRead(self):
        data = 'SOUR:PROT:HCUT?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")


    # Read the soft cutout set-point
    def FlukeSourProtScutLevRead(self):
        data = 'PROT:SCUT:LEV?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Set the soft cutout set-point 
    # - val: integer value from 0 to 700
    # !!! Protected with password !!!
    def FlukeSourProtScutLevSet(self, val):
        data = 'PROT:SCUT:LEV ' + str(val) + '\r'
        self.serialport.write(data.encode('ascii'))


    # Read the temperature cutout tripped state
    def FlukeSourProtTripRead(self):
        data = 'PROT:PROT:TRIP?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Read the control temperature rate of change (Scan Rate), °C or °F per minute.
    def FlukeSourRateRead(self):
        data = 'SOUR:RATE?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Set the control temperature rate of change (Scan Rate), °C or °F per minute.
    # - val: Min: 0.10, Max: 500.00; Default: 100.00
    def FlukeSourRateSet(self, val):
        data = 'SOUR:RATE ' + str(val) + '\r'
        self.serialport.write(data.encode('ascii'))

    
    # Reads the target temperature (uncompensated sensor temperature MENU|VIEW TEMP|BLOCK TEMP) in °C or °F
    def FlukeSourSensBlocRead(self):
        data = 'SOUR:SENS:BLOC?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Reads the apparent temperature, in °C or °F
    def FlukeSourSensDataRead(self):
        data = 'SOUR:SENS:DATA?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")


    # Reads the control set-point, °C or °F 
    def FlukeSourSpoRead(self):
        data = 'SOUR:SPO?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Set the control set-point, °C or °F 
    # - val: a real value with acceptance limits based on the model
    def FlukeSourSpoSet(self, val):
        data = 'SOUR:SPO ' + str(val) + '\r'
        self.serialport.write(data.encode('ascii'))
    

    # Read the stability alert (beep)
    def FlukeSourStabBeepRead(self):
        data = 'SOUR:STAB:BEEP?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Set the stability alert (beep) 
    # - n: [0] is disable, [1] is enable beep. Default: 1 (Enable Beep)
    def FlukeSourStabBeepSet(self, n):
        data = 'SOUR:STAB:BEEP ' + str(n) + '\r'
        self.serialport.write(data.encode('ascii'))

    
    # Read the control temperature stability, °C or °F
    def FlukeSourStabDatRead(self):
        data = 'SOUR:STAB:DAT?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Read the control temperature stability limit, °C or °F 
    def FlukeSourStabLimRead(self):
        data = 'SOUR:STAB:LIM?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Read or set the control temperature stability limit
    # - n: positive real value. Range = {0.01 to 5.0 (°C)}; Default: 0.1 (°C) (Model 4180) 0.4 (°C) (Model 4181)
    def FlukeSourStabLimSet(self, n):
        data = 'SOUR:STAB:LIM ' + str(n) + '\r'
        self.serialport.write(data.encode('ascii'))
    

    # Read the temperature stability test results. Stable = 1; Unstable = 0 
    def FlukeSourStabTestRead(self):
        data = 'SOUR:STAB:TEST?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Beep the system beeper
    def FlukeSystBeepImm(self):
        data = 'SYST:BEEP:IMM' + '\r'
        self.serialport.write(data.encode('ascii'))

    
    # Read the keyboard beep function
    def FlukeSystBeepKeybRead(self):
        data = 'SYST:BEEP:KEYB?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Set the keyboard beep function
    # - n: 0=Off, 1=On. Default: 1
    def FlukeSystBeepKeybSet(self, n):
        data = 'SYST:BEEP:KEYB ' + str(n) + '\r'
        self.serialport.write(data.encode('ascii'))

    
    # Read the main code version
    def FlukeSystCodVersRead(self):
        data = 'SYST:COD:VERS?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Read serial interface baud rate
    def FlukeSystCommSerBaudRead(self):
        data = 'SYST:COMM:SER:BAUD?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Set serial interface baud rate 
    # - baud: standard baud rate value. Range baud = {1200, 2400, 4800, 9600, 19200, and 38400}; Default: 9600
    def FlukeSystBeepKeybSet(self, baud):
        data = 'SYST:COMM:SER:BAUD ' + str(baud) + '\r'
        self.serialport.write(data.encode('ascii'))

    
    # Read serial interface linefeed enable
    def FlukeSystCommSerLinRead(self):
        data = 'SYST:COMM:SER:LIN?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Set serial interface linefeed enable
    # - n: value 1 or 0. [0] = LF OFF, [1] = LF ON; Default: 0 (OFF)
    def FlukeSystCommSerLinSet(self, n):
        data = 'SYST:COMM:SER:LIN ' + str(n) + '\r'
        self.serialport.write(data.encode('ascii'))

    
    # Read the decimal format
    def FlukeSystDecFormRead(self):
        data = 'SYST:DEC:FORM?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Set the decimal format
    # - n: period [0], comma [1]. Default: 0 (Period)
    def FlukeSystDecFormSet(self, n):
        data = 'SYST:DEC:FORM ' + str(n) + '\r'
        self.serialport.write(data.encode('ascii'))

    
    # Read the most recent error from the error queue
    def FlukeSystErrRead(self):
        data = 'SYST:ERR?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Read the keypad lockout
    def FlukeSystKlockRead(self):
        data = 'SYST:KLOCK?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Set the keypad lockout
    # - n: [0] = unlock, and [1] = lock. Default: 0 (Unlock)
    # !!! Protected with password !!!
    def FlukeSystKlockSet(self, n):
        data = 'SYST:KLOCK ' + str(n) + '\r'
        self.serialport.write(data.encode('ascii'))

    
    # Read the display language
    def FlukeSystLangRead(self):
        data = 'SYST:LANG?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Set the display language
    # - lang: ENGL, FREN, SPAN, ITAL, GERM, RUSS, JAP, CHIN; Default: English. (Default: Russian for Model 418x-RS)
    def FlukeSystLangSet(self, lang):
        data = 'SYST:LANG ' + lang + '\r'
        self.serialport.write(data.encode('ascii'))

    
    # Read the available display languages
    def FlukeSystLangCatRead(self):
        data = 'SYST:LANG:CAT?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Disable access to password protected setting commands
    def FlukeSystPassCdisSet(self):
        data = 'SYST:PASS:CDIS ' + '\r'
        self.serialport.write(data.encode('ascii'))

    
    # Enable access to password protected setting commands
    # - n: four digit password. Range = {0000 – 9999};
    def FlukeSystPassCenSet(self, n):
        data = 'SYST:PASS:CEN ' + str(n) + '\r'
        self.serialport.write(data.encode('ascii'))

    
    # Read the access state of password protected setting commands
    def FlukeSystPassCenStatRead(self):
        data = 'SYST:PASS:CEN:STAT?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Set the password
    # - n: new four digit password. Range = {0000 – 9999}; Default: 1234
    # !!! Protected with password !!!
    def FlukeSystPassNewSet(self, n):
        data = 'SYST:PASS:NEW ' + str(n) + '\r'
        self.serialport.write(data.encode('ascii'))


    # Read password protection level
    def FlukeSystPassProtRead(self):
        data = 'SYST:PASS:PROT?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Set password protection level
    # - n: [0] = low, [1] = high
    def FlukeSystPassProtSet(self, n):
        data = 'SYST:PASS:PROT ' + str(n) + '\r'
        self.serialport.write(data.encode('ascii'))

    
    # Read the display temperature units
    def FlukeUnitTempRead(self):
        data = 'UNIT:TEMP?' + '\r'
        self.serialport.write(data.encode('ascii'))
        time.sleep(0.05)
        response = self.serialport.readline().decode().strip()
        print(f"Response: {response}")

    
    # Set the display temperature units
    # - n: character “C” or “F”. Default: C
    def FlukeUnitTempSet(self, n):
        data = 'UNIT:TEMP ' + str(n) + '\r'
        self.serialport.write(data.encode('ascii'))

    

    




 
 

