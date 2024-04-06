import serial
import serial.tools.list_ports
import time
import fluke
import cyclops

# List all available serial ports
def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    print("Available Serial Ports:")
    for port in ports:
        print(f"{port.device} - {port.description}")
    if not ports:
        print("No serial ports found!")


if __name__ == "__main__":

    # Declare classes #
    fluke = fluke.Fluke()
    cyclops = cyclops.Cyclops()

    # Open serial communication with devices #
    fluke.FlukeOpenSerial("COM5", 9600)
    cyclops.CyclopsOpenSerial("COM3", 4800)




    cyclops.CyclopsGetTemp()
