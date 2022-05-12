from code_SRC.game import Game
from copy import copy

class Test_game:
    dicto = {"id":"v1pxjz68","names":{"international":"Super Mario Sunshine","japanese":"\u30b9\u30fc\u30d1\u30fc\u30de\u30ea\u30aa\u30b5\u30f3\u30b7\u30e3\u30a4\u30f3","twitch":"Super Mario Sunshine"},"boostReceived":0,"boostDistinctDonors":0,"abbreviation":"sms","weblink":"https://www.speedrun.com/sms","discord":"https://discord.gg/jX38aXCv9y","released":2002,"release-date":"2002-07-19","ruleset":{"show-milliseconds":True,"require-verification":True,"require-video":False,"run-times":["realtime"],"default-time":"realtime","emulators-allowed":True},"romhack":False,"gametypes":[],"platforms":["4p9z06rn","v06dk3e4","7m6ylw9p"],"regions":["pr184lqn","e6lxy1dz","o316x197","p2g50lnk"],"genres":["qdnqkn8k","jp23ox26"],"engines":[],"developers":["xv6dvx62"],"publishers":["m0rvylrx"],"moderators":{"98r36381":"super-moderator","qj239pxk":"moderator","o8663m38":"moderator","kj9k3lr8":"moderator","48gk35pj":"moderator","zxzg570j":"moderator","jpre0408":"super-moderator","j2wyv4lj":"super-moderator"},"created":"2014-12-07T12:50:20Z","assets":{"logo":{"uri":"https://www.speedrun.com/themeasset/q8gvyq80/logo?v=045fe23"},"cover-tiny":{"uri":"https://www.speedrun.com/gameasset/v1pxjz68/cover?v=899a4c6"},"cover-small":{"uri":"https://www.speedrun.com/gameasset/v1pxjz68/cover?v=899a4c6"},"cover-medium":{"uri":"https://www.speedrun.com/gameasset/v1pxjz68/cover?v=899a4c6"},"cover-large":{"uri":"https://www.speedrun.com/gameasset/v1pxjz68/cover?v=899a4c6"},"icon":{"uri":"https://www.speedrun.com/themeasset/q8gvyq80/favicon?v=61d9059"},"trophy-1st":{"uri":"https://www.speedrun.com/themeasset/q8gvyq80/1st?v=8c2f559"},"trophy-2nd":{"uri":"https://www.speedrun.com/themeasset/q8gvyq80/2nd?v=3b81193"},"trophy-3rd":{"uri":"https://www.speedrun.com/themeasset/q8gvyq80/3rd?v=b0301cd"},"trophy-4th":{"uri":None},"background":{"uri":"https://www.speedrun.com/themeasset/q8gvyq80/background?v=cf0364f"},"foreground":{"uri":None}},"links":[{"rel":"self","uri":"https://www.speedrun.com/api/v1/games/v1pxjz68"},{"rel":"runs","uri":"https://www.speedrun.com/api/v1/runs?game=v1pxjz68"},{"rel":"levels","uri":"https://www.speedrun.com/api/v1/games/v1pxjz68/levels"},{"rel":"categories","uri":"https://www.speedrun.com/api/v1/games/v1pxjz68/categories"},{"rel":"variables","uri":"https://www.speedrun.com/api/v1/games/v1pxjz68/variables"},{"rel":"records","uri":"https://www.speedrun.com/api/v1/games/v1pxjz68/records"},{"rel":"series","uri":"https://www.speedrun.com/api/v1/series/rv7emz49"},{"rel":"derived-games","uri":"https://www.speedrun.com/api/v1/games/v1pxjz68/derived-games"},{"rel":"romhacks","uri":"https://www.speedrun.com/api/v1/games/v1pxjz68/derived-games"},{"rel":"leaderboard","uri":"https://www.speedrun.com/api/v1/leaderboards/v1pxjz68/category/n2y3r8do"}]}
    def test_init(self):
        assert Game(Test_game.dicto).__dict__ == {"name":"Super Mario Sunshine", "release": 2002, "series":{"Super Mario"}}

    def test_str(self):
        test_classe = Game(Test_game.dicto)
        assert str(test_classe) == f'{"Super Mario Sunshine":<40}'

    def test_operators(self):
        test1 = Game(copy(Test_game.dicto))
        test2 = Game(copy(Test_game.dicto))
        test2.name = "Tomate"
        assert test1 != test2
        assert test1 <= test2