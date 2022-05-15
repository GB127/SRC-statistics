from code_SRC.api import api
from entries.run import Run, PB

class User:
    def __init__(self, username:str):
        user_id = api.user_id(username)
        self.username = username.capitalize()
        self.runs = api.user_runs(user_id)
        self.pbs = api.user_pbs(user_id)
