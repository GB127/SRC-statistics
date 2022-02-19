from requests import get

class api:
    URL = "https://www.speedrun.com/api/v1/"
    game_db = {}
    system_db = {}
    category_db = {}
    level_db = {}
    region_db = {}

    @staticmethod
    def game(id:str) -> str:
        try:
            return api.game_db[id]
        except KeyError:
            req = get(f'{api.URL}games/{id}').json()
            api.game_db[id] = req["data"]["names"]["international"].replace("Category Extensions", "").rstrip()
        return api.game_db[id]

    @staticmethod
    def system(id:str) -> str:
        try:
            return api.system_db[id]
        except KeyError:
            req = get(f'{api.URL}platforms/{id}').json()
            api.system_db[id] = req["data"]["name"].replace("Virtual Console", "VC")

        return api.system_db[id]

    @staticmethod
    def region(id:str) -> str:
        try:
            return api.region_db[id]
        except KeyError:
            req = get(f'{api.URL}regions/{id}').json()
            api.region_db[id] = req["data"]["name"]
        return api.region_db[id]

    @staticmethod
    def category(id:str) -> str:
        try:
            return api.category_db[id]
        except KeyError:
            req = get(f'{api.URL}categories/{id}').json()
            api.category_db[id] = req["data"]["name"]
        return api.category_db[id]

    @staticmethod
    def level(id) -> str:
        try:
            return api.level_db[id]
        except KeyError:
            req = get(f'{api.URL}levels/{id}').json()
            api.level_db[id] = req["data"]["name"]
        return api.level_db[id]


    @staticmethod
    def user_id(username) -> str:
        req = get(f'{api.URL}users/{username}').json()
        return req["data"]["id"]

    @staticmethod
    def user_runs(user_id) -> list:
        req = get(f'{api.URL}runs?user={user_id}').json()
        return req["data"]

    @staticmethod
    def user_pbs(user_id) -> list:
        req = get(f'{api.URL}users/{user_id}/personal-bests').json()
        return req["data"]
