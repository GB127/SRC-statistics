from PyQt5.QtWidgets import QPushButton
from plots.base import Base_app
from numpy import arange


class Histo_app(Base_app):
    def plot_inter_widgets(self):

        self.keys = []  # Look if I need self
        for x, value in self.data[0].items():
            if isinstance(value, (int, float)): 
                self.keys.append(x)

        buttons = []
        for x in self.keys:
            dropbox = QPushButton(x)
            dropbox.clicked.connect(lambda checked, a=x : self.update_plot(number=a))
            buttons.append(dropbox)
        return buttons

    def update_plot(self, **kargs):
        to_plot = [x[kargs["number"]] for x in self.data]
        self.canvas.figure.clf()
        self.ax = self.canvas.figure.subplots()

        def labels():
            self.ax.set_title(f'{self.data[0].__class__.__name__} - {"time"}')
            self.ax.set_xlabel(kargs["number"])
            self.ax.set_ylabel("Frequency")
            self.ax.hist(to_plot, range=(min(to_plot), max(to_plot)))

            self.canvas.draw()


        def set_xticks():
            self.ax.set_xticks(arange(
                                    min(to_plot),
                                    max(to_plot),
                                    (max(to_plot)-min(to_plot))/5
                                    )[1:])
            #self.ax.set_yticks(range(0, int(max(self.ax.get_yticks())+1), int(max(self.ax.get_yticks()) // 14 + 1))[1:-1])

            self.canvas.draw()

            self.ax.set_xlim([min(to_plot), max(to_plot)])
            
            
            if kargs["number"] in ["time"]:
                time_str = lambda x : f'{int(x//3600):>3}:{int(x) % 3600 // 60:02}:{int(x) % 3600 % 60 % 60:02}'
                self.ax.set_xticklabels([time_str(float(x)) for x in self.ax.get_xticks()], horizontalalignment="center")

            elif kargs["number"] in ["WR %"]:
                perc_str = lambda x : f'{x:.1%}'
                self.ax.set_xticklabels([perc_str(float(x)) for x in self.ax.get_xticks()], horizontalalignment="center")





        labels()
        set_xticks()
        self.canvas.draw()