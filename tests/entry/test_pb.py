from requests_mock import Mocker
from tables.leaderboard import LB
from tests.class_builder import build_run_l, build_pb_l, build_gamecat, build_system, build_lb_l
from code_SRC.composantes import GameCate, System, Time
from statistics import mean, geometric_mean as geomean

class Test_PB:
    def test_init(self, requests_mock:Mocker):
        test = build_pb_l(requests_mock)
        assert ("leaderboard") in test.__dict__.keys() and isinstance(test.leaderboard, LB)
        assert ("delta" ,Time(1)) in test.__dict__.items(), f'Time({test.delta.seconds})'
        assert ("perc" ,5423/5422) in test.__dict__.items(), f'{test.perc}'

    def test_wr(self, requests_mock:Mocker):
        test = build_pb_l(requests_mock)
        assert test["WR"] == Time(5422), f'{test["WR"]} == {Time(5422)}'

    def test_str(self, requests_mock:Mocker):
        test = build_pb_l(requests_mock)
        assert "   1/10   (90.00%)" in str(test)
        assert f'+{str(Time(1)).lstrip()} (100.02%)' in str(test)
        # Uncomment this following line when adjusting.
        # raise BaseException(f'\n{test}')