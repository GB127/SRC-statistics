import requests
import matplotlib
import datetime
import isodate


URL = "https://www.speedrun.com/api/v1"

def get_runs(username):
    runs = []
    unwanted = ["weblink", "videos", "comment", "status","links","values", "id", "level", "players", "date", "submitted", "splits"]
    link_1 = f"{URL}/runs?user={get_userID(username)}&max=200"

    def getter(link):
        print(link)
        rep = requests.get(link)
        if rep.status_code == 200:
            rep = rep.json()
        for run in rep["data"]:
            for unwant in unwanted: del run[unwant]
            run["times"] = run["times"]["primary"]
            runs.append(run)
        if rep["pagination"]["size"] == rep["pagination"]["max"]:
            print("hallo")
            getter(rep["pagination"]["links"][-1]["uri"])
        if rep["pagination"]["size"] < rep["pagination"]["max"]:
            pass
    
    getter(link_1)
    return runs




def get_userID(username):
    rep = requests.get(f"{URL}/users/{username}")
    if rep.status_code == 200:
        rep = rep.json()
        return rep["data"]["id"]

games = {}
def get_game(ID):
    # ID or acronym
    try:
        return games[ID]
    except KeyError:
        rep = requests.get(f"{URL}/games/{ID}")
        if rep.status_code == 200:
            rep = rep.json()
            games[ID] = rep["data"]["names"]["international"]
    return games[ID]

categories = {}
def get_category(ID):
    try:
        return categories[ID]
    except KeyError:
        rep = requests.get(f'{URL}/categories/{ID}')
        if rep.status_code == 200:
            rep = rep.json()
            categories[ID] = rep["data"]["name"]
    return categories[ID]

WRs = {}
def get_WR(ID):
    try:
        return WRs[ID]
    except KeyError:
        WRs[ID] = []
        rep = requests.get(f'{URL}/categories/{ID}/records')
        if rep.status_code == 200:
            rep = rep.json()
            for place in rep["data"][0]["runs"]:
                WRs[ID].append(place["run"]["times"]["primary"])
            WRs[ID].sort()
    return WRs[ID]

def get_leaderboard():
    # TODO: Doublons à éliminer quand possible!
    # TODO: Séparer les onglets
    # TODO: Game Argument & Category argument
    ranking = []
    rep = requests.get(f"{URL}/leaderboards/sml2/category/Any_Glitchless")
    if rep.status_code == 200:
        rep= rep.json()

        for run in rep["data"]["runs"]:
            ranking.append((int(run["place"]), isodate.parse_duration(run["run"]["times"]["primary"]).total_seconds()))
    else:
        raise BaseException(rep.status_code)
    return ranking


if __name__ == "__main__":
    print(get_runs("niamek"))