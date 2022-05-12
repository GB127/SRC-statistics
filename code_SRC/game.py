class Game:
    def __init__(self, dicto):
        self.name = dicto["names"]["international"]
        self.release = dicto["released"]

    def __str__(self):
        return f'{self.name:<40}'
    
    def __eq__(self, other):
        return self.name == other.name

    def __le__(self, other):
        return self.name <= other.name