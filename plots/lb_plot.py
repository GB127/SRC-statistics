import warnings
from statistics import mean, median, geometric_mean as geomean
from PyQt5.QtGui import QFont 
from PyQt5.QtWidgets import (QHBoxLayout,
    QListWidgetItem, QCheckBox,
    QGridLayout,
    QWidget, QComboBox,
    QListWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
import matplotlib.pyplot as plt
from code_SRC.composantes import Time
from datetime import date


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
    # S  G  W M # # Plot selection # Metrics to display # 
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
            current_ranking = self.data[date.today().year]
            for rank, entry in enumerate(current_ranking, start=1):
                delta = Time(entry - current_ranking[0])
                string = f'{rank:4} {Time(entry)} + {delta} ({entry / current_ranking[0]:.2%})'

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

        def plot_selection()->QComboBox:
            """Fetches the buttons that will change the filters of the pie charts
            Returns:
                List: QtPushButtons
            """
            self.filter = QComboBox()
            self.filter.addItems(["Current LB", "LB Evolution", "Metrics Evo"])
            self.filter.currentTextChanged.connect(self.update_plot)
            return self.filter

        def metrics_selection():
            mini_layout = QHBoxLayout()
            self.WR = QCheckBox("WR")
            self.WR.setChecked(True)
            self.WR.stateChanged.connect(self.update_plot)
            mini_layout.addWidget(self.WR)
            self.moy = QCheckBox("Moy")
            self.moy.setChecked(True)
            self.moy.stateChanged.connect(self.update_plot)
            mini_layout.addWidget(self.moy)
            self.geo = QCheckBox("Geo")
            self.geo.setChecked(True)
            self.geo.stateChanged.connect(self.update_plot)
            mini_layout.addWidget(self.geo)
            self.med = QCheckBox("Med")
            self.med.setChecked(True)
            self.med.stateChanged.connect(self.update_plot)
            mini_layout.addWidget(self.med)

            return mini_layout


        super().__init__()
        self.data = data_dict
        self.setMinimumSize(1400, 600)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(list_widget(), 0, 0)
        self.layout.addLayout(metrics_selection(), 1,0)
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



    def metrics_bools(self):
        return (self.WR.isChecked(), self.moy.isChecked(), self.geo.isChecked(), self.med.isChecked())

    def plot_metrics_evolution(self):
        self.canvas.figure.clf()
        self.ax = self.canvas.figure.subplots()

        WR_evo = [x[0] for x in self.data.values()]
        mean_evo = [mean(x) for x in self.data.values()]
        geomean_evo = [geomean(x) for x in self.data.values()]
        median_evo = [median(x) for x in self.data.values()]
        plotted = []

        for name, toplot, booly in zip(["WR","Mean", "GeoMean", "Median"], [WR_evo, mean_evo, geomean_evo, median_evo], self.metrics_bools()):
            if booly:
                self.ax.plot(self.data.keys(),toplot, label=name)
                plotted.append(toplot)

        self.ax.legend()#loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=4)
        self.ax.set_yticks(self.ax.get_yticks())
        self.ax.set_yticklabels([str(Time(x)) for x in self.ax.get_yticks()])
        # FIXME : Use map
        if len(plotted) > 1:
            self.ax.set_ylim(top=1.005 * max([max(x) for x in  plotted]),
                                    bottom=0.995 * min([min(x) for x in plotted])
            )
        self.canvas.draw()

    def plot_current(self):
        self.canvas.figure.clf()
        self.ax = self.canvas.figure.subplots()
        current_ranking = self.data[date.today().year]

        x_label = [x for x in range(1, len(current_ranking) +1)]

        self.ax.plot(x_label,current_ranking)
        self.ax.invert_xaxis()
        self.ax.set_yticks(self.ax.get_yticks())
        self.ax.set_yticklabels([str(Time(x)) for x in self.ax.get_yticks()])
        self.ax.set_ylim(top=current_ranking[-1],
                            bottom=current_ranking[0])
        self.ax.set_xlim(left=len(x_label), right=1)


        self.canvas.draw()

    def update_plot(self):
        [self.plot_current, self.plot_evolution, self.plot_metrics_evolution][self.filter.currentIndex()]()