from entries.one_run import Run

class Rank(Run):
    def __init__(self, data:dict, WR_time:int):
        super().__init__(data["run"])
        self.place = data["place"]
        self["WR time"] = WR_time
        self.update_data()

    def update_data(self):
        self["WR %"] = self.time / self["WR time"]
        self["delta WR"] = self.time - self["WR time"]

    def __add__(self, other):
        tempo = super().__add__(other)
        tempo["WR %"] = tempo.time / tempo["WR time"]

        return tempo

    def __truediv__(self, other):
        tempo = super().__truediv__(other)
        tempo["WR %"] = tempo.time / tempo["WR time"]

        return tempo



    def __str__(self):  #TODO: use the new attri
        time_str = lambda x : f'{int(x)//3600:>3}:{int(x) % 3600 // 60:02}:{int(x) % 3600 % 60 % 60:02}'
        return "   ".join(map(str, [time_str(self.time),f'-{time_str(self.time - self["WR time"]).lstrip()}', f'{self["WR %"]:.2%}']))