from requests_mock.mocker import Mocker
from code_SRC.api import api
from tests.datas_fx import link_m, dicto_m, id_m




def clear_db(original_function):
    def new_function(self, requests_mock):
        for database in ["game_db", "category_db", "level_db", "system_db", "region_db", "system_db"]:
            setattr(api, database, {})
        original_function(self, requests_mock)
    return new_function


class Test_game:
    @clear_db
    def test_game_remove_cat_ext(self, requests_mock:Mocker):
        dicto_CE = dicto_m("game")
        dicto_CE["data"]["names"]["international"] += " Category Extensions"
        requests_mock.get(link_m("game"), json=dicto_CE)
        assert 'Super Mario Sunshine' == api.game(id_m("game"))

    @clear_db
    def test_game(self, requests_mock: Mocker):
        requests_mock.get(link_m("game"), json=dicto_m("game"))
        assert 'Super Mario Sunshine' == api.game(id_m("game"))

    @clear_db
    def test_game_update_db(self, requests_mock:Mocker):
        requests_mock.get(link_m("game"), json=dicto_m("game"))
        api.game(id_m("game"))
        assert  api.game_db[id_m("game")] == "Super Mario Sunshine", "Game database not updated"

    @clear_db
    def test_game_no_request(self, requests_mock:Mocker):
        requests_mock.get(link_m("game"), exc=NotImplementedError("Requested instead of using saved data"))
        api.game_db[id_m("game")] = "Super Mario Sunshine"
        assert api.game(id_m("game")) == "Super Mario Sunshine"

class Test_category:
    @clear_db
    def test_category(self, requests_mock: Mocker):
        requests_mock.get(link_m("category"), json=dicto_m("category"))
        assert 'Any%' == api.category(id_m("category"))

    @clear_db
    def test_category_update_db(self, requests_mock:Mocker):
        requests_mock.get(link_m("category"), json=dicto_m("category"))
        api.category(id_m("category"))
        assert 'Any%' == api.category_db[id_m("category")]


    @clear_db
    def test_category_no_requests(self, requests_mock:Mocker):
        api.category_db["nxd1rk8q"] = "Any% (No SSU)"
        requests_mock.get("https://www.speedrun.com/api/v1/categories/nxd1rk8q", exc=NotImplementedError("Requested instead of using saved data"))
        assert api.category_db["nxd1rk8q"] == "Any% (No SSU)"

class Test_system:

    @clear_db
    def test_system(self, requests_mock: Mocker):
        requests_mock.get(link_m("system"), json=dicto_m("system"))
        assert 'Nintendo Entertainment System' == api.system(id_m("system"))

    @clear_db
    def test_system_update_db(self, requests_mock: Mocker):
        requests_mock.get(link_m("system"), json=dicto_m("system"))
        api.system(id_m("system"))
        assert api.system_db[id_m("system")] == "Nintendo Entertainment System"

    @clear_db
    def test_system_norequest(self, requests_mock: Mocker):
        api.system_db[id_m("system")] = "Nintendo Entertainment System"
        requests_mock.get(link_m("system"), exc=NotImplementedError("Requested instead of using saved data"))
        assert api.system(id_m("system")) == "Nintendo Entertainment System"

    @clear_db
    def test_system_acro_vc(self, requests_mock:Mocker):
        dicto_VC = dicto_m("system")
        dicto_VC["data"]["name"] += " Virtual Console"
        requests_mock.get(link_m("system"), json=dicto_VC)
        assert api.system(id_m("system")) == "Nintendo Entertainment System VC"

class Test_user:
    def test_user_id(self, requests_mock:Mocker):
        requests_mock.get(link_m("user"), json=dicto_m("user"))
        assert id_m("user") == api.user_id(id_m("user"))  # Note : SRC s'occupe déjà de rediriger.

class Test_level:
    @clear_db
    def test_level(self, requests_mock: Mocker):
        requests_mock.get(link_m("level"), json=dicto_m("level"))
        assert 'Slip Slide Icecapades' == api.level(id_m('level'))
    @clear_db
    def test_level_update_db(self, requests_mock: Mocker):
        requests_mock.get(link_m("level"), json=dicto_m("level"))
        api.level(id_m('level'))
        assert api.level_db[id_m('level')] == 'Slip Slide Icecapades'
    @clear_db
    def test_level_norequest(self, requests_mock:Mocker):
        requests_mock.get(link_m("level"), exc=NotImplementedError("Requested instead of using saved data"))
        api.level_db[id_m('level')] = 'Slip Slide Icecapades'
        assert api.level(id_m("level")) == 'Slip Slide Icecapades'

class Test_region:
    @clear_db
    def test_region(self, requests_mock: Mocker):
        requests_mock.get(link_m("region"), json=dicto_m("region"))
        assert 'USA / NTSC' == api.region(id_m('region'))
    @clear_db
    def test_region_update_db(self, requests_mock: Mocker):
        requests_mock.get(link_m("region"), json=dicto_m("region"))
        api.region(id_m("region"))
        assert api.region_db[id_m("region")] == "USA / NTSC"

    @clear_db
    def test_region_norequest(self, requests_mock:Mocker):
        requests_mock.get(link_m("region"), exc=NotImplementedError("Requested instead of using saved data"))
        api.region_db[id_m("region")] = "US"
        assert api.region(id_m("region")) == "US"

    def test_api_rest(self, requests_mock:Mocker):
        raise NotImplementedError

class Test_tables:
    @clear_db
    def test_lb(self, requests_mock: Mocker):
        requests_mock.get("https://www.speedrun.com/api/v1/leaderboards/xldev513/category/rklg3rdn", json=dicto_m("lb"))
        tempo = api.leaderboard("xldev513", "rklg3rdn")
        assert len(tempo) == 3
        assert all([isinstance(x, dict) for x in tempo])
        for clé in ["place", "run"]:
            assert clé in tempo[0].keys()

    @clear_db
    def test_runs(self, requests_mock: Mocker):
        raise NotImplementedError
    @clear_db
    def test_pbs(self, requests_mock: Mocker):
        raise NotImplementedError
