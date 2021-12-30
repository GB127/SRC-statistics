from api import requester, URL, recursive_requester
from generic import table, filtered_table
from entries import Run, PB

class user:
    def __init__(self, username):
        """ Class of a Speedrun.com user. The class contains informations such as username, runs, etc.
                username (str) : Username on speedrun.com"""
        def get_user_data(username):
            print(f"Getting {username}'s ID...")
            rep = requester(f"/users/{username}")
            return rep["data"]

        def get_PBs(ID):
            """Requests the PBs of the username's ID provided."""
            print(f"Getting {self.username}'s PBs...")
            rep = requester(f"/users/{ID}/personal-bests")
            return rep["data"]

        def get_runs(ID):
            """Returns a list of runs of the provided ID of the user."""
            print(f"Getting {self.username}'s Runs")
            runs = []  # List to update with the recursive requester.
            link_1 = f"{URL}/runs?user={ID}&max=200"  # First link of the recursive requester.
            recursive_requester(link_1, runs)  # Recursive request will update the list.
            return runs

        self.username = username.capitalize()
        ID = get_user_data(self.username)["id"]
        Runs = get_runs(ID)
        PBs = get_PBs(ID)

        self.Runs = table(Run,[x for x in Runs if not x["level"]])
        self.PBs = table(PB,[x for x in PBs if not x["run"]["level"]])


        self.Games = filtered_table("game", self.Runs, self.PBs)

        self.Systems = filtered_table("system", self.Runs, self.PBs)

        print(f"user {self.username} initialized!")

if __name__ == "__main__":
    test = user("V0oid")
    print(test.Systems)