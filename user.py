from api import get_user_id, get_user_pbs, get_user_runs
from entries import Entry
from tables import Table_PBs, Table_Runs

class User:
    def __init__(self, username: str):
        def update_database(all_runs):
            def get_series_links(all_runs) -> tuple:
                """Small function that returns all series links."""
                links = []
                for run in all_runs:
                    for link in run["game"]["data"]["links"]:
                        if link["rel"] != "series":
                            continue
                        links.append(link["uri"])
                return tuple(set(links))
            Entry.update_game([y["game"]["data"] for y in all_runs])
            Entry.update_system([y["platform"]["data"] for y in all_runs])
            Entry.update_category([y["category"] for y in all_runs])
            Entry.update_subcategory(set(y["game"]["data"]["id"] for y in all_runs))
            Entry.update_release([y["game"]["data"] for y in all_runs])
            Entry.update_series(get_series_links(all_runs))

        self.username = username.capitalize()
        self.user_id = get_user_id(username)

        PBs = get_user_pbs(self.user_id)
        all_runs = get_user_runs(self.user_id)
        update_database(all_runs)

        self.PBs = Table_PBs(PBs)

    def __str__(self):
        return f'{self.username}\n{len(self.PBs)} runs'


if __name__ == "__main__":
    test = User("niamek")
    #test.PBs.sort()
    print(test.PBs)
