from code_SRC.api import api
from tables.runs import Table_run
from tables.pbs import Table_pb
import os

clear = lambda: os.system('cls')


class User:
    """User class regrouping user's runs and PBs from SRC.
        username (str): username of the user.
        if (str): id of the user
        runs (list) : list of runs objects
        pbs (list): list of pbs objects
        runs_level (list) : list of runs objects. Level runs only.
        pbs_level (list): list of pbs objects. Level pbs only.
        """
    def __init__(self, username:str):
        self.username = username.capitalize()
        self.id = api.user_id(username)
        
        runs_list  = api.user_runs(self.id)
        pbs_list = api.user_pbs(self.id)
        if any([not bool(x["level"]) for x in runs_list]):
            self.runs = Table_run(runs_list, False)
            self.pbs = Table_pb(pbs_list, False)
        if any([x["level"] for x in runs_list]):
            self.runs_lvl = Table_run(runs_list, True)
            self.pbs_lvl = Table_pb(pbs_list, True)

    def __call__(self):
        while True:
            clear()
            print(self)
            for index, fx in enumerate([x for x in ["pbs", "runs", "pbs_lvl", "runs_lvl"] if hasattr(self, x)]):
                print(index, fx)
            command = input(f"Select option: [0-{2 -1}] | Type end to exit\nInput : ")
            if command == "end":
                break
            self.__dict__[["pbs", "runs","pbs_lvl", "runs_lvl"][int(command)]]()


    def __str__(self):
        time_str = lambda x : f'{int(x)//3600:>3}:{int(x) % 3600 // 60:02}:{int(x) % 3600 % 60 % 60:02}'
        list_str = [f'{self.username}']
        if hasattr(self, "runs"):
            list_str += ["Full runs:",
                            f'{len(self.runs)} Runs     ({time_str(self.runs.sum().time).lstrip()})  :   ' + f'{len(self.pbs)} PBs    ({time_str(self.pbs.sum().time).lstrip()})']
        if hasattr(self, "runs_lvl"):
            list_str += ["Individual level runs:",
                            f'{len(self.runs_lvl)} Runs     ({time_str(self.runs_lvl.sum().time).lstrip()})  :   ' + f'{len(self.pbs_lvl)} PBs    ({time_str(self.pbs_lvl.sum().time).lstrip()})']
        string = "\n".join(list_str)

        return string