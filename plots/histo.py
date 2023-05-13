from statistics import quantiles
from numpy import arange
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QListWidgetItem,
    QComboBox,
    QDoubleSpinBox,
    QGridLayout,
    QWidget,
    QSpinBox,
    QListWidget,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
import matplotlib.pyplot as plt
from code_SRC.composantes import Time


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
    #           #########################################
    #           #  Filter  #   Granularity # Outliners  #
    #           #  Box     #      number   #  factors   #
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
                for x in self.data[0].keys():
                    if isinstance(self.data[0][x], (int, float, Time)):
                        clés.append(x)
                return clés

            self.options = QComboBox()
            self.options.addItems(filters())
            self.options.currentTextChanged.connect(self.update_plot)
            return self.options

        def trim_power_widget():
            self.trim_power = QDoubleSpinBox()
            self.trim_power.setMinimum(0.1)
            self.trim_power.setValue(1.0)
            self.trim_power.setSingleStep(0.1)

            self.trim_power.valueChanged.connect(self.update_plot)
            return self.trim_power

        def granularity_widget():
            self.granularity = QSpinBox()
            self.granularity.setMinimum(2)
            self.granularity.setValue(10)
            self.granularity.valueChanged.connect(self.update_plot)
            return self.granularity

        super().__init__()
        self.data = data_list
        self.setMinimumSize(1400, 800)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(list_widget(), 0, 0, 0, 1)
        self.layout.addWidget(plot_x_selection(), 1, 1)
        self.layout.addWidget(granularity_widget(), 1, 2)
        self.layout.addWidget(trim_power_widget(), 1, 3)

        self.layout.addWidget(plot_widget(), 0, 1, 1, 3)

    def update_plot(self):
        def trim_data(to_trim):
            if isinstance(to_trim[0], Time):
                to_trim = [float(x) for x in to_trim]
            if len(set(to_trim)) == 1:  # pragma: no cover
                return to_trim
            IQ1, IQ2, IQ3 = quantiles(to_trim)
            IQR = (IQ3 - IQ1) * self.trim_power.value()
            trimmed = [x for x in to_trim if (IQ1 - IQR) < x < (IQ3 + IQR)]
            return trimmed

        def labels():
            self.ax.set_title(
                f"{self.data[0].__class__.__name__} - {str(self.options.currentText())}"
            )
            self.ax.set_xlabel(str(self.options.currentText()))
            self.ax.set_ylabel("Frequency")

        def set_xticks():
            if len(set(to_plot)) == 1:  # pragma: no cover
                return

            self.ax.set_xticks(
                arange(min(to_plot), max(to_plot), (max(to_plot) - min(to_plot)) / 5)[
                    1:
                ]
            )

            if str(self.options.currentText()) in ["time", "delta"]:
                time_str = (
                    lambda x: f"{int(x//3600):>3}:{int(x) % 3600 // 60:02}:{int(x) % 3600 % 60 % 60:02}"
                )
                self.ax.set_xticklabels(
                    [time_str(float(x)) for x in self.ax.get_xticks()],
                    horizontalalignment="center",
                )

            elif str(self.options.currentText()) in ["perc", "perc_lb"]:
                perc_str = lambda x: f"{x:.1%}"
                self.ax.set_xticklabels(
                    [perc_str(float(x)) for x in self.ax.get_xticks()],
                    horizontalalignment="center",
                )
            elif str(self.options.currentText()) in ["place", "leaderboard"]:
                self.ax.set_xticklabels(
                    [int(x) for x in self.ax.get_xticks()], horizontalalignment="center"
                )
            else:
                raise KeyError(
                    f"{str(self.options.currentText())} is not assigned to an approach in histogram."
                )  # pragma: no cover
            self.ax.set_xlim([min(to_plot), max(to_plot)])

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

        def update_data_list_color():
            for index, data in enumerate(self.data):
                test = self.listwidget.item(index)
                test.setBackground(QColor(142, 250, 171))
                if str(self.options.currentText()) in ["time", "delta"]:
                    if float(data[str(self.options.currentText())]) not in to_plot:
                        test.setBackground(QColor(252, 154, 149))
                elif data[str(self.options.currentText())] not in to_plot:
                    test.setBackground(QColor(252, 154, 149))

        self.canvas.figure.clf()
        self.ax = self.canvas.figure.subplots()

        to_plot = trim_data([x[str(self.options.currentText())] for x in self.data])
        update_data_list_color()

        self.ax.hist(
            to_plot, range=(min(to_plot), max(to_plot)), bins=self.granularity.value()
        )
        self.ax.grid(visible=True, axis="x")
        labels()
        set_xticks()
        set_yticks()
