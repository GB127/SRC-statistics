from code_SRC.api import api
from tables.solo_runs import Table_pb, Table_run
from os import system as text_terminal
from tables.grouped import Table_grouped, Table_saved

clear = lambda: text_terminal("cls")


class User:
    def __init__(self, username: str):
        user_id = api.user_id(username)
        self.username = username.capitalize()
        all_runs = api.user_runs(user_id)
        all_pbs = api.user_pbs(user_id)

        self.runs = Table_run(all_runs, False)
        self.runs_l = Table_run(all_runs, True)
        self.pbs = Table_pb(all_pbs, False)
        self.pbs_l = Table_pb(all_pbs, True)

        for clé in self.runs.keys():
            if clé == "category":
                self.__dict__["saves"] = Table_saved(clé, self.runs, self.pbs)
            else:
                try:
                    self.__dict__[clé] = Table_grouped(clé, self.runs, self.pbs)
                except TypeError:
                    pass

    def keys(self):
        string_nol = []
        string_l = []
        for x in self.__dict__.keys():
            if callable(self.__dict__[x]) and bool(self.__dict__[x]):
                if x[-2:] == "_l":
                    string_l.append(x)
                else:
                    string_nol.append(x)
        return string_nol + string_l

    def __call__(self):
        while True:
            clear()
            print(self)
            print("\n")
            for index, fx in enumerate(self.keys()):
                print(index, fx)
            command = input(
                f"Select option: [0-{len(self.keys()) -1}] | Type end to exit\nInput : "
            )
            if command == "end":
                break
            elif command.isnumeric():
                self.__dict__[self.keys()[int(command)]]()
