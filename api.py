from requests import get
from requests.exceptions import InvalidURL
from time import sleep

URL = "https://www.speedrun.com/api/v1/"


def requester(link):
    """Make a request using the link provided. If data received doesn't have data in it, will wait 2 minutes and retry."""
    while True:
        data = get(link).json()
        if "data" in data.keys():
            return data
        elif data["status"] == 404:
            raise InvalidURL(link)
        elif data["status"] == 420:
            print("Got the maximum of requests per minute, waiting...")
            sleep(20)
        raise BaseException(f'Please do something here\n{data}')


def get_user_id(username: str) -> str:
        """Makes a request to the SRC API to retrieve the ID of the given username.
        Args:
            username (str): Username
        Returns:
            str: ID of the username
        """
        req = requester(f"{URL}users/{username}")
        return req["data"]["id"]

def get_user_pbs(user_id:str) -> list:
        req = requester(URL + f"users/{user_id}/personal-bests")
        return req["data"]

def get_user_runs(user_id:str) -> list:
    def recursive_request(link, current=0):
        print(f"Data fetched: {current * 200}")
        req = requester(link)
        runs = req["data"]
        if not req["pagination"]["links"]:
            return runs
        elif req["pagination"]["links"][-1]["rel"] != "next":
            return runs
        return runs + recursive_request(
            req["pagination"]["links"][-1]["uri"], current + 1
        )
    link = f"{URL}runs?user={user_id}&max=200&embed=game,category,level,region,platform"
    data = recursive_request(link)
    return data

def get_game_variables(game_id:str):
    data = requester(URL + f"games/{game_id}/variables")
    return data["data"]

def get_serie(link:str) -> dict:
    return requester(link)["data"]



def get_leaderboard(game_id, level_id, category_id, subcat_ids):
    variables = ""
    if subcat_ids:
        variables = "&var-".join([f"{x}={y}" for x, y in subcat_ids])

    if level_id:
        req = requester(
            URL
            + f"leaderboards/{game_id}/level/{level_id}/{category_id}?var-{variables}"
        )
        return [x["run"]["times"]["primary_t"] for x in req["data"]["runs"]]
    req = requester(
        URL + f"leaderboards/{game_id}/category/{category_id}?var-{variables}"
    )
    return tuple(x["run"]["times"]["primary_t"] for x in req["data"]["runs"])


"""
def past_lb(released, game_id, level_id, category_id, subcat_ids):
    def request_lb(year):
        if level_id:
            req = requester(
                api.URL
                + f"leaderboards/{game_id}/level/{level_id}/{category_id}?var-{variables}&date={year}"
            )
            return [x["run"]["times"]["primary_t"] for x in req["data"]["runs"]]
        req = requester(
            api.URL
            + f"leaderboards/{game_id}/category/{category_id}?var-{variables}&date={year}"
        )
        return [x["run"]["times"]["primary_t"] for x in req["data"]["runs"]]

    variables = ""
    if subcat_ids:
        variables = "&var-".join([f"{x}={y}" for x, y in subcat_ids])
    date_filter = datetime.date.today()

    rankings = {}
    for new_year in range(date_filter.year, released, -1):
        this_year_ranking = request_lb(date_filter.isoformat())
        if this_year_ranking in rankings.values():
            continue
        elif this_year_ranking:
            rankings[new_year] = this_year_ranking
            date_filter = date_filter.replace(year=new_year - 1)
        else:  # No more leaderboard : lb is empty
            break
    return rankings
"""

if __name__ == "__main__":
    print(get_game_variables("pdvzywv6"))