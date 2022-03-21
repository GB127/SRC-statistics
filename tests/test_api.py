from requests_mock.mocker import Mocker
from code_SRC.api import api
from tests.datas_fx import link_m, dicto_m, id_m, clear_db

#def test_category_no_requests(self, requests_mock:Mocker):
#    api.category_db["nxd1rk8q"] = "Any% (No SSU)"
#    requests_mock.get("https://www.speedrun.com/api/v1/categories/nxd1rk8q", exc=NotImplementedError("Requested instead of using saved data"))
#    assert api.category_db["nxd1rk8q"] == "Any% (No SSU)"

class Test_apis:
    @clear_db
    def test_game(self, requests_mock: Mocker):
        dicto_CE = dicto_m("game")
        dicto_CE["data"]["names"]["international"] += " Category Extensions"
        dicto_CE["data"]["names"]["international"] = "The Legend of " + dicto_CE["data"]["names"]["international"]
        requests_mock.get(link_m("game"), json=dicto_CE)
        assert 'Super Mario Sunshine' == api.game(id_m("game"))
        assert  api.game_db[id_m("game")] == "Super Mario Sunshine", "Game database not updated"

    def test_category(self, requests_mock: Mocker):
        requests_mock.get(link_m("category"), json=dicto_m("category"))
        assert 'Any%' == api.category(id_m("category"))
        assert 'Any%' == api.category_db[id_m("category")]

    def test_system(self, requests_mock: Mocker):
        dicto_VC = dicto_m("system")
        dicto_VC["data"]["name"] += " Virtual Console"
        requests_mock.get(link_m("system"), json=dicto_VC)
        assert 'Nintendo Entertainment System VC' == api.system(id_m("system")), api.system(id_m("system"))
        assert "Nintendo Entertainment System VC" == api.system_db[id_m("system")]
        assert "???" == api.system(None)

    def test_user_id(self, requests_mock:Mocker):
        requests_mock.get(link_m("user"), json=dicto_m("user"))
        assert id_m("user") == api.user_id(id_m("user"))  # Note : SRC s'occupe déjà de rediriger.

    def test_level(self, requests_mock: Mocker):
        requests_mock.get(link_m("level"), json=dicto_m("level"))
        assert 'Slip Slide Icecapades' == api.level(id_m('level'))
        assert api.level_db[id_m('level')] == 'Slip Slide Icecapades'

    def test_region(self, requests_mock: Mocker):
        requests_mock.get(link_m("region"), json=dicto_m("region"))
        assert 'USA / NTSC' == api.region(id_m('region'))
        assert api.region_db[id_m("region")] == "USA / NTSC"

    def test_lb(self, requests_mock: Mocker):
        requests_mock.get("https://www.speedrun.com/api/v1/leaderboards/xldev513/category/rklg3rdn", json=dicto_m("lb"))
        tempo = api.leaderboard("xldev513", "rklg3rdn")
        assert len(tempo) == 3
        assert all([isinstance(x, dict) for x in tempo])
        for clé in ["place", "run"]:
            assert clé in tempo[0].keys()





def test_api_rest(requests_mock:Mocker):
    requests_mock.get(link_m("region"), json={"status" : 420, "message": "allo"})
    pass


def test_runs(requests_mock: Mocker):
    raise NotImplementedError
def test_pbs(requests_mock: Mocker):
    raise NotImplementedError
