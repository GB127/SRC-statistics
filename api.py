import requests
import matplotlib
import datetime
import isodate
import time


URL = "https://www.speedrun.com/api/v1"

def requester(link):
    while True:
        rep = requests.get(f"{URL}{link}")
        if rep.status_code == 200:
            return rep.json()
        if rep.status_code == 502:
            print("502 error, let's wait and try again")
            time.sleep(20)


def get_PBs(username):
    rep = requester(f"/users/{get_userID(username)}/personal-bests")
    return rep["data"]

def get_userID(username):
    rep = requester(f"/users/{username}")
    return rep["data"]["id"]

games = {}
def get_game(ID):
    # ID or acronym
    try:
        return games[ID]
    except KeyError:
        rep = requester(f"/games/{ID}")
        games[ID] = rep["data"]["names"]["international"]
    return games[ID]

categories = {}
def get_category(ID):
    try:
        return categories[ID]
    except KeyError:
        rep = requester(f'/categories/{ID}')
        categories[ID] = rep["data"]["name"]
    return categories[ID]

WRs = {}
def get_WR(ID):
    try:
        return WRs[ID]
    except KeyError:
        WRs[ID] = []
        rep = requester(f'/categories/{ID}/records?top=1')
        for place in rep["data"][0]["runs"]:
            WRs[ID].append(place["run"]["times"]["primary"])
    return WRs[ID]


leaderboard = {}
def get_len_leaderboard(gameID, categID):
    try:
        return len(leaderboard[(gameID, categID)])
    except KeyError:
        ranking = []
        rep = requester(f"/leaderboards/{gameID}/category/{categID}")
        for run in rep["data"]["runs"]:
            ranking.append((int(run["place"]), isodate.parse_duration(run["run"]["times"]["primary"]).total_seconds()))
        leaderboard[(gameID, categID)] = ranking
    return len(leaderboard[(gameID, categID)])

def get_leaderboard(gameID, categID):
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
def get_newsystem(newsystem):
    rep = requester(f"/platforms?max=200")
    for system in rep["data"]:
        if system["name"] == newsystem: 
            print("-------------------------------------")
            print(f'"{system["id"]}" : "{system["name"]}",')
            print("-------------------------------------")
            return
    for system in rep["data"]:
        print(system["name"])

def get_system(ID):
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