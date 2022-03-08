import sys
from PyQt5.QtWidgets import QGridLayout,QPushButton, QApplication,QComboBox, QWidget, QHBoxLayout, QVBoxLayout, QListWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib
import random

class Histo_app(QWidget):
    def __init__(self, data_list):
        def create_list_widget():
            self.listwidget = QListWidget()
            self.listwidget.setFixedWidth(300)
            for index, entry in enumerate(data_list):
                self.listwidget.insertItem(index, str(entry))
            self.listwidget.clicked.connect(self.clicked)
            layout.addWidget(self.listwidget, 0, 0, 0,1)

        def insert_buttons():
            for numéro, x in enumerate(data_list[0].keys()):
                print(numéro, x)
                dropbox = QPushButton(x)
                dropbox.clicked.connect(lambda checked, a=x : self.update_chart(a))
                layout.addWidget(dropbox, 1,1+numéro)


        def insert_plot():
            self.canvas = FigureCanvas(plt.Figure(figsize=(15, 6)))
            layout.addWidget(self.canvas, 0,1, 0, 1+ len(data_list[0].keys()))
            font = {'weight': 'normal',
                    'size': 16}
            matplotlib.rc('font', **font)
            self.update_chart(random.choice(list(self.data[0].keys())))

        super().__init__()
        self.data = data_list
        self.setWindowTitle('Histogram!')
        self.window_width, self.window_height = 1200, 800
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QGridLayout()
        self.setLayout(layout)
        create_list_widget()
        insert_plot()
        insert_buttons()

    def clicked(self):
        item = self.listwidget.currentItem()
        print(item.text())


    def update_chart(self, y):
        self.canvas.figure.clf()
        self.ax = self.canvas.figure.subplots()
        self.ax.hist([x[y] for x in self.data])
        self.ax.set_title("allo")
        self.ax.set_xlabel("XXXXXX")
        self.ax.set_ylabel("YYYYYY")

        self.canvas.draw()




if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    # Need to have this before the app.
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 30px;
        }
    ''')
    
    myApp = Histo_app([{"patate":3, "macaroni":"lll", "name":x, "allo": str(random.randint(0,10))} for x in range(30)])
    myApp.show()

    # Need to keep this so it doesn't close the window
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')