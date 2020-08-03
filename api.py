import requests
import matplotlib
import datetime
import isodate
import time


URL = "https://www.speedrun.com/api/v1"

def requester(link):
    """Generic requester.

        Args:
            link (string): link addition of the request

        Raises:
            BaseException: Raise error if the status code isn't 200 or 502.

        Returns:
            json: return the data in a json form
        """
    while True:
        # It's in a loop in order to bypass the 502 status code.
        rep = requests.get(f"{URL}{link}")
        if rep.status_code == 200:
            return rep.json()
        if rep.status_code == 502:
            time.sleep(10)
        else:
            print(f"{URL}{link}")
            raise BaseException


def get_PBs(username):
    """Requests the PBs of the said username

        Args:
            username (str): username

        Returns:
            data
        """
    rep = requester(f"/users/{get_userID(username)}/personal-bests")
    return rep["data"]

def get_userID(username):
    """Get the user ID of a username.

    Args:
        username (str): username

    Returns:
        ID (str)
    """
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

def get_WR(gameID, categID, vari):
    varistr = ""
    if vari != {}:
        tempo = []
        for key in vari:
            if get_variable(key)["is-subcategory"] is True: tempo.append(f"var-{key}={vari[key]}")
        varistr = "&".join(tempo)
        if varistr != "": varistr = "?" + varistr
    try:
        leaderboard[(gameID, categID, varistr)]
    except KeyError:
        get_leaderboard(gameID, categID, vari)
    return leaderboard[(gameID, categID, varistr)][0][1]

def get_variable(variID):
    rep = requester(f'/variables/{variID}')
    return rep["data"]


leaderboard = {}
def get_len_leaderboard(gameID, categID, vari):
    # vari is a dicto!
    varistr = ""
    if vari != {}:
        tempo = []
        for key in vari:
            if get_variable(key)["is-subcategory"] is True: tempo.append(f"var-{key}={vari[key]}")
        varistr = "&".join(tempo)
        if varistr != "": varistr = "?" + varistr
    try:
        return len(leaderboard[(gameID, categID, varistr)])
    except KeyError:
        ranking = []
        rep = requester(f"/leaderboards/{gameID}/category/{categID}" + varistr)
        for run in rep["data"]["runs"]:
            ranking.append((int(run["place"]), isodate.parse_duration(run["run"]["times"]["primary"]).total_seconds()))
        leaderboard[(gameID, categID, varistr)] = ranking
    return len(leaderboard[(gameID, categID, varistr)])

def get_leaderboard(gameID, categID, vari):
    # TODO: Doublons à éliminer quand possible!
    # TODO: Séparer les onglets
    varistr = ""
    if vari != {}:
        tempo = []
        for key in vari:
            if get_variable(key)["is-subcategory"] is True: tempo.append(f"var-{key}={vari[key]}")
        varistr = "&".join(tempo)
        if varistr != "": varistr = "?" + varistr
    try:
        return leaderboard[(gameID, categID, varistr)]
    except KeyError:
        ranking = []
        rep = requester(f"/leaderboards/{gameID}/category/{categID}" + varistr)
        for run in rep["data"]["runs"]:
            ranking.append((int(run["place"]), isodate.parse_duration(run["run"]["times"]["primary"]).total_seconds()))
        leaderboard[(gameID, categID, varistr)] = ranking
    return leaderboard[(gameID, categID, varistr)]

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