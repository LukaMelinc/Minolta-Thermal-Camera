import serial
import serial.tools.list_ports
import time

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    print("Available Serial Ports:")
    for port in ports:
        print(f"{port.device} - {port.description}")
    if not ports:
        print("No serial ports found!")

def open_serial_port(port, baudrate):
    try:
        ser = serial.Serial(port="COM3", baudrate=baudrate, bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_TWO, xonxoff=False, rtscts=True, dsrdtr=False, timeout=1)
        print(f"Opened {port} at {baudrate} baudrate.")
        return ser
    except serial.SerialException as e:
        print(f"Error opening serial port {port}: {e}")
        return None
    
def main():
    #list_serial_ports()
    port = "COM3" #input("Enter the port name (e.g., COM3, /dev/ttyUSB0): ")
    baudrate = 4800 #int(input("Enter baud rate (e.g., 9600): "))
    
    ser = open_serial_port(port, baudrate)

    if ser.is_open == True:
        try:

            while True:
                data_to_send = input("Enter data to send (type 'exit' to close): ")
                print(f"Sending:", {data_to_send})
                if data_to_send.lower() == 'exit':
                    break

                data = data_to_send + ' \r'
                ser.write(data.encode('ascii'))
                time.sleep(0.05)
                response = ser.readline().decode().strip()
                print(f"Received: {response}")

        finally:
            ser.close()
            print("Serial port closed.")

if __name__ == "__main__":
    main()
