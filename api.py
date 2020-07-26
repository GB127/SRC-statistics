joimport requests
import matplotlib
import datetime
import isodate


URL = "https://www.speedrun.com/api/v1"

def get_runs(username):
    runs = []
    link_1 = f"{URL}/runs?user={get_userID(username)}&max=200"

    def getter(link):
        rep = requests.get(link)
        if rep.status_code == 200:
            rep = rep.json()
        for run in rep["data"]:
            runs.append(run)
        if rep["pagination"]["size"] == rep["pagination"]["max"]:
            getter(rep["pagination"]["links"][-1]["uri"])
        if rep["pagination"]["size"] < rep["pagination"]["max"]:
            pass
    
    getter(link_1)
    return runs

def get_PBs(username):
    rep = requests.get(f"{URL}/users/{get_userID(username)}/personal-bests")
    if rep.status_code == 200:
        rep = rep.json()
    return rep["data"]

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

def get_leaderboard(gameID, categID):
    # TODO: Doublons à éliminer quand possible!
    # TODO: Séparer les onglets
    ranking = []
    rep = requests.get(f"{URL}/leaderboards/{gameID}/category/{categID}")
    if rep.status_code == 200:
        rep= rep.json()

        for run in rep["data"]["runs"]:
            ranking.append((int(run["place"]), isodate.parse_duration(run["run"]["times"]["primary"]).total_seconds()))
    else:
        raise BaseException(rep.status_code)
    return ranking


if __name__ == "__main__":
    get_PBs("niamek")