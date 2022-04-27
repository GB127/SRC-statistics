from statistics import quantiles
from PyQt5.QtWidgets import QPushButton
from matplotlib.pyplot import axes
from numpy import arange
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QListWidgetItem,
    QGridLayout,
    QWidget,
    QListWidget,
    QPushButton,
)

from PyQt5.QtGui import QFont, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
import matplotlib.pyplot as plt
from copy import copy


class Histo_app(QWidget):
    """Histo app that shows a Histo chart of all the datas provided.
    The datas on the histo is for datas that are numbers.

    #####################################################
    #           #                                       #
    #           #                                       #
    #           #                                       #
    #           #                                       #
    #           #               Histo                   #
    #   DATA    #               CHART                   #
    #   LIST    #                                       #
    #           #                                       #
    #           #                                       #
    #           #                                       #
    #           #                                       #
    #####################################################
    #  +     +  #               FILTERS                 #
    #  -     -  #               BUTTONS                 #
    #####################################################
    """

    def __init__(self, data_list):
        def list_widget() -> QListWidget:
            self.listwidget = QListWidget()
            self.listwidget.setFixedWidth(450)
            for entry in self.data:
                one_line = QListWidgetItem(str(entry))
                one_line.setFont(QFont("Lucida Sans Typewriter", 10))
                self.listwidget.addItem(one_line)
            # self.listwidget.clicked.connect(self.list_clicked)
            return self.listwidget

        def plot_widget() -> FigureCanvas:
            self.canvas = FigureCanvas(plt.Figure(tight_layout=True))
            matplotlib.rc("font", **{"weight": "normal", "size": 16})
            self.update_plot()
            return self.canvas

        def plot_x_selection() -> list:
            """Fetches the buttons that will change the filters of the pie charts
            Returns:
                List: QtPushButtons
            """
            def filters():
                clés = []
                for x, value in self.data[0].items():
                    if isinstance(value, (int, float)):
                        clés.append(x)
                return clés

            def update_valeur(new_filter):
                self.current_parameter = new_filter
                self.update_plot()

            self.keys = []  # Look if I need self
            for x, value in self.data[0].items():
                if isinstance(value, (int, float)):
                    self.keys.append(x)

            buttons = []
            for x in filters():
                dropbox = QPushButton(x)
                dropbox.clicked.connect(lambda checked, a=x: update_valeur(a))
                buttons.append(dropbox)
            return buttons

        super().__init__()
        self.data = data_list
        self.setMinimumSize(1400, 800)
        self.current_parameter = "time"  # FIXME : This is a temporary fix
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(list_widget(), 0, 0, 0, 1)
        self.layout.addWidget(plot_widget(), 0, 1, 1, len(plot_x_selection()))

        for numéro, wid in enumerate(plot_x_selection(), start=1):
            self.layout.addWidget(wid, 1, numéro)

    def update_plot(self):
        def trim_data(to_trim):
            quantilles = quantiles(to_trim)
            IQ1 = quantilles[0]
            IQ3 = quantilles[2]
            IQR = IQ3 - IQ1
            trimmed = [x for x in to_trim if IQ1 - IQR < x < (IQ3 + IQR)]
            if len(trimmed) != len(to_trim):
                trimmed = trim_data(trimmed)
            return trimmed
        
        def labels():
            self.ax.set_title(f'{self.data[0].__class__.__name__} - {self.current_parameter}')
            self.ax.set_xlabel(self.current_parameter)
            self.ax.set_ylabel("Frequency")

        def set_xticks():
            if len(set(to_plot)) == 1:
                return

            self.ax.set_xticks(
                arange(min(to_plot), max(to_plot), (max(to_plot) - min(to_plot)) / 5)[
                    1:
                ]
            )
            self.ax.set_xlim([min(to_plot), max(to_plot)])

            if self.current_parameter in ["time", "delta WR", "WR time"]:
                time_str = (
                    lambda x: f"{int(x//3600):>3}:{int(x) % 3600 // 60:02}:{int(x) % 3600 % 60 % 60:02}"
                )
                self.ax.set_xticklabels(
                    [time_str(float(x)) for x in self.ax.get_xticks()],
                    horizontalalignment="center",
                )

            elif self.current_parameter in ["WR %", "LB %"]:
                perc_str = lambda x: f"{x:.1%}"
                self.ax.set_xticklabels(
                    [perc_str(float(x)) for x in self.ax.get_xticks()],
                    horizontalalignment="center",
                )
            elif self.current_parameter in ["place"]:
                self.ax.set_xticklabels(
                    [int(x) for x in self.ax.get_xticks()], horizontalalignment="center"
                )
            else:
                raise KeyError(
                    f'{self.current_parameter} is not assigned.'
                )  # pragma: no cover
            self.canvas.draw()

        def set_yticks():
            self.ax.set_yticks(
                [
                    x
                    for x in range(
                        0,
                        int(max(self.ax.get_yticks()) + 1),
                        int(max(self.ax.get_yticks()) + 1) // 14 + 1,
                    )
                ][1:]
            )
            self.canvas.draw()

        self.canvas.figure.clf()
        self.ax = self.canvas.figure.subplots()

        to_plot = [x[self.current_parameter] for x in self.data]
        if len(set(to_plot)) > 1:
            to_plot = trim_data([x[self.current_parameter] for x in self.data])

        for index, data in enumerate(self.data):
            test = self.listwidget.item(index)
            test.setBackground(QColor(142, 250, 171))
            if data[self.current_parameter] not in to_plot:
                test.setBackground(QColor(252, 154, 149))

        self.ax.hist(to_plot, range=(min(to_plot), max(to_plot)))
        self.ax.grid(visible=True, axis="x")
        labels()
        set_xticks()
        set_yticks()
