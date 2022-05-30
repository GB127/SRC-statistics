from entries.run import PB, Run
from code_SRC.composantes import Time
from plots.handler import window_handler
from plots.histo import Histo_app
from plots.pie import Pie_app
from copy import deepcopy
from statistics import mean, geometric_mean as geomean
from tables.base import Base_table
import itertools


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

    def all_value_key(self, key):
        assert key in self.keys()
        if key in ["level", "time", "delta", "perc", "perc_lb", "leaderboard"]:
            return
        elif key == "series":
            return set(itertools.chain(*[x[key] for x in self.data]))
        return {x[key] for x in self.data}

    def match_key_value(self, key, wanted_value):
        if key == "series":
            return [
                x
                for x in self.data
                if any([one_serie == wanted_value for one_serie in x[key]])
            ]
        return [x for x in self.data if x[key] == wanted_value]

    def methods(self):  # pragma: no cover
        return self.sort, self.pie, self.histo

    def pie(self):  # pragma: no cover
        window_handler(self.data, Pie_app)

    def histo(self):  # pragma: no cover
        window_handler(self.data, Histo_app)

    def create_grouped(self, infos):
        sum_class = deepcopy(self[0])
        sum_class.gamecat.game.game = f""
        sum_class.gamecat.category = f""
        sum_class.gamecat.subcategory = ""
        sum_class.time = Time(infos["time"])
        sum_class.system.system = f""
        return sum_class


class Table_pb(Table_run):
    def __init__(self, list_runs: list, include_lvl: bool):
        self.data = []
        for no, data in enumerate(list_runs, start=1):
            if include_lvl == bool(data["run"]["level"]):
                self.data.append(PB(data))
            print(f"{no}/{len(list_runs)} PBs processed!")

    def methods(self):  # pragma: no cover
        return self.sort, self.pie, self.histo, self.open_leaderboard

    def sum(self):
        def new_ranking():
            return list(itertools.chain(*[x.leaderboard.ranking for x in self.data]))

        def new_place():
            return sum([x.leaderboard.place for x in self.data])

        def new_WR():
            return sum([x.leaderboard.WR for x in self.data])

        LB_copy = deepcopy(self.data[0].leaderboard)
        dicto = super().sum()
        LB_copy.ranking = new_ranking()
        LB_copy.place = new_place()
        LB_copy.WR = new_WR()
        dicto["leaderboard"] = LB_copy
        return dicto

    def mean(self):
        def new_ranking():
            new_len = int(mean([len(x.leaderboard) for x in self.data]))
            return list(itertools.chain(*[x.leaderboard.ranking for x in self.data]))[
                :new_len
            ]

        def new_place():
            return int(mean([x.leaderboard.place for x in self.data]))

        def new_WR():
            return mean([x.leaderboard.WR for x in self.data])

        LB_copy = deepcopy(self.data[0].leaderboard)
        dicto = super().mean()
        LB_copy.ranking = new_ranking()
        LB_copy.place = new_place()
        LB_copy.WR = new_WR()
        dicto["leaderboard"] = LB_copy
        return dicto

    def geomean(self):
        def new_ranking():
            new_len = int(geomean([len(x.leaderboard) for x in self.data]))
            return list(itertools.chain(*[x.leaderboard.ranking for x in self.data]))[
                :new_len
            ]

        def new_place():
            return int(geomean([x.leaderboard.place for x in self.data]))

        def new_WR():
            return geomean([x.leaderboard.WR for x in self.data])

        LB_copy = deepcopy(self.data[0].leaderboard)
        dicto = super().geomean()
        LB_copy.ranking = new_ranking()
        LB_copy.place = new_place()
        LB_copy.WR = new_WR()
        dicto["leaderboard"] = LB_copy
        return dicto

    def create_grouped(self, infos):
        sum_class = super().create_grouped(infos)
        sum_class.delta = Time(infos["delta"])
        sum_class.leaderboard = infos["leaderboard"]
        sum_class.perc = sum_class.time / sum_class.leaderboard["WR"]
        return sum_class

    def open_leaderboard(self):  # pragma: no cover
        command = input(f"Which leaderboard? [0-{len(self) -1}] ")
        self[int(command) - 1].leaderboard()
