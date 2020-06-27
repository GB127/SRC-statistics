import requests
import matplotlib

URL = "https://www.speedrun.com/api/v1"

gamesid = {}

def get_game(gameid):
    try:
        gamesid[gameid]
        return gamesid[gameid]
    except KeyError:
        rep = requests.get(f"{URL}/games/{gameid}")
        if rep.status_code == 200:
            rep = rep.json()
            gamesid[gameid] = rep["data"]["names"]["international"]
            return gamesid[gameid]

categoriesid = {}
def get_category(categid):
    try:
        categoriesid[categid]
        return categoriesid[categid]
    except KeyError:
        rep = requests.get(f"{URL}/categories/{categid}")
        if rep.status_code == 200:
            rep = rep.json()
            categoriesid[categid] = rep["data"]["name"]
            return categoriesid[categid]

def get_WR(game, category):
    rep = requests.get(f"{URL}/leaderboards/{game}/category/{category}?top=1")
    if rep.status_code == 200:
        rep = rep.json()
        return rep["data"]["runs"][0]["run"]["times"]["primary"]

def get_userID(username):
    rep = requests.get(f"{URL}/users/{username}")
    if rep.status_code == 200:
        rep = rep.json()
    return rep["data"]["id"]


def get_runs(username, all=False):
    unwanted_data = ["values", "players", "date", "level", "submitted", "id", "comment", "weblink", "videos", "status", "splits", "links"]
    if not all:
        rep = requests.get(f"{URL}/users/{get_userID(username)}/personal-bests")
        if rep.status_code == 200:
            rep = rep.json()
        return rep["data"]
            # This returns my list of PBs : 1 dicto per run
                # place : my rank
                # run :
                    # Game
                    # Category
                    # Status
                    # Times (OK)
    elif all:
        rep = requests.get(f"{URL}/runs?user={get_userID(username)}&max=200")
        if rep.status_code == 200:
            rep = rep.json()
        return rep["data"]