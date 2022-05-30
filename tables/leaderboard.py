from plots.handler import window_handler
from code_SRC.api import api
from code_SRC.composantes import Time
from statistics import mean, geometric_mean as geomean
from plots.lb_plot import LB_plot_app


class LB:
    def __init__(self, release, place, game_id, level_id, category_id, subcat_ids):
        self.ranking = tuple(
            api.leaderboard(game_id, level_id, category_id, subcat_ids)
        )
        self.place = place
        self.WR = self.ranking[0]
        self.ids = (game_id, level_id, category_id, subcat_ids)
        self.release = int(release)

    def __str__(self):
        return f"{self.place:>4}/{len(self):<4} ({(len(self) - self.place)/len(self):6.2%})"

    def __len__(self):
        return len(self.ranking)

    def __getitem__(self, key_index):
        if key_index == "WR":
            return Time(self.WR)
        else:
            return Time(self.ranking[key_index])

    def __call__(self):
        while True:
            print(self.str_lb())
            for index, fx in enumerate(self.methods()):
                print(index, fx.__name__)
            command = input(
                f"Select option: [0-{len(self.methods()) -1}] | Type end to exit\nInput : "
            )
            if command == "end":
                break
            self.methods()[int(command)]()

    def str_lb(self):
        moyenne = mean(self.ranking)
        geomoyenne = geomean(self.ranking)
        somme = sum(self.ranking)
        WR = self.ranking[0]

        def mean_index():
            differences = [abs(x - moyenne) for x in self.ranking]
            mean_ind = differences.index(min(differences))
            return mean_ind

        def geomean_index():
            differences = [abs(x - geomoyenne) for x in self.ranking]
            mean_ind = differences.index(min(differences))
            return mean_ind

        string = ""
        for rank, run_time in enumerate(self.ranking, start=1):
            delta = Time(run_time) - self["WR"]
            string += f'{rank:4}   {Time(run_time)} + {delta} ({Time(run_time) / self["WR"]:.2%})'
            if self.place == rank:
                string += "<---Runner"
            if rank - 1 == mean_index():
                string += "<---Mean"
            if rank - 1 == geomean_index():
                string += "<---Geomean"
            if rank == len(self) // 2:
                string += "<---Median"

            string += "\n"
        string += f"Sum    {Time(somme)} + {Time(somme) - Time(WR * len(self.ranking))} ({Time(somme) / Time(WR * len(self.ranking)):.2%})\n"
        string += f"Mean   {Time(moyenne)} + {Time(moyenne) - Time(self.ranking[0])} ({Time(moyenne) / Time(WR):.2%})\n"
        string += f"GeoM   {Time(geomoyenne)} + {Time(geomoyenne) - Time(self.ranking[0])} ({Time(geomoyenne) / Time(WR):.2%})\n"
        return string

    def methods(self):  # pragma: no cover
        return [self.plot]

    def plot(self):  # pragma: no cover
        print("Prepping informations...")
        yearly_ranking = api.past_lb(self.release, *self.ids)
        window_handler(yearly_ranking, LB_plot_app)

    def __eq__(self, other):
        return all([self.ranking == other.ranking, self.place == other.place])
