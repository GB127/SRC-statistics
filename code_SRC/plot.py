import sys
from PyQt5.QtWidgets import QApplication,QComboBox, QWidget, QHBoxLayout, QVBoxLayout, QListWidget
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
            layout.addWidget(self.listwidget)

        def insert_dropbox():
            self.dropbox = QComboBox()
            self.dropbox.setFixedWidth(300)
            self.dropbox.addItems(["One", "Two", "Three"])
            layout.addWidget(self.dropbox)


        def insert_plot():
            font = {'weight': 'normal',
                    'size': 16}
            matplotlib.rc('font', **font)
            self.ax = self.canvas.figure.subplots()
            self.ax.hist([x[self.filter] for x in data_list])


        self.filter = random.choice(list(data_list[0].keys()))
        super().__init__()
        self.setWindowTitle('Histogram!')
        self.window_width, self.window_height = 1200, 800
        self.setMinimumSize(self.window_width, self.window_height)


        layout = QHBoxLayout()
        self.setLayout(layout)

        create_list_widget()


        self.canvas = FigureCanvas(plt.Figure(figsize=(15, 6)))

        # Graphic zone
        layout.addWidget(self.canvas)

        insert_plot()


        insert_dropbox()

    def clicked(self, qmodelindex):
        item = self.listwidget.currentItem()
        print(item.text())


    def update_chart(self):
        value = self.input.text()
        try:
            value = float(value)
        except ValueError:
            value = 0

        x_position = [0.5]

        if self.bar:
            self.bar.remove()
        self.bar = self.ax.bar(x_position, value, width=0.2, color='g')
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
    
    myApp = Histo_app([{"name":x, "allo": str(random.randint(0,10))} for x in range(30)])
    myApp.show()

    # Need to keep this so it doesn't close the window
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')