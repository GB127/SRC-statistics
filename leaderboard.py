from api import get_leaderboard, get_user, get_leaderboard_level, get_leaderboards, get_leaderboards_level
from generic import table
from tools import run_time, plot_line

class leaderboard(table):
    def foot(self):
        tempo = " | ".join([
                f'Total time  ',
                f'{sum([x.time for x in self.data])}'])

        tempo2 = " | ".join([
                f'Average time',
                f'{run_time(sum([x.time for x in self.data])/len(self))}'])


        return f'{"-" * 47}\n{tempo}\n{tempo2}'

    def __call__(self):
        super().__call__()


    def __init__(self, IDs, game, category, rank, level=None):
        super().__init__()

        self.IDs = IDs
        self.game = game
        self.category = category
        self.place = rank
        self.level = level
        if not IDs[2]:
            print(f"Fetching {self.game} - {self.category}")
            infos = get_leaderboard(IDs)["data"]["runs"]
        else:
            print(f"Fetching {self.game} - {level} - {self.category}")
            infos = get_leaderboard_level(IDs)["data"]["runs"]
        self.WR = run_time(infos[0]["run"]["times"]["primary_t"])
        for no, one in enumerate(infos):
            self.data.append(entry(one, self.WR, no==rank -1))

    def methods(self):
        return {"Truncate the leaderboard": self.filter_select,
                "Plot the position" : self.plot,
                "Plot the leaderboard evolution" : self.plot_evolution,
                "end": "end"}
    
    def filter_select(self):
        while True:
            print("Select the last entry you want to keep by entering a number.\nTo reset the filtering, enter reset\nTo cancel, type end")
            command = input()
            if command == "reset":
                self.reset_filter()
                break
            elif command == "end":
                break
            else:
                try:
                    self.filter(0, int(command))
                    break
                except:
                    pass






    def plot_evolution(self):
        if not self.IDs[2]:
            toplot = get_leaderboards(self.IDs)
            plot_line(toplot.values(), f"{self.game} - {self.category}\nLeaderboard evolution\n{min(toplot.keys())}-{max(toplot.keys())}", mirror=True)
        if self.IDs[2]:
            toplot = get_leaderboards_level(self.IDs)
            plot_line(toplot.values(), f"{self.game} - {self.level} - {self.category}\nLeaderboard evolution\n{min(toplot.keys())}-{max(toplot.keys())}", mirror=True)

    def __len__(self):
        return len(self.data)

    def plot(self):
        plot_line([[x.time for x in self.data[::-1]]], f'{self.game} - {self.category}', ymin=None)

    def head(self):
        tempo = super().head()
        return f'{self.game} - {self.category} | {len(self)} runs\n' + tempo


    def get_header(self):
        types = list(self.data[0].__dict__.keys())
        types.remove("user")
        types.remove("WR")
        types.remove("place")
        return types


class entry:
    table_size = [6,5, 5, 0]
    def __init__(self, data, WR, place=False):
        self.user = place
        self.WR = WR
        self.place = data["place"]
        self.time = run_time(data["run"]["times"]["primary_t"])
        self.delta = self.time - self.WR
        self.perc = round(self.time / self.WR * 100, 2)

        if self.place != 1:
            self.moy_rank = run_time((self.time-self.WR) / (self.place-1))
        else:
            self.moy_rank = run_time(0)






    def __str__(self):
        tempo = [f'{self.time:>9}',
                f"+{self.delta:>8}",
                f'{self.perc:<6} %',
                f'{self.moy_rank}']
        if self.user:
            tempo.append(f'<----')
        return " | ".join(tempo)

    def __lt__(self, other):
        return self.time < other.time


if __name__ == "__main__":
    test = ['j1l9qz1g', '9d85yqdn',None, {}]
    test = leaderboard(test, "Ocarina of time", "GSR", 2)
    test()