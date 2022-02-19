from copy import copy

class Base_Entry:
    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __radd__(self, other):
        return self + other

    def __add__(self, other):
        copie = copy(self)
        if isinstance(other, int):
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
                copie[attribute] = len(copie[attribute]) / denom
        return copie

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __lt__(self, other):
        return self.time < other.time
