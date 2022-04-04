from entries.lb_entry import Rank
from tables.leaderboard import LB
from code_SRC.api import api

class PB(Rank):
    def __init__(self, data):
        category_id = data["run"]["category"]
        game_id = data["run"]["game"]
        sub_cat_ids = {}
        for field, selection in data["run"]["values"].items():
            if field in api.subcat_db:
                sub_cat_ids[field] = selection
        level_id = None
        if data["run"]["level"]: level_id = data["run"]["level"]
        self.leaderboard = LB(api.leaderboard(game_id, category_id, sub_cat_ids, level_id))
        super().__init__(data, self.leaderboard.WR)

        if isinstance(self.leaderboard, LB):
            self["LB %"] = (len(self.leaderboard) - self.place)/len(self.leaderboard)
        elif isinstance(self.leaderboard, (int, float)):
            self["LB %"] = (self.leaderboard - self.place)/self.leaderboard

    def __str__(self):
        time_str = lambda x : f'{int(x)//3600:>3}:{int(x) % 3600 // 60:02}:{int(x) % 3600 % 60 % 60:02}'
        inted_lb = self.leaderboard if isinstance(self.leaderboard, (float, int)) else len(self.leaderboard)
        system = f'{self.system[:4]:4}'
        game= f'{self.game[:20]:20}'
        category = f'{self.category[:20]:20}'
        WR_time = f'{time_str(self["WR time"]):10} +{time_str(self["delta WR"])}'
        time = f'{time_str(self.time):10} ({self["WR %"]:.2%})'
        rank = f'{int(self.place):>4}/{int(inted_lb):<4}  {self["LB %"]:.2%}'
        return "   ".join([system, game, category,WR_time,  time, rank])