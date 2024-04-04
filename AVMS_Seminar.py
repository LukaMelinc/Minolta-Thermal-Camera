import serial
import serial.tools.list_ports
import time
import fluke

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    print("Available Serial Ports:")
    for port in ports:
        print(f"{port.device} - {port.description}")
    if not ports:
        print("No serial ports found!")
            

if __name__ == "__main__":

    fluke = fluke.Fluke()

    fluke.open_serial_fluke()
    fluke.FlukeRegisterReset()
    fluke.FlukeID()
