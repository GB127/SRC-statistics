from entries.pb_entry import PB
from entries.rank_entry import Rank
from entries.run_entry import Run
from tables.pbs import Table_pb
from tables.runs import Table_run

class Run_mock(Run):
    def __init__(self, include_level=False):
        self.level = False
        self.game = "game"
        self.system = "system"
        self.level = None if not include_level else "level"
        self.time = 1
        self.category = "Category"


class Rank_mock(Rank):
    def __init__(self):
        self.level = False
        self.game = "game"
        self.system = "system"
        self.time = 2
        self.category = "Category"
        self["WR time"] = 1
        self["WR %"] = 2


class PB_mock(PB):
    def __init__(self, include_level=False):
        self.level = False
        self.game = "game"
        self.system = "system"
        self.place = 2
        self.time = 2
        self["WR time"] = 1
        self["WR %"] = 2
        self.category = "Category"
        self.leaderboard = [0,0,0,0]
        self.level = None if not include_level else "level"


class Table_pb_mock(Table_pb):
    def __init__(self):
        self.data = [PB_mock() for _ in range(20)]
        for x in range(5):
            self.data[x].time = 50 * x
            self.data[x].game += str(x)
            self.data[x]["WR %"] = 1 + (0.2 * x)
            self.data[x].place = x +1
            self.data[x]["WR time"] = 20 * x

class Table_run_mock(Table_run):
    def __init__(self):
        self.data = [Run_mock() for x in range(5)]
        for x in range(5):
            self.data[x].time = 50 * x
            self.data[x].game += str(x)
