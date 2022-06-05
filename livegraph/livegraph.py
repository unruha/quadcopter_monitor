import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation

class LiveGraph:
    def __init__(self, root, ymin, ymax, col, row):
        self.xar = []
        self.yar = []
        self.latest_val = [0]
        self.count = -1
        for i in range(1, 1001):
            self.xar.append(i)
            self.yar.append(0)
        self.fig = plt.figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.set_ylim(ymin, ymax)
        self.ax.axes.xaxis.set_visible(False)
        self.line, = self.ax.plot(self.xar, self.yar)

        # create the canvas and start the animate loop
        self.potentiometer_canvas = FigureCanvasTkAgg(self.fig, root)
        self.potentiometer_canvas.get_tk_widget().grid(column=col, row=row)
        self.potentiometer_ani = animation.FuncAnimation(self.fig, self.animate, interval=50, blit=False)

    def animate(self, i):
        self.yar.append(int(self.latest_val[0]))
        self.yar = self.yar[-1000:]
        self.line.set_data(self.xar, self.yar)
