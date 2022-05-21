from PyQt5.QtWidgets import (
    QListWidgetItem,
    QGridLayout,
    QWidget,
    QComboBox,
    QListWidget)
from PyQt5.QtGui import QFont, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
import matplotlib.pyplot as plt
from code_SRC.composantes import Time
from copy import copy
from collections import Counter


class Pie_app(QWidget):
    """Pie app that shows a pie chart of all the datas provided.
    The datas on the pie is for datas that aren't numbers.

    #####################################################
    #           #                                       #
    #           #                                       #
    #           #                                       #
    #           #                                       #
    #           #                 PIE                   #
    #   DATA    #                CHART                  #
    #   LIST    #                                       #
    #           #                                       #
    #           #                                       #
    #           #                                       #
    #           #                                       #
    #           #########################################
    #           #               FILTERS                 #
    #           #               BUTTONS                 #
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

        def plot_filters()->list:
            """Fetches the buttons that will change the filters of the pie charts
            Returns:
                List: QtPushButtons
            """

            def filters():
                clés = []
                for x in self.data[0].keys():
                    if x in ["subcat", "leaderboard"]:
                        continue
                    elif not isinstance(self.data[0][x], (int, float, Time)):
                        clés.append(x)
                return clés

            self.filter = QComboBox()
            self.filter.addItems(filters())
            self.filter.currentTextChanged.connect(self.update_plot)
            return self.filter

        def pie_sommation():
            def filters():
                clés = []
                for x in self.data[0].keys():
                    if x in ["perc", "perc_lb"]:
                        continue
                    elif isinstance(self.data[0][x], (int, float, Time)):
                        clés.append(x)
                return clés

            self.options = QComboBox()
            self.options.addItems(["count"] + filters())
            self.options.currentTextChanged.connect(self.update_plot)
            return self.options

        super().__init__()
        self.data = data_list
        self.setMinimumSize(1400, 800)
        self.current_filter = "game"  # FIXME : This is a temporary fix
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(list_widget(), 0, 0,0,1)
        self.layout.addWidget(pie_sommation(), 1, 1)
        self.layout.addWidget(plot_filters(), 1,2)
        self.layout.addWidget(plot_widget(), 0, 1, 1,2)  # TODO

    def update_plot(self):
        filter = str(self.filter.currentText())
        # raise BaseException(plt.rcParams['axes.prop_cycle'].by_key()['color'])
        def count_data():
            def initial_count():
                count = {}
                for x in self.data:
                    if str(self.options.currentText()) == "count":
                        value = 1
                    elif str(self.options.currentText()) in ["time", "delta"]:
                        value = x[str(self.options.currentText())].seconds
                    if isinstance(x[filter], set):
                        for serie in x[filter]:
                            count[serie] = count.get(serie, 0) + value
                    else:
                        count[x[filter]] = count.get(x[filter], 0) + value
                return count
                


            def remove_small(count):
                for x in copy(count):
                    if count[x] / sum(count.values()) < 0.05:  # pragma: no cover
                        count["others"] = (
                            count.get("others", 0) + count[x]
                        )  # pragma: no cover
                        del count[x]  # pragma: no cover
                return count

            return remove_small(initial_count())

        def update_listwidget():
            if filter in ["series"]: return  #FIXME
            def color_legend():
                légende_couleurs = {}
                for texte, couleur in zip(graphique_data[1], graphique_data[0]):
                    légende_couleurs[texte.get_text()] = matplotlib.colors.to_hex(
                        couleur.get_facecolor()
                    )
                return légende_couleurs

            for index, data in enumerate(self.data):
                test = self.listwidget.item(index)
                if data[filter] in color_legend():
                    test.setBackground(QColor(color_legend()[data[filter]]))
                elif not data[filter]:
                    continue  # pragma: no cover
                else:
                    test.setBackground(
                        QColor(color_legend()["others"])
                    )  # pragma: no cover

        self.canvas.figure.clf()
        self.ax = self.canvas.figure.subplots()
        graphique_data = self.ax.pie(
                                        count_data().values(),
                                        labels=count_data().keys(),
                                        startangle=90,
                                        autopct="%1.1f%%",
                                    )
        update_listwidget()

        #raise BaseException(dir(graphique_data[1][0]))
        if any([len(x.get_text())>=15 for x in graphique_data[1]]):
            self.canvas.figure.clf()
            self.ax = self.canvas.figure.subplots()

            self.ax.pie(
                                        count_data().values(),
                                        startangle=90,
                                        autopct="%1.1f%%",
                                        labels = [x[:15] for x in count_data().keys()]
                                    )
            self.canvas.draw()
            #raise BaseException("OOoh")
        # for x in graphique_data[1]])


        self.ax.set_title(f"{self.data[0].__class__.__name__}s - {filter}")
        self.canvas.draw()
