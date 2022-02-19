from entries.pb_entry import PB
from tables.base import Base_Table

class Table_pb(Base_Table):
    def __init__(self, list_runs:list):
        self.data = []
        for data in list_runs:
            self.data.append(PB(data))
