from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QColor
import matplotlib
import matplotlib.colors
from copy import copy
from plots.base import Base_app


class Pie_app(Base_app):
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
    
    def plot_inter_widgets(self)->list:
        """Fetches the buttons that will change the filters of the pie charts
            Returns:
                List: QtPushButtons
            """
        clés = []
        for x, value in self.data[0].items():
            if x in ["category", "subcat", "leaderboard"]:
                continue
            elif not isinstance(value, (int, float)):
                clés.append(x)

        buttons = []
        for x in clés:
            dropbox = QPushButton(x)
            dropbox.clicked.connect(lambda checked, a=x: self.update_plot(filter=a))
            buttons.append(dropbox)
        return buttons

    def update_plot(self, **kargs):
        filter = kargs["filter"]

        def count_data():
            count = {}
            for x in self.data:
                count[x[filter]] = count.get(x[filter], 0) + 1
            for x in copy(count):
                if count[x] / sum(count.values()) < 0.05:  # pragma: no cover
                    count["autres"] = (
                        count.get("autres", 0) + count[x]
                    )  # pragma: no cover
                    del count[x]  # pragma: no cover
            return count

        self.canvas.figure.clf()
        self.ax = self.canvas.figure.subplots()
        tempo = self.ax.pie(
            count_data().values(),
            labels=count_data().keys(),
            startangle=90,
            autopct="%1.1f%%",
        )

        légende_couleurs = {}
        for texte, couleur in zip(tempo[1], tempo[0]):
            légende_couleurs[texte.get_text()] = matplotlib.colors.to_hex(
                couleur.get_facecolor()
            )

        for index, data in enumerate(self.data):
            test = self.listwidget.item(index)
            if data[filter] in légende_couleurs:
                test.setBackground(QColor(légende_couleurs[data[filter]]))
            elif not data[filter]:
                continue  # pragma: no cover
            else:
                test.setBackground(
                    QColor(légende_couleurs["autres"])
                )  # pragma: no cover

        self.ax.set_title(f"{self.data[0].__class__.__name__}s - {filter}")
        self.canvas.draw()
