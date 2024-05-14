from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtCore import QTimer, QDateTime
from PyQt6.QtGui import QPixmap
#import datetime
import serial
import serial.tools.list_ports
import sys
import numpy as np
import matplotlib.pyplot as plt
import pyqtgraph as pg
import time
import threading
#import queue
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


######################################################################
########################## CONNECTED WINDOW ##########################
######################################################################

Ui_ConnectedWindow, BaseClass = uic.loadUiType("connectedWindow.ui")

class ConnectedWindow(QMainWindow, Ui_ConnectedWindow):
    def __init__(self, parent=None):
        super(ConnectedWindow, self).__init__(parent)
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
        self.timerSample = threading.Timer(0, None) # test values (crash protection)
        self.recordThread = threading.Thread()
        self.stopEvent = threading.Event()

        self.errorWindow = ErrorWindow() # Error for connection on calibrator
        self.focusWindow = FocusWindow() # Report window after focusing
        self.E34Window = E34Window()     # Error in communication
        self.connectedWindow = ConnectedWindow() # Succesfuly connected

        # Variables
        self.ports = []
        self.portsDescription = []
        self.baudRate = ["4800", "9600", "19200", "38400", "57600", "115200", "230400", "460800", "921600"]
        self.calibratorStatus = 0
        self.cameraStatus = 0
        self.recording = 0
        self.sample = 0
        self.CameraMode = ["Normal", "Average", "Peak", "Valley"]
        self.CalibratorProgNum = ["1", "2", "3", "4", "5", "6", "7", "8"]

        self.measurements = [] # Buffer for collected measurements - Measurements buffer
        self.times = [] # Buffer for measurements times - Time buffer
        self.sampleTime = 0
        self.timerCounter = 0
        self.sampleNumber = 0

        # Date, TIme
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)  # 1000 milliseconds (1 second)
        self.updateTime()

        # GUI
        self.tabWidgetMeasure.setCurrentIndex(0)
        self.tabFluke.setCurrentIndex(0)
        self.btnRefreshCal.clicked.connect(self.list_serial_ports)      # Refresh button 
        self.btnRefreshCam.clicked.connect(self.list_serial_ports)      # Refresh button 
        self.cmbBaudCal.addItems(self.baudRate)                         # BaudRate combo box - fluke
        self.cmbBaudCam.addItems(self.baudRate)                         # BaudRate combo box - cyclopse
        self.btnExit.clicked.connect(self.appExit)                      # Exit
        self.cmbCamMode.addItems(self.CameraMode)                       # Measuring modes of camera
        self.btnAutofocus.clicked.connect(self.focus)                   # Triger auto focus of camera
        self.btnSetMode.clicked.connect(self.setMode)                   # Set measuring mode of camera
        self.btnSetAlarm.clicked.connect(self.setAlarm)                 # Set alarm for temperature
        self.cbUpperAlarm.stateChanged.connect(self.grayOut)            # Grayout alarm settings if not enabled
        self.cbLowerAlarm.stateChanged.connect(self.grayOut)            # Grayout alarm settings if not enabled
        self.btnConnectCal.clicked.connect(self.calibratorConnect)      # Connect to calibrator
        self.btnSetEmisivity.clicked.connect(self.setEmisivityCamera)   # Set emisivity
        self.btnExport.clicked.connect(self.exportCSV)                  # Export measurements in CSV file
        #self.btnAlarmRead.clicked.connect(self.alarmRead)               # Read alarm values
        self.btnRecord.clicked.connect(self.recordMeas)                 # Record measurements
        self.btnStartSample.clicked.connect(self.sampleMeas)            # Start measuring - sample
        self.btnCameraStatusRead.clicked.connect(self.readCameraData)   # Read camera data
        self.cbTimerOnOff.stateChanged.connect(self.grayOut)            # Enable / disable sample timer
        self.btnConnectCam.clicked.connect(self.cameraConnect)          # Camera connect in main
        self.tabWidgetMeasure.currentChanged.connect(self.tabMainChange)# Read camera data with tab click
        self.tabFluke.currentChanged.connect(self.tabFlukeChange)       # Read fluke data with tab click


        # add picture 
        pixmap = QPixmap("./Dokumentacija/Tabela_241x276.png")  # Replace with the path to your image file
        self.lblTable.setPixmap(pixmap)
        self.lblTable

        # Graph
        self.figure, self.graph = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout(self.graphWidget)
        layout.addWidget(self.canvas)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.graph.set_xlabel('Time [s]')
        self.graph.set_ylabel('Temp. [°C]')
        self.graph.grid()
        self.figure.tight_layout()


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
    def grayOut(self):
        self.dsbUpperAlarm.setEnabled(self.cbUpperAlarm.isChecked())
        self.dsbLowerAlarm.setEnabled(self.cbLowerAlarm.isChecked())
        self.dsbTimerHours.setEnabled(self.cbTimerOnOff.isChecked())
        self.dsbTimerMinutes.setEnabled(self.cbTimerOnOff.isChecked())

    
    def tabMainChange(self, index):
        # Main tab widget
        if index == 1: # Measure tab
            self.alarmRead()
            self.readCameraData()
        if index == 2: # Calibrator tab
            self.tabFlukeChange(0)


    def tabFlukeChange(self, index):
        # Main tab widget
        if index == 0: # Measure tab
            response = self.fluke.FlukeSourRateRead()
            self.dsbScanRate.setValue(response)
            response = self.fluke.FlukeSourEmisRead()
            self.dsrSetIRT.setValue(response)
            response = self.fluke.FlukeSourProtHcutRead()
            self.lblHardCutout.setText(response)
            response = self.fluke.FlukeSourProtScutLevRead()
            self.dsbSoftCutout.setValue(response)
            #response = self.fluke.FlukeProgOptSettRead()
            #self.dsbStabLimit.setValue(response)


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
            selectedPort = self.cmbPortsCal.currentText()
            
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
                    self.btnConnectCal.setText("Disconnect")
                    self.calibratorStatus = 1
        else:
            report = self.fluke.FlukeCloseSerial()
            if report != None:
                self.lblCalibratorStatus.setText("Connected")
                self.errorWindow.show() # ERROR - cant disconnect
            else:
                self.lblCalibratorStatus.setText("Disconnected")
                self.cmbPortsCal.clear() # clear all devices in list
                self.btnConnectCal.setText("Connect")
                self.calibratorStatus = 0 # disconnected


    # Connect camera #
    def cameraConnect(self):
        if self.cameraStatus == 0:
            selectedBaud = self.cmbBaudCam.currentText()
            selectedPort = self.cmbPortsCam.currentText()
            
            if selectedPort == "" or selectedBaud == "":
                self.errorWindow.show() # ERROR - unselected baud or port
            else: 
                index = self.portsDescription.index(selectedPort) # get name of that port ("COM3")
                report = self.cyclops.CyclopsOpenSerial(self.ports[index], selectedBaud)
                if report != True:
                    self.lblCamStatus.setText("Disconnected")
                    self.errorWindow.show() # ERROR - unselected baud or port
                else:
                    self.lblCamStatus.setText("Connected")
                    self.btnConnectCam.setText("Disconnect")
                    self.cameraStatus = 1
        else:
            report = self.cyclops.CyclopsCloseSerial()
            if report != None:
                self.lblCamStatus.setText("Connected")
                self.errorWindow.show() # ERROR - cant disconnect
            else:
                self.lblCamStatus.setText("Disconnected")
                self.btnConnectCam.setText("Connect")
                self.cmbPortsCam.clear() # clear all devices in list
                self.cameraStatus = 0 # disconnected


    # Set emisivity #
    def setEmisivityCamera(self):
        emisivity = self.dsbCameraEmisivity.value()
        response = self.cyclops.CyclopsEmissivitySet(emisivity)
        if response == "E34" or response == "":
            self.E34Window.show() # ERROR

    
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
        return response


    # Read temperature in monitor mode
    def recordMeas(self):
        if self.recording == 0:
            self.btnRecord.setText("Stop")
            self.cyclops.CyclopsMonitorModeSet()
            self.recording = 1
            # Function runs continiously and read data
            if self.recordThread is None or not self.recordThread.is_alive():
                self.recordThread = threading.Thread(target=self.Measure, args=(self.stopEvent,))
                self.recordThread.start() # start thread
            return None
        
        if self.recording == 1:
            self.btnRecord.setText("Start")
            self.cyclops.CyclopsCancleModeSet()
            self.recording = 0
            if self.recordThread is not None and self.recordThread.is_alive():
                self.stopEvent.set() # stop thread
                self.recordThread.join() 
            return None

    def Measure(self, output):
        while not self.stopEvent.is_set():
            # LPH 31.1
            val = self.cyclops.CyclopsReadSerial()
            val = float(val[3:])
            #print(val)
            self.lcdTemperature.display(val)


    # Read temperature in sample mode
    def sampleMeas(self):
        if self.sample == 0:
            self.measurements.clear() # clear measurements buffer
            self.times.clear() # clear times buffer
            if self.focus() != "OK!":
                self.sample = 0
                self.btnStartSample.setText("Start")
                self.timerSample.cancel()  # Stop the timer
            self.sampleTime = self.dsbSampleTime.value()
            self.sample = 1
            if self.cbTimerOnOff.isChecked() == True:
                hours = self.dsbTimerHours.value()
                minutes = self.dsbTimerMinutes.value()
                self.sampleNumber = hours * 3600 + minutes * 60 / self.sampleTime
            self.cyclops.CyclopsNormalModeSet()
            self.lblMode.setText("Normal")
            index = self.CameraMode.index("Normal")
            self.btnStartSample.setText("Stop")
            self.cmbCamMode.setCurrentIndex(index)
            self.RepeatFunctionSample(self.sampleTime, self.MeasureSample) # Call my_function every n seconds
            return None
        if self.sample == 1:
            self.sample = 0
            self.btnStartSample.setText("Start")
            self.timerSample.cancel()  # Stop the timer
            return None
        

    # Thread function to parallel measure values
    def RepeatFunctionSample(self, interval, function, *args, **kwargs):
        self.timerSample = threading.Timer(interval, self.RepeatFunctionSample, [interval, function] + list(args), kwargs)
        self.timerSample.start()
        function(*args, **kwargs)

    def MeasureSample(self):
        # LPH 31.1
        if self.cbTimerOnOff.isChecked() == True:
            if self.sampleNumber == 0:
                self.sample = 0
                self.btnStartSample.setText("Start")
                self.timerSample.cancel()  # Stop the timer
                return None
            else:
                self.sampleNumber -= 1

        val = self.cyclops.CyclopsGetTemp()
        if val == "":
            self.sample = 0
            self.btnStartSample.setText("Start")
            self.timerSample.cancel()  # Stop the timer
            self.errorWindow.show()
            return None

        val = float(val[3:]) # clean data
        #print(val)
        self.timerCounter += self.sampleTime
        self.measurements.append(val) # Add measurement to buffer
        self.times.append(self.timerCounter) # Add times to time buffer
        # Plot drawing
        self.graph.clear()
        self.graph.set_xlabel('Time [s]')
        self.graph.set_ylabel('Temp. [°C]')
        self.graph.plot(self.times, self.measurements, label='Temperature')
        self.graph.grid()
        self.graph.legend()
        self.canvas.draw()
        self.figure.tight_layout()

    
    # Read status data of cyclops cymera
    def readCameraData(self):
        response = self.cyclops.CyclopsStatusRead()
        if len(response) == 8:
            splitValue = list(response)
            if splitValue[0] == "C":
                self.lblUnits.setText("°C")
            elif splitValue[0] == "F":
                self.lblUnits.setText("°F")
            emisivity = int(splitValue[1] + splitValue[2] + splitValue[3] + splitValue[4])
            self.lblEmisivity.setText(str(emisivity))
            if splitValue[5] == "H":
                self.lblMeasurMode.setText("Manual")
            elif splitValue[5] == "M":
                self.lblMeasurMode.setText("Monitor")   
            if splitValue[6] == "A":
                self.lblMeasurMode.setText("AF")
            elif splitValue[6] == "M":
                self.lblMeasurMode.setText("MANU")    
            if splitValue[7] == "A":
                self.lblMeasurMode.setText("Over!")
            elif splitValue[7] == "N":
                self.lblMeasurMode.setText("In range")     
        else:
            self.E34Window.show() # ERROR


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
        self.cmbPortsCam.clear() # clear all devices in list
        self.cmbPorts.addItems(self.portsDescription) # add all new devices
        self.cmbPortsCam.addItems(self.portsDescription) # add all new devices
    

    # Save measurements to CSV file
    def exportCSV(self): # lists of times and measurement values
        filename = time.strftime("%Y_%m_%d-%H_%M-meritve")
        with open(str(filename) + '.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Time', 'Temp.'])
            for time_val, temp_val in zip(self.times, self.measurements):
                writer.writerow([time_val, temp_val]) 


    # Close application #
    def appExit(self):
        if self.timerSample and self.timerSample.is_alive():
            self.timerSample.cancel()  # Stop the timer
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
                self.mainWindow.cameraStatus = 1
                index = self.baudRate.index(str(selectedBaud))
                self.mainWindow.cmbBaudCam.setCurrentIndex(index)
                index = self.portsDescription.index(str(selectedPort))
                self.mainWindow.lblCamStatus.setText("Connected")
                self.mainWindow.btnConnectCam.setText("Disconnect")
                self.mainWindow.cmbPortsCam.setCurrentIndex(index)
                self.window.close()
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
        self.mainWindow.cmbPortsCam.clear() # clear all devices in list
        self.form.cmbPorts.addItems(self.portsDescription) # add all new devices
        self.mainWindow.cmbPortsCam.addItems(self.portsDescription) # add all new devices




        
