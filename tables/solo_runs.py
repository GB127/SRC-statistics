from entries.run import PB, Run
from code_SRC.composantes import Time
from statistics import fmean, geometric_mean as geomean
from plots.handler import window_handler
from plots.histo import Histo_app
from plots.pie import Pie_app
from math import fsum
from collections import Counter
from itertools import chain
from copy import deepcopy

class Base_table:
    def __init__(self):
        raise BaseException("This table can't be created : need to go by the childs")


    def group_attr(self)->dict:
        dicto_sets = {}
        for clé in self.keys():
            if isinstance(self[0][clé], set):
                dicto_sets[clé] = Counter(chain(*[x[clé] for x in self.data]))
            elif isinstance(self[0][clé], (Time, int, float)):
                dicto_sets[clé] = list(x[clé] for x in self.data)
            else:
                dicto_sets[clé] = Counter(x[clé] for x in self.data)
        assert list(dicto_sets.keys()) == self.keys(), f'{dicto_sets.keys()} == {self.keys()}'
        return dicto_sets

    def sum(self)->dict:
        dicto_groups = self.group_attr()
        dicto_sum = {}
        for clé in self.keys():
            if isinstance(self[0][clé], (int, float, Time)):
                dicto_sum[clé] = fsum(dicto_groups[clé])
            else:
                dicto_sum[clé] = len(dicto_groups[clé])
        return dicto_sum

    def mean(self)->dict:
        dicto_groups = self.group_attr()
        dicto_mean = {}
        for clé in self.keys():
            if isinstance(self[0][clé], (int, float, Time)):
                dicto_mean[clé] = fmean(dicto_groups[clé])
            else:
                dicto_mean[clé] = len(dicto_groups[clé]) / len(self)
        return dicto_mean
            
    def geomean(self)->dict:
        dicto_groups = self.group_attr()
        dicto_mean = {}
        for clé in self.keys():
            if isinstance(self[0][clé], (int, float, Time)):
                dicto_mean[clé] = geomean([float(x) for x in dicto_groups[clé] if float(x) > 0])
            else:
                dicto_mean[clé] = len(self) / len(dicto_groups[clé])
        return dicto_mean

    def __str__(self):
        line  = "-------" + "-" * len(str(self.data[0])) + "\n"
        string = line
        for index, object in enumerate(self.data, start=1):
            string += f"{index:>4}   {str(object)}\n"
        string += line
        string += f'       {self.create_grouped(self.sum())}\n'
        string += f'       {self.create_grouped(self.mean())}\n'
        string += f'       {self.create_grouped(self.geomean())}'
        return string

    def __len__(self):
        return len(self.data)


    def __getitem__(self, index: int):
        return self.data[index]

    def keys(self):
        """Retrieves keys that can be used for sorting."""
        return self[0].keys()

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
