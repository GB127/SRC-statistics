from requests_mock import Mocker
from entries.run import Run
from code_SRC.composantes import Time
from tests.class_builder import build_lb_l, build_lb, build_run, build_table_pb, build_table_run

class Test_table_base:
    # Uses Table_run as a base.
    def test_str(self, requests_mock:Mocker):
        test = build_table_run(requests_mock)
        one_entry = str(build_run(requests_mock))
        one_line = "-" * len(one_entry)
        assert one_entry in str(test)
        assert str(test).count(one_entry) == 3
        assert one_line in str(test)
        assert str(test).count(one_line) == 2

    def test_group(self, requests_mock:Mocker):
        test = build_table_run(requests_mock)
        test.group_attr().items()

    def test_sum(self, requests_mock:Mocker):
        test = build_table_run(requests_mock)
        assert ("time",5422* 3) in test.sum().items()

    def test_dont_edit_table(self, requests_mock:Mocker):
        test = build_table_run(requests_mock)
        str1 = str(test[0])
        test.create_grouped(test.sum())
        assert str1 == str(test[0])
        

    def test_ineq_sumean(self, requests_mock:Mocker):
        test = build_table_run(requests_mock)
        assert test.create_grouped(test.sum()) != test.create_grouped(test.mean())
        assert test.create_grouped(test.sum()) != test.create_grouped(test.geomean())
        assert test.create_grouped(test.geomean()) != test.create_grouped(test.mean())
        assert test.create_grouped(test.sum()) != test[0]

    def test_mean(self, requests_mock:Mocker):
        test = build_table_run(requests_mock)
        assert ("time", 5422) in test.mean().items()

    def test_geomean(self, requests_mock:Mocker):
        test = build_table_run(requests_mock)
        assert ("time") in test.geomean().keys()

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

    def test_init(self, requests_mock:Mocker):
        test = build_table_run(requests_mock)
        assert str(test.create_grouped(test.sum())) in str(test)
        assert str(test.create_grouped(test.geomean())) in str(test)
        assert str(test.create_grouped(test.mean())) in str(test)