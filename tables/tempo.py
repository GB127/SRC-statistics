from itertools import chain

tempo = [{"allo", "patate"}, {"allo", "manam"}]
print(list(chain(*tempo)))
