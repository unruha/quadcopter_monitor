import matplotlib.pyplot as plt

class LiveGraph:
    def __init__(self):
        self.xar = []
        self.yar = []
        self.count = -1
        for i in range(1, 1001):
            self.xar.append(i)
            self.yar.append(0)
        self.fig = plt.figure(figsize=(8, 5), dpi=100)
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.set_ylim(0, 1023)
        self.ax.axes.xaxis.set_visible(False)
        self.line, = self.ax.plot(self.xar, self.yar)

    def animate(self, i, potentiometer_num):
        self.yar.append(int(potentiometer_num[0]))
        self.yar = self.yar[-1000:]
        self.line.set_data(self.xar, self.yar)
