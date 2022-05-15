from requests_mock import Mocker
from tests.class_builder import build_lb_l, build_lb

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
