import requests, datetime
from copy import deepcopy
from time import sleep

URL = "https://www.speedrun.com/api/v1"

amount = 0

def SRC_request(link, initial=[]):
    toupdate = deepcopy(initial)
    def request_counter():
        global amount
        amount += 1
        print(amount)
        if amount % 80 == 0:
            print("Slowing down...")
            sleep(20)

    def valid_link(response):
        if response.status_code == 200:
            return True
        elif response.status_code == 420:
            print(response.json()["message"])  # FIXME
            sleep(60)
        elif response.status_code == 404:
            raise BaseException(f"Error {response.status_code} : Incorrect info, please check again\nlink: {URL}{link}")
        else:
            raise BaseException(f"Please report the following informations on github => https://github.com/GB127/SRC-statistics/issues\nLink: {URL}{link}\nResponse code: {response.status_code}\nResponse message: {response.json()['message']}")

    request_counter()
    rep = requests.get(f"{link}")
    while not valid_link(rep):
        request_counter()
        rep = requests.get(f"{link}")
    rep = rep.json()
    if isinstance(rep["data"], list):
        toupdate += rep["data"]
    try:
        if rep["pagination"]["size"] == rep["pagination"]["max"]:
            SRC_request(rep["pagination"]["links"][-1]["uri"], toupdate)
        if rep["pagination"]["size"] < rep["pagination"]["max"]:
            pass
    except KeyError:
        return rep
    return toupdate




def get_leaderboards(IDs):
    varistr = ""
    if IDs[3] != {}:
        tempo = []
        for key in IDs[3]:
            tempo.append(f"var-{key}={IDs[3][key]}")
        varistr = "&".join(tempo)
        if varistr != "": varistr = "?" + varistr


    game_date = requester(f"/games/{IDs[0]}")['data']["release-date"]
    now = str(datetime.date.today())




    rankings = {}
    for year in range(int(now[:4]), int(game_date[:4]), -1):
        base_URL = f'/leaderboards/{IDs[0]}/'
        base_date = f"?date={f'{year}-{now[5:7]}-{now[8:10]}'}"
        if IDs[2]:
            full_level = f"level/{IDs[2]}/{IDs[1]}"
        else:
            full_level = f'category/{IDs[1]}'

        print(f"Getting year {year} leaderboard")
        tempo = []
        rep = requester(f"{base_URL}{full_level}{base_date}{varistr}")
        for run in rep["data"]["runs"]:
            tempo.append((run_time(run["run"]["times"]["primary_t"])))
        if len(tempo) == 0: break
        else: 
            rankings[year] = tempo
    return rankings


def get_level(ID):
    """Fetch the full name of the level with an ID.
        """
    rep = requester(f"/levels/{ID}")
    return rep["data"]["name"]


if __name__ == "__main__":
    #print(get_game("ootextras"))

    rep = SRC_request(f"{URL}/games/{'ootextras'}")

    rep_recu = SRC_request("https://www.speedrun.com/api/v1/runs?user=x7qz6qq8&max=200")
