from requests_mock.mocker import Mocker
from code_SRC.api import api
from tests.datas_fx import link_m, dicto_m, id_m

def clear_db(original_function):
    def new_function(requests_mock):
        for database in ["game_db", "category_db", "level_db", "system_db"]:
            setattr(api, database, {})
        original_function(requests_mock)
    return new_function

@clear_db
def test_game_remove_cat_ext(requests_mock:Mocker):
    dicto_CE = dicto_m("game")
    dicto_CE["data"]["names"]["international"] += " Category Extensions"
    requests_mock.get(link_m("game"), json=dicto_CE)
    assert 'Super Mario Sunshine' == api.game(id_m("game"))

@clear_db
def test_game(requests_mock: Mocker):
    requests_mock.get(link_m("game"), json=dicto_m("game"))
    assert 'Super Mario Sunshine' == api.game(id_m("game"))

@clear_db
def test_game_update_db(requests_mock:Mocker):
    requests_mock.get(link_m("game"), json=dicto_m("game"))
    api.game(id_m("game"))
    assert  api.game_db[id_m("game")] == "Super Mario Sunshine", "Game database not updated"

@clear_db
def test_game_no_request(requests_mock:Mocker):
    requests_mock.get(link_m("game"), exc=NotImplementedError("Requested instead of using saved data"))
    api.game_db[id_m("game")] = "Super Mario Sunshine"
    assert api.game(id_m("game")) == "Super Mario Sunshine"


@clear_db
def test_category(requests_mock: Mocker):
    requests_mock.get(link_m("category"), json=dicto_m("category"))
    assert 'Any%' == api.category(id_m("category"))

@clear_db
def test_category_update_db(requests_mock:Mocker):
    requests_mock.get(link_m("category"), json=dicto_m("category"))
    api.category(id_m("category"))
    assert 'Any%' == api.category_db[id_m("category")]


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
    requests_mock.get(link_m("level"), json=dicto_m("level"))
    assert 'Slip Slide Icecapades' == api.level(id_m('level'))

def test_level_update_db(requests_mock: Mocker):
    requests_mock.get(link_m("level"), json=dicto_m("level"))
    api.level(id_m('level'))
    assert api.level_db[id_m('level')] == 'Slip Slide Icecapades'

def test_level_norequest(requests_mock:Mocker):
    requests_mock.get(link_m("level"), exc=NotImplementedError("Requested instead of using saved data"))
    api.level_db[id_m('level')] = 'Slip Slide Icecapades'
    assert api.level("495ggmwp") == 'Slip Slide Icecapades'

def test_region_norequest(requests_mock:Mocker):
    requests_mock.get("https://www.speedrun.com/api/v1/levels/495ggmwp", exc=NotImplementedError("Requested instead of using saved data"))
    api.region_db["tempo"] = "US"
    assert api.region("495ggmwp") == "US"

def test_region_update_db(requests_mock: Mocker):
    requests_mock.get("https://www.speedrun.com/api/v1/levels/495ggmwp", json=level_data)
    api.level("495ggmwp")
    assert api.region_db["495ggmwp"] == "Shrub Forest"

def test_region(requests_mock: Mocker):
    requests_mock.get("https://www.speedrun.com/api/v1/levels/495ggmwp", json=level_data)
    assert 'US' == api.region('495ggmwp')

