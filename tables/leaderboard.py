from code_SRC.api import api
from code_SRC.composantes import Time

class LB:
    def __init__(self,place, game_id, level_id, category_id, subcat_ids):
        if level_id:
            self.ranking = tuple(api.leaderboard_l(game_id, level_id, category_id, subcat_ids))
        else:
            self.ranking = tuple(api.leaderboard(game_id, category_id, subcat_ids))
        self.place = place
    def __str__(self):
        return f'{self.place:>4}/{len(self):<4} ({(len(self) - self.place)/len(self):6.2%})'
    def __len__(self):
        return len(self.ranking)

    def __getitem__(self, key_index):
        if key_index == "WR":
            return Time(self.ranking[0])
        else:
            return Time(self.ranking[key_index])