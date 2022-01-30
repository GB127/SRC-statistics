from requests import get

class api:
    URL = "https://www.speedrun.com/api/v1/"
    tempo = {}

    @staticmethod
    def game(id:str) -> str:
        req = get(f'{api.URL}games/{id}').json()
        try:
            return req["data"]["names"]["international"]
        except:
            raise BaseException(id)

    def system(id) -> str:
        req = get(f'{api.URL}platforms/{id}').json()
        return req["data"]["name"]


    @staticmethod
    def category(id) -> str:
        req = get(f'{api.URL}categories/{id}').json()
        return req["data"]["name"]

    def level(id) -> str:
        req = get(f'{api.URL}levels/{id}').json()
        return req["data"]["name"]

    @staticmethod
    def user_id(username) -> str:
        req = get(f'{api.URL}users/{username}').json()
        return req["data"]["id"]

    @staticmethod
    def user_runs(user_id) -> list:
        pass

    @staticmethod
    def user_pbs(user_id) -> list:
        pass


if __name__ == "__main__":
    api.game("v1pxjz68")
    print(api.game("v1pxjz68"))