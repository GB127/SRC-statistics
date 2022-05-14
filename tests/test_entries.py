from requests_mock import Mocker
from tests.class_builder import build_run, build_pb

class Test_Run:
    def test_init(self, requests_mock:Mocker):
        test = build_run(requests_mock)
        assert set(test.__dict__) == {"time", "system", "game"}

    def test_str(self, requests_mock:Mocker):
        test = build_run(requests_mock)
        assert str(test) == "NES   Super Mario Sunshine: Shrub Forest       Any% (No SSU)     1:30:21"

class Test_PB:
    def test_init(self, requests_mock:Mocker):
        test = build_pb(requests_mock)
        assert set(test.__dict__) == {"time", "system", "game", "place", "leaderboard"}

    def test_str(self, requests_mock:Mocker):
        test = build_pb(requests_mock)
        assert str(test) == "NES   Super Mario Sunshine: Shrub Forest       Any% (No SSU)     1:30:21 (XXX%)"
