from PyQt5.QtWidgets import QLineEdit, QListWidgetItem,QGridLayout,QPushButton, QWidget, QListWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.colors
from random import choice as random_data
from PyQt5.QtGui import QFont

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
            layout.addWidget(self.canvas, 0, 1, 1, 2)
            font = {'weight': 'normal',
                    'size': 16}
            matplotlib.rc('font', **font)
            self.selected_id = random_data(range(len(self.data)))
            self.update_chart()

        super().__init__()
        self.data = data_list
        self.setWindowTitle('Histogram!')
        self.window_width, self.window_height = 1400, 800
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QGridLayout()
        self.setLayout(layout)
        insert_list_widget()

        self.threshold = QLineEdit()
        self.threshold.setText("300")
        layout.addWidget(self.threshold,1,1)
        self.button = QPushButton("Update")
        self.button.clicked.connect(self.update_chart)
        layout.addWidget(self.button, 1,2)
        insert_plot()

    def clicked(self):
        self.selected_id = self.listwidget.currentRow()
        self.update_chart()

    def update_chart(self):
        self.canvas.figure.clf()
        self.ax = self.canvas.figure.subplots()

        data = [x["time"] for x in self.data[self.selected_id]["leaderboard"]]
        adjusted = [x for x in data if 100*x/min(data) <= float(self.threshold.text())]

        self.ax.plot(adjusted)
        self.ax.invert_xaxis()
        self.ax.axhline(sum(adjusted) / len(adjusted),linestyle="--", color="darkblue", label="Mean")
        self.ax.axhline(min(adjusted),linestyle="--",label="WR", color="gold")
        self.ax.plot(0, min(adjusted),"o", color="gold")
        self.ax.axvline(len(adjusted)//2,linestyle="--", color="green", label="Median")
        if self.data[self.selected_id]["WR %"] * 100 <= float(self.threshold.text()):
            self.ax.plot(self.data[self.selected_id]["place"] -1, self.data[self.selected_id]["time"], "o", color="red", label="PB")
        self.ax.legend()
        self.ax.set_title(f'{self.data[self.selected_id]["game"]} - {self.data[self.selected_id]["category"]}')

        self.canvas.draw()


if __name__ == "__main__":
    from handler import window_handler, Mockery

    data = [Mockery(x) for x in range(20)]
    window_handler(data, Plot_app, debug=False)