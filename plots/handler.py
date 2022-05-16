import sys
from PyQt5.QtWidgets import QApplication

global app
app = QApplication(sys.argv)


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
    
    