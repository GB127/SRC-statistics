from api import get_leaderboard, get_user, get_leaderboard_level, get_leaderboards
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
        self.IDs = IDs
        self.game = game
        self.category = category
        self.place = rank
        if not IDs[2]:
            print(f"Initializing {self.game} - {self.category}'s leaderboard data")
            infos = get_leaderboard(IDs)["data"]["runs"]
        else:
            print(f"Initializing {self.game} - {level} - {self.category}'s leaderboard data")
            infos = get_leaderboard_level(IDs)["data"]["runs"]
        self.data = []
        self.WR = run_time(infos[0]["run"]["times"]["primary_t"])
        for no, one in enumerate(infos):
            self.data.append(entry(one, self.WR, no==rank -1))

    def methods(self):
        return {"Plot the position" : self.plot,
                "Plot the leaderboard evolution" : self.plot_evolution,
                "end": "end"}
    
    def plot_evolution(self):
        if not self.IDs[2]:
            toplot = get_leaderboards(self.IDs)
            plot_line(toplot.values(), f"{self.game} - {self.category}\nLeaderboard evolution\n{min(toplot.keys())}-{max(toplot.keys())}", mirror=True)
        if self.IDs[2]:
            pass

    def __len__(self):
        return len(self.data)

    def plot(self):
        plot_line([[x.time for x in self.data[::-1]]], f'{self.game} - {self.category}', ymin=None)

    def head(self):
        tempo = super().head()
        return f'{self.game} - {self.category} | {len(self)} runs\n' + tempo


class entry:
    table_size = [10,10]
    def __init__(self, data, WR, place=False):
        self.user = place
        self.WR = WR
        self.place = data["place"]
        # WONTFIX : The thing with the current api is that it returns IDs. If I want all of them I have to update all of them...
        #try:
        #    self.player = [data["run"]["players"][0]["id"]]  # TODO: For now solo runs only
        #except KeyError:
        #    self.player = data["run"]["players"][0]["name"]  # TODO: For now solo runs only
        self.time = run_time(data["run"]["times"]["primary_t"])
        self.delta = self.time - self.WR

        if self.place != 1:
            self.moy_rank = run_time((self.time-self.WR) / (self.place-1))
        else:
            self.moy_rank = run_time(0)
        self.perc = round(self.time / self.WR * 100, 2)


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
    test.plot_evolution()