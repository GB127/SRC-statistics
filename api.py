import requests
import matplotlib
import datetime
import isodate

URL = "https://www.speedrun.com/api/v1"

def getruns(username):
    rep = requests.get(f"{URL}/users/niamek/personal-bests")
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
            # category: ???


runs = getruns("niamek")
for i in runs :
    print(isodate.parse_duration(i["run"]["times"]["primary"]))
