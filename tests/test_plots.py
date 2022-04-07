from PyQt5 import QtCore
from plots.histo import Histo_app
from plots.pie import Pie_app
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import (   QListWidgetItem,    QGridLayout, 
                                QWidget,            QListWidget, QPushButton)


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

    def test_fig(self, qtbot):
        widget = Pie_app(Test_pie.data)
        qtbot.addWidget(widget)
        for widget_id in range(widget.layout.count()):
            plot_widget = widget.layout.itemAt(widget_id).widget()
            if isinstance(plot_widget, FigureCanvasQTAgg):
                break
        tempo = widget.canvas.figure
        tempo.savefig("tests/figures/pie")



class Test_hist:
    data = [{"time":x*60, "str":str(x), "place":x*2, "str2": str(x**2)} for x in range(3)]

    def test_widgets(self, qtbot):
        widget = Histo_app(Test_hist.data)
        qtbot.addWidget(widget)
        if not any([isinstance(widget.layout.itemAt(x).widget(), FigureCanvasQTAgg) for x in range(widget.layout.count())]):
            raise AssertionError("A plot is not created.")
        if not any([isinstance(widget.layout.itemAt(x).widget(), QListWidget) for x in range(widget.layout.count())]):
            raise AssertionError("A list of entry is not created.")
        assert [isinstance(widget.layout.itemAt(x).widget(), QPushButton) for x in range(widget.layout.count())].count(True) == 2

    def test_push_buttons_names(self, qtbot):
        widget = Histo_app(Test_hist.data)
        qtbot.addWidget(widget)
        buttons = [widget.layout.itemAt(x).widget() for x in range(widget.layout.count()) if isinstance(widget.layout.itemAt(x).widget(), QPushButton)]
        assert {x.text() for x in buttons} == {"time", "place"}

    def test_histo(self, qtbot):
        widget = Histo_app(Test_hist.data)
        qtbot.addWidget(widget)
        for widget_id in range(widget.layout.count()):
            plot_widget = widget.layout.itemAt(widget_id).widget()
            if isinstance(plot_widget, FigureCanvasQTAgg):
                break

        tempo = widget.canvas.figure
        tempo.savefig("tests/figures/histo")
        raise BaseException("The figure needs to be imprived")
