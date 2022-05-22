import pytest
from plots.lb_plot import LB_plot_app
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import (      QComboBox,
                                 QSpinBox,           QListWidget,  QDoubleSpinBox)
from numpy import arange
from code_SRC.composantes import Time
import warnings

class Test_lb_plot:
    data = {x:list(range(5, 10 + x, (2023 - x)))[:x - 2000]
    
         for x in range(2022, 2012, -1)}

    def test_widgets(self, qtbot):
        widget = LB_plot_app(Test_lb_plot.data)
        qtbot.addWidget(widget)
        warnings.warn("Need to check identity of widgets")

        assert widget.layout.count() == 6

    def test_lb_evo_plot(self, qtbot):
        widget = LB_plot_app(Test_lb_plot.data)
        qtbot.addWidget(widget)
        widget.plot_evolution()
        widget.canvas.figure.savefig("tests/plots/LB/lb_evo_plot")

    def test_metrics_evo_plot(self, qtbot):
        widget = LB_plot_app(Test_lb_plot.data)
        qtbot.addWidget(widget)
        widget.plot_metrics_evolution()
        widget.canvas.figure.savefig("tests/plots/LB/lb_metrics_evo_plot")

    def test_current_plot(self, qtbot):
        widget = LB_plot_app(Test_lb_plot.data)
        qtbot.addWidget(widget)
        widget.plot_current()
        widget.canvas.figure.savefig("tests/plots/LB/lb_current_plot")
