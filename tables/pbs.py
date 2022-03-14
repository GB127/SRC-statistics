from entries.pb_entry import PB
from tables.base import Base_Table
from plots.handler import window_handler
from plots.histo import Histo_app
from plots.pie import Pie_app

class Table_pb(Base_Table):
    def __init__(self, list_runs:list):
        self.data = []
        for data in list_runs:
            self.data.append(PB(data))

    def __call__(self):
        super().__call__(self.histo, self.pie, self.sort)


    def histo(self):
        window_handler(self.data, Histo_app)

    def pie(self):
        window_handler(self.data, Pie_app)