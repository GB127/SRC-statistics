from requests import get
import warnings

def requester(link):
    data = get(link).json()
    return data

class api:
    """api class to manage all requests. Stores data in a database.
        """
    URL = "https://www.speedrun.com/api/v1/"


    def user_pbs(user_id):
        req = requester(api.URL + f'users/{user_id}/personal-bests')
        return req["data"]


    def system(id):
        req = requester(api.URL + f'platforms/{id}')
        return req["data"]["name"]

    def level(id):
        req = requester(api.URL + f'levels/{id}')
        return req["data"]["name"]

    def category(id):
        req = requester(api.URL + f'categories/{id}')
        return req["data"]["name"]

    def subcategory(id:dict):
        req = requester(api.URL + f'variables/{id[0]}')
        if req["data"]["is-subcategory"]:
            return req["data"]["values"]["values"][id[1]]["label"]

    def leaderboard(game_id, category_id, subcat_ids):
        variables= ""
        if subcat_ids:
            variables = "&var-".join([f"{x}={y}" for x,y in subcat_ids])
        req = requester(api.URL + f'leaderboards/{game_id}/category/{category_id}?var-{variables}')
        return [x["run"]["times"]["primary_t"] for x in req["data"]["runs"]]

    def leaderboard_l(game_id, level_id, category_id, subcat_ids):
        variables= ""
        if subcat_ids:
            variables = "&var-".join([f"{x}={y}" for x,y in subcat_ids])
        req = requester(api.URL + f'leaderboards/{game_id}/level/{level_id}/{category_id}?var-{variables}')
        return [x["run"]["times"]["primary_t"] for x in req["data"]["runs"]]

    def user_id(username:str) -> str:
            """Makes a request to the SRC API to retrieve the ID of the given username.
            Args:
                username (str): Username
            Returns:
                str: ID of the username
            """
            req = requester(f'{api.URL}users/{username}')
            return req["data"]["id"]

    def user_runs(user_id:str) -> list:
        req = requester(f'{api.URL}runs?user={user_id}&max=200')
        return req["data"]


    @staticmethod
    def game(id):  #TODO : Embed thing with series so we avoid to duplicate requests
        def serie(links):
            toreturn = set()
            for link in links:
                if link["rel"] == "series":
                    req_serie = requester(link["uri"])
                    toreturn.add(req_serie["data"]["names"]["international"])
            return toreturn
        req = requester(api.URL + f'games/{id}')
        return req["data"]["names"]["international"], req["data"]["released"], serie(req["data"]["links"])