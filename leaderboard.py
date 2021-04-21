from api import get_leaderboard2, get_user
from generic import table
from tools import run_time

class leaderboard(table):
    def __init__(self, IDs):
        print("Initializing leaderboard data, please wait")
        infos = get_leaderboard2(IDs)["data"]["runs"]
        self.data = []

        self.WR = run_time(infos[0]["run"]["times"]["primary_t"])
        for one in infos:
            self.data.append(entry(one, self.WR))

    def __len__(self):
        return len(self.data)

class entry:
    table_size = [10,10]
    def __init__(self, data, WR):
        self.WR = WR
        self.place = data["place"]
        # WONTFIX : The thing with the current api is that it returns IDs. If I want all of them I have to update all of them...
        #try:
        #    self.player = [data["run"]["players"][0]["id"]]  # TODO: For now solo runs only
        #except KeyError:
        #    self.player = data["run"]["players"][0]["name"]  # TODO: For now solo runs only
        self.time = run_time(data["run"]["times"]["primary_t"])
    
    def __str__(self):
        return f'{self.time:>9} |'

    def __lt__(self, other):
        return self.time < other.time


if __name__ == "__main__":
    test = ['j1l9qz1g', '9d85yqdn', {}]
    test = leaderboard(test)
    test()