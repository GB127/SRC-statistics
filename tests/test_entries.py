from requests_mock.mocker import Mocker
from entries.base_entry import Base_Entry
from entries.one_run import Run
from entries.lb_entry import Rank
from entries.personal_best import PB
# from mock_examples.main import slow_dataset

class Test_run:
    testing_case = {
                "id": "1zx46vqy",
                "game": "4d709l17",
                "level": "ywep57dl",
                "category": "9d8x94w2",
                "times": {
                    "primary_t": 15855,
                },
                "system": {
                    "platform": "4p9z06rn",
                    "emulated": False,
                    "region": "pr184lqn",
                },
                "values": {"0nw200nq": "gq79nvlp"}
            }

    def test_init(self):
        Test_run.classe = Run(Test_run.testing_case)
        assert set(Test_run.classe.keys()) == {"game", "category", "time", "system", "emu", "level", "region"}

    def test_str(self):
        assert str(Test_run.classe) == "Game   Zelda: The Wind Wake   Dragon Roost Cavern    Any% (Tuner)                       4:24:15"
        Test_run.classe["level"] = None
        assert str(Test_run.classe) == "Game   Zelda: The Wind Wake   Any% (Tuner)                       4:24:15"

class Test_lb_entry:
    testing_case = {
                "place": 2,
                "run": {
                    "id": "7z037xoz",
                    "game": "4d709l17",
                    "level": None,
                    "category": "9d8x94w2",
                    "times": {"primary_t": 1401},
                    "system": {
                        "platform": "4p9z06rn",
                        "emulated": False,
                        "region": "pr184lqn",
                    },
                    "values": {"p854r2vl": "5q85yy6q"},
                },
            }
    def test_init(self):
        Test_lb_entry.classe = Rank(Test_lb_entry.testing_case, 1401 * 0.5)
        assert set(Test_lb_entry.classe.keys()) == {"place", "WR %", "delta WR", "time", "system", "emu", "region", "min/rk", "category", "game", "level", "WR time"}

    def test_str(self):
        assert str(Test_lb_entry.classe) == "  0:23:21   +0:11:40   (200.00%)   0:11:40"

# def test_mocking_class_method(mocker):
#     expected = 'xyz'

#     def mock_load(self):
#         return 'xyz'

#     mocker.patch(
#         # Dataset is in slow.py, but imported to main.py
#         'mock_examples.main.Dataset.load_data',
#         mock_load
#     )
#     actual = slow_dataset()
#     assert expected == actual


class Test_pb:
    pb_dict = {"place": 2,
                    "run": {
                        "id": "7z037xoz",
                        "game": "4d709l17",
                        "level": None,
                        "category": "9d8x94w2",
                        "times": {"primary_t": 1401 + 2},
                        "system": {
                            "platform": "4p9z06rn",
                            "emulated": False,
                            "region": "pr184lqn",
                        },
                        "values": {"0nw200nq": "gq79nvlp"}}}
    def test_init(self, requests_mock:Mocker):
        lb_data = {"data":{"runs":[{
                    "place": x + 1,
                    "run": {
                        "id": "7z037xoz",
                        "game": "4d709l17",
                        "level": None,
                        "category": "9d8x94w2",
                        "times": {"primary_t": 1401 + x},
                        "system": {
                            "platform": "4p9z06rn",
                            "emulated": False,
                            "region": "pr184lqn",
                        },
                        "values": {"p854r2vl": "5q85yy6q"},
                    }} for x in range(3)]}}
        link = "https://www.speedrun.com/api/v1/leaderboards/4d709l17/category/9d8x94w2?var-0nw200nq=gq79nvlp"
        requests_mock.get(link, json=lb_data)
        Test_pb.classe = PB(Test_pb.pb_dict)
        assert set(Test_pb.classe.keys()) == {"place","WR time", "WR %", "delta WR","game", "category", "time", "system", "emu", "level", "region", "leaderboard", "min/rk", "LB %"}


    def test_str(self):
        attendu =  "Game   Zelda: The Wind Wake   Any% (Tuner)             0:23:21    0:23:23 +0:00:02   (100.14%)      2/3     33.33%"
        assert str(Test_pb.classe) == attendu, str(Test_pb.classe)

class Test_base:
    def test_set_get(self):
        testing_case = Base_Entry()
        testing_case["a"] = 1
        assert testing_case["a"] == 1

    def test_eq(self):
        testing_case = Base_Entry()
        testing_case.__dict__ = {"a":1}
        testing_case2 = Base_Entry()
        testing_case2.__dict__ = {"a":1}
        assert testing_case == testing_case2

    def test_keys(self):
        testing_case = Base_Entry()
        testing_case["a"] = 1
        assert testing_case.keys() == {"a":1}.keys()
        assert testing_case.items() == {"a":1}.items()