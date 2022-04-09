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

class Test_hist:
    data = [{"time":x*60, "str":str(x), "place":x*2, "str2": str(x**2), "WR %":1 + 1/x} for x in range(1, 4)]*13

    def test_unique_data(self, qtbot):
        raise NotImplementedError("Need to figure out a way to take account of data with identical values if someone somehow has that")

    def test_with_outsiders_data(self, qtbot):
        raise NotImplementedError("TODO")


    def test_widgets(self, qtbot):
        widget = Histo_app(Test_hist.data)
        qtbot.addWidget(widget)
        if not any([isinstance(widget.layout.itemAt(x).widget(), FigureCanvasQTAgg) for x in range(widget.layout.count())]):
            raise AssertionError("A plot is not created.")
        if not any([isinstance(widget.layout.itemAt(x).widget(), QListWidget) for x in range(widget.layout.count())]):
            raise AssertionError("A list of entry is not created.")
        assert [isinstance(widget.layout.itemAt(x).widget(), QPushButton) for x in range(widget.layout.count())].count(True) == 3

    def test_push_buttons_names(self, qtbot):
        widget = Histo_app(Test_hist.data)
        qtbot.addWidget(widget)
        buttons = [widget.layout.itemAt(x).widget() for x in range(widget.layout.count()) if isinstance(widget.layout.itemAt(x).widget(), QPushButton)]
        assert {x.text() for x in buttons} == {"time", "place", "WR %"}

    def test_y_axis(self, qtbot):
        widget = Histo_app(Test_hist.data)
        qtbot.addWidget(widget)
        assert widget.canvas.figure.gca().get_ylabel() == "Frequency"
        assert len(widget.canvas.figure.gca().get_yticks()) <= 14
        assert list(widget.canvas.figure.gca().get_yticks()) == [x for x in range(2,16,2)]

    def test_x_axes_time(self, qtbot):
        widget = Histo_app(Test_hist.data)
        qtbot.addWidget(widget)
        assert list(widget.canvas.figure.gca().get_xticks()) == [x for x in arange(60,60 * 3, 120 / 5)][1:]
        widget.canvas.figure.savefig("tests/histo_time")

    def test_x_axes_perc(self, qtbot):
        widget = Histo_app(Test_hist.data)
        qtbot.addWidget(widget)
        widget.update_plot(number="WR %")
        widget.canvas.figure.savefig("tests/histo_perc")
        assert list(widget.canvas.figure.gca().get_xticks()) == [x for x in arange(4/3,2,2/15 )][1:-1]

