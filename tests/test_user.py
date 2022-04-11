from attr import has
from code_SRC.api import api
from code_SRC.user import User
from requests_mock.mocker import Mocker


class Test_user:
    dicto_pbs = {
        "data": [
{
        "place": 2,
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
                        "values": {"0nw200nq": "gq79nvlp"},
        },
    },{
        "place": 2,
        "run": {
            "id": "7z037xoz",
            "game": "4d709l17",
            "level": "ywep57dl",
            "category": "9d8x94w2",
            "times": {"primary_t": 1401 + 2},
            "system": {
                "platform": "4p9z06rn",
                "emulated": False,
                "region": "pr184lqn",
            },
                        "values": {"0nw200nq": "gq79nvlp"},
        },
    }        ]
    }
    dicto_runs = {
        "data": [
{
        "id": "1zx46vqy",
        "game": "4d709l17",
        "level": None,
        "category": "9d8x94w2",
        "times": {
            "primary_t": 15855,
        },
        "system": {
            "platform": "4p9z06rn",
            "emulated": False,
            "region": "pr184lqn",
        },
                        "values": {"0nw200nq": "gq79nvlp"},
    },
    {
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
                        "values": {"0nw200nq": "gq79nvlp"},
    }

        ],
        "pagination": {"offset": 0, "max": 20, "size": 3, "links": []},
    }
    dicto_userid = {"data": {"id": "dx3r2qxl","names": {"international": "Niamek", "japanese": None}}}
    dicto_lb = {"data":{"runs":[{
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
                        "values": {"0nw200nq": "gq79nvlp"},
                    }} for x in range(3)]}}

    def set_links(self, requests_mock:Mocker):
        link = "https://www.speedrun.com/api/v1/users/niamek"
        requests_mock.get(link, json=Test_user.dicto_userid)
        link = "https://www.speedrun.com/api/v1/runs?user=dx3r2qxl"
        requests_mock.get(link, json=Test_user.dicto_runs)
        link = "https://www.speedrun.com/api/v1/users/dx3r2qxl/personal-bests"
        requests_mock.get(link, json=Test_user.dicto_pbs)
        link = "https://www.speedrun.com/api/v1/leaderboards/4d709l17/category/9d8x94w2?var-0nw200nq=gq79nvlp"
        requests_mock.get(link, json=Test_user.dicto_lb)
        link = "https://www.speedrun.com/api/v1/leaderboards/4d709l17/level/ywep57dl/9d8x94w2?var-0nw200nq=gq79nvlp"
        requests_mock.get(link, json=Test_user.dicto_lb)



    def test_init_all(self, requests_mock: Mocker):
        Test_user.set_links(self, requests_mock)
        #raise BaseException(api.subcat_db)
        Test_user.classe = User("niamek")
        for attribute in ["runs", "pbs", "runs_lvl", "pbs_lvl"]:
            assert hasattr(Test_user.classe, attribute), f'{attribute} not created'


    def test_init_nolvl(self, requests_mock: Mocker):
        def remove_lvls():
            Test_user.dicto_pbs["data"] = Test_user.dicto_pbs["data"][:-1]
            Test_user.dicto_runs["data"] = Test_user.dicto_runs["data"][:-1]
        def reset_dictos():
            pass
        remove_lvls()
        Test_user.set_links(self, requests_mock)
        #raise BaseException(api.subcat_db)
        for attribute in ["runs", "pbs"]:
            assert hasattr(User("niamek"), attribute), f'{attribute} not created'
        for attribute in ["runs_lvl", "pbs_lvl"]:
            assert not hasattr(User("niamek"), attribute), f'{attribute} created'


    def test_str(self):
        attendu = ( "Niamek\n"
                    "Full runs:\n"
                    "1 Runs     (4:24:15)  :   1 PBs    (0:23:23)\n"
                    "Individual level runs:\n"
                    "1 Runs     (4:24:15)  :   1 PBs    (0:23:23)"
                    )
        assert str(Test_user.classe) == attendu, str(Test_user.classe) + "\n"