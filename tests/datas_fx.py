from ast import literal_eval
from code_SRC.api import api

dicto_m = lambda filename : literal_eval(open(f"tests/datas_from_api/{filename}.txt", "r").read())

id_m = lambda filename : literal_eval(open(f"tests/datas_from_api/{filename}.txt", "r").read())["data"]["id"]

link_m = lambda filename : literal_eval(open(f"tests/datas_from_api/{filename}.txt", "r").read())["data"]["links"][0]["uri"]

def fill_db(original_function):
    def new_function(self):
        api.game_db["29d30dlp"] = "Super Mario Sunshine"
        api.category_db["nxd1rk8q"] = "Any%"
        api.system_db["rdjq4vwe"] = "Gamecube"
        original_function(self)
    return new_function

def clear_db(original_function):
    def new_function(self, requests_mock):
        api.game_db = {}
        api.category_db = {}
        api.system_db = {}
        original_function(self, requests_mock)
    return new_function


def liste_dicto(filename):
        liste = []
        for _ in range(3):
            liste.append(dicto_m(filename)["data"])
        return liste
