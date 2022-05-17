from code_SRC.composantes import Category, Game, GameCate, System
from requests_mock.mocker import Mocker
from entries.run import Run, PB
from tables.leaderboard import LB
from code_SRC.user import User
from tables.solo_runs import Table_pb, Table_run



def req_mocker(requests_mock: Mocker):
    """Function that will handle all mocks of the get"""
    system_data = {"data": {"id": "system_id","name": "Nintendo Entertainment System","released": 1983}}
    game_data = {"data": {"id": "game_id","names": {"international": "Super Mario Sunshine"},"abbreviation": "sms","released": 2002,"release-date": "2002-07-19","gametypes": [],"platforms": ["4p9z06rn", "v06dk3e4", "7m6ylw9p"],"regions": ["pr184lqn", "e6lxy1dz", "o316x197", "p2g50lnk"],"genres": ["qdnqkn8k", "jp23ox26"],"developers": ["xv6dvx62"],"publishers": ["m0rvylrx"],"links": [{"rel": "series","uri": "https://www.speedrun.com/api/v1/series/serie_id"}]}}
    series_data = {"data": {"id": "serie_id","names": {"international": "Super Mario"},"abbreviation": "mario"}}
    level_data = {"data": {"id": "level_id", "name": "Shrub Forest"}}
    category_data = {"data": {"id": "category_id", "name": "Any% (No SSU)"}}
    subcat_data_t = {"data": {"id": "subcat_id_t","name": "cc","values": {"values": {"selected_subcat": {"label": "150cc"}}},"is-subcategory": True}}
    subcat_data_f = {"data": {"id": "subcat_id_f","name": "cc","values": {"values": {"selected_subcat": {"label": "150cc"}}},"is-subcategory": False}}
    lb_data = {"data": {"game": "game_id","category": "category_id","level": "level_id",
                "runs": [{"place": x, "run": {"times": {"primary_t": 5421 + x}}} for x in range(1, 11)]}}

    requests_mock.get("https://www.speedrun.com/api/v1/platforms/system_id", json=system_data)
    requests_mock.get("https://www.speedrun.com/api/v1/series/serie_id", json=series_data)
    requests_mock.get("https://www.speedrun.com/api/v1/games/game_id", json=game_data)
    requests_mock.get("https://www.speedrun.com/api/v1/levels/level_id", json=level_data)
    requests_mock.get("https://www.speedrun.com/api/v1/categories/category_id", json=category_data)
    requests_mock.get("https://www.speedrun.com/api/v1/variables/subcat_id_t", json=subcat_data_t)
    requests_mock.get("https://www.speedrun.com/api/v1/variables/subcat_id_f", json=subcat_data_f)
    requests_mock.get("https://www.speedrun.com/api/v1/leaderboards/game_id/level/level_id/category_id",json=lb_data)
    requests_mock.get("https://www.speedrun.com/api/v1/leaderboards/game_id/category/category_id",json=lb_data)
    user_data = {"data":{"id":"user_id","names":{"international":"Niamek","japanese":None}}}
    requests_mock.get("https://www.speedrun.com/api/v1/users/username", json=user_data)
    user_pbs_data = {"data":
                            [
                                {"place": 1,"run": {"id": "run_id","game": "game_id","category": "category_id","status": {"status": "verified"}, "date": "2014-02-25", "times": {"primary_t": 5423}, "system": {"platform": "system_id", "emulated": False, "region": None}, "values": {"subcat_id_t": "selected_subcat", "subcat_id_f": "selected_subcat"},
                                            "level": None}},
                                {"place": 1,"run": {"id": "run_id","game": "game_id","category": "category_id","status": {"status": "verified"}, "date": "2014-02-25", "times": {"primary_t": 5423}, "system": {"platform": "system_id", "emulated": False, "region": None}, "values": {"subcat_id_t": "selected_subcat", "subcat_id_f": "selected_subcat"},
                                            "level": "level_id"}}
                            ]
                    }
    user_runs_data = {"data":
                            [
                                {"id": "run_id","game": "game_id","category": "category_id","status": {"status": "verified"}, "date": "2014-02-25", "times": {"primary_t": 5422}, "system": {"platform": "system_id", "emulated": False, "region": None}, "values": {"subcat_id_t": "selected_subcat", "subcat_id_f": "selected_subcat"},
                                            "level": None},
                                {"id": "run_id","game": "game_id","category": "category_id","status": {"status": "verified"}, "date": "2014-02-25", "times": {"primary_t": 5422}, "system": {"platform": "system_id", "emulated": False, "region": None}, "values": {"subcat_id_t": "selected_subcat", "subcat_id_f": "selected_subcat"},
                                            "level": "level_id"}
                            ],
                    "pagination":{"offset":0, "max":200, "size" : 2,
                        "links":[]}
                    }

    requests_mock.get("https://www.speedrun.com/api/v1/users/user_id/personal-bests", json=user_pbs_data)
    requests_mock.get("https://www.speedrun.com/api/v1/runs?user=user_id&max=200", json=user_runs_data)


def build_table_run(requests_mock:Mocker):
    req_mocker(requests_mock)
    tempo = Table_run([], True)
    tempo.data = [build_run(requests_mock) for _ in range(3)]
    return tempo

def build_table_pb(requests_mock:Mocker):
    req_mocker(requests_mock)
    tempo = Table_pb([], True)
    tempo.data = [build_pb(requests_mock) for _ in range(3)]
    return tempo


def build_user(requests_mock:Mocker):
    req_mocker(requests_mock)
    return User("username")

def build_run(requests_mock: Mocker):
    req_mocker(requests_mock)
    run_data = {
        "id": "run_id",
        "game": "game_id",
        "level": None,
        "category": "category_id",
        "status": {"status": "verified"},
        "date": "2014-02-25",
        "times": {"primary_t": 5422},
        "system": {"platform": "system_id", "emulated": False, "region": None},
        "values": {"subcat_id_t": "selected_subcat", "subcat_id_f": "selected_subcat"},
    }
    return Run(run_data)


def build_run_l(requests_mock: Mocker):
    req_mocker(requests_mock)
    run_data = {
        "id": "run_id",
        "game": "game_id",
        "level": "level_id",
        "category": "category_id",
        "status": {"status": "verified"},
        "date": "2014-02-25",
        "times": {"primary_t": 5422},
        "system": {"platform": "system_id", "emulated": False, "region": None},
        "values": {"subcat_id_t": "selected_subcat", "subcat_id_f": "selected_subcat"},
    }
    return Run(run_data)


def build_pb(requests_mock: Mocker):
    req_mocker(requests_mock)
    pb_data = {
        "place": 1,
        "run": {
            "id": "run_id",
            "game": "game_id",
            "level": None,
            "category": "category_id",
            "status": {"status": "verified"},
            "date": "2014-02-25",
            "times": {"primary_t": 5423},
            "system": {"platform": "system_id", "emulated": False, "region": None},
            "values": {
                "subcat_id_t": "selected_subcat",
                "subcat_id_f": "selected_subcat",
            },
        },
    }
    return PB(pb_data)


def build_pb_l(requests_mock: Mocker):
    req_mocker(requests_mock)
    pb_data = {
        "place": 1,
        "run": {
            "id": "run_id",
            "game": "game_id",
            "level": "level_id",
            "category": "category_id",
            "status": {"status": "verified"},
            "date": "2014-02-25",
            "times": {"primary_t": 5423},
            "system": {"platform": "system_id", "emulated": False, "region": None},
            "values": {
                "subcat_id_t": "selected_subcat",
                "subcat_id_f": "selected_subcat",
            },
        },
    }
    return PB(pb_data)


def build_system(requests_mock: Mocker):
    req_mocker(requests_mock)
    return System("system_id")


def build_game(requests_mock: Mocker):
    req_mocker(requests_mock)
    return Game("game_id", "level_id")


def build_category(requests_mock: Mocker):
    req_mocker(requests_mock)
    return Category(
        "category_id",
        {"subcat_id_t": "selected_subcat", "subcat_id_f": "selected_subcat"},
    )


def build_gamecat(requests_mock: Mocker):
    req_mocker(requests_mock)
    return GameCate(build_game(requests_mock), build_category(requests_mock))


def build_lb_l(requests_mock: Mocker):
    req_mocker(requests_mock)
    return LB(1, 
        *("game_id", "level_id", "category_id", [("subcat_id_t", "selected_subcat")])
    )

def build_lb(requests_mock: Mocker):
    req_mocker(requests_mock)
    return LB(1,
        *("game_id", None, "category_id", [("subcat_id_t", "selected_subcat")])
    )
