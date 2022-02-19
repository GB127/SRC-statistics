from entries.run_entry import Run
from tables.base import Base_Table

class Table_run(Base_Table):
    def __init__(self, list_runs:list):
        self.data = []
        for data in list_runs:
            self.data.append(Run(data))
