from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
from PyQt6.QtCore import QTimer, QDateTime
import datetime
import serial
import serial.tools.list_ports
import sys
import numpy as np
import matplotlib.pyplot as plt
import pyqtgraph as pg
import time
import threading
import csv

import fluke
import cyclops

# INFO:
"""
    # Open serial communication with devices #
     - fluke.FlukeOpenSerial("COM5", 9600)
     - cyclops.CyclopsOpenSerial("COM3", 4800)

     # Error: "isModal" or "setSizeGripEnabled" -> delete "modal" or "setSizeGrip" in .ui files

"""
fluke = fluke.Fluke()
cyclops = cyclops.Cyclops()

################################################################
########################## E34 WINDOW ##########################
################################################################

Ui_E34Window, BaseClass = uic.loadUiType("E34Window.ui")

class E34Window(QMainWindow, Ui_E34Window):
    def __init__(self, parent=None):
        super(E34Window, self).__init__(parent)
        self.setupUi(self)
        self.btnOK.clicked.connect(self.close_window)

    def close_window(self):
        self.close()  


##################################################################
########################## ERROR WINDOW ##########################
##################################################################

Ui_ErrorWindow, BaseClass = uic.loadUiType("errorWindow.ui")

class ErrorWindow(QMainWindow, Ui_ErrorWindow):
    def __init__(self, parent=None):
        super(ErrorWindow, self).__init__(parent)
        self.setupUi(self)
        self.btnOK.clicked.connect(self.close_window)

    def close_window(self):
        self.close()  


##################################################################
########################## FOCUS WINDOW ##########################
##################################################################

Ui_FocusWindow, BaseClass = uic.loadUiType("focusWindow.ui")

class FocusWindow(QMainWindow, Ui_FocusWindow):
    def __init__(self, parent=None):
        super(FocusWindow, self).__init__(parent)
        self.setupUi(self)
        self.btnOK.clicked.connect(self.close_window)

    def close_window(self):
        self.close()


#################################################################
########################## MAIN WINDOW ##########################
#################################################################

Ui_MainWindow, BaseClass = uic.loadUiType("mainWindow.ui")

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        #self.setMinimumSize(870, 550)

        # Declare files / functions
        self.fluke = fluke
        self.cyclops = cyclops
        self.timerRecord = threading.Timer
        self.timerSample = threading.Timer

        # Variables
        self.ports = []
        self.portsDescription = []
        self.baudRate = ["4800", "9600", "19200", "38400", "57600", "115200", "230400", "460800", "921600"]
        self.calibratorStatus = 0
        self.recording = 0
        self.sample = 0
        self.CameraMode = ["Normal", "Average", "Peak", "Valley"]

        self.errorWindow = ErrorWindow() # Error for connection on calibrator
        self.focusWindow = FocusWindow() # Report window after focusing
        self.E34Window = E34Window()

        # Date, TIme
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)  # 1000 milliseconds (1 second)
        self.updateTime()

        # GUI
        self.btnRefresh.clicked.connect(self.list_serial_ports)         # Refresh button 
        self.cmbBaud.addItems(self.baudRate)                            # BaudRate combo box
        self.btnExit.clicked.connect(self.appExit)                      # Exit
        self.cmbCamMode.addItems(self.CameraMode)                       # Measuring modes of camera
        self.btnAutofocus.clicked.connect(self.focus)                   # Triger auto focus of camera
        self.btnSetMode.clicked.connect(self.setMode)                   # Set measuring mode of camera
        self.btnSetAlarm.clicked.connect(self.setAlarm)                 # Set alarm for temperature
        self.cbUpperAlarm.stateChanged.connect(self.grayOutAlarm)       # Grayout alarm settings if not enabled
        self.cbLowerAlarm.stateChanged.connect(self.grayOutAlarm)       # Grayout alarm settings if not enabled
        self.btnConnect.clicked.connect(self.calibratorConnect)         # Connect to calibrator
        self.btnSetEmisivity.clicked.connect(self.setEmisivityCamera)   # Connect to calibrator
        self.btnExport.clicked.connect(self.exportCSV)                  # Export measurements in CSV file
        self.btnAlarmRead.clicked.connect(self.alarmRead)               # Read alarm values
        self.btnRecord.clicked.connect(self.recordMeas)                 # Record measurements
        self.btnStartSample.clicked.connect(self.sampleMeas)            # Read sample data

        # Graph
        self.plot(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],  # Hours
            [30, 32, 34, 32, 33, 31, 29, 32, 35, 45],  # Temperature
        )


    # Plot drawing #
    def plot(self, hour, temperature):
        self.graphWidget.plot(hour, temperature)


    # Updating time and date #
    def updateTime(self):
        current_time = QDateTime.currentDateTime()
        formatted_time = current_time.toString('HH:mm:ss')
        formatted_date = current_time.toString('dd.MM.yyyy')
        self.lblTime.setText(formatted_time)
        self.lblDate.setText(formatted_date)


    # Set camera mode #
    def setMode(self):
        selectedMode = self.cmbCamMode.currentText()
        match selectedMode:
            case "Normal":
                response = self.cyclops.CyclopsNormalModeSet()
            case "Average":
                response = self.cyclops.CyclopsAverageModeSet()
            case "Peak":
                response = self.cyclops.CyclopsPeakModeSet()
            case "Valley":
                response = self.cyclops.CyclopsValleyModeSet()
            case _:
                response = self.cyclops.CyclopsNormalModeSet()
        
        self.lblMode.setText(selectedMode)


    # Grying out widgets #
    def grayOutAlarm(self):
        self.dsbUpperAlarm.setEnabled(self.cbUpperAlarm.isChecked())
        self.dsbLowerAlarm.setEnabled(self.cbLowerAlarm.isChecked())


    # Set alarm values #
    def setAlarm(self):
        # S - enable, C - desable
        if self.cbUpperAlarm.isChecked():
            upperAlarm = "S"
            upperTemp = round(self.dsbUpperAlarm.value())
        else:
            upperAlarm = "C"
            upperTemp = ""

        if self.cbLowerAlarm.isChecked():
            lowerAlarm = "S"
            lowerTemp = round(self.dsbLowerAlarm.value())
        else:
            lowerAlarm = "C"
            lowerTemp = ""

        if self.cbSoundAlarm.isChecked():
            soundAlarm = "S"
        else:
            soundAlarm = "C"
        
        self.cyclops.CyclopsAlarmSet(upperAlarm, upperTemp, lowerAlarm, lowerTemp, soundAlarm)

    # Connect fluke calibrator #
    def calibratorConnect(self):
        if self.calibratorStatus == 0:
            selectedBaud = self.cmbBaud.currentText()
            selectedPort = self.cmbPorts.currentText()
            
            if selectedPort == "" or selectedBaud == "":
                self.errorWindow.show() # ERROR - unselected baud or port
            else: 
                index = self.portsDescription.index(selectedPort) # get name of that port ("COM3")
                report = self.fluke.FlukeOpenSerial(self.ports[index], selectedBaud)
                if report != True:
                    self.lblCalibratorStatus.setText("Disconnected")
                    self.errorWindow.show() # ERROR - unselected baud or port
                else:
                    self.lblCalibratorStatus.setText("Connected")
                    self.btnConnect.setText("Disconnect")
                    self.calibratorStatus = 1
        else:
            report = self.fluke.FlukeCloseSerial()
            if report != None:
                self.lblCalibratorStatus.setText("Connected")
                self.errorWindow.show() # ERROR - cant disconnect
            else:
                self.lblCalibratorStatus.setText("Disconnected")
                self.btnConnect.setText("Connect")
                self.calibratorStatus = 0 # disconnected


    # Set emisivity #
    def setEmisivityCamera(self):
        emisivity = self.dsbCameraEmisivity.value()
        self.cyclops.CyclopsEmissivitySet(emisivity)

    
    # Read alarm setting from camera and set them in program #
    def alarmRead(self):
        response = self.cyclops.CyclopsAlarmRead()
        if response == "E34" or response == "":
            self.E34Window.show() # ERROR

        splitValue = list(response)
        # Alarm high
        if splitValue[0] == "S": # ON
            self.dsbUpperAlarm.setEnabled(1)
            self.cbUpperAlarm.setChecked(True)
            AlUp = int(splitValue[1] + splitValue[2] + splitValue[3] + splitValue[4])
            self.dsbUpperAlarm.setValue(AlUp)
        elif splitValue[0] == "C": # OFF
            self.dsbUpperAlarm.setEnabled(0)
            self.cbUpperAlarm.setChecked(False)
        # Alarm low
        if splitValue[5] == "S": # ON
            self.dsbLowerAlarm.setEnabled(1)
            self.cbLowerAlarm.setChecked(True)
            AlLow = int(splitValue[6] + splitValue[7] + splitValue[8] + splitValue[9])
            self.dsbLowerAlarm.setValue(AlLow)
        elif splitValue[5] == "C": # OFF
            self.dsbLowerAlarm.setEnabled(0)
            self.cbLowerAlarm.setChecked(False)
        # Alarm sound
        if splitValue[10] == "S": # ON
            self.cbSoundAlarm.setChecked(True)
        elif splitValue[10] == "C": # OFF
            self.cbSoundAlarm.setChecked(False)


    # Focus and response #
    def focus(self):
        response = self.cyclops.CyclopsAutofocus()
        if response == "OK!":
            self.focusWindow.show()
            self.focusWindow.txtFocus.setText("Focus achived!")
        if response == "DF?":
            self.focusWindow.show()
            self.focusWindow.txtFocus.setText("Can't focus!")
        if response == "MAN":
            self.focusWindow.show()
            self.focusWindow.txtFocus.setText("Focus set to manual!")


    # Thread function to parallel measure values
    def RepeatFunction(self, interval, function, *args, **kwargs):
        self.timerRecord = threading.Timer(interval, self.RepeatFunction, [interval, function] + list(args), kwargs)
        self.timerRecord.start()
        function(*args, **kwargs)

    def Measure(self):
        # LPH 31.1
        val = self.cyclops.CyclopsReadSerial()
        val = val[3:]
        print(val)
        self.lcdTemperature.display(val)

    
    # Thread function to parallel measure values
    def RepeatFunctionSample(self, interval, function, *args, **kwargs):
        self.timerSample = threading.Timer(interval, self.RepeatFunctionSample, [interval, function] + list(args), kwargs)
        self.timerSample.start()
        function(*args, **kwargs)

    def MeasureSample(self):
        # LPH 31.1
        val = self.cyclops.CyclopsGetTemp()
        val = val[3:]
        print(val)
        


    # Read temperature in monitor mode
    def recordMeas(self):
        if self.recording == 0:
            self.btnRecord.setText("Stop")
            self.cyclops.CyclopsMonitorModeSet()
            self.recording = 1
             # Call my_function every n seconds
            self.RepeatFunction(0.25, self.Measure)
            return None
        if self.recording == 1:
            self.btnRecord.setText("Start")
            self.cyclops.CyclopsCancleModeSet()
            self.recording = 0
            self.timerRecord.cancel()  # Stop the timer
            return None
        

    # Read temperature in sample mode
    def sampleMeas(self):
        if self.sample == 0:
            self.sample = 1
             # Call my_function every n seconds
            sampleTime = self.dsbSampleTime.value()
            self.RepeatFunctionSample(sampleTime, self.MeasureSample)
            self.btnStartSample.setText("Stop")
            return None
        if self.sample == 1:
            self.sample = 0
            self.timerSample.cancel()  # Stop the timer
            self.btnStartSample.setText("Start")
            return None
            

    # List all available serial ports #
    def list_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        self.portsDescription = []
        self.ports = []
        if not ports:
            #print("No serial ports found!")
            return None

        for port in ports:
            #print(f"{port.device} - {port.description}")
            self.ports.append(port.device)
            self.portsDescription.append(port.description)
        
        self.cmbPorts.clear() # clear all devices in list
        self.cmbPorts.addItems(self.portsDescription) # add all new devices
    

    # Save measurements to CSV file
    def exportCSV(timestamps, values): # lists of times and measurement values
        DateTime = time.strftime("%Y_%m_%d-%H_%M-meritve")
        with open(str(DateTime) + 'file.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Time', 'Temp.'])
            writer.writerow([timestamps, values])  


    # Close application #
    def appExit(self):
        sys.exit() # dont call it directly
    


##################################################################
########################## START WINDOW ##########################
##################################################################

class StartWindow:
    def __init__(self):
        super().__init__()

        # Declare files / functions
        self.fluke = fluke
        self.cyclops = cyclops

        # Variables
        self.ports = []
        self.portsDescription = []
        self.baudRate = ["4800", "9600", "19200", "38400", "57600", "115200", "230400", "460800", "921600"]

        # GUI
        #self.setMinimumSize(400, 220)
        Form, Window = uic.loadUiType("startWindow.ui")
        self.app = QApplication([])       # Create an application object
        self.window = Window()            # Create a window object from the loaded UI class
        self.form = Form()                # Create a form object from the loaded UI class
        self.form.setupUi(self.window)    # Set up the UI from the form onto the window

        self.mainWindow = MainWindow()
        self.errorWindow = ErrorWindow()

        # Connect the button click to the function [Ensure pushButton matches the object name in Qt Designer]
        self.form.btnRefresh.clicked.connect(self.list_serial_ports)         # Refresh button 
        self.form.cmbBaud.addItems(self.baudRate)                            # BaudRate combo box
        self.form.btnExit.clicked.connect(self.appExit)                      # Exit
        self.form.btnConnect.clicked.connect(self.OpenMainWindow)            # Connect
    
        self.window.show()           # Display the window
        self.app.exec()              # Start the application's event loop


    # Close application #
    def appExit(self):
        sys.exit() # dont call it directly

    # Open main window or error #
    def OpenMainWindow(self):
        selectedBaud = self.form.cmbBaud.currentText()
        selectedPort = self.form.cmbPorts.currentText()
        
        if selectedPort == "" or selectedBaud == "":
            self.errorWindow.show() # ERROR - unselected baud or port
        else: 
            index = self.portsDescription.index(selectedPort) # get name of that port
            report = self.cyclops.CyclopsOpenSerial(self.ports[index], int(selectedBaud))
            if report == True:
                self.mainWindow.show() # OK -> main window
            else:
                self.errorWindow.show() # ERROR - unselected baud or port

   # List all available serial ports #
    def list_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        self.portsDescription = []
        self.ports = []
        if not ports:
            #print("No serial ports found!")
            return None

        for port in ports:
            #print(f"{port.device} - {port.description}")
            self.ports.append(port.device)
            self.portsDescription.append(port.description)
        
        self.form.cmbPorts.clear() # clear all devices in list
        self.form.cmbPorts.addItems(self.portsDescription) # add all new devices




        
