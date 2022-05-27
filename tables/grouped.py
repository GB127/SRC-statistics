from tables.solo_runs import Table_pb, Table_run
from entries.grouped import Grouped
from tables.base import Base_table
from copy import deepcopy
from code_SRC.composantes import Time
from statistics import StatisticsError, mean, geometric_mean as geomean

class Table_grouped(Base_table):
    def __init__(self, clé, runs:Table_run, pbs:Table_pb):
        self.data = []
        for x in runs.all_value_key(clé):
            self.data.append(Grouped(x, runs.match_key_value(clé, x), pbs.match_key_value(clé, x)))

    def methods(self):# pragma: no cover
        return  [self.sort]

    def __str__(self):
        line  = "-------" + "-" * len(str(self.data[0])) + "\n"
        string = line
        for index, object in enumerate(self.data, start=1):
            string += f"{index:>4}   {str(object)}\n"
        string += line

        # Sum
        group_runs = [Grouped.mode(x.runs) for x in self.data]
        try:
            group_pbs = [Grouped.mode(x.pbs) for x in self.data]
        except StatisticsError:
            group_pbs = [Grouped.mode(x.pbs) for x in self.data if x.pbs]
 
        lens_runs = [len(x.runs) for x in self.data]
        lens_pbs = [len(x.pbs) for x in self.data]
        for stat in [sum, mean, geomean]:
            if stat == geomean:
                group_runs = [x for x in group_runs if x != 0]
                group_pbs = [x for x in group_pbs if x != 0]
                lens_runs = [x for x in lens_runs if x != 0]
                lens_pbs = [x for x in lens_pbs if x != 0]
            string += f'{"":38}  {round(stat(lens_runs)):3}   {Time(stat(group_runs))}  {round(stat(lens_pbs)):3}   {Time(stat(group_pbs))}\n'




        return string