from requests_mock.mocker import Mocker
from code_SRC.api import api
from tests.datas_fx import link_m, dicto_m, id_m, clear_db

class Test_apis:
    def test_update(self, requests_mock:Mocker):
        raise NotImplementedError


    def test_user_id(self, requests_mock:Mocker):
        requests_mock.get(link_m("user"), json=dicto_m("user"))
        assert id_m("user") == api.user_id(id_m("user"))  # Note : SRC s'occupe déjà de rediriger.

    def test_lb(self, requests_mock: Mocker):
        requests_mock.get("https://www.speedrun.com/api/v1/leaderboards/xldev513/category/rklg3rdn", json=dicto_m("lb"))
        tempo = api.leaderboard("xldev513", "rklg3rdn")
        assert len(tempo) == 3
        assert all([isinstance(x, dict) for x in tempo])
        for clé in ["place", "run"]:
            assert clé in tempo[0].keys()


def test_api_rest(requests_mock:Mocker):
    raise NotImplementedError("Need to figure out a way to test if the stalling works")

def test_runs(requests_mock: Mocker):
    requests_mock.get("https://www.speedrun.com/api/v1/runs?user=qxkq4o2x", json=dicto_m("user_runs"))
    assert api.user_runs("qxkq4o2x") == dicto_m("user_runs")["data"]

def test_pbs(requests_mock: Mocker):
    requests_mock.get("https://www.speedrun.com/api/v1/users/qxkgl2j0/personal-bests", json=dicto_m("user_pb"))
    assert api.user_pbs("qxkgl2j0") == dicto_m("user_pb")["data"]