liste = [1,2,3,4,5,6,7,9]

for id in range(len(liste)):
    for item in liste:
        if liste.index(item) == id:
            print(id, item)

for id, item in enumerate(liste):
    print(id, item)