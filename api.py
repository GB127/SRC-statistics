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

def get_leaderboard():
    # No game ID for now. Only SML1 any
    # TODO: Doublons à éliminer quand possible!
    ranking = []
    rep = requests.get(f"{URL}/leaderboards/sms/category/Any")
    if rep.status_code == 200:
        rep= rep.json()

        for run in rep["data"]["runs"]:
            ranking.append((int(run["place"]), isodate.parse_duration(run["run"]["times"]["primary"]).total_seconds()))
    else:
        raise BaseException(rep.status_code)
    return ranking


if __name__ == "__main__":
    get_leaderboard()