import requests
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
        else: raise BaseException(rep.status_code)
        for run in rep["data"]:
            if run["level"] is None: pass
            else: runs.append(run)
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
        rep = requests.get(f'{URL}/categories/{ID}/records?top=1')
        if rep.status_code == 200:
            rep = rep.json()
            for place in rep["data"][0]["runs"]:
                WRs[ID].append(place["run"]["times"]["primary"])
            WRs[ID].sort()
        else:
            raise BaseException
    return WRs[ID]


leaderboard = {}
def get_len_leaderboard(gameID, categID):
    try:
        return len(leaderboard[(gameID, categID)])
    except KeyError:
        ranking = []
        rep = requests.get(f"{URL}/leaderboards/{gameID}/category/{categID}")
        if rep.status_code == 200:
            rep= rep.json()
            for run in rep["data"]["runs"]:
                ranking.append((int(run["place"]), isodate.parse_duration(run["run"]["times"]["primary"]).total_seconds()))
            leaderboard[(gameID, categID, variable)] = ranking
        else:
            raise BaseException(rep.status_code)
    return len(leaderboard[(gameID, categID, variable)])

def get_leaderboard(gameID, categID):
    # TODO: Doublons à éliminer quand possible!
    # TODO: Séparer les onglets
    try:
        return leaderboard[(gameID, categID)]
    except KeyError:
        ranking = []
        rep = requests.get(f"{URL}/leaderboards/{gameID}/category/{categID}")
        if rep.status_code == 200:
            rep= rep.json()
            for run in rep["data"]["runs"]:
                ranking.append((int(run["place"]), isodate.parse_duration(run["run"]["times"]["primary"]).total_seconds()))
            leaderboard[(gameID, categID)] = ranking
        else:
            raise BaseException(rep.status_code)
    return leaderboard[(gameID, categID)]

systems = {
    None : "PC",
    "n5683oev" : "GB",
    "gde3g9k1" : "GBC",
    "3167d6q2" : "GBA",
    "w89rwelk" : "N64",
    "jm95z9ol" : "NES",
    "3167jd6q" : "SGB",
    "83exk6l5" : "SNES",
    "nzelreqp" : "WII VC"}
def get_newsystem(newsystem):
    rep = requests.get(f"{URL}/platforms?max=200")
    if rep.status_code == 200:
        rep= rep.json()
        for system in rep["data"]:
            if system["name"] == newsystem: 
                print("-------------------------------------")
                print(f'"{system["id"]}" : "{system["name"]}",')
                print("-------------------------------------")
                return
        for system in rep["data"]:
            print(system["name"])
    else:
        raise BaseException(rep.status_code)


def get_system(ID):
    try:
        return systems[ID]
    except KeyError:
        rep = requests.get(f"{URL}/platforms/{ID}")
        if rep.status_code == 200:
            rep= rep.json()
            systems[ID] = rep["data"]["name"]
        else:
            raise BaseException(rep.status_code)
    return systems[ID]


if __name__ == "__main__":
    
    
    game = "o1y9wo6q"
    cat = "7dgrrxk4"

    test = get_leaderboard(game, cat)

    print(test)