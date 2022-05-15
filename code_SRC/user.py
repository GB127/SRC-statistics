from code_SRC.api import api
from tables.solo_runs import Table_pb, Table_run

class User:
    def __init__(self, username:str):
        user_id = api.user_id(username)
        self.username = username.capitalize()
        self.runs = Table_run(api.user_runs(user_id), False)
        self.runs_l = Table_run(api.user_runs(user_id), True)
        self.pbs = Table_pb(api.user_pbs(user_id), False)
        self.pbs_l = Table_pb(api.user_pbs(user_id), True)