from tables.solo_runs import Table_pb, Table_run
from entries.grouped import Grouped, Saved
from tables.base import Base_table
from code_SRC.composantes import Time
from statistics import StatisticsError, fmean, geometric_mean as geomean


class Table_grouped(Base_table):
    def __init__(self, clé, runs: Table_run, pbs: Table_pb):
        self.data = []
        for x in runs.all_value_key(clé):
            self.data.append(
                Grouped(x, runs.match_key_value(clé, x), pbs.match_key_value(clé, x))
            )

    def change_mode(self):
        for index, fx in enumerate([sum, fmean, geomean ]):
            print(index, fx.__name__)
        command = input(
            f"Select option: [0-{len(self.methods()) -1}] | Type end to exit\nInput : "
        )
        


    def methods(self):  # pragma: no cover
        return self.sort, self.change_mode

    def __str__(self):
        line = "-------" + "-" * len(str(self.data[0])) + "\n"
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
        for ind, stat in enumerate([sum, fmean, geomean]):
            if stat == geomean:
                group_runs = [x for x in group_runs if x != 0]
                group_pbs = [x for x in group_pbs if x != 0]
                lens_runs = [x for x in lens_runs if x != 0]
                lens_pbs = [x for x in lens_pbs if x != 0]
            string += f'{["Sum", "Mean", "Geomean"][ind]:>38}  {round(stat(lens_runs)):3}   {Time(stat(group_runs))}  {round(stat(lens_pbs)):3}   {Time(stat(group_pbs))}\n'

        return string


class Table_saved(Base_table):
    def __init__(self, clé, runs: Table_run, pbs: Table_pb):
        self.data = []
        for x in runs.all_value_key(clé):
            if len(runs.match_key_value(clé, x)) > 1:
                try:
                    self.data.append(
                        Saved(
                            x,
                            runs.match_key_value(clé, x),
                            pbs.match_key_value(clé, x)[0],
                        )
                    )
                except IndexError:
                    continue

    def __str__(self):
        line = "-------" + "-" * len(str(self.data[0])) + "\n"
        string = line
        for index, object in enumerate(self.data, start=1):
            string += f"{index:>4}   {str(object)}\n"
        string += line
        return string

    def methods(self):
        return [self.sort]
