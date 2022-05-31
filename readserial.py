import serial

arduino_port = "COM3"
baud = 9600
reader = serial.Serial(arduino_port, baud)

while True:
    line = str(reader.readline())
    data = line[2:][:-5]
    print(data)
