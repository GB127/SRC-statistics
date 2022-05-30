from requests import get
from datetime import datetime
from time import sleep


def requester(link):
    """Make a request using the link provided. If data received doesn't have data in it, will wait 2 minutes and retry."""
    while True:
        data = get(link).json()
        if "data" in data.keys():
            return data
        print("Got the mximum of requests per minute, waiting...")
        sleep(120)


class api:
    """api class to manage all requests. Stores data in a database."""

    URL = "https://www.speedrun.com/api/v1/"

    game_db = {}
    system_db = {}
    category_db = {}
    subcategory_db = {}
    region_db = {}
    series_db = {}
    level_db = {}
    release_db = {}

    @staticmethod
    def db(desired_db, key_id):
        try:
            return api.__dict__[desired_db + "_db"][key_id]
        except KeyError:
            return ""

    @staticmethod
    def user_id(username: str) -> str:
        """Makes a request to the SRC API to retrieve the ID of the given username.
        Args:
            username (str): Username
        Returns:
            str: ID of the username
        """
        req = requester(f"{api.URL}users/{username}")
        return req["data"]["id"]

    @staticmethod
    def user_pbs(user_id):
        req = requester(api.URL + f"users/{user_id}/personal-bests")
        return req["data"]

    @staticmethod
    def user_runs(user_id: str) -> list:
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

        def update_databases(data):
            def update_subcategory(id: tuple):
                req = requester(api.URL + f"variables/{id[0]}")
                if req["data"]["is-subcategory"]:
                    api.subcategory_db[id] = req["data"]["values"]["values"][id[1]][
                        "label"
                    ]
                else:
                    api.subcategory_db[id] = ""

            def get_series(links):
                all_series = []
                for link in links:
                    if link["rel"] != "series":
                        continue
                    serie_data = requester(link["uri"])
                    all_series.append(serie_data["data"]["names"]["international"])
                return set(all_series)

            for no_run, run in enumerate(data, start=1):
                print(f"Updating databases with run #{no_run}/{len(data)}")
                api.game_db[run["game"]["data"]["id"]] = run["game"]["data"]["names"][
                    "international"
                ]
                if not run["game"]["data"]["id"] in api.series_db:
                    api.series_db[run["game"]["data"]["id"]] = get_series(
                        run["game"]["data"]["links"]
                    )
                api.category_db[run["category"]["data"]["id"]] = run["category"][
                    "data"
                ]["name"]
                if run["region"]["data"]:
                    api.region_db[run["region"]["data"]["id"]] = run["region"]["data"][
                        "name"
                    ]

                if run["platform"]["data"]:
                    api.system_db[run["platform"]["data"]["id"]] = run["platform"][
                        "data"
                    ]["name"]
                if run["level"]["data"]:
                    api.level_db[run["level"]["data"]["id"]] = run["level"]["data"][
                        "name"
                    ]
                api.release_db[run["game"]["data"]["id"]] = run["game"]["data"][
                    "released"
                ]

                for variable in run["values"].items():
                    update_subcategory(variable)

        def change_to_id(data):
            for no_run, run in enumerate(data, start=1):
                print(f"Updating data of run #{no_run}/{len(data)}")
                run["game"] = run["game"]["data"]["id"]
                run["category"] = run["category"]["data"]["id"]
                if run["region"]["data"]:
                    run["region"] = run["region"]["data"]["id"]
                if run["level"]["data"]:
                    run["level"] = run["level"]["data"]["id"]
                else:
                    run["level"] = None

        link = f"{api.URL}runs?user={user_id}&max=200&embed=game,category,level,region,platform"
        data = recursive_request(link)
        print("All runs data obtained!")
        update_databases(data)
        change_to_id(data)

        return data

    @staticmethod
    def leaderboard(game_id, level_id, category_id, subcat_ids):
        variables = ""
        if subcat_ids:
            variables = "&var-".join([f"{x}={y}" for x, y in subcat_ids])

        if level_id:
            req = requester(
                api.URL
                + f"leaderboards/{game_id}/level/{level_id}/{category_id}?var-{variables}"
            )
            return [x["run"]["times"]["primary_t"] for x in req["data"]["runs"]]
        req = requester(
            api.URL + f"leaderboards/{game_id}/category/{category_id}?var-{variables}"
        )
        return [x["run"]["times"]["primary_t"] for x in req["data"]["runs"]]

    @staticmethod
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
