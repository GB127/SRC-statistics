from allRuns import Runs, Run
from api import get_leaderboard
from leaderboard import leaderboard
from tools import run_time, command_select, clear, plot_histo


class PBs(Runs):
    def __init__(self, data):
        print("Initializing PBs data")
        self.data = []
        for pb in data:
            self.data.append(PB(pb))


    # STRING RELATED
    def __str__(self):
        return f'{len(self)} PBs ({sum([x.time for x in self.data]).days()})'

    def get_header(self):
        types = super().get_header()
        types.remove("leaderboard")
        types.remove("WR")
        return types


    def foot(self):  #TODO: Redo this
        string1, string2, string3, string4 = super().foot().split("\n")
        
        total_time = sum([pb.time for pb in self.data])
        total_wr = sum([pb.WR for pb in self.data])

        percentage = round(100* total_time / total_wr, 2)

        total_deltaWR = sum([pb.delta_WR for pb in self.data])

        string1 += "-" * 46
        string2 += f' |+ {total_deltaWR} |  {percentage} % |'
        string3 += f' |+ {run_time(total_deltaWR / len(self))}  |  {percentage} % |'





        return "\n".join([string1, string2, string3])





    def stats_leaderboard(self):
        clear()
        which = command_select(self.data, printer=True)
        which.leaderboard()

    def methods(self):
        metho = super().methods()
        metho["Leaderboard"] = self.stats_leaderboard
        return metho

    def plot_histo(self):
        command = command_select(["WR%", "delta_WR", "time"], printer=True)
        if command == "WR%":
            plot_histo(sorted([one.perc_WR for one in self.data]), "Histogram of %WR", typ="%", min_data=100)
        if command == "time":
            tempo = sorted([one.time.time for one in self.data])
            plot_histo(tempo, "Histogram of PBs time", typ="time")
        elif command == "delta_WR":
            tempo = sorted([one.delta_WR.time for one in self.data])
            plot_histo(tempo, "Histogram of PBs-WR deltas", typ="time")



class PB(Run):
    table_size = Run.table_size + [2, 3, 5, 1]

    def sortable(self):
        tempo = super().sortable()
        tempo.remove("leaderboard")
        return tempo

    def __init__(self, data):
        super().__init__(data["run"])
        self.place = data["place"]
        self.leaderboard = leaderboard(self.IDs, self.game, self.category, self.place, self.level)
        self.WR = self.leaderboard.WR
        self.delta_WR = self.time - self.WR
        self.perc_WR = round((self.time) / self.WR * 100, 2)
        self.perc_LB = round((len(self.leaderboard) - self.place) / len(self.leaderboard) * 100,2)

    def __str__(self):
        return super().__str__() + " | ".join([
                                    f'+ {self.delta_WR:<8}',
                                    f'{str(self.perc_WR) + " %":>9}',
                                    f"{f'{self.place}/{len(self.leaderboard)}':9}",
                                    f"{self.perc_LB:6} %"]) + "|"
