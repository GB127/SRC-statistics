from entries.pb_entry import PB
from tables.pbs import Table_pb
from entries.run_entry import Run
from tests.datas_fx import dicto_m, fill_db


def liste_runs():
    liste = []
    for _ in range(5):
        liste.append(dicto_m("pb")["data"])
    return liste
