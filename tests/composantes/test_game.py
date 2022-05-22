from requests_mock.mocker import Mocker
from tests.class_builder import build_game



class Test_game:
    def test_init(self, requests_mock: Mocker):
        game = build_game(requests_mock)
        assert game.__dict__ == {'ids': ('game_id', 'level_id'),'level': 'Shrub Forest', "game":"Super Mario Sunshine", "release": "2002", "series":{"Super Mario"}}

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

