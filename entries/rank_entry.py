from entries.run_entry import Run

class Rank(Run):
    def __init__(self, data:dict, WR_time:int):
        super().__init__(data["run"])
        self.place = data["place"]
        self.WR = WR_time
        self.WR_perc = self.time / WR_time

    def __str__(self):
        time_str = lambda x : f'{int(x)//3600:>3}:{int(x) % 3600 // 60:02}:{int(x) % 3600 % 60 % 60:02}'
        return "   ".join(map(str, [time_str(self.time),f'-{time_str(self.time - self.WR).lstrip()}', f'{self.WR_perc:.2%}']))