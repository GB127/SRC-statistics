from code_SRC.api import api
from tables.runs import Table_run
from tables.pbs import Table_pb
import os

clear = lambda: os.system('cls')


class User:
    def __init__(self, username):  # pragma: no cover
        self.username = username  # pragma: no cover
        self.id = api.user_id(username)  # pragma: no cover
        self.runs = Table_run(api.user_runs(self.id))  # pragma: no cover
        self.pbs = Table_pb(api.user_pbs(self.id))  # pragma: no cover

    def __call__(self):
        while True:
            clear()
            print(self)
            for index, fx in enumerate(["pbs", "runs"]):
                print(index, fx)
            command = input(f"Select option: [0-{2 -1}] | Type end to exit\nInput : ")
            if command == "end":
                break
            self.__dict__[["pbs", "runs"][int(command)]]()


    def __str__(self):
        time_str = lambda x : f'{int(x)//3600:>3}:{int(x) % 3600 // 60:02}:{int(x) % 3600 % 60 % 60:02}'
        return f"{self.username} | {len(self.runs)} Runs ({time_str(self.runs.sum().time):>10})| {len(self.pbs)} PBs  ({time_str(self.pbs.sum().time):>10})"