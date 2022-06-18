from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QListWidgetItem,
    QCheckBox,
    QGridLayout,
    QWidget,
    QComboBox,
    QListWidget,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
import matplotlib.pyplot as plt
from code_SRC.composantes import Time
from datetime import date


class Save_plot_app(QWidget):
    """Plot app that shows a plot chart of a specific leaderboard.

    #####################################################
    #           #                                       #
    #           #                                       #
    #           #                                       #
    #           #                                       #
    #           #               Plot                    #
    #   DATA    #               CHART                   #
    #   LIST    #                                       #
    #           #                                       #
    #           #                                       #
    #           #                                       #
    #           #                                       #
    #####################################################
    """

    def __init__(self, data):
        def list_widget() -> QListWidget:
            self.listwidget = QListWidget()
            self.listwidget.setFixedWidth(450)
            for rank, entry in enumerate(runs_times, start=1):
                delta = Time(entry - runs_times[0])
                string = f"{rank:4} {Time(entry)} {str(delta):>10} (-{(runs_times[0] - entry) / runs_times[0]:>6.2%})"

                one_line = QListWidgetItem(string)
                one_line.setFont(QFont("Lucida Sans Typewriter", 10))
                self.listwidget.addItem(one_line)
            # self.listwidget.clicked.connect(self.list_clicked)
            return self.listwidget

        def plot_widget() -> FigureCanvas:
            self.canvas = FigureCanvas(plt.Figure(tight_layout=True))
            matplotlib.rc("font", **{"weight": "normal", "size": 16})
            self.update_plot()
            return self.canvas

        runs_times, pb, WR_time = data

        super().__init__()
        self.data = runs_times
        self.pb = pb.seconds
        self.WR = WR_time
        self.setMinimumSize(1400, 600)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(list_widget(), 0, 0)
        self.layout.addWidget(plot_widget(), 0, 1)

    def plot(self):
        self.canvas.figure.clf()
        self.ax = self.canvas.figure.subplots()

        self.ax.plot([x for x in range(1, len(self.data) + 1)], self.data)
        self.ax.axhline(self.WR, color="goldenrod")
        self.ax.set_yticks(self.ax.get_yticks())
        self.ax.set_yticklabels([str(Time(x)) for x in self.ax.get_yticks()])
        self.canvas.draw()

    def update_plot(self):
        self.plot()