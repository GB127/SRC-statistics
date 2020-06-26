from api import *
import datetime
import isodate
import matplotlib.pyplot as plot
import numpy

class runner:
    def __init__(self, username):
        self.runs = {}
        for run in get_runs(username, True):
            tempo = Run(run)
            if self.runs.get(tempo.game) is None:
                self.runs[tempo.game] = {}
            if self.runs[tempo.game].get(tempo.category) is None:
                self.runs[tempo.game][tempo.category] = []
            self.runs[tempo.game][tempo.category].append(tempo.time)

    def __str__(self):
        pass
    def plot_all(self):
        for game in self.runs:
            for category in self.runs[game]:
                if len(self.runs[game][category]) > 1:
                    self.runs[game][category].sort(reverse=True)
                    plot.plot(self.runs[game][category], label=f'{game} - {category}')
        plot.legend()
        plot.xlabel("PB #")
        plot.ylabel("PB time")
        plot.show()

    def plot(self):
        listofgames = []
        for no, game in enumerate(self.runs):
            listofgames.append(game)
            print(f'{no} - {game}')
        game = listofgames[int(input("Which game do you want to plot? "))]
        listofcat = []
        for no, cat in enumerate(self.runs[game]):
            listofcat.append(cat)
            print(f'{no} - {cat}')
        category = listofcat[int(input("Which category do you want to plot? "))]

        self.runs[game][category].sort(reverse=True)
        plot.plot(self.runs[game][category])
        plot.xlabel("PB #")
        plot.ylabel("Time")

        plot.show()



WRs = {}


class Run:
    def __init__(self, info):
        """
            Structure of info: dicto
                id          NOPE
                weblink     NOPE
                game        OK
                level       NOPE
                category    OK  
                videos      NOPE
                comment     NOPE
                status      maybe
                players     NOPE
                date        NOPE
                submitted   NOPE
                times       OK
                system      OK
                splits      NOPE
                values      NOPE
                links       NOPE
        """
        self.game = get_game(info["game"])
        self.category = get_category(info["category"])
        self.time = isodate.parse_duration(info["times"]["primary"]).total_seconds()

        if WRs.get(self.game) is None:
            WRs[self.game] = {}
        if WRs[self.game].get(self.category) is None:
            WRs[self.game][self.category] = isodate.parse_duration(get_WR(info["game"], info["category"]))

        self.system = f'{info["system"]["platform"]}'

    def __str__(self):
        return f'{self.game} ({self.category}) {self.time}'