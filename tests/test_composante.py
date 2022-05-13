from code_SRC.composantes import Category, Game
from requests_mock.mocker import Mocker

def build_game(requests_mock:Mocker):
    game_data = {"data":{"id":"v1pxjz68","names":{"international":"Super Mario Sunshine","japanese":"\u30b9\u30fc\u30d1\u30fc\u30de\u30ea\u30aa\u30b5\u30f3\u30b7\u30e3\u30a4\u30f3","twitch":"Super Mario Sunshine"},"boostReceived":0,"boostDistinctDonors":0,"abbreviation":"sms","weblink":"https://www.speedrun.com/sms","discord":"https://discord.gg/jX38aXCv9y","released":2002,"release-date":"2002-07-19","ruleset":{"show-milliseconds":True,"require-verification":True,"require-video":False,"run-times":["realtime"],"default-time":"realtime","emulators-allowed":True},"romhack":False,"gametypes":[],"platforms":["4p9z06rn","v06dk3e4","7m6ylw9p"],"regions":["pr184lqn","e6lxy1dz","o316x197","p2g50lnk"],"genres":["qdnqkn8k","jp23ox26"],"engines":[],"developers":["xv6dvx62"],"publishers":["m0rvylrx"],"moderators":{"98r36381":"super-moderator","qj239pxk":"moderator","o8663m38":"moderator","kj9k3lr8":"moderator","48gk35pj":"moderator","zxzg570j":"moderator","jpre0408":"super-moderator","j2wyv4lj":"super-moderator"},"created":"2014-12-07T12:50:20Z","assets":{"logo":{"uri":"https://www.speedrun.com/themeasset/q8gvyq80/logo?v=045fe23"},"cover-tiny":{"uri":"https://www.speedrun.com/gameasset/v1pxjz68/cover?v=899a4c6"},"cover-small":{"uri":"https://www.speedrun.com/gameasset/v1pxjz68/cover?v=899a4c6"},"cover-medium":{"uri":"https://www.speedrun.com/gameasset/v1pxjz68/cover?v=899a4c6"},"cover-large":{"uri":"https://www.speedrun.com/gameasset/v1pxjz68/cover?v=899a4c6"},"icon":{"uri":"https://www.speedrun.com/themeasset/q8gvyq80/favicon?v=61d9059"},"trophy-1st":{"uri":"https://www.speedrun.com/themeasset/q8gvyq80/1st?v=8c2f559"},"trophy-2nd":{"uri":"https://www.speedrun.com/themeasset/q8gvyq80/2nd?v=3b81193"},"trophy-3rd":{"uri":"https://www.speedrun.com/themeasset/q8gvyq80/3rd?v=b0301cd"},"trophy-4th":{"uri":None},"background":{"uri":"https://www.speedrun.com/themeasset/q8gvyq80/background?v=cf0364f"},"foreground":{"uri":None}},"links":[{"rel":"self","uri":"https://www.speedrun.com/api/v1/games/v1pxjz68"},{"rel":"runs","uri":"https://www.speedrun.com/api/v1/runs?game=v1pxjz68"},{"rel":"levels","uri":"https://www.speedrun.com/api/v1/games/v1pxjz68/levels"},{"rel":"categories","uri":"https://www.speedrun.com/api/v1/games/v1pxjz68/categories"},{"rel":"variables","uri":"https://www.speedrun.com/api/v1/games/v1pxjz68/variables"},{"rel":"records","uri":"https://www.speedrun.com/api/v1/games/v1pxjz68/records"},{"rel":"series","uri":"https://www.speedrun.com/api/v1/series/rv7emz49"},{"rel":"derived-games","uri":"https://www.speedrun.com/api/v1/games/v1pxjz68/derived-games"},{"rel":"romhacks","uri":"https://www.speedrun.com/api/v1/games/v1pxjz68/derived-games"},{"rel":"leaderboard","uri":"https://www.speedrun.com/api/v1/leaderboards/v1pxjz68/category/n2y3r8do"}]}}
    series_data = {"data":{"id":"rv7emz49","names":{"international":"Super Mario","japanese":"\u30b9\u30fc\u30d1\u30fc\u30de\u30ea\u30aa"},"abbreviation":"mario","weblink":"https://www.speedrun.com/mario","discord":"","moderators":{},"created":None,"assets":{"logo":{"uri":"https://www.speedrun.com/images/logo.png"},"cover-tiny":{"uri":"https://www.speedrun.com/gameasset/kyd4og1e/cover?v=8f254bf"},"cover-small":{"uri":"https://www.speedrun.com/gameasset/kyd4og1e/cover?v=8f254bf"},"cover-medium":{"uri":"https://www.speedrun.com/gameasset/kyd4og1e/cover?v=8f254bf"},"cover-large":{"uri":"https://www.speedrun.com/gameasset/kyd4og1e/cover?v=8f254bf"},"icon":{"uri":"https://www.speedrun.com/images/1st.png"},"trophy-1st":{"uri":"https://www.speedrun.com/images/1st.png"},"trophy-2nd":{"uri":"https://www.speedrun.com/images/2nd.png"},"trophy-3rd":{"uri":"https://www.speedrun.com/images/3rd.png"},"trophy-4th":{"uri":None},"background":{"uri":None},"foreground":{"uri":None}},"links":[{"rel":"self","uri":"https://www.speedrun.com/api/v1/series/rv7emz49"},{"rel":"games","uri":"https://www.speedrun.com/api/v1/series/rv7emz49/games"}]}}
    level_data = {"data":{"id":"495ggmwp","name":"Shrub Forest","weblink":"https://www.speedrun.com/pokemon_rumble_world/Shrub_Forest","rules":"Normal Mode: Just go as fast as you can through the level.\r\n\r\nhard Mode: You must kill every Pokemon [Except the infinite re-spawning ones at the boss battle]\r\n\r\nYour time is the In game time.","links":[{"rel":"self","uri":"https://www.speedrun.com/api/v1/levels/495ggmwp"},{"rel":"game","uri":"https://www.speedrun.com/api/v1/games/v1p3yz68"},{"rel":"categories","uri":"https://www.speedrun.com/api/v1/levels/495ggmwp/categories"},{"rel":"variables","uri":"https://www.speedrun.com/api/v1/levels/495ggmwp/variables"},{"rel":"records","uri":"https://www.speedrun.com/api/v1/levels/495ggmwp/records"},{"rel":"runs","uri":"https://www.speedrun.com/api/v1/runs?level=495ggmwp"},{"rel":"leaderboard","uri":"https://www.speedrun.com/api/v1/leaderboards/v1p3yz68/level/495ggmwp/mkeg0926"}]}}
    requests_mock.get("https://www.speedrun.com/api/v1/series/rv7emz49", json=series_data)
    requests_mock.get("https://www.speedrun.com/api/v1/games/v1pxjz68", json=game_data)
    requests_mock.get("https://www.speedrun.com/api/v1/levels/495ggmwp", json=level_data)
    return Game("v1pxjz68", "495ggmwp")

def build_category(requests_mock:Mocker):
    category_data = {"data":{"id":"nxd1rk8q","name":"Any% (No SSU)","weblink":"https://www.speedrun.com/gtavc#Any_No_SSU","type":"per-game","rules":"__**TIMING**__\r\n\r\nTiming starts when the loading screen after starting a new game is gone, and ends when control is lost over Tommy Vercetti after killing Sonny on \u0027Keep Your Friends Close...\u0027\r\n\r\n__**ADDITIONAL RESTRICTIONS**__\r\n\r\n* [Script Stack Underflow](https://www.reddit.com/r/speedrun/comments/4vp5ui/wr_new_skip_found_in_vice_city_shaves_20_minutes/d60ugoe/) is banned from use in this category.","players":{"type":"exactly","value":1},"miscellaneous":False,"links":[{"rel":"self","uri":"https://www.speedrun.com/api/v1/categories/nxd1rk8q"},{"rel":"game","uri":"https://www.speedrun.com/api/v1/games/29d30dlp"},{"rel":"variables","uri":"https://www.speedrun.com/api/v1/categories/nxd1rk8q/variables"},{"rel":"records","uri":"https://www.speedrun.com/api/v1/categories/nxd1rk8q/records"},{"rel":"runs","uri":"https://www.speedrun.com/api/v1/runs?category=nxd1rk8q"},{"rel":"leaderboard","uri":"https://www.speedrun.com/api/v1/leaderboards/29d30dlp/category/nxd1rk8q"}]}}
    requests_mock.get("https://www.speedrun.com/api/v1/categories/nxd1rk8q", json=category_data)
    return Category("nxd1rk8q")



class Test_game:
    def test_init(self, requests_mock: Mocker):
        test = build_game(requests_mock)
        assert test.__dict__ == {'ids': ('v1pxjz68', '495ggmwp'),'level': 'Shrub Forest', "game":"Super Mario Sunshine", "release": 2002, "series":{"Super Mario"}}

    def test_str(self, requests_mock: Mocker):
        test = build_game(requests_mock)
        assert str(test) == f'{"Super Mario Sunshine: Shrub Forest":<40}'

    def test_operators(self, requests_mock: Mocker):
        test1 = build_game(requests_mock)
        test2 = build_game(requests_mock)

        assert test1 == test2
        test2.game = "Tomate"
        assert test1 != test2
        assert test1 <= test2


class Test_category:
    def test_init(self, requests_mock: Mocker):
        test = build_category(requests_mock)
        assert test.__dict__ == {"category" :"Any% (No SSU)", "ids":('nxd1rk8q')}
        raise NotImplementedError("Subcategories")

    def test_str(self, requests_mock: Mocker):
        test = build_category(requests_mock)
        assert str(test) == "Any% (No SSU)"
        raise NotImplementedError("Subcategories")
