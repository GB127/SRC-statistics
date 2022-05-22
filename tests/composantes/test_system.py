from code_SRC.composantes import Time
from requests_mock.mocker import Mocker
from tests.class_builder import build_category, build_game, build_gamecat, build_system


class Test_system:
    def test_init(self, requests_mock:Mocker):
        test = build_system(requests_mock)
        assert test.__dict__ == {"system" : "Nintendo Entertainment System"}

    def test_keys(self, requests_mock:Mocker):
        test = build_system(requests_mock)
        assert test.keys() == {"system"}

    def test_str(self, requests_mock:Mocker):
        test = build_system(requests_mock)
        assert str(test) == "NES"

    def test_getitem(self, requests_mock:Mocker):
        test = build_system(requests_mock)
        assert test["system"] == "Nintendo Entertainment System"
