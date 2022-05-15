from code_SRC.composantes import Time
from requests_mock.mocker import Mocker
from tests.class_builder import build_category, build_game, build_gamecat, build_system

class Test_game:
    def test_init(self, requests_mock: Mocker):
        game = build_game(requests_mock)
        assert game.__dict__ == {'ids': ('game_id', 'level_id'),'level': 'Shrub Forest', "game":"Super Mario Sunshine", "release": 2002, "series":{"Super Mario"}}

    def test_keys(self, requests_mock:Mocker):
        test = build_game(requests_mock)
        assert set(test.keys()) == {"level", "game", "release", "series"}

    def test_getitem(self, requests_mock:Mocker):
        game = build_game(requests_mock)
        assert game["level"] == "Shrub Forest"

    def test_str(self, requests_mock: Mocker):
        game = build_game(requests_mock)
        assert str(game) == f'{"Super Mario Sunshine: Shrub Forest"}'

    def test_operators(self, requests_mock: Mocker):
        game1 = build_game(requests_mock)
        game2 = build_game(requests_mock)

        assert game1 == game2
        game2.game = "Tomate"
        assert game1 != game2
        assert game1 <= game2

class Test_category:
    def test_init(self, requests_mock: Mocker):
        category = build_category(requests_mock)
        assert category.__dict__ == {"category" :"Any% (No SSU)", 'ids': ('category_id', [('subcat_id_t', 'selected_subcat')]), "subcategory":["150cc"]}

    def test_getitem(self, requests_mock:Mocker):
        category = build_category(requests_mock)
        assert category["subcategory"] == ["150cc"]

    def test_keys(self, requests_mock:Mocker):
        test = build_category(requests_mock)
        assert set(test.keys()) == {"category", "subcategory"}


    def test_str(self, requests_mock: Mocker):
        category = build_category(requests_mock)
        assert str(category) == "Any% (No SSU) (150cc)"

class Test_gamecat:
    def test_init(self, requests_mock:Mocker):
        test = build_gamecat(requests_mock)
        assert test.__dict__ == {"game":build_game(requests_mock), "category": build_category(requests_mock)}

    def test_keys(self, requests_mock:Mocker):
        test = build_gamecat(requests_mock)
        assert set(test.keys()) == {"level", "game","category", "subcategory", "release", "series"}


    def test_str(self, requests_mock:Mocker):
        test = build_gamecat(requests_mock)
        assert str(test) == "Super Mario Sunshine: Shrub Fo   Any% (No SSU) (150cc"

    def test_ids(self, requests_mock:Mocker):
        test = build_gamecat(requests_mock)
        assert test.ids() == ('game_id', 'level_id', 'category_id', [('subcat_id_t', 'selected_subcat')])

    def test_getitem(self, requests_mock:Mocker):
        test = build_gamecat(requests_mock)
        assert test["subcategory"] == ["150cc"]
        assert test["level"] == "Shrub Forest"


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

class Test_time:
    def test_init(self):
        assert Time(4).__dict__ == {"seconds":4}

    def test_str(self):
        assert str(Time(500000)) == "138:53:20"

    def test_operators(self):
        assert Time(1) == Time(1)
        assert Time(1) + Time(2) == Time(3)
        assert Time(3) - Time(2) == Time(1)
        assert Time(1) <= Time(2)
        assert Time(2) / 2 == Time(1)
        assert Time(10) / Time(2) == Time(10/2)