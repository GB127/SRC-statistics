from PyQt5.QtWidgets import (   QListWidgetItem,    QGridLayout, 
                                QWidget,            QListWidget)
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib  # TODO : remove this



class Base_app(QWidget):
    def list_widget(self):
        self.listwidget = QListWidget()
        self.listwidget.setFixedWidth(450)
        for entry in self.data:
            one_line = QListWidgetItem(str(entry))
            one_line.setFont(QFont("Lucida Sans Typewriter", 10))
            self.listwidget.addItem(one_line)
        self.listwidget.clicked.connect(self.list_clicked)
        return self.listwidget

    def list_clicked(self):
        self.selected_id = self.listwidget.currentRow()
        print(self.data[self.selected_id])
    
    def __init__(self, data_list):
        super().__init__()
        self.data = data_list
        self.setMinimumSize(1400, 800)

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.list_widget(), 0,0,0,1)
        self.layout.addWidget(self.plot_widget(), 0, 1, 1, 2)  # TODO

    def plot_widget(self):
        self.canvas = FigureCanvas(plt.Figure(tight_layout=True))
        matplotlib.rc('font', **{'weight': 'normal',
                                    'size': 16})
        self.update_plot(list=0,
                        filter="game",
                        number="time")
        return self.canvas

    def update_plot(self, **kargs):
        raise NotImplementedError("This function is defined in childs only")