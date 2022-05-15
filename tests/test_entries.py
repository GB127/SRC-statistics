from requests_mock import Mocker
from tests.class_builder import build_run_l, build_pb_l, build_gamecat, build_system, build_lb_l
from code_SRC.composantes import GameCate, System, Time

class Test_Run:
    def test_init(self, requests_mock:Mocker):
        test = build_run_l(requests_mock)
        assert set(test.__dict__) == {"time", "system", "gamecat"}
        assert isinstance(test.gamecat, GameCate)
        assert isinstance(test.time, Time)
        assert isinstance(test.system, System)

    def test_keys(self, requests_mock:Mocker):
        test = build_run_l(requests_mock)
        assert set(test.keys()) == {"game","series", "level", "release", "system", "time", "category"}
        for clé, valeur in [
            ("game", "Super Mario Sunshine"),
            ("series", {"Super Mario"}),
            ("level", "Shrub Forest"),
            ("release", "2002"),
            ("system", "Nintendo Entertainment System"),
            ("category", "Super Mario Sunshine: Shrub Forest Any% (No SSU) (150cc)")
            
            ]:
            assert test[clé] == valeur

    def test_str(self, requests_mock:Mocker):
        test = build_run_l(requests_mock)
        for composante in [build_gamecat, build_system]:
            assert str(composante(requests_mock)) in str(test)
        assert str(Time(5421)) in str(test)

class Test_PB:
    def test_init(self, requests_mock:Mocker):
        test = build_pb_l(requests_mock)
        assert ("leaderboard") in test.__dict__.keys()
    
    def test_str(self, requests_mock:Mocker):
        test = build_pb_l(requests_mock)
        assert "   1/10   (90.00%)" in str(test)