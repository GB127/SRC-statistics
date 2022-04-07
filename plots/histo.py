from PyQt5.QtWidgets import QPushButton
from plots.base import Base_app


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
        filter = kargs["number"]
        to_plot = [x[filter] for x in self.data]
        def generic():
            self.canvas.figure.clf()
            self.ax = self.canvas.figure.subplots()
            self.ax.set_title(f'{self.data[0].__class__.__name__} - {filter}')
            self.ax.set_xlabel(filter)
            self.ax.set_ylabel("Frequency")


        def filter_time():
            time_str = lambda x : f'{int(x//3600):>3}:{int(x) % 3600 // 60:02}:{int(x) % 3600 % 60 % 60:02}'

            self.ax.hist(to_plot, range=(min(to_plot), max(to_plot)))
            self.canvas.draw()
            self.ax.set_xticks(self.ax.get_xticks())  # Noise code to remove a warning from matplotlib

            self.ax.set_xlim([min(to_plot), max(to_plot)])
            self.ax.set_xticklabels([time_str(float(x.get_text().replace("−", "-"))) for x in self.ax.get_xticklabels()], rotation=17)#, horizontalalignment="right")
            self.canvas.draw()

        def filter_place():
            self.ax.hist(to_plot, range=(min(to_plot), max(to_plot)))
            self.ax.set_xticks(self.ax.get_xticks())  # Noise code to remove a warning from matplotlib

            self.canvas.draw()

            self.ax.set_xlim([min(to_plot), max(to_plot)])
            self.ax.set_xticklabels([int(float((x.get_text().replace("−", "-")))) for x in self.ax.get_xticklabels()])
            self.canvas.draw()

        def filter_perc():
            self.ax.hist(to_plot, range=(max(min(to_plot), 1), max(to_plot)))
            self.ax.set_xticks(self.ax.get_xticks())  # Noise code to remove a warning from matplotlib

            self.canvas.draw()
            self.ax.set_xlim([max(min(to_plot), 1), max(to_plot)])
            self.ax.set_xticklabels([f'{float(x.get_text().replace("−", "-")):.1%}' for x in self.ax.get_xticklabels()])
            self.canvas.draw()

        filtering = {"time":filter_time, "place":filter_place, "WR %" : filter_perc, "WR time":filter_time, "delta WR":filter_time}

        generic()
        filtering[filter]()