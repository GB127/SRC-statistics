from entries.rank_entry import Rank
from tables.leaderboard import LB
from code_SRC.api import api

class PB(Rank):
    def __init__(self, data):
        category_id = data["run"]["category"]
        game_id = data["run"]["game"]
        sub_cat_ids = data["run"]["values"]
        self.leaderboard = LB(api.leaderboard(game_id, category_id, sub_cat_ids))
        super().__init__(data, 400)
