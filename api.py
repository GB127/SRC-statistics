import requests, datetime, time
from tools import run_time

URL = "https://www.speedrun.com/api/v1"


def get_leaderboard_level(IDs):
    varistr = ""
    if IDs[3] != {}:
        tempo = []
        for key in IDs[3]:
            tempo.append(f"var-{key}={IDs[3][key]}")
        varistr = "&".join(tempo)
        if varistr != "": varistr = "?" + varistr

    rep = requester(f"/leaderboards/{IDs[0]}/level/{IDs[2]}/{IDs[1]}" + varistr)
    return rep



def get_leaderboards(IDs):
    # TODO: Enlever les temps sans date! (Ils sont dans toutes les années)
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
        print(f"Getting year {year} leaderboard")
        tempo = []
        rep = requester(f"/leaderboards/{IDs[0]}/category/{IDs[1]}?date={f'{year}-{now[5:7]}-{now[8:10]}'}" + varistr)
        for run in rep["data"]["runs"]:
            tempo.append((run_time(run["run"]["times"]["primary_t"])))
        if len(tempo) == 0: break
        else: 
            rankings[year] = tempo
    return rankings

def get_leaderboards_level(IDs):
    # TODO: Enlever les temps sans date! (Ils sont dans toutes les années)
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
        print(f"Getting year {year} leaderboard")
        tempo = []
        rep = requester(f"/leaderboards/{IDs[0]}/level/{IDs[2]}/{IDs[1]}?date={f'{year}-{now[5:7]}-{now[8:10]}'}" + varistr)

        for run in rep["data"]["runs"]:
            tempo.append((run_time(run["run"]["times"]["primary_t"])))
        if len(tempo) == 0: break
        else: 
            rankings[year] = tempo
    return rankings




########### Below this are function that works. No need of improving.

def get_leaderboard(IDs):
    varistr = ""
    if IDs[2] != {}:
        tempo = []
        for key in IDs[3]:
            tempo.append(f"var-{key}={IDs[3][key]}")
        varistr = "&".join(tempo)
        if varistr != "": varistr = "?" + varistr
    rep = requester(f"/leaderboards/{IDs[0]}/category/{IDs[1]}" + varistr)
    return rep




def get_variable(variID):
    """ Returns json data about the speedrun variable identified by ID.
        => Notable infos: 
            "is-subcategory"
            "values", "values", "label"
    """
    rep = requester(f'/variables/{variID}')
    return rep["data"]


def get_newsystem(newsystem):
    """Debug function to find a new system to give a new acronym in the dictionnary.

        Args:
            newsystem (str): string to "acronymize". Need to be exact.

        Result : print([ID] : "Full name")
            NOTE: If no system matches, print all available systems.

        """
    rep = requester(f"/platforms?max=200")
    for system in rep["data"]:
        if system["name"] == newsystem: 
            print("-------------------------------------")
            print(f'"{system["id"]}" : "{system["name"]}",')
            print("-------------------------------------")
            return
    for system in rep["data"]:
        print(system["name"])


def recursive_requester(link, toupdate):
    """Recursive requester with the provided link.

        Args:
            link (string): Complete link of the request to do. 
            toupdate (list): list to update with all the recursive requests.
                Should be an empty list as the goal of this function is to "return" a list.

        Returns nothing, but modify the "toupdate" list that can then be used elsewhere.
        """
    rep = requests.get(link)
    if rep.status_code == 200:
        rep = rep.json()
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
        # It's in a loop in order to bypass the 502 status code.
        rep = requests.get(f"{URL}{link}")
        if rep.status_code == 200:
            return rep.json()
        elif rep.status_code == 502:
            time.sleep(10)
        elif rep.status_code == 404:
            print(rep.status_code)
            print(f"{URL}{link}")
            raise BaseException(f"Incorrect info, please check again\n{URL}{link}")
        else:
            raise BaseException(f"Please report this, {rep.status_code} - {URL}{link}\n{rep.json()['message']}")


def get_PBs(ID):
    """Requests the PBs of the said username identified with the ID.
        Returns: data (json format)
        """
    rep = requester(f"/users/{ID}/personal-bests")
    return rep["data"]

def get_userID(username):
    """Get the user ID of a username.
        Returns:
            ID (str)
        """
    rep = requester(f"/users/{username}")
    return rep["data"]["id"]

def get_game(ID):
    """Fetch the full name of the game with an ID or acronym(str).
        """
    rep = requester(f"/games/{ID}")
    return rep["data"]["names"]["international"]

def get_category(ID):
    """Fetch the full name of the category with an ID.
        Returns (str): Full name of the category
        """
    rep = requester(f'/categories/{ID}')
    return rep["data"]["name"]


def get_system(ID):
    """Return the system.
        Returns: (str) full name of the system.
        """
    rep = requester(f"/platforms/{ID}")
    return rep["data"]["name"]

def get_runs(ID):
    """Returns a list of all the runs (json form) by the user 
        identified with the ID provided. Uses the recursive requester.

        Returns (list) : list of all runs of the user (still in json data form).
    """
    runs = []  # List to update with the recursive requester.
    link_1 = f"{URL}/runs?user={ID}&max=200"  # First link of the recursive requester.

    recursive_requester(link_1, runs)  # Recursive request will update the list.
    return runs

def get_user(ID):
    """Get the user  of a user ID.
        Returns:
            ID (str)
        """
    rep = requester(f"/users/{ID}")
    return rep["data"]["names"]["international"]







#####################


def get_level(ID):
    """Fetch the full name of the level with an ID.
        """
    rep = requester(f"/levels/{ID}")
    return rep["data"]["name"]




if __name__ == "__main__":
    print(get_level("nwl6ky0w"))