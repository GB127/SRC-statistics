from PyQt5 import QtCore
from plots.histo import Histo_app
from plots.pie import Pie_app
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import (   QListWidgetItem,    QGridLayout, 
                                QWidget,            QListWidget, QPushButton)
from numpy import arange

class Test_pie:
    data = [{"time":x*60, "str":str(x), "place":x*2, "game": "a" * (x+1)} for x in range(3)]

    def test_widgets(self, qtbot):
        widget = Pie_app(Test_pie.data)
        qtbot.addWidget(widget)
        if not any([isinstance(widget.layout.itemAt(x).widget(), FigureCanvasQTAgg) for x in range(widget.layout.count())]):
            raise AssertionError("A plot is not created.")
        if not any([isinstance(widget.layout.itemAt(x).widget(), QListWidget) for x in range(widget.layout.count())]):
            raise AssertionError("A list of entry is not created.")
        assert [isinstance(widget.layout.itemAt(x).widget(), QPushButton) for x in range(widget.layout.count())].count(True) == 2

    def test_push_buttons_names(self, qtbot):
        widget = Pie_app(Test_pie.data)
        qtbot.addWidget(widget)
        buttons = [widget.layout.itemAt(x).widget() for x in range(widget.layout.count()) if isinstance(widget.layout.itemAt(x).widget(), QPushButton)]
        assert {x.text() for x in buttons} == {"game", "str"}

    def test_long_game_names(self, qtbot):
        raise NotImplementedError("TODO")
