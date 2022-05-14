from requests_mock import Mocker
from tests.class_builder import build_run, build_pb, build_gamecat, build_system
from code_SRC.composantes import Time

class Test_Run:
    def test_init(self, requests_mock:Mocker):
        test = build_run(requests_mock)
        assert set(test.__dict__) == {"time", "system", "game"}

    def test_str(self, requests_mock:Mocker):
        test = build_run(requests_mock)
        for composante in [build_gamecat, build_system]:
            assert str(composante(requests_mock)) in str(test)
        assert str(Time(5421)) in str(test)

class Test_PB:
    def test_init(self, requests_mock:Mocker):
        test = build_pb(requests_mock)
        assert ("place", 1) in test.__dict__.items()
        raise NotImplementedError("Leaderboard")