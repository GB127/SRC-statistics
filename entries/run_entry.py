from code_SRC.api import api
from copy import copy


class Run:
    def __init__(self, data:dict):
        # self.__dict__ = data
        self.game = api.game(data["game"])
        self.category = api.category(data["category"])
        self.emu = data["system"]["emulated"]
        self.region = data["system"]["region"]
        self.system = api.system(data["system"]["platform"])
        self.time = data["times"]["primary_t"]

    def __str__(self):
        time_str = lambda x : f'{int(x)//3600:>3}:{int(x) % 3600 // 60:02}:{int(x) % 3600 % 60 % 60:02}'

        liste = []
        for attribute in ["system", "game","category", "time"]:
            if isinstance(self[attribute], int) and "time" in attribute:
                liste.append(time_str(self[attribute]))
            else:
                liste.append(self[attribute])
        return "   ".join(liste)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __add__(self, other):
        copie = copy(self)
        if isinstance(other, int) and other == 0:
            return copie
        for attribute in self.__dict__:
            if isinstance(copie[attribute] , bool):
                continue
            elif isinstance(copie[attribute] , int):
                copie[attribute] += other[attribute]
            elif copie[attribute] == other[attribute]:
                continue
            elif not isinstance(copie[attribute], set):
                copie[attribute] = {copie[attribute], other[attribute]}
            else:
                copie[attribute].add(other[attribute])

        return copie

    def __truediv__(self, denom):
        copie = copy(self)
        for attribute in self.__dict__:
            if isinstance(copie[attribute], bool):
                continue
            elif isinstance(copie[attribute], int):
                copie[attribute] /= denom
            elif isinstance(copie[attribute], set):
                copie[attribute] = f'{len(copie[attribute]) / denom} {attribute}'
        return copie

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __lt__(self, other):
        return self.time < other.time
