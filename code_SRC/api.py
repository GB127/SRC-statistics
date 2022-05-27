from requests import get
import datetime

def requester(link):
    try:
        data = get(link).json()
        data["data"]
        return data
    except:
        raise BaseException(data)

class api:
    """api class to manage all requests. Stores data in a database.
        """
    URL = "https://www.speedrun.com/api/v1/"
    def leaderboard(game_id, level_id, category_id, subcat_ids):
        variables= ""
        if subcat_ids:
            variables = "&var-".join([f"{x}={y}" for x,y in subcat_ids])

        if level_id:
            req = requester(api.URL + f'leaderboards/{game_id}/level/{level_id}/{category_id}?var-{variables}')
            return [x["run"]["times"]["primary_t"] for x in req["data"]["runs"]]
        req = requester(api.URL + f'leaderboards/{game_id}/category/{category_id}?var-{variables}')
        return [x["run"]["times"]["primary_t"] for x in req["data"]["runs"]]

    @staticmethod
    def past_lb(released, game_id, level_id, category_id, subcat_ids):
        def request_lb(year):
            if level_id:
                req = requester(api.URL + f'leaderboards/{game_id}/level/{level_id}/{category_id}?var-{variables}&date={year}')
                return [x["run"]["times"]["primary_t"] for x in req["data"]["runs"]]
            req = requester(api.URL + f'leaderboards/{game_id}/category/{category_id}?var-{variables}&date={year}')
            return [x["run"]["times"]["primary_t"] for x in req["data"]["runs"]]

        variables= ""
        if subcat_ids:
            variables = "&var-".join([f"{x}={y}" for x,y in subcat_ids])
        date_filter = datetime.date.today()
        
        rankings = {}
        for new_year in range(date_filter.year, released, -1):
            this_year_ranking = request_lb(date_filter.isoformat())
            if this_year_ranking in rankings.values():
                continue
            elif this_year_ranking:
                rankings[new_year] = this_year_ranking
                date_filter = date_filter.replace(year=new_year -1)
            else: # No more leaderboard : lb is empty
                break
        return rankings
