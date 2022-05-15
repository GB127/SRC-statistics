import warnings
from entries.run import PB, Run
from code_SRC.composantes import Time
from tables.leaderboard import LB

class Table_run:
    def __init__(self, list_runs:list, include_lvl:bool):
        self.data = []
        for no, data in enumerate(list_runs, start=1):
            if include_lvl == bool(data["level"]):
                self.data.append(Run(data))
            print(f'{no}/{len(list_runs)} runs processed!')

    def __str__(self):
        string = "-------" + "-" * len(str(self.data[0])) + "\n"
        for index, object in enumerate(self.data, start=1):
            string += f'{index:>4}   {str(object)}\n'
        string += "-------" + "-" * len(str(object)) + "\n"
        string += "Sum    "
        string += self.str_sum()
        warnings.warn("Please use summation symbol")


        return string

    def keys(self):
        return self[0].keys()

    def __getitem__(self, index:int):
        return self.data[index]

    def count(self, clé):
        if isinstance(self[0][clé], str) or clé == "release":
            return len(set(x[clé] for x in self.data))
        elif isinstance(self[0][clé], set):
            return len(set().union(*[x[clé] for x in self.data]))
        elif isinstance(self[0][clé], (int, float, Time)):
            return sum(x[clé] for x in self.data)


    def str_sum(self):
        def max_len(tostr):
            return len(str(tostr))
        system = f'{self.count("system")} systems'
        game = f'{self.count("game")} games'
        categories = f'{self.count("category")} categories'
        times = f'{self.count("time")}'
        
        string = f'{system[:max_len(self[0].system)]:{max_len(self[0].system)}}'
        string += f'   {game:<30}'
        string += f'   {categories:<20}'
        string += f'   {times}'

        return string
class Table_pb(Table_run):
    def __init__(self, list_runs:list, include_lvl:bool):
        self.data = []
        for no, data in enumerate(list_runs, start=1):
            if include_lvl == bool(data["run"]["level"]):
                self.data.append(PB(data))
            print(f'{no}/{len(list_runs)} PBs processed!')


