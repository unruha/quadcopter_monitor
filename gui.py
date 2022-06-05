from tkinter import *
from readserial import SerialReader
from livegraph import LiveGraph
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import threading
import sys

arduino_port = "COM3"
baud = 9600
reader = SerialReader(arduino_port, baud)

root = Tk()

root.title("Quadcopter Monitor")
root.geometry("900x700")

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

# reads data in a separate thread and manipulates global variables that can be accessed by other functions
def read_data():
    global potentiometer_num, pwm_num
    while finished == False:
        data = reader.readLine()
        potentiometer_num[0] = data[0]
        pwm_num[0] = data[1]
        
data_feed = threading.Thread(target=read_data)
data_feed.start()

def live_update():
    potentiometer_value['text'] = potentiometer_num[0]
    pwm_value['text'] = pwm_num[0]
    root.after(1, live_update)

potentiometer_graph = LiveGraph()
pwm_graph = LiveGraph()

# runs when the X button is pressed on the window
# closes other threads and exits the process
def on_closing():
    root.destroy()
    global data_feed, finished
    finished = True
    data_feed.join()
    sys.exit()

live_update() # to start the update loop

potentiometer_canvas = FigureCanvasTkAgg(potentiometer_graph.fig, root)
potentiometer_canvas.get_tk_widget().grid(column=0, row=3)
potentiometer_ani = animation.FuncAnimation(potentiometer_graph.fig, potentiometer_graph.animate, fargs=(potentiometer_num, ), interval=50, blit=False)
pwm_canvas = FigureCanvasTkAgg(pwm_graph.fig, root)
pwm_canvas.get_tk_widget().grid(column=1, row=3)
pwm_ani = animation.FuncAnimation(pwm_graph.fig, pwm_graph.animate, fargs=(pwm_num, ), interval=50, blit=False)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
