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
        rep = requests.get(f"{URL}/runs?user={get_userID(username)}")
        if rep.status_code == 200:
            rep = rep.json()
        return rep["data"]

test = getruns("niamek", True)
print(test)