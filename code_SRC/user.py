from code_SRC.api2 import api
from code_SRC.composantes import Time
from tables.solo_runs import Table_pb, Table_run
from os import system as text_terminal

clear = lambda: text_terminal('cls')


class User:
    def __init__(self, username:str):
        user_id = api.user_id(username)
        self.username = username.capitalize()
        self.runs = Table_run(api.user_runs(user_id), False)
        self.runs_l = Table_run(api.user_runs(user_id), True)
        self.pbs = Table_pb(api.user_pbs(user_id), False)
        self.pbs_l = Table_pb(api.user_pbs(user_id), True)

    def __call__(self):
        while True:
            clear()
            print(self)
            print("\n")
            for index, fx in enumerate([x for x in ["pbs", "runs", "pbs_lvl", "runs_lvl"] if hasattr(self, x)]):
                print(index, fx)
            command = input(f"Select option: [0-{2 -1}] | Type end to exit\nInput : ")
            if command == "end":
                break
            self.__dict__[["pbs", "runs","pbs_lvl", "runs_lvl"][int(command)]]()