from plots.pie import Pie_app
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import (QComboBox,
                                            QListWidget)

class Test_pie:
    data = [{"time":x*60, "str":str(x), "place":x*2, "game": "a" * (x+1), "series":{"allo" + str(x)}} for x in range(3)]

    def test_widgets(self, qtbot):
        widget = Pie_app(Test_pie.data)
        qtbot.addWidget(widget)
        if not any([isinstance(widget.layout.itemAt(x).widget(), FigureCanvasQTAgg) for x in range(widget.layout.count())]):
            raise AssertionError("A plot is not created.")
        if not any([isinstance(widget.layout.itemAt(x).widget(), QListWidget) for x in range(widget.layout.count())]):
            raise AssertionError("A list of entry is not created.")
        assert [isinstance(widget.layout.itemAt(x).widget(), QComboBox) for x in range(widget.layout.count())].count(True) == 2
        assert widget.layout.count() == 4
            # Plot, List, Filter, Counting
        widget.canvas.figure.savefig("tests/plots/pie")

    def test_filter_options(self, qtbot):
        widget = Pie_app(Test_pie.data)
        qtbot.addWidget(widget)
        assert widget.layout.itemAt(2).widget().count() == 3

    def test_long_game_names(self, qtbot):
        for x in range(3):
            Test_pie.data[x]["str"] = "a" * (30 + x)
        widget = Pie_app(Test_pie.data)
        qtbot.addWidget(widget)
        widget.canvas.figure.savefig("tests/plots/pie_long")