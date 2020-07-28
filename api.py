import requests
import matplotlib
import datetime
import isodate


URL = "https://www.speedrun.com/api/v1"

def requester(link):
    rep = requests.get(f"{URL}{link}")
    if rep.status_code == 200:
        return rep.json()
    else:
        raise BaseException(rep.status_code)


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

def get_PBs(username):  # Requester DONE
    rep = requester(f"/users/{get_userID(username)}/personal-bests")
    return rep["data"]

def get_userID(username):  # requester DONE
    rep = requester(f"/users/{username}")
    return rep["data"]["id"]

games = {}
def get_game(ID):  # requester DONE
    # ID or acronym
    try:
        return games[ID]
    except KeyError:
        rep = requester(f"/games/{ID}")
        games[ID] = rep["data"]["names"]["international"]
    return games[ID]

categories = {}
def get_category(ID):  # requester DONE
    try:
        return categories[ID]
    except KeyError:
        rep = requester(f'/categories/{ID}')
        categories[ID] = rep["data"]["name"]
    return categories[ID]

WRs = {}
def get_WR(ID):  # Requester DONE
    try:
        return WRs[ID]
    except KeyError:
        WRs[ID] = []
        rep = requester(f'/categories/{ID}/records?top=1')
        for place in rep["data"][0]["runs"]:
            WRs[ID].append(place["run"]["times"]["primary"])
    return WRs[ID]


leaderboard = {}
def get_len_leaderboard(gameID, categID):  # Requester Done!
    try:
        return len(leaderboard[(gameID, categID)])
    except KeyError:
        ranking = []
        rep = requester(f"/leaderboards/{gameID}/category/{categID}")
        for run in rep["data"]["runs"]:
            ranking.append((int(run["place"]), isodate.parse_duration(run["run"]["times"]["primary"]).total_seconds()))
        leaderboard[(gameID, categID)] = ranking
    return len(leaderboard[(gameID, categID)])

def get_leaderboard(gameID, categID):  # Requester done!
    # TODO: Doublons à éliminer quand possible!
    # TODO: Séparer les onglets
    try:
        return leaderboard[(gameID, categID)]
    except KeyError:
        ranking = []
        rep = requester(f"/leaderboards/{gameID}/category/{categID}")
        for run in rep["data"]["runs"]:
            ranking.append((int(run["place"]), isodate.parse_duration(run["run"]["times"]["primary"]).total_seconds()))
        leaderboard[(gameID, categID)] = ranking
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
def get_newsystem(newsystem): # Requester done!
    rep = requester(f"/platforms?max=200")
    for system in rep["data"]:
        if system["name"] == newsystem: 
            print("-------------------------------------")
            print(f'"{system["id"]}" : "{system["name"]}",')
            print("-------------------------------------")
            return
    for system in rep["data"]:
        print(system["name"])

def get_system(ID):  # Requester done!
    try:
        return systems[ID]
    except KeyError:
        rep = requester(f"/platforms/{ID}")
        systems[ID] = rep["data"]["name"]
    return systems[ID]


if __name__ == "__main__":
    
    
    game = "allo"
    cat = "7dgrrxk4"

    print(get_game("sml1"))