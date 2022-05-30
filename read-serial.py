import serial

arduino_port = "COM3"
baud = 9600

ser = serial.Serial(arduino_port, baud)
print("Connected to Arduino port: " + arduino_port)

while True:
    line = str(ser.readline())
    data = line[2:][:-5]
    print(data)
