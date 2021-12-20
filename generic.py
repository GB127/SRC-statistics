from time import time
from tools import command_select, run_time, clear
from copy import deepcopy

times_format = 8
perc_format = 5
format_string = {
                    "category":13, # Ok
                    "count" : 3,
                    "delta" : times_format,
                    "delta_p" : times_format,
                    "first": times_format,
                    "game" : 30,  # Ok
                    "moy_rank" : 10,
                    "perc" : perc_format,
                    "PB_average" : times_format,
                    "PB_count" : 3,
                    "PB_delta_average" : times_format,
                    "PB_Total": times_format,
                    "PB_time" : times_format,
                    "PB_delta" : times_format,
                    "perc1st": perc_format,
                    "percmax": perc_format,
                    "perc_LB" : perc_format,
                    "perc_WR" : perc_format,
                    "Run_average" : times_format,
                    "Run_count" : 3,
                    "Run_Total": times_format,
                    "ranking" : 10,
                    "runs_count" : 3,
                    "runs_time" : times_format,
                    "system" : 3, 
                    "time" : times_format,
                    "WR" : times_format,
                    "WR_time" : times_format,
                    "WR_average" : times_format,
                    "WR_Total": times_format
                }



class table:
    def __init__(self):
        self.backup = []
        self.data = []

    def __str__(self):
        line = f'{"-" * len(str(self.data[0]))}-----'

        def head():
            head_prep = []
            for cle in self.data[0].__dict__.keys():
                if cle in ["runs", "pbs", "IDs", "leaderboard", "place"] :
                    continue
                head_prep.append(f'{cle[:min(len(cle), format_string[cle])]:{format_string[cle]}}')
                if "perc" in cle:
                    head_prep[-1] += "  "

            return f"{'':4}|" + " | ".join(head_prep)

        def body():
            body_str = ""
            for no, x in enumerate(self.data):
                body_str += f"{no+1:>3} |{x}\n"
            return body_str.rstrip()

        def foot():
            total = "Total: | " + str(sum(self)).lstrip(" |")
            average = "Average: | " + str(sum(self) / len(self)).lstrip(" |")
            return "\n".join([f'{total:>{len(str(self.data[0])) + 5}}',
                            f'{average:>{len(str(self.data[0])) + 5}}'])
        
        return  f"\n{line}\n".join([head(), body(), foot()])

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
            getattr(self.__class__, command)(self)  # What is this???


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
                continue
            tempo.append(f'{str(valeur)[:min(len(str(valeur)), format_string[cle])]:{format_string[cle]}}')
            if "perc" in cle:
                tempo[-1] += " %"
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