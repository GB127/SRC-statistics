import warnings
from statistics import mean, median, geometric_mean as geomean
from PyQt5.QtGui import QFont 
from PyQt5.QtWidgets import (
    QListWidgetItem,
    QGridLayout,
    QWidget, QComboBox,
    QListWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
import matplotlib.pyplot as plt
from code_SRC.composantes import Time


class LB_plot_app(QWidget):
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
    #             # Plot selection # Metrics to display # 
    #####################################################
    """

    def __init__(self, data_dict:dict):
        """
            Args:
                data_dict (dict): {YEAR (int) : RANKING(list[ints])}
                """
        def list_widget() -> QListWidget:
            self.listwidget = QListWidget()
            self.listwidget.setFixedWidth(450)
            for entry in self.data[2022]:
                warnings.warn("Need to change this so it's always the current year. But it will work until 31st December.")
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

        def plot_selection()->QComboBox:
            """Fetches the buttons that will change the filters of the pie charts
            Returns:
                List: QtPushButtons
            """
            self.filter = QComboBox()
            self.filter.addItems(["Current LB", "LB Evolution", "Metrics Evo"])
            self.filter.currentTextChanged.connect(self.update_plot)
            return self.filter




        super().__init__()
        self.data = data_dict
        self.setMinimumSize(1400, 800)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(list_widget(), 0, 0, 0, 1)
        self.layout.addWidget(plot_selection(),1,1)
        self.layout.addWidget(plot_widget(), 0, 1, 1, 3)




    def plot_evolution(self):
        self.canvas.figure.clf()
        self.ax = self.canvas.figure.subplots()

        for year, lb in self.data.items():
            self.ax.plot([x for x in range(1, len(lb) + 1)],lb, label=year)
        self.ax.invert_xaxis()
        self.ax.legend()

        self.ax.set_yticks(self.ax.get_yticks())
        self.ax.set_yticklabels([str(Time(x)) for x in self.ax.get_yticks()])
        self.ax.set_ylim(top=max(x[-1] for x in self.data.values()),
                            bottom=min(x[0] for x in self.data.values()))
        self.ax.set_xlim(right=1)
        self.canvas.draw()

    def plot_metrics_evolution(self):
        self.canvas.figure.clf()
        self.ax = self.canvas.figure.subplots()

        WR_evo = [x[0] for x in self.data.values()]
        mean_evo = [mean(x) for x in self.data.values()]
        geomean_evo = [geomean(x) for x in self.data.values()]
        median_evo = [median(x) for x in self.data.values()]

        for name, toplot in zip(["WR","Mean", "GeoMean", "Median"], [WR_evo, mean_evo, geomean_evo, median_evo]):
            self.ax.plot(self.data.keys(),toplot, label=name)

        self.ax.legend()
        self.ax.set_yticks(self.ax.get_yticks())
        self.ax.set_yticklabels([str(Time(x)) for x in self.ax.get_yticks()])
        # FIXME : Use map
        self.ax.set_ylim(top=1.01 * max([max(x) for x in  [WR_evo, mean_evo, geomean_evo, median_evo]]),
                                bottom=0.99 * min([min(x) for x in  [WR_evo, mean_evo, geomean_evo, median_evo]])
        )
        self.canvas.draw()

    def plot_current(self):
        self.canvas.figure.clf()
        self.ax = self.canvas.figure.subplots()
        x_label = [x for x in range(1, len(self.data[2022]) +1)]

        self.ax.plot(x_label,self.data[2022])
        self.ax.invert_xaxis()
        self.ax.set_yticks(self.ax.get_yticks())
        self.ax.set_yticklabels([str(Time(x)) for x in self.ax.get_yticks()])
        self.ax.set_ylim(top=self.data[2022][-1],
                            bottom=self.data[2022][0])
        self.ax.set_xlim(left=len(x_label), right=1)


        self.canvas.draw()

    def update_plot(self):
        [self.plot_current, self.plot_evolution, self.plot_metrics_evolution][self.filter.currentIndex()]()