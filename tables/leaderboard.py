from entries.rank_entry import Rank
from tables.base import Base_Table

class LB(Base_Table):
    def __init__(self, list_Ranks:list):
        self.data = []
        for data in list_Ranks:
            self.data.append(Rank(data))
