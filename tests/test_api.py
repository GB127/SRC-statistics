from tests.test_datas import VC_mock, game_data, category_data,level_data, user_data, system_mock, game_category_extension
from requests_mock.mocker import Mocker
from code_SRC.api import api

def clear_db(original_function):
    def new_function(requests_mock):
        for database in ["game_db", "category_db", "level_db", "system_db"]:
            setattr(api, database, {})
        original_function(requests_mock)
    return new_function

@clear_db
def test_game_remove_cat_ext(requests_mock:Mocker):
    requests_mock.get('https://www.speedrun.com/api/v1/games/o1ymwk1q', json=game_category_extension)
    assert 'Super Mario 64' == api.game('o1ymwk1q')

@clear_db
def test_game(requests_mock: Mocker):
    requests_mock.get('https://www.speedrun.com/api/v1/games/v1pxjz68', json=game_data)
    assert 'Super Mario Sunshine' == api.game('v1pxjz68')

@clear_db
def test_game_update_db(requests_mock:Mocker):
    requests_mock.get('https://www.speedrun.com/api/v1/games/v1pxjz68', json=game_data)
    api.game("v1pxjz68")
    assert  api.game_db["v1pxjz68"] == "Super Mario Sunshine", "Game database not updated"

@clear_db
def test_game_no_request(requests_mock:Mocker):
    requests_mock.get('https://www.speedrun.com/api/v1/games/v1pxjz68', exc=NotImplementedError("Requested instead of using saved data"))
    api.game_db["v1pxjz68"] = "Super Mario Sunshine"
    assert api.game("v1pxjz68") == "Super Mario Sunshine"


@clear_db
def test_category(requests_mock: Mocker):
    requests_mock.get("https://www.speedrun.com/api/v1/categories/nxd1rk8q", json=category_data)
    assert 'Any% (No SSU)' == api.category('nxd1rk8q')

@clear_db
def test_category_update_db(requests_mock:Mocker):
    requests_mock.get("https://www.speedrun.com/api/v1/categories/nxd1rk8q", json=category_data)
    api.category('nxd1rk8q')
    assert 'Any% (No SSU)' == api.category_db["nxd1rk8q"]


@clear_db
def test_category_no_requests(requests_mock:Mocker):
    api.category_db["nxd1rk8q"] = "Any% (No SSU)"
    requests_mock.get("https://www.speedrun.com/api/v1/categories/nxd1rk8q", exc=NotImplementedError("Requested instead of using saved data"))
    assert api.category_db["nxd1rk8q"] == "Any% (No SSU)"


@clear_db
def test_system(requests_mock: Mocker):
    requests_mock.get("https://www.speedrun.com/api/v1/platforms/mx6pow93", json=system_mock)
    assert 'Acorn Archimedes' == api.system('mx6pow93')

@clear_db
def test_system_update_db(requests_mock: Mocker):
    requests_mock.get("https://www.speedrun.com/api/v1/platforms/mx6pow93", json=system_mock)
    api.system("mx6pow93")
    assert api.system_db["mx6pow93"] == "Acorn Archimedes"

@clear_db
def test_system_norequest(requests_mock: Mocker):
    api.system_db["mx6pow93"] = "Acorn Archimedes"
    requests_mock.get("https://www.speedrun.com/api/v1/platforms/mx6pow93", exc=NotImplementedError("Requested instead of using saved data"))
    assert api.system("mx6pow93") == "Acorn Archimedes"

@clear_db
def test_system_acro_vc(requests_mock:Mocker):
    requests_mock.get("https://www.speedrun.com/api/v1/platforms/mx6pow93", json=VC_mock)
    assert api.system("mx6pow93") == "Wii VC"



def test_user_id(requests_mock:Mocker):
    requests_mock.get("https://www.speedrun.com/api/v1/users/niamek", json=user_data)
    assert 'x7qz6qq8' == api.user_id('niamek')

def test_level(requests_mock: Mocker):
    requests_mock.get("https://www.speedrun.com/api/v1/levels/495ggmwp", json=level_data)
    assert 'Shrub Forest' == api.level('495ggmwp')

def test_level_update_db(requests_mock: Mocker):
    requests_mock.get("https://www.speedrun.com/api/v1/levels/495ggmwp", json=level_data)
    api.level("495ggmwp")
    assert api.level_db["495ggmwp"] == "Shrub Forest"

def test_level_norequest(requests_mock:Mocker):
    requests_mock.get("https://www.speedrun.com/api/v1/levels/495ggmwp", exc=NotImplementedError("Requested instead of using saved data"))
    api.level_db["495ggmwp"] = "Shrub Forest"
    assert api.level("495ggmwp") == "Shrub Forest"
