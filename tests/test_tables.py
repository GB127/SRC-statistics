from PyQt5 import QtCore
import pytest
from entries.lb_entry import Rank
from entries.one_run import Run
from requests_mock.mocker import Mocker
from tables.base import Base_Table
from entries.base_entry import Base_Entry
from tables.runs import Table_run
from tables.leaderboard import LB
from entries.personal_best import PB
from tables.pbs import Table_pb
from plots.histo import Histo_app
from plots.pie import Pie_app
from PyQt5.QtWidgets import QPushButton


class Test_base:
    case = Base_Table()
    case.data = [Base_Entry() for _ in range(3)]
    for numéro, x in zip([3, 1, 2], case.data):
        x.__dict__ = {"tempo": numéro, "tempo2": "str"}

    def test_str(self):
        for symbol in ["∑", "X̅", "gX̅"]:
            assert symbol in str(Test_base.case)
        for element in Test_base.case.data:
            assert str(element) in str(Test_base.case)
        assert str(Test_base.case).count("\n") == 10

    def test_operations(self):
        assert Test_base.case.sum().__dict__ == {"tempo": 6, "tempo2": "1"}
        assert Test_base.case.mean().__dict__ == {"tempo": 2, "tempo2": "3.0"}
        assert Test_base.case.geomean().__dict__["tempo"] != 2
        assert len(Test_base.case) == 3
        assert Test_base.case[0].__dict__ == {"tempo": 3, "tempo2": "str"}

    def test_sort(self, monkeypatch):
        Test_base.case.sort("tempo")
        for no, x in enumerate(Test_base.case.data):
            assert (
                x.__dict__ == [{"tempo": x, "tempo2": "str"} for x in range(1, 4)][no]
            )

        for numéro, x in zip([3, 1, 2], Test_base.case.data):
            x.__dict__ = {"tempo": numéro, "tempo2": "str"}

        monkeypatch.setattr("builtins.input", lambda _: "0")
        Test_base.case.sort()
        for no, x in enumerate(Test_base.case.data):
            assert (
                x.__dict__ == [{"tempo": x, "tempo2": "str"} for x in range(1, 4)][no]
            )

    def test_call(self, monkeypatch):
        def test():
            raise BaseException
        def test2():
            raise BaseException


        with pytest.raises(BaseException):
            for x in ["1", "2"]:
                    monkeypatch.setattr("builtins.input", lambda _: x)
                    Test_base.case(test, test2)
        monkeypatch.setattr("builtins.input", lambda _: "end")
        Test_base.case(test, test2)
        monkeypatch.setattr("builtins.input", lambda _: "not a number")
        Test_base.case(test, test2)



class Test_runs:
    dicto = {
        "id": "1zx46vqy",
        "game": "4d709l17",
        "level": "ywep57dl",
        "category": "9d8x94w2",
        "times": {
            "primary_t": 15855,
        },
        "system": {
            "platform": "4p9z06rn",
            "emulated": False,
            "region": "pr184lqn",
        },
        "values": {"0nw200nq": "gq79nvlp"},
    }

    def test_init(self):
        Test_runs.classe = Table_run([Test_runs.dicto for _ in range(3)], True)
        assert isinstance(Test_runs.classe.data, list) and isinstance(
            self.classe.data[0], Run
        )
        assert all([bool(x.level) for x in Test_runs.classe.data])

        Test_runs.dicto["level"] = None
        Test_runs.classe = Table_run([Test_runs.dicto for _ in range(3)], False)
        assert isinstance(self.classe.data, list) and isinstance(
            self.classe.data[0], Run
        )
        assert all([not bool(x.level) for x in Test_runs.classe.data])

    def test_hist(self, qtbot):
        for x in range(3):
            Test_runs.classe[x]["time"] += x

        widget = Histo_app(Test_runs.classe.data)
        qtbot.addWidget(widget)
        buttons = [
            widget.layout.itemAt(x).widget()
            for x in range(widget.layout.count())
            if isinstance(widget.layout.itemAt(x).widget(), QPushButton)
        ]

        for button in buttons:
            qtbot.mouseClick(button, QtCore.Qt.LeftButton)

    def test_pie(self, qtbot):
        widget = Pie_app(Test_runs.classe.data)
        qtbot.addWidget(widget)
        buttons = [
            widget.layout.itemAt(x).widget()
            for x in range(widget.layout.count())
            if isinstance(widget.layout.itemAt(x).widget(), QPushButton)
        ]

        for button in buttons:
            qtbot.mouseClick(button, QtCore.Qt.LeftButton)


class Test_lb:
    dicto = [
        {
            "place": x + 1,
            "run": {
                "id": "7z037xoz",
                "game": "4d709l17",
                "level": None,
                "category": "9d8x94w2",
                "times": {"primary_t": 1401 + x},
                "system": {
                    "platform": "4p9z06rn",
                    "emulated": False,
                    "region": "pr184lqn",
                },
                "values": {"p854r2vl": "5q85yy6q"},
            },
        }
        for x in range(3)
    ]

    def test_init(self):
        Test_lb.classe = LB(Test_lb.dicto)
        assert isinstance(Test_lb.classe.data, list) and isinstance(
            Test_lb.classe.data[0], Rank
        )

    def test_str(self):
        attendu = (
            "-------------------------------------------------\n"
            "   1     0:23:21   +0:00:00   (100.00%)   0:00:00\n"
            "   2     0:23:22   +0:00:01   (100.07%)   0:00:01\n"
            "   3     0:23:23   +0:00:02   (100.14%)   0:00:01\n"
            "-------------------------------------------------\n"
            "   ∑     1:10:06   +0:00:03   (100.07%)   0:00:02\n"
            "-------------------------------------------------\n"
            "   X̅     0:23:22   +0:00:01   (100.07%)   0:00:00\n"
            "  gX̅     0:23:21   +0:00:01   (100.07%)   0:00:01\n"
            "-------------------------------------------------\n"
        )
        assert str(Test_lb.classe) == attendu, str(Test_lb.classe)


class Test_pbs:
    pb_dict = {
        "place": 2,
        "run": {
            "id": "7z037xoz",
            "game": "4d709l17",
            "level": None,
            "category": "9d8x94w2",
            "times": {"primary_t": 1401 + 2},
            "system": {
                "platform": "4p9z06rn",
                "emulated": False,
                "region": "pr184lqn",
            },
            "values": {"p854r2vl": "5q85yy6q"},
        },
    }

    def test_init(self, requests_mock: Mocker):
        lb_data = {
            "data": {
                "runs": [
                    {
                        "place": x + 1,
                        "run": {
                            "id": "7z037xoz",
                            "game": "4d709l17",
                            "level": None,
                            "category": "9d8x94w2",
                            "times": {"primary_t": 1401 + x},
                            "system": {
                                "platform": "4p9z06rn",
                                "emulated": False,
                                "region": "pr184lqn",
                            },
                            "values": {"p854r2vl": "5q85yy6q"},
                        },
                    }
                    for x in range(3)
                ]
            }
        }
        link = "https://www.speedrun.com/api/v1/leaderboards/4d709l17/category/9d8x94w2?var-"
        requests_mock.get(link, json=lb_data)
        Test_pbs.classe = Table_pb(
            [Test_pbs.pb_dict for _ in range(3)], include_lvl=False
        )

        assert hasattr(Test_pbs.classe, "data")
        assert isinstance(Test_pbs.classe[0], PB)

    def test_str(self):
        attendu = (
            "-------------------------------------------------------------------------------------------------------------------------\n"
            "   1   Game   Zelda: The Wind Wake   Any%                     0:23:21    0:23:23 +0:00:02   (100.14%)      2/3     33.33%\n"
            "   2   Game   Zelda: The Wind Wake   Any%                     0:23:21    0:23:23 +0:00:02   (100.14%)      2/3     33.33%\n"
            "   3   Game   Zelda: The Wind Wake   Any%                     0:23:21    0:23:23 +0:00:02   (100.14%)      2/3     33.33%\n"
            "-------------------------------------------------------------------------------------------------------------------------\n"
            "   ∑   1      1                      1                        1:10:03    1:10:09 +0:00:06   (100.14%)      6/9     33.33%\n"
            "-------------------------------------------------------------------------------------------------------------------------\n"
            "   X̅   3.0    3.0                    3.0                      0:23:21    0:23:23 +0:00:02   (100.14%)      2/3     33.33%\n"
            "  gX̅                                                          0:23:20    0:23:23 +0:00:02   (100.14%)      2/3     33.33%\n"
            "-------------------------------------------------------------------------------------------------------------------------\n"
        )
        assert str(Test_pbs.classe) == attendu, "\n" + str(Test_pbs.classe)

    def test_hist(self, qtbot):
        for x in range(3):
            Test_pbs.classe[x]["time"] += x
            Test_pbs.classe[x]["place"] += x
            Test_pbs.classe[x]["LB %"] += x
            Test_pbs.classe[x]["WR %"] += x
            Test_pbs.classe[x]["WR time"] += x
            Test_pbs.classe[x]["delta WR"] += x

        widget = Histo_app(Test_pbs.classe.data)
        qtbot.addWidget(widget)
        buttons = [
            widget.layout.itemAt(x).widget()
            for x in range(widget.layout.count())
            if isinstance(widget.layout.itemAt(x).widget(), QPushButton)
        ]

        for button in buttons:
            qtbot.mouseClick(button, QtCore.Qt.LeftButton)

    def test_pie(self, qtbot):
        widget = Pie_app(Test_pbs.classe.data)
        qtbot.addWidget(widget)
        buttons = [
            widget.layout.itemAt(x).widget()
            for x in range(widget.layout.count())
            if isinstance(widget.layout.itemAt(x).widget(), QPushButton)
        ]

        for button in buttons:
            qtbot.mouseClick(button, QtCore.Qt.LeftButton)
