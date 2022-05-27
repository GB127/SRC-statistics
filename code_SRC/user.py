from code_SRC.api2 import api
from tables.solo_runs import Table_pb, Table_run
from os import system as text_terminal
from tables.grouped import Table_grouped
clear = lambda: text_terminal('cls')


class User:
    def __init__(self, username:str):
        user_id = api.user_id(username)
        self.username = username.capitalize()
        all_runs = api.user_runs(user_id)
        all_pbs = api.user_pbs(user_id)

        self.runs = Table_run(all_runs, False)
        self.runs_l = Table_run(all_runs, True)
        self.pbs = Table_pb(all_pbs, False)
        self.pbs_l = Table_pb(all_pbs, True)

        for clé in self.runs.keys():
            try:
                self.__dict__[clé] = Table_grouped(clé,self.runs, self.pbs)
            except TypeError:
                continue


    def __call__(self):
        while True:
            clear()
            print(self)
            print("\n")
            for index, fx in enumerate([x for x in ["pbs", "runs", "pbs_lvl", "runs_lvl", "game", "system", "series", "release"] if hasattr(self, x)]):
                print(index, fx)
            command = input(f"Select option: [0-{2 -1}] | Type end to exit\nInput : ")
            if command == "end":
                break
            self.__dict__[["pbs", "runs","pbs_lvl", "runs_lvl" , "game", "system", "series", "release"][int(command)]]()