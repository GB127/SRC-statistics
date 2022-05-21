from plots.histo import Histo_app
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import (      QComboBox,
                                 QSpinBox,           QListWidget,  QDoubleSpinBox)
from numpy import arange
from code_SRC.composantes import Time

class Test_hist:
    data = [{"time":Time(x*60), "str":str(x), "place":x*2, "str2": str(x**2), "WR %":1 + 1/x} for x in range(1, 4)]*13

    def test_unique_data(self, qtbot):
        single_data = [{"time":1, "str":str(1), "place":1, "str2": str(1), "WR %":1} for x in range(1, 4)]

        widget = Histo_app(single_data)
        qtbot.addWidget(widget)


    def test_widgets(self, qtbot):
        widget = Histo_app(Test_hist.data)
        qtbot.addWidget(widget)
        assert widget.layout.count() == 5
        if not any([isinstance(widget.layout.itemAt(x).widget(), FigureCanvasQTAgg) for x in range(widget.layout.count())]):
            raise AssertionError("A plot is not created.")
        if not any([isinstance(widget.layout.itemAt(x).widget(), QListWidget) for x in range(widget.layout.count())]):
            raise AssertionError("A list of entry is not created.")
        assert [isinstance(widget.layout.itemAt(x).widget(), QComboBox) for x in range(widget.layout.count())].count(True) == 1
        assert [isinstance(widget.layout.itemAt(x).widget(), QSpinBox) for x in range(widget.layout.count())].count(True) == 1
        assert [isinstance(widget.layout.itemAt(x).widget(), QDoubleSpinBox) for x in range(widget.layout.count())].count(True) == 1

    def test_x_axis_options(self, qtbot):
        widget = Histo_app(Test_hist.data)
        qtbot.addWidget(widget)
        assert widget.layout.itemAt(1).widget().count() == 3

    def test_y_axis(self, qtbot):
        widget = Histo_app(Test_hist.data)
        qtbot.addWidget(widget)
        assert widget.canvas.figure.gca().get_ylabel() == "Frequency"
        assert len(widget.canvas.figure.gca().get_yticks()) <= 14
        assert list(widget.canvas.figure.gca().get_yticks()) == [x for x in range(2,16,2)]

    def test_x_axes_time(self, qtbot):
        widget = Histo_app(Test_hist.data)
        qtbot.addWidget(widget)
        widget.canvas.figure.savefig("tests/plots/histo_time")
        assert list(widget.canvas.figure.gca().get_xticks()) == [x for x in arange(60,60 * 3, 120 / 5)][1:]

    def test_with_outsiders_data(self, qtbot):
        Test_hist.data.append({"time":600000, "str":str(2), "place":44444444, "str2": str(2), "WR %":333333})
        widget = Histo_app(Test_hist.data)
        qtbot.addWidget(widget)
        assert sum([x.get_height() for x in widget.canvas.figure.gca().patches]) == 39.0