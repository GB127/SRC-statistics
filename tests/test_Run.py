from code_SRC.entries import Run

test_case = {'id': 'z073gloy', 'weblink': 'https://www.speedrun.com/bhero/run/z073gloy', 'game': 'nd2eeqd0', 'level': None, 'category': 'zd3yzr2n', 'videos': {'links': [{'uri': 'https://www.twitch.tv/videos/1110770410'}]}, 'comment': 'Blind race. Stellar hitboxes right here.', 'status': {'status': 'verified', 'examiner': '98rpeqj1', 'verify-date': '2021-08-08T19:00:00Z'}, 'players': [{'rel': 'user', 'id': 'x7qz6qq8', 'uri': 'https://www.speedrun.com/api/v1/users/x7qz6qq8'}], 'date': '2021-08-06', 'submitted': '2021-08-07T05:35:16Z', 'times': {'primary': 'PT4H2M40S', 'primary_t': 14560, 'realtime': 'PT4H2M40S', 'realtime_t': 14560, 'realtime_noloads': None, 'realtime_noloads_t': 0, 'ingame': None, 'ingame_t': 0}, 'system': {'platform': 'nzelreqp', 'emulated': False, 'region': 'pr184lqn'}, 'splits': None, 'values': {}, 'links': [{'rel': 'self', 'uri': 'https://www.speedrun.com/api/v1/runs/z073gloy'}, {'rel': 'game', 'uri': 'https://www.speedrun.com/api/v1/games/nd2eeqd0'}, {'rel': 'category', 'uri': 'https://www.speedrun.com/api/v1/categories/zd3yzr2n'}, {'rel': 'platform', 'uri': 'https://www.speedrun.com/api/v1/platforms/nzelreqp'}, {'rel': 'region', 'uri': 'https://www.speedrun.com/api/v1/regions/pr184lqn'}, {'rel': 'examiner', 'uri': 'https://www.speedrun.com/api/v1/users/98rpeqj1'}]}

def test_Run_attributes():
    for attribute in ["game", "system", "category", "date", "time", "emu", "region"]:
        assert hasattr(test_case, attribute), f'{attribute} not created'

def test_Run_init_game():
    assert Run(test_case)["game"] == "Bomberman Hero"

def test_Run_init_system():
    assert Run(test_case)["system"] == "Wii VC"

def test_Run_init_categ():
    assert Run(test_case)["category"] == "Any %"

def test_Run_init_date():
    assert Run(test_case)["date"] == "2021-08-06"

def test_Run_init_time():
    assert Run(test_case)["time"] == 14560

def test_Run_init_emu():
    assert Run(test_case)["emu"] == False

def test_Run_init_region():
    assert Run(test_case)["region"] == "US"


def test_Run_add_time():
    somme = Run(test_case) + Run(test_case)
    assert Run(test_case)["time"] * 2 == somme["time"]

def test_Run_add_game():
    somme = Run(test_case) + Run(test_case)
    assert Run(test_case)["game"] == somme["game"]

def test_Run_div_time():
    divide = Run(test_case) / 2
    assert Run(test_case)["time"] / 2 == divide["time"]
