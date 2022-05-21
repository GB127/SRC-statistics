from copy import deepcopy
from code_SRC.api import api
from code_SRC.composantes import Time
from statistics import mean, geometric_mean as geomean, median

class LB:
    def __init__(self,place, game_id, level_id, category_id, subcat_ids):
        if level_id:
            self.ranking = tuple(api.leaderboard_l(game_id, level_id, category_id, subcat_ids))
        else:
            self.ranking = tuple(api.leaderboard(game_id, category_id, subcat_ids))
        self.place = place
        self.WR = self.ranking[0]

    def __str__(self):
        return f'{self.place:>4}/{len(self):<4} ({(len(self) - self.place)/len(self):6.2%})'
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
            input("Finish? press enter when yes")
            break
    
    
    
    def str_lb(self):
        def median_index():
            differences = [abs(x - median(self.ranking)) for x in self.ranking]
            median_ind = differences.index(min(differences))
            return median_ind

        def mean_index():
            differences = [abs(x - mean(self.ranking)) for x in self.ranking]
            mean_ind = differences.index(min(differences))
            return mean_ind
        def geomean_index():
            differences = [abs(x - geomean(self.ranking)) for x in self.ranking]
            mean_ind = differences.index(min(differences))
            return mean_ind
        string = ""
        for rank, run_time in enumerate(self.ranking, start=1):
            delta = Time(run_time) - self["WR"]
            string += f'{rank:4}   {Time(run_time)} + {delta} ({Time(run_time) / self["WR"]:.2%}) {delta / (rank-1 if rank != 1 else 1)}'
            if self.place == rank:
                string += "<---Runner"
            if rank - 1 == mean_index():
                string += "<---Mean"
            if rank - 1  == geomean_index():
                string += "<---Geomean"
            if rank - 1  == median_index():
                string += "<---Median"

            string += "\n"
        string += f'Sum    {Time(sum(self.ranking))}\n'
        string += f'Mean   {Time(mean(self.ranking))}\n'
        string += f'Geomean{Time(geomean(self.ranking))}\n'
        string += f'Median{Time(median(self.ranking))}'

        return string





    def __eq__(self, other):
        return all([self.ranking == other.ranking, self.place == other.place])