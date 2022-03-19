from PyQt5.QtWidgets import QListWidgetItem,QGridLayout,QPushButton, QWidget, QListWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.colors
from random import choice as random_key
from copy import copy
from PyQt5.QtGui import QFont, QColor

class Pie_app(QWidget):
    def __init__(self, data_list):
        def insert_list_widget():
            self.listwidget = QListWidget()
            self.listwidget.setFixedWidth(450)
            for entry in data_list:
                one_line = QListWidgetItem(str(entry))
                one_line.setFont(QFont("Lucida Sans Typewriter", 10))
                self.listwidget.addItem(one_line)
            self.listwidget.clicked.connect(self.clicked)
            layout.addWidget(self.listwidget, 0, 0, 0,1)

        def insert_buttons_widget():
            for numéro, x in enumerate(self.keys):
                dropbox = QPushButton(x)
                dropbox.clicked.connect(lambda checked, a=x : self.update_chart(a))
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
                if x == "leaderboard":continue
                elif not isinstance(value, (int, float)):
                    self.keys.append(x)

        super().__init__()
        fetch_valid_keys()
        self.data = data_list
        self.setWindowTitle('Histogram!')
        self.window_width, self.window_height = 1400, 800
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QGridLayout()
        self.setLayout(layout)
        insert_list_widget()
        insert_plot()
        insert_buttons_widget()

    def clicked(self):
        item = self.listwidget.currentItem()
        print(item.text())


    def update_chart(self, y):
        def count_data():
            count = {}
            for x in self.data:
                count[x[y]] = count.get(x[y], 0) + 1
            for x in copy(count):
                if count[x] / sum(count.values()) < 0.05:  # pragma: no cover
                    count["autres"] = count.get("autres", 0) + count[x]# pragma: no cover
                    del count[x]# pragma: no cover
            return count
        self.canvas.figure.clf()
        self.ax = self.canvas.figure.subplots()
        tempo = self.ax.pie(count_data().values(),labels=count_data().keys(), startangle=90, autopct='%1.1f%%')

        légende_couleurs = {}
        for texte, couleur in zip(tempo[1], tempo[0]):
            légende_couleurs[texte.get_text()] = matplotlib.colors.to_hex(couleur.get_facecolor())

        for index, data in enumerate(self.data):
            test = self.listwidget.item(index)
            if data[y] in légende_couleurs:
                test.setBackground(QColor(légende_couleurs[data[y]]))
            elif not data[y]: continue# pragma: no cover
            else:# pragma: no cover
                test.setBackground(QColor(légende_couleurs["autres"])) # pragma: no cover

        self.ax.set_title(f"{self.data[0].__class__.__name__}s - {y}")
        self.canvas.draw()
