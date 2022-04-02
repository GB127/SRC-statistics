from requests import get
from time import sleep

def requester(link):
    while True:
        try:
            data = get(link).json()
            assert "data" in data
            return data
        except AssertionError:
            print(data)
            print("Waiting...")
            sleep(20)

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
    def update_db(game_id:str):
        """Method that will update all the datas related to the given game id.

            Args:
                game_id (str): id of game

            Summary:
                Request data on SRC's api with embedding.
                Updates all data related to game:
                    game_db
                    system_db
                    category_db
                    level_db
                    region_db
                    sublevel_db
                    subcat_db
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

        req = requester(f'{api.URL}games/{game_id}?embed=categories,levels,variables,regions,platforms')["data"]
        update_game(req["names"]["international"])
        update_systems(req["platforms"]["data"])
        update_categories(req["categories"]["data"])
        update_regions(req["regions"]["data"])
        update_subcategories(req["variables"]["data"])
        update_levels(req["levels"]["data"])

    @staticmethod
    def game(id:str) -> str:
        """ This is always the first method to be called.
            Fetches the game related to the given id.
                If a KeyError is thrown during the attempt, calls api.update_db
                to update the data.
            Args:
                id (str): ID of the game

        Returns:
            str: Game's name linked to the id
        """
        try:
            return api.game_db[id]
        except KeyError:
            api.update_db(id)
            return api.game_db[id]

    @staticmethod
    def sub_cat(id_1:str, id_2:str)->str:
        """Returns the subcategory related to the two ids

        Args:
            id_1 (_type_): field of the subcategory
            id_2 (_type_): value of the subcategory selected

        Returns:
            str : Subcategory name
        """
        return api.subcat_db[id_1][id_2]

    @staticmethod
    def system(id:str) -> str:
        """Returns the system's name related to id
        Args:
            id (str): id of the system

        Returns:
            str: system's name
        """
        if id:
            return api.system_db[id]
        return ""

    @staticmethod
    def region(id:str) -> str:
        """Returns the region related to id

        Args:
            id (str): id of the region

        Returns:
            str: Region
        """
        if id:
            return api.region_db[id]

    @staticmethod
    def category(id:str) -> str:
        """Returns the category related to the id

        Args:
            id (str): id of the category

        Returns:
            str: Category's name
        """
        return api.category_db[id]

    @staticmethod
    def level(id:str) -> str:
        """Returns the level's name

        Args:
            id (str): Level's id

        Returns:
            str: level's name
        """
        return api.level_db[id]

    @staticmethod
    def user_id(username:str) -> str:
        # TODO : Adress scenarios where username is invalid
        """Makes a request to the SRC API to retrieve the ID of the given username.

        Args:
            username (str): Username

        Returns:
            str: ID of the username
        """
        req = requester(f'{api.URL}users/{username}')
        return req["data"]["id"]


    @staticmethod
    def user_runs(user_id:str) -> list:
        """Make request(s) to SRC's database in order to retrieve all runs from a user ID.
            Use api.user_id before in order to get the id of a user before using this method.
        Args:
            user_id (str): User's ID

        Returns:
            list of dict: [dict1, dict2, dict3, ...] where dict is the data of a run.
        """
        liste = []
        req = requester(f'{api.URL}runs?user={user_id}&max=200')
        liste += req["data"]
        while(req["pagination"]["links"]) and (req["pagination"]["size"] == req["pagination"]["max"]):
            req = get(req["pagination"]["links"][0]["uri"]).json()
            liste += req["data"]
        return req["data"]

    @staticmethod
    def user_pbs(user_id:str) -> list:
        """Make a request to SRC's api to retrieve all PBs from a user with the given user's ID.
            Use api.user_id before in order to retrieve the id.
        Args:
            user_id (str): User's id

        Returns:
            list of dict: [dict1, dict2, dict3, ...] where dict is the data of a run.
        """
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
