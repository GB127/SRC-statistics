from .api import api

#from api import api
from copy import copy


class Run:
    def __init__(self, data:dict):
        self.__dict__ = data
        self["game"] = api.game(self["game"])
        self["category"] = api.category(self["category"])
        self["system"] = api.system(self["system"]["platform"])
        self["time"] = self["times"]["primary_t"]
        for unwanted in ["id", "weblink", "videos","level", "values", "submitted", "splits", "links", "comment", "times", "players", "status"]:
            del self.__dict__[unwanted]

    def __str__(self):
        string = " ".join([str(self[x]) for x in ["game", "time", "system"]])
        return string

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __add__(self, other):
        copie = copy(self)
        if other == 0:
            return copie
        for attribute in self.__dict__:
            copie[attribute] += other[attribute]
        return copie


    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __lt__(self, other):
        return self.time < other.time


if __name__== "__main__":
    run_base = {'id': 'z073gloy', 'weblink': 'https://www.speedrun.com/bhero/run/z073gloy', 'game': 'nd2eeqd0', 'level': None, 'category': 'zd3yzr2n', 'videos': {'links': [{'uri': 'https://www.twitch.tv/videos/1110770410'}]}, 'comment': 'Blind race. Stellar hitboxes right here.', 'status': {'status': 'verified', 'examiner': '98rpeqj1', 'verify-date': '2021-08-08T19:00:00Z'}, 'players': [{'rel': 'user', 'id': 'x7qz6qq8', 'uri': 'https://www.speedrun.com/api/v1/users/x7qz6qq8'}], 'date': '2021-08-06', 'submitted': '2021-08-07T05:35:16Z', 'times': {'primary': 'PT4H2M40S', 'primary_t': 14560, 'realtime': 'PT4H2M40S', 'realtime_t': 14560, 'realtime_noloads': None, 'realtime_noloads_t': 0, 'ingame': None, 'ingame_t': 0}, 'system': {'platform': 'nzelreqp', 'emulated': False, 'region': 'pr184lqn'}, 'splits': None, 'values': {}, 'links': [{'rel': 'self', 'uri': 'https://www.speedrun.com/api/v1/runs/z073gloy'}, {'rel': 'game', 'uri': 'https://www.speedrun.com/api/v1/games/nd2eeqd0'}, {'rel': 'category', 'uri': 'https://www.speedrun.com/api/v1/categories/zd3yzr2n'}, {'rel': 'platform', 'uri': 'https://www.speedrun.com/api/v1/platforms/nzelreqp'}, {'rel': 'region', 'uri': 'https://www.speedrun.com/api/v1/regions/pr184lqn'}, {'rel': 'examiner', 'uri': 'https://www.speedrun.com/api/v1/users/98rpeqj1'}]}
    test = Run(run_base)
    print(test)