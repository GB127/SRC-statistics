from requests_mock.mocker import Mocker
from code_SRC.api import api


def test_update_dbs(requests_mock: Mocker):
    dbs = [
        "api.game_db",
        "api.system_db",
        "api.category_db",
        "api.level_db",
        "api.region_db",
        "api.sub_cat"
    ]
    api.system_db = {}
    link = "https://www.speedrun.com/api/v1/games/4d709l17?embed=categories,levels,variables,regions,platforms"
    returned_data = {
        "data": {
            "id": "4d709l17",
            "names": {"international": "The Legend of Zelda: The Wind Waker"},
            "released": 2002,
            "platforms": {"data": [{"id": "4p9z06rn", "name": "GameCube"}]},
            "regions": {
                "data": [
                    {
                        "id": "pr184lqn",
                        "name": "USA / NTSC",
                    },
                ]
            },
            "levels": {"data": [{"id": "ywep57dl", "name": "Dragon Roost Cavern"}]},
            "variables": {
                "data": [
                    {
                        "id": "0nw200nq",
                        "name": "Tingle Tuner",
                        "category": None,
                        "scope": {"type": "global"},
                        "mandatory": True,
                        "user-defined": False,
                        "obsoletes": True,
                        "values": {
                            "_note": "`choices` is deprecated, please use `values` instead",
                            "choices": {"gq79nvlp": "Tuner", "21gejnlz": "No Tuner"},
                            "values": {
                                "gq79nvlp": {"label": "Tuner"},
                                "21gejnlz": {"label": "No Tuner"},
                            },
                            "default": None,
                        },
                        "is-subcategory": True,
                    }
                ]
            },
            "categories": {
                "data": [
                    {
                        "id": "9d8x94w2",
                        "name": "Any%",
                        "variables": {
                            "data": [
                                {
                                    "id": "0nw200nq",
                                    "name": "Tingle Tuner",
                                    "category": None,
                                    "scope": {"type": "global"},
                                    "mandatory": True,
                                    "user-defined": False,
                                    "obsoletes": True,
                                    "values": {
                                        "_note": "`choices` is deprecated, please use `values` instead",
                                        "choices": {
                                            "gq79nvlp": "Tuner",
                                            "21gejnlz": "No Tuner",
                                        },
                                        "values": {
                                            "gq79nvlp": {"label": "Tuner"},
                                            "21gejnlz": {"label": "No Tuner"},
                                        },
                                        "default": None,
                                    },
                                    "is-subcategory": False,
                                    "links": [
                                        {
                                            "rel": "self",
                                            "uri": "https://www.speedrun.com/api/v1/variables/0nw200nq",
                                        },
                                        {
                                            "rel": "game",
                                            "uri": "https://www.speedrun.com/api/v1/games/4d709l17",
                                        },
                                    ],
                                }
                            ]
                        },
                    },
                ]
            },
        }
    }

    requests_mock.get(link, json=returned_data)
    api.update_db("4d709l17")

    for no, db in enumerate(
        [
            api.game_db,
            api.system_db,
            api.category_db,
            api.level_db,
            api.region_db,
            api.subcat_db
        ]
    ):
        assert db != {}, f"{dbs[no]} didn't get updated\n"


def test_user_id(requests_mock: Mocker):
    link = "https://www.speedrun.com/api/v1/users/niamek"
    returned_data = {
        "data": {
            "id": "x7qz6qq8",
            "names": {"international": "Niamek", "japanese": None},
            }
        }
    
    requests_mock.get(link, json=returned_data)
    assert api.user_id("niamek") == "x7qz6qq8"


def test_correct_data():
    api_callers = [
        api.game,
        api.system,
        api.category,
        api.level,
        api.region,
    ]
    ids = ["4d709l17", "4p9z06rn", "9d8x94w2", "ywep57dl", "pr184lqn"]
    attendus = [
        "Zelda: The Wind Waker",
        "GameCube",
        "Any%",
        "Dragon Roost Cavern",
        "USA / NTSC",
    ]
    for function, id, attendu in zip(api_callers, ids, attendus):
        assert function(id) == attendu
    api.sub_cat("0nw200nq", "gq79nvlp") == "Tuner"


def test_user_pbs(requests_mock: Mocker):
    returned_data = {
        "data": [
            {
                "place": 366,
                "run": {
                    "id": "7z037xoz",
                    "game": "j1l9qz1g",
                    "level": None,
                    "category": "z275w5k0",
                    "times": {"primary_t": 1401},
                    "system": {
                        "platform": "nzelreqp",
                        "emulated": False,
                        "region": "o316x197",
                    },
                    "values": {"p854r2vl": "5q85yy6q"},
                }
            }
        ]
    }

    link = "https://www.speedrun.com/api/v1/users/dx3r2qxl/personal-bests"
    requests_mock.get(link, json=returned_data)
    assert isinstance(api.user_pbs("dx3r2qxl"), list)


def test_user_runs(requests_mock: Mocker):
    returned_data = {
        "data": [
            {
                "id": "1zx46vqy",
                "game": "4d709l17",
                "level": None,
                "category": "z275r4k0",
                "videos": {
                    "links": [{"uri": "https://www.twitch.tv/koljai7/v/47191409"}]
                },
                "times": {
                    "primary_t": 15855,
                },
                "system": {
                    "platform": "4p9z06rn",
                    "emulated": False,
                    "region": "o316x197",
                },
                "values": {"0nw200nq": "gq79nvlp"}
            }
        ],
        "pagination": {"offset": 0, "max": 20, "size": 3, "links": []},
    }
    link = "https://www.speedrun.com/api/v1/runs?user=dx3r2qxl"
    requests_mock.get(link, json=returned_data)
    assert isinstance(api.user_runs("dx3r2qxl"), list)
