import sys
from PyQt5.QtWidgets import QApplication
from random import random, randint

global app
app = QApplication(sys.argv)



class Mockery:  # for tests
    def __init__(self, x):
        self["A %"] = random()
        self.time = 2 * x**2
        self.place = x
        self["game"] = str(randint(1,4)) + "APPPP"
        self.leaderboard = [{"place" : x, "time": x * 30} for x in range(1,21)]
        self.category = "Please"

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value



def window_handler(data, application, debug=False):
    # Need to have this before the app.
    app.setStyleSheet('''
        QWidget {
            font-size: 30px;
        }
    ''')
    
    myApp = application(data)
    if debug: return

    myApp.show()
    app.exec_()
    
    