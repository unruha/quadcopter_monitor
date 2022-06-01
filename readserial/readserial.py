import serial

class SerialReader:
    def __init__(self, port, baud):
        self.port = port
        self.baud = baud
        try:
            self.reader = serial.Serial(self.port, self.baud)
        except:
            print("ERROR: Unable to connect to serial port")
        
    # readLine
    # returns a list of data items on the line
    def readLine(self):
        data = str(self.reader.readline())[2:][:-5]
        return data.split(" ")
