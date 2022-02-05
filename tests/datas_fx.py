from ast import literal_eval

dicto_m = lambda filename : literal_eval(open(f"tests/datas/{filename}.txt", "r").read())

id_m = lambda filename : literal_eval(open(f"tests/datas/{filename}.txt", "r").read())["data"]["id"]


link_m = lambda filename : literal_eval(open(f"tests/datas/{filename}.txt", "r").read())["data"]["links"][0]["uri"]
