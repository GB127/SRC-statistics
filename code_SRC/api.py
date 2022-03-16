from requests import get
from time import sleep

def requester(link):
    while True:
        try:
            data = get(link).json()
            assert "data" in data
            return data
        except AssertionError:  # pragma: no cover
            print(data)  # pragma: no cover
            print("Waiting...")  # pragma: no cover
            sleep(20)  # pragma: no cover

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
            req = requester(f'{api.URL}games/{id}')
            api.game_db[id] = req["data"]["names"]["international"].replace("Category Extensions", "").rstrip()
        return api.game_db[id]

    @staticmethod
    def system(id:str) -> str:
        if not id:
            return "???"
        try:
            return api.system_db[id]
        except KeyError:
            req = requester(f'{api.URL}platforms/{id}')
            api.system_db[id] = req["data"]["name"].replace("Virtual Console", "VC")

        return api.system_db[id]

    @staticmethod
    def region(id:str) -> str:
        try:
            return api.region_db[id]
        except KeyError:
            req = requester(f'{api.URL}regions/{id}')
            api.region_db[id] = req["data"]["name"]
        return api.region_db[id]

    @staticmethod
    def category(id:str) -> str:
        try:
            return api.category_db[id]
        except KeyError:
            req = requester(f'{api.URL}categories/{id}')
            api.category_db[id] = req["data"]["name"]
        return api.category_db[id]

    @staticmethod
    def level(id) -> str:
        try:
            return api.level_db[id]
        except KeyError:
            req = requester(f'{api.URL}levels/{id}')
            api.level_db[id] = req["data"]["name"]
        return api.level_db[id]


    @staticmethod
    def user_id(username) -> str:
        req = requester(f'{api.URL}users/{username}')
        return req["data"]["id"]



    @staticmethod
    def user_runs(user_id) -> list:
        liste = []
        req = requester(f'{api.URL}runs?user={user_id}&max=200')
        liste += req["data"]
        while(req["pagination"]["links"]) and (req["pagination"]["size"] == req["pagination"]["max"] ):
            req = get(req["pagination"]["links"][0]["uri"]).json()
            liste += req["data"]
        return req["data"]

    @staticmethod
    def user_pbs(user_id) -> list:
        req = requester(f'{api.URL}users/{user_id}/personal-bests')
        return req["data"]

    @staticmethod
    def leaderboard(game_id, category_id, subcat_id=None, level_id=None):
        variables = ""
        if subcat_id:
            variables = "&var-".join([f"{x}={y}" for x,y in subcat_id.items()])


        if not level_id:
            req = requester(f'{api.URL}leaderboards/{game_id}/category/{category_id}?var-{variables}')
        else:
            req = requester(f'{api.URL}leaderboards/{game_id}/level/{level_id}/{category_id}?var-{variables}')
        return req["data"]["runs"]
