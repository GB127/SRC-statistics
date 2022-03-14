import sys
from PyQt5.QtWidgets import QApplication
from random import random, randint


class Mockery:  # for tests
    def __init__(self):
        self["A %"] = random()
        self.time = randint(3,5)

        self["Game"] = str(randint(1,4)) + "APPPP"



    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value



def window_handler(data, application, debug=False):
    # Need to have this before the app.
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 30px;
        }
    ''')
    
    myApp = application(data)
    myApp.show()

    if not debug:
    # Need to keep this so it doesn't close the window
        try:
            sys.exit(app.exec_())
        except SystemExit:
            print('Closing Window...')


