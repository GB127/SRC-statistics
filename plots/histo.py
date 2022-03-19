from PyQt5.QtWidgets import QListWidgetItem,QGridLayout,QPushButton, QWidget, QListWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib
from random import choice as random_key
from PyQt5.QtGui import QFont

class Histo_app(QWidget):
    def __init__(self, data_list):
        def create_list_widget():
            self.listwidget = QListWidget()
            self.listwidget.setFixedWidth(450)
            self.listwidget.alternatingRowColors()
            for entry in data_list:
                one_line = QListWidgetItem(str(entry))
                #one_line.setFont(QFont("Courier New", 10))
                one_line.setFont(QFont("Lucida Sans Typewriter", 10))
                self.listwidget.addItem(one_line)
            self.listwidget.clicked.connect(self.clicked)
            layout.addWidget(self.listwidget, 0, 0, 0,1)

        def insert_buttons():
            self.buttons = []
            for numéro, x in enumerate(self.keys):
                dropbox = QPushButton(x)
                dropbox.clicked.connect(lambda checked, a=x : self.update_chart(a))
                self.buttons.append(dropbox)
                layout.addWidget(dropbox, 1,1+numéro)


        def insert_plot():
            self.canvas = FigureCanvas(plt.Figure(tight_layout=True))
            layout.addWidget(self.canvas, 0, 1, 1, len(self.keys))
            font = {'weight': 'normal',
                    'size': 16}
            matplotlib.rc('font', **font)
            self.update_chart(random_key(self.keys))


        def fetch_valid_keys():
            self.keys = []
            for x, value in data_list[0].__dict__.items():
                if isinstance(value, (int, float)): self.keys.append(x)


        super().__init__()
        fetch_valid_keys()
        self.data = data_list
        self.setWindowTitle('Histogram!')
        self.window_width, self.window_height = 1400, 800
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QGridLayout()
        self.setLayout(layout)
        create_list_widget()
        insert_plot()
        insert_buttons()

    def clicked(self):
        item = self.listwidget.currentItem()
        print(item.text())


    def update_chart(self, filter):
        to_plot = [x[filter] for x in self.data]
        def generic():
            self.canvas.figure.clf()
            self.ax = self.canvas.figure.subplots()
            self.ax.set_title(f'{self.data[0].__class__.__name__} - {filter}')
            self.ax.set_xlabel(filter)
            self.ax.set_ylabel("Frequency")


        def filter_time():
            time_str = lambda x : f'{x//3600:>3}:{int(x) % 3600 // 60:02}:{int(x) % 3600 % 60 % 60:02}'

            self.ax.hist(to_plot, range=(min(to_plot), max(to_plot)))
            self.canvas.draw()
            self.ax.set_xticks(self.ax.get_xticks())  # Noise code to remove a warning from matplotlib

            self.ax.set_xlim([min(to_plot), max(to_plot)])
            #self.ax.set_xticklabels([time_str(float(x.get_text().replace("−", "-"))) for x in self.ax.get_xticklabels()])
            self.ax.set_xticklabels([float(x.get_text().replace("−", "-")) for x in self.ax.get_xticklabels()])
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

        filtering = {"time":filter_time, "place":filter_place, "WR %" : filter_perc, "WR time":filter_time}

        generic()
        filtering[filter]()