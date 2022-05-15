from requests_mock import Mocker
from entries.run import Run
from code_SRC.composantes import Time
from tests.class_builder import build_lb_l, build_lb, build_run, build_table_run

class Test_LB:
    def test_init(self, requests_mock:Mocker):
        test = build_lb_l(requests_mock)
        assert test.__dict__ == {"ranking":[5421 + x for x in range(1, 11)], "place":1}

        test = build_lb(requests_mock)
        assert test.__dict__ == {"ranking":[5421 + x for x in range(1, 11)], "place":1}
    def test_len(self,  requests_mock:Mocker):
        test = build_lb(requests_mock)
        assert len(test) == 10

    def test_str(self,  requests_mock:Mocker):
        test = build_lb(requests_mock)
        assert str(test) == "   1/10   (90.00%)"

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
        raise NotImplementedError(str(test))

    def test_count(self, requests_mock:Mocker):
        test = build_table_run(requests_mock)
        for x in test.keys():
            if isinstance(test[0][x], (str, set)):
                assert test.count(x) == 1
