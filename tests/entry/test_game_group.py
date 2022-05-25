from requests_mock import Mocker
from tables.leaderboard import LB
from tests.class_builder import build_game_group
from code_SRC.composantes import GameCate, System, Time
from statistics import mean, geometric_mean as geomean

class Test_Group:
    def test_init(self, requests_mock:Mocker):
        test = build_game_group(requests_mock)
        assert set(test.__dict__.keys()) == {"mode", "group_name", "runs", "pbs"}


    def test_str(self, requests_mock:Mocker):
        test = build_game_group(requests_mock)
        assert str(test) == "allo"