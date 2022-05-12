from entries.pb_evolution import PB_evo
from tables.base import Base_Table

class Evolutions(Base_Table):

    def __init__(self, runs, pbs):
        self.data = []
        for pb in pbs:
            same_cat = runs.fetch()
            self.data.append()