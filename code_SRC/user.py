from code_SRC.api import api
from tables.runs import Table_run
from tables.pbs import Table_pb
import os

clear = lambda: os.system('cls')


class User:
    def __init__(self, username:str):
        self.username = username.capitalize()
        self.id = api.user_id(username)
        self.runs = Table_run(api.user_runs(self.id), False)
        self.pbs = Table_pb(api.user_pbs(self.id), False)
        self.runs_lvl = Table_run(api.user_runs(self.id), True)
        self.pbs_lvl = Table_pb(api.user_pbs(self.id), True)

    def __call__(self):
        while True:
            clear()
            print(self)
            for index, fx in enumerate(["pbs", "runs", "pbs_lvl", "runs_lvl"]):
                print(index, fx)
            command = input(f"Select option: [0-{2 -1}] | Type end to exit\nInput : ")
            if command == "end":
                break
            self.__dict__[["pbs", "runs","pbs_lvl", "runs_lvl"][int(command)]]()


    def __str__(self):
        time_str = lambda x : f'{int(x)//3600:>3}:{int(x) % 3600 // 60:02}:{int(x) % 3600 % 60 % 60:02}'
        string = "\n".join([f'{self.username}',
                            f'------------------------------------',
                            f'Runs : {time_str(sum(self.runs).time):11} | {time_str(self.runs.mean().time):11} | {time_str(self.runs.median("time").time):11}',
                            f'PBs  : {time_str(sum(self.pbs).time):11} | {time_str(self.pbs.mean().time):11} | {time_str(self.pbs.median("time").time):11}'])
        return string