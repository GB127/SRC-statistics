from requests_mock.mocker import Mocker
from tests.class_builder import build_category, build_game, build_gamecat

class Test_gamecat:
    def test_init(self, requests_mock:Mocker):
        test = build_gamecat(requests_mock)
        assert test.__dict__ == {"game":build_game(requests_mock), "category": build_category(requests_mock)}

    def test_keys(self, requests_mock:Mocker):
        test = build_gamecat(requests_mock)
        assert set(test.keys()) == {"level", "game","category", "release", "series"}


    def test_str(self, requests_mock:Mocker):
        test = build_gamecat(requests_mock)
        assert str(test) == "Super Mario Sunshine: Shrub Fo   Any% (No SSU) (150cc"

    def test_ids(self, requests_mock:Mocker):
        test = build_gamecat(requests_mock)
        assert test.ids() == ('game_id', 'level_id', 'category_id', [('subcat_id_t', 'selected_subcat')])

    def test_getitem(self, requests_mock:Mocker):
        test = build_gamecat(requests_mock)
        assert test["game"] == "Super Mario Sunshine"
        assert test["category"] == "Super Mario Sunshine: Shrub Forest Any% (No SSU) (150cc)"
