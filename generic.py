from tools import command_select, run_time, clear
from copy import deepcopy

def formatting(cle, valeur, which):
    tostr = {"cle":cle, "valeur":valeur}
    if "count" in cle:
        if which == "cle":
            return f'{"#":^3}'
        return f'{tostr[which]:^3}'
    elif isinstance(valeur, run_time):
        tempo = ""
        if "delta" in cle:
            tempo = "+"
        return f'{tempo + str(tostr[which])[:9]:>9}'
    elif cle == "game":
        return f'{tostr[which][:30]:30}'
    elif cle == "system":
        return f'{tostr[which][:6]:^6}'
    elif cle == "category":
        return f'{tostr[which][:20]:20}'
    elif cle == "level":
        return f'{tostr[which][:12]:12}'

    elif "perc" in cle:
        tempo = "" if which == "cle" else " %"
        tempo2 = str(tostr[which])
        if tempo2[-2] == "." :
            tempo2 += "0"
        return f'{ tempo2 + tempo:>9}'
    elif cle == "ranking":
        return f'{tostr[which]:^10}'

class table:

    def __init__(self):
        if self.__class__.__name__ != "leaderboard":
            print(f"Prepping the {self.__class__.__name__} table...")
        self.backup = []
        self.data = []

    def __str__(self):
        def head():
            head_prep = []
            for cle , valeur in self.data[0].__dict__.items():
                if cle in ["leaderboard", "place", "IDs", "runs", "pbs"]:
                    pass
                elif "average" in cle:
                    pass
                elif cle == "level":
                    pass
                else:
                    head_prep.append(formatting(cle, valeur, "cle"))

            return f"{'':4}|" + " | ".join(head_prep)

        line = f'{"-" * len(str(self.data[0]))}-----'

        body = ""
        for no, x in enumerate(self.data):
            body += f"{no+1:>3} |{x}\n"

        total = str(sum(self))
        average = str(sum(self) / len(self))

        return  f'{head()}\n{line}\n{body}{line}\nTotal{total}\nAvera{average}'

    def __call__(self):
        def methods_fetcher():
            toreturn = []
            method_list = [func for func in dir(self) if callable(getattr(self, func))]
            for method in method_list:
                if "__" not in method:
                    toreturn.append(method)
            return toreturn + ["end"]

        while True:
            clear()
            self.data.sort()
            print(self)
            command = command_select(methods_fetcher(), printer=True)
            if command == "end":
                break
            getattr(self.__class__, command)(self)


    def change_sorting(self):
        sortables = list(self.data[0].__dict__.keys())
        for not_sortable in ["IDs", "runs", "pbs"]:
            if not_sortable in sortables: sortables.remove(not_sortable)
        new_sorter = command_select(sortables, printer=True)
        if new_sorter != "end":
            self.data[0].__class__.sorter = new_sorter



    # Basic stuffs for making the stuff an iterable and all.
    def __getitem__(self, argument):
        return self.data[argument]
    def __iter__(self):
        return iter(self.data)        
    def __len__(self):
        return len(self.data)


class entry:
    def __str__(self):
        tempo = []
        for cle, valeur in self.__dict__.items():
            if cle in ["leaderboard", "place", "IDs", "runs", "pbs"]:
                pass
            else:
                tempo.append(formatting(cle, valeur, "valeur"))
        return " | ".join(tempo)


    def __add__(self, other):
        tempo = deepcopy(self)
        if other == 0:
            return tempo
        for cle, value in self.__dict__.items():
            if isinstance(value, run_time):
                tempo.__dict__[cle] += other.__dict__[cle]
            elif isinstance(value, int) or isinstance(value, float):
                tempo.__dict__[cle] += other.__dict__[cle]
            elif cle == "leaderboard":
                tempo.__dict__[cle] += other.__dict__[cle]
            else:
                tempo.__dict__[cle] = ""
        return tempo

    __radd__ = __add__

    def __truediv__(self, integ):
        tempo = deepcopy(self)
        for cle, value in tempo.__dict__.items():
            if isinstance(value, run_time):
                tempo.__dict__[cle] = run_time(tempo.__dict__[cle] / integ)
            elif isinstance(value, int) or isinstance(value, float):
                tempo.__dict__[cle] /= integ
                if "count" in cle:
                    tempo.__dict__[cle] = int(tempo.__dict__[cle])

            else:
                pass
        return tempo


    def __lt__(self, other):
        if self.__dict__[self.sorter] != other.__dict__[self.sorter]:
            return self.__dict__[self.sorter] < other.__dict__[self.sorter]
        for attribut in ["system", "game", "category","level", "time"]:
            try:
                if self.__dict__[attribut] != other.__dict__[attribut]:
                    return self.__dict__[attribut] < other.__dict__[attribut]
            except KeyError:
                pass
            except TypeError:
                raise TypeError(f'\n{self}\n{other}\n{list(self.__dict__.keys())}')                
        raise BaseException(f'\n{self}\n{other}\n{list(self.__dict__.keys())}')