from entries.one_run import Run
from tables.base import Base_Table
from plots.handler import window_handler
from plots.histo import Histo_app
from plots.pie import Pie_app


class Table_run(Base_Table):
    def __init__(self, list_runs:list, include_lvl:bool):
        self.data = []
        for data in list_runs:
            if include_lvl == bool(data["level"]):
                self.data.append(Run(data))

    def __call__(self):
        super().__call__(self.histo, self.pie, self.sort)  # pragma: no cover


    def histo(self):
        window_handler(self.data, Histo_app)  # pragma: no cover

    def pie(self):
        window_handler(self.data, Pie_app)  # pragma: no cover
