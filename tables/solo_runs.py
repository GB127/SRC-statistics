from entries.run import PB, Run
from code_SRC.composantes import Time
from statistics import mean, geometric_mean as geomean


class Table_run:
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

    def __str__(self):
        """Uses self.str_sum, selt.str_mean and self.str_geomean.
            Had to create methods for these three option so that
            PB can inherit from this class easily.
            """
        string = "-------" + "-" * len(str(self.data[0])) + "\n"
        for index, object in enumerate(self.data, start=1):
            string += f"{index:>4}   {str(object)}\n"
        string += "-------" + "-" * len(str(object)) + "\n"
        string += f"  ∑    {self.str_sum()}\n"
        string += f"Mea    {self.str_mean()}\n"
        string += f"geo    {self.str_geomean()}\n"
        return string

    def __len__(self):
        return len(self.data)

    def keys(self):
        """Retrieves keys that can be used for sorting."""
        return self[0].keys()

    def __getitem__(self, index: int):
        return self.data[index]

    def count(self, clé: str) -> int:
        """Calculate the total of the given field.
            If the field is a set (namely the series),
            or a string (game, level, system, category...),
            all values are grouped in a set to exclude duplicates.
            Then the length of the set is returned.
            If the field is a Time or a int, the sum is calculated.
            """
        if isinstance(self[0][clé], str) or clé == "release":
            return len(set(x[clé] for x in self.data))
        elif isinstance(self[0][clé], set):
            return len(set().union(*[x[clé] for x in self.data]))
        elif isinstance(self[0][clé], (int, float, Time)):
            return sum(x[clé] for x in self.data)

    def str_sum(self) -> str:
        """returns a string representing the summation of the table.
            Uses the count method."""

        def max_len(tostr):
            return len(str(tostr))

        system = f'{self.count("system")} systems'
        game = f'{self.count("game")} games'
        categories = f'{self.count("category")} categories'
        times = f'{self.count("time")}'

        string = f"{system[:max_len(self[0].system)]:{max_len(self[0].system)}}"
        string += f"   {game:<30}"
        string += f"   {categories:<20}"
        string += f"   {times}"

        return string

    def str_mean(self) -> str:
        """returns a string representing the arithmetic mean of the table.
            -> For values that were strings in the mean, the total
                number is divided by this value. to represent the
                mean of game per run.
                    formula : (# of runs)/ value
            -> For values that were Time, int or float, the mean is calculated as usual.
            Uses the count method."""

        def max_len(tostr):
            return len(str(tostr))

        system = f'{round(len(self) / self.count("system"), 2)} systems'
        game = f'{round(len(self) / self.count("game"),2)} games'
        categories = f'{round(len(self) / self.count("category"),2)} categories'
        times = f"{Time(mean([x.time.seconds for x in self.data]))}"

        string = f"{system[:max_len(self[0].system)]:{max_len(self[0].system)}}"
        string += f"   {game:<30}"
        string += f"   {categories:<20}"
        string += f"   {times}"

        return string

    def str_geomean(self) -> str:
        """returns a string representing the geometric mean of the table. A geometric mean,
            according to my uninformed research, is less sensitive to extreme values and could be a good
            mean if a runner has some outliners. Only the int, float or Time values
            are calculated.

            Uses the count method."""

        def max_len(tostr):
            return len(str(tostr))

        times = f"{Time(geomean([x.time.seconds for x in self.data]))}"

        string = f'{"":{max_len(self[0].system) + 56}}'
        string += f"   {times}"

        return string


class Table_pb(Table_run):
    def __init__(self, list_runs: list, include_lvl: bool):
        self.data = []
        for no, data in enumerate(list_runs, start=1):
            if include_lvl == bool(data["run"]["level"]):
                self.data.append(PB(data))
            print(f"{no}/{len(list_runs)} PBs processed!")

    def str_sum(self):
        sum_delta = str(Time(sum([x.delta.seconds for x in self.data])))
        sum_place = sum([x.leaderboard.place for x in self.data])
        sum_lb = sum([len(x.leaderboard) for x in self.data])
        sum_perc = sum([x.time.seconds for x in self.data])/sum([x["WR"].seconds for x in self.data])
        sum_lb_perc = (sum_lb - sum_place)/sum_lb
        return super().str_sum() + f' +{str(sum_delta).lstrip()} ({sum_perc:.2%})  {sum_place:>4}/{sum_lb:<4} ({sum_lb_perc:.2%})'

    def str_mean(self):
        sum_delta = str(Time(mean([x.delta.seconds for x in self.data])))
        sum_place = int(mean([x.leaderboard.place for x in self.data]))
        sum_lb = int(mean([len(x.leaderboard) for x in self.data]))
        sum_perc = mean([x.time.seconds for x in self.data])/mean([x["WR"].seconds for x in self.data])
        sum_lb_perc = (sum_lb - sum_place)/sum_lb
        return super().str_mean() + f' +{str(sum_delta).lstrip()} ({sum_perc:.2%})  {sum_place:>4}/{sum_lb:<4} ({sum_lb_perc:.2%})'

    def str_geomean(self):
        sum_delta = str(Time(geomean([x.delta.seconds for x in self.data if x.delta.seconds != 0])))
        sum_place = int(geomean([x.leaderboard.place for x in self.data]))
        sum_lb = int(geomean([len(x.leaderboard) for x in self.data]))
        sum_perc = geomean([x.time.seconds for x in self.data])/geomean([x["WR"].seconds for x in self.data])
        sum_lb_perc = (sum_lb - sum_place)/sum_lb
        return super().str_geomean() + f' +{str(sum_delta).lstrip()} ({sum_perc:.2%})  {sum_place:>4}/{sum_lb:<4} ({sum_lb_perc:.2%})'
