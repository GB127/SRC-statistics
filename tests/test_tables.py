from requests_mock import Mocker
from entries.run import Run
from code_SRC.composantes import Time
from tests.class_builder import build_lb_l, build_lb, build_run, build_table_pb, build_table_run

class Test_LB:
    def test_init(self, requests_mock:Mocker):
        test = build_lb_l(requests_mock)
        assert test.__dict__ == {"ranking":tuple(5421 + x for x in range(1, 11)), "place":1}

        test = build_lb(requests_mock)
        assert test.__dict__ == {"ranking":tuple(5421 + x for x in range(1, 11)), "place":1}
    def test_len(self,  requests_mock:Mocker):
        test = build_lb(requests_mock)
        assert len(test) == 10

    def test_str(self,  requests_mock:Mocker):
        test = build_lb(requests_mock)
        assert str(test) == "   1/10   (90.00%)"

    def test_getitem(self, requests_mock:Mocker):
        test = build_lb(requests_mock)
        assert test["WR"] == Time(5422), f'Time({test["WR"].seconds})'


class Test_table_runs:
    def test_init(self, requests_mock:Mocker):
        test = build_table_run(requests_mock)
        assert "data" in test.__dict__.keys() and isinstance(test.__dict__["data"], list)
        assert isinstance(test.__dict__["data"][0], Run)


    def test_str(self, requests_mock:Mocker):
        test = build_table_run(requests_mock)
        one_entry = str(build_run(requests_mock))
        one_line = "-" * len(one_entry)
        assert one_entry in str(test)
        assert str(test).count(one_entry) == 3
        assert one_line in str(test)
        assert str(test).count(one_line) == 2
        for strings in [test.str_sum(), test.str_geomean(), test.str_sum()]:
            assert strings in str(test)

    def test_count(self, requests_mock:Mocker):
        test = build_table_run(requests_mock)
        for x in test.keys():
            if isinstance(test[0][x], (str, set)):
                assert test.count(x) == 1

    def test_str_sum(self, requests_mock:Mocker):
        test = build_table_run(requests_mock)
        assert str(Time(5422*3)) in test.str_sum()
        for counts in ["1 games", "1 categories", "1 s"]:
            assert counts in test.str_sum()

    def test_str_mean(self, requests_mock:Mocker):
        test = build_table_run(requests_mock)
        assert str(Time(5422)) in test.str_mean()
        for counts in ["3.0 games", "3.0 categories", "3.0"]:
            assert counts in test.str_mean(), test.str_mean()


class Test_table_pbs:
    def test_str(self, requests_mock:Mocker):
        test = build_table_pb(requests_mock)
        str(test)


    def test_getitem(self, requests_mock:Mocker):
        test = build_table_pb(requests_mock)
        assert f' +{str(Time(3)).lstrip()}' in test.str_sum()
        assert f"   3/30   ({27/30:.2%})" in test.str_sum()