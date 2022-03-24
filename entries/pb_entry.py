from entries.rank_entry import Rank
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

    def __str__(self):
        time_str = lambda x : f'{int(x)//3600:>3}:{int(x) % 3600 // 60:02}:{int(x) % 3600 % 60 % 60:02}'
        inted_lb = self.leaderboard if isinstance(self.leaderboard, (float, int)) else len(self.leaderboard)
        p = [4, 20,20, 30 ,10, 9, 8]
        liste = []
        for no, attribute in enumerate(["system", "game","level", "category","WR time", "time"]):
            if isinstance(self[attribute], (float,int)):
                liste.append(f'{time_str(self[attribute])[:p[no]]:>{p[no]}}')
            elif isinstance(self[attribute], set):
                tempo = f'{str(len(self[attribute]))} {attribute}'[:p[no]]
                liste.append(f'{tempo:{p[no]}}')
            elif attribute == "level" and not self[attribute]: 
                continue

            else:
                liste.append(f'{self[attribute][:p[no]]:{p[no]}}')
        string =  "   ".join(liste)
        string += f' ({self["WR %"]:.2%})'
        rank = f'{int(self.place):>4}/{int(inted_lb):<4}'
        string += f'    {rank:^9}'
        string += f'    ({int(inted_lb - self.place)/int(inted_lb):.2%})'
        return string
