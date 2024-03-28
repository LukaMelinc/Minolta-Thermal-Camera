import serial
import serial.tools.list_ports
import time

ser = serial.Serial(port="COM3", baudrate=4800, bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_TWO, xonxoff=False, rtscts=True, dsrdtr=False, timeout=1)
#ser.is_open()

sendData = 'AF \r'
ser.write(sendData.encode('ascii'))
time.sleep(0.5)
data = ser.readline().decode().strip()
print(data)

ser.close()