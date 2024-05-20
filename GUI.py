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


###################################################################
########################## REPORT WINDOW ##########################
###################################################################

Ui_ReportWindow, BaseClass = uic.loadUiType("reportWindow.ui")

class ReportWindow(QMainWindow, Ui_ReportWindow):
    def __init__(self, parent=None):
        super(ReportWindow, self).__init__(parent)
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
        self.reportWindow = ReportWindow() # Succesfuly connected

        # Variables
        self.ports = []
        self.portsDescription = []
        self.baudRate = ["4800", "9600", "19200", "38400", "57600", "115200", "230400", "460800", "921600"]
        self.calibratorStatus = 0 # is connected or not
        self.cameraStatus = 0 # is connected or not
        self.recording = 0 # record button / monitor mode
        self.sample = 0 # automatic measurements
        self.calibration = 0 # state of calibration process
        self.CameraMode = ["Normal", "Average", "Peak", "Valley"]

        self.CalibratorProgNum = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.settleTest = ["AUTO", "LIMIT"]
        self.advance = ["PROMPT", "AUTO"]
        self.languages = ["ENGLISH", "FRENCH", "SPANISH", "ITALIAN" , "GERMAN", "RUSSIAN", "JAPANESE", "CHINESE"]
        self.languagesCode = ["ENGL", "FREN", "SPAN", "ITAL", "GERM", "RUSS", "JAP", "CHIN"]
        self.passwordProtection = ["HIGH", "LOW"]
        self.baudRateCal = ["1200", "2400", "4800", "9600", "19200", "38400"]
        self.wavelengt = ["8-14um", "Undefined"]

        self.measurements = [] # Buffer for collected measurements - Measurements buffer
        self.calibratorTemp = [] # Buffer for calibrator temperature
        self.times = [] # Buffer for measurements times - Time buffer
        self.sampleTime = 0
        self.timerCounter = 0
        self.sampleNumber = 0
        self.standardDeviation = [] # buffer for standard deviation measurements

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
        self.cmbBaudCal.addItems(self.baudRateCal)                         # BaudRate combo box - fluke
        self.cmbBaudCam.addItems(self.baudRate)                      # BaudRate combo box - cyclopse
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
        self.btnRecord.clicked.connect(self.recordMeas)                 # Record measurements
        self.btnStartSample.clicked.connect(self.sampleMeas)            # Start measuring - sample
        self.btnCameraStatusRead.clicked.connect(self.readCameraData)   # Read camera data
        self.cbTimerOnOff.stateChanged.connect(self.grayOut)            # Enable / disable sample timer
        self.btnConnectCam.clicked.connect(self.cameraConnect)          # Camera connect in main
        self.tabWidgetMeasure.currentChanged.connect(self.tabMainChange)# Read camera data with tab click
        self.tabFluke.currentChanged.connect(self.tabFlukeChange)       # Read fluke data with tab click
        self.btnSetIRT.clicked.connect(self.SetCalIRT)                  # Set calibrator emisivity
        self.btnSetCutout.clicked.connect(self.setCutout)               # Set calibrator cutout temperature
        self.btnSetScan.clicked.connect(self.setScan)                   # Set calibrator scan
        self.cmbSettle.addItems(self.settleTest)                        # set settle options
        self.cmbProgAdvance.addItems(self.advance)                      # program advance options
        self.cmbProgramNum.addItems(self.CalibratorProgNum)             # program number
        self.dsrSetProgStepNum.valueChanged.connect(self.setSteps)# read selected program 
        self.cmbLanguage.addItems(self.languages)                       # program language
        self.btnSaveDisplay.clicked.connect(self.saveLanguage)          # save language settings
        self.cbPeriod.stateChanged.connect(self.flipPeriod)             # select coma or period
        self.cbComa.stateChanged.connect(self.flipComa)                 # select coma or period 
        self.cmbSelectProfile.addItems(self.CalibratorProgNum)          # list programs in measure tab
        self.btnSetSetpoint.clicked.connect(self.setSetpoint)          # set calibrator setpoint
        self.btnSaveProgramOpt.clicked.connect(self.saveProgOprions)    # save language settings
        self.btnSaveProgramEdit.clicked.connect(self.saveProgEdit)      # save language settings
        self.cmbProtection.addItems(self.passwordProtection)            # password enable
        self.cmbBaudCalChange.addItems(self.baudRateCal)                # calibrator baud rate
        self.cmbWavelenght.addItems(self.wavelengt)                     # calibrator baud rate
        self.btnReadINFO.clicked.connect(self.calibratorInfo)           # save language settings
        self.cmbProgramNum.currentIndexChanged.connect(self.readCalProgram) # read selected program
        self.cmbSelectProfile.currentIndexChanged.connect(self.selectProfile) # read selected program
        self.btnAdvanceNext.clicked.connect(self.fluke.FlukeProgPromAdvSet) # save language settings
        self.btnStartCalibration.clicked.connect(self.startCalibration) # save language settings
        self.btnStopHeating.clicked.connect(self.stopHeater)            # turn off heater
        self.btnExportCalibration.clicked.connect(self.exportCSV)       # turn off heater


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
        if response != "":
            self.lblMode.setText(selectedMode)
        else:
            self.E34Window.show()


    # Grying out widgets #
    def grayOut(self):
        self.dsbUpperAlarm.setEnabled(self.cbUpperAlarm.isChecked())
        self.dsbLowerAlarm.setEnabled(self.cbLowerAlarm.isChecked())
        self.dsbTimerHours.setEnabled(self.cbTimerOnOff.isChecked())
        self.dsbTimerMinutes.setEnabled(self.cbTimerOnOff.isChecked())

    
    def tabMainChange(self, index):
        # Main tab widget
        if index == 0: # Measure tab
            #if self.calibratorStatus == 1:
            return None
            #if self.cameraStatus == 1:
            #    self.readCameraData()
                #self.readCameraInfo()

        if index == 1: # Camera tab
            if self.cameraStatus == 1:
                self.readCameraData()
                self.alarmRead()
                
        if index == 2: # Calibrator tab
            self.tabFlukeChange(0)


    def tabFlukeChange(self, index):
        # Fluke tab widget
        if self.calibratorStatus == 1:
            if index == 0: # TEMP SETUP
                response = self.fluke.FlukeSourRateRead() # scan rate
                self.dsbScanRate.setValue(float(response))
                response = self.fluke.FlukeSourStabLimRead() # stable limit
                self.dsbStabLimit.setValue(float(response))
                response = self.fluke.FlukeSourStabBeepRead() # alarm beep
                self.cbStableAlarm.setChecked(int(response))
                response = self.fluke.FlukeSourEmisRead() # emisivity
                self.dsrSetIRT.setValue(float(response))
                response = self.fluke.FlukeSourProtScutLevRead() # soft cutout
                print(response)
                if response == "": response = 0
                self.dsbSoftCutout.setValue(float(response))
                response = self.fluke.FlukeSourProtHcutRead() # hard cutout
                self.lblHardCutout.setText(response)
            if index == 1: # PROG MENU
                response = self.fluke.FlukeProgOptSettRead() # settle test
                self.cmbSettle.setCurrentIndex(int(response))
                response = self.fluke.FlukeProgOptSoakRead() # soak time in minutes
                self.dsrSoakTime.setValue(float(response))
                response = self.fluke.FlukeProgOptAdvRead() # advance
                self.cmbProgAdvance.setCurrentIndex(int(response))
                response = self.fluke.FlukeProgOptCyclRead() # cycles
                self.dsrCyclesNo.setValue(int(response))
                self.readCalProgram() # Read selected program

            if index == 2: # SYSTEM MENU
                self.readSystemMenu()

            if index == 3: # VIEW TEMP
                val = self.fluke.FlukeSourSensDataRead()
                self.lcBlockTemperature.display(float(val))


    def saveProgOprions(self):
        # settle test
        val = self.cmbSettle.currentText() 
        if val == "AUTO":
            self.fluke.FlukeProgOptSettSet(0)
        elif val == "LIMIT":
            self.fluke.FlukeProgOptSettSet(1)
        
        # soak time in minutes
        val = self.dsrSoakTime.value() 
        self.fluke.FlukeProgOptSoakSet(val) 
        
        # Advance
        val = self.cmbProgAdvance.currentText() 
        if val == "PROMPT":
            self.fluke.FlukeProgOptAdvSet(0)
        elif val == "AUTO":
            self.fluke.FlukeProgOptAdvSet(1)

        # cycles
        val = self.dsrCyclesNo.value() 
        self.fluke.FlukeProgOptCyclSet(val) 
        

    # Read selected program parameter         
    def readCalProgram(self):
        # select program by number
        selectedProg = self.cmbProgramNum.currentText()
        #self.fluke.FlukeProgSelRead(int(selectedProg))
        name = self.fluke.FlukeProgNameRead(selectedProg)
        name = name.replace('"', '') # delete "" in name
        self.lblProgName.setText(name)
        self.lblProgNum.setText(selectedProg)
        self.leProgName.setText(name)
        val = self.fluke.FlukeProgParParRead(int(selectedProg), "IRTE")
        if val == "": val = 0
        self.dsrSetProgIRT.setValue(float(val))
        val = self.fluke.FlukeProgParParRead(int(selectedProg), "DIST")
        if val == "": val = 0
        self.dsrSetProgDistance.setValue(float(val))
        val = self.fluke.FlukeProgParParRead(int(selectedProg), "APER")
        self.cbProgAperture.setChecked(bool(val))
        steps = self.fluke.FlukeProgParParRead(int(selectedProg), "POIN")
        if steps == "" or steps == 0: 
            steps = 1
        else:
            steps = int(steps)

        self.dsrSetProgStepNum.setValue(steps)

        for i in range(8):
            if i < steps:
                enable = 1
            else:
                enable = 0
            if i == 0: self.dsrSP1.setEnabled(enable)
            if i == 1: self.dsrSP2.setEnabled(enable)
            if i == 2: self.dsrSP3.setEnabled(enable)
            if i == 3: self.dsrSP4.setEnabled(enable)
            if i == 4: self.dsrSP5.setEnabled(enable)
            if i == 5: self.dsrSP6.setEnabled(enable)
            if i == 6: self.dsrSP7.setEnabled(enable)
            if i == 7: self.dsrSP8.setEnabled(enable)

        for i in range(8):
            if i < steps:
                command = "SPO" + str(i + 1)
                val = self.fluke.FlukeProgParParRead(int(selectedProg), command)
                print("return", val)
                val = float(val)
            else:
                val = 0
            if i == 0: self.dsrSP1.setValue(val)
            if i == 1: self.dsrSP2.setValue(val)
            if i == 2: self.dsrSP3.setValue(val)
            if i == 3: self.dsrSP4.setValue(val)
            if i == 4: self.dsrSP5.setValue(val)
            if i == 5: self.dsrSP6.setValue(val)
            if i == 6: self.dsrSP7.setValue(val)
            if i == 7: self.dsrSP8.setValue(val)
            #time.sleep(0.05)

    def setSteps(self):
        steps = self.dsrSetProgStepNum.value()
        if steps == "" or steps == 0: 
            steps = 1
        else:
            steps = int(steps)

        for i in range(8):
            if i < steps:
                enable = 1
            else:
                enable = 0
            if i == 0: self.dsrSP1.setEnabled(enable)
            if i == 1: self.dsrSP2.setEnabled(enable)
            if i == 2: self.dsrSP3.setEnabled(enable)
            if i == 3: self.dsrSP4.setEnabled(enable)
            if i == 4: self.dsrSP5.setEnabled(enable)
            if i == 5: self.dsrSP6.setEnabled(enable)
            if i == 6: self.dsrSP7.setEnabled(enable)
            if i == 7: self.dsrSP8.setEnabled(enable)
                
    
    # Save selected program parameters
    def saveProgEdit(self):
        # select program by number
        selectedProg = self.cmbProgramNum.currentText()
        name = self.leProgName.text()
        self.fluke.FlukeProgNameSet(int(selectedProg), name)
        val = self.dsrSetProgIRT.value()
        self.fluke.FlukeProgParParSet(int(selectedProg), "IRTE", val)
        val = self.dsrSetProgDistance.value()
        self.fluke.FlukeProgParParSet(int(selectedProg), "DIST", val)
        val = self.cbProgAperture.isChecked()
        if val == True: 
            val = 1
        else:
            val = 0
        self.fluke.FlukeProgParParSet(int(selectedProg), "APER", val)
        steps = self.dsrSetProgStepNum.value()
        self.fluke.FlukeProgParParSet(int(selectedProg), "POIN", steps)
        for i in range(int(steps)):
            if i == 0: val = self.dsrSP1.value()
            if i == 1: val = self.dsrSP2.value()
            if i == 2: val = self.dsrSP3.value()
            if i == 3: val = self.dsrSP4.value()
            if i == 4: val = self.dsrSP5.value()
            if i == 5: val = self.dsrSP6.value()
            if i == 6: val = self.dsrSP7.value()
            if i == 7: val = self.dsrSP8.value()
            command = "SPO" + str(i + 1)
            val = self.fluke.FlukeProgParParSet(int(selectedProg), str(command), val)
            time.sleep(0.05)
        self.reportWindow.show()
        self.reportWindow.lblReport.setText("Successful")


    # Read all the data to show in system menu
    def readSystemMenu(self):
        code = self.fluke.FlukeSystLangRead() # language
        self.cmbLanguage.setCurrentIndex(int(self.languagesCode.index(code)))
        val = self.fluke.FlukeSystDecFormRead() # period / coma
        if val == "0":
            self.cbPeriod.setChecked(1)
            self.cbComa.setChecked(0)
        elif val == "1":
            self.cbPeriod.setChecked(0)
            self.cbComa.setChecked(1)
        val = self.fluke.FlukeSystBeepKeybRead() # keyboard sound
        self.cbAudioOnOff.setChecked(int(val))
        code = self.fluke.serialport.baudrate
        print("code",code)
        self.cmbBaudCalChange.setCurrentIndex(int(self.baudRateCal.index(str(code)))) # baud rate
        val = self.fluke.FlukeSystCommSerLinRead() # line feed
        self.cbLinefeed.setChecked(int(val))

        val = self.fluke.FlukeSourCalParxRead(1) # read IRCAL1
        self.dsrIRCAL1.setValue(float(val))
        val = self.fluke.FlukeSourCalParxRead(2) # read IRCAL2
        self.dsrIRCAL2.setValue(float(val))
        val = self.fluke.FlukeSourCalParxRead(3) # read IRCAL2
        self.dsrIRCAL3.setValue(float(val))

        val = self.fluke.FlukeSourLconPbanRead() # PID - P
        self.dsrPID_P.setValue(float(val))
        val = self.fluke.FlukeSourLconIntRead() # PID - I
        self.dsrPID_I.setValue(float(val))
        val = self.fluke.FlukeSourLconDerRead() # PID - D
        self.dsrPID_D.setValue(float(val))

        val = self.fluke.FlukeSourCalWavRead() # wavelenght
        self.cmbWavelenght.setCurrentIndex(int(val))


        


    # set soft cutout temperature - PROTECTED WITH PASSWORD
    def saveLanguage(self):
        language = self.cmbLanguage.currentText()
        code = self.languagesCode[self.languages.index(language)]
        self.fluke.FlukeSystLangSet(code)
        if self.cbPeriod.isChecked() == 1:
            self.fluke.FlukeSystDecFormSet(0)
        else:
            self.fluke.FlukeSystDecFormSet(1)

        if self.cbAudioOnOff.isChecked() == 1:
            self.fluke.FlukeSystBeepKeybSet(1)
        else:
            self.fluke.FlukeSystBeepKeybSet(0)

    

    # Set scan parameters
    def setScan(self):
        self.fluke.FlukeSourRateSet(self.dsbScanRate.value())
        self.fluke.FlukeSourStabLimSet(self.dsbStabLimit.value())
        self.fluke.FlukeSourStabBeepSet(self.cbStableAlarm.isChecked())

    
    # Flip check box for . and ,
    def flipComa(self):
            self.cbPeriod.setChecked(not self.cbComa.isChecked())

    def flipPeriod(self):
            self.cbComa.setChecked(not self.cbPeriod.isChecked())
            

    
    # list calibrator info
    def calibratorInfo(self):
        id = self.fluke.FlukeID() # model
        self.lblModel.setText(id[:10])
        self.lblSerial.setText(id[11:]) # serial
        date = self.fluke.FlukeSourCalDateRead() # calib. data
        self.lblCalDate.setText(date)
        fw = self.fluke.FlukeSystCodVersRead() # fw version
        self.lblFWVer.setText(fw)


    # select profile for calibration in main window
    def selectProfile(self):
        selectedProg = self.cmbSelectProfile.currentText()
        name = self.fluke.FlukeProgNameRead(int(selectedProg))
        name = name.replace('"', '') # delete "" in name
        self.lblProgNameMeasurePage.setText(name)
        #response = self.fluke.FlukeProgOptAdvRead() # advance
        #if response == "0":
        #    self.btnAdvanceNext.setEnabled(1)
        #else:
        #    self.btnAdvanceNext.setEnabled(0)

    
    # start calibration profile    
    def startCalibration(self):
        if self.calibration == 0:
            if self.sample == 1:
                self.sampleMeas() # stop sampling event
                self.sampleMeas() # start sampling event
            else:
                self.sampleMeas() # start sampling event
                self.btnStartCalibration.setText("Stop")
                self.calibration = 1
                # start calibrator
                selectedProg = self.cmbSelectProfile.currentText()
                self.fluke.FlukeProgSelSet(int(selectedProg))
                self.fluke.FlukeProgStatSet(1)
        else:
            self.fluke.FlukeProgStatSet(0)
            self.sampleMeas()
            self.btnStartCalibration.setText("Start")


    # turn on the calibrator
    def setSetpoint(self):
        # FlukeOutpStatRead
        # FlukeOutpData
        val = self.dsbSetpoint.value()
        self.fluke.FlukeSourSpoSet(val)
        self.fluke.FlukeOutpStatSet(1)

    
    # turn off calibrator
    def stopHeater(self):
        self.fluke.FlukeOutpStatSet(0)


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
        
        response = self.cyclops.CyclopsAlarmSet(upperAlarm, upperTemp, lowerAlarm, lowerTemp, soundAlarm)
        if response != "OK!":
            self.E34Window.show()


    # Connect fluke calibrator #
    def calibratorConnect(self):
        if self.calibratorStatus == 0:
            selectedBaud = self.cmbBaudCal.currentText()
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
                    self.btnConnectCal.setText("Disconnect")
                    self.calibratorStatus = 1
                    self.fluke.FlukeRegisterReset()
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
        #print(response)
        if response == "E34" or response == "":
            self.E34Window.show() # ERROR
            return None

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
            if self.recordThread is not None and self.recordThread.is_alive():
                self.stopEvent.set() # stop thread
                self.recordThread.join() 
            self.cyclops.CyclopsCancleModeSet()
            self.recording = 0
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
        self.timerCounter += self.sampleTime
        self.measurements.append(val) # Add measurement to buffer
        self.standardDeviation.append(val) # add measurement to standard deviation buffer
        self.times.append(self.timerCounter) # Add times to time buffer

        # Read fluke temp
        val = self.fluke.FlukeOutpStatRead()
        val = float(val)
        self.dsbSetpoint.setValue(val)
        self.calibratorTemp.append(val)
        # time is the same as camera

        # calculate standard deviation
        if len(self.standardDeviation) == 10:
            val = 0
            maxVal = max(self.standardDeviation)
            minVal = min(self.standardDeviation)
            delta = maxVal- minVal
            if delta < 2:
                # Add std calculation
                val = np.std(self.standardDeviation)
                self.lcdStandardDeviation.display(val)
                self.standardDeviation.clear() # clear all saved measurements
            else:
                self.lcdStandardDeviation.display(0)
                self.standardDeviation.clear() # clear all saved measurements

        # fluke temp e=0.95 (last widget)
        val = self.fluke.FlukeSourSensDataRead()
        self.lcBlockTemperature.display(float(val))
        
        # Plot drawing
        self.graph.clear()
        self.graph.set_xlabel('Time [s]')
        self.graph.set_ylabel('Temp. [°C]')
        self.graph.plot(self.times, self.measurements, label='Camera', color = 'Red')
        self.graph.plot(self.times, self.calibratorTemp, label='Calibrator', color = 'Blue')
        self.graph.grid()
        self.graph.legend()
        self.canvas.draw()
        self.figure.tight_layout()

        # Detect if the calibrator needs advance command
        val = self.fluke.FlukeProgPromStatRead()
        if val == '0':
            self.btnAdvanceNext.setEnabled(0)
        else:
            self.btnAdvanceNext.setEnabled(1)




    
    # Read status data of cyclops cymera
    def readCameraData(self):
        response = self.cyclops.CyclopsStatusRead()
        if len(response) == 8:
            splitValue = list(response)
            if splitValue[0] == "C":
                self.lblUnits.setText("°C")
            elif splitValue[0] == "F":
                self.lblUnits.setText("°F")
            emisivity = splitValue[1] + splitValue[2] + splitValue[3] + splitValue[4]
            self.lblEmisivity.setText(emisivity)
            self.dsbCameraEmisivity.setValue(float(emisivity))
            if splitValue[5] == "H":
                self.lblMeasurMode.setText("Manual")
            elif splitValue[5] == "M":
                self.lblMeasurMode.setText("Monitor")   
            if splitValue[6] == "A":
                self.lblFocusMode.setText("AF")
            elif splitValue[6] == "M":
                self.lblFocusMode.setText("MANU")    
            """    
            if splitValue[7] == "A":
                self.lblMeasurMode.setText("Over!")
            elif splitValue[7] == "N":
                self.lblMeasurMode.setText("In range")  """   
            self.readCameraInfo()
        else:
            self.E34Window.show() # ERROR


    # data returned by each function
    def readCameraInfo(self):
        response = self.cyclops.CyclopsCancleModeSet()
        #print(response)
        if len(response) == 8:
            splitValue = list(response)

            if splitValue[0] == "L":
                self.lblUnits.setText("°C")
            elif splitValue[0] == "F":
                self.lblUnits.setText("°F")

            if splitValue[1] == "N":
                self.lblMeasurMode.setText("Normal")
                self.lblMode.setText("Normal")
                self.lblAlarmStatus.setText("Normal") 
            elif splitValue[1] == "P":
                self.lblMeasurMode.setText("Peak") 
                self.lblMode.setText("Peak")   
                self.lblAlarmStatus.setText("Peak") 
            elif splitValue[1] == "G":
                self.lblMeasurMode.setText("Average") 
                self.lblMode.setText("Average") 
                self.lblAlarmStatus.setText("Average") 
            elif splitValue[1] == "V":
                self.lblMeasurMode.setText("Valley") 
                self.lblMode.setText("Valley") 
                self.lblAlarmStatus.setText("Valley") 
            elif splitValue[1] == "A":
                self.lblAlarmStatus.setText("Over!") 
            elif splitValue[1] == "O":
                self.lblAlarmStatus.setText("Over MAX!") 
            elif splitValue[1] == "U":
                self.lblAlarmStatus.setText("Under MIN!") 
            else:
                self.lblAlarmStatus.setText("OK!")

            if splitValue[2] == "C":
                self.lblState.setText("Monitor")
            elif splitValue[2] == "H":
                self.lblState.setText("Hold")   
            else:
                self.lblState.setText("Idle") 
        else:
            self.E34Window.show() # ERROR


    # Set fluke emisivity
    def SetCalIRT(self):
        self.fluke.FlukeSourEmisSet(self.dsrSetIRT.value())


    # Set fluke cutout temperature
    def setCutout(self):
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
        #self.mainWindow.show() # BRIŠI
        
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




        
