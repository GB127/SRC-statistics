import requests
import matplotlib
import datetime
import isodate

URL = "https://www.speedrun.com/api/v1"

def get_userID(username):
    rep = requests.get(f"{URL}/users/{username}")
    if rep.status_code == 200:
        rep = rep.json()
    return rep["data"]["id"]


def getruns(username, all=False):

    if not all:
        rep = requests.get(f"{URL}/users/{username}/personal-bests")
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
        rep = requests.get(f"{URL}/runs?user=x7qz6qq8")
        if rep.status_code == 200:
            rep = rep.json()
        return rep["data"]

test = get_userID("niamek")
print(test)