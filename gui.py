from tkinter import *
from readserial import SerialReader
from livegraph import LiveGraph
import threading
import sys

arduino_port = "COM3"
baud = 9600
reader = SerialReader(arduino_port, baud)

root = Tk()

root.title("Quadcopter Monitor")
#getting screen width and height of display
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
#setting tkinter window size
root.geometry("%dx%d" % (width, height))

potentiometer_label = Label(root, text="Potentiometer Value:", font=("Helvetica", 18, "bold"))
pwm_label = Label(root, text="PWM Value:", font=("Helvetica", 18, "bold"))
potentiometer_value = Label(root, text="", font=("Helvetica", 16))
pwm_value = Label(root, text="", font=("Helvetica", 16))

potentiometer_label.grid(
    row=1,
    column=0, 
    padx=(30, 30), 
    pady=(10,10)
)
pwm_label.grid(
    row=1,
    column=1,
    padx=(30, 30),
    pady=(10,10)
)
potentiometer_value.grid(
    row=2,
    column=0
)
pwm_value.grid(
    row=2,
    column=1
)

potentiometer_num = [0]
pwm_num = [0]
finished = False

potentiometer_graph = LiveGraph(root, 0, 1023, 0, 3)
pwm_graph = LiveGraph(root, 0, 2000, 1, 3)

# reads data in a separate thread and manipulates global variables that can be accessed by other functions
def read_data():
    global potentiometer_num, pwm_num
    while finished == False:
        data = reader.readLine()
        potentiometer_graph.latest_val[0] = data[0]
        potentiometer_num[0] = data[0]
        pwm_graph.latest_val[0] = data[1]
        pwm_num[0] = data[1]
        
data_feed = threading.Thread(target=read_data)
data_feed.start()

def live_update():
    potentiometer_value['text'] = potentiometer_num[0]
    pwm_value['text'] = pwm_num[0]
    root.after(1, live_update)

# runs when the X button is pressed on the window
# closes other threads and exits the process
def on_closing():
    root.destroy()
    global data_feed, finished
    finished = True
    data_feed.join()
    sys.exit()

live_update() # to start the update loop

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
