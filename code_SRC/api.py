from requests import get
from time import sleep

def requester(link):
    while True:
        try:
            data = get(link).json()
            assert "data" in data
            return data
        except AssertionError:
            print(data)
            print("Waiting... If you see this very often, please report")
            sleep(20)

class api:
    """api class to manage all requests. Stores data in a database.
        """
    URL = "https://www.speedrun.com/api/v1/"

