import sys
from PyQt5.QtWidgets import QListWidgetItem,QGridLayout,QPushButton, QApplication,QComboBox, QWidget, QHBoxLayout, QVBoxLayout, QListWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib
import random
from PyQt5.QtGui import QFont

class Histo_app(QWidget):
    def __init__(self, data_list):
        def create_list_widget():
            self.listwidget = QListWidget()
            self.listwidget.setFixedWidth(450)
            self.listwidget.alternatingRowColors()
            for entry in data_list:
                one_line = QListWidgetItem(str(entry))
                #one_line.setFont(QFont("Courier New", 10))
                one_line.setFont(QFont("Lucida Sans Typewriter", 10))
                # Lucida Sans Typewriter
                self.listwidget.addItem(one_line)
            testing = self.listwidget
            self.listwidget.clicked.connect(self.clicked)
            layout.addWidget(self.listwidget, 0, 0, 0,1)

        def insert_buttons():
            for numéro, x in enumerate(self.keys):
                dropbox = QPushButton(x)
                dropbox.clicked.connect(lambda checked, a=x : self.update_chart(a))
                layout.addWidget(dropbox, 1,1+numéro)


        def insert_plot():
            self.canvas = FigureCanvas(plt.Figure())
            layout.addWidget(self.canvas, 0,1, 0, len(self.keys))
            font = {'weight': 'normal',
                    'size': 16}
            matplotlib.rc('font', **font)
            self.update_chart(random.choice(self.keys))



        def fetch_valid_keys():
            self.keys = []
            for x, value in data_list[0].__dict__.items():
                if isinstance(value, (int, float)): self.keys.append(x)


        super().__init__()
        fetch_valid_keys()
        self.data = data_list
        self.setWindowTitle('Histogram!')
        self.window_width, self.window_height = 1400, 800
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
        def update_x():
            self.ax.set_xlabel(y)
        self.canvas.figure.clf()
        self.ax = self.canvas.figure.subplots()
        self.ax.hist([x[y] for x in self.data])
        self.ax.set_title(y)
        update_x()
        self.ax.set_ylabel("Frequency")
        self.canvas.draw()


def window_handler(data):
    # don't auto scale when drag app to a different monitor.
    # QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    # Need to have this before the app.
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 30px;
        }
    ''')
    
    myApp = Histo_app(data)
    myApp.show()

    # Need to keep this so it doesn't close the window
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')




class Mockery:
    def __init__(self):
        self.a = random.randint(122,333)
        self.b = random.randint(63,500)
        self.time = random.randint(3000,5000)
        self.d = random.randint(0,10)
        self.e = random.randint(0,10)
    def __getitem__(self, key):
        return self.__dict__[key]

if __name__ == "__main__":
    data = [Mockery() for _ in range(40)]
    window_handler(data)