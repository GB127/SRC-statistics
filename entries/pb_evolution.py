from entries.one_run import Run
from entries.personal_best import PB
from entries.base_entry import Base_Entry
from copy import copy


class PB_evo(Base_Entry):
    """Class representating the evolution of a PB
        Attributes:
            game (str): Game of the speedrun
                example: Super Mario 64

            level (str or None) : Level of the speedrun, if the run is on a level. If the run is not on a level, the value is None
                example : Dragon Roost Cavern (a dungeon in Zelda: Wind Waker)

            category (str): Category of the speedrun. String in parenthesis is the subcategory if there is one.
                example : 120 stars (WII VC)

            system (str): System of the run.
                example : Gamecube

        """

    def __init__(self, pb:PB, runs:list[Run]):
        # Basic infos
        self.__dict__ = copy(pb.__dict__)
        self.__dict__["PB time"] = copy(pb.time)

        self.runs_times = tuple(sorted([x.time for x in runs if x.time > pb.time]))


        for unwanted in ["emu", "place", "region", "time", "LB %", "leaderboard"]:
            del self.__dict__[unwanted]



    def __str__(self):
        time_str = lambda x : f'{int(x)//3600:>3}:{int(x) % 3600 // 60:02}:{int(x) % 3600 % 60 % 60:02}'

        return f'{self.game} | {self.category} | {time_str(self.runs_times[0])} | {time_str(self["PB time"])} | -{time_str(self.runs_times[0]- self["PB time"])} ({(self.runs_times[0]- self["PB time"])/self.runs_times[0]:.2%}) | {time_str(self.runs_times[0] - self["WR time"])}'



