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
    system_db = {'jm95z9ol': 'NES', '83exk6l5': 'SNES', '3167d6q2': 'GBA', 'mr6k409z': 'FDS', '4p9z06rn': 'GC', 'n5e17e27': 'PS2', 'mx6pwe3g': 'PS3','8gej2n93': 'PC', '8gejn93d': 'Wii U', 'w89rwelk': 'N64', 'n5683oev': 'GB', '3167jd6q': 'SGB', '7m6yvw6p': 'GB Player', 'n5e147e2': 'SGB2', '5negk9y7': 'PSP', 'p36nd598': 'iQue', 'vm9v3ne3': 'GB Interface', 'gde3g9k1': 'GBC', '7g6m8erk': 'NDS'}
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
                if one["id"] in api.system_db: continue
                api.system_db[one["id"]] = one["name"].replace("Virtual Console", "VC")

        def update_categories(liste):
            for one in liste:
                if one["id"] in api.category_db: continue
                api.category_db[one["id"]] = one["name"]
        
        def update_regions(liste):
            for one in liste:
                if one["id"] in api.region_db: continue
                api.region_db[one["id"]] = one["name"]

        def update_subcategories(liste):
            for one in liste:
                if one["id"] in api.subcat_db: continue
                if one["is-subcategory"]:
                    api.subcat_db[one["id"]] = {}
                    for subcat_id, subcat_name in one["values"]["values"].items():
                        api.subcat_db[one["id"]][subcat_id] = subcat_name["label"]

        def update_levels(liste):
            for one in liste:
                if one["id"] in api.level_db: continue
                api.level_db[one["id"]] = one["name"]

        def update_game(name):
            nom_a_modif = name
            for unwanted in [" Category Extensions", "The Legend of "]:
                nom_a_modif = nom_a_modif.replace(unwanted, "")
            api.game_db[game_id] = nom_a_modif

        req = requester(f'{api.URL}games/{game_id}?embed=categories,levels,variables,platforms,regions')["data"]

        update_game(req["names"]["international"])

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
            return api.game_db[id]

    @staticmethod
    def sub_cat(id_1, id_2):
        return api.subcat_db[id_1][id_2]

    @staticmethod
    def system(id:str) -> str:
        if not id:
            return "???"
        return api.system_db[id]

    @staticmethod
    def region(id:str) -> str:
        if id:
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
