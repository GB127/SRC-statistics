from speedruncompy import GetUserLeaderboard
from speedruncompy import GetGameLeaderboard, GetGameLeaderboard2
from tqdm import tqdm

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

    runs = [    {
                "game" : x["gameId"],
                "time" : x["time"],
                "category": x["categoryId"]
                }
            for x in data["runs"] if x["time"]
        ]
    games = {x["id"]: x["name"] for x in data["games"]}
    categoreis = {x["id"] : x["name"] for x in data["categories"]}
    pbs = [{
                "game" : x["gameId"],
                "time" : x["time"],
                "category": x["categoryId"]
                }
            for x in data["runs"] if x["time"] and not x["obsolete"]
            ]


    return runs, pbs, games, categoreis



def get_lb(game_id, cat_id):
    test = GetGameLeaderboard2(game_id, cat_id, video=0)
    test3 = test.perform_all_sync().model_dump()

    test = test.perform_sync().model_dump()


    runs = test3["runList"]
    runs = [x["time"] for x in runs]
    # TQDm with leave=False may be working? Maybe not on pycharm. We'll see.
    #for x in range(1, test["pagination"]["pages"]):  # for now, use minimum!
    #for x in range(1, min(20, test["pagination"]["pages"])):  # for now, use minimum!
    #    test2 = GetGameLeaderboard2(game_id, cat_id, video=0, page=x).perform_sync()
    #    test2 = test2.model_dump()
    #    next_page = test2["runList"]
    #    next_page = [x["time"] for x in next_page]
    #    runs = runs + next_page
    return runs

if __name__ == "__main__":
    get_user_infos()
    #get_lb("om1m3625","w20p0zkn")
# dict_items([('gameId', ), ('categoryId', 'w20p0zkn'), ('levelId', None), ('time', 651.0), ('platformId', 'jm95z9ol'), ('obsolete', False), ('place', 1865), ('valueIds', ['013zwgxq'])])