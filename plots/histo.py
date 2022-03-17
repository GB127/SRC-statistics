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


    def update_chart(self, y):
        def update_x():
            if "time" in y:
                time_str = lambda x : f'{x//3600:>3}:{int(x) % 3600 // 60:02}:{int(x) % 3600 % 60 % 60:02}'
                self.ax.set_xticklabels([time_str(float(x.get_text().replace("−", "-"))) for x in self.ax.get_xticklabels()])
                self.canvas.draw()
            elif "%" in y:
                self.ax.set_xticklabels([f'{float(x.get_text().replace("−", "-")):.2%}' for x in self.ax.get_xticklabels()])
                self.canvas.draw()

        self.canvas.figure.clf()
        self.ax = self.canvas.figure.subplots()
        self.ax.hist([x[y] for x in self.data])
        self.canvas.draw()
        self.ax.set_title(y)
        self.ax.set_ylabel("Frequency")
        self.ax.set_xlabel(y)
        update_x()
