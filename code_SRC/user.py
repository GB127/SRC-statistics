from code_SRC.api import api

class User:
    def __init__(self, username):
        self.username = username
        self.id = api.user_id(username)