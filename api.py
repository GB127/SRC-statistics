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

def get_leaderboard():
    # TODO: Doublons à éliminer quand possible!
    ranking = []
    rep = requests.get(f"{URL}/leaderboards/sm64/category/16_Star")
    if rep.status_code == 200:
        rep= rep.json()

        for run in rep["data"]["runs"]:
            ranking.append((int(run["place"]), isodate.parse_duration(run["run"]["times"]["primary"]).total_seconds()))
    else:
        raise BaseException(rep.status_code)
    return ranking


if __name__ == "__main__":
    print(get_game("sms"))
    print(games)