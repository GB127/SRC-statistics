import requests
import datetime
import isodate
import time

URL = "https://www.speedrun.com/api/v1"

def recursive_requester(link, toupdate):
    """Recursive requester.

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
    """Generic requester.

        Args:
            link (string): link addition of the request

        Raises:
            BaseException: Raise error if the status code is 404.

        Returns:
            json: return the data in a json form
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
            raise BaseException("Incorrect info, please check again")
        else:
            raise BaseException(f"Please report this, {rep.status_code} - {URL}{link}")

def get_PBs(ID):
    """Requests the PBs of the said username

        Args:
            username (str): username

        Returns:
            data
        """
    rep = requester(f"/users/{ID}/personal-bests")
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

games = {}  # Used by get_game(ID) to reduce requests.
def get_game(ID):
    """Fetch the full name of the game.

        Args:
            ID (string): ID of the game, or acronym.
                If used elsewhere than this script, you can use an acronym instead
                of ID. But everywhere in this script, it uses ID, as the API gives
                you the ID of the games instead of the full name in the runs datas.

        Note : It uses the variable games to return data in order to reduce requests quantity.
        if it's a new game, it will do a request and update games accordingly so that future requests
        won't do a new request.

        Returns (str): Full name of the game
        """
    # ID or acronym
    try:
        return games[ID]
    except KeyError:
        rep = requester(f"/games/{ID}")
        games[ID] = rep["data"]["names"]["international"]
    return games[ID]

categories = {}  # Used by get_category(ID) to reduce requests.
def get_category(ID):
    """Fetch the full name of the category.

        Args:
            ID (string): ID of the category. Everywhere in this script, it uses ID, as the API gives
                you the ID of the games instead of the full name in the runs datas.

        Note : It uses the variable categories to return data in order to reduce requests quantity.
        if it's a new category, it will do a request and update categories accordingly so that future requests
        won't do a new request.

        Returns (str): Full name of the category
        """
    try:
        return categories[ID]
    except KeyError:
        rep = requester(f'/categories/{ID}')
        categories[ID] = rep["data"]["name"]
    return categories[ID]

def get_WR(gameID, categID, vari):
    """[summary]

    Args:
        gameID ([type]): [description]
        categID ([type]): [description]
        vari ([type]): [description]

    Returns:
        [type]: [description]
    """
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
    """[summary]

        Args:
            variID ([type]): [description]

        Returns:
            [type]: [description]
    """
    rep = requester(f'/variables/{variID}')
    return rep["data"]


leaderboard = {}
def get_len_leaderboard(gameID, categID, vari):
    """[summary]

    Args:
        gameID ([type]): [description]
        categID ([type]): [description]
        vari ([type]): [description]

    Returns:
        [type]: [description]
    """
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
    """[summary]

    Args:
        gameID ([type]): [description]
        categID ([type]): [description]
        vari ([type]): [description]

    Returns:
        [type]: [description]
    """
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

def get_leaderboards(gameID, categID, vari):
    # TODO: Enlever les temps sans date! (Ils sont dans toutes les années)
    """[summary]

        Args:
            gameID ([type]): [description]
            categID ([type]): [description]
            vari ([type]): [description]

        Returns:
            [type]: [description]
        """
    varistr = ""
    if vari != {}:
        tempo = []
        for key in vari:
            if get_variable(key)["is-subcategory"] is True: tempo.append(f"var-{key}={vari[key]}")
        varistr = "&" + "&".join(tempo)


    game_date = requester(f"/games/{gameID}")['data']["release-date"]
    now = str(datetime.date.today())

    rankings = {}
    for year in range(int(now[:4]), int(game_date[:4]), -1):
        tempo = []
        rep = requester(f"/leaderboards/{gameID}/category/{categID}?date={f'{year}-{now[5:7]}-{now[8:10]}'}" + varistr)
        for run in rep["data"]["runs"]:
            tempo.append((int(run["place"]), isodate.parse_duration(run["run"]["times"]["primary"]).total_seconds()))
        if len(tempo) == 0: break
        else: 
            rankings[year] = tempo
    return rankings


def get_newsystem(newsystem):
    """Debug function to find a new system to give a new acronym in the dictionnary.

        Args:
            newsystem (str): string to "acronymize". Need to be exactly the same.

        Result : print([ID] : "Full name")

        If no system matches with the newsystem seeked, it will print all available systems.
        Find the system you want to acronymize and rerun the code with the corrections.

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
systems = {  # It's the approach I use for using acronyms, as requesting a system will give you the full name.
    None : "PC",
    "n5683oev" : "GB",
    "gde3g9k1" : "GBC",
    "3167d6q2" : "GBA",
    "w89rwelk" : "N64",
    "jm95z9ol" : "NES",
    "3167jd6q" : "SGB",
    "83exk6l5" : "SNES",
    "4p9z06rn" : "GC",
    "mr6k0ezw" : "S.GEN",
    "nzelreqp" : "WII VC",
    "3167jd6q" : "SGB",
    "n5e147e2" : "SGB2",
    "wxeod9rn" : "PS",
    "n5e17e27" : "PS2",
    "mx6pwe3g" : "PS3",
    "nzelkr6q" : "PS4",
    }
def get_system(ID):
    """Return the system linked to the ID. If already defined, use a acornym. Else,
        return the full name.

        Args:
            ID (str): ID of the system.

        Returns: (str) Acronym of the system, or full name of the system.

        Note : it uses the variable systems defined in the code in order to reduce
        amount of requests. It doesn't update while running the code though: it needs to be updated manually
        before running the code.
    """
    try:
        return systems[ID]
    except KeyError:
        rep = requester(f"/platforms/{ID}")
        systems[ID] = rep["data"]["name"]
    return systems[ID]


def get_runs(ID):
    """Returns a list of all the runs (json form) by the user 
        identified with the ID provided. Uses the recursive requester.

        Args:
            ID (string) : ID of the user to fetch runs from.

        Returns (list) : list of all runs of the user (still in json data form).
    """
    runs = []  # List to update with the recursive requester.
    link_1 = f"{URL}/runs?user={ID}&max=200"  # First link of the recursive requester.

    recursive_requester(link_1, runs)  # Recursive request will update the list.
    return runs



if __name__ == "__main__":
    get_leaderboards("o1y9wo6q","7dgrrxk4", vari={}).keys()