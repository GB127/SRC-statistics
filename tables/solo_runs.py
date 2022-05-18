from entries.run import PB, Run
from code_SRC.composantes import Time
from plots.handler import window_handler
from plots.histo import Histo_app
from plots.pie import Pie_app
from copy import deepcopy
from tables.base import Base_table


class Table_run(Base_table):
    def __init__(self, list_runs: list, include_lvl: bool):
        """Class listing full OR level runs.
            Args:
                list_runs (list): list of dictionnaries received from SRC.
                include_lvl (bool): Level runs and non-level runs aren't combined.
                    True : Only keep level runs
                    False : Only keep full runs
            """
        self.data = []
        for no, data in enumerate(list_runs, start=1):
            if include_lvl == bool(data["level"]):
                self.data.append(Run(data))
            print(f"{no}/{len(list_runs)} runs processed!")
    
    def methods(self):
        return  self.pie, self.histo


    def pie(self):
            window_handler(self.data, Pie_app)

    def histo(self):
        window_handler(self.data, Histo_app)

    def create_grouped(self, infos):
        sum_class = deepcopy(self[0])
        sum_class.gamecat.game.game = f''
        sum_class.gamecat.category = f''
        sum_class.gamecat.subcategory = ""
        sum_class.time = f'{Time(infos["time"])}'
        sum_class.system.system = f''
        return sum_class


class Table_pb(Table_run):
    def __init__(self, list_runs: list, include_lvl: bool):
        self.data = []
        for no, data in enumerate(list_runs, start=1):
            if include_lvl == bool(data["run"]["level"]):
                self.data.append(PB(data))
            print(f"{no}/{len(list_runs)} PBs processed!")


    def create_grouped(self, infos):
        sum_class = super().create_grouped(infos)
        sum_class.delta = Time(infos["delta"])
        sum_class.perc = 9

        return sum_class
