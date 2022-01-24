import requests
from copy import deepcopy
from time import sleep

URL = "https://www.speedrun.com/api/v1"

amount = 0

def SRC_request(link, initial=[]):
    toupdate = deepcopy(initial)
    def request_counter():
        global amount
        amount += 1
        if amount % 60 == 0:
            print("Slowing down...")
            sleep(20)

    def valid_link(response):
        if response.status_code == 200:
            return True
        elif response.status_code == 420:
            print(response.json()["message"])  # FIXME
            sleep(60)
        elif response.status_code == 404:
            raise BaseException(f"Error {response.status_code} : Incorrect info, please check again\nlink:{link}")
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


def get_level(ID):
    """Fetch the full name of the level with an ID.
        """
    rep = requester(f"/levels/{ID}")
    return rep["data"]["name"]


if __name__ == "__main__":
    #print(get_game("ootextras"))

    rep = SRC_request(f"{URL}/games/{'ootextras'}")

    rep_recu = SRC_request("https://www.speedrun.com/api/v1/runs?user=x7qz6qq8&max=200")
