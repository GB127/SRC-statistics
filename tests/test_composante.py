from requests_mock.mocker import Mocker
from tests.class_builder import build_category, build_game

class Test_game:
    def test_init(self, requests_mock: Mocker):
        game = build_game(requests_mock)
        assert game.__dict__ == {'ids': ('v1pxjz68', '495ggmwp'),'level': 'Shrub Forest', "game":"Super Mario Sunshine", "release": 2002, "series":{"Super Mario"}}

    def test_str(self, requests_mock: Mocker):
        game = build_game(requests_mock)
        assert str(game) == f'{"Super Mario Sunshine: Shrub Forest":<40}'

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
        assert category.__dict__ == {"category" :"Any% (No SSU)", "ids":('nxd1rk8q')}
        raise NotImplementedError("Subcategories")

    def test_str(self, requests_mock: Mocker):
        category = build_category(requests_mock)
        assert str(category) == "Any% (No SSU)"
        raise NotImplementedError("Subcategories")
