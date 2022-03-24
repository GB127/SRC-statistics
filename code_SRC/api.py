from requests import get
from time import sleep

def requester(link):
    while True:
        try:
            data = get(link).json()
            assert "data" in data
            return data  # TODO: remove this
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
    sublevel_db = {}
    subcat_db = {}

    @staticmethod
    def update_db(game_id):
        """Use src's embedding to reduce request count.
            """
        def update_systems(liste):
            for one in liste:
                api.system_db[one["id"]] = one["name"]
        
        def update_categories(liste):
            for one in liste:
                api.category_db[one["id"]] = one["name"]
        
        def update_regions(liste):
            for one in liste:
                api.region_db[one["id"]] = one["name"]

        def update_subcategories(liste):
            for one in liste:
                if one["is-subcategory"]:
                    api.subcat_db[one["id"]] = {}
                    for subcat_id, subcat_name in one["values"]["values"].items():
                        api.subcat_db[one["id"]][subcat_id] = subcat_name["label"]

        def update_levels(liste):
            for one in liste:
                api.level_db[one["id"]] = one["name"]

        req = requester(f'{api.URL}games/{game_id}?embed=categories,levels,variables,platforms,regions')["data"]
        api.game_db[game_id] = req["names"]["international"]

        update_systems(req["platforms"]["data"])
        update_categories(req["categories"]["data"])
        update_regions(req["regions"]["data"])
        update_subcategories(req["variables"]["data"])
        update_levels(req["levels"]["data"])

    @staticmethod
    def game(id:str) -> str:
        try:
            return api.game_db[id]
        except KeyError:
            api.update_db(id)
            print(api.game_db)
            return api.game_db[id]

    @staticmethod
    def system(id:str) -> str:
        if not id:
            return "???"
        return api.system_db[id]

    @staticmethod
    def region(id:str) -> str:
        return api.region_db[id]

    @staticmethod
    def category(id:str) -> str:
        return api.category_db[id]

    @staticmethod
    def level(id) -> str:
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
        while(req["pagination"]["links"]) and (req["pagination"]["size"] == req["pagination"]["max"]):  # pragma: no cover
            req = get(req["pagination"]["links"][0]["uri"]).json()# pragma: no cover
            liste += req["data"]# pragma: no cover
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

    @staticmethod
    def subcat_id(subcat_id) -> str:
        return api.subcat_db[subcat_id]
