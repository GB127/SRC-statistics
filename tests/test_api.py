from code_SRC.api import api
from requests_mock.mocker import Mocker
from tests.class_builder import req_mocker


def test_nordanix():
    nordanix_id = api.user_id("nordanix")
    nordanix = api.user_runs(nordanix_id)
    assert len(nordanix) == 3765

class Test_api:
    def test_user_pbs(self, requests_mock:Mocker):
        req_mocker(requests_mock)
        for run in api.user_pbs("user_id"):
            for clé in ["place", "run"]:
                assert clé in run
            for clé in ["game", "category", "times", "system", "values", "level", "date", "status"]:
                    assert clé in run["run"]

    def test_system(self, requests_mock:Mocker):
        req_mocker(requests_mock)
        assert api.system("system_id") == "Nintendo Entertainment System"
        assert not api.system(None)

    def test_level(self, requests_mock:Mocker):
        req_mocker(requests_mock)
        assert api.level("level_id") == "Shrub Forest"

    def test_category(self, requests_mock:Mocker):
        req_mocker(requests_mock)
        assert api.category("category_id") == "Any% (No SSU)"

    def test_subcategory(self, requests_mock:Mocker):
        req_mocker(requests_mock)
        assert api.subcategory(('subcat_id_t', 'selected_subcat')) == "150cc"
        assert not api.subcategory( ('subcat_id_f', 'selected_subcat'))

    def test_leaderboard(self, requests_mock:Mocker):
        req_mocker(requests_mock)
        assert api.leaderboard("game_id",None, "category_id", [("subcat_id_t", "selected_subcat")]) == list(range(5422,5432))
        assert api.leaderboard("game_id","level_id", "category_id", [("subcat_id_t", "selected_subcat")]) == list(range(5422,5432))

    def test_user_id(self, requests_mock:Mocker):
        req_mocker(requests_mock)
        assert api.user_id("username") == "user_id"

    def test_game(self, requests_mock:Mocker):
        req_mocker(requests_mock)
        assert api.game("game_id") == ("Super Mario Sunshine", 2002, {"Super Mario"})

    def test_user_runs(self, requests_mock:Mocker):
        req_mocker(requests_mock)
        for run in api.user_runs("user_id"):
            for clé in ["game", "category", "times", "system", "values", "level", "date", "status"]:
                    assert clé in run

    def test_past_lb(self, requests_mock:Mocker):
        # NOTE : I don't know why my requests still works even if I did not defined a link. Only the data type are validated.
        req_mocker(requests_mock)
        for year, ranking in api.past_lb(2002, "game_id", "level_id", "category_id", [("subcat_id_t", "selected_subcat")]).items():
            assert isinstance(year, int) and isinstance(ranking, list)
            assert all([isinstance(x, int) for x in ranking])