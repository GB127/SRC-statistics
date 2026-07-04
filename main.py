from speedruncompy import GetUserLeaderboard

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