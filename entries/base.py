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
            if copie[attribute] is None:
                continue
            if isinstance(copie[attribute] , bool):
                continue
            elif isinstance(copie[attribute] , (set,str)):
                if copie[attribute] == other[attribute]:
                    continue
                if not isinstance(copie[attribute], set):
                    copie[attribute] = {copie[attribute], other[attribute]}
                else:
                    copie[attribute].add(other[attribute])
            else:
                copie[attribute] += other[attribute]

        return copie

    def __truediv__(self, denom):
        copie = copy(self)
        for attribute in self.__dict__:
            if isinstance(copie[attribute], bool):
                continue
            elif isinstance(copie[attribute], (int, float)):
                copie[attribute] /= denom
            elif isinstance(copie[attribute], set):
                copie[attribute] = f'{len(copie[attribute]) / denom:.2}'
            elif isinstance(copie[attribute], str):
                copie[attribute] = f'{1 / denom :.2} {attribute}'
        return copie

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
