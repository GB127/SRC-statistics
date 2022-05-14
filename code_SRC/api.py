from requests import get

def requester(link):
    data = get(link).json()
    return data

class api:
    """api class to manage all requests. Stores data in a database.
        """
    URL = "https://www.speedrun.com/api/v1/"

    def system(id):
        req = requester(api.URL + f'platforms/{id}')
        return req["data"]["name"]

    def level(id):
        req = requester(api.URL + f'levels/{id}')
        return req["data"]["name"]

    def category(id):
        req = requester(api.URL + f'categories/{id}')
        return req["data"]["name"]


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