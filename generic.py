from tools import command_select, run_time

def formatting(cle, valeur, which):
    tostr = {"cle":cle, "valeur":valeur}
    if "count" in cle:
        return f'{"#":^3}'
    elif isinstance(valeur, run_time):
        tempo = "-" if "delta" in cle else ""
        return f'{tempo + str(tostr[which])[:9]:^9}'
    elif cle == "game":
        return f'{tostr[which][:30]:30}'
    elif cle == "system":
        return f'{tostr[which][:6]:^6}'
    elif cle == "category":
        return f'{tostr[which][:20]:20}'
    elif "perc" in cle:
        return f'{tostr[which]:^9}'
    elif cle == "ranking":
        return f'{tostr[which]:^10}'
    else:
        return tostr[which]


class table:
    def __init__(self):
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
            self.data.sort()
            print(self)
            command_key = command_select(sorted(self.methods().keys()), printer=True)
            command = self.methods()[command_key]
            if command != "end":
                command()
            else:
                self.reset_filter()
                break

    # COMMAND PROMPT related
    def methods(self):
        return {
                "Filter the table" : self.filter_select,
                "end": "end"}

    def filter_select(self):
        while True:
            print("To remove a single run, enter a single number\nTo remove a range, enter 2 numbers serparated by a -\nTo reset the filtering, enter reset\nTo cancel, type end")
            command = input()
            if command == "reset":
                self.reset_filter()
                break
            elif command == "end":
                break
            else:
                try:
                    number1, number2 = command.split("-")
                    self.filter(int(number1) -1, int(number2))
                    break
                except ValueError:
                    self.filter(int(command)-1)
                    break
                except:
                    pass

    def filter(self, start, end=None):
        if end:
            self.backup += self.data[:start]
            self.backup += self.data[end:]
            self.data = self.data[start: end]
        else:  # This works
            self.back = self.data[start]
            self.data.pop(start)

    def reset_filter(self):
        self.data = self.backup + self.data
        self.backup = []

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

