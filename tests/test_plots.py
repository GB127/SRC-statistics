from plots.histo import Histo_app
from plots.pie import Pie_app
from tests.mocks import Table_pb_mock, Table_run_mock
from PyQt5 import QtCore

class Test_entry_list:
    def test_quantity(self, qtbot):
        for histo in [Histo_app, Pie_app]:
            widget = histo(Table_pb_mock().data)
            qtbot.addWidget(widget)
            assert len(widget.listwidget) == 20

class Test_filters:
    def test_quantity(self, qtbot):
        # run : time
        # PBs : time, place, WR %, WR time
        for tableau, expected_len in [(Table_pb_mock, 4), (Table_run_mock, 1)]:
            widget = Histo_app(tableau().data)
            qtbot.addWidget(widget)
            assert len(widget.buttons) == expected_len, f'{tableau.__name__} has {len(widget.buttons)} filter buttons, expected {expected_len}.'

    def test_title(self, qtbot):
        widget = Histo_app(Table_pb_mock().data)
        qtbot.addWidget(widget)
        qtbot.mouseClick(widget.buttons[0], QtCore.Qt.LeftButton)
        assert widget.ax.get_title() == "PB_mock - place"

class Test_histo:
    def test_xticks(self, qtbot):
        def place():
            qtbot.mouseClick(widget.buttons[0], QtCore.Qt.LeftButton)
            liste = list(widget.ax.get_xticklabels())

            assert widget.ax.get_xlabel() == "place"
            assert all([liste.count(x) == 1 for x in liste])
        
        def times():
            for clé in [1,2]:
                qtbot.mouseClick(widget.buttons[clé], QtCore.Qt.LeftButton)
                assert "time" in widget.ax.get_xlabel()
                raise NotImplementedError("Time string format check : TODO : Use regex to check format")
        
        def percentage():
            qtbot.mouseClick(widget.buttons[3], QtCore.LeftButton)
            assert widget.ax.get_xlabel() == "WR %"

        widget = Histo_app(Table_pb_mock().data)
        qtbot.addWidget(widget)
        place()
        times()
        percentage()

    def test_yticks(self, qtbot):
        widget = Histo_app(Table_pb_mock().data)
        assert widget.ax.get_ylabel() == "Frequency"
        assert min(widget.ax.get_yticks()) == 0
        assert all([isinstance(x, int) for x in widget.ax.get_yticks()]), "Not all y ticks are integer : some are floats"


    #def test_bins(self, qtbot):
    #    widget = Histo_app(Table_pb_mock().data)
    #    assert False, widget.ax.containers[0][0]




    # click in the Greet button and make sure it updates the appropriate label
    #qtbot.mouseClick(widget.button_greet, QtCore.Qt.LeftButton)

    #assert widget.greet_label.text() == "Hello!"