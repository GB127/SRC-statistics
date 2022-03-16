from plots.handler import window_handler
from plots.histo import Histo_app
from tests.mocks import Table_run_mock


def test_hello(qtbot):
    widget = Histo_app(Table_run_mock().data)
    qtbot.addWidget(widget)
    assert False


    # click in the Greet button and make sure it updates the appropriate label
    #qtbot.mouseClick(widget.button_greet, QtCore.Qt.LeftButton)

    #assert widget.greet_label.text() == "Hello!"