from entries.pb_entry import PB
from entries.rank_entry import Rank
from entries.run_entry import Run

class Run_mock(Run):
    def __init__(self):
        self.level = False
        self.game = "game"
        self.system = "system"
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
    def __init__(self):
        self.level = False
        self.game = "game"
        self.system = "system"
        self.place = 2
        self.time = 2
        self["WR time"] = 1
        self["WR %"] = 2
        self.category = "Category"
        self.leaderboard = [0,0,0,0]
