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

def get_gameid(game):
    for key in gamesid:
        if gamesid[key] == game:
            return key



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

def get_categoryid(category):
    for key in categoriesid:
        if categoriesid[key] == category:
            return key


WRs = {}




def get_WR(game, category):
    if WRs.get(game) is None:  # new game? Create a new entry. Not doing this will lead to an error.
        WRs[game] = {}
    if WRs[game].get(category) is None:  # This means we don't have a WR for said category
        rep = requests.get(f"{URL}/leaderboards/{get_gameid(game)}/category/{get_categoryid(category)}?top=1")
        print(rep.status_code)
        if rep.status_code == 200:  # Because my stuffs now doesn't call with IDs, it doesn't work
            rep = rep.json()
            WRs[game][category] = datetime.timedelta(seconds=isodate.parse_duration(rep["data"]["runs"][0]["run"]["times"]["primary"]).total_seconds())
    return WRs[game][category]



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