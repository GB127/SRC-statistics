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

