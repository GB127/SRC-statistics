from tools import command_select, run_time
class table:
    def __init__(self):
        self.backup = []
        self.data = []

    def __str__(self):
        head_prep = []
        for attribut, value in self.data[0].__dict__.items():
            if attribut in ["leaderboard", "place", "IDs", "runs", "pbs"]:
                pass
            elif attribut == "level":
                pass
            elif "count" in attribut:
                head_prep.append(f'{"#":^3}')
            elif isinstance(value, run_time):
                head_prep.append(f'{attribut[:9]:^9}')
            elif attribut == "game":
                head_prep.append(f'{attribut[:30]:30}')
            elif attribut == "system":
                head_prep.append(f'{"syst":^7}')
            elif attribut == "category":
                head_prep.append(f'{attribut[:20]:20}')
            elif "perc" in attribut:
                head_prep.append(f'{attribut:^9}')
            elif attribut == "ranking":
                head_prep.append(f'{attribut:^10}')

            else:
                head_prep.append(attribut)

        head = " | ".join(head_prep)


        line = f'{"-" * len(str(self.data[0]))}'
        body = "\n".join([str(x) for x in self.data])
        return  f'{head}\n{line}\n{body}\n{line}'


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
        return {"Change the sorting": self.change_sort,
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

    def change_sort(self):
        self.data[0].change_sort()

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

            if isinstance(valeur, run_time):
                tempo.append(f'{valeur:>9}')
            elif "count" in cle:
                tempo.append(f'{valeur:>3}')
            elif cle == "game":
                tempo.append(f'{valeur[:30]:30}')
            elif cle == "system":
                tempo.append(f'{valeur:^7}')
            elif cle == "category":
                tempo.append(f'{valeur[:20]:20}')
            elif cle == "ranking":
                tempo.append(f'{valeur:^10}')
            elif "perc" in cle:
                tempo2 = str(valeur)
                if tempo2[-2] == "." : tempo2 += "0"
                tempo.append(f'{tempo2:>7} %')
            elif cle == "X":
                tempo.append(f'{valeur:2}')


        return " | ".join(tempo)

    def change_sort(self):
        for no, one in enumerate(self.sortable()):
            print(no + 1, one)
        self.__class__.sorter = command_select(self.sortable())

    def __lt__(self, other):  # FIXME : If equal, it needs to have some sub-sorting.
        if self.__dict__[self.sorter] != other.__dict__[self.sorter]:
            return self.__dict__[self.sorter] < other.__dict__[self.sorter]
        elif self.game == other.game and self.category == other.category:
            return self.time > other.time
        elif self.game != other.game:
            return self.game < other.game
        elif self.category != other.category:
            return self.category < other.category

