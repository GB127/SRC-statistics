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
        self.time = 1
        self.category = "Category"


class PB_mock(PB):
    def __init__(self):
        self.level = False
        self.game = "game"
        self.system = "system"
        self.time = 1
        self.category = "Category"