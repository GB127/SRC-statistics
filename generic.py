from tools import command_select, run_time

def formatting(cle, valeur, which):
    tostr = {"cle":cle, "valeur":valeur}
    if "count" in cle:  #FIXME
        return f'{"#":^3}'
    elif isinstance(valeur, run_time):
        tempo = ""
        if "delta" in cle:
            if which == "valeur":
                if "p" in cle:
                    tempo += "+"
                elif "m" in cle:
                    tempo += "-"
            elif which == "cle" :
                tostr[which] = tostr[which][:-2]
        return f'{tempo + str(tostr[which])[:9]:^9}'
    elif cle == "game":
        return f'{tostr[which][:30]:30}'
    elif cle == "system":
        return f'{tostr[which][:6]:^6}'
    elif cle == "category":
        return f'{tostr[which][:20]:20}'
    elif "perc" in cle:
        tempo = "" if which == "cle" else " %"
        tempo2 = str(tostr[which])
        if tempo2[-2] == "." :
            tempo2 += "0"
        return f'{ tempo2 + tempo:>9}'
    elif cle == "ranking":
        return f'{tostr[which]:^10}'
    else:
        return tostr[which]


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
                elif cle == "level":
                    pass
                else:
                    head_prep.append(formatting(cle, valeur, "cle"))

            return f"{'':4}|" + " | ".join(head_prep)

        line = f'{"-" * len(str(self.data[0]))}-----'

        body = ""
        for no, x in enumerate(self.data):
            body += f"{no:>3} |{x}\n"

        return  f'{head()}\n{line}\n{body}{line}'


    def __call__(self):
        while True:
            print(self)
            if input("end?") == "end":
                break

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
            elif cle == "level":
                pass
            else:
                tempo.append(formatting(cle, valeur, "valeur"))
        return " | ".join(tempo)


    def __lt__(self, other):  # FIXME : If equal, it needs to have some sub-sorting.
        if self.__dict__[self.sorter] != other.__dict__[self.sorter]:
            return self.__dict__[self.sorter] < other.__dict__[self.sorter]
        elif self.game == other.game and self.category == other.category:
            return self.time > other.time
        elif self.game != other.game:
            return self.game < other.game
        elif self.category != other.category:
            return self.category < other.category
