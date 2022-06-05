from tkinter import *
from readserial import SerialReader
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

potentiometer_num = 0
pwm_num = 0
finished = False

# reads data in a separate thread and manipulates global variables that can be accessed by other functions
def read_data():
    global potentiometer_num, pwm_num
    while finished == False:
        data = reader.readLine()
        potentiometer_num = data[0]
        pwm_num = data[1]
        
data_feed = threading.Thread(target=read_data)
data_feed.start()

def live_update():
    global potentiometer_num, pwm_num
    potentiometer_value['text'] = potentiometer_num
    pwm_value['text'] = pwm_num
    root.after(1, live_update)

xar = []
yar = []
for i in range(1, 1001):
    xar.append(i)
    yar.append(0)
fig = plt.figure(figsize=(8, 5), dpi=100)
ax = fig.add_subplot(1, 1, 1)
ax.set_ylim(0, 1023)
ax.axes.xaxis.set_visible(False)
line, = ax.plot(xar, yar)
count = -1

def animate(i):
    global count, yar, xar, potentiometer_num, line
    if count < 1000:
        count = count + 1
    yar.append(int(potentiometer_num))
    yar = yar[-count:]
    line.set_data(xar[-count:], yar)

# runs when the X button is pressed on the window
# closes other threads and exits the process
def on_closing():
    root.destroy()
    global data_feed, finished
    finished = True
    data_feed.join()
    sys.exit()

live_update() # to start the update loop

plotcanvas = FigureCanvasTkAgg(fig, root)
plotcanvas.get_tk_widget().grid(column=0, row=3)
ani = animation.FuncAnimation(fig, animate, interval=50, blit=False)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
