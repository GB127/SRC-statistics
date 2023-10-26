from tables.solo_runs import Table_pb, Table_run
from entries.grouped import Grouped, Saved
from tables.base import Base_table
from code_SRC.composantes import Time
from statistics import StatisticsError, fmean, geometric_mean as geomean
from plots.handler import window_handler
from plots.save_plot import Save_plot_app


class Table_grouped(Base_table):
    def __init__(self, clé, runs: Table_run, pbs: Table_pb):
        self.data = []
        self.groupe = clé
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
        if command.isnumeric:
            Grouped.mode = [sum, fmean, geomean ][int(command)]
        


    def methods(self):  # pragma: no cover
        return self.sort, self.change_mode

    def __str__(self):
        heading = f"{'#':>4}   {self.groupe.capitalize():^32}   {'#'}   {'Runs':^9}   {' #'}   {'PBs':^9}\n"
        
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

        string += f'Current mode : {Grouped.mode.__name__.capitalize()}'

        return heading + string


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
        heading = f"{'#':>4}   {'Game (Category)':^40}   {'#':2}   {'1st':^7} | {'PB':^9} {'PB Δ%':^18} | {'max Δ%':^18} | {'potential Δ%':^18}\n"
        line = "-------" + "-" * len(str(self.data[0])) + "\n"
        string = line
        for index, object in enumerate(self.data, start=1):
            string += f"{index:>4}   {str(object)}\n"
        string += line
        return heading + string

    def methods(self):
        return self.sort, self.plot


    def plot(self):
        #command = input(f"Which one? [0-{len(self.data)}] ")
        command = "1"
        if command.isnumeric():
            testing_runs = self[int(command)].runs
            testing_pb = self[int(command)].pb
            testing_WR = self[int(command)].WR.seconds
            window_handler((testing_runs, testing_pb, testing_WR), Save_plot_app)