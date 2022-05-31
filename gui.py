from tkinter import *
import serial

arduino_port = "COM3"
baud = 9600
reader = serial.Serial(arduino_port, baud)

root = Tk()

root.title("Quadcopter Monitor")
root.geometry("600x500")

potentiometer_label = Label(root, text="Potentiometer Value:", font="Helvetica 18 bold")
pwm_label = Label(root, text="PWM Value:", font="Helvetica 18 bold")
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

def live_update():
    line = str(reader.readline())
    data = line[2:][:-5]
    potentiometer_value["text"] = data.split(" ")[0]
    pwm_value["text"] = data.split(" ")[1]
    root.after(1, live_update)

root.after(1, live_update)

root.mainloop()
