from api import URL, SRC_request
from generic import table, filtered_table
from entries import Run, PB, Saves

class User:
    def __init__(self, username):
        """ Class of a Speedrun.com user. The class contains informations such as username, runs, etc.
                username (str) : Username on speedrun.com"""
        def get_user_data(username):
            print(f"Getting {username}'s ID...")
            rep = SRC_request(f"{URL}/users/{username}")
            return rep["data"]

        def get_PBs(ID):
            """Requests the PBs of the username's ID provided."""
            print(f"Getting {self.username}'s PBs...")
            rep = SRC_request(f"{URL}/users/{ID}/personal-bests")
            return rep["data"]

        def get_runs(ID):
            """Returns a list of runs of the provided ID of the user."""
            print(f"Getting {self.username}'s Runs")
            runs = SRC_request(f"{URL}/runs?user={ID}&max=200")
            return runs

        self.username = username.capitalize()
        ID = get_user_data(self.username)["id"]
        Runs = get_runs(ID)

        PBs = get_PBs(ID)

        self.Runs = table(Run,[x for x in Runs if not x["level"]])
        self.PBs = table(PB,[x for x in PBs if not x["run"]["level"]])


        self.Games = filtered_table("game", self.Runs, self.PBs)
        self.Systems = filtered_table("system", self.Runs, self.PBs)


        self.Saves = Saves(self.PBs, self.Runs)
        print(f"user {self.username} initialized!")

    def __str__(self):
        string = f'{self.username}\n'
        for tableau in self.__dict__:
            if callable(self.__dict__[tableau]):
                string += f'{len(self.__dict__[tableau])} {tableau}\n'
        return string

    def __call__(self):
        command = input("Which table do you want to open? ")
        [tableau for tableau in self.__dict__.values() if callable(tableau)][int(command)]()

if __name__ == "__main__":
    # test = User("rudestjade")  # Has ran 1 game only.
    #test = User("libre")  # Has not a lot of runs.
    test = User("niamek")
    print(test.Saves)
    #print(test.Games)
    #print(test.PBs)
    #test()