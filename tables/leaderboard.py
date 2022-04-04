from entries.lb_entry import Rank
from tables.base import Base_Table

class LB(Base_Table):
    def __init__(self, list_Ranks:list):
        self.data = []
        self.WR = list_Ranks[0]["run"]["times"]["primary_t"]

        #self.WR = list_Ranks[0]["run"]["times"]["primary_t"]
        for data in list_Ranks:
            self.data.append(Rank(data, self.WR))

    def sum(self):
        tempo = super().sum()
        tempo["WR %"] = tempo.time / tempo["WR time"]
        return tempo