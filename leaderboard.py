from api import get_leaderboard2, get_user
from generic import table
from tools import run_time

class leaderboard(table):
    def __init__(self, IDs, game, category):
        self.game = game
        self.category = category
        print(f"Initializing {self.game} - {self.category}'s leaderboard data")
        infos = get_leaderboard2(IDs)["data"]["runs"]
        self.data = []

        self.WR = run_time(infos[0]["run"]["times"]["primary_t"])
        for one in infos:
            self.data.append(entry(one, self.WR))

    def __len__(self):
        return len(self.data)



    def head(self):
        tempo = super().head()
        return f'{self.game} - {self.category} | {len(self)} runs\n' + tempo


class entry:
    table_size = [10,10]
    def __init__(self, data, WR):
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
        return " | ".join(tempo)

    def __lt__(self, other):
        return self.time < other.time


if __name__ == "__main__":
    test = ['j1l9qz1g', '9d85yqdn', {}]
    test = leaderboard(test, "Ocarina of time", "GSR")
    test()