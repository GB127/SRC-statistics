from plots.pie import Pie_app
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import (QListWidget, QPushButton)

class Test_pie:
    data = [{"time":x*60, "str":str(x), "place":x*2, "game": "a" * (x+1)} for x in range(3)]

    def test_widgets(self, qtbot):
        widget = Pie_app(Test_pie.data)
        qtbot.addWidget(widget)
        if not any([isinstance(widget.layout.itemAt(x).widget(), FigureCanvasQTAgg) for x in range(widget.layout.count())]):
            raise AssertionError("A plot is not created.")
        if not any([isinstance(widget.layout.itemAt(x).widget(), QListWidget) for x in range(widget.layout.count())]):
            raise AssertionError("A list of entry is not created.")
        widget.canvas.figure.savefig("tests/pie")

    def test_long_game_names(self, qtbot):
        raise NotImplementedError("I do not know how to completely remove the labels without chaging everything. So I will leave it as is.")
