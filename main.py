from speedruncompy import GetUserLeaderboard
from speedruncompy import GetGameLeaderboard, GetGameLeaderboard2


def get_user_infos(user_id="x7qz6qq8"):
    unwanted_fields = { "userProfile",
                        "user",
                        "users",
                        "regions",
                        "followedGameIds",
                        "challengeList",
                        "challengeRunList",
                       }
    data = GetUserLeaderboard("x7qz6qq8").perform_sync()  # I have no idea what this is.
    data = data.model_dump(exclude=unwanted_fields)
    return data

def get_lb(game_id, cat_id):
    test = GetGameLeaderboard2(game_id, cat_id, video=0).perform_sync()
    test = test.model_dump()
    test = test["runList"]
    test = [x["time"] for x in test]
    return test

# dict_items([('gameId', ), ('categoryId', 'w20p0zkn'), ('levelId', None), ('time', 651.0), ('platformId', 'jm95z9ol'), ('obsolete', False), ('place', 1865), ('valueIds', ['013zwgxq'])])