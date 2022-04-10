from entries.one_run import Run


class Rank(Run):
    """Class related to one entry in a leaderboard. TODO : Remove inheritance to Run because we don't need all these infos
        Attributes:
            place (int) : Place of the object on a specific leaderboard.
                self.place = 3 means the entry is 3rd on the leaderboard
            min/rk (float) : Average time to gain 1 rank on the leaderboard
                min/rk = 5 => In average, the runner need to improve 5 seconds in order to move up in the leaderboard for one place
                    NOTE : equalizing an another run is considered moving up a rank.

            WR time (float) : WR time of the leaderboard, in seconds
                (TODO : Remove this attribute for Rank)
            delta WR (float): Difference of the time compared to WR, in seconds
                delta WR = 5 means the rank is 5 secondes behind WR
            WR % (float) : % of the time compared to WR
                self["WR %"] = 2 means the rank is 200% longer than the WR
                self["WR %"] = 1 means the rank is the WR
        """

    def __init__(self, data: dict, WR_time: float):
        """Args:
            data (dict): Informations received from SRC's api.
                keys:
            WR_time (float): WR time of the leaderboard, in seconds
            """
        super().__init__(data["run"])
        self.place = data["place"]
        self["WR time"] = WR_time
        self["WR %"] = self.time / self["WR time"]
        self["delta WR"] = self.time - self["WR time"]
        self["min/rk"] = 0
        if self.place > 1:
            self["min/rk"] = self["delta WR"] / (self.place - 1)

    def __str__(self):
        time_str = lambda x: f"{int(x)//3600:>3}:{int(x) % 3600 // 60:02}:{int(x) % 3600 % 60 % 60:02}"
        return "   ".join(map(str,  [
                                        time_str(self.time),
                                        f'+{time_str(self["delta WR"]).lstrip()}',
                                        f'({self["WR %"]:.2%})',
                                        f'{time_str(self["min/rk"]).lstrip()}'
                                    ]
                            )
                        )
