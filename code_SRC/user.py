from code_SRC.api import api
from tables.runs import Table_run
from tables.pbs import Table_pb

class User:
    def __init__(self, username):
        self.username = username
        self.id = api.user_id(username)
        self.runs = Table_run(api.user_runs(self.id))
        self.pbs = Table_pb(api.user_pbs(self.id))


    def __str__(self):
        time_str = lambda x : f'{int(x)//3600:>3}:{int(x) % 3600 // 60:02}:{int(x) % 3600 % 60 % 60:02}'
        return f"{self.username} | {len(self.runs.join('game'))} game | {len(self.runs.join('system'))} system\n{len(self.runs)} Runs ({time_str(self.runs.sum().time):>10})\n{len(self.pbs)} PBs  ({time_str(self.pbs.sum().time):>10})"