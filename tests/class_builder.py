from code_SRC.composantes import Category, Game, GameCate, System
from requests_mock.mocker import Mocker
from entries.run import Run, PB


def req_mocker(requests_mock: Mocker):
    """Function that will handle all mocks of the get"""
    system_data = {"data": {"id": "system_id","name": "Nintendo Entertainment System", "released": 1983}}
    game_data = {"data": {"id": "game_id", "names": {"international": "Super Mario Sunshine"},"abbreviation": "sms","released": 2002,"release-date": "2002-07-19","gametypes": [], "platforms": ["4p9z06rn", "v06dk3e4", "7m6ylw9p"], "regions": ["pr184lqn", "e6lxy1dz", "o316x197", "p2g50lnk"], "genres": ["qdnqkn8k", "jp23ox26"], "developers": ["xv6dvx62"], "publishers": ["m0rvylrx"],"links": [{"rel": "series", "uri": "https://www.speedrun.com/api/v1/series/serie_id"}]}}
    series_data = {"data": {"id": "serie_id","names": {"international": "Super Mario"},"abbreviation": "mario"}}
    level_data = {"data": {"id": "level_id","name": "Shrub Forest"}}
    category_data = {"data": {"id": "category_id","name": "Any% (No SSU)"}}

    requests_mock.get("https://www.speedrun.com/api/v1/platforms/system_id", json=system_data)
    requests_mock.get("https://www.speedrun.com/api/v1/series/serie_id", json=series_data)
    requests_mock.get("https://www.speedrun.com/api/v1/games/game_id", json=game_data)
    requests_mock.get("https://www.speedrun.com/api/v1/levels/level_id", json=level_data)
    requests_mock.get("https://www.speedrun.com/api/v1/categories/category_id", json=category_data)


def build_run(requests_mock: Mocker):
    req_mocker(requests_mock)
    run_data = {"id": "run_id", "game": "game_id", "level": "level_id", "category": "category_id","status": {"status": "verified"},"date": "2014-02-25", "times": {"primary_t": 5421},"system": {"platform": "system_id", "emulated": False, "region": None},"values": {"subcat_id":"selected_subcat"}}
    return Run(run_data)


def build_pb(requests_mock: Mocker):
    req_mocker(requests_mock)
    pb_data = {"place": 1, "run": {"id": "run_id", "game": "game_id", "level": "level_id", "category": "category_id","status": {"status": "verified"},"date": "2014-02-25", "times": {"primary_t": 5421},"system": {"platform": "system_id", "emulated": False, "region": None},"values": {"subcat_id":"selected_subcat"}}}
    return PB(pb_data)


def build_system(requests_mock: Mocker):
    req_mocker(requests_mock)
    return System("system_id")


def build_game(requests_mock: Mocker):
    req_mocker(requests_mock)
    return Game("game_id", "level_id")


def build_category(requests_mock: Mocker):
    req_mocker(requests_mock)
    return Category("category_id")


def build_gamecat(requests_mock: Mocker):
    req_mocker(requests_mock)
    return GameCate(Game("game_id", "level_id"), Category("category_id"))
