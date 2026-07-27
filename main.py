from api import get_user_infos
from Speedrunner import Speedrunner
from entry import Entry

runs, pbs, games, categories = get_user_infos()
Entry.update_games(games)
Entry.update_categories(categories)
test = Speedrunner(runs, pbs)
print(test.pbs)