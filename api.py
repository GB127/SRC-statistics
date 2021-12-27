import requests, datetime, time

URL = "https://www.speedrun.com/api/v1"

amount = 0

def response_analyser(response):
    if response.status_code == 200:
        return True
    elif response.status_code == 502:
        time.sleep(10)
    elif response.status_code == 404:
        raise BaseException(f"Error {response.status_code} : Incorrect info, please check again\n")
    elif response.status_code == 420 and response.json()['message'] == "The service is too busy to handle your request. Please try again later.":
        print("Server is busy, pausing...")
        time.sleep(60)
    else:
        raise BaseException(f"Please report this, {response.status_code}\n{response.json()['message']}")
    return False


def request_counter():
    global amount
    amount += 1

    if amount == 100:
        print("Slowing down...")
        time.sleep(20)
        amount = 0


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


def recursive_requester(link, toupdate):
    """Recursive requester with the provided link.

        Args:
            link (string): Complete link of the request to do. 
            toupdate (list): list to update with all the recursive requests.
                Should be an empty list as the goal of this function is to "return" a list.

        Returns nothing, but modify the "toupdate" list that can then be used elsewhere.
        """
    while True:
        rep = requests.get(link)
        if response_analyser(rep):
            rep = rep.json()
            break

    for run in rep["data"]:
        toupdate.append(run)
    if rep["pagination"]["size"] == rep["pagination"]["max"]:
        recursive_requester(rep["pagination"]["links"][-1]["uri"], toupdate)
    if rep["pagination"]["size"] < rep["pagination"]["max"]:
        pass


def requester(link):
    """Generic requester that request data with the link provided.
        Raises: BaseException: Raise error if bad data is given in the link.
        Returns : data in a json form
        """
    while True:
        rep = requests.get(f"{URL}{link}")
        request_counter()
        if response_analyser(rep):
            return rep.json()

def get_level(ID):
    """Fetch the full name of the level with an ID.
        """
    rep = requester(f"/levels/{ID}")
    return rep["data"]["name"]


if __name__ == "__main__":
    #print(get_game("ootextras"))

    rep = requester(f"/games/{'ootextras'}")
    print(rep["data"]["id"])