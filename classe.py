from api import *
import datetime
import isodate
import matplotlib.pyplot as plot
import numpy

class runner:
    def __init__(self, username):
        self.runs = {}
        for run in get_runs(username, True):
            print(Run(run))
    def __str__(self):
        plot.plot([1, 2, 3, 4])
        plot.ylabel('some numbers')
        plot.show()
        return "plot closed"

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
        self.time = isodate.parse_duration(info["times"]["primary"])
        self.system = f'{info["system"]["platform"]}'

    def __str__(self):
        return f'{self.game} ({self.category}) {self.time}'