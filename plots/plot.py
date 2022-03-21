from PyQt5.QtWidgets import QListWidgetItem,QGridLayout,QPushButton, QWidget, QListWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.colors
from random import choice as random_data
from copy import copy
from PyQt5.QtGui import QFont, QColor

class Plot_app(QWidget):
    def __init__(self, data_list):
        def insert_list_widget():
            self.listwidget = QListWidget()
            self.listwidget.setFixedWidth(450)
            for entry in data_list:
                one_line = QListWidgetItem(str(entry))
                one_line.setFont(QFont("Lucida Sans Typewriter", 10))
                self.listwidget.addItem(one_line)
            self.listwidget.clicked.connect(self.clicked)
            layout.addWidget(self.listwidget, 0, 0, 0, 1)

        def insert_plot():
            self.canvas = FigureCanvas(plt.Figure(tight_layout=True))
            layout.addWidget(self.canvas, 0, 1, 1, len(self.keys))
            font = {'weight': 'normal',
                    'size': 16}
            matplotlib.rc('font', **font)
            self.update_chart(random_data(range(len(self.data))))

        def fetch_valid_keys():
            self.keys = []
            for x, value in data_list[0].__dict__.items():
                if x == "leaderboard":continue
                elif isinstance(value, (int, float)):
                    self.keys.append(x)

        super().__init__()
        fetch_valid_keys()
        self.data = sorted(data_list, key=lambda x:x["place"])
        self.setWindowTitle('Histogram!')
        self.window_width, self.window_height = 1400, 800
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QGridLayout()
        self.setLayout(layout)
        insert_list_widget()
        insert_plot()

    def clicked(self):
        selected_pb = self.listwidget.currentItem().text
        selected_id = self.listwidget.currentRow()
        self.update_chart(selected_id)

    def update_chart(self, selection):
        self.canvas.figure.clf()
        self.ax = self.canvas.figure.subplots()
        self.ax.plot([x["time"] for x in self.data[selection]["leaderboard"]])
        self.ax.invert_xaxis()
        self.ax.axhline(sum([x["time"] for x in self.data[selection]["leaderboard"]]) / len([x["time"] for x in self.data[selection]["leaderboard"]]),linestyle="--", color="red")

        self.ax.plot(len([x["time"] for x in self.data[selection]["leaderboard"]])//2,[x["time"] for x in self.data[selection]["leaderboard"]][len([x["time"] for x in self.data[selection]["leaderboard"]])//2],"o", color="green")

        self.canvas.draw()


if __name__ == "__main__":
    from handler import window_handler, Mockery

    data = [Mockery(x) for x in range(20)]
    window_handler(data, Plot_app)