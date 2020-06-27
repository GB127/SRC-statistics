import requests
import matplotlib

URL = "https://www.speedrun.com/api/v1"

def get_game(gameid):
    rep = requests.get(f"{URL}/games/{gameid}")
    if rep.status_code == 200:
        rep = rep.json()
    return rep["data"]["names"]["international"]

def get_category(categid):
    rep = requests.get(f"{URL}/categories/{categid}")
    if rep.status_code == 200:
        rep = rep.json()
    return rep["data"]["name"]

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