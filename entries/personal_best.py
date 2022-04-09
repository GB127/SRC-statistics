from entries.lb_entry import Rank
from tables.leaderboard import LB
from code_SRC.api import api

class PB(Rank):
    """Class related to one PB on SRC.
        Attributes:
            game (str): Game of the speedrun
                example: Super Mario 64

            level (str or None) : Level of the speedrun, if the run is on a level. If the run is not on a level, the value is None
                example : Dragon Roost Cavern (a dungeon in Zelda: Wind Waker)

            category (str): Category of the speedrun. String in parenthesis is the subcategory if there is one.
                example : 120 stars (WII VC)

            emu (bool): True if run is ran on an emulator. False otherwise

            region (str): Region of the game being ran.
                example : USA / NTSC

            system (str): System of the run.
                example : Gamecube

            time (float) : Time of the speedrun, in seconds.

            place (int) : Place of the object on a specific leaderboard.
                self.place = 3 means the entry is 3rd on the leaderboard

        WR time (float) : WR time of the leaderboard, in seconds

        delta WR (float): Difference of the time compared to WR, in seconds
            delta WR = 5 means the rank is 5 secondes behind WR

        WR % (float) : % of the time compared to WR
            self["WR %"] = 2 means the rank is 200% longer than the WR
            self["WR %"] = 1 means the rank is the WR

    """
    def __init__(self, data):
        """

        Args:
            data (dict): Informations received from SRC's api.
                keys:
        """

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
        self["LB %"] = (len(self.leaderboard) - self.place)/len(self.leaderboard)
        del self.__dict__["min/rk"]
    def __str__(self):
        time_str = lambda x : f'{int(x)//3600:>3}:{int(x) % 3600 // 60:02}:{int(x) % 3600 % 60 % 60:02}'
        inted_lb = self.leaderboard if isinstance(self.leaderboard, (float, int)) else len(self.leaderboard)

        prelim_infos = f'{self.system[:4]:4}   {self.game[:20]:20}   {self.category[:20]:20}'
        time_infos = f'{time_str(self["WR time"]):10} {time_str(self.time):10}+{time_str(self["delta WR"]).lstrip():9} ({self["WR %"]:.2%})'
        rank = f'{int(self.place):>4}/{int(inted_lb):<4}  {self["LB %"]:.2%}'
        return "   ".join([prelim_infos, time_infos, rank])