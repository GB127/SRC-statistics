from api import get_leaderboard2, get_user
from generic import table
from tools import run_time
import matplotlib.pyplot as plot
from copy import deepcopy


class leaderboard(table):
    filter = 600

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
        leaderboard.filter = 600
        self.filter_data()


    def change_filter(self):
        while True:
            try:
                leaderboard.filter = int(input("Enter a number >100 %: "))
                if leaderboard.filter > 100:
                    break
            except:
                pass
        self.filter_data()



    def __init__(self, IDs, game, category, rank):
        self.game = game
        self.category = category
        self.place = rank
        print(f"Initializing {self.game} - {self.category}'s leaderboard data")
        infos = get_leaderboard2(IDs)["data"]["runs"]
        self.backup = []
        self.WR = run_time(infos[0]["run"]["times"]["primary_t"])
        for no, one in enumerate(infos):
            self.backup.append(entry(one, self.WR, no==rank -1))
        self.filter_data()

    def methods(self):
        return {"Plot the position" : self.plot,
                "Change filter" : self.change_filter,
                "end": "end"}

    def filter_data(self):
        backup = deepcopy(self.backup)
        self.data = []
        self.removed = []
        for entry in backup:
            if entry.perc > leaderboard.filter:
                self.removed.append(entry)
            else:
                self.data.append(entry)


    def __len__(self):
        return len(self.data)

    def plot(self):
        plot.plot([x.time.time for x in self.data[::-1]])
        if len(self) > self.place:
            plot.plot([len(self) - self.place], [self.data[self.place-1].time.time], 'o', color="red")
        plot.title(f'{self.game} - {self.category}')
        plot.yticks(plot.yticks()[0],[str(run_time(x)) for x in plot.yticks()[0]])
        plot.show()

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
    test = ['j1l9qz1g', '9d85yqdn', {}]
    test = leaderboard(test, "Ocarina of time", "GSR", 2)
    test()